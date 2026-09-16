#!/usr/bin/env python
"""
Fallback path for YouTube videos whose caption endpoint is rate-limited.

Reads an existing _reports/selected_videos.csv, downloads a low-resolution
media stream, transcribes it with FFmpeg's whisper.cpp filter, and writes the
same Markdown structure as channel_to_markdown.py.
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from channel_to_markdown import VideoRecord, sanitize_filename, write_markdown

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def read_selected(report_path: Path) -> list[VideoRecord]:
    videos: list[VideoRecord] = []
    with report_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            categories = [item for item in (row.get("categories") or "").split("|") if item]
            if not categories:
                continue
            video_id = row.get("video_id") or ""
            title = row.get("title") or video_id
            url = row.get("url") or f"https://www.youtube.com/watch?v={video_id}"
            if video_id:
                videos.append(VideoRecord(video_id, title, url, categories))
    return videos


def markdown_targets(output_root: Path, video: VideoRecord) -> list[Path]:
    filename = sanitize_filename(f"{video.title} [{video.video_id}]") + ".md"
    return [output_root / category / filename for category in video.categories]


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def append_report(path: Path, row: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "timestamp",
        "video_id",
        "title",
        "url",
        "categories",
        "status",
        "media_path",
        "transcript_path",
        "detail",
    ]
    write_header = not path.exists()
    with path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        if write_header:
            writer.writeheader()
        writer.writerow(row)


def run_command(args: list[str], cwd: Path, timeout: int | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=str(cwd),
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
    )


def find_media(media_dir: Path, video_id: str) -> Path | None:
    matches = sorted(media_dir.glob(f"{video_id}.*"))
    return matches[0] if matches else None


def download_media(workspace: Path, media_dir: Path, video: VideoRecord) -> Path:
    existing = find_media(media_dir, video.video_id)
    if existing:
        return existing

    media_dir.mkdir(parents=True, exist_ok=True)
    outtmpl = str((media_dir / "%(id)s.%(ext)s").as_posix())
    cmd = [
        sys.executable,
        "-m",
        "yt_dlp",
        "--extractor-args",
        "youtube:player_client=android",
        "-f",
        "18/bestaudio/best",
        "--no-playlist",
        "--no-overwrites",
        "--output",
        outtmpl,
        video.url,
    ]
    completed = run_command(cmd, workspace)
    if completed.returncode != 0:
        raise RuntimeError(completed.stdout.strip()[-4000:])

    downloaded = find_media(media_dir, video.video_id)
    if not downloaded:
        raise FileNotFoundError(f"yt-dlp completed but no media file was found for {video.video_id}")
    return downloaded


def to_filter_path(path: Path) -> str:
    return path.as_posix()


def transcribe_media(
    workspace: Path,
    media_path: Path,
    transcript_path: Path,
    model_path: Path,
    language: str,
    use_gpu: bool,
) -> str:
    if transcript_path.exists() and transcript_path.stat().st_size > 0:
        return transcript_path.read_text(encoding="utf-8", errors="replace").strip()

    transcript_path.parent.mkdir(parents=True, exist_ok=True)
    whisper_args = [
        f"model={to_filter_path(model_path)}",
        f"language={language}",
        "format=text",
        f"destination={to_filter_path(transcript_path)}",
        f"use_gpu={'true' if use_gpu else 'false'}",
    ]
    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-nostdin",
        "-y",
        "-i",
        str(media_path),
        "-af",
        "whisper=" + ":".join(whisper_args),
        "-f",
        "null",
        "NUL",
    ]
    completed = run_command(cmd, workspace)
    if completed.returncode != 0:
        raise RuntimeError(completed.stdout.strip()[-4000:])

    text = transcript_path.read_text(encoding="utf-8", errors="replace").strip()
    if not text:
        raise RuntimeError("ffmpeg whisper completed but transcript file is empty")
    return text


def process_video(args: argparse.Namespace, workspace: Path, video: VideoRecord, state: dict) -> str:
    targets = markdown_targets(args.output_root, video)
    missing_targets = [target for target in targets if args.force or not target.exists()]
    if not missing_targets:
        return "already_done"

    media_dir = args.output_root / "_media"
    transcript_dir = args.output_root / "_reports" / "audio_fallback_transcripts"
    media_path = download_media(workspace, media_dir, video)
    transcript_path = transcript_dir / f"{video.video_id}.txt"
    transcript = transcribe_media(
        workspace=workspace,
        media_path=media_path,
        transcript_path=transcript_path,
        model_path=args.model,
        language=args.language,
        use_gpu=not args.no_gpu,
    )

    for target in missing_targets:
        write_markdown(
            target,
            video,
            transcript,
            f"ffmpeg-whisper:{args.model.stem}",
            args.language,
        )

    state.setdefault("videos", {})[video.video_id] = {
        "status": "transcribed",
        "title": video.title,
        "url": video.url,
        "categories": video.categories,
        "media_path": str(media_path),
        "transcript_path": str(transcript_path),
        "updated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }
    return "transcribed"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--selected-report", type=Path)
    parser.add_argument("--model", default=Path("models/ggml-base.bin"), type=Path)
    parser.add_argument("--language", default="vi")
    parser.add_argument("--max-videos", type=int)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--no-gpu", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    workspace = Path.cwd()
    args.output_root = args.output_root
    args.model = args.model
    selected_report = args.selected_report or (args.output_root / "_reports" / "selected_videos.csv")
    if not selected_report.exists():
        raise SystemExit(f"Missing selected report: {selected_report}")
    if not args.model.exists():
        raise SystemExit(f"Missing Whisper model: {args.model}")

    report_path = args.output_root / "_reports" / "audio_fallback.csv"
    checkpoint_path = args.output_root / "_reports" / "audio_fallback_checkpoint.json"
    state = load_json(checkpoint_path)
    videos = read_selected(selected_report)
    processed = 0

    for video in videos:
        targets = markdown_targets(args.output_root, video)
        if not args.force and all(target.exists() for target in targets):
            continue
        if args.max_videos is not None and processed >= args.max_videos:
            break

        timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        try:
            print(f"[audio-fallback] {video.video_id} | {video.title}", flush=True)
            status = process_video(args, workspace, video, state)
            save_json(checkpoint_path, state)
            append_report(
                report_path,
                {
                    "timestamp": timestamp,
                    "video_id": video.video_id,
                    "title": video.title,
                    "url": video.url,
                    "categories": "|".join(video.categories),
                    "status": status,
                    "media_path": state.get("videos", {}).get(video.video_id, {}).get("media_path", ""),
                    "transcript_path": state.get("videos", {}).get(video.video_id, {}).get("transcript_path", ""),
                    "detail": "",
                },
            )
            processed += 1
        except Exception as exc:
            state.setdefault("videos", {})[video.video_id] = {
                "status": "error",
                "title": video.title,
                "url": video.url,
                "categories": video.categories,
                "error": str(exc),
                "updated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            }
            save_json(checkpoint_path, state)
            append_report(
                report_path,
                {
                    "timestamp": timestamp,
                    "video_id": video.video_id,
                    "title": video.title,
                    "url": video.url,
                    "categories": "|".join(video.categories),
                    "status": "error",
                    "media_path": "",
                    "transcript_path": "",
                    "detail": str(exc)[:4000],
                },
            )
            print(f"[audio-fallback:error] {video.video_id}: {exc}", flush=True)
            processed += 1

    print(f"Processed via audio fallback this run: {processed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
