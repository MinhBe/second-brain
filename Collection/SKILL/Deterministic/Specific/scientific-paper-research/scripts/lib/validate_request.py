"""Request validation: schema -> mode rules -> defaults -> clarification. No network."""

from dataclasses import dataclass
from datetime import date
from typing import Any, Dict, List, Optional, Tuple

from lib.config import load_schema, load_yaml
from lib.doi import is_valid_doi, normalize_doi
from lib.output import make_clarification, make_error

SEARCH_MODES = ("TOPIC_SEARCH", "KEYWORD_SEARCH")
ANALYSIS_MODES = ("PAPER_ANALYSIS", "BATCH_ANALYSIS")


@dataclass
class ValidationResult:
    normalized: Optional[Dict[str, Any]]
    clarification: Optional[Dict[str, Any]]
    error: Optional[Dict[str, Any]]

    @property
    def status(self) -> str:
        if self.error:
            return "invalid_request"
        if self.clarification:
            return "clarification_required"
        return "ok"


def _mode_of(request: Any) -> Optional[str]:
    if isinstance(request, dict):
        mode = request.get("mode")
        if isinstance(mode, str):
            return mode
    return None


def _schema_error_message(err: Any, mode: str) -> str:
    path = ".".join(str(p) for p in err.absolute_path) or "request"
    if err.validator == "required":
        missing = [f for f in err.validator_value if f not in (err.instance or {})]
        return f"field '{missing[0] if missing else '?'}' is required for {mode}"
    if err.validator == "additionalProperties":
        extra = sorted(set(err.instance) - set(err.schema.get("properties", {})))
        return f"unknown field '{extra[0] if extra else '?'}' is not allowed in {mode}"
    if err.validator == "enum":
        return f"field '{path}' must be one of {err.validator_value}"
    if err.validator == "const":
        return f"field '{path}' must be {err.validator_value!r}"
    return f"field '{path}' is invalid: {err.message}"


def _schema_validate(request: Dict[str, Any], mode: str) -> Optional[str]:
    import jsonschema

    schema = load_schema("request")
    branch = next(b for b in schema["oneOf"] if b["properties"]["mode"]["const"] == mode)
    validator = jsonschema.Draft202012Validator(branch)
    errors = sorted(validator.iter_errors(request), key=lambda e: (list(e.absolute_path), e.validator))
    if not errors:
        return None
    return _schema_error_message(errors[0], mode)


def _resolve_result_count(value: Any, defaults: Dict[str, Any]) -> Optional[int]:
    if value is None:
        return int(defaults["result_count"])
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return max(1, min(int(value), int(defaults["result_count_max"])))
    words = defaults["result_count_words"]
    return int(words[value]) if value in words else None


def validate(request: Any, today: Optional[date] = None) -> ValidationResult:
    today = today or date.today()
    defaults = load_yaml("defaults")
    modes_cfg = load_yaml("modes")

    mode = _mode_of(request)
    if mode is None:
        return ValidationResult(None, None, make_error("invalid_request", "field 'mode' is required"))
    if mode not in modes_cfg["modes"]:
        return ValidationResult(
            None, None, make_error("invalid_request", f"field 'mode' must be one of {sorted(modes_cfg['modes'])}")
        )

    message = _schema_validate(request, mode)
    if message:
        return ValidationResult(None, None, make_error("invalid_request", message))

    normalized: Dict[str, Any] = dict(request)
    defaults_applied: List[str] = []
    missing: List[Tuple[str, str]] = []

    def apply_default(key: str, value: Any) -> None:
        if normalized.get(key) is None:
            normalized[key] = value
            defaults_applied.append(key)

    if mode in SEARCH_MODES:
        count = _resolve_result_count(request.get("result_count"), defaults)
        if count is None:
            missing.append(("result_count", "unrecognized quantity word"))
        else:
            if request.get("result_count") is None:
                defaults_applied.append("result_count")
            normalized["result_count"] = count
        year_from = request.get("year_from")
        if year_from is not None and int(year_from) > today.year:
            missing.append(("year_from", "start year is in the future"))
        for slot in request.get("unresolved_filters") or []:
            missing.append((slot, "restriction mentioned without a value"))
        apply_default("language", defaults["language"])
        apply_default("document_type", defaults["document_type"])
        apply_default("download", False)
        apply_default("outdir", defaults["outdir"])
        if mode == "KEYWORD_SEARCH":
            normalized["query"] = request["query"].strip()
            apply_default("query_is_scopus_syntax", False)
        if mode == "TOPIC_SEARCH":
            normalized["concepts"] = [
                {"slot": c["slot"], "term": c["term"].strip()} for c in request["concepts"] if c["term"].strip()
            ]
            if not normalized["concepts"]:
                missing.append(("concepts", "no non-empty concept term"))

    elif mode == "DOI_DOWNLOAD":
        valid: List[str] = []
        invalid: List[Dict[str, str]] = []
        seen = set()
        for raw in request["dois"]:
            doi = normalize_doi(raw)
            if not is_valid_doi(doi):
                invalid.append({"input": raw, "reason": "not a DOI (expected 10.xxxx/...)"})
                continue
            if doi.lower() in seen:
                continue
            seen.add(doi.lower())
            valid.append(doi)
        normalized["dois"] = valid
        normalized["invalid_dois"] = invalid
        if not valid:
            missing.append(("dois", "no valid DOI in the list"))
        apply_default("outdir", defaults["outdir"])

    elif mode == "TITLE_DOWNLOAD":
        titles = []
        seen_titles = set()
        for raw in request["titles"]:
            title = " ".join(raw.split())
            if title and title.lower() not in seen_titles:
                seen_titles.add(title.lower())
                titles.append(title)
        normalized["titles"] = titles
        if not titles:
            missing.append(("titles", "no non-empty title"))
        apply_default("outdir", defaults["outdir"])

    elif mode in ANALYSIS_MODES:
        apply_default("workdir", defaults["workdir"])

    normalized["defaults_applied"] = defaults_applied
    if missing:
        return ValidationResult(normalized, make_clarification(missing), None)
    return ValidationResult(normalized, None, None)
