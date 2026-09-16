"""Candidate-URL resolvers, one per acquisition chain step, plus deterministic URL expanders.

Each resolver swallows its own errors and returns []. Expanders derive extra candidate URLs from
known publisher patterns (config/acquisition.yaml: candidate_rewrites, landing_expanders).
"""

import re
import urllib.parse
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from lib.doi import normalize_doi
from lib.http import HttpGet, HttpPolicy, classify_exception, get_json, urllib_get
from lib.unpaywall import build_candidate_urls, unpaywall_lookup

ARXIV_RE = re.compile(r"^10\.48550/arxiv\.(.+)$", re.IGNORECASE)


@dataclass
class ResolveContext:
    doi: str
    email: Optional[str]
    contact_email: str
    policy: HttpPolicy
    cfg: Dict[str, Any]
    http_get: Optional[HttpGet] = None
    meta: Dict[str, Any] = field(default_factory=lambda: {
        "title": None, "is_oa": None, "landing_urls": [], "lookup_404": [], "lookup_errors": {}, "skipped": [],
        "expanded_landings": [], "arxiv_id": None, "version": None,
    })
    tried: set = field(default_factory=set)

    def landing(self, url: Optional[str]) -> None:
        if url and url not in self.meta["landing_urls"]:
            self.meta["landing_urls"].append(url)

    def note_error(self, name: str, exc: BaseException) -> None:
        cls, msg = classify_exception(exc)
        if cls == "not_found":
            self.meta["lookup_404"].append(name)
        self.meta["lookup_errors"][name] = f"{cls}: {msg}"


def _dedupe(urls: List[Optional[str]]) -> List[str]:
    out: List[str] = []
    for u in urls:
        if u and u not in out:
            out.append(u)
    return out


# ---- resolvers ---------------------------------------------------------------

def resolve_arxiv_direct(doi: str, ctx: ResolveContext) -> List[str]:
    m = ARXIV_RE.match(doi)
    if not m:
        return []
    arxiv_id = m.group(1)
    cfg = ctx.cfg["arxiv_direct"]
    ctx.landing(cfg["landing_url"].format(id=arxiv_id))
    api_url = cfg.get("api_url")
    if api_url and not ctx.meta["title"]:
        try:
            get = ctx.http_get or urllib_get
            resp = get(api_url.format(id=arxiv_id), {"User-Agent": ctx.policy.ua(), "Accept": "application/atom+xml"}, ctx.policy.timeout, True)
            titles = re.findall(r"<entry>.*?<title>(.*?)</title>", resp.data.decode("utf-8", "ignore"), re.S)
            if titles:
                ctx.meta["title"] = re.sub(r"\s+", " ", titles[0]).strip()
        except Exception as exc:  # noqa: BLE001 - title is a nicety, never blocks the download
            ctx.note_error("arxiv_api", exc)
    return [cfg["pdf_url"].format(id=arxiv_id)]


def resolve_unpaywall(doi: str, ctx: ResolveContext) -> List[str]:
    if not ctx.email:
        ctx.meta["skipped"].append("unpaywall:no_email")
        return []
    try:
        record = unpaywall_lookup(doi, ctx.email, ctx.cfg["unpaywall"]["timeout_s"], ctx.http_get, ctx.policy, ctx.cfg["unpaywall"]["base_url"])
    except Exception as exc:  # noqa: BLE001
        ctx.note_error("unpaywall", exc)
        return []
    ctx.meta["title"] = ctx.meta["title"] or record.get("title") or None
    ctx.meta["is_oa"] = bool(record.get("is_oa")) if record.get("is_oa") is not None else ctx.meta["is_oa"]
    for loc in [record.get("best_oa_location") or {}] + list(record.get("oa_locations") or []):
        ctx.landing(loc.get("url_for_landing_page"))
    ctx.landing(record.get("doi_url"))
    return build_candidate_urls(record)


def resolve_europe_pmc(doi: str, ctx: ResolveContext) -> List[str]:
    cfg = ctx.cfg["europe_pmc"]
    params = urllib.parse.urlencode({"query": f'DOI:"{doi}"', "format": "json", "resultType": "lite", "email": ctx.contact_email})
    try:
        data = get_json(f"{cfg['search_url']}?{params}", ctx.policy, ctx.http_get)
    except Exception as exc:  # noqa: BLE001
        ctx.note_error("europe_pmc", exc)
        return []
    results = (data.get("resultList") or {}).get("result") or []
    urls: List[str] = []
    for r in results:
        if not ctx.meta["title"] and r.get("title"):
            ctx.meta["title"] = r["title"]
        pmcid = r.get("pmcid")
        if pmcid:
            urls.append(cfg["pdf_url"].format(pmcid=pmcid))
            ctx.landing(cfg["landing_url"].format(pmcid=pmcid))
    return _dedupe(urls)


def resolve_openalex(doi: str, ctx: ResolveContext) -> List[str]:
    cfg = ctx.cfg["openalex"]
    url = f"{cfg['base_url']}/works/https://doi.org/{urllib.parse.quote(doi, safe='/')}?mailto={urllib.parse.quote(ctx.contact_email)}"
    try:
        work = get_json(url, ctx.policy, ctx.http_get)
    except Exception as exc:  # noqa: BLE001
        ctx.note_error("openalex", exc)
        return []
    if not ctx.meta["title"] and work.get("display_name"):
        ctx.meta["title"] = work["display_name"]
    oa = work.get("open_access") or {}
    if ctx.meta["is_oa"] is None and oa.get("is_oa") is not None:
        ctx.meta["is_oa"] = bool(oa.get("is_oa"))
    best = work.get("best_oa_location") or {}
    urls: List[Optional[str]] = [best.get("pdf_url")]
    for loc in work.get("locations") or []:
        if loc.get("is_oa") and loc.get("pdf_url"):
            urls.append(loc["pdf_url"])
        ctx.landing(loc.get("landing_page_url"))
    urls.append(oa.get("oa_url"))
    urls.append(best.get("landing_page_url"))
    ctx.landing(best.get("landing_page_url"))
    pmcid = (work.get("ids") or {}).get("pmcid")
    if pmcid:
        pmcid = pmcid.rstrip("/").split("/")[-1]
        urls.append(ctx.cfg["europe_pmc"]["pdf_url"].format(pmcid=pmcid))
    return _dedupe(urls)


def resolve_semantic_scholar(doi: str, ctx: ResolveContext) -> List[str]:
    """Open-access PDF URL plus the arXiv id (kept in meta for arxiv_preprint). No API key."""
    cfg = ctx.cfg.get("semantic_scholar") or {}
    if not cfg.get("api_url"):
        return []
    try:
        data = get_json(cfg["api_url"].format(doi=urllib.parse.quote(doi, safe="/")), ctx.policy, ctx.http_get)
    except Exception as exc:  # noqa: BLE001
        ctx.note_error("semantic_scholar", exc)
        return []
    if not ctx.meta["title"] and data.get("title"):
        ctx.meta["title"] = data["title"]
    arxiv_id = (data.get("externalIds") or {}).get("ArXiv")
    if arxiv_id and not ctx.meta.get("arxiv_id"):
        ctx.meta["arxiv_id"] = str(arxiv_id)
    url = (data.get("openAccessPdf") or {}).get("url") or None
    return [url] if url else []


def _arxiv_entries(xml: str) -> List[Dict[str, str]]:
    out = []
    for entry in re.findall(r"<entry>(.*?)</entry>", xml, re.S):
        ident = re.search(r"<id>\s*(.*?)\s*</id>", entry, re.S)
        title = re.search(r"<title>(.*?)</title>", entry, re.S)
        if ident and title:
            arxiv_id = re.sub(r"v\d+$", "", ident.group(1).rstrip("/").split("/abs/")[-1])
            out.append({"id": arxiv_id, "title": re.sub(r"\s+", " ", title.group(1)).strip()})
    return out


def resolve_arxiv_preprint(doi: str, ctx: ResolveContext) -> List[str]:
    """arXiv preprint of a paper whose version of record is unreachable. Exact-title match only."""
    from lib.search import normalize_title

    if ARXIV_RE.match(doi):
        return []
    cfg = ctx.cfg.get("arxiv_preprint") or {}
    arxiv_id: Optional[str] = ctx.meta.get("arxiv_id")
    if not arxiv_id and ctx.meta.get("title") and cfg.get("search_url"):
        query = urllib.parse.quote(f'ti:"{ctx.meta["title"].replace(chr(34), "")}"')
        try:
            get = ctx.http_get or urllib_get
            resp = get(cfg["search_url"].format(query=query), {"User-Agent": ctx.policy.ua(), "Accept": "application/atom+xml"}, ctx.policy.timeout, True)
        except Exception as exc:  # noqa: BLE001
            ctx.note_error("arxiv_preprint", exc)
            return []
        wanted = normalize_title(ctx.meta["title"])
        hits = [e for e in _arxiv_entries(resp.data.decode("utf-8", "ignore")) if normalize_title(e["title"]) == wanted]
        if len(hits) == 1 or not cfg.get("require_exact_title", True) and hits:
            arxiv_id = hits[0]["id"]
    if not arxiv_id:
        return []
    ctx.meta["arxiv_id"] = arxiv_id
    ctx.meta["version"] = "preprint"
    ctx.landing(cfg.get("landing_url", "https://arxiv.org/abs/{id}").format(id=arxiv_id))
    return [cfg.get("pdf_url", "https://arxiv.org/pdf/{id}").format(id=arxiv_id)]


RESOLVERS: Dict[str, Callable[[str, ResolveContext], List[str]]] = {
    "arxiv_direct": resolve_arxiv_direct,
    "unpaywall": resolve_unpaywall,
    "europe_pmc": resolve_europe_pmc,
    "openalex": resolve_openalex,
    "semantic_scholar": resolve_semantic_scholar,
    "arxiv_preprint": resolve_arxiv_preprint,
}


# ---- expanders ---------------------------------------------------------------

def rewrite_candidates(urls: List[str], cfg: Dict[str, Any]) -> List[str]:
    """Apply candidate_rewrites: every matching URL yields one extra URL (appended after the originals)."""
    rules = cfg.get("candidate_rewrites") or []
    extra: List[str] = []
    for u in urls:
        for rule in rules:
            m = re.search(rule["pattern"], u)
            if m:
                n = next((g for g in m.groups() if g), None)
                if n:
                    extra.append(rule["template"].format(n=n))
    return extra


def expand_figshare(landing_url: str, ctx: ResolveContext) -> List[str]:
    fs = ctx.cfg.get("figshare") or {}
    m = re.search(fs.get("pattern", r"figshare\.com/articles/[^/]+/[^/]+/(\d+)"), landing_url)
    if not m:
        return []
    try:
        data = get_json(fs["api_url"].format(id=m.group(1)), ctx.policy, ctx.http_get)
    except Exception as exc:  # noqa: BLE001
        ctx.note_error("figshare", exc)
        return []
    files = data.get("files") or []
    pdfs = [f.get("download_url") for f in files if (f.get("name") or "").lower().endswith(".pdf")]
    others = [f.get("download_url") for f in files if f.get("download_url") not in pdfs]
    return _dedupe(pdfs + others)


def expand_landings(ctx: ResolveContext) -> List[str]:
    """Run landing_expanders once per landing URL seen so far."""
    urls: List[str] = []
    for land in list(ctx.meta["landing_urls"]):
        if land in ctx.meta["expanded_landings"]:
            continue
        ctx.meta["expanded_landings"].append(land)
        for name in ctx.cfg.get("landing_expanders") or []:
            if name == "figshare":
                urls += expand_figshare(land, ctx)
    return _dedupe(urls)


def expand_candidates(candidates: List[str], ctx: ResolveContext) -> List[str]:
    """Originals first, then rewrites of originals and landing pages, then landing-expander results."""
    base = _dedupe(list(candidates))
    rewritten = rewrite_candidates(base + list(ctx.meta["landing_urls"]), ctx.cfg)
    return _dedupe(base + rewritten + expand_landings(ctx))


def manual_urls(doi: str, ctx: ResolveContext) -> List[str]:
    cap = int(ctx.cfg["http"].get("manual_urls_max", 5))
    urls = _dedupe([f"https://doi.org/{normalize_doi(doi)}"] + list(ctx.meta["landing_urls"]))
    return urls[:cap]
