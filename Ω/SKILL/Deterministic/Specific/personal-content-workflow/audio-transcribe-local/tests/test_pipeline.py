import copy
from dataclasses import dataclass
import json
from pathlib import Path
import sys
import tempfile
import unittest
from types import SimpleNamespace
import wave
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from common import fingerprint, stamp, validate_segments, write_json, read_json
from inventory import inventory
from quality_report import analyze
from transcribe import valid_cache, worker_command, parser, run_batch, run_file
from assemble import validate_editorial

class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.raw = {'duration_s': 4000, 'segments': [{'id': 'S00001', 'start': 3601, 'end': 3603,
            'text': 'Không được bỏ điều kiện.', 'avg_logprob': -.3, 'no_speech_prob': .01}]}
        self.editorial = {'raw_content_hash': fingerprint(self.raw['segments']), 'reviewed_segment_ids': ['S00001']}
        self.knowledge = {'claims': [{'id': 'C1', 'text': 'Giữ điều kiện.', 'confidence': 'vừa', 'confidence_reason': 'Có lời trực tiếp.',
            'evidence': [{'segment_id': 'S00001', 'quote': 'Không được bỏ điều kiện.'}]}]}

    def test_unicode_duplicate_and_slug_collision(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name, body in [('Voice 010.m4a', b'a'), ('Voice 010 (2).m4a', b'a'), ('thầy.m4a', b'b'), ('thay.m4a', b'c')]:
                (root/name).write_bytes(body)
            with patch('inventory.probe', return_value={'duration_s': 1, 'sample_rate': 16000, 'channels': 1}):
                rows = inventory(root)
            self.assertEqual(len({r['slug'] for r in rows}), 4)
            duplicate = next(r for r in rows if r['file']=='Voice 010 (2).m4a')
            self.assertEqual(duplicate['duplicate_of'], 'voice-010')
            self.assertEqual(len(list(root.iterdir())), 4)

    def test_decode_error_is_recorded(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp)/'bad.m4a').write_bytes(b'broken')
            with patch('inventory.probe', side_effect=ValueError('decode failed')):
                self.assertIn('decode failed', inventory(tmp)[0]['error'])

    def test_timestamp_over_hour(self):
        self.assertEqual(stamp(3601.123, True), '01:00:01,123')
        validate_segments(self.raw)

    def test_empty_speech_is_not_confident_success(self):
        self.raw['segments'] = []
        result = analyze(self.raw)
        self.assertEqual(result['status'], 'no_usable_speech')
        self.assertEqual(result['untranscribed_gaps'][0]['end'], 4000)

    def test_bad_acoustics_and_repetition(self):
        self.raw['segments'][0].update(text='a b c d a b c d a b c d', avg_logprob=-1.2)
        result = analyze(self.raw)
        self.assertEqual(result['flagged_pct'], 100)
        self.assertIn('repetition', result['review_segments'][0]['flags'])

    def test_cache_requires_content_and_config(self):
        self.raw.update(status='asr_complete', run_key='abc', content_hash=fingerprint(self.raw['segments']))
        self.assertTrue(valid_cache(self.raw, 'abc'))
        self.assertFalse(valid_cache(self.raw, 'changed'))
        self.raw['segments'][0]['text'] = 'tampered'
        self.assertFalse(valid_cache(self.raw, 'abc'))

    def test_atomic_checkpoint_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)/'checkpoint.json'
            write_json(p, {'complete': 1})
            write_json(p, {'complete': 2})
            self.assertEqual(read_json(p)['complete'], 2)
            self.assertEqual(len(list(Path(tmp).iterdir())), 1)

    def test_fallback_worker_is_separate_and_explicit(self):
        args = parser().parse_args([])
        command = worker_command(args, 'source.m4a', 'out', True)
        self.assertEqual(command[command.index('--model')+1], 'medium')
        self.assertEqual(command[command.index('--compute-type')+1], 'int8')

    def test_batch_oom_fallback_resume_and_source_provenance(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            args = parser().parse_args(['--output', str(output)])
            row = {'slug':'sample','file':'sample.m4a','path':'sample.m4a',
                'sha256':'source-hash','error':'','duplicate_of':''}
            config = {'model':'large-v3','device':'cuda','compute_type':'int8_float16','beam_size':5}
            commands = []
            class Worker:
                def __init__(self, command, **kwargs):
                    commands.append(command)
                    self.fallback = command[command.index('--model')+1] == 'medium'
                    self.stdout = iter(['COMPLETE\n'] if self.fallback else ['CUDA out of memory\n'])
                def wait(self):
                    if self.fallback:
                        actual = {**config,'model':'medium','compute_type':'int8','beam_size':3}
                        raw = {'status':'asr_complete','source_sha256':'source-hash','config':actual,
                            'run_key':fingerprint({'sha256':'source-hash','config':actual}),
                            'segments':[],'content_hash':fingerprint([]),'duration_s':10,'processing_s':1}
                        write_json(output/'_work/sample/raw.json', raw)
                        write_json(output/'_work/sample/quality.json', {'flagged_pct':0})
                    return 0 if self.fallback else 1
            with patch('transcribe.save_inventory', return_value=[row]), patch('transcribe.configuration', return_value=config), \
                patch('transcribe.subprocess.Popen', side_effect=Worker), patch('transcribe.export'):
                self.assertEqual(run_batch(args), 0)
                self.assertEqual(len(commands), 2)
                self.assertEqual(run_batch(args), 0)
                self.assertEqual(len(commands), 2, 'valid fallback cache should resume without a worker')
                raw_path = output/'_work/sample/raw.json'
                raw = read_json(raw_path)
                raw['source_sha256'] = 'unrelated-source'
                write_json(raw_path, raw)
                self.assertEqual(run_batch(args), 0)
                self.assertEqual(len(commands), 4, 'wrong-source cache must be recomputed')

    def test_batch_non_oom_error_does_not_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = parser().parse_args(['--output', tmp])
            row = {'slug':'bad','file':'bad.m4a','path':'bad.m4a', 'sha256':'x','error':'','duplicate_of':''}
            class Worker:
                stdout = ['invalid audio data\n']
                def wait(self): return 1
            with patch('transcribe.save_inventory', return_value=[row]), patch('transcribe.configuration', return_value={}), \
                patch('transcribe.subprocess.Popen', return_value=Worker()) as launch:
                self.assertEqual(run_batch(args), 1)
                self.assertEqual(launch.call_count, 1)
                self.assertEqual(read_json(Path(tmp)/'_reports/checkpoint.json')['files']['bad']['status'], 'error')

    def test_interrupted_file_resumes_chunks_and_changed_source_recomputes(self):
        @dataclass
        class Word:
            start: float
            end: float
            word: str
        @dataclass
        class Segment:
            start: float
            end: float
            text: str
            words: list
        class Model:
            calls = 0
            def transcribe(self, samples, **kwargs):
                self.calls += 1
                if self.calls == 2:
                    raise RuntimeError('interrupted before second checkpoint')
                segments = [Segment(.2,.4,'một',[Word(.2,.4,' một')]),
                    Segment(1.2,1.4,'hai',[Word(1.2,1.4,' hai')])]
                return iter(segments), None
        model = Model()
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            source = folder/'source.m4a'
            source.write_bytes(b'original-source')
            wav = folder/'fixture.wav'
            with wave.open(str(wav),'wb') as audio:
                audio.setnchannels(1)
                audio.setsampwidth(2)
                audio.setframerate(16000)
                audio.writeframes(b'\x00\x00'*32000)
            args = parser().parse_args(['--input',str(source),'--output',str(folder/'out'),
                '--device','cpu','--compute-type','int8','--chunk-seconds','1'])
            with patch('transcribe.preprocess',return_value=wav), \
                patch.dict(sys.modules, {'faster_whisper':SimpleNamespace(WhisperModel=lambda *a,**k:model)}):
                with self.assertRaisesRegex(RuntimeError,'interrupted'):
                    run_file(args)
                self.assertTrue((folder/'out/chunks/0000.json').exists())
                self.assertFalse((folder/'out/raw.json').exists())
                raw = run_file(args)
                self.assertEqual(model.calls,3)
                self.assertEqual([s['text'] for s in raw['segments']],['một','hai'])
                source.write_bytes(b'changed-source')
                changed = run_file(args)
                self.assertEqual(model.calls,5)
                self.assertNotEqual(raw['run_key'],changed['run_key'])

    def test_full_editorial_coverage_required(self):
        validate_editorial(self.raw, self.editorial, self.knowledge)
        self.editorial['reviewed_segment_ids'] = []
        with self.assertRaisesRegex(ValueError, 'coverage'):
            validate_editorial(self.raw, self.editorial, self.knowledge)

    def test_fabricated_evidence_rejected(self):
        self.knowledge['claims'][0]['evidence'][0]['quote'] = 'được bỏ điều kiện khác'
        with self.assertRaisesRegex(ValueError, 'evidence'):
            validate_editorial(self.raw, self.editorial, self.knowledge)

    def test_changed_source_invalidates_editorial(self):
        self.raw['segments'][0]['text'] = 'Được bỏ điều kiện.'
        with self.assertRaisesRegex(ValueError, 'source changed'):
            validate_editorial(self.raw, self.editorial, self.knowledge)

    def test_unfounded_verified_claim_rejected(self):
        self.knowledge['claims'][0]['verification'] = 'đã kiểm chứng'
        with self.assertRaisesRegex(ValueError, 'external source'):
            validate_editorial(self.raw, self.editorial, self.knowledge)

if __name__ == '__main__':
    unittest.main()
