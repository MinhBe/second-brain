"""Fixed output envelope, exit codes, error and clarification objects."""

from typing import Any, Dict, List, Optional, Sequence, Tuple

from lib.config import CONTRACT_VERSION, load_yaml

SETUP_HINTS = {
    "missing_env_ELSEVIER_API_KEY": "Set ELSEVIER_API_KEY (see references/setup.md).",
    "scopus_syntax_requires_key": "Set ELSEVIER_API_KEY, or set query_is_scopus_syntax to false so OpenAlex can run the query.",
    "missing_dependency": "pip install pyyaml jsonschema pymupdf (see references/setup.md).",
}


def envelope(
    mode: Optional[str],
    status: str,
    request: Optional[Dict[str, Any]] = None,
    result: Optional[Dict[str, Any]] = None,
    clarification: Optional[Dict[str, Any]] = None,
    error: Optional[Dict[str, Any]] = None,
    next_command: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        "mode": mode,
        "status": status,
        "request": request,
        "result": result,
        "clarification": clarification,
        "error": error,
        "next_command": next_command,
        "contract_version": CONTRACT_VERSION,
    }


def exit_code_for(status: str) -> int:
    codes = load_yaml("output-contracts")["exit_codes"]
    return int(codes.get(status, 1))


def make_error(code: str, message: str, setup_hint: Optional[str] = None) -> Dict[str, Any]:
    return {"code": code, "message": message, "setup_hint": setup_hint or SETUP_HINTS.get(code)}


def make_clarification(missing: Sequence[Tuple[str, str]]) -> Dict[str, Any]:
    """missing: sequence of (field, reason). The ask text is fixed in modes.yaml."""
    asks = load_yaml("modes")["clarifications"]
    items: List[Dict[str, str]] = []
    for field, reason in missing:
        items.append({"field": field, "reason": reason, "ask": asks.get(field, f"Please provide '{field}'.")})
    return {"missing": items, "relay_verbatim": " ".join(item["ask"] for item in items)}
