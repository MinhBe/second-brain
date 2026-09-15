"""Mode handlers. Each returns (status, result, next_command). Network/PDF functions are injectable via deps."""

import hashlib
import json
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from lib.acquire import acquire_dois, build_fallback_config
from lib.compile_query import (
    attach_filters,
    attach_filters_openalex,
    compile_keyword_query,
    compile_keyword_query_openalex,
    compile_topic_query,
    compile_topic_query_openalex,
    openalex_compiled_string,
    resolve_concept,
    resolve_from_year,
)
from lib.config import load_yaml
from lib.parse_paper import parse_pdf
from lib.providers import available_search_providers, contact_email, resolve_title_chain, search_openalex, search_scopus
from lib.validate_evidence import validate_evidence

Handler = Callable[[Dict[str, Any], Dict[str, Any], Dict[str, Any]], Tuple[str, Dict[str, Any], Optional[str]]]
STEP2_COMMAND = "python -X utf8 scripts/run.py --request {path}"


class ModeError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


class EvidenceInvalid(Exception):
    def __init__(self, result: Dict[str, Any]):
        super().__init__("evidence_invalid")
        self.result = result


def _acquire(dois: List[str], req: Dict[str, Any], env: Dict[str, Any], deps: Dict[str, Any]) -> List[Dict[str, Any]]:
    email = env.get("UNPAYWALL_EMAIL") or None
    defaults = load_yaml("defaults")
    return acquire_dois(
        dois,
        outdir=req["outdir"],
        email=email,
        timeout=int(defaults["http_timeout_s"]),
        http_get=deps.get("http_get"),
        scihub_fn=deps.get("scihub_fn"),
        fallback=deps.get("fallback") or build_fallback_config(email),
        contact_email=contact_email(env),
    )


def _attach_acquisition(found_papers: List[Dict[str, Any]], req: Dict[str, Any], env: Dict[str, Any], deps: Dict[str, Any]) -> Tuple[str, Optional[Dict[str, Any]]]:
    if not req.get("download"):
        return "ok", None
    dois = [p["doi"] for p in found_papers if p["doi"]]
    items = _acquire(dois, req, env, deps)
    by_doi = {i["doi"].lower(): i for i in items}
    for paper in found_papers:
        hit = by_doi.get((paper["doi"] or "").lower())
        if hit:
            paper["full_text_available"] = hit["full_text_available"]
            paper["evidence_level"] = hit["evidence_level"]
    downloaded = sum(1 for i in items if i["status"] == "downloaded")
    status = "ok" if downloaded == len(items) else "partial"
    return status, {"attempted_count": len(items), "downloaded_count": downloaded, "items": items}


def _search(req: Dict[str, Any], env: Dict[str, Any], deps: Dict[str, Any], blocks=None) -> Tuple[str, Dict[str, Any]]:
    """Run the first available provider. blocks is set for TOPIC_SEARCH; req['query'] for KEYWORD_SEARCH."""
    defaults = load_yaml("defaults")
    providers = available_search_providers(env)
    provider = providers[0]
    if req.get("query_is_scopus_syntax") and provider != "scopus":
        raise ModeError("scopus_syntax_requires_key", "query_is_scopus_syntax needs ELSEVIER_API_KEY")
    from_year = resolve_from_year(req.get("year_from"), req.get("years_back"), req.get("freshness"), defaults, deps.get("today"))
    count = int(req["result_count"])

    if provider == "scopus":
        base = compile_topic_query(blocks) if blocks is not None else compile_keyword_query(req["query"], bool(req.get("query_is_scopus_syntax")))
        plan = attach_filters(base, from_year, req["language"], req["document_type"], defaults)
        found = search_scopus(plan, count, env, int(defaults["page_size"]), deps.get("request_fn"))
        compiled, sort, filters = plan.query, plan.sort, plan.filters
    else:
        base = compile_topic_query_openalex(blocks) if blocks is not None else compile_keyword_query_openalex(req["query"])
        plan = attach_filters_openalex(base, from_year, req["language"], req["document_type"])
        found = search_openalex(plan, count, env, http_get=deps.get("http_get"))
        compiled, sort, filters = openalex_compiled_string(plan), plan.sort, plan.filters_dict

    req["providers_used"] = [provider]
    status, acquisition = _attach_acquisition(found["papers"], req, env, deps)
    result: Dict[str, Any] = {
        "compiled_query": compiled,
        "provider": provider,
        "sort": sort,
        "filters": filters,
        "total_hits": found["total_hits"],
        "returned_count": len(found["papers"]),
        "papers": found["papers"],
        "acquisition": acquisition,
    }
    return status, result


def topic_search(req: Dict[str, Any], env: Dict[str, Any], deps: Dict[str, Any]):
    blocks = [resolve_concept(c["slot"], c["term"]) for c in req["concepts"]]
    status, result = _search(req, env, deps, blocks=blocks)
    ordered = {"compiled_query": result["compiled_query"], "provider": result["provider"], "sort": result["sort"],
               "filters": result["filters"], "concept_blocks": [b.to_dict() for b in blocks]}
    for k in ("total_hits", "returned_count", "papers", "acquisition"):
        ordered[k] = result[k]
    return status, ordered, None


def keyword_search(req: Dict[str, Any], env: Dict[str, Any], deps: Dict[str, Any]):
    status, result = _search(req, env, deps)
    return status, result, None


def doi_download(req: Dict[str, Any], env: Dict[str, Any], deps: Dict[str, Any]):
    items = _acquire(req["dois"], req, env, deps)
    downloaded = sum(1 for i in items if i["status"] == "downloaded")
    result = {
        "requested_count": len(req["dois"]) + len(req.get("invalid_dois") or []),
        "valid_dois": list(req["dois"]),
        "invalid_dois": list(req.get("invalid_dois") or []),
        "downloaded_count": downloaded,
        "failed_count": len(items) - downloaded,
        "items": items,
    }
    return ("ok" if downloaded == len(items) else "partial"), result, None


def title_download(req: Dict[str, Any], env: Dict[str, Any], deps: Dict[str, Any]):
    resolutions = [resolve_title_chain(t, env, deps) for t in req["titles"]]
    used: List[str] = []
    for r in resolutions:
        for p in r.pop("providers_used", []):
            if p not in used:
                used.append(p)
    req["providers_used"] = used
    exact_dois = [r["resolved_doi"] for r in resolutions if r["resolution"] == "exact"]
    acquired = {i["doi"].lower(): i for i in _acquire(exact_dois, req, env, deps)} if exact_dois else {}
    items = []
    for r in resolutions:
        items.append({
            "input_title": r["input_title"],
            "resolution": r["resolution"],
            "provider": r.get("provider"),
            "resolved_doi": r["resolved_doi"],
            "candidates": r["candidates"],
            "suggestion": r.get("suggestion"),
            "acquisition": acquired.get((r["resolved_doi"] or "").lower()),
        })
    downloaded = sum(1 for i in items if i["acquisition"] and i["acquisition"]["status"] == "downloaded")
    result = {"requested_count": len(items), "resolved_count": len(exact_dois), "downloaded_count": downloaded, "items": items}
    return ("ok" if downloaded == len(items) else "partial"), result, None


# ---- analysis -------------------------------------------------------------

def _meta_path(workdir: str, paper_id: str) -> Path:
    return Path(workdir) / f"{paper_id}.meta.json"


def _step1(pdf_path: str, workdir: str, deps: Dict[str, Any]) -> Dict[str, Any]:
    try:
        info = parse_pdf(pdf_path, workdir, extract_fn=deps.get("extract_fn"))
    except FileNotFoundError:
        raise ModeError("pdf_not_found", f"PDF not found: {pdf_path}")
    except RuntimeError as exc:
        raise ModeError("pdf_unreadable", f"could not extract text from {pdf_path}: {exc}")
    _meta_path(workdir, info["paper_id"]).write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")
    return info


def _paper_id(pdf_path: str) -> str:
    p = Path(pdf_path)
    if not p.is_file():
        raise ModeError("pdf_not_found", f"PDF not found: {pdf_path}")
    return hashlib.sha256(p.read_bytes()).hexdigest()[:12]


def _step2(pdf_path: str, workdir: str, evidence_path: str) -> Tuple[bool, Dict[str, Any]]:
    paper_id = _paper_id(pdf_path)
    meta_file = _meta_path(workdir, paper_id)
    if not meta_file.is_file():
        raise ModeError("pdf_unreadable", f"step 1 output missing for {pdf_path}; run step 1 first")
    meta = json.loads(meta_file.read_text(encoding="utf-8"))
    text = Path(meta["text_path"]).read_text(encoding="utf-8")
    sections = json.loads(Path(meta["sections_path"]).read_text(encoding="utf-8"))
    ev_file = Path(evidence_path)
    if not ev_file.is_file():
        raise ModeError("evidence_invalid", f"evidence file not found: {evidence_path}")
    base = {"paper_id": paper_id, "pdf_path": pdf_path, "doi": meta.get("detected_doi"), "title": None,
            "evidence_level": meta["evidence_level"], "full_text_available": meta["full_text_available"]}
    try:
        evidence = json.loads(ev_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors = [{"code": "schema_violation", "field": None, "message": f"invalid JSON: {exc}"}]
        return False, {**base, "fields": None, "validation": {"ok": False, "error_count": 1, "errors": errors}}
    errors = validate_evidence(evidence, sections, text, meta["evidence_level"])
    return (not errors), {**base, "fields": evidence if not errors else None,
                          "validation": {"ok": not errors, "error_count": len(errors), "errors": errors}}


def _write_step2_request(workdir: str, name: str, request: Dict[str, Any]) -> str:
    path = Path(workdir) / f"{name}.request.step2.json"
    path.write_text(json.dumps(request, ensure_ascii=False, indent=2), encoding="utf-8")
    return path.as_posix()


def paper_analysis(req: Dict[str, Any], env: Dict[str, Any], deps: Dict[str, Any]):
    workdir = req["workdir"]
    if not req.get("evidence_path"):
        info = _step1(req["pdf_path"], workdir, deps)
        step2 = {"mode": "PAPER_ANALYSIS", "pdf_path": req["pdf_path"], "workdir": workdir, "evidence_path": info["evidence_template_path"]}
        path = _write_step2_request(workdir, info["paper_id"], step2)
        return "needs_evidence", info, STEP2_COMMAND.format(path=path)
    ok, result = _step2(req["pdf_path"], workdir, req["evidence_path"])
    if not ok:
        raise EvidenceInvalid(result)
    return "ok", result, None


def batch_analysis(req: Dict[str, Any], env: Dict[str, Any], deps: Dict[str, Any]):
    workdir = req["workdir"]
    batch_id = hashlib.sha256("\n".join(req["pdf_paths"]).encode("utf-8")).hexdigest()[:12]
    if not req.get("evidence_dir"):
        papers, failed = [], 0
        for pdf in req["pdf_paths"]:
            try:
                papers.append(_step1(pdf, workdir, deps))
            except ModeError as exc:
                failed += 1
                papers.append({"pdf_path": pdf, "error": {"code": exc.code, "message": exc.message}})
        step2 = {"mode": "BATCH_ANALYSIS", "pdf_paths": req["pdf_paths"], "workdir": workdir, "evidence_dir": workdir}
        path = _write_step2_request(workdir, f"batch-{batch_id}", step2)
        summary = {"total": len(req["pdf_paths"]), "parsed": len(req["pdf_paths"]) - failed, "failed": failed, "validated": 0}
        return "needs_evidence", {"papers": papers, "summary": summary}, STEP2_COMMAND.format(path=path)
    papers, validated, failed = [], 0, 0
    for pdf in req["pdf_paths"]:
        try:
            pid = _paper_id(pdf)
            ok, result = _step2(pdf, workdir, (Path(req["evidence_dir"]) / f"{pid}.evidence.json").as_posix())
            validated += 1 if ok else 0
            papers.append(result)
        except ModeError as exc:
            failed += 1
            papers.append({"pdf_path": pdf, "error": {"code": exc.code, "message": exc.message}})
    summary = {"total": len(papers), "parsed": len(papers) - failed, "failed": failed, "validated": validated}
    status = "ok" if validated == len(papers) else "partial"
    return status, {"papers": papers, "summary": summary}, None


MODE_HANDLERS: Dict[str, Handler] = {
    "TOPIC_SEARCH": topic_search,
    "KEYWORD_SEARCH": keyword_search,
    "DOI_DOWNLOAD": doi_download,
    "TITLE_DOWNLOAD": title_download,
    "PAPER_ANALYSIS": paper_analysis,
    "BATCH_ANALYSIS": batch_analysis,
}
