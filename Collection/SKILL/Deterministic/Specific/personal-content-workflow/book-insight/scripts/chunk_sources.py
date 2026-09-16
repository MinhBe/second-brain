"""Split at complete source paragraphs; offsets use Python Unicode characters."""
import argparse
from pathlib import Path

from common import blocks, json_write, read, write


def chunk(text, size=3000):
    parsed = blocks(text)
    result, start, end, rids = [], None, None, set()
    for block in parsed:
        if start is not None and block['end'] - start > size:
            result.append((start, end, sorted(rids)))
            start, rids = None, set()
        if start is None:
            start = block['start']
        end = block['end']
        rids.add(block['rid'])
    if start is not None:
        result.append((start, end, sorted(rids)))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dir', type=Path, required=True)
    parser.add_argument('--size', type=int, default=3000)
    args = parser.parse_args()
    if args.size < 1:
        parser.error('size must be positive')
    text = read(args.dir / 'sources.md')
    index = []
    for n, (start, end, rids) in enumerate(chunk(text, args.size), 1):
        ident = f'chunk_{n:03d}'
        write(args.dir / 'chunks' / f'{ident}.md', text[start:end])
        index.append({'chunk_id': ident, 'rids': rids, 'char_start': start, 'char_end': end})
        if end-start > args.size:
            print(f'WARNING: {ident} exceeds target; intact source paragraph preserved')
    json_write(args.dir / 'chunks' / 'index.json', index)
    print(f'{len(index)} chunks; use index.json, not a directory glob (old files may remain)')


if __name__ == '__main__':
    main()
