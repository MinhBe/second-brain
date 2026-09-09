"""Run the planned two-source, two-model, two-filter comparison without a domain prompt."""
import subprocess
import sys
from pathlib import Path
from common import DEFAULT_INPUT, DEFAULT_OUTPUT, read_json, write_json, write_csv

def main():
    root = DEFAULT_OUTPUT / '_calibration'
    rows = []
    for source in ['Voice 016.m4a', 'Record thầy Lâm (2).m4a']:
        for model in ['large-v3', 'medium']:
            for denoise in [False, True]:
                target = root / ('voice-016' if source.startswith('Voice') else 'record-thay-lam-2') / (model + ('-denoise' if denoise else '-baseline'))
                target.mkdir(parents=True, exist_ok=True)
                cmd = [sys.executable, '-X', 'utf8', '-u', '-B', str(Path(__file__).with_name('transcribe.py')),
                    '--input', str(DEFAULT_INPUT/source), '--output', str(target), '--model', model, '--seconds', '300']
                if denoise:
                    cmd.append('--denoise')
                with (target/'worker.log').open('w', encoding='utf-8') as log:
                    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
                    for line in p.stdout:
                        print(line.rstrip(), flush=True)
                        log.write(line)
                        log.flush()
                    code = p.wait()
                raw, quality = read_json(target/'raw.json', {}), read_json(target/'quality.json', {})
                rows.append({'source': source, 'model': model, 'denoise': denoise, 'exit_code': code,
                    'segments': quality.get('segments'), 'flagged_pct': quality.get('flagged_pct'),
                    'processing_s': raw.get('processing_s'), 'text_chars': sum(len(s['text']) for s in raw.get('segments', []))})
                write_json(root/'comparison.json', rows)
                write_csv(root/'comparison.csv', rows, list(rows[0]))
    return int(any(r['exit_code'] for r in rows))

if __name__ == '__main__':
    raise SystemExit(main())
