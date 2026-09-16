"""Local CUDA ASR with atomic per-chunk checkpoints and process-isolated file workers."""
from __future__ import annotations
import argparse
from dataclasses import asdict
import importlib.metadata
import math
import os
from pathlib import Path
import subprocess
import sys
import time
import wave
from common import (DEFAULT_INPUT, DEFAULT_OUTPUT, VERSION, digest, fingerprint, now,
    read_json, setup_cuda, stamp, validate_segments, write_csv, write_json, write_text)
from inventory import save_inventory, probe
from preprocess import preprocess
from quality_report import report

def configuration(args):
    return {'version': VERSION, 'model': args.model, 'device': args.device,
        'compute_type': args.compute_type, 'beam_size': args.beam_size,
        'denoise': args.denoise, 'language': args.language, 'prompt': args.prompt,
        'chunk_seconds': args.chunk_seconds, 'limit_seconds': args.seconds,
        'vad_filter': True, 'vad_parameters': {'min_silence_duration_ms': 500, 'speech_pad_ms': 200},
        'condition_on_previous_text': False, 'word_timestamps': True,
        'temperature': [0, .2, .4], 'best_of': 5,
        'faster_whisper': importlib.metadata.version('faster-whisper'),
        'ctranslate2': importlib.metadata.version('ctranslate2')}

def export(raw, directory):
    validate_segments(raw)
    write_json(directory / 'raw.json', raw)
    write_text(directory / 'raw.txt', '\n'.join(f"[{stamp(s['start'])}] {s['text']}" for s in raw['segments']) + '\n')
    write_text(directory / 'raw.srt', '\n'.join(f"{i}\n{stamp(s['start'], True)} --> {stamp(s['end'], True)}\n{s['text']}\n" for i, s in enumerate(raw['segments'], 1)))
    return report(raw, directory)

def valid_cache(raw, key):
    if not raw or raw.get('run_key') != key or raw.get('status') != 'asr_complete':
        return False
    try:
        validate_segments(raw)
        return raw['content_hash'] == fingerprint(raw['segments'])
    except (KeyError, ValueError, TypeError):
        return False

def run_file(args):
    source, directory = args.input.resolve(), args.output.resolve()
    directory.mkdir(parents=True, exist_ok=True)
    config = configuration(args)
    source_hash = digest(source)
    key = fingerprint({'sha256': source_hash, 'config': config})
    previous = read_json(directory / 'raw.json')
    if valid_cache(previous, key) and not args.force:
        export(previous, directory)
        print(f'REUSED {source.name}', flush=True)
        return previous
    started = time.perf_counter()
    wav = preprocess(source, directory / 'audio_16k.wav', args.denoise, args.seconds)
    if args.device == 'cuda':
        setup_cuda()
    import numpy as np
    from faster_whisper import WhisperModel
    model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type, local_files_only=True)
    with wave.open(str(wav), 'rb') as audio:
        sr = audio.getframerate()
        duration = audio.getnframes() / sr
        segments = []
        for index in range(math.ceil(duration / args.chunk_seconds)):
            core_start = index * args.chunk_seconds
            core_end = min(duration, core_start + args.chunk_seconds)
            chunk_path = directory / 'chunks' / f'{index:04}.json'
            chunk = read_json(chunk_path)
            if args.force or not chunk or chunk.get('run_key') != key or chunk.get('content_hash') != fingerprint(chunk.get('segments')):
                offset = max(0, core_start - 2)
                end = min(duration, core_end + 2)
                audio.setpos(round(offset * sr))
                samples = np.frombuffer(audio.readframes(round((end-offset)*sr)), dtype=np.int16).astype(np.float32) / 32768
                generated, info = model.transcribe(samples, language=args.language, beam_size=args.beam_size,
                    best_of=5, temperature=[0, .2, .4], vad_filter=True,
                    vad_parameters=config['vad_parameters'], word_timestamps=True,
                    condition_on_previous_text=False, initial_prompt=args.prompt or None)
                rows = []
                for segment in generated:
                    data = asdict(segment)
                    words = []
                    for word in data.get('words') or []:
                        word['start'] += offset
                        word['end'] += offset
                        midpoint = (word['start'] + word['end']) / 2
                        if core_start <= midpoint < core_end:
                            words.append(word)
                    if not words:
                        continue
                    data.update(start=max(core_start, words[0]['start']), end=min(core_end, words[-1]['end']),
                        text=''.join(w['word'] for w in words).strip(), words=words)
                    data.pop('tokens', None)
                    if data['text']:
                        rows.append(data)
                chunk = {'run_key': key, 'start': core_start, 'end': core_end, 'segments': rows, 'content_hash': fingerprint(rows)}
                write_json(chunk_path, chunk)
            segments.extend(chunk['segments'])
            write_json(directory / 'progress.json', {'run_key': key, 'source': source.name, 'completed_seconds': core_end,
                'duration_s': duration, 'updated': now(), 'model': args.model})
            print(f'PROGRESS {source.name} {core_end:.0f}/{duration:.0f}s {len(segments)} segments', flush=True)
    segments.sort(key=lambda s: s['start'])
    for i, segment in enumerate(segments, 1):
        segment['id'] = f'S{i:05}'
    raw = {'schema_version': VERSION, 'source': str(source), 'source_sha256': source_hash,
        'duration_s': duration, 'config': config, 'run_key': key, 'status': 'asr_complete',
        'created': now(), 'processing_s': time.perf_counter()-started, 'segments': segments,
        'content_hash': fingerprint(segments)}
    export(raw, directory)
    print(f'COMPLETE {source.name} {raw["processing_s"]:.1f}s', flush=True)
    return raw

def worker_command(args, source, target, fallback=False):
    command = [sys.executable, '-X', 'utf8', '-u', '-B', str(Path(__file__).resolve()),
        '--input', str(source), '--output', str(target), '--model', 'medium' if fallback else args.model,
        '--compute-type', 'int8' if fallback else args.compute_type,
        '--beam-size', '3' if fallback else str(args.beam_size), '--chunk-seconds', str(args.chunk_seconds),
        '--device', args.device, '--language', args.language]
    if args.denoise:
        command.append('--denoise')
    if args.force:
        command.append('--force')
    if args.prompt:
        command += ['--prompt', args.prompt]
    return command

def run_batch(args):
    output = args.output.resolve()
    rows = save_inventory(args.input, output)
    checkpoint_path = args.checkpoint or output / '_reports' / 'checkpoint.json'
    checkpoint = read_json(checkpoint_path, {'version': VERSION, 'files': {}})
    logs = []
    errors = 0
    for row in rows:
        ident = row['slug']
        if row['error'] or row['duplicate_of']:
            checkpoint['files'][ident] = {'status': 'input_error' if row['error'] else 'duplicate',
                'duplicate_of': row['duplicate_of'], 'error': row['error'], 'sha256': row['sha256']}
            errors += bool(row['error'])
            write_json(checkpoint_path, checkpoint)
            continue
        directory = output / '_work' / ident
        directory.mkdir(parents=True, exist_ok=True)
        old = checkpoint['files'].get(ident, {})
        requested = configuration(args)
        config_key = fingerprint(requested)
        cached = read_json(directory / 'raw.json')
        cached_config = (cached or {}).get('config', {})
        allowed_configs = [requested, {**requested, 'model': 'medium', 'compute_type': 'int8', 'beam_size': 3}]
        cached_key = fingerprint({'sha256': row['sha256'], 'config': cached_config})
        if (not args.force and old.get('requested_config') == config_key and old.get('sha256') == row['sha256']
            and cached and cached.get('source_sha256') == row['sha256'] and cached_config in allowed_configs
            and valid_cache(cached, cached_key) and old.get('status') == 'asr_complete'):
            export(cached, directory)
        else:
            checkpoint['files'][ident] = {'status': 'running', 'sha256': row['sha256'], 'requested_config': config_key, 'started': now()}
            write_json(checkpoint_path, checkpoint)
            code, error_text = 1, ''
            for fallback in (False, True):
                log_path = directory / ('worker_fallback.log' if fallback else 'worker.log')
                with log_path.open('w', encoding='utf-8') as log:
                    process = subprocess.Popen(worker_command(args, row['path'], directory, fallback),
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
                    for line in process.stdout:
                        print(line.rstrip(), flush=True)
                        log.write(line)
                        log.flush()
                    code = process.wait()
                error_text = log_path.read_text(encoding='utf-8')[-6000:]
                if code == 0 or not any(s in error_text.lower() for s in ('out of memory', 'cuda_error_out_of_memory')):
                    break
            checkpoint['files'][ident].update(status='asr_complete' if code == 0 else 'error',
                finished=now(), error='' if code == 0 else error_text)
            errors += code != 0
            write_json(checkpoint_path, checkpoint)
        raw = read_json(directory / 'raw.json')
        if checkpoint['files'][ident]['status'] == 'asr_complete' and raw:
            q = read_json(directory / 'quality.json')
            logs.append({'file': row['file'], 'model': raw['config']['model'], 'device': raw['config']['device'],
                'compute_type': raw['config']['compute_type'], 'duration_s': raw['duration_s'],
                'processing_s': round(raw['processing_s'], 2), 'rtf': round(raw['processing_s']/raw['duration_s'], 3),
                'flagged_pct': q['flagged_pct'], 'status': 'asr_complete'})
            write_csv(output / '_reports' / 'run_log.csv', logs,
                ['file', 'model', 'device', 'compute_type', 'duration_s', 'processing_s', 'rtf', 'flagged_pct', 'status'])
    return int(errors > 0)

def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input', type=Path, default=DEFAULT_INPUT)
    p.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    p.add_argument('--batch', action='store_true')
    p.add_argument('--checkpoint', type=Path)
    p.add_argument('--model', default='large-v3')
    p.add_argument('--compute-type', default='int8_float16')
    p.add_argument('--device', choices=['cuda', 'cpu'], default='cuda')
    p.add_argument('--language', default='vi')
    p.add_argument('--beam-size', type=int, default=5)
    p.add_argument('--chunk-seconds', type=int, default=600)
    p.add_argument('--denoise', action='store_true')
    p.add_argument('--seconds', type=float)
    p.add_argument('--prompt', default='')
    p.add_argument('--force', action='store_true')
    return p

if __name__ == '__main__':
    args = parser().parse_args()
    if args.chunk_seconds <= 0 or (args.seconds is not None and args.seconds <= 0):
        raise SystemExit('duration must be positive')
    if args.batch:
        if args.seconds is not None:
            raise SystemExit('--seconds is a single-file calibration option')
        raise SystemExit(run_batch(args))
    run_file(args)
