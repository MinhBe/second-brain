#!/usr/bin/env python
"""
Batch-download YouTube captions from a channel and export them to Markdown.

This script selects only videos related to speaking/writing, downloads the
best available caption track, cleans it, and writes the transcript to
Speaking/ and/or Writing/ folders under the chosen output root.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
import shutil
import time
import sys
import tempfile
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

try:
    import yt_dlp
except ImportError as exc:
    raise SystemExit(
        "Missing dependency: yt-dlp. Install it in the active environment first."
    ) from exc

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api.proxies import GenericProxyConfig
except ImportError:
    YouTubeTranscriptApi = None
    GenericProxyConfig = None


CHANNEL_URL_DEFAULT = "https://www.youtube.com/@bao-brian2568/videos"
DEFAULT_LANGS = ("vi-orig", "en-orig", "vi", "en")
NO_CAPTION_SKIP = "skip"
MAX_FILENAME_LENGTH = 110
STATUS_PENDING = "pending"
STATUS_DOWNLOADED = "downloaded"
STATUS_SKIPPED = "skipped_no_caption"
STATUS_BLOCKED = "blocked"
STATUS_ERROR = "error"

WRITING_BASE_KEYWORDS = (
    "writing",
    "write",
    "essay",
    "letter",
    "formal letter",
    "informal letter",
    "opinion essay",
    "cause & effect essay",
    "cause and effect essay",
    "task 2",
    "viet",
    "thu",
)

SPEAKING_BASE_KEYWORDS = (
    "speaking",
    "speak",
    "presentation",
    "task 1",
    "task 3",
    "part 1",
    "part 2",
    "part 3",
    "noi",
    "tra loi",
)

SHARED_CONTEXT_KEYWORDS = (
    "template",
    "mau cau",
    "vocabulary",
    "idiom",
    "mindmap",
    "topic",
    "health",
    "environment",
    "education",
    "technology",
    "transport",
    "languages",
)

SPEAKING_HINTS = ("speaking", "speak", "noi", "tra loi", "presentation")
WRITING_HINTS = ("writing", "write", "viet", "essay", "letter", "thu")
VSTEP_HINTS = ("vstep", "task", "part", "b1", "b2", "c1")


@dataclass
class VideoRecord:
    video_id: str
    title: str
    url: str
    categories: list[str]


@dataclass
class DownloadResult:
    text: str | None
    source: str | None
    language: str | None
    error: str | None


@dataclass
class RuntimeOptions:
    sleep_seconds: float
    stop_on_rate_limit: bool
    max_videos_per_run: int | None
    yt_dlp_proxy: str | None
    http_proxy: str | None
    https_proxy: str | None
    cookies_from_browser: str | None
    cookies_file: str | None
    resume: bool
    list_only: bool
    retry_blocked: bool
    preflight_check: bool


def normalize_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    stripped = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    stripped = stripped.lower()
    stripped = re.sub(r"[^a-z0-9]+", " ", stripped)
    return re.sub(r"\s+", " ", stripped).strip()


def sanitize_filename(value: str) -> str:
    collapsed = re.sub(r"\s+", " ", value).strip()
    safe = re.sub(r'[<>:"/\\|?*]', "-", collapsed)
    safe = re.sub(r"-{2,}", "-", safe).strip(" .-")
    if not safe:
        safe = "untitled"
    return safe[:MAX_FILENAME_LENGTH].rstrip(" .-")


def title_has_any(normalized_title: str, keywords: Iterable[str]) -> bool:
    return any(keyword in normalized_title for keyword in keywords)


def classify_title(title: str) -> list[str]:
    normalized = normalize_text(title)
    categories: list[str] = []

    if title_has_any(normalized, WRITING_BASE_KEYWORDS):
        categories.append("Writing")
    if title_has_any(normalized, SPEAKING_BASE_KEYWORDS):
        categories.append("Speaking")

    if title_has_any(normalized, SHARED_CONTEXT_KEYWORDS):
        has_speaking_context = title_has_any(normalized, SPEAKING_HINTS)
        has_writing_context = title_has_any(normalized, WRITING_HINTS)
        is_vstep_context = title_has_any(normalized, VSTEP_HINTS)

        if has_speaking_context or (is_vstep_context and not has_writing_context):
            if "Speaking" not in categories:
                categories.append("Speaking")
        if has_writing_context or (is_vstep_context and not has_speaking_context):
            if "Writing" not in categories:
                categories.append("Writing")

    return categories


def list_channel_videos(channel_url: str) -> list[dict]:
    options = {
        "extract_flat": "in_playlist",
        "quiet": True,
        "skip_download": True,
        "playlistend": None,
        "compat_opts": ["no-youtube-unavailable-videos"],
        "extractor_args": {"youtube": {"player_client": ["android"]}},
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(channel_url, download=False)
    entries = info.get("entries") or []
    return [entry for entry in entries if entry and entry.get("id") and entry.get("title")]


def is_rate_limited_or_blocked(error_text: str | None) -> bool:
    if not error_text:
        return False
    lowered = error_text.lower()
    indicators = (
        "http error 429",
        "too many requests",
        "ipblocked",
        "requestblocked",
        "youtube is blocking requests from your ip",
        "youtube is blocking your requests",
        "unable to download video subtitles",
    )
    return any(item in lowered for item in indicators)


def is_no_caption_error(error_text: str | None) -> bool:
    if not error_text:
        return False
    lowered = error_text.lower()
    indicators = (
        "no preferred caption track available",
        "transcript is disabled",
        "no transcript",
        "no subtitles",
        "could not find a transcript",
        "transcript api returned no usable text",
        "downloaded caption was empty after cleaning",
    )
    return any(item in lowered for item in indicators)


def export_selected_report(report_path: Path, videos: list[VideoRecord]) -> None:
    with report_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["video_id", "title", "url", "categories"])
        for video in videos:
            writer.writerow([video.video_id, video.title, video.url, "|".join(video.categories)])


def get_caption_inventory(url: str, yt_dlp_proxy: str | None = None) -> tuple[dict, dict]:
    options = {
        "quiet": True,
        "skip_download": True,
        "extractor_args": {"youtube": {"player_client": ["android"]}},
    }
    if yt_dlp_proxy:
        options["proxy"] = yt_dlp_proxy
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=False)
    return info.get("subtitles") or {}, info.get("automatic_captions") or {}


def choose_caption_track(
    subtitles: dict, auto_subtitles: dict, preferred_langs: list[str]
) -> tuple[str, bool] | None:
    for lang in preferred_langs:
        if lang in subtitles:
            return lang, False
    for lang in preferred_langs:
        if lang in auto_subtitles:
            return lang, True
    return None


def download_vtt(
    url: str,
    language: str,
    is_auto: bool,
    workspace: Path,
    yt_dlp_proxy: str | None = None,
    cookies_from_browser: str | None = None,
    cookies_file: str | None = None,
) -> Path:
    workspace.mkdir(parents=True, exist_ok=True)
    outtmpl = str(workspace / "caption")
    options = {
        "skip_download": True,
        "quiet": True,
        "no_warnings": True,
        "outtmpl": outtmpl,
        "subtitleslangs": [language],
        "subtitlesformat": "vtt",
        "writesubtitles": not is_auto,
        "writeautomaticsub": is_auto,
        "extractor_args": {"youtube": {"player_client": ["android"]}},
    }
    if yt_dlp_proxy:
        options["proxy"] = yt_dlp_proxy
    if cookies_from_browser:
        options["cookiesfrombrowser"] = (cookies_from_browser,)
    if cookies_file:
        options["cookiefile"] = cookies_file
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])

    matches = sorted(workspace.glob("*.vtt"))
    if not matches:
        raise FileNotFoundError(f"No VTT file created for language {language}")
    return matches[0]


def clean_vtt_text(vtt_text: str) -> str:
    lines: list[str] = []
    seen: set[str] = set()

    for raw_line in vtt_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")):
            continue
        if "-->" in line or re.fullmatch(r"\d+", line):
            continue

        line = re.sub(r"<[^>]+>", "", line)
        line = html.unescape(line).strip()
        if not line:
            continue
        if line in seen:
            continue

        seen.add(line)
        lines.append(line)

    return "\n".join(lines).strip()


def fetch_via_ytdlp(url: str, preferred_langs: list[str], runtime: RuntimeOptions) -> DownloadResult:
    try:
        subtitles, auto_subtitles = get_caption_inventory(url, runtime.yt_dlp_proxy)
        selected = choose_caption_track(subtitles, auto_subtitles, preferred_langs)
        if not selected:
            return DownloadResult(None, None, None, "No preferred caption track available")

        language, is_auto = selected
        with tempfile.TemporaryDirectory(prefix="yt_caps_") as temp_dir:
            vtt_path = download_vtt(
                url,
                language,
                is_auto,
                Path(temp_dir),
                runtime.yt_dlp_proxy,
                runtime.cookies_from_browser,
                runtime.cookies_file,
            )
            raw_text = vtt_path.read_text(encoding="utf-8", errors="replace")
        cleaned = clean_vtt_text(raw_text)
        if not cleaned:
            return DownloadResult(None, None, language, "Downloaded caption was empty after cleaning")
        source = "yt-dlp:auto" if is_auto else "yt-dlp:manual"
        return DownloadResult(cleaned, source, language, None)
    except Exception as exc:
        return DownloadResult(None, None, None, str(exc))


def build_proxy_config(runtime: RuntimeOptions):
    if GenericProxyConfig is None:
        return None
    if not runtime.http_proxy and not runtime.https_proxy:
        return None
    return GenericProxyConfig(
        http_url=runtime.http_proxy,
        https_url=runtime.https_proxy,
    )


def fetch_via_transcript_api(video_id: str, preferred_langs: list[str], runtime: RuntimeOptions) -> DownloadResult:
    if YouTubeTranscriptApi is None:
        return DownloadResult(None, None, None, "youtube-transcript-api is not installed")

    try:
        api = YouTubeTranscriptApi(proxy_config=build_proxy_config(runtime))
        transcript = api.fetch(video_id, languages=preferred_langs)
        snippets = []
        for snippet in transcript.snippets:
            text = " ".join(snippet.text.split())
            if text:
                snippets.append(text)

        cleaned = "\n".join(dict.fromkeys(snippets)).strip()
        if not cleaned:
            return DownloadResult(None, None, None, "Transcript API returned no usable text")

        language = getattr(transcript, "language_code", None)
        return DownloadResult(cleaned, "youtube-transcript-api", language, None)
    except Exception as exc:
        return DownloadResult(None, None, None, str(exc))


def write_markdown(
    destination: Path,
    video: VideoRecord,
    transcript: str,
    caption_source: str,
    caption_language: str | None,
) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    metadata = [
        f"# {video.title}",
        "",
        f"- Video ID: `{video.video_id}`",
        f"- URL: {video.url}",
        f"- Category: `{destination.parent.name}`",
        f"- Caption source: `{caption_source}`",
        f"- Caption language: `{caption_language or 'unknown'}`",
        f"- Downloaded at: `{timestamp}`",
        "",
        "## Transcript",
        "",
        transcript,
        "",
    ]
    destination.write_text("\n".join(metadata), encoding="utf-8")


def append_csv_row(path: Path, row: list[str]) -> None:
    write_header = not path.exists()
    with path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        if write_header:
            writer.writerow(
                [
                    "video_id",
                    "title",
                    "url",
                    "categories",
                    "caption_source",
                    "caption_language",
                    "detail",
                ]
            )
        writer.writerow(row)


def compact_detail(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def reset_output_dirs(root: Path) -> None:
    for dirname in ("Speaking", "Writing", "_reports"):
        target = root / dirname
        if target.exists():
            shutil.rmtree(target)
        target.mkdir(parents=True, exist_ok=True)


def checkpoint_path(reports_dir: Path) -> Path:
    return reports_dir / "checkpoint.json"


def load_checkpoint(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_checkpoint(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def build_checkpoint(videos: list[VideoRecord], channel_url: str, preferred_langs: list[str], runtime: RuntimeOptions) -> dict:
    return {
        "channel_url": channel_url,
        "preferred_languages": preferred_langs,
        "runtime": {
            "sleep_seconds": runtime.sleep_seconds,
            "stop_on_rate_limit": runtime.stop_on_rate_limit,
            "max_videos_per_run": runtime.max_videos_per_run,
        },
        "videos": {
            video.video_id: {
                "title": video.title,
                "url": video.url,
                "categories": video.categories,
                "status": STATUS_PENDING,
                "detail": "",
            }
            for video in videos
        },
    }


def update_checkpoint_status(checkpoint: dict, video: VideoRecord, status: str, detail: str = "") -> None:
    videos = checkpoint.setdefault("videos", {})
    record = videos.setdefault(
        video.video_id,
        {
            "title": video.title,
            "url": video.url,
            "categories": video.categories,
        },
    )
    record["status"] = status
    record["detail"] = compact_detail(detail) if detail else ""


def should_process_video(checkpoint: dict, video_id: str, resume: bool) -> bool:
    if not resume:
        return True
    record = checkpoint.get("videos", {}).get(video_id, {})
    return record.get("status", STATUS_PENDING) == STATUS_PENDING


def reset_blocked_to_pending(checkpoint: dict) -> int:
    reset_count = 0
    for record in checkpoint.get("videos", {}).values():
        if record.get("status") == STATUS_BLOCKED:
            record["status"] = STATUS_PENDING
            record["detail"] = ""
            reset_count += 1
    return reset_count


def summarize_checkpoint_statuses(checkpoint: dict) -> dict[str, int]:
    counts = {
        STATUS_PENDING: 0,
        STATUS_DOWNLOADED: 0,
        STATUS_SKIPPED: 0,
        STATUS_BLOCKED: 0,
        STATUS_ERROR: 0,
    }
    for record in checkpoint.get("videos", {}).values():
        status = record.get("status", STATUS_PENDING)
        counts[status] = counts.get(status, 0) + 1
    return counts


def write_summary(
    reports_dir: Path,
    channel_url: str,
    checkpoint: dict,
    processed_this_run: int,
    downloaded_this_run: int,
    preferred_langs: list[str],
    runtime: RuntimeOptions,
    preflight_status: str,
    preflight_detail: str = "",
) -> None:
    status_counts = summarize_checkpoint_statuses(checkpoint)
    summary = {
        "channel_url": channel_url,
        "selected_videos": len(checkpoint.get("videos", {})),
        "processed_this_run": processed_this_run,
        "downloaded_this_run": downloaded_this_run,
        "downloaded_total": status_counts.get(STATUS_DOWNLOADED, 0),
        "skipped_no_caption": count_csv_rows(reports_dir / "skipped_no_caption.csv"),
        "blocked": count_csv_rows(reports_dir / "blocked.csv"),
        "errors": count_csv_rows(reports_dir / "errors.csv"),
        "pending": status_counts.get(STATUS_PENDING, 0),
        "preferred_languages": preferred_langs,
        "resume_enabled": runtime.resume,
        "preflight_status": preflight_status,
    }
    if preflight_detail:
        summary["preflight_detail"] = compact_detail(preflight_detail)
    (reports_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


def run_preflight_probe(
    videos: list[VideoRecord],
    preferred_langs: list[str],
    runtime: RuntimeOptions,
) -> tuple[bool, str, VideoRecord | None, DownloadResult | None]:
    if not runtime.preflight_check or not videos:
        return True, "preflight_skipped", None, None

    probe_video = videos[0]
    result = fetch_via_ytdlp(probe_video.url, preferred_langs, runtime)
    if result.text:
        return True, "yt-dlp_ok", probe_video, result
    if is_rate_limited_or_blocked(result.error):
        return False, f"yt-dlp={result.error}", probe_video, None
    if is_no_caption_error(result.error):
        fallback = fetch_via_transcript_api(probe_video.video_id, preferred_langs, runtime)
        if fallback.text:
            return True, "transcript_api_ok", probe_video, fallback
        if is_rate_limited_or_blocked(fallback.error):
            return False, f"transcript_api={fallback.error}", probe_video, None
        return True, f"preflight_no_caption={fallback.error or result.error}", None, None

    fallback = fetch_via_transcript_api(probe_video.video_id, preferred_langs, runtime)
    if fallback.text:
        return True, "transcript_api_ok", probe_video, fallback
    if is_rate_limited_or_blocked(fallback.error):
        return False, f"transcript_api={fallback.error}", probe_video, None
    return True, f"preflight_nonblocking={fallback.error or result.error}", None, None


def process_channel(
    channel_url: str,
    output_root: Path,
    preferred_langs: list[str],
    no_caption_policy: str,
    runtime: RuntimeOptions,
) -> int:
    if runtime.resume:
        for dirname in ("Speaking", "Writing", "_reports"):
            (output_root / dirname).mkdir(parents=True, exist_ok=True)
    else:
        reset_output_dirs(output_root)
    speaking_dir = output_root / "Speaking"
    writing_dir = output_root / "Writing"
    reports_dir = output_root / "_reports"
    selected_report = reports_dir / "selected_videos.csv"
    downloaded_report = reports_dir / "downloaded.csv"
    skipped_report = reports_dir / "skipped_no_caption.csv"
    blocked_report = reports_dir / "blocked.csv"
    errors_report = reports_dir / "errors.csv"
    state_file = checkpoint_path(reports_dir)

    entries = list_channel_videos(channel_url)
    selected_videos: list[VideoRecord] = []
    for entry in entries:
        categories = classify_title(entry["title"])
        if not categories:
            continue
        selected_videos.append(
            VideoRecord(
                video_id=entry["id"],
                title=entry["title"],
                url=f"https://www.youtube.com/watch?v={entry['id']}",
                categories=categories,
            )
        )

    export_selected_report(selected_report, selected_videos)
    checkpoint = load_checkpoint(state_file) if runtime.resume else {}
    if not checkpoint or checkpoint.get("channel_url") != channel_url:
        checkpoint = build_checkpoint(selected_videos, channel_url, preferred_langs, runtime)
        save_checkpoint(state_file, checkpoint)
    elif runtime.retry_blocked:
        reset_blocked_to_pending(checkpoint)
        save_checkpoint(state_file, checkpoint)

    if runtime.max_videos_per_run is not None:
        pending = [v for v in selected_videos if should_process_video(checkpoint, v.video_id, runtime.resume)]
        selected_videos = pending[: runtime.max_videos_per_run]
    elif runtime.resume:
        selected_videos = [v for v in selected_videos if should_process_video(checkpoint, v.video_id, True)]

    print(f"Selected {len(selected_videos)} videos from channel")
    if runtime.list_only:
        write_summary(
            reports_dir,
            channel_url,
            checkpoint,
            processed_this_run=0,
            downloaded_this_run=0,
            preferred_langs=preferred_langs,
            runtime=runtime,
            preflight_status="skipped",
        )
        return 0

    cached_results: dict[str, DownloadResult] = {}
    preflight_ok, preflight_detail, preflight_video, preflight_result = run_preflight_probe(
        selected_videos,
        preferred_langs,
        runtime,
    )
    if preflight_video is not None and preflight_result is not None and preflight_result.text:
        cached_results[preflight_video.video_id] = preflight_result
    if not preflight_ok:
        if preflight_video is not None:
            append_csv_row(
                blocked_report,
                [
                    preflight_video.video_id,
                    preflight_video.title,
                    preflight_video.url,
                    "|".join(preflight_video.categories),
                    "",
                    "",
                    compact_detail(preflight_detail),
                ],
            )
            update_checkpoint_status(checkpoint, preflight_video, STATUS_BLOCKED, preflight_detail)
            save_checkpoint(state_file, checkpoint)
        print("Preflight blocked: stopping before full batch")
        write_summary(
            reports_dir,
            channel_url,
            checkpoint,
            processed_this_run=0,
            downloaded_this_run=0,
            preferred_langs=preferred_langs,
            runtime=runtime,
            preflight_status="blocked",
            preflight_detail=preflight_detail,
        )
        return 2

    success_count = 0
    for index, video in enumerate(selected_videos, start=1):
        print(f"[{index}/{len(selected_videos)}] {video.video_id} | {video.title}")

        result = cached_results.pop(video.video_id, None)
        if result is None:
            result = fetch_via_ytdlp(video.url, preferred_langs, runtime)
        if not result.text:
            if runtime.stop_on_rate_limit and is_rate_limited_or_blocked(result.error):
                detail = f"yt-dlp={result.error}"
                append_csv_row(
                    blocked_report,
                    [video.video_id, video.title, video.url, "|".join(video.categories), "", "", compact_detail(detail)],
                )
                update_checkpoint_status(checkpoint, video, STATUS_BLOCKED, detail)
                save_checkpoint(state_file, checkpoint)
                print("  blocked: stopping after rate-limit detection")
                return 2

            fallback = fetch_via_transcript_api(video.video_id, preferred_langs, runtime)
            if fallback.text:
                result = fallback
            else:
                detail = f"yt-dlp={result.error}; transcript_api={fallback.error}"
                if runtime.stop_on_rate_limit and (
                    is_rate_limited_or_blocked(result.error) or is_rate_limited_or_blocked(fallback.error)
                ):
                    append_csv_row(
                        blocked_report,
                        [video.video_id, video.title, video.url, "|".join(video.categories), "", "", compact_detail(detail)],
                    )
                    update_checkpoint_status(checkpoint, video, STATUS_BLOCKED, detail)
                    save_checkpoint(state_file, checkpoint)
                    print("  blocked: stopping after IP/rate-limit detection")
                    return 2

                report_row = [
                    video.video_id,
                    video.title,
                    video.url,
                    "|".join(video.categories),
                    "",
                    "",
                    compact_detail(detail),
                ]
                if no_caption_policy == NO_CAPTION_SKIP:
                    target_report = skipped_report if is_no_caption_error(detail) else errors_report
                    append_csv_row(target_report, report_row)
                    status = STATUS_SKIPPED if target_report == skipped_report else STATUS_ERROR
                    update_checkpoint_status(checkpoint, video, status, detail)
                    save_checkpoint(state_file, checkpoint)
                    print("  skipped: no caption available" if status == STATUS_SKIPPED else "  error: non-caption failure")
                    if runtime.sleep_seconds > 0:
                        time.sleep(runtime.sleep_seconds)
                    continue
                append_csv_row(errors_report, report_row)
                update_checkpoint_status(checkpoint, video, STATUS_ERROR, detail)
                save_checkpoint(state_file, checkpoint)
                print("  error: stopping due to no-caption policy")
                return 1

        safe_name = sanitize_filename(f"{video.title} [{video.video_id}]") + ".md"
        for category in video.categories:
            destination_root = speaking_dir if category == "Speaking" else writing_dir
            write_markdown(destination_root / safe_name, video, result.text, result.source or "unknown", result.language)

        append_csv_row(
            downloaded_report,
            [
                video.video_id,
                video.title,
                video.url,
                "|".join(video.categories),
                result.source or "",
                result.language or "",
                "ok",
            ],
        )
        update_checkpoint_status(checkpoint, video, STATUS_DOWNLOADED, result.source or "")
        save_checkpoint(state_file, checkpoint)
        success_count += 1
        if runtime.sleep_seconds > 0:
            time.sleep(runtime.sleep_seconds)

    write_summary(
        reports_dir,
        channel_url,
        checkpoint,
        processed_this_run=len(selected_videos),
        downloaded_this_run=success_count,
        preferred_langs=preferred_langs,
        runtime=runtime,
        preflight_status="ok" if runtime.preflight_check else "skipped",
    )
    return 0


def count_csv_rows(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8", newline="") as handle:
        return max(sum(1 for _ in handle) - 1, 0)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download channel transcripts into Speaking/Writing markdown folders."
    )
    parser.add_argument("--channel-url", default=CHANNEL_URL_DEFAULT, help="YouTube channel videos URL")
    parser.add_argument("--output-root", default=".", help="Directory that will contain Speaking/Writing/_reports")
    parser.add_argument(
        "--caption-langs",
        default=",".join(DEFAULT_LANGS),
        help="Comma-separated caption language priority, e.g. vi-orig,en-orig,vi,en",
    )
    parser.add_argument(
        "--no-caption-policy",
        default=NO_CAPTION_SKIP,
        choices=[NO_CAPTION_SKIP, "fail"],
        help="Behavior when a selected video has no usable captions",
    )
    parser.add_argument(
        "--sleep-seconds",
        type=float,
        default=10.0,
        help="Delay between videos to reduce request bursts",
    )
    parser.add_argument(
        "--stop-on-rate-limit",
        action="store_true",
        help="Stop the batch immediately when rate-limit/IP-block is detected",
    )
    parser.add_argument(
        "--max-videos-per-run",
        type=int,
        default=25,
        help="Maximum number of pending videos to process in one run",
    )
    parser.add_argument(
        "--yt-dlp-proxy",
        default=None,
        help="Proxy URL for yt-dlp requests",
    )
    parser.add_argument(
        "--http-proxy",
        default=None,
        help="HTTP proxy URL for youtube-transcript-api requests",
    )
    parser.add_argument(
        "--https-proxy",
        default=None,
        help="HTTPS proxy URL for youtube-transcript-api requests",
    )
    parser.add_argument(
        "--cookies-from-browser",
        default=None,
        help="Browser name for yt-dlp cookie extraction, e.g. chrome or edge",
    )
    parser.add_argument(
        "--cookies-file",
        default=None,
        help="Path to a Netscape cookie file for yt-dlp",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume from checkpoint instead of resetting output directories",
    )
    parser.add_argument(
        "--list-only",
        action="store_true",
        help="Only build the selected_videos report and checkpoint",
    )
    parser.add_argument(
        "--retry-blocked",
        action="store_true",
        help="Reset blocked videos to pending when resuming",
    )
    parser.add_argument(
        "--no-preflight-check",
        action="store_true",
        help="Disable the single-video preflight probe before the batch",
    )
    return parser.parse_args()


def configure_stdout() -> None:
    stdout = getattr(sys, "stdout", None)
    if stdout is None:
        return
    reconfigure = getattr(stdout, "reconfigure", None)
    if callable(reconfigure):
        try:
            reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def main() -> int:
    configure_stdout()
    args = parse_args()
    preferred_langs = [item.strip() for item in args.caption_langs.split(",") if item.strip()]
    output_root = Path(args.output_root).resolve()
    runtime = RuntimeOptions(
        sleep_seconds=args.sleep_seconds,
        stop_on_rate_limit=args.stop_on_rate_limit,
        max_videos_per_run=args.max_videos_per_run,
        yt_dlp_proxy=args.yt_dlp_proxy,
        http_proxy=args.http_proxy,
        https_proxy=args.https_proxy,
        cookies_from_browser=args.cookies_from_browser,
        cookies_file=args.cookies_file,
        resume=args.resume,
        list_only=args.list_only,
        retry_blocked=args.retry_blocked,
        preflight_check=not args.no_preflight_check,
    )
    return process_channel(
        args.channel_url,
        output_root,
        preferred_langs,
        args.no_caption_policy,
        runtime,
    )


if __name__ == "__main__":
    sys.exit(main())
