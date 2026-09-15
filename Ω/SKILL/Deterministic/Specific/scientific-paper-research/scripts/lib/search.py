"""Scopus search and exact title resolution. Network calls go through an injectable request_fn."""

import re
from typing import Any, Callable, Dict, List, Optional

from lib.compile_query import compile_title_query
from lib.doi import is_valid_doi, normalize_doi
from lib.scopus import extract_entries, scopus_request

RequestFn = Callable[..., Dict[str, Any]]


def _paper_item(entry: Dict[str, Any]) -> Dict[str, Any]:
    doi = normalize_doi(entry.get("doi") or "")
    return {
        "title": entry.get("title") or "",
        "doi": doi if is_valid_doi(doi) else None,
        "year": entry.get("year") or None,
        "source": entry.get("source") or "",
        "cited_by": int(entry.get("cited_by") or 0),
        "authors": entry.get("authors") or "",
        "eid": entry.get("eid") or "",
        "full_text_available": False,
        "evidence_level": "metadata_only",
    }


def run_search(
    query: str,
    sort: str,
    count: int,
    api_key: str,
    page_size: int = 25,
    request_fn: Optional[RequestFn] = None,
) -> Dict[str, Any]:
    """Page through Scopus until `count` entries are collected or results run out."""
    request_fn = request_fn or scopus_request
    start = 0
    total_hits: Optional[int] = None
    papers: List[Dict[str, Any]] = []
    seen = set()
    missing_doi = 0

    while len(papers) < count:
        page = min(max(1, page_size), count - len(papers))
        raw = request_fn(api_key=api_key, query=query, count=page, start=start, sort=sort)
        parsed = extract_entries(raw)
        if total_hits is None:
            total_hits = parsed["total"]
        entries = parsed["entries"]
        if not entries:
            break
        for entry in entries:
            item = _paper_item(entry)
            key = item["doi"].lower() if item["doi"] else item["eid"] or item["title"]
            if item["doi"] is None:
                missing_doi += 1
            if key in seen:
                continue
            seen.add(key)
            papers.append(item)
            if len(papers) >= count:
                break
        start += len(entries)
        if total_hits is not None and start >= total_hits:
            break

    return {"total_hits": total_hits or 0, "scanned": start, "missing_doi": missing_doi, "papers": papers}


def normalize_title(value: str) -> str:
    text = re.sub(r"[^a-z0-9 ]+", " ", (value or "").lower())
    return re.sub(r"\s+", " ", text).strip()


def resolve_title(
    title: str,
    api_key: str,
    request_fn: Optional[RequestFn] = None,
    candidate_count: int = 5,
) -> Dict[str, Any]:
    """Exact-match resolution only: exact | ambiguous | not_found. Never picks the closest match."""
    request_fn = request_fn or scopus_request
    raw = request_fn(api_key=api_key, query=compile_title_query(title), count=candidate_count, start=0, sort="-citedby-count")
    entries = [_paper_item(e) for e in extract_entries(raw)["entries"]]
    return decide_exact(title, entries)


def decide_exact(title: str, entries: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Shared exact-match rule for every title provider. entries need title/doi/year."""
    wanted = normalize_title(title)
    exact = [e for e in entries if normalize_title(e["title"]) == wanted and e["doi"]]
    distinct_dois = {e["doi"].lower() for e in exact}
    candidates = [{"title": e["title"], "doi": e["doi"], "year": e["year"]} for e in entries]
    if not entries:
        return {"input_title": title, "resolution": "not_found", "resolved_doi": None, "candidates": [], "suggestion": None}
    if len(distinct_dois) == 1:
        return {"input_title": title, "resolution": "exact", "resolved_doi": exact[0]["doi"], "candidates": [], "suggestion": None}
    return {"input_title": title, "resolution": "ambiguous", "resolved_doi": None, "candidates": candidates, "suggestion": None}
