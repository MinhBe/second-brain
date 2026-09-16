from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import shutil
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path


LANGUAGE_ROOT = Path(__file__).resolve().parents[1]
CATALOG_DIR = LANGUAGE_ROOT / "_catalog"
GLOSSIKA_ROOT = LANGUAGE_ROOT / "Glossika"


@dataclass
class MoveAction:
    kind: str
    source: str
    target: str
    reason: str


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(LANGUAGE_ROOT))
    except ValueError:
        return str(path)


def inventory(root: Path = LANGUAGE_ROOT) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in sorted(root.rglob("*")):
        if path == CATALOG_DIR or CATALOG_DIR in path.parents:
            continue
        if path.is_dir():
            continue
        suffix = path.suffix.lower()
        provider = "Glossika" if "glossika" in str(path).lower() or "gms" in str(path).lower() else ""
        rows.append({
            "path": str(path),
            "relative_path": rel(path),
            "name": path.name,
            "extension": suffix,
            "size": str(path.stat().st_size),
            "provider_guess": provider,
        })
    return rows


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_json(path: Path, data) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def add(action_list: list[MoveAction], source: Path, target: Path, reason: str) -> None:
    if source.exists():
        action_list.append(MoveAction("move", str(source), str(target), reason))


def pdf_in(folder: Path) -> list[Path]:
    return sorted(folder.glob("*.pdf"))


def djvu_in(folder: Path) -> list[Path]:
    return sorted(folder.glob("*.djvu"))


def build_plan() -> list[MoveAction]:
    actions: list[MoveAction] = []

    chinese_complete = LANGUAGE_ROOT / "Chinese (Mandarin) Complete Fluency Course - 2014"
    for vol in [1, 2, 3]:
        src_vol = chinese_complete / str(vol)
        dst = GLOSSIKA_ROOT / "Chinese" / "Complete Fluency" / f"Glossika Chinese Complete Fluency {vol}"
        for src in pdf_in(src_vol):
            add(actions, src, dst / f"Glossika Chinese Complete Fluency {vol}.pdf", "rename Chinese Complete Fluency PDF")
        for src in djvu_in(src_vol):
            add(actions, src, dst / f"Glossika Chinese Complete Fluency {vol}.djvu", "rename Chinese Complete Fluency DJVU")
        add(actions, src_vol / "GMS", dst / "Audio" / "GMS", "move simplified Mandarin audio")
        add(actions, src_vol / "GMS-UPDATE", dst / "Audio" / "GMS-UPDATE", "move traditional Mandarin update audio")
    add(actions, chinese_complete / "anki_build", GLOSSIKA_ROOT / "Chinese" / "Complete Fluency" / "_derived" / "anki_build", "move Anki build artifacts")

    business = LANGUAGE_ROOT / "Chinese Mandarine Complete Fluency Course. Business 1 - 2014"
    business_dst = GLOSSIKA_ROOT / "Chinese" / "Business" / "Glossika Chinese Business 1"
    for src in pdf_in(business):
        add(actions, src, business_dst / "Glossika Chinese Business 1.pdf", "rename Chinese Business 1 PDF")
    add(actions, business / "Audio", business_dst / "Audio", "move Chinese Business 1 audio")

    daily = LANGUAGE_ROOT / "Chinese Mandarine Complete Fluency Course. Daily Life - 2014"
    daily_root = GLOSSIKA_ROOT / "Chinese" / "Daily Life"
    books = daily / "Books"
    gms = daily / "GMS"
    intro_pdf = books / "GLOSSIKA-DAILY-ENZH-INTRO.unlocked.pdf"
    add(actions, intro_pdf, daily_root / "Glossika Chinese Daily Life Intro" / "Glossika Chinese Daily Life Intro.pdf", "rename Daily Life intro PDF")
    for idx in range(1, 21):
        lesson = f"{idx:02d}"
        lesson_dst = daily_root / f"Glossika Chinese Daily Life {lesson}"
        add(actions, books / f"GLOSSIKA-DAILY-ENZH-{lesson}.unlocked.pdf", lesson_dst / f"Glossika Chinese Daily Life {lesson}.pdf", "rename Daily Life lesson PDF")
        lesson_audio = [p for p in sorted(gms.glob(f"GLOSSIKA-DAILY-ENZH-{lesson}*.mp3"))]
        if lesson_audio:
            # Move individual files so each lesson owns its A/B/C audio.
            for src in lesson_audio:
                add(actions, src, lesson_dst / "Audio" / src.name, "move Daily Life lesson audio")

    japanese = LANGUAGE_ROOT / "Campbell M., Shirakawa - Japanese Complete Fluency Course - 2015"
    for vol in [1, 2, 3]:
        src_vol = japanese / str(vol)
        dst = GLOSSIKA_ROOT / "Japanese" / "Complete Fluency" / f"Glossika Japanese Complete Fluency {vol}"
        for src in pdf_in(src_vol):
            add(actions, src, dst / f"Glossika Japanese Complete Fluency {vol}.pdf", "rename Japanese Complete Fluency PDF")
        add(actions, src_vol / "Audio 1", dst / "Audio" / "Audio 1", "move Japanese Audio 1")
        add(actions, src_vol / "Audio 2", dst / "Audio" / "Audio 2", "move Japanese Audio 2")

    korean = LANGUAGE_ROOT / "Campbell M., Dahye J. - Glossika Korean. Complete Fluency Course - 2016"
    for vol in [1, 2, 3]:
        src_vol = korean / str(vol)
        dst = GLOSSIKA_ROOT / "Korean" / "Complete Fluency" / f"Glossika Korean Complete Fluency {vol}"
        for src in pdf_in(src_vol):
            add(actions, src, dst / f"Glossika Korean Complete Fluency {vol}.pdf", "rename Korean Complete Fluency PDF")
        add(actions, src_vol / "GMS", dst / "Audio" / "GMS", "move Korean GMS audio")

    converted = LANGUAGE_ROOT / "_converted_pdf_text"
    add(actions, converted, GLOSSIKA_ROOT / "_derived" / "converted_pdf_text", "move converted text artifacts")
    output_pdf = LANGUAGE_ROOT / "output" / "pdf"
    add(actions, output_pdf, GLOSSIKA_ROOT / "_derived" / "pdf_exports", "move PDF export artifacts")
    output_dir = LANGUAGE_ROOT / "output"
    if output_dir.exists() and not output_pdf.exists():
        add(actions, output_dir, GLOSSIKA_ROOT / "_derived" / "output", "move remaining output artifacts")

    for src in sorted(LANGUAGE_ROOT.glob("*")):
        if src.is_file() and src.suffix.lower() in {".zip", ".rar", ".7z", ".torrent"}:
            add(actions, src, GLOSSIKA_ROOT / "_archives" / src.name, "move Glossika archive/download metadata")

    return actions


def check_conflicts(actions: list[MoveAction]) -> list[dict[str, str]]:
    conflicts: list[dict[str, str]] = []
    seen_targets: dict[str, str] = {}
    for action in actions:
        src = Path(action.source)
        dst = Path(action.target)
        key = str(dst).lower()
        if key in seen_targets:
            conflicts.append({"source": action.source, "target": action.target, "issue": f"duplicate target also used by {seen_targets[key]}"})
            continue
        seen_targets[key] = action.source
        if not src.exists():
            conflicts.append({"source": action.source, "target": action.target, "issue": "source missing"})
            continue
        if dst.exists():
            if src.is_dir() and not any(src.iterdir()):
                continue
            if src.is_file() and dst.is_file() and src.stat().st_size == dst.stat().st_size and file_sha256(src) == file_sha256(dst):
                conflicts.append({"source": action.source, "target": action.target, "issue": "target exists with identical file"})
            else:
                conflicts.append({"source": action.source, "target": action.target, "issue": "target exists"})
    return conflicts


def save_plan(actions: list[MoveAction], conflicts: list[dict[str, str]], stamp: str) -> tuple[Path, Path]:
    plan_csv = CATALOG_DIR / f"move_plan_{stamp}.csv"
    plan_json = CATALOG_DIR / f"move_plan_{stamp}.json"
    write_csv(plan_csv, [asdict(a) for a in actions], ["kind", "source", "target", "reason"])
    write_json(plan_json, [asdict(a) for a in actions])
    write_csv(CATALOG_DIR / f"conflicts_{stamp}.csv", conflicts, ["source", "target", "issue"])
    return plan_csv, plan_json


def load_plan(path: Path) -> list[MoveAction]:
    if path.suffix.lower() == ".json":
        return [MoveAction(**x) for x in json.loads(path.read_text(encoding="utf-8"))]
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [MoveAction(**row) for row in csv.DictReader(f)]


def apply_plan(actions: list[MoveAction]) -> None:
    conflicts = [c for c in check_conflicts(actions) if c["issue"] != "target exists with identical file"]
    if conflicts:
        write_csv(CATALOG_DIR / f"conflicts_apply_{timestamp()}.csv", conflicts, ["source", "target", "issue"])
        raise SystemExit(f"Refusing to apply plan with {len(conflicts)} conflict(s).")
    for action in actions:
        src = Path(action.source)
        dst = Path(action.target)
        if not src.exists():
            continue
        if dst.exists():
            if src.is_dir() and not any(src.iterdir()):
                try:
                    src.rmdir()
                except OSError:
                    pass
            continue
        ensure_dir(dst.parent)
        shutil.move(str(src), str(dst))
    remove_empty_known_dirs()


def remove_empty_known_dirs() -> None:
    candidates = [
        LANGUAGE_ROOT / "Chinese (Mandarin) Complete Fluency Course - 2014",
        LANGUAGE_ROOT / "Chinese Mandarine Complete Fluency Course. Business 1 - 2014",
        LANGUAGE_ROOT / "Chinese Mandarine Complete Fluency Course. Daily Life - 2014",
        LANGUAGE_ROOT / "Campbell M., Shirakawa - Japanese Complete Fluency Course - 2015",
        LANGUAGE_ROOT / "Campbell M., Dahye J. - Glossika Korean. Complete Fluency Course - 2016",
        LANGUAGE_ROOT / "output",
    ]
    for root in candidates:
        if not root.exists():
            continue
        for current, dirs, files in os.walk(root, topdown=False):
            path = Path(current)
            try:
                if not any(path.iterdir()):
                    path.rmdir()
            except OSError:
                pass


def command_scan(args: argparse.Namespace) -> None:
    stamp = timestamp()
    rows = inventory(Path(args.root))
    out = CATALOG_DIR / f"inventory_{stamp}.csv"
    write_csv(out, rows, ["path", "relative_path", "name", "extension", "size", "provider_guess"])
    print(f"Wrote {out}")
    print(f"Files: {len(rows)}")


def command_plan(args: argparse.Namespace) -> None:
    stamp = timestamp()
    actions = build_plan()
    conflicts = check_conflicts(actions)
    plan_csv, plan_json = save_plan(actions, conflicts, stamp)
    print(f"Actions: {len(actions)}")
    print(f"Conflicts: {len(conflicts)}")
    print(f"Plan CSV: {plan_csv}")
    print(f"Plan JSON: {plan_json}")


def command_apply(args: argparse.Namespace) -> None:
    stamp = timestamp()
    before = inventory(LANGUAGE_ROOT)
    write_csv(CATALOG_DIR / f"pre_move_inventory_{stamp}.csv", before, ["path", "relative_path", "name", "extension", "size", "provider_guess"])
    actions = load_plan(Path(args.plan))
    apply_plan(actions)
    after = inventory(LANGUAGE_ROOT)
    write_csv(CATALOG_DIR / f"post_move_inventory_{stamp}.csv", after, ["path", "relative_path", "name", "extension", "size", "provider_guess"])
    print(f"Applied actions: {len(actions)}")
    print(f"Files before: {len(before)}")
    print(f"Files after: {len(after)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Organize local language-course library.")
    parser.add_argument("--root", default=str(LANGUAGE_ROOT))
    sub = parser.add_subparsers(dest="command", required=True)
    scan = sub.add_parser("scan")
    scan.set_defaults(func=command_scan)
    plan = sub.add_parser("plan")
    plan.set_defaults(func=command_plan)
    apply_cmd = sub.add_parser("apply")
    apply_cmd.add_argument("--plan", required=True)
    apply_cmd.set_defaults(func=command_apply)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
