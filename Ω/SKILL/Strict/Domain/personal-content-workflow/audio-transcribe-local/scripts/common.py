"""Shared paths, atomic artifacts and Windows CUDA discovery; no torch dependency."""
from __future__ import annotations
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import re
import sysconfig
import unicodedata
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[6]
DEFAULT_INPUT = ROOT / 'Data' / 'Recording'
DEFAULT_OUTPUT = ROOT / 'Data' / 'Transcripts'
VERSION = 1
_DLL_HANDLES = []

def now():
    return datetime.now(timezone.utc).isoformat()

def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest()

def read_json(path, default=None):
    p = Path(path)
    return json.loads(p.read_text(encoding='utf-8-sig')) if p.exists() else default

def write_text(path, value):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + f'.{os.getpid()}.tmp')
    with tmp.open('w', encoding='utf-8', newline='') as stream:
        stream.write(value)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(tmp, p)

def write_json(path, value):
    write_text(path, json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def write_csv(path, rows, fields):
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=fields, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(rows)
    write_text(path, '\ufeff' + stream.getvalue())

def slug(text):
    value = unicodedata.normalize('NFKD', text.replace('đ', 'd').replace('Đ', 'D'))
    value = ''.join(c for c in value if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+', '-', value.lower()).strip('-') or 'audio'

def stamp(seconds, srt=False):
    n = max(0, round(float(seconds) * 1000))
    h, n = divmod(n, 3600000)
    m, n = divmod(n, 60000)
    s, ms = divmod(n, 1000)
    return f'{h:02}:{m:02}:{s:02}' + (f',{ms:03}' if srt else '')

def setup_cuda():
    if os.name != 'nt':
        return []
    lib = Path(sysconfig.get_paths()['purelib'])
    dirs = [lib / 'nvidia' / name / 'bin' for name in ('cublas', 'cudnn', 'cuda_runtime')]
    dirs = [p for p in dirs if p.is_dir()]
    for p in dirs:
        _DLL_HANDLES.append(os.add_dll_directory(str(p)))
    os.environ['PATH'] = os.pathsep.join([str(p) for p in dirs] + [os.environ.get('PATH', '')])
    return [str(p) for p in dirs]

def validate_segments(raw):
    duration = raw['duration_s']
    ids = set()
    previous = -1
    for seg in raw['segments']:
        if seg['id'] in ids or not (0 <= seg['start'] <= seg['end'] <= duration + .05):
            raise ValueError('duplicate ID or timestamp outside source')
        if seg['start'] < previous:
            raise ValueError('segments not chronological')
        ids.add(seg['id'])
        previous = seg['start']
    return ids
