"""PDF -> text + section map + empty evidence template. Step 1 of PAPER_ANALYSIS."""

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from lib.config import load_schema, load_yaml
from lib.doi import first_doi

ExtractFn = Callable[..., Tuple[List[Any], int, str]]

EVIDENCE_FIELDS = [
    "study_design", "population", "sample_size", "intervention", "comparator", "outcomes",
    "inclusion_criteria", "exclusion_criteria", "methods", "statistical_methods", "key_results",
    "conclusions", "limitations",
]


def evidence_template() -> Dict[str, Any]:
    fields = list(load_schema("evidence")["properties"].keys()) or EVIDENCE_FIELDS
    return {f: {"value": None, "source": None, "location": None, "status": "not_found"} for f in fields}


def build_text(pages: List[Any]) -> Tuple[str, List[int]]:
    """Join page texts with a blank line; return full text and the char offset where each page starts."""
    offsets: List[int] = []
    parts: List[str] = []
    cursor = 0
    for page in pages:
        text = (getattr(page, "text", None) or "").strip()
        offsets.append(cursor)
        parts.append(text)
        cursor += len(text) + 2
    return "\n\n".join(parts), offsets


def _page_of(offset: int, page_offsets: List[int]) -> int:
    page = 1
    for idx, start in enumerate(page_offsets, 1):
        if start <= offset:
            page = idx
        else:
            break
    return page


def detect_sections(text: str, page_offsets: Optional[List[int]] = None, cfg: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Find heading lines; return ordered spans. A synthetic 'body' section always covers the whole text."""
    cfg = cfg if cfg is not None else load_yaml("sections")
    page_offsets = page_offsets or [0]
    prefix = cfg["number_prefix"]
    max_len = int(cfg["max_line_len"])
    compiled = [
        (entry["canonical"], re.compile(prefix + "(?:" + "|".join(entry["patterns"]) + r")\s*:?\s*$", re.IGNORECASE))
        for entry in cfg["sections"]
    ]
    found: List[Dict[str, Any]] = []
    pos = 0
    for line in text.splitlines(keepends=True):
        stripped = line.strip()
        if stripped and len(stripped) <= max_len:
            for canonical, rx in compiled:
                if rx.match(stripped):
                    found.append({"name": stripped, "canonical": canonical, "page_start": _page_of(pos, page_offsets), "char_start": pos, "char_end": None})
                    break
        pos += len(line)
    for idx, sec in enumerate(found):
        sec["char_end"] = found[idx + 1]["char_start"] if idx + 1 < len(found) else len(text)
    body = {"name": "body", "canonical": "body", "page_start": 1, "char_start": 0, "char_end": len(text)}
    return [body] + found


def parse_pdf(
    pdf_path: str,
    workdir: str,
    defaults: Optional[Dict[str, Any]] = None,
    extract_fn: Optional[ExtractFn] = None,
) -> Dict[str, Any]:
    """Returns the step-1 result dict. Raises FileNotFoundError / RuntimeError with fixed messages."""
    defaults = defaults if defaults is not None else load_yaml("defaults")
    analysis = defaults["analysis"]
    path = Path(pdf_path)
    if not path.is_file():
        raise FileNotFoundError(str(pdf_path))

    if extract_fn is None:
        from lib.pdf_text import extract_pdf

        extract_fn = extract_pdf
    pages, page_count, engine = extract_fn(path, "auto", "eng")

    text, page_offsets = build_text(pages)
    sha = hashlib.sha256(path.read_bytes()).hexdigest()
    paper_id = sha[:12]
    sections = detect_sections(text, page_offsets)
    char_count = len(text.strip())
    full_text = char_count >= int(analysis["full_text_min_chars"])

    scan_pages = int(analysis.get("doi_scan_pages", 2))
    head_end = page_offsets[scan_pages] if len(page_offsets) > scan_pages else len(text)
    detected_doi = first_doi(text[:head_end])

    wd = Path(workdir)
    wd.mkdir(parents=True, exist_ok=True)
    text_path = wd / f"{paper_id}.text.txt"
    sections_path = wd / f"{paper_id}.sections.json"
    evidence_path = wd / f"{paper_id}.evidence.json"
    text_path.write_text(text, encoding="utf-8")
    sections_path.write_text(json.dumps(sections, ensure_ascii=False, indent=2), encoding="utf-8")
    if not evidence_path.exists():  # never overwrite a template the model already filled
        evidence_path.write_text(json.dumps(evidence_template(), ensure_ascii=False, indent=2), encoding="utf-8")

    return {
        "paper_id": paper_id,
        "pdf_path": str(pdf_path),
        "sha256": sha,
        "engine": engine,
        "page_count": page_count,
        "char_count": char_count,
        "evidence_level": "full_text" if full_text else "none",
        "full_text_available": full_text,
        "detected_doi": detected_doi,
        "sections": sections,
        "sections_path": sections_path.as_posix(),
        "text_path": text_path.as_posix(),
        "evidence_template_path": evidence_path.as_posix(),
        "instructions_ref": "references/evidence-fields.md",
    }
