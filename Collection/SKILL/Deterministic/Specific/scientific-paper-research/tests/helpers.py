"""Shared offline fakes and fixture loaders for the test suite."""

import json
import re
import urllib.error
from datetime import date
from pathlib import Path
from typing import Any, Callable, Dict, List, Tuple

from lib.http import HttpResponse

FIXTURES = Path(__file__).resolve().parent / "fixtures"
TODAY = date(2026, 9, 11)
PDF_BYTES = b"%PDF-1.4\n" + b"0" * 3000
HTML_WITH_LINK = b'<html><head><meta name="citation_pdf_url" content="https://example.org/pdf/from-html.pdf"></head></html>'
HTML_NO_LINK = b"<html><body>Article landing page without any PDF link.</body></html>"


def fixture_json(rel: str) -> Any:
    return json.loads((FIXTURES / rel).read_text(encoding="utf-8"))


def request(name: str) -> Dict[str, Any]:
    return fixture_json(f"requests/{name}.json")


def scopus_fake(**kwargs: Any) -> Dict[str, Any]:
    """Return the canned Scopus payload regardless of query; honours count so paging terminates."""
    payload = fixture_json("scopus_response.json")
    entries = payload["search-results"]["entry"]
    start = int(kwargs.get("start", 0))
    count = int(kwargs.get("count", len(entries)))
    payload["search-results"]["entry"] = entries[start:start + count]
    return payload


def http_error(url: str, code: int) -> urllib.error.HTTPError:
    return urllib.error.HTTPError(url, code, f"http {code}", {}, None)  # type: ignore[arg-type]


def ssl_error() -> urllib.error.URLError:
    import ssl

    return urllib.error.URLError(ssl.SSLCertVerificationError("certificate verify failed: unable to get local issuer"))


def json_response(url: str, payload: Any) -> HttpResponse:
    return HttpResponse(200, json.dumps(payload).encode("utf-8"), "application/json", url)


def pdf_response(url: str) -> HttpResponse:
    return HttpResponse(200, PDF_BYTES, "application/pdf", url)


Route = Tuple[str, Any]  # (regex, HttpResponse | Exception | callable(url, headers, verify_ssl))


def http_fake_factory(routes: List[Route]) -> Callable:
    """Route URLs by regex. Records every call as (url, user_agent, verify_ssl) on .calls."""
    compiled = [(re.compile(p), r) for p, r in routes]

    def http_get(url: str, headers: Dict[str, str], timeout: int, verify_ssl: bool = True) -> HttpResponse:
        http_get.calls.append((url, headers.get("User-Agent", ""), verify_ssl))
        for rx, responder in compiled:
            if rx.search(url):
                if callable(responder) and not isinstance(responder, HttpResponse):
                    out = responder(url, headers, verify_ssl)
                    if isinstance(out, BaseException):
                        raise out
                    return out
                if isinstance(responder, BaseException):
                    raise responder
                if isinstance(responder, HttpResponse):
                    return HttpResponse(responder.status, responder.data, responder.content_type, responder.final_url or url)
                return json_response(url, responder)
        raise http_error(url, 404)

    http_get.calls = []  # type: ignore[attr-defined]
    return http_get


def unpaywall_record(doi: str, is_oa: bool = True, pdf_url: str = "https://example.org/pdf/paper.pdf", title: str = "Alpha Paper") -> Dict[str, Any]:
    rec = {"doi": doi, "title": title, "is_oa": is_oa, "doi_url": f"https://doi.org/{doi}", "best_oa_location": None, "oa_locations": []}
    if is_oa:
        rec["best_oa_location"] = {"url_for_pdf": pdf_url, "url": pdf_url, "url_for_landing_page": "https://example.org/landing"}
        rec["oa_locations"] = [rec["best_oa_location"]]
    return rec


def default_routes(downloadable=("10.1000/aaa",)) -> List[Route]:
    """Unpaywall knows 10.1000/aaa (OA -> PDF) and 10.1000/bbb (not OA); everything else 404s."""
    def unpaywall(url, headers, verify_ssl):
        doi = url.split("/v2/")[1].split("?")[0].replace("%2F", "/")
        if doi.lower() in {d.lower() for d in downloadable}:
            return json_response(url, unpaywall_record(doi))
        if doi.lower() == "10.1000/bbb":
            return json_response(url, unpaywall_record(doi, is_oa=False, title="Beta Paper"))
        return http_error(url, 404)

    return [
        (r"api\.unpaywall\.org/v2/", unpaywall),
        (r"europepmc/webservices", {"resultList": {"result": []}}),
        (r"api\.openalex\.org/works/", http_error("openalex", 404)),
        (r"example\.org/pdf/", pdf_response("https://example.org/pdf/paper.pdf")),
    ]


def scihub_fake_factory(success_dois=()):
    wanted = {d.lower() for d in success_dois}

    def scihub(doi, outdir, filename_base, fallback):
        if doi.lower() in wanted:
            path = Path(outdir) / f"{filename_base}.pdf"
            path.write_bytes(PDF_BYTES)
            return True, str(path), "https://sci-hub.example/x.pdf", None
        return False, None, None, "scihub_cli_not_found"

    return scihub


def fake_extract_factory(text: str):
    from lib.pdf_text import PageText

    def fake_extract(path, ocr_mode, ocr_lang):
        half = len(text) // 2
        return [PageText(1, text[:half]), PageText(2, text[half:])], 2, "fake"

    return fake_extract
