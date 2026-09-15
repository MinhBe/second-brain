"""DOI parsing and normalization. Pure functions, no network."""

import re
from typing import List, Optional

DOI_RE = re.compile(r"10\.\d{4,9}/[^\s\"'<>]+", re.IGNORECASE)
_FULL_RE = re.compile(r"^10\.\d{4,9}/\S+$", re.IGNORECASE)
_PREFIXES = ("https://doi.org/", "http://doi.org/", "https://dx.doi.org/", "http://dx.doi.org/", "doi.org/", "doi:", "DOI:")
_TRAILING = ".,;:)]}>"


def normalize_doi(value: str) -> str:
    text = (value or "").strip()
    lowered = text.lower()
    for prefix in _PREFIXES:
        if lowered.startswith(prefix.lower()):
            text = text[len(prefix):].strip()
            break
    return text.rstrip(_TRAILING).strip()


def is_valid_doi(value: str) -> bool:
    return bool(_FULL_RE.match(value or ""))


def find_dois(text: str) -> List[str]:
    found: List[str] = []
    seen = set()
    for match in DOI_RE.findall(text or ""):
        doi = normalize_doi(match)
        key = doi.lower()
        if is_valid_doi(doi) and key not in seen:
            seen.add(key)
            found.append(doi)
    return found


def first_doi(text: str) -> Optional[str]:
    dois = find_dois(text)
    return dois[0] if dois else None
