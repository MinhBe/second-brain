#!/usr/bin/env python3
"""Single entrypoint: python -X utf8 scripts/run.py --request request.json

Reads one JSON request, validates it, executes exactly the declared pipeline for its mode,
and prints one JSON envelope. Exit codes: 0 ok/partial, 1 error, 2 invalid_request,
3 clarification_required, 4 needs_evidence.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, Optional

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))


def _emit(payload: Dict[str, Any], out: Optional[str] = None) -> int:
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if out:
        Path(out).write_text(text, encoding="utf-8")
    print(text)
    from lib.output import exit_code_for

    return exit_code_for(payload["status"])


def _load_request(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def execute(request: Any, env: Optional[Dict[str, Any]] = None, deps: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Pure function used by run() and by tests. Never raises; always returns an envelope."""
    from lib.modes import MODE_HANDLERS, EvidenceInvalid, ModeError
    from lib.output import envelope, make_error
    from lib.validate_request import validate

    if env is None:  # real CLI run: fill UNPAYWALL_EMAIL / ELSEVIER_API_KEY from the Windows registry (setx) when missing
        from lib.env import resolved_env

        env = resolved_env(dict(os.environ))
    deps = deps or {}

    checked = validate(request, today=deps.get("today"))
    mode = request.get("mode") if isinstance(request, dict) else None
    if checked.error:
        return envelope(mode, "invalid_request", request if isinstance(request, dict) else None, error=checked.error)
    if checked.clarification:
        return envelope(mode, "clarification_required", checked.normalized, clarification=checked.clarification)

    normalized = checked.normalized
    try:
        status, result, next_command = MODE_HANDLERS[mode](normalized, env, deps)
        return envelope(mode, status, normalized, result=result, next_command=next_command)
    except EvidenceInvalid as exc:
        err = make_error("evidence_invalid", "evidence file rejected; fix result.validation.errors and rerun the same command")
        return envelope(mode, "error", normalized, result=exc.result, error=err)
    except ModeError as exc:
        return envelope(mode, "error", normalized, error=make_error(exc.code, exc.message))
    except ImportError as exc:
        return envelope(mode, "error", normalized, error=make_error("missing_dependency", f"missing Python package: {exc.name or exc}"))
    except RuntimeError as exc:
        text = str(exc)
        m = re.search(r"HTTP (\d{3})", text)
        code = f"scopus_http_{m.group(1)}" if m and "Scopus" in text else "network_error"
        return envelope(mode, "error", normalized, error=make_error(code, text[:500]))
    except Exception as exc:  # noqa: BLE001 - never leak a traceback to the model
        return envelope(mode, "error", normalized, error=make_error("internal_error", f"{type(exc).__name__}: {exc}"[:500]))


def main(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(description="Strict scientific paper research runner")
    parser.add_argument("--request", required=True, help="Path to request.json")
    parser.add_argument("--out", help="Also write the JSON envelope to this file")
    parser.add_argument("--report", help="Write a Markdown acquisition report (download modes) to this path")
    args = parser.parse_args(argv)

    try:
        from lib.output import envelope, make_error  # noqa: F401  (also checks lib imports)
    except ImportError as exc:
        payload = {"mode": None, "status": "error", "request": None, "result": None, "clarification": None,
                   "error": {"code": "missing_dependency", "message": f"missing Python package: {exc.name or exc}",
                             "setup_hint": "pip install pyyaml jsonschema pymupdf (see references/setup.md)"},
                   "next_command": None, "contract_version": "1.0"}
        print(json.dumps(payload, indent=2))
        return 1

    try:
        request = _load_request(args.request)
    except (OSError, json.JSONDecodeError) as exc:
        return _emit(envelope(None, "invalid_request", error=make_error("invalid_request", f"cannot read request file: {exc}")), args.out)

    payload = execute(request)
    if args.report and payload["status"] in ("ok", "partial"):
        try:
            from lib.report import collect_items, write_report

            if payload["mode"] in ("DOI_DOWNLOAD", "TITLE_DOWNLOAD") or collect_items(payload):
                write_report(payload, args.report)
        except Exception as exc:  # noqa: BLE001 - a report problem never changes the envelope
            print(f"report_error: {exc}", file=sys.stderr)
    return _emit(payload, args.out)


if __name__ == "__main__":
    raise SystemExit(main())
