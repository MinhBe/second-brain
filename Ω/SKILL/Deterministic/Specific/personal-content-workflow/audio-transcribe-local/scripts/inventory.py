"""Read-only source inspection; hash duplicate detection does not delete inputs."""
import argparse
import json
from pathlib import Path
import subprocess
from common import DEFAULT_INPUT, DEFAULT_OUTPUT, digest, slug, write_csv, write_json

FIELDS = ['file', 'path', 'slug', 'duration_s', 'sample_rate', 'channels', 'bytes', 'sha256', 'duplicate_of', 'error']

def probe(path):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
        'format=duration:stream=codec_type,sample_rate,channels', '-of', 'json', str(path)],
        capture_output=True, text=True, encoding='utf-8', check=True)
    data = json.loads(result.stdout)
    stream = next(s for s in data['streams'] if s['codec_type'] == 'audio')
    return {'duration_s': float(data['format']['duration']), 'sample_rate': int(stream['sample_rate']), 'channels': stream['channels']}

def inventory(source):
    source = Path(source).resolve()
    paths = [source] if source.is_file() else list(source.iterdir())
    paths = [p for p in paths if p.is_file() and p.suffix.lower() in {'.m4a', '.wav', '.mp3', '.flac', '.ogg', '.aac', '.mp4'}]
    # Prefer the unnumbered copy, independently of filesystem enumeration order.
    paths.sort(key=lambda p: (len(p.stem), p.name.casefold()))
    hashes, slugs, rows = {}, {}, []
    for p in paths:
        row = dict.fromkeys(FIELDS, '')
        row.update(file=p.name, path=str(p), bytes=p.stat().st_size)
        ident = slug(p.stem)
        if ident in slugs:
            ident += '-' + digest(p)[:8]
        if ident in slugs:
            ident += '-' + str(len(rows))
        slugs[ident] = p
        row['slug'] = ident
        try:
            row['sha256'] = digest(p)
            row.update(probe(p))
            row['duplicate_of'] = hashes.get(row['sha256'], '')
            hashes.setdefault(row['sha256'], ident)
        except Exception as exc:
            row['error'] = str(exc)
        rows.append(row)
    return sorted(rows, key=lambda r: (r['duration_s'] or float('inf'), r['file']))

def save_inventory(source, output):
    rows = inventory(source)
    target = Path(output) / '_reports'
    write_csv(target / 'inventory.csv', rows, FIELDS)
    write_json(target / 'inventory.json', rows)
    return rows

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=DEFAULT_INPUT)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    rows = save_inventory(args.input, args.output)
    print(f'{len(rows)} sources, {sum(bool(r["duplicate_of"]) for r in rows)} duplicates')
