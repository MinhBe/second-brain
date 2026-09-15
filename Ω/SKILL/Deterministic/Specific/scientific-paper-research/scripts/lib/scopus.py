#!/usr/bin/env python3
"""Scopus Search API client (library, no CLI). Derived from sci-papers-downloder (MIT)."""

import json
import urllib.parse
import urllib.request
from typing import Any, Dict, List

SCOPUS_SEARCH_URL = "https://api.elsevier.com/content/search/scopus"


def quote_term(term: str) -> str:
    # Scopus query grammar supports quoted literals; quote when spaces exist.
    if any(ch.isspace() for ch in term):
        return f'"{escape_quotes(term)}"'
    return term


def escape_quotes(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def scopus_request(api_key: str, query: str, count: int, start: int, sort: str) -> Dict[str, Any]:
    params = urllib.parse.urlencode(
        {
            "query": query,
            "count": count,
            "start": start,
            "sort": sort,
        }
    )
    url = f"{SCOPUS_SEARCH_URL}?{params}"
    req = urllib.request.Request(
        url,
        headers={
            "X-ELS-APIKey": api_key,
            "Accept": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8", "ignore"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "ignore")
        raise RuntimeError(f"Scopus API error HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error: {exc}") from exc


def extract_entries(raw: Dict[str, Any]) -> Dict[str, Any]:
    results = raw.get("search-results", {})
    total = int(results.get("opensearch:totalResults", "0") or "0")
    entries_raw = results.get("entry") or []

    entries: List[Dict[str, Any]] = []
    for item in entries_raw:
        entry = {
            "title": item.get("dc:title") or "",
            "doi": item.get("prism:doi") or "N/A",
            "year": (item.get("prism:coverDate") or "")[:4] or "N/A",
            "source": item.get("prism:publicationName") or "",
            "cited_by": safe_int(item.get("citedby-count")),
            "authors": item.get("dc:creator") or "",
            "eid": item.get("eid") or "",
        }
        entries.append(entry)

    return {
        "total": total,
        "entries": entries,
    }


def safe_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0
