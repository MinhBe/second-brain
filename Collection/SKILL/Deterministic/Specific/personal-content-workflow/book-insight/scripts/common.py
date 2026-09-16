"""Shared UTF-8 I/O, source locators and confidence rules."""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from pathlib import Path

TYPES = ('decision', 'action', 'opinion', 'question', 'term')
CAPS = {'manual': 100, 'auto_native': 90, 'auto_translated': 70,
        'unknown': 60, 'book_text': 100, 'note': 80}
LABEL = re.compile(r'^\[((?:R\d+ \d+:\d{2})|(?:BOOK ch\.\d+ ¶\d+)|(?:NOTE \d+))\]\s*$', re.M)
CITATION = re.compile(r'\[((?:R\d+)(?: \d+:\d{2})?|BOOK ch\.\d+ ¶\d+|NOTE \d+)\]')


def read(path):
    return Path(path).read_text(encoding='utf-8-sig')


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(value, encoding='utf-8', newline='\n')
    tmp.replace(path)


def json_read(path):
    return json.loads(read(path))


def json_write(path, value):
    write(path, json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def jsonl_read(path, optional=False):
    if optional and not Path(path).exists():
        return []
    result = []
    for n, line in enumerate(read(path).splitlines(), 1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
            if not isinstance(obj, dict):
                raise ValueError('expected JSON object')
            result.append(obj)
        except (ValueError, TypeError) as exc:
            raise ValueError(f'{path}:{n}: {exc}') from exc
    return result


def jsonl_write(path, rows):
    write(path, ''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in rows))


def norm(text):
    # Preserve accents, punctuation and negation; tolerate typographic quotes only.
    value = unicodedata.normalize('NFKC', text).translate(str.maketrans({'“': '"', '”': '"', '’': "'", '‘': "'"}))
    return ' '.join(value.split())


def term_key(text):
    return ''.join(c for c in unicodedata.normalize('NFKC', text).casefold() if c.isalnum())


def slugify(text):
    value = unicodedata.normalize('NFKD', text.replace('đ', 'd').replace('Đ', 'D'))
    return re.sub(r'[^a-z0-9]+', '-', value.encode('ascii', 'ignore').decode().lower()).strip('-') or 'book'


def stamp(t):
    return f'{int(t) // 60:02d}:{int(t) % 60:02d}'


def source_id(locator):
    return locator.split()[0]


def blocks(text):
    matches = list(LABEL.finditer(text))
    result = []
    for i, match in enumerate(matches):
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        result.append({'locator': match[1], 'rid': source_id(match[1]),
                       'text': text[match.end():end].strip(), 'start': match.start(), 'end': end})
    if len({b['locator'] for b in result}) != len(result):
        raise ValueError('Duplicate source locators; merge paragraphs sharing a timestamp first')
    return result


def source_map(manifest):
    rows = manifest.get('sources', []) + manifest.get('supplements', [])
    result = {x['rid']: x for x in rows}
    if len(result) != len(rows):
        raise ValueError('Duplicate source IDs in manifest')
    return result


def cap(source):
    value = CAPS[source['sub_kind']]
    if source['rid'].startswith('R') and source.get('duration_s', 300) < 300:
        value = min(value, 60)
    return value


def citations(evidence):
    return ' '.join('[' + e['locator'] + ']' for e in evidence)


def fingerprint(directory):
    h = hashlib.sha256()
    for name in ('manifest.json', 'sources.md', 'extractions.jsonl', 'terms.jsonl', 'qa.jsonl'):
        path = Path(directory) / name
        h.update(name.encode())
        h.update(path.read_bytes() if path.exists() else b'<missing>')
    return h.hexdigest()


def cell(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')


def table(headers, rows):
    lines = ['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join('---' for _ in headers) + ' |']
    lines.extend('| ' + ' | '.join(cell(v) for v in row) + ' |' for row in rows)
    return '\n'.join(lines)


def core_ideas(extractions, manifest):
    sources = source_map(manifest)
    result = []
    for item in extractions:
        groups = {sources[r].get('independence_group', sources[r].get('channel', r))
                  for r in item['rids'] if r.startswith('R')}
        direct = 'BOOK' in item['rids']
        if item['type'] == 'decision' and item['confidence'] >= 75 and (direct or len(groups) >= 2):
            result.append(item)
    return sorted(result, key=lambda e: (-int('BOOK' in e['rids']), -len(e['rids']), -e['confidence'], e['id']))
