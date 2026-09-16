"""Chain-driven acquisition: arxiv_direct -> unpaywall -> europe_pmc -> openalex -> scihub_fallback -> metadata_only.

The chain order comes from config/acquisition.yaml and is never reordered at runtime.
"""

import hashlib
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from lib.config import load_yaml
from lib.http import HttpGet, HttpPolicy, fetch_pdf
from lib.manifest import load_manifest, lookup, record, save_manifest
from lib.resolvers import RESOLVERS, ResolveContext, expand_candidates, manual_urls
from lib.unpaywall import FallbackConfig, attempt_scihub_fallback, resolve_scihub_command, safe_filename, unique_path

ScihubFn = Callable[..., Any]
FETCH_CLASSES = ("blocked_403", "blocked_challenge", "ssl_error", "invalid_pdf", "network")
PREPRINT_SUFFIX = "_preprint"


def build_fallback_config(email: Optional[str], cfg: Optional[Dict[str, Any]] = None) -> FallbackConfig:
    cfg = cfg if cfg is not None else load_yaml("acquisition")
    sh = cfg["scihub_fallback"]
    mode = sh.get("mode", "off")
    command, setup_error = (None, None)
    if mode in ("auto", "force"):
        command, setup_error = resolve_scihub_command(sh.get("command_override"))
    return FallbackConfig(
        mode=mode,
        command=command,
        email=email,
        timeout=max(60, int(sh.get("timeout_s", 180))),
        setup_error=setup_error,
        extra_args=list(sh.get("extra_args") or []),
        timeout_divisor=int(sh.get("timeout_divisor", 3)),
    )


def build_http_policy(cfg: Dict[str, Any], contact_email: str, timeout: int) -> HttpPolicy:
    h = cfg["http"]
    return HttpPolicy(
        user_agent=h["user_agent"],
        alt_user_agent=h.get("alt_user_agent", ""),
        contact_email=contact_email,
        timeout=timeout,
        retry_alt_ua_on_403=bool(h.get("retry_alt_ua_on_403", True)),
        ssl_retry_unverified=bool((h.get("ssl") or {}).get("retry_unverified", True)),
        follow_html_pdf_link=bool(h.get("follow_html_pdf_link", True)),
        impersonate_on_403=bool(h.get("impersonate_on_403", True)),
        challenge_markers=tuple(h.get("challenge_markers") or ("challenge", "verify you are", "just a moment", "captcha", "enable javascript")),
        challenge_max_bytes=int(h.get("challenge_max_bytes", 20000)),
    )


def verify_pdf(path: Optional[str], cfg: Dict[str, Any]) -> Dict[str, Any]:
    """Return {ok, sha256, error} for a downloaded file."""
    if not path:
        return {"ok": False, "sha256": None, "error": "no_path"}
    p = Path(path)
    if not p.is_file():
        return {"ok": False, "sha256": None, "error": "file_missing"}
    data = p.read_bytes()
    v = cfg["verify"]
    if v.get("require_pdf_magic", True) and not data.startswith(b"%PDF"):
        return {"ok": False, "sha256": None, "error": "not_a_pdf"}
    if len(data) < int(v.get("min_bytes", 0)):
        return {"ok": False, "sha256": None, "error": "file_too_small"}
    digest = hashlib.sha256(data).hexdigest() if v.get("compute_sha256", True) else None
    return {"ok": True, "sha256": digest, "error": None}


def classify_failure(attempts: List[Dict[str, Any]], meta: Dict[str, Any], cfg: Dict[str, Any]) -> str:
    seen = set()
    for a in attempts:
        for cls in a.get("error_classes") or []:
            seen.add(cls)
    for cls in FETCH_CLASSES:
        if cls in seen:
            return cls
    if meta.get("is_oa") is False:
        return "subscription_only"
    looked_up = [a["resolver"] for a in attempts if a["resolver"] in ("unpaywall", "openalex") and a["outcome"] != "skipped"]
    if looked_up and all(name in meta.get("lookup_404", []) for name in looked_up):
        return "not_found"
    return "no_oa"


def _base_name(doi: str, title: Optional[str]) -> str:
    """File stem this run uses: title when known, else the DOI. Also the name a manual download must use."""
    doi_name = safe_filename(doi.replace("/", "_"), "paper")
    return safe_filename(title, doi_name) if title else doi_name


def _adopt_existing(doi: str, title: Optional[str], out: Path, cfg: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """A verified PDF already saved under the name this run would use (e.g. from an older run) counts as downloaded."""
    names = [safe_filename(doi.replace("/", "_"), "paper")]
    if title:
        names.insert(0, _base_name(doi, title))
    for name in names:
        candidate = out / f"{name}.pdf"
        if candidate.is_file():
            check = verify_pdf(str(candidate), cfg)
            if check["ok"]:
                return {"path": str(candidate), "sha256": check["sha256"]}
    return None


def _new_item(doi: str) -> Dict[str, Any]:
    return {
        "doi": doi, "status": "failed", "method": None, "path": None, "expected_filename": None, "sha256": None, "title": None, "is_oa": None,
        "full_text_available": False, "evidence_level": "none", "version": None, "chain_attempted": [], "attempts": [],
        "failure_class": "none", "warnings": [], "manual_urls": [], "error": None,
    }


def _finish_downloaded(item: Dict[str, Any], method: str, path: str, sha: Optional[str], version: str = "published") -> Dict[str, Any]:
    item.update(status="downloaded", method=method, path=path, expected_filename=Path(path).name, sha256=sha,
                full_text_available=True, evidence_level="full_text", version=version, error=None)
    return item


def acquire_one(
    doi: str,
    out: Path,
    ctx: ResolveContext,
    fallback: FallbackConfig,
    cfg: Dict[str, Any],
    scihub_fn: ScihubFn,
    manifest: Dict[str, Any],
) -> Dict[str, Any]:
    item = _new_item(doi)
    cached = lookup(manifest, doi, cfg) if cfg["manifest"].get("enabled", True) else None
    if cached:
        item.update(title=cached.get("title"), chain_attempted=["cache"])
        return _finish_downloaded(item, "cache", cached["path"], cached.get("sha256"), cached.get("version") or "published")

    chain = list(cfg["chain"])
    if fallback.mode == "force":
        chain = [c for c in chain if c in ("scihub_fallback", "metadata_only")]
    last_error: Optional[str] = None

    for name in chain:
        attempt: Dict[str, Any] = {"resolver": name, "candidates": [], "outcome": "skipped", "error": None}
        item["chain_attempted"].append(name)

        if name == "metadata_only":
            attempt["outcome"] = "failed"
            item["attempts"].append(attempt)
            break

        if name == "scihub_fallback":
            if fallback.mode == "off":
                attempt["error"] = "disabled"
                item["attempts"].append(attempt)
                continue
            base = _base_name(doi, ctx.meta.get("title"))
            ok, path, resolved, err = scihub_fn(doi, out, base, fallback)
            if ok:
                check = verify_pdf(path, cfg)
                if check["ok"]:
                    attempt.update(outcome="downloaded", candidates=[resolved] if resolved else [])
                    item["attempts"].append(attempt)
                    item["title"] = ctx.meta.get("title")
                    item["is_oa"] = ctx.meta.get("is_oa")
                    _finish_downloaded(item, "scihub_fallback", path, check["sha256"])
                    record(manifest, item)
                    return item
                err = f"verify_failed: {check['error']}"
            attempt.update(outcome="failed", error=(err or "")[:240] or None)
            attempt["error_classes"] = []
            item["attempts"].append(attempt)
            continue

        resolver = RESOLVERS[name]
        candidates = [u for u in expand_candidates(resolver(doi, ctx), ctx) if u not in ctx.tried]
        if name == "unpaywall" and "unpaywall:no_email" in ctx.meta["skipped"]:
            attempt["error"] = "no_unpaywall_email"
            if "no_unpaywall_email" not in item["warnings"]:
                item["warnings"].append("no_unpaywall_email")
            item["attempts"].append(attempt)
            continue
        if not candidates:
            attempt["outcome"] = "no_candidates"
            attempt["error"] = ctx.meta["lookup_errors"].get(name)
            item["attempts"].append(attempt)
            continue

        attempt["candidates"] = candidates
        classes: List[str] = []
        existing = _adopt_existing(doi, ctx.meta.get("title"), out, cfg)
        if existing:
            attempt.update(outcome="downloaded", candidates=[])
            item["attempts"].append(attempt)
            item["title"] = ctx.meta.get("title")
            item["is_oa"] = ctx.meta.get("is_oa")
            _finish_downloaded(item, "cache", existing["path"], existing["sha256"])
            record(manifest, item)
            return item
        for url in candidates:
            ctx.tried.add(url)
            res = fetch_pdf(url, ctx.policy, ctx.http_get)
            for w in res.warnings:
                if w not in item["warnings"]:
                    item["warnings"].append(w)
            if res.ok:
                title = ctx.meta.get("title")
                version = "preprint" if name == "arxiv_preprint" else "published"
                suffix = PREPRINT_SUFFIX if version == "preprint" else ""
                path = unique_path(out / f"{_base_name(doi, title)}{suffix}.pdf")
                path.write_bytes(res.data)
                check = verify_pdf(str(path), cfg)
                if check["ok"]:
                    attempt.update(outcome="downloaded")
                    item["attempts"].append(attempt)
                    item["title"] = title
                    item["is_oa"] = ctx.meta.get("is_oa")
                    _finish_downloaded(item, name, str(path), check["sha256"], version)
                    record(manifest, item)
                    return item
                path.unlink(missing_ok=True)
                classes.append("invalid_pdf")
                last_error = f"verify_failed: {check['error']}"
            else:
                classes.append(res.error_class)
                last_error = res.error
        attempt.update(outcome="failed", error=last_error)
        attempt["error_classes"] = classes
        item["attempts"].append(attempt)

    item["title"] = ctx.meta.get("title")
    item["is_oa"] = ctx.meta.get("is_oa")
    item["expected_filename"] = f"{_base_name(doi, item['title'])}.pdf"
    item["status"] = "metadata_only" if item["title"] else "failed"
    item["evidence_level"] = "metadata_only" if item["title"] else "none"
    item["failure_class"] = classify_failure(item["attempts"], ctx.meta, cfg)
    item["manual_urls"] = manual_urls(doi, ctx)
    lookup_errors = "; ".join(f"{k}={v}" for k, v in ctx.meta["lookup_errors"].items())
    item["error"] = last_error or lookup_errors or item["failure_class"]
    return item


def acquire_dois(
    dois: List[str],
    outdir: str,
    email: Optional[str],
    timeout: int = 45,
    cfg: Optional[Dict[str, Any]] = None,
    http_get: Optional[HttpGet] = None,
    scihub_fn: Optional[ScihubFn] = None,
    fallback: Optional[FallbackConfig] = None,
    contact_email: Optional[str] = None,
) -> List[Dict[str, Any]]:
    cfg = cfg if cfg is not None else load_yaml("acquisition")
    scihub_fn = scihub_fn or attempt_scihub_fallback
    fallback = fallback or build_fallback_config(email, cfg)
    contact = contact_email or email or "scientific-paper-research@users.noreply.github.com"
    policy = build_http_policy(cfg, contact, timeout)
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    manifest = load_manifest(out, cfg)

    items: List[Dict[str, Any]] = []
    for doi in dois:
        ctx = ResolveContext(doi=doi, email=email, contact_email=contact, policy=policy, cfg=cfg, http_get=http_get)
        items.append(acquire_one(doi, out, ctx, fallback, cfg, scihub_fn, manifest))
    if cfg["manifest"].get("enabled", True):
        save_manifest(out, manifest, cfg)
    for item in items:
        item.pop("_", None)
        for a in item["attempts"]:
            a.pop("error_classes", None)
    return items
