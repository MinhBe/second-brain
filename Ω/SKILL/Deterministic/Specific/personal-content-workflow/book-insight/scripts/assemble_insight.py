"""Assemble one report exclusively from validated artifacts and authored sections."""
from __future__ import annotations

import argparse
import csv
from datetime import date, timedelta
import hashlib
import io
import json
from pathlib import Path
import re

from common import (CITATION, blocks, cap, citations, core_ideas, fingerprint, json_read, json_write,
                    jsonl_read, read, slugify, source_map, table, term_key, write)


def parse_parts(directory):
    sections = {}
    expected = {'part1_summary.md': {1, 2, 3, 4, 5, 10, 11, 12}, 'part2_map.md': {6}, 'part3_extractions.md': {8, 9}}
    for file, allowed in expected.items():
        text = read(directory / file)
        headings = list(re.finditer(r'^## (\d+)\. ([^\n]+)\n', text, re.M))
        preamble = text[:headings[0].start()] if headings else text
        if preamble.strip():
            raise ValueError(f'{file}: content before first numbered heading')
        for i, heading in enumerate(headings):
            number = int(heading[1])
            if number not in allowed or number in sections:
                raise ValueError(f'{file}: unexpected/duplicate section {number}')
            sections[number] = (heading[2], text[heading.end():headings[i+1].start() if i+1 < len(headings) else len(text)].strip())
    return sections


def extraction_table(items):
    return table(['ID', 'Nội dung', 'Confidence', 'Speaker', 'Nguồn', 'Snippet'],
                 [[x['id'], x['content'], x['confidence'], x['speaker'], citations(x['evidence']),
                   '<br>'.join(e['snippet'] for e in x['evidence'])] for x in items]) if items else 'Nguồn không đủ để xác nhận mục nào.'


def generated_tables(items, terms, manifest):
    result = []
    for n, (kind, title) in enumerate([('decision', 'Decisions'), ('action', 'Actions'), ('opinion', 'Opinions'), ('question', 'Questions')], 1):
        result.append(f'### 8.{n} {title}\n\n' + extraction_table([x for x in items if x['type'] == kind]))
    keywords = sorted([t for t in terms if t['frequency'] >= 2 or len(t['rids']) >= 2], key=lambda t: (-t['frequency'], t['term']))
    result.append('### 8.5 Keyword\n\n' + (table(['VI', 'EN', 'Định nghĩa', 'Số đoạn đã xác minh', 'Nguồn'],
        [[t['term_vi'], t['term'], t['definition'], t['frequency'], citations(t['evidence'])] for t in keywords]) if keywords else 'Nguồn không đủ thuật ngữ lặp lại.'))
    clusters = []
    for item in core_ideas(items, manifest):
        keys = {term_key(t) for t in item['relatedTerms']}
        related = [e for e in items if e['type'] in ('action', 'opinion') and keys & {term_key(t) for t in e['relatedTerms']}]
        clusters.append(f"**{item['id']}**: {item['content']} {citations(item['evidence'])}\n\n" +
                        '\n'.join(f"- {e['type']}: {e['content']} {citations(e['evidence'])}" for e in related))
    result.append('### 8.6 Core idea\n\n' + ('\n\n'.join(clusters) or 'Nguồn không đủ ý đạt ngưỡng; xem các ý tạm thời ở mục 2.'))
    return '\n\n'.join(result)


def render_qa(qa, items):
    by_id = {x['id']: x for x in items}
    result = []
    for n, title in enumerate(['Hiểu', 'Phản biện', 'Chuyển giao', 'Nối kết'], 1):
        result.append(f'### 7.{n} {title}')
        for q in qa:
            if q['round'] != n:
                continue
            source = ' '.join(citations(by_id[v]['evidence']) for v in q['evidence_ids'])
            answer = q.get('answer') or f"Chưa có trong nguồn → {q['id']}"
            prefix = '[mở rộng] ' if q['origin'] == 'generated' and q.get('answer') else ''
            result.append(f"**H ({q['id']}):** {q['question']}\n\n**Đ:** {prefix}{answer} {source}".strip())
    return '\n\n'.join(result)


def export_cards(directory, slug, book, items, terms, qa, manifest):
    # Persist the source identity separately from the output's sort order.
    registry_path = directory / 'anki_ids.json'
    registry = json_read(registry_path) if registry_path.exists() else {}
    rows, by_id = [], {x['id']: x for x in items}
    entries = [('core', e['id'], 'Giải thích ý chính về: ' + (', '.join(e['relatedTerms']) or e['id']), e['content'], citations(e['evidence'])) for e in core_ideas(items, manifest)]
    entries += [('term', t['id'], t['term_vi'], t['definition'] + ' (' + t['term'] + ')', citations(t['evidence'])) for t in terms]
    entries += [('qa', q['id'], q['question'], q['answer'], ' '.join(citations(by_id[v]['evidence']) for v in q['evidence_ids'])) for q in qa if q.get('answer')]
    for kind, ident, front, back, source in entries:
        key = f'{slug}:{kind}:{ident}'
        registry.setdefault(key, f'{slug}-{kind}-' + hashlib.sha256(key.encode()).hexdigest()[:16])
        rows.append([registry[key], front, back, source, book, f'book-insight {slug} {kind}'])
    buf = io.StringIO(newline='')
    buf.write('#separator:Comma\n#html:false\n#notetype:Book Insight\n#tags column:6\n')
    buf.write('#columns:ID,Front,Back,Source,Book,Tags\n')
    csv.writer(buf, lineterminator='\n').writerows(rows)
    write(directory / 'cards.csv', buf.getvalue())
    json_write(registry_path, registry)


def assemble(directory, slug=None, draft=False, anki=False):
    directory = Path(directory)
    stats = json_read(directory / 'extractions_stats.json')
    if stats['errors'] or stats['unverified_snippets'] or stats['input_fingerprint'] != fingerprint(directory):
        raise ValueError('Validation failed or inputs changed; run validate_extractions.py again')
    for name, digest in stats['clean_hashes'].items():
        if hashlib.sha256((directory / name).read_bytes()).hexdigest() != digest:
            raise ValueError(f'{name} was modified outside validator')
    manifest = json_read(directory / 'manifest.json')
    sources = source_map(manifest)
    items = jsonl_read(directory / 'extractions.clean.jsonl')
    terms = jsonl_read(directory / 'terms.clean.jsonl')
    qa = jsonl_read(directory / 'qa.clean.jsonl')
    sections = parse_parts(directory)
    warnings = []
    for n in [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12]:
        if n not in sections or not sections[n][1]:
            warnings.append(f'missing/empty section {n}')
            sections[n] = (str(n), 'Nguồn không đủ; mục này chưa được biên soạn.')
    source_rows = [[r['rid'], r.get('channel', r['rid']), r.get('url', r.get('file', '')), r.get('duration_s', '-'),
                    r.get('lang', '-'), r['sub_kind'], r.get('perspective', 'Chưa xác định góc nhìn.')] for r in sources.values()]
    sections[0] = ('Bảng nguồn', table(['rid', 'Kênh', 'Nguồn', 'Giây', 'Ngôn ngữ', 'Loại', 'Góc nhìn'], source_rows))
    sections[7] = ('Vấn đáp 4 vòng', render_qa(qa, items))
    if re.search(r'^### 8\.[1-6]\b', sections[8][1], re.M):
        raise ValueError('8.1..8.6 are generated; authored part3 may contain only 8.7..8.9')
    sections[8] = (sections[8][0], generated_tables(items, terms, manifest) + '\n\n' + sections[8][1])
    body = '\n\n'.join(f'## {n}. {sections[n][0]}\n\n{sections[n][1]}' for n in range(13)) + '\n'
    if re.search(r'\{[a-zA-Z_][^}\n]*\}|\bTODO\b|\bTBD\b|<slug>|<out>', body):
        warnings.append('unfilled placeholder')
    paragraphs = {b['locator']: b for b in blocks(read(directory / 'sources.md'))}
    for label in re.findall(r'\[(?:R\d+|BOOK|NOTE)(?:\b[^\]]*)\]', body):
        if not CITATION.fullmatch(label):
            raise ValueError(f'Malformed source citation {label}')
    for match in CITATION.finditer(body):
        value = match[1]
        if value not in sources and value not in paragraphs:
            raise ValueError(f'Unknown source citation [{value}]')
    for n in (1, 2, 3):
        for paragraph in re.split(r'\n\s*\n', sections[n][1]):
            if paragraph.strip().startswith('#') or 'Nguồn không đủ' in paragraph or 'nguồn không đủ' in paragraph:
                continue
            if not CITATION.search(paragraph):
                warnings.append(f'section {n}: paragraph missing source citation')
    for match in CITATION.finditer(sections[3][1]):
        rid = match[1].split()[0]
        if sources[rid]['sub_kind'] in ('auto_translated', 'unknown', 'note') or cap(sources[rid]) <= 60:
            raise ValueError(f'Section 3 cannot quote source {rid} ({sources[rid]["sub_kind"]})')
    for n in range(1, 5):
        if not 3 <= sum(q['round'] == n for q in qa) <= 5:
            warnings.append(f'QA round {n}: expected 3..5 questions')
    index = re.search(r'^### 6\.1[^\n]*\n(.*?)(?=^### |\Z)', sections[6][1], re.M | re.S)
    if index and len(index[1].strip().splitlines()) > 40:
        warnings.append('book index exceeds 40 lines')
    for block in re.findall(r'^#### [^\n]*\n(.*?)(?=^#{3,4} |\Z)', sections[6][1], re.M | re.S):
        if len(block.strip().splitlines()) > 15:
            warnings.append('chapter block exceeds 15 lines')
    length = sum(len(sections[n][1].split()) for n in (1, 2, 3, 4, 5, 10, 11))
    if not 600 <= length <= 1000:
        warnings.append(f'analytical summary word count {length}; expected 600..1000 whitespace-separated words')
    if '[mở rộng]' not in sections[9][1]:
        warnings.append('section 9 must explicitly mark [mở rộng]')
    if warnings and not draft:
        raise ValueError('Report not ready:\n' + '\n'.join(warnings))
    thesis_rids = {m[1].split()[0] for m in CITATION.finditer(sections[1][1])}
    weakest = min(thesis_rids, key=lambda r: cap(sources[r])) if thesis_rids else None
    direct = next((s for s in manifest.get('supplements', []) if s['rid'] == 'BOOK'), None)
    quality = direct['reading_state'] if direct else ('reconstructed-from-machine-translated-reviews' if weakest and sources[weakest]['sub_kind'] == 'auto_translated' else 'reconstructed-from-reviews')
    meta = {'book': manifest['book'], 'source_quality': quality,
            'source_quality_note': (f"Reconstructed from {len(manifest['sources'])} reviews, no direct read" if not direct else f"Book text: {direct['reading_state']}"),
            'thesis_source_cap': cap(sources[weakest]) if weakest else None,
            'sources': list(sources), 'book_text': bool(direct), 'notes': 'NOTE' in sources,
            'purpose': manifest.get('purpose'), 'domain': manifest.get('domain'), 'created': date.today().isoformat(),
            'chunks': stats['chunks'], 'extractions': stats['extractions'], 'new_terms': stats['new_terms'],
            'extractions_by_type': stats['extractions_by_type'], 'status': 'draft' if draft else 'validated',
            'review_dates': {str(d): (date.today() + timedelta(days=d)).isoformat() for d in (1, 4, 12, 30)}}
    header = '---\n' + ''.join(k + ': ' + json.dumps(v, ensure_ascii=False) + '\n' for k, v in meta.items()) + '---\n\n'
    book = manifest['book']
    title = f"# {book['title_vi']} ({book['title_orig']}) - Book Insight\n\n"
    title += 'Dịch giả bản Việt: ' + (book.get('translator_vi') or 'chưa rõ') + '.\n\n'
    slug = slugify(slug or book['title_orig'])
    output = directory / f'{slug}_INSIGHT.md'
    if draft:
        output = directory / f'{slug}_DRAFT.md'
    write(output, header + title + body)
    json_write(directory / 'assembly_report.json', {'file': str(output), 'warnings': warnings, 'word_count': length, 'unknown_labels': 0})
    if anki:
        if draft:
            raise ValueError('Anki export requires a validated report')
        export_cards(directory, slug, book['title_orig'], items, terms, qa, manifest)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dir', type=Path, required=True)
    parser.add_argument('--slug')
    parser.add_argument('--draft', action='store_true', help='Allow incomplete editorial content, never bad evidence')
    parser.add_argument('--anki', action='store_true')
    args = parser.parse_args()
    print(assemble(args.dir, args.slug, args.draft, args.anki))


if __name__ == '__main__':
    main()
