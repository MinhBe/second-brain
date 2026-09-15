"""Per-outdir manifest so a rerun skips verified downloads. Deterministic file: no timestamps."""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

VERSION = 1


def manifest_path(outdir: Path, cfg: Dict[str, Any]) -> Path:
    return Path(outdir) / cfg["manifest"].get("filename", ".acquired.json")


def load_manifest(outdir: Path, cfg: Dict[str, Any]) -> Dict[str, Any]:
    path = manifest_path(outdir, cfg)
    if not path.is_file():
        return {"version": VERSION, "items": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or not isinstance(data.get("items"), dict):
            raise ValueError("bad manifest")
        return data
    except (OSError, ValueError):
        return {"version": VERSION, "items": {}}


def save_manifest(outdir: Path, manifest: Dict[str, Any], cfg: Dict[str, Any]) -> None:
    path = manifest_path(outdir, cfg)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(tmp, path)


def lookup(manifest: Dict[str, Any], doi: str, cfg: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Return the entry only if the file still exists, verifies, and its sha256 matches."""
    from lib.acquire import verify_pdf

    entry = manifest["items"].get(doi.lower())
    if not entry:
        return None
    check = verify_pdf(entry.get("path"), cfg)
    if not check["ok"] or (entry.get("sha256") and check["sha256"] != entry["sha256"]):
        return None
    return entry


def record(manifest: Dict[str, Any], item: Dict[str, Any]) -> None:
    manifest["items"][item["doi"].lower()] = {
        "doi": item["doi"],
        "path": item["path"],
        "sha256": item["sha256"],
        "title": item.get("title"),
        "method": item.get("method"),
        "version": item.get("version") or "published",
    }
