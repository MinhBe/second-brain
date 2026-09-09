"""Normalize a source without trimming silence or changing the original timeline."""
import argparse
from pathlib import Path
import subprocess
import wave
from common import digest, read_json, write_json

def preprocess(source, target, denoise=False, seconds=None, channel=None):
    source, target = Path(source).resolve(), Path(target).resolve()
    if source == target:
        raise ValueError('source and output must differ')
    config = {'sha256': digest(source), 'denoise': denoise, 'seconds': seconds, 'channel': channel, 'version': 1}
    meta = target.with_suffix('.meta.json')
    if target.exists() and read_json(meta) == config:
        with wave.open(str(target), 'rb') as w:
            if w.getframerate() == 16000 and w.getnchannels() == 1 and w.getnframes() > 0:
                return target
    target.parent.mkdir(parents=True, exist_ok=True)
    temp = target.with_name(target.stem + '.partial.wav')
    filters = []
    if channel is not None:
        filters.append(f'pan=mono|c0=c{channel}')
    if denoise:
        filters += ['highpass=f=80', 'lowpass=f=7800', 'afftdn=nf=-25:nt=w']
    filters.append('loudnorm=I=-16:TP=-1.5:LRA=11')
    command = ['ffmpeg', '-nostdin', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source)]
    if seconds is not None:
        command += ['-t', str(seconds)]
    command += ['-af', ','.join(filters), '-ac', '1', '-ar', '16000', '-c:a', 'pcm_s16le', str(temp)]
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if result.returncode:
        raise RuntimeError(result.stderr[-3000:])
    with wave.open(str(temp), 'rb') as w:
        if w.getnframes() == 0:
            raise ValueError('decoded audio is empty')
    temp.replace(target)
    write_json(meta, config)
    return target

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--in', dest='source', type=Path, required=True)
    parser.add_argument('--out', dest='target', type=Path, required=True)
    parser.add_argument('--denoise', action='store_true')
    parser.add_argument('--seconds', type=float)
    parser.add_argument('--channel', type=int, choices=[0, 1])
    args = parser.parse_args()
    print(preprocess(args.source, args.target, args.denoise, args.seconds, args.channel))
