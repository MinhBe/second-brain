"""Materialize manually reviewed annotations, never infer a claim from keyword matches."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'Skills/Domain/content-production/personal-content-workflow/book-insight/scripts'))
from common import json_read, jsonl_write


def build(name):
    directory = Path(__file__).parent / name
    paragraphs = {p['locator']: p for p in json_read(directory / 'source_index.json')}
    annotations = json_read(directory / 'annotations.json')
    languages = {r['rid']: r.get('lang', 'unknown').split('-')[0] for r in json_read(directory / 'manifest.json')['sources']}
    extractions = []
    for row in annotations['extractions']:
        ident, kind, content, confidence, speaker, terms, refs = row
        evidence = []
        for locator, snippet in refs:
            block = paragraphs[locator]
            if snippet not in block['text']:
                raise ValueError(f'{name} {ident}: snippet not in {locator}: {snippet}')
            evidence.append({'rid': block['rid'], 'locator': locator, 'snippet': snippet})
        extractions.append({'id': ident, 'type': kind, 'content': content, 'confidence': confidence,
                            'speaker': speaker, 'relatedTerms': terms, 'rids': sorted({e['rid'] for e in evidence}),
                            'sourceSnippet': evidence[0]['snippet'], 'sourceTimestamp': evidence[0]['locator'],
                            'chapter_hint': None, 'sub_kind_min': 'unknown', 'lang': languages[evidence[0]['rid']], 'evidence': evidence})
    by_id = {e['id']: e for e in extractions}
    terms = []
    for ident, en, vi, definition, aliases, refs in annotations['terms']:
        evidence = []
        for ref in refs:
            for e in by_id[ref]['evidence']:
                if e not in evidence:
                    evidence.append(e)
        terms.append({'id': ident, 'term': en, 'term_vi': vi, 'definition': definition,
                      'aliases': aliases, 'approved': False, 'evidence': evidence})
    jsonl_write(directory / 'extractions.jsonl', extractions)
    jsonl_write(directory / 'terms.jsonl', terms)
    jsonl_write(directory / 'qa.jsonl', annotations['qa'])
    print(f'{name}: {len(extractions)} reviewed claims, {len(terms)} terms, {len(annotations["qa"])} QA')


if __name__ == '__main__':
    for name in sys.argv[1:]:
        build(name)
