"""Evidence validation: schema + provenance rules + quote-in-text check. Step 2 of PAPER_ANALYSIS."""

import re
from typing import Any, Dict, List, Optional

from lib.config import load_schema, load_yaml

SOURCES = ("metadata", "abstract", "full_text")


def _norm(value: str) -> str:
    return re.sub(r"\s+", " ", (value or "")).strip().lower()


def _err(code: str, field: Optional[str], message: str) -> Dict[str, Any]:
    return {"code": code, "field": field, "message": message}


def _sections_named(sections: List[Dict[str, Any]], name: str) -> List[Dict[str, Any]]:
    wanted = _norm(name)
    return [s for s in sections if _norm(s.get("canonical", "")) == wanted or _norm(s.get("name", "")) == wanted]


def validate_evidence(
    evidence: Any,
    sections: List[Dict[str, Any]],
    text: str,
    evidence_level: str,
    defaults: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """Return a list of fixed-code errors. Empty list means the evidence file is accepted."""
    import jsonschema

    defaults = defaults if defaults is not None else load_yaml("defaults")
    quote_min = int(defaults["analysis"]["quote_min_chars"])
    errors: List[Dict[str, Any]] = []

    schema = load_schema("evidence")
    if not isinstance(evidence, dict):
        return [_err("schema_violation", None, "evidence must be a JSON object")]
    expected = set(schema["properties"])
    for f in sorted(expected - set(evidence)):
        errors.append(_err("missing_field", f, f"field '{f}' is missing"))
    for f in sorted(set(evidence) - expected):
        errors.append(_err("extra_field", f, f"field '{f}' is not in the evidence schema"))

    bad_fields = set()
    for err in jsonschema.Draft202012Validator(schema).iter_errors(evidence):
        field = str(err.absolute_path[0]) if err.absolute_path else None
        if field is None and err.validator in ("required", "additionalProperties"):
            continue  # already reported as missing_field / extra_field
        if field in bad_fields:
            continue  # one fixed error per field
        bad_fields.add(field)
        inst = evidence.get(field) if field else None
        src = inst.get("source") if isinstance(inst, dict) else None
        if src is not None and src not in SOURCES:
            errors.append(_err("source_forbidden", field, f"source '{src}' is not allowed; use metadata|abstract|full_text"))
        else:
            errors.append(_err("schema_violation", field, err.message))

    has_abstract = any(s.get("canonical") == "abstract" for s in sections)
    for field, item in evidence.items():
        if field in bad_fields or field not in expected:
            continue
        status, value, source, location = item["status"], item["value"], item["source"], item["location"]
        if status == "found":
            if value is None:
                errors.append(_err("found_without_value", field, "status is 'found' but value is null"))
            if source is None:
                errors.append(_err("found_without_source", field, "status is 'found' but source is null"))
            if location is None:
                errors.append(_err("found_without_location", field, "status is 'found' but location is null"))
            if errors and errors[-1]["field"] == field:
                continue
            if source == "full_text" and evidence_level != "full_text":
                errors.append(_err("source_exceeds_evidence_level", field, f"source 'full_text' not allowed at evidence_level '{evidence_level}'"))
                continue
            if source == "abstract" and not has_abstract:
                errors.append(_err("source_exceeds_evidence_level", field, "source 'abstract' but no abstract section was detected"))
                continue
            spans = _sections_named(sections, location["section"])
            if not spans:
                errors.append(_err("section_unknown", field, f"section '{location['section']}' was not detected in the paper"))
                continue
            quote = _norm(location["quote"])
            if len(quote) < quote_min:
                errors.append(_err("quote_not_in_text", field, f"quote shorter than {quote_min} characters"))
                continue
            if not any(quote in _norm(text[s["char_start"]:s["char_end"]]) for s in spans):
                errors.append(_err("quote_not_in_text", field, "quote is not a verbatim substring of the named section"))
        else:
            if value is not None:
                errors.append(_err("not_found_with_value", field, "status is 'not_found' but value is set"))
            if source is not None:
                errors.append(_err("not_found_with_source", field, "status is 'not_found' but source is set"))
            if location is not None:
                errors.append(_err("not_found_with_source", field, "status is 'not_found' but location is set"))
    return errors
