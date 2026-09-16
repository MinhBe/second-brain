#!/usr/bin/env python3
"""Unpaywall resolver + scihub-cli fallback (library, no CLI). Derived from sci-papers-downloder (MIT)."""

import json
import os
import re
import shlex
import shutil
import subprocess
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

UNPAYWALL_URL = "https://api.unpaywall.org/v2"
UVX_FALLBACK_CMD = [
    "uvx",
    "--from",
    "git+https://github.com/Oxidane-bot/scihub-cli.git",
    "scihub-cli",
]


@dataclass
class FallbackConfig:
    mode: str
    command: Optional[List[str]]
    email: Optional[str]
    timeout: int
    setup_error: Optional[str] = None
    extra_args: List[str] = field(default_factory=list)
    timeout_divisor: int = 3


def quote_doi(doi: str) -> str:
    return urllib.parse.quote(doi, safe="")


def unpaywall_lookup(doi: str, email: str, timeout: int, http_get=None, policy=None, base_url: str = UNPAYWALL_URL) -> Dict[str, Any]:
    from lib.http import HttpPolicy, get_json  # lazy: lib.http imports helpers from this module

    policy = policy or HttpPolicy(user_agent="scientific-paper-research/1.1 (mailto:{email})", alt_user_agent="", contact_email=email, timeout=timeout)
    url = f"{base_url}/{quote_doi(doi)}?email={urllib.parse.quote(email, safe='@._+-')}"
    return get_json(url, policy, http_get, timeout)


def unique_urls(urls: List[Optional[str]]) -> List[str]:
    out: List[str] = []
    seen = set()
    for url in urls:
        if not url:
            continue
        u = url.strip()
        if not u or u in seen:
            continue
        seen.add(u)
        out.append(u)
    return out


def build_candidate_urls(record: Dict[str, Any]) -> List[str]:
    best = record.get("best_oa_location") or {}
    urls: List[Optional[str]] = [
        best.get("url_for_pdf"),
        best.get("url"),
    ]

    for location in record.get("oa_locations") or []:
        urls.append(location.get("url_for_pdf"))
        urls.append(location.get("url"))

    return unique_urls(urls)


def maybe_extract_pdf_url_from_html(html_text: str) -> Optional[str]:
    """Fixed-order heuristics for a PDF link inside an HTML page. Returns the first hit."""
    q = "[\"']"
    nq = "[^\"']"
    patterns = [
        rf'<meta[^>]+name={q}citation_pdf_url{q}[^>]+content={q}({nq}+){q}',
        rf'<meta[^>]+content={q}({nq}+){q}[^>]+name={q}citation_pdf_url{q}',
        rf'<iframe[^>]+src={q}({nq}+\.pdf(?:\?{nq}*)?){q}',
        rf'<a[^>]+\bdownload\b[^>]*href={q}({nq}+){q}',
        rf'<a[^>]+href={q}({nq}+){q}[^>]*\sdownload[\s>=]',
        rf'href={q}({nq}*stampPDF/getPDF\.jsp{nq}*){q}',
        rf'href={q}({nq}+(?:\?download=true|/pdf\?{nq}*)){q}',
        rf'href={q}({nq}+\.pdf(?:\?{nq}*)?){q}',
    ]
    for pattern in patterns:
        m = re.search(pattern, html_text, re.I)
        if m:
            return m.group(1)
    return None


def is_pdf(data: bytes, content_type: str) -> bool:
    return data.startswith(b"%PDF") or "pdf" in (content_type or "").lower()


def safe_filename(value: str, default: str) -> str:
    text = value.strip() if value else ""
    if not text:
        text = default
    text = re.sub(r"[^A-Za-z0-9._-]+", "_", text)
    text = text.strip("._")
    if not text:
        text = default
    return text[:120]


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    for idx in range(2, 10000):
        candidate = parent / f"{stem}_{idx}{suffix}"
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"Could not allocate unique path for {path}")


def resolve_scihub_command(command_override: Optional[str]) -> Tuple[Optional[List[str]], Optional[str]]:
    if command_override:
        cmd = shlex.split(command_override)
        if not cmd:
            return None, "empty_scihub_cmd"
        first = cmd[0]
        if os.path.sep in first:
            if not Path(first).exists():
                return None, f"scihub_cmd_not_found: {first}"
            return cmd, None
        if shutil.which(first):
            return cmd, None
        return None, f"scihub_cmd_not_found: {first}"

    if shutil.which("scihub-cli"):
        return ["scihub-cli"], None

    if shutil.which("uvx"):
        return UVX_FALLBACK_CMD.copy(), None

    return None, "scihub_cli_not_found (install with: uv tool install git+https://github.com/Oxidane-bot/scihub-cli.git)"


def is_valid_pdf_file(path: Path) -> bool:
    try:
        with path.open("rb") as f:
            return f.read(4) == b"%PDF"
    except Exception:  # noqa: BLE001
        return False


def find_best_pdf(root: Path) -> Optional[Path]:
    pdfs = [p for p in root.rglob("*.pdf") if p.is_file()]
    if not pdfs:
        return None
    pdfs.sort(key=lambda p: p.stat().st_size, reverse=True)
    return pdfs[0]


def compact_log_tail(text: str, max_lines: int = 6) -> str:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if not lines:
        return ""
    tail = lines[-max_lines:]
    return " | ".join(tail)


def attempt_scihub_fallback(
    doi: str,
    outdir: Path,
    filename_base: str,
    fallback: FallbackConfig,
) -> Tuple[bool, Optional[str], Optional[str], Optional[str]]:
    if fallback.command is None:
        return False, None, None, fallback.setup_error or "scihub_fallback_not_available"

    with tempfile.TemporaryDirectory(prefix="scihub_fallback_") as td:
        tmp = Path(td)
        input_file = tmp / "input.txt"
        input_file.write_text(f"{doi}\n", encoding="utf-8")

        tmp_out = tmp / "out"
        tmp_out.mkdir(parents=True, exist_ok=True)

        cmd = list(fallback.command)
        cmd.extend([str(input_file), "-o", str(tmp_out), "-t", str(max(15, fallback.timeout // max(1, fallback.timeout_divisor)))])
        cmd.extend(list(fallback.extra_args))
        if fallback.email:
            cmd.extend(["--email", fallback.email])

        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=max(60, fallback.timeout),
                check=False,
            )
        except subprocess.TimeoutExpired:
            return False, None, None, f"scihub_cli_timeout_after_{max(60, fallback.timeout)}s"
        except Exception as exc:  # noqa: BLE001
            return False, None, None, f"scihub_cli_exec_error: {exc}"

        logs = "\n".join([proc.stdout or "", proc.stderr or ""])
        best_pdf = find_best_pdf(tmp_out)
        if not best_pdf:
            err_tail = compact_log_tail(logs)
            if proc.returncode != 0:
                return (
                    False,
                    None,
                    None,
                    f"scihub_cli_no_pdf_exit_{proc.returncode}: {err_tail or 'no_detail'}",
                )
            return False, None, None, f"scihub_cli_no_pdf: {err_tail or 'no_detail'}"

        if not is_valid_pdf_file(best_pdf):
            return False, None, None, "scihub_cli_invalid_pdf_header"

        target = unique_path(outdir / f"{filename_base}.pdf")
        shutil.copy2(best_pdf, target)

        m = re.search(r"Download URL:\s*(\S+)", logs)
        resolved = m.group(1) if m else None
        return True, str(target), resolved, None


