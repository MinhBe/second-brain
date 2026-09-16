"""Deterministic Markdown report for download results. Pure function of the output envelope."""

from pathlib import Path
from typing import Any, Dict, List

from lib.config import load_yaml

ACTION = {
    "blocked_403": "The publisher CDN rejects non-browser clients. Open a manual URL in a real browser and save the PDF.",
    "blocked_challenge": "The publisher serves a JavaScript challenge that only a real browser can pass. Open the link in your browser and save the PDF.",
    "ssl_error": "The host's TLS certificate could not be verified even after retry. Open a manual URL in a browser.",
    "invalid_pdf": "Every candidate URL returned a web page instead of a PDF. Open a manual URL in a browser.",
    "network": "A network or server error occurred. Rerun later; verified downloads are skipped automatically.",
    "subscription_only": "No open-access copy exists. Use a library subscription, VPN, or contact the authors.",
    "no_oa": "No open-access location was found. Check the manual URLs; the paper may be paywalled.",
    "not_found": "The DOI is unknown to every lookup service. Check the DOI for typos.",
}
MANUAL_CLASSES = ("blocked_403", "blocked_challenge", "ssl_error", "invalid_pdf", "network", "no_oa")


def _row(cells: List[Any]) -> str:
    return "| " + " | ".join(str(c if c is not None else "").replace("|", "\\|").replace("\n", " ") for c in cells) + " |"


def collect_items(envelope: Dict[str, Any]) -> List[Dict[str, Any]]:
    result = envelope.get("result") or {}
    mode = envelope.get("mode")
    if mode == "DOI_DOWNLOAD":
        return list(result.get("items") or [])
    if mode == "TITLE_DOWNLOAD":
        return [t["acquisition"] for t in result.get("items") or [] if t.get("acquisition")]
    acq = result.get("acquisition") or {}
    return list(acq.get("items") or [])


def _outdir(envelope: Dict[str, Any]) -> str:
    return str(((envelope.get("request") or {}).get("outdir")) or "./downloads")


def render_report(envelope: Dict[str, Any]) -> str:
    classes = load_yaml("output-contracts")["failure_classes"]
    mode = envelope.get("mode")
    result = envelope.get("result") or {}
    items = collect_items(envelope)
    downloaded = [i for i in items if i["status"] == "downloaded"]
    cached = [i for i in downloaded if i.get("method") == "cache"]
    failed = [i for i in items if i["status"] != "downloaded"]

    lines: List[str] = ["# Acquisition report", "", "## Summary", ""]
    lines.append(_row(["mode", "status", "requested", "downloaded", "from cache", "failed"]))
    lines.append(_row(["---", "---", "---", "---", "---", "---"]))
    requested = result.get("requested_count", len(items))
    lines.append(_row([mode, envelope.get("status"), requested, len(downloaded), len(cached), len(failed)]))
    if failed:
        lines += ["", "Failures by class:", ""]
        for cls in classes:
            n = sum(1 for i in failed if i.get("failure_class") == cls)
            if n:
                lines.append(f"- `{cls}`: {n}")

    lines += ["", "## Downloaded", ""]
    if downloaded:
        lines.append(_row(["#", "title / DOI", "method", "path", "sha256"]))
        lines.append(_row(["---", "---", "---", "---", "---"]))
        for idx, i in enumerate(downloaded, 1):
            label = (i.get("title") or i["doi"]) + (" (preprint)" if i.get("version") == "preprint" else "")
            lines.append(_row([idx, label, i.get("method"), i.get("path"), (i.get("sha256") or "")[:12]]))
        preprints = [i for i in downloaded if i.get("version") == "preprint"]
        if preprints:
            lines += ["", f"{len(preprints)} file(s) marked (preprint) are arXiv preprints, not the published version of record."]
    else:
        lines.append("None.")

    lines += ["", "## Failed", ""]
    if not failed:
        lines.append("None.")
    for cls in classes:
        group = [i for i in failed if i.get("failure_class") == cls]
        if not group:
            continue
        lines += [f"### {cls} ({len(group)})", "", ACTION.get(cls, ""), ""]
        for i in group:
            lines.append(f"- `{i['doi']}` {i.get('title') or ''}".rstrip())
            lines.append(f"  - error: {i.get('error')}")
            if i.get("warnings"):
                lines.append(f"  - warnings: {', '.join(i['warnings'])}")
            for url in i.get("manual_urls") or []:
                lines.append(f"  - <{url}>")
        lines.append("")

    manual = [i for i in failed if i.get("failure_class") in MANUAL_CLASSES]
    if manual:
        lines += ["## Manual download", ""]
        lines.append(_row(["#", "DOI", "save as", "open"]))
        lines.append(_row(["---", "---", "---", "---"]))
        for idx, i in enumerate(manual, 1):
            first = (i.get("manual_urls") or [f"https://doi.org/{i['doi']}"])[0]
            lines.append(_row([idx, f"`{i['doi']}`", f"`{i.get('expected_filename') or ''}`", f"<{first}>"]))
        lines += [
            "",
            "1. Open the link in a real browser and download the PDF.",
            f"2. Save it into `{_outdir(envelope)}` using exactly the `save as` name.",
            "3. Run the same command again: the file is verified and adopted (`method: cache`); only remaining failures are retried.",
            "",
        ]
        subs = [i for i in failed if i.get("failure_class") == "subscription_only"]
        if subs:
            lines.append(f"{len(subs)} paper(s) are subscription-only and need library access or the authors; they are not listed above.")
            lines.append("")

    if mode == "TITLE_DOWNLOAD":
        unresolved = [t for t in result.get("items") or [] if t.get("resolution") != "exact"]
        lines += ["## Unresolved titles", ""]
        if not unresolved:
            lines.append("None.")
        for t in unresolved:
            lines.append(f"- {t['input_title']} ({t['resolution']}, provider: {t.get('provider')})")
            for c in t.get("candidates") or []:
                lines.append(f"  - candidate: {c.get('title')} | {c.get('doi')} | {c.get('year')}")
            s = t.get("suggestion")
            if s:
                lines.append(f"  - suggested: `{s['doi']}` ({s['rule']} match) - not downloaded; add it to a DOI_DOWNLOAD request to fetch it")
        lines.append("")

    invalid = result.get("invalid_dois") or []
    if invalid:
        lines += ["## Invalid DOIs", ""]
        for d in invalid:
            lines.append(f"- `{d['input']}`: {d['reason']}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def write_report(envelope: Dict[str, Any], path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(render_report(envelope), encoding="utf-8")
