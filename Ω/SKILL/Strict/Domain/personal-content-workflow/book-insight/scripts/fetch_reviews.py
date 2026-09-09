"""Collect reviews or import cached VTT/SRT without a language-model API."""
from __future__ import annotations

import argparse
import html
import math
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from common import json_read, json_write, jsonl_write, read, slugify, write

TIMING = re.compile(r'(\d{1,2}:\d{2}:\d{2}[.,]\d{3}|\d{2}:\d{2}[.,]\d{3})\s+-->\s+(\S+)')
REJECT = re.compile(r'sách nói|audiobook|full book|nghe sách|đọc sách full|chương\s+\d+', re.I)


def seconds(value):
    parts = value.replace(',', '.').split(':')
    return sum(float(p) * 60 ** i for i, p in enumerate(reversed(parts)))


def parse_subtitles(text):
    cues, current, lines = [], None, []
    for line in text.replace('\r', '').split('\n') + ['']:
        timing = TIMING.search(line)
        if timing or not line.strip():
            if current is not None and lines:
                content = ' '.join(lines)
                cues.append({'t': current, 'text': content})
            lines = []
            current = seconds(timing[1]) if timing else None
        elif current is not None:
            if re.fullmatch(r'\d+:\d{2}:\d{2}\.\d{3},\d+:\d{2}:\d{2}\.\d{3}', line.strip()):
                continue
            clean = ' '.join(html.unescape(re.sub(r'<[^>]*>', '', line)).split())
            if clean and (not lines or clean != lines[-1]):
                lines.append(clean)
    # Rolling auto-captions repeat the previous cue's tail in the next cue.
    result, previous = [], []
    for cue in cues:
        words = cue['text'].split()
        overlap = 0
        for n in range(min(len(previous), len(words)), 0, -1):
            if previous[-n:] == words[:n]:
                overlap = n
                break
        new = words[overlap:]
        previous = words
        if new:
            if result and result[-1]['t'] == cue['t']:
                result[-1]['text'] += ' ' + ' '.join(new)
            else:
                result.append({'t': cue['t'], 'text': ' '.join(new)})
    return result


def run_ytdlp(args):
    cmd = [sys.executable, '-m', 'yt_dlp', '--socket-timeout', '20', '--retries', '0', '--extractor-retries', '0'] + args
    for attempt in range(2):
        process = subprocess.run(cmd, capture_output=True, encoding='utf-8', errors='replace', timeout=180)
        if process.returncode == 0:
            return process.stdout
        if '429' in process.stderr and attempt == 0:
            print('429: retry once after 30 seconds', file=sys.stderr)
            time.sleep(30)
        else:
            raise RuntimeError(process.stderr[-1500:])
    raise RuntimeError('subtitle retry exhausted')


def subtitle_options(info, langs):
    options = []
    for field in ('subtitles', 'automatic_captions'):
        for lang, formats in (info.get(field) or {}).items():
            if lang.split('-')[0] not in langs:
                continue
            translated = any('tlang' in parse_qs(urlparse(f.get('url', '')).query) for f in formats)
            if field == 'subtitles':
                kind = 'manual'
            elif translated:
                kind = 'auto_translated'
            else:
                kind = 'auto_native'
            priority = (0 if lang == 'vi' and kind == 'manual' else
                        1 if lang == 'vi' and kind == 'auto_native' else
                        2 if lang == 'en-orig' else 3 if lang.startswith('en') and kind != 'auto_translated' else 4)
            options.append((priority, lang, kind, field))
    return sorted(options)


def score(item):
    title = item.get('title', '')
    duration = item.get('duration') or 0
    return (math.log10((item.get('view_count') or 0) + 1)
            + bool(re.search(r'review|cảm nhận|suy tư|phản biện', title, re.I))
            - .5 * bool(re.search(r'tóm tắt|summary', title, re.I)) + .5 * (480 <= duration <= 2700))


def rejection(item, args):
    title = item.get('title', '')
    duration = item.get('duration')
    if REJECT.search(title):
        return 'audiobook/chapter title'
    if duration is None:
        return 'missing duration'
    if not args.min_minutes * 60 <= duration <= 5400:
        return 'duration outside limits'
    haystack = slugify(title + ' ' + (item.get('description') or ''))
    names = [slugify(args.book), slugify(args.title_orig)]
    if not any(name in haystack for name in names):
        return 'off-topic: neither book title found in title/description'
    return None


def save_transcript(out, row, subtitle):
    cues = parse_subtitles(read(subtitle))
    if not cues:
        raise ValueError(f'No subtitle cues: {subtitle}')
    text = '\n'.join(c['text'] for c in cues) + '\n'
    row.update(file=f"{row['id']}.txt", timed_file=f"{row['id']}.timed.jsonl", chars=len(text))
    row.setdefault('duration_s', math.ceil(cues[-1]['t']))
    row['subtitle_file'] = str(Path(subtitle).resolve())
    write(out / row['file'], text)
    jsonl_write(out / row['timed_file'], cues)
    return row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--book', required=True)
    parser.add_argument('--title-orig', required=True)
    parser.add_argument('--author', required=True)
    parser.add_argument('--year', type=int, required=True)
    parser.add_argument('--translator')
    parser.add_argument('--alt')
    parser.add_argument('--n', '--n-videos', type=int, default=10)
    parser.add_argument('--min-minutes', type=float, default=5)
    parser.add_argument('--max-per-channel', type=int, default=2)
    parser.add_argument('--langs', '--lang', default='vi,en')
    parser.add_argument('--purpose', default='tham khảo cá nhân')
    parser.add_argument('--domain', default='học tập và quản lý thông tin')
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--import-dir', type=Path, help='Offline import; never invent subtitle kind from file name')
    parser.add_argument('--catalog', type=Path, help='JSON list with id/channel/title/subtitle_file/sub_kind')
    args = parser.parse_args()
    if args.n < 1 or args.max_per_channel < 1:
        parser.error('n and max-per-channel must be positive')
    args.out.mkdir(parents=True, exist_ok=True)
    old = json_read(args.out / 'manifest.json') if (args.out / 'manifest.json').exists() else {}
    book = dict(title_vi=args.book, title_orig=args.title_orig, author=args.author, year=args.year, translator_vi=args.translator)
    if old.get('book') and old['book'] != book:
        parser.error('output directory belongs to different book metadata; use a new directory')
    sources, rejected = [], []
    old_ids = {**old.get('rid_registry', {}), **{r['id']: r['rid'] for r in old.get('sources', [])}}
    next_rid = max([int(r[1:]) for r in old_ids.values()] + [0]) + 1

    def add(row, subtitle):
        nonlocal next_rid
        if any(r['id'] == row['id'] for r in sources):
            raise ValueError('Duplicate video in catalog')
        if row['id'] in old_ids:
            row['rid'] = old_ids[row['id']]
        else:
            row['rid'] = f'R{next_rid}'
            next_rid += 1
        old_ids[row['id']] = row['rid']
        row.setdefault('url', 'https://www.youtube.com/watch?v=' + row['id'])
        row.setdefault('sub_kind', 'unknown')
        row.setdefault('views', None)
        row.setdefault('score', None)
        row.setdefault('independence_group', row.get('channel') or row['id'])
        sources.append(save_transcript(args.out, row, subtitle))
        print(f"{row['rid']} {row['id']}: {row['chars']} chars ({row['sub_kind']})")

    if args.import_dir:
        catalog = json_read(args.catalog) if args.catalog else []
        if not catalog:
            ids = sorted({p.name.split('.')[0] for p in args.import_dir.iterdir() if p.suffix in ('.vtt', '.srt')})
            catalog = [{'id': ident, 'channel': ident, 'title': ident, 'lang': 'unknown'} for ident in ids]
        for row in catalog:
            row = dict(row)
            try:
                if row.get('subtitle_file'):
                    subtitle = args.import_dir / row['subtitle_file']
                else:
                    matches = sorted(args.import_dir.glob(row['id'] + '.*'), key=lambda p: ('en-orig' not in p.name, p.name))
                    subtitle = next(p for p in matches if p.suffix in ('.vtt', '.srt'))
                add(row, subtitle)
            except (ValueError, OSError, StopIteration) as exc:
                rejected.append({'id': row['id'], 'reason': str(exc)})
    else:
        import json
        candidates = {}
        for query in (f'review sách {args.book}', f'tóm tắt sách {args.book}', f'{args.alt or args.title_orig} book review'):
            try:
                data = json.loads(run_ytdlp(['--flat-playlist', '--dump-single-json', f'ytsearch{max(args.n*3, 20)}:{query}']))
                candidates.update({x['id']: x for x in data.get('entries', []) if x})
            except (ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
                rejected.append({'query': query, 'reason': str(exc)})
        channels = {}
        for candidate in sorted(candidates.values(), key=score, reverse=True):
            if len(sources) >= args.n:
                break
            ident = candidate['id']
            try:
                info_path = args.out / f'{ident}.info.json'
                info = json_read(info_path) if info_path.exists() else json.loads(run_ytdlp(['--skip-download', '--dump-single-json', 'https://www.youtube.com/watch?v=' + ident]))
                json_write(info_path, info)
                reason = rejection(info, args)
                channel = info.get('channel_id') or info.get('channel') or ident
                if reason or channels.get(channel, 0) >= args.max_per_channel:
                    rejected.append({'id': ident, 'reason': reason or 'channel limit'})
                    continue
                choices = subtitle_options(info, args.langs.split(','))
                if not choices:
                    raise ValueError('No requested subtitles')
                _, lang, kind, field = choices[0]
                paths = [args.out / f'{ident}.{lang}.{ext}' for ext in ('vtt', 'srt')]
                if not any(p.exists() for p in paths):
                    run_ytdlp(['--skip-download', '--write-sub' if field == 'subtitles' else '--write-auto-sub',
                               '--sub-langs', lang, '--sub-format', 'vtt/srt', '-o', str(args.out / '%(id)s.%(ext)s'),
                               'https://www.youtube.com/watch?v=' + ident])
                subtitle = next(p for p in paths if p.exists())
                add({'id': ident, 'channel': info.get('channel', channel), 'title': info['title'],
                     'duration_s': info['duration'], 'views': info.get('view_count'), 'lang': lang,
                     'sub_kind': kind, 'score': score(info), 'independence_group': channel}, subtitle)
                channels[channel] = channels.get(channel, 0) + 1
            except (ValueError, RuntimeError, OSError, StopIteration, subprocess.TimeoutExpired) as exc:
                rejected.append({'id': ident, 'reason': str(exc)})
            finally:
                time.sleep(3)
    manifest = {'schema_version': 1, 'book': book, 'fetched_at': datetime.now().astimezone().isoformat(),
                'purpose': args.purpose, 'domain': args.domain, 'sources': sources, 'rejected': rejected,
                'supplements': old.get('supplements', []), 'imported': bool(args.import_dir), 'rid_registry': old_ids}
    json_write(args.out / 'manifest.json', manifest)
    json_write(args.out / 'fetch_log.json', {'accepted': len(sources), 'requested': args.n, 'rejected': rejected})
    if not sources:
        raise SystemExit('No usable reviews; see fetch_log.json. Book text can still be merged.')
    if len(sources) < args.n:
        print(f'WARNING: {len(sources)}/{args.n} sources available; do not invent missing sources', file=sys.stderr)


if __name__ == '__main__':
    main()
