"""Merge timed reviews, optional plain book text and notes into labeled paragraphs."""
import argparse
import re
from pathlib import Path

from common import blocks, json_read, json_write, jsonl_read, read, stamp, table, write


def paragraph_groups(cues, target=600):
    result, text, start = [], '', None
    for cue in cues:
        if start is None:
            start = cue['t']
        text += (' ' if text else '') + cue['text']
        if len(text) >= target and re.search(r'[.!?…][\"\u201d\u2019\)]?$', text):
            result.append((start, text))
            text, start = '', None
        elif len(text) >= target * 2:
            result.append((start, text))
            text, start = '', None
    if text:
        result.append((start, text))
    merged = []
    for t, text in result:
        if merged and stamp(t) == stamp(merged[-1][0]):
            merged[-1] = (merged[-1][0], merged[-1][1] + ' ' + text)
        else:
            merged.append((t, text))
    return merged


def book_blocks(text, toc=None):
    headings = {}
    if toc:
        for line in read(toc).splitlines():
            if not line.strip():
                continue
            label, title = line.split('|', 1)
            number = re.search(r'\d+', label)
            if not number:
                raise ValueError(f'Invalid TOC label: {label}')
            headings[title.strip()] = int(number[0])
    chapter, paragraph, buffer = 0, 0, []
    output = []
    for line in text.splitlines() + ['']:
        match = re.match(r'^(?:Chương|Chapter)\s+(\d+)\b', line.strip(), re.I)
        heading = int(match[1]) if match else headings.get(line.strip())
        if heading is not None or not line.strip():
            if buffer:
                paragraph += 1
                output.append((f'BOOK ch.{chapter} ¶{paragraph}', ' '.join(buffer)))
                buffer = []
            if heading is not None:
                chapter, paragraph = heading, 0
                buffer = [line.strip()]
        else:
            buffer.append(line.strip())
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dir', type=Path, required=True)
    parser.add_argument('--book-text', type=Path)
    parser.add_argument('--toc', type=Path)
    parser.add_argument('--notes', type=Path)
    parser.add_argument('--reading-state', choices=['full-read', 'partial-read', 'highlights-only'], default='partial-read')
    args = parser.parse_args()
    path = args.dir / 'manifest.json'
    manifest = json_read(path)
    source_rows, paragraphs = [], []
    for source in manifest['sources']:
        source_rows.append([source['rid'], source['channel'], source['duration_s'], source['sub_kind']])
        cues = jsonl_read(args.dir / source['timed_file'])
        if any(cues[i]['t'] > cues[i+1]['t'] for i in range(len(cues)-1)):
            raise ValueError('Subtitle timestamps must be monotonic')
        paragraphs.extend((source['rid'] + ' ' + stamp(t), text) for t, text in paragraph_groups(cues))
    supplements = []
    if args.book_text:
        paragraphs.extend(book_blocks(read(args.book_text), args.toc))
        supplements.append({'rid': 'BOOK', 'sub_kind': 'book_text', 'file': str(args.book_text.resolve()), 'reading_state': args.reading_state})
        source_rows.append(['BOOK', 'Text sách', '-', 'book_text'])
    if args.notes:
        for n, paragraph in enumerate(re.split(r'\n\s*\n', read(args.notes).strip()), 1):
            if paragraph.strip():
                paragraphs.append((f'NOTE {n}', paragraph.strip()))
        supplements.append({'rid': 'NOTE', 'sub_kind': 'note', 'file': str(args.notes.resolve())})
        source_rows.append(['NOTE', 'Ghi chú cá nhân', '-', 'note'])
    manifest['supplements'] = supplements
    text = '# Nguồn để trích xuất\n\n' + table(['rid', 'kênh', 'duration_s', 'sub_kind'], source_rows) + '\n\n'
    text += '\n\n'.join(f'[{locator}]\n{content}' for locator, content in paragraphs) + '\n'
    parsed = blocks(text)
    if not parsed:
        raise ValueError('No source paragraphs')
    json_write(path, manifest)
    write(args.dir / 'sources.md', text)
    json_write(args.dir / 'source_index.json', parsed)
    print(f'{len(text)} chars, {len(parsed)} labeled paragraphs')
    if len(text) > 300000:
        print('WARNING: >300k chars; reduce reviews or extract in chunk batches')


if __name__ == '__main__':
    main()
