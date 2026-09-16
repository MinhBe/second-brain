"""One HTTP transport for every resolver/provider, plus the PDF fetch policy (UA retry, SSL retry, HTML follow,
optional curl_cffi browser impersonation)."""

import json
import ssl
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Any, Callable, Dict, List, Optional, Tuple

from lib.unpaywall import is_pdf, maybe_extract_pdf_url_from_html


@dataclass
class HttpResponse:
    status: int
    data: bytes
    content_type: str
    final_url: str


@dataclass
class HttpPolicy:
    user_agent: str
    alt_user_agent: str
    contact_email: str
    timeout: int = 45
    retry_alt_ua_on_403: bool = True
    ssl_retry_unverified: bool = True
    follow_html_pdf_link: bool = True
    impersonate_on_403: bool = True
    challenge_markers: Tuple[str, ...] = ("challenge", "verify you are", "just a moment", "captcha", "enable javascript")
    challenge_max_bytes: int = 20000

    def ua(self) -> str:
        return self.user_agent.replace("{email}", self.contact_email)


def looks_like_challenge(data: bytes, policy: HttpPolicy) -> bool:
    """A small HTML page carrying a bot-check marker is a JavaScript challenge only a real browser can pass."""
    if len(data) > policy.challenge_max_bytes:
        return False
    text = data.decode("utf-8", "ignore").lower()
    return any(marker.lower() in text for marker in policy.challenge_markers)


@dataclass
class FetchResult:
    ok: bool
    data: bytes = b""
    final_url: str = ""
    error: Optional[str] = None
    error_class: str = "none"
    warnings: List[str] = field(default_factory=list)


HttpGet = Callable[[str, Dict[str, str], int, bool], HttpResponse]


def urllib_get(url: str, headers: Dict[str, str], timeout: int, verify_ssl: bool = True) -> HttpResponse:
    context = None if verify_ssl else ssl._create_unverified_context()  # noqa: SLF001
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout, context=context) as resp:
        data = resp.read()
        content_type = resp.headers.get_content_type() if resp.headers else ""
        return HttpResponse(status=resp.status, data=data, content_type=content_type or "", final_url=resp.geturl())


@lru_cache(maxsize=1)
def has_curl_cffi() -> bool:
    try:
        import curl_cffi.requests  # noqa: F401
    except Exception:  # noqa: BLE001
        return False
    return True


def curl_cffi_get(url: str, headers: Dict[str, str], timeout: int, verify_ssl: bool = True) -> HttpResponse:
    """Optional transport: real browser TLS fingerprint via curl_cffi (only used when installed)."""
    from curl_cffi import requests as creq

    resp = creq.get(url, headers={k: v for k, v in headers.items() if k != "User-Agent"}, timeout=timeout, verify=verify_ssl,
                    impersonate="chrome", allow_redirects=True)
    if resp.status_code >= 400:
        raise urllib.error.HTTPError(url, resp.status_code, f"http {resp.status_code}", {}, None)  # type: ignore[arg-type]
    ct = (resp.headers.get("content-type") or "").split(";")[0].strip()
    return HttpResponse(status=resp.status_code, data=resp.content, content_type=ct, final_url=str(resp.url))


def is_ssl_verify_error(exc: BaseException) -> bool:
    if isinstance(exc, ssl.SSLCertVerificationError):
        return True
    reason = getattr(exc, "reason", None)
    if isinstance(reason, ssl.SSLCertVerificationError):
        return True
    return "CERTIFICATE_VERIFY_FAILED" in str(exc)


def classify_exception(exc: BaseException) -> Tuple[str, str]:
    """Map a transport exception to (failure_class, short message)."""
    if is_ssl_verify_error(exc):
        return "ssl_error", "ssl_certificate_verify_failed"
    if isinstance(exc, urllib.error.HTTPError):
        if exc.code == 403:
            return "blocked_403", "http_403"
        if exc.code in (404, 410):
            return "not_found", f"http_{exc.code}"
        return "network", f"http_{exc.code}"
    return "network", f"{type(exc).__name__}: {str(exc)[:120]}"


def _headers(policy: HttpPolicy, accept: str, ua: Optional[str] = None) -> Dict[str, str]:
    return {"User-Agent": ua or policy.ua(), "Accept": accept, "From": policy.contact_email}


def get_json(url: str, policy: HttpPolicy, http_get: Optional[HttpGet] = None, timeout: Optional[int] = None) -> Dict[str, Any]:
    http_get = http_get or urllib_get
    resp = http_get(url, _headers(policy, "application/json"), timeout or policy.timeout, True)
    return json.loads(resp.data.decode("utf-8", "ignore"))


def _is_403(exc: BaseException) -> bool:
    return isinstance(exc, urllib.error.HTTPError) and exc.code == 403


def _get_with_retries(
    url: str, policy: HttpPolicy, http_get: HttpGet, warnings: List[str], curl_get: Optional[HttpGet]
) -> Tuple[Optional[HttpResponse], Optional[BaseException]]:
    accept = "application/pdf, text/html;q=0.9, */*;q=0.8"
    try:
        return http_get(url, _headers(policy, accept), policy.timeout, True), None
    except Exception as exc:  # noqa: BLE001
        last = exc
    if _is_403(last) and policy.retry_alt_ua_on_403:
        try:
            return http_get(url, _headers(policy, accept, policy.alt_user_agent), policy.timeout, True), None
        except Exception as exc:  # noqa: BLE001
            last = exc
    if _is_403(last) and policy.impersonate_on_403 and curl_get is not None:
        try:
            resp = curl_get(url, _headers(policy, accept, policy.alt_user_agent), policy.timeout, True)
            warnings.append("impersonated_client")
            return resp, None
        except Exception as exc:  # noqa: BLE001
            last = exc
    if is_ssl_verify_error(last) and policy.ssl_retry_unverified:
        try:
            resp = http_get(url, _headers(policy, accept), policy.timeout, False)
            warnings.append("ssl_unverified")
            return resp, None
        except Exception as exc:  # noqa: BLE001
            last = exc
    return None, last


def fetch_pdf(url: str, policy: HttpPolicy, http_get: Optional[HttpGet] = None, curl_get: Optional[HttpGet] = None) -> FetchResult:
    """Fetch one candidate URL and return PDF bytes, following one HTML -> pdf-link hop."""
    http_get = http_get or urllib_get
    if curl_get is None and http_get is urllib_get and has_curl_cffi():
        curl_get = curl_cffi_get
    warnings: List[str] = []
    resp, exc = _get_with_retries(url, policy, http_get, warnings, curl_get)
    if resp is None:
        cls, msg = classify_exception(exc)
        return FetchResult(False, final_url=url, error=msg, error_class=cls, warnings=warnings)
    if is_pdf(resp.data, resp.content_type):
        return FetchResult(True, data=resp.data, final_url=resp.final_url, warnings=warnings)
    if "html" not in resp.content_type.lower():
        return FetchResult(False, final_url=resp.final_url, error=f"non_pdf_content_type: {resp.content_type}", error_class="invalid_pdf", warnings=warnings)
    if looks_like_challenge(resp.data, policy):
        return FetchResult(False, final_url=resp.final_url, error="js_challenge_page", error_class="blocked_challenge", warnings=warnings)
    if not policy.follow_html_pdf_link:
        return FetchResult(False, final_url=resp.final_url, error="html_response", error_class="invalid_pdf", warnings=warnings)
    discovered = maybe_extract_pdf_url_from_html(resp.data.decode("utf-8", "ignore"))
    if not discovered:
        return FetchResult(False, final_url=resp.final_url, error="html_without_pdf_link", error_class="invalid_pdf", warnings=warnings)
    next_url = urllib.parse.urljoin(resp.final_url, discovered)
    resp2, exc2 = _get_with_retries(next_url, policy, http_get, warnings, curl_get)
    if resp2 is None:
        cls, msg = classify_exception(exc2)
        return FetchResult(False, final_url=next_url, error=f"followup_{msg}", error_class=cls, warnings=warnings)
    if is_pdf(resp2.data, resp2.content_type):
        return FetchResult(True, data=resp2.data, final_url=resp2.final_url, warnings=warnings)
    if "html" in resp2.content_type.lower() and looks_like_challenge(resp2.data, policy):
        return FetchResult(False, final_url=resp2.final_url, error="followup_js_challenge_page", error_class="blocked_challenge", warnings=warnings)
    return FetchResult(False, final_url=resp2.final_url, error=f"followup_non_pdf_content_type: {resp2.content_type}", error_class="invalid_pdf", warnings=warnings)
