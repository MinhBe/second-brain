"""Validate evidence per locator; preserve rejected rows and rebuild clean artifacts."""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import math
from pathlib import Path

from common import (TYPES, blocks, cap, fingerprint, json_read, json_write, jsonl_read,
                    jsonl_write, norm, read, source_map, term_key)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def evidence_check(evidence, sources, paragraphs):
    if not isinstance(evidence, list) or not evidence:
        raise ValueError('evidence must be a nonempty list')
    found = []
    for e in evidence:
        if not isinstance(e, dict):
            raise ValueError('evidence entry must be an object')
        rid, locator, snippet = e.get('rid'), e.get('locator'), e.get('snippet')
        if rid not in sources or locator not in paragraphs:
            raise ValueError(f'unknown source/locator: {rid} {locator}')
        block = paragraphs[locator]
        if block['rid'] != rid:
            raise ValueError(f'locator belongs to {block["rid"]}, not {rid}')
        if not nonempty(snippet) or len(snippet) > 200:
            raise ValueError('snippet must contain 1..200 characters')
        if norm(snippet) not in norm(block['text']):
            raise ValueError(f'unverified snippet at {locator}: {snippet}')
        clean = {'rid': rid, 'locator': locator, 'snippet': snippet}
        if clean not in found:
            found.append(clean)
    return found


def validate(directory):
    directory = Path(directory)
    manifest = json_read(directory / 'manifest.json')
    sources = source_map(manifest)
    paragraphs = {b['locator']: b for b in blocks(read(directory / 'sources.md'))}
    errors, unverified, low, candidates, id_map = [], [], [], [], {}
    seen = set()
    for original in jsonl_read(directory / 'extractions.jsonl'):
        item = deepcopy(original)
        try:
            ident = item.get('id')
            if not nonempty(ident) or ident in seen:
                raise ValueError('missing or duplicate extraction id')
            seen.add(ident)
            if item.get('type') not in TYPES:
                raise ValueError('invalid type')
            for field in ('content', 'speaker', 'sourceSnippet', 'sourceTimestamp', 'lang'):
                if not nonempty(item.get(field)):
                    raise ValueError(f'missing {field}')
            if not isinstance(item.get('relatedTerms'), list) or not all(nonempty(t) for t in item['relatedTerms']):
                raise ValueError('relatedTerms must be a list of strings')
            if item.get('chapter_hint') is not None and not isinstance(item['chapter_hint'], str):
                raise ValueError('chapter_hint must be text or null')
            if not isinstance(item.get('rids'), list) or not all(nonempty(v) for v in item['rids']):
                raise ValueError('rids must be a list of strings')
            confidence = item.get('confidence')
            if isinstance(confidence, bool) or not isinstance(confidence, (int, float)) or not math.isfinite(confidence) or not 0 <= confidence <= 100:
                raise ValueError('confidence must be finite number 0..100')
            evidence = evidence_check(item.get('evidence'), sources, paragraphs)
            rids = sorted({e['rid'] for e in evidence})
            if not isinstance(item.get('rids'), list) or sorted(set(item['rids'])) != rids:
                raise ValueError('rids must equal verified evidence source IDs')
            if not any(e['locator'] == item['sourceTimestamp'] and e['snippet'] == item['sourceSnippet'] for e in evidence):
                raise ValueError('sourceSnippet/sourceTimestamp must match primary evidence')
            speaker = item['speaker']
            if item['type'] == 'decision' and speaker != 'author' and not speaker.startswith('author-via-'):
                raise ValueError('decision must explicitly attribute the claim to the author')
            if speaker not in rids and speaker not in ['author-via-' + r for r in rids] and not (speaker == 'author' and 'BOOK' in rids) and not (speaker == 'user' and rids == ['NOTE']):
                raise ValueError('speaker is not supported by evidence')
            if 'NOTE' in rids and (item['type'] != 'opinion' or speaker != 'user' or rids != ['NOTE']):
                raise ValueError('personal notes must remain user opinions, separate from author claims')
            if any(sources[r]['sub_kind'] == 'auto_translated' for r in rids) and item['type'] not in ('decision', 'opinion'):
                raise ValueError('translated-only support cannot create action/question/term; use native support')
            contradicts = item.get('contradicts', [])
            if not isinstance(contradicts, list) or not all(nonempty(v) for v in contradicts):
                raise ValueError('contradicts must be an ID list')
            item['evidence'], item['rids'] = evidence, rids
            weakest = min(rids, key=lambda r: cap(sources[r]))
            item['confidence_original'] = confidence
            item['confidence'] = min(confidence, cap(sources[weakest]))
            item['sub_kind_min'] = sources[weakest]['sub_kind']
            if item['confidence'] < 60:
                low.append(item)
            else:
                candidates.append(item)
        except (ValueError, TypeError, KeyError) as exc:
            entry = {'id': item.get('id'), 'error': str(exc), 'record': original}
            errors.append(entry)
            if 'snippet' in str(exc) or 'locator' in str(exc):
                unverified.append(entry)
    # No fuzzy merging. Speaker/chapter/language/contradiction boundaries remain intact.
    merged = {}
    for item in sorted(candidates, key=lambda e: e['id']):
        key = (item['type'], norm(item['content']), item['speaker'], item.get('chapter_hint'),
               item['lang'], tuple(sorted(item.get('contradicts', []))))
        if key in merged:
            target = merged[key]
            id_map[item['id']] = target['id']
            target['evidence'] += [e for e in item['evidence'] if e not in target['evidence']]
            target['rids'] = sorted({e['rid'] for e in target['evidence']})
            target['relatedTerms'] = sorted(set(target['relatedTerms'] + item['relatedTerms']))
            target['confidence_original'] = max(target['confidence_original'], item['confidence_original'])
            weakest = min(target['rids'], key=lambda r: cap(sources[r]))
            target['confidence'] = min(target['confidence_original'], cap(sources[weakest]))
            target['sub_kind_min'] = sources[weakest]['sub_kind']
        else:
            merged[key] = item
            id_map[item['id']] = item['id']
    clean = list(merged.values())
    by_id = {e['id']: e for e in clean}
    for item in clean:
        targets = [id_map.get(v, v) for v in item.get('contradicts', [])]
        if any(v not in by_id or v == item['id'] for v in targets):
            errors.append({'id': item['id'], 'error': 'dangling/self contradicts reference'})
        item['contradicts'] = targets
    terms = []
    term_ids = set()
    for original in sorted(jsonl_read(directory / 'terms.jsonl', optional=True), key=lambda t: str(t.get('id', ''))):
        term = deepcopy(original)
        try:
            for field in ('id', 'term', 'term_vi', 'definition'):
                if not nonempty(term.get(field)):
                    raise ValueError(f'term missing {field}')
            if term['id'] in term_ids:
                raise ValueError('duplicate term id')
            if not isinstance(term.get('approved', False), bool):
                raise ValueError('approved must be a boolean')
            term_ids.add(term['id'])
            if not isinstance(term.get('aliases', []), list) or not all(nonempty(v) for v in term.get('aliases', [])):
                raise ValueError('invalid term aliases')
            term['evidence'] = evidence_check(term.get('evidence'), sources, paragraphs)
            term['rids'] = sorted({e['rid'] for e in term['evidence']})
            if any(sources[r]['sub_kind'] in ('auto_translated', 'note') for r in term['rids']):
                raise ValueError('term needs original/native source evidence')
            names = {term_key(v) for v in [term['term'], term['term_vi']] + term.get('aliases', [])}
            matches = [t for t in terms if names & t['_keys']]
            if len(matches) > 1:
                raise ValueError('ambiguous alias bridges multiple terms; resolve manually')
            if matches:
                target = matches[0]
                target['_keys'] |= names
                target['aliases'] = sorted(set(target['aliases'] + term.get('aliases', []) + [term['term'], term['term_vi']]))
                target['evidence'] += [e for e in term['evidence'] if e not in target['evidence']]
            else:
                term['_keys'] = names
                term.setdefault('aliases', [])
                term['approved'] = bool(term.get('approved', False))
                terms.append(term)
        except (ValueError, TypeError, KeyError) as exc:
            errors.append({'id': term.get('id'), 'error': str(exc), 'record': original})
            if 'snippet' in str(exc) or 'locator' in str(exc):
                unverified.append({'id': term.get('id'), 'error': str(exc)})
    for term in terms:
        term.pop('_keys')
        term['rids'] = sorted({e['rid'] for e in term['evidence']})
        # Frequency means verified passages, not an LLM's guessed token count.
        term['frequency'] = len({e['locator'] for e in term['evidence']})
        term['firstMentioned'] = min(term['evidence'], key=lambda e: paragraphs[e['locator']]['start'])['locator']
    qa_clean, qa_ids = [], set()
    for q in jsonl_read(directory / 'qa.jsonl', optional=True):
        try:
            if not nonempty(q.get('id')) or q['id'] in qa_ids:
                raise ValueError('missing/duplicate QA id')
            qa_ids.add(q['id'])
            if q.get('round') not in (1, 2, 3, 4) or not nonempty(q.get('question')):
                raise ValueError('QA requires round 1..4 and question')
            if q.get('origin') not in ('source', 'generated'):
                raise ValueError('QA origin must be source or generated')
            refs = q.get('evidence_ids', [])
            if not isinstance(refs, list) or not all(nonempty(v) for v in refs):
                raise ValueError('QA evidence_ids must be an ID list')
            q['evidence_ids'] = [id_map.get(v, v) for v in refs]
            if any(v not in by_id for v in q['evidence_ids']):
                raise ValueError('unknown QA extraction reference')
            if q.get('answer') is not None and not nonempty(q.get('answer')):
                raise ValueError('QA answer must be text or null')
            if q.get('answer') and not refs:
                raise ValueError('answered QA requires supporting extraction references')
            if not q.get('answer') and q['origin'] != 'generated':
                raise ValueError('unanswered QA must have origin=generated')
            qa_clean.append(q)
        except (ValueError, TypeError, KeyError) as exc:
            errors.append({'id': q.get('id'), 'error': str(exc), 'record': q})
    counts = Counter(e['type'] for e in clean)
    stats = {'schema_version': 1, 'input_fingerprint': fingerprint(directory),
             'chunks': len(json_read(directory / 'chunks/index.json')) if (directory / 'chunks/index.json').exists() else 1,
             'extractions': len(clean), 'new_terms': len(terms), 'generated_questions': sum(not q.get('answer') for q in qa_clean),
             'extractions_by_type': {t: counts[t] for t in TYPES},
             'by_source': dict(Counter(r for e in clean for r in e['rids'])),
             'unverified_snippets': unverified, 'errors': errors, 'low_confidence': len(low), 'id_map': id_map}
    for name, rows in [('extractions.clean.jsonl', clean), ('terms.clean.jsonl', terms), ('qa.clean.jsonl', qa_clean),
                       ('extractions_lowconf.jsonl', low), ('extractions.rejected.jsonl', errors)]:
        jsonl_write(directory / name, rows)
    stats['clean_hashes'] = {name: hashlib.sha256((directory / name).read_bytes()).hexdigest()
                             for name in ('extractions.clean.jsonl', 'terms.clean.jsonl', 'qa.clean.jsonl')}
    json_write(directory / 'extractions_stats.json', stats)
    return stats


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dir', type=Path, required=True)
    args = parser.parse_args()
    stats = validate(args.dir)
    print(f"extractions={stats['extractions']}; terms={stats['new_terms']}; errors={len(stats['errors'])}; unverified={len(stats['unverified_snippets'])}")
    raise SystemExit(1 if stats['errors'] else 0)


if __name__ == '__main__':
    main()
