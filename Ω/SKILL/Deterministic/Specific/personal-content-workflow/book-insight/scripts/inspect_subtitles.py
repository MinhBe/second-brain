"""Verify cached subtitle metadata without downloading subtitle content."""
import argparse
import json
from pathlib import Path
import subprocess
import time

from common import json_read, json_write
from fetch_reviews import run_ytdlp, subtitle_options


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--metadata-dir', type=Path, required=True)
    args = parser.parse_args()
    rows = json_read(args.catalog)
    args.metadata_dir.mkdir(parents=True, exist_ok=True)
    for row in rows:
        ident = row['id']
        try:
            cached = args.metadata_dir / f'{ident}.info.json'
            info = json_read(cached) if cached.exists() else json.loads(run_ytdlp(['--skip-download', '--dump-single-json', 'https://www.youtube.com/watch?v=' + ident]))
            json_write(cached, info)
            lang = row['subtitle_file'].split('.')[1]
            options = [o for o in subtitle_options(info, ['vi', 'en']) if o[1] == lang]
            kinds = {o[2] for o in options}
            # Existing file has no origin marker if both manual and auto exist.
            row['sub_kind'] = next(iter(kinds)) if len(kinds) == 1 else 'unknown'
            row['metadata_note'] = 'Live subtitle listing; ambiguous original file remains unknown' if len(kinds) != 1 else 'Verified against cached live yt-dlp subtitle metadata'
            row['lang'] = lang
            row['duration_s'] = info.get('duration') or row.get('duration_s')
            row['title'] = info.get('title') or row['title']
            row['channel'] = info.get('channel') or row['channel']
            row['independence_group'] = info.get('channel_id') or row['channel']
        except (ValueError, RuntimeError, OSError, subprocess.TimeoutExpired) as exc:
            row['sub_kind'] = 'unknown'
            row['metadata_note'] = str(exc)[-300:]
        print(f"{ident}: {row['sub_kind']}", flush=True)
        json_write(args.out, rows)
        time.sleep(3)


if __name__ == '__main__':
    main()
