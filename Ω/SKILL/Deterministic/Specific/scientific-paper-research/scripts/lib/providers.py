"""Search and title-resolution providers. Chain order comes from config/providers.yaml."""

import urllib.parse
from typing import Any, Dict, List, Optional

from lib.compile_query import OpenAlexPlan, QueryPlan
from lib.config import load_yaml
from lib.doi import is_valid_doi, normalize_doi
from lib.http import HttpGet, HttpPolicy, get_json
from lib.search import decide_exact, resolve_title as resolve_title_scopus_raw, run_search


def contact_email(env: Dict[str, Any], cfg: Optional[Dict[str, Any]] = None) -> str:
    cfg = cfg if cfg is not None else load_yaml("providers")
    return env.get(cfg["contact"]["email_env"]) or cfg["contact"]["fallback"]


def _policy(env: Dict[str, Any], cfg: Dict[str, Any]) -> HttpPolicy:
    acq = load_yaml("acquisition")["http"]
    return HttpPolicy(user_agent=acq["user_agent"], alt_user_agent=acq.get("alt_user_agent", ""), contact_email=contact_email(env, cfg),
                      timeout=int(load_yaml("defaults")["http_timeout_s"]))


def provider_available(name: str, env: Dict[str, Any]) -> bool:
    if name == "scopus":
        return bool(env.get("ELSEVIER_API_KEY"))
    return name in ("openalex", "crossref")


def available_search_providers(env: Dict[str, Any], cfg: Optional[Dict[str, Any]] = None) -> List[str]:
    cfg = cfg if cfg is not None else load_yaml("providers")
    return [p for p in cfg["search"] if provider_available(p, env)]


# ---- search ----------------------------------------------------------------

def search_scopus(plan: QueryPlan, count: int, env: Dict[str, Any], page_size: int, request_fn=None) -> Dict[str, Any]:
    found = run_search(plan.query, plan.sort, count, env["ELSEVIER_API_KEY"], page_size, request_fn)
    found["provider"] = "scopus"
    return found


def openalex_paper_item(work: Dict[str, Any]) -> Dict[str, Any]:
    doi = normalize_doi(work.get("doi") or "")
    source = ((work.get("primary_location") or {}).get("source") or {}).get("display_name") or ""
    authors = [((a.get("author") or {}).get("display_name") or "") for a in work.get("authorships") or []]
    ident = (work.get("id") or "").rstrip("/").split("/")[-1]
    return {
        "title": work.get("display_name") or "",
        "doi": doi if is_valid_doi(doi) else None,
        "year": str(work["publication_year"]) if work.get("publication_year") else None,
        "source": source,
        "cited_by": int(work.get("cited_by_count") or 0),
        "authors": "; ".join(a for a in authors if a),
        "eid": ident,
        "full_text_available": False,
        "evidence_level": "metadata_only",
    }


def search_openalex(plan: OpenAlexPlan, count: int, env: Dict[str, Any], cfg: Optional[Dict[str, Any]] = None, http_get: Optional[HttpGet] = None) -> Dict[str, Any]:
    cfg = cfg if cfg is not None else load_yaml("providers")
    oa = cfg["openalex"]
    policy = _policy(env, cfg)
    papers: List[Dict[str, Any]] = []
    seen = set()
    total: Optional[int] = None
    page = 1
    missing_doi = 0
    per_page = min(int(oa.get("per_page_max", 200)), max(1, count))
    while len(papers) < count:
        params = {"search": plan.search, "per-page": per_page, "page": page, "sort": plan.sort, "mailto": policy.contact_email}
        if plan.filters:
            params["filter"] = ",".join(plan.filters)
        data = get_json(f"{oa['base_url']}/works?{urllib.parse.urlencode(params)}", policy, http_get)
        if total is None:
            total = int((data.get("meta") or {}).get("count") or 0)
        results = data.get("results") or []
        if not results:
            break
        for work in results:
            item = openalex_paper_item(work)
            key = item["doi"].lower() if item["doi"] else item["eid"]
            if item["doi"] is None:
                missing_doi += 1
            if key in seen:
                continue
            seen.add(key)
            papers.append(item)
            if len(papers) >= count:
                break
        page += 1
        if page * per_page > (total or 0) + per_page:
            break
    return {"total_hits": total or 0, "scanned": (page - 1) * per_page, "missing_doi": missing_doi, "papers": papers, "provider": "openalex"}


# ---- title resolution --------------------------------------------------------

def resolve_title_crossref(title: str, env: Dict[str, Any], cfg: Optional[Dict[str, Any]] = None, http_get: Optional[HttpGet] = None) -> Dict[str, Any]:
    cfg = cfg if cfg is not None else load_yaml("providers")
    cr = cfg["crossref"]
    policy = _policy(env, cfg)
    params = urllib.parse.urlencode({"query.bibliographic": title, "rows": cr["rows"], "select": cr["select"], "mailto": policy.contact_email})
    data = get_json(f"{cr['base_url']}/works?{params}", policy, http_get)
    entries = []
    for it in (data.get("message") or {}).get("items") or []:
        parts = ((it.get("issued") or {}).get("date-parts") or [[None]])[0]
        doi = normalize_doi(it.get("DOI") or "")
        entries.append({"title": (it.get("title") or [""])[0], "doi": doi if is_valid_doi(doi) else None, "year": str(parts[0]) if parts and parts[0] else None})
    return decide_exact(title, entries)


def resolve_title_openalex(title: str, env: Dict[str, Any], cfg: Optional[Dict[str, Any]] = None, http_get: Optional[HttpGet] = None) -> Dict[str, Any]:
    cfg = cfg if cfg is not None else load_yaml("providers")
    oa = cfg["openalex"]
    policy = _policy(env, cfg)
    safe_title = title.replace('"', "")
    params = urllib.parse.urlencode({"filter": f'title.search:"{safe_title}"', "per-page": oa.get("title_candidates", 5), "mailto": policy.contact_email})
    data = get_json(f"{oa['base_url']}/works?{params}", policy, http_get)
    entries = [openalex_paper_item(w) for w in data.get("results") or []]
    return decide_exact(title, entries)


def resolve_title_scopus(title: str, env: Dict[str, Any], request_fn=None) -> Dict[str, Any]:
    return resolve_title_scopus_raw(title, env["ELSEVIER_API_KEY"], request_fn)


def resolve_title_chain(title: str, env: Dict[str, Any], deps: Optional[Dict[str, Any]] = None, cfg: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Iterate providers in config order; stop at the first exact match. Never picks a closest match."""
    cfg = cfg if cfg is not None else load_yaml("providers")
    deps = deps or {}
    first_ambiguous: Optional[Dict[str, Any]] = None
    used: List[str] = []
    for name in cfg["title_resolution"]:
        if not provider_available(name, env):
            continue
        try:
            if name == "crossref":
                res = resolve_title_crossref(title, env, cfg, deps.get("http_get"))
            elif name == "openalex":
                res = resolve_title_openalex(title, env, cfg, deps.get("http_get"))
            else:
                res = resolve_title_scopus(title, env, deps.get("request_fn"))
        except Exception:  # noqa: BLE001 - a provider outage must not stop the chain
            continue
        used.append(name)
        res["provider"] = name
        if res["resolution"] == "exact":
            res["providers_used"] = used
            return res
        if res["resolution"] == "ambiguous" and first_ambiguous is None:
            first_ambiguous = res
    result = first_ambiguous or {"input_title": title, "resolution": "not_found", "resolved_doi": None, "candidates": [],
                                 "suggestion": None, "provider": used[-1] if used else None}
    if result["resolution"] == "ambiguous":
        result["suggestion"] = suggest_doi(title, result["candidates"], cfg)
    result["providers_used"] = used
    return result


def suggest_doi(title: str, candidates: List[Dict[str, Any]], cfg: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """Propose one DOI for an ambiguous title when exactly one candidate fits a fixed rule. Never downloads."""
    from difflib import SequenceMatcher

    from lib.search import normalize_title

    cfg = cfg if cfg is not None else load_yaml("providers")
    ts = cfg.get("title_suggest") or {}
    min_chars = int(ts.get("min_chars", 30))
    min_ratio = float(ts.get("min_ratio", 0.9))
    inp = normalize_title(title)
    if len(inp) < min_chars:
        return None
    matches: List[Dict[str, Any]] = []
    for c in candidates:
        if not c.get("doi"):
            continue
        cand = normalize_title(c.get("title") or "")
        if cand.startswith(inp) or inp.startswith(cand):
            rule = "prefix"
        elif SequenceMatcher(None, inp, cand).ratio() >= min_ratio:
            rule = "ratio"
        else:
            continue
        matches.append({"doi": c["doi"], "title": c.get("title"), "year": c.get("year"), "rule": rule})
    return matches[0] if len(matches) == 1 else None
