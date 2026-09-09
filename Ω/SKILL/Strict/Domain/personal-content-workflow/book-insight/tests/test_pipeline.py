import csv
import io
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from common import blocks, core_ideas, json_read, json_write, jsonl_read, jsonl_write, read, write
from fetch_reviews import parse_subtitles, subtitle_options, rejection
from merge_sources import book_blocks
from chunk_sources import chunk
from validate_extractions import validate
from assemble_insight import assemble, export_cards


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.manifest = {'book': {'title_vi': 'Thử nghiệm', 'title_orig': 'Test Book', 'author': 'Test', 'year': 2026},
                         'sources': [{'rid': 'R1', 'id': 'a', 'channel': 'A', 'duration_s': 600, 'sub_kind': 'manual'},
                                     {'rid': 'R2', 'id': 'b', 'channel': 'B', 'duration_s': 600, 'sub_kind': 'auto_translated'}],
                         'supplements': [{'rid': 'BOOK', 'sub_kind': 'book_text', 'reading_state': 'full-read'}]}
        self.text = '# Sources\n\n[R1 00:01]\nTruyền hình làm giảm khả năng lập luận.\n\n[R2 00:02]\nTruyền hình không làm giảm khả năng lập luận.\n\n[BOOK ch.1 ¶1]\nMột khái niệm nền tảng.\n'
        json_write(self.root / 'manifest.json', self.manifest)
        write(self.root / 'sources.md', self.text)
        jsonl_write(self.root / 'extractions.jsonl', [])
        jsonl_write(self.root / 'terms.jsonl', [])
        jsonl_write(self.root / 'qa.jsonl', [])

    def tearDown(self):
        self.tmp.cleanup()

    def item(self, ident='e1', rid='R1', confidence=85, content='Truyền hình làm giảm khả năng lập luận.'):
        p = next(p for p in blocks(self.text) if p['rid'] == rid)
        return {'id': ident, 'type': 'decision', 'content': content, 'confidence': confidence,
                'speaker': 'author' if rid == 'BOOK' else 'author-via-' + rid,
                'sourceSnippet': p['text'], 'sourceTimestamp': p['locator'], 'relatedTerms': [],
                'rids': [rid], 'chapter_hint': None, 'sub_kind_min': 'manual', 'lang': 'vi',
                'evidence': [{'rid': rid, 'locator': p['locator'], 'snippet': p['text']}]}

    def run_items(self, items):
        jsonl_write(self.root / 'extractions.jsonl', items)
        return validate(self.root)

    def test_snippet_wrong_source_rejected(self):
        item = self.item()
        item['evidence'][0]['locator'] = 'R2 00:02'
        stats = self.run_items([item])
        self.assertEqual(stats['extractions'], 0)
        self.assertEqual(len(stats['unverified_snippets']), 1)

    def test_fabricated_support_rid_rejected(self):
        item = self.item()
        item['rids'].append('R2')
        self.assertTrue(self.run_items([item])['errors'])

    def test_fake_snippet_rejected(self):
        item = self.item()
        item['evidence'][0]['snippet'] = 'Invented quote'
        self.assertTrue(self.run_items([item])['unverified_snippets'])

    def test_no_fuzzy_merge_of_negation(self):
        a, b = self.item(), self.item('e2')
        b['content'] = 'Truyền hình không làm giảm khả năng lập luận.'
        self.assertEqual(self.run_items([a, b])['extractions'], 2)

    def test_boundary_and_translated_cap(self):
        stats = self.run_items([self.item('e1', confidence=59), self.item('e2', confidence=60), self.item('e3', 'R2', 98)])
        self.assertEqual(stats['low_confidence'], 1)
        self.assertEqual([e['confidence'] for e in jsonl_read(self.root / 'extractions.clean.jsonl')], [60, 70])

    def test_bad_confidence(self):
        for value in (True, float('nan'), -1, 101, '90'):
            with self.subTest(value=value):
                self.assertTrue(self.run_items([self.item(confidence=value)])['errors'])

    def test_duplicate_source_ids_rejected(self):
        self.manifest['sources'].append(self.manifest['sources'][0])
        json_write(self.root / 'manifest.json', self.manifest)
        with self.assertRaises(ValueError):
            validate(self.root)

    def test_book_only_core_idea(self):
        item = self.item(rid='BOOK')
        self.assertEqual(len(core_ideas([item], self.manifest)), 1)

    def test_same_channel_not_independent(self):
        item = self.item()
        item['rids'] = ['R1', 'R2']
        self.manifest['sources'][1]['channel'] = 'A'
        self.assertEqual(core_ideas([item], self.manifest), [])

    def test_alias_dedup_idempotent(self):
        e = self.item()['evidence']
        a = {'id': 't1', 'term': 'behavior', 'term_vi': 'hành vi', 'definition': 'định nghĩa', 'aliases': ['behaviour'], 'evidence': e}
        b = {**a, 'id': 't2', 'term': 'behaviour'}
        jsonl_write(self.root / 'terms.jsonl', [a, b])
        first = validate(self.root)
        data = read(self.root / 'terms.clean.jsonl')
        validate(self.root)
        self.assertEqual(first['new_terms'], 1)
        self.assertEqual(jsonl_read(self.root / 'terms.clean.jsonl')[0]['frequency'], 1)
        self.assertEqual(data, read(self.root / 'terms.clean.jsonl'))

    def test_unanswered_qa_is_not_source_extraction(self):
        jsonl_write(self.root / 'qa.jsonl', [{'id': 'Q1', 'round': 1, 'question': 'Vì sao?', 'answer': None, 'origin': 'generated', 'evidence_ids': []}])
        stats = validate(self.root)
        self.assertFalse(stats['errors'])
        self.assertEqual(stats['generated_questions'], 1)
        self.assertEqual(stats['extractions'], 0)

    def test_stale_raw_and_tampered_clean_block_assembly(self):
        self.run_items([self.item()])
        write(self.root / 'sources.md', self.text + '\n')
        with self.assertRaisesRegex(ValueError, 'inputs changed'):
            assemble(self.root, draft=True)
        validate(self.root)
        write(self.root / 'extractions.clean.jsonl', '')
        with self.assertRaisesRegex(ValueError, 'modified outside'):
            assemble(self.root, draft=True)

    def test_subtitles_srt_vtt_rolling_and_html(self):
        vtt = 'WEBVTT\n\n00:00:01.000 --> 00:00:02.000\n<c>Hello &amp; world</c>\n\n00:00:02.000 --> 00:00:03.000\nHello &amp; world again\n\n'
        self.assertEqual(parse_subtitles(vtt), [{'t': 1., 'text': 'Hello & world'}, {'t': 2., 'text': 'again'}])
        srt = '1\n00:00:01,400 --> 00:00:02,500\nXin chào.\n\n2\n00:00:02,600 --> 00:00:04,000\nTiếp theo.\n'
        self.assertEqual(parse_subtitles(srt)[0], {'t': 1.4, 'text': 'Xin chào.'})

    def test_machine_translation_identified_by_url(self):
        info = {'automatic_captions': {'vi': [{'url': 'https://example.org/caption?lang=en&tlang=vi'}], 'en-orig': [{'url': 'https://example.org/caption?lang=en'}]}}
        opts = subtitle_options(info, ['vi', 'en'])
        self.assertEqual(opts[0][1:3], ('en-orig', 'auto_native'))
        self.assertEqual(opts[1][2], 'auto_translated')

    def test_wrong_book_rejection(self):
        import argparse
        args = argparse.Namespace(book='Giải trí đến chết', title_orig='Amusing Ourselves to Death', min_minutes=5)
        self.assertIn('off-topic', rejection({'title': 'Guilty Bonds review', 'duration': 600}, args))
        self.assertIn('audiobook', rejection({'title': 'Amusing Ourselves to Death audiobook', 'duration': 600}, args))

    def test_chunks_round_trip_no_orphan_label(self):
        result = chunk(self.text, 80)
        reconstructed = ''.join(self.text[start:end] for start, end, _ in result)
        self.assertEqual(reconstructed, self.text[self.text.index('[R1'):])
        for start, end, _ in result:
            self.assertTrue(blocks(self.text[start:end]))

    def test_book_chapters(self):
        result = book_blocks('Chapter 1 First\n\nText one.\n\nChapter 2 Next\n\nText two.')
        self.assertEqual([p[0] for p in result], ['BOOK ch.1 ¶1', 'BOOK ch.1 ¶2', 'BOOK ch.2 ¶1', 'BOOK ch.2 ¶2'])

    def test_draft_has_all_thirteen_sections(self):
        self.run_items([self.item()])
        for file in ('part1_summary.md', 'part2_map.md', 'part3_extractions.md'):
            write(self.root / file, '')
        output = assemble(self.root, draft=True)
        self.assertTrue(output.name.endswith('_DRAFT.md'))
        self.assertEqual(sum(line.startswith('## ') for line in read(output).splitlines()), 13)
        with self.assertRaises(ValueError):
            assemble(self.root)

    def test_anki_id_stable_on_reorder_and_edit(self):
        a = self.item('a', 'BOOK')
        b = self.item('b', 'BOOK', content='Another idea')
        export_cards(self.root, 'book', 'Book', [a, b], [], [], self.manifest)
        before = json_read(self.root / 'anki_ids.json')
        b['content'] = 'Updated idea'
        export_cards(self.root, 'book', 'Book', [b, a], [], [], self.manifest)
        self.assertEqual(before, json_read(self.root / 'anki_ids.json'))
        rows = list(csv.reader(io.StringIO('\n'.join(l for l in read(self.root / 'cards.csv').splitlines() if not l.startswith('#')))))
        self.assertEqual(len(rows), 2)
        self.assertEqual(len({r[0] for r in rows}), 2)

    def test_dedup_ids_stable_after_raw_reorder(self):
        a, b = self.item('a'), self.item('b')
        self.run_items([a, b])
        first = read(self.root / 'extractions.clean.jsonl')
        self.run_items([b, a])
        self.assertEqual(first, read(self.root / 'extractions.clean.jsonl'))

    def test_embedded_manual_timing_line_removed(self):
        text = 'WEBVTT\n\n00:00:00.599 --> 00:00:05.600\n0:00:00.599,0:00:05.600\nHello.\n'
        self.assertEqual(parse_subtitles(text)[0]['text'], 'Hello.')

    def test_book_and_notes_cli_integration(self):
        import subprocess
        scripts = Path(__file__).resolve().parents[1] / 'scripts'
        write(self.root / 'book.txt', 'Chapter 1 Evidence\n\nA claim needs evidence.\n\nChapter 2 Limits\n\nA model has limits.\n')
        write(self.root / 'notes.md', 'My own opinion.')
        self.manifest['sources'] = []
        json_write(self.root / 'manifest.json', self.manifest)
        subprocess.run([sys.executable, str(scripts / 'merge_sources.py'), '--dir', str(self.root), '--book-text', str(self.root / 'book.txt'), '--notes', str(self.root / 'notes.md'), '--reading-state', 'full-read'], check=True, capture_output=True)
        subprocess.run([sys.executable, str(scripts / 'chunk_sources.py'), '--dir', str(self.root)], check=True, capture_output=True)
        self.text = read(self.root / 'sources.md')
        item = self.item(rid='BOOK', content='The test book introduces evidence.')
        stats = self.run_items([item])
        self.assertFalse(stats['errors'])
        self.assertEqual(stats['by_source'], {'BOOK': 1})
        for file in ('part1_summary.md', 'part2_map.md', 'part3_extractions.md'):
            write(self.root / file, '')
        result = read(assemble(self.root, draft=True))
        self.assertIn('source_quality: "full-read"', result)
        self.assertIn('BOOK ch.1', result)

    def test_broken_qa_reference_rejected(self):
        jsonl_write(self.root / 'qa.jsonl', [{'id': 'Q1', 'round': 1, 'question': 'Why?', 'answer': 'Answer', 'origin': 'source', 'evidence_ids': ['missing']}])
        self.assertTrue(validate(self.root)['errors'])

    def test_translated_new_term_rejected(self):
        item = self.item(rid='R2')
        item['type'] = 'term'
        self.assertTrue(self.run_items([item])['errors'])

    def test_dangling_contradiction_rejected(self):
        item = self.item()
        item['contradicts'] = ['missing']
        self.assertTrue(self.run_items([item])['errors'])

    def test_reviewer_claim_cannot_be_author_decision(self):
        item = self.item()
        item['speaker'] = 'R1'
        self.assertTrue(self.run_items([item])['errors'])

    def test_import_registry_survives_source_removal(self):
        import subprocess
        scripts = Path(__file__).resolve().parents[1] / 'scripts'
        cached, output = self.root / 'cache', self.root / 'run'
        cached.mkdir()
        for ident in ('a', 'b', 'c'):
            write(cached / f'{ident}.en.srt', '1\n00:00:01,000 --> 00:00:02,000\nOne sentence.\n')
        base = [sys.executable, str(scripts / 'fetch_reviews.py'), '--book', 'Test', '--title-orig', 'Test', '--author', 'Test', '--year', '2026', '--n', '1', '--import-dir', str(cached), '--out', str(output), '--catalog', str(self.root / 'catalog.json')]
        for ids in [('a', 'b'), ('a',), ('c', 'b')]:
            json_write(self.root / 'catalog.json', [{'id': ident, 'channel': ident, 'title': ident, 'lang': 'en', 'subtitle_file': f'{ident}.en.srt'} for ident in ids])
            subprocess.run(base, check=True, capture_output=True)
        registry = json_read(output / 'manifest.json')['rid_registry']
        self.assertEqual(registry, {'a': 'R1', 'b': 'R2', 'c': 'R3'})


if __name__ == '__main__':
    unittest.main()
