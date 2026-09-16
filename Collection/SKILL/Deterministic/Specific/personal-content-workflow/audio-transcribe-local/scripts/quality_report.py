"""Acoustic triage signals are not word error rate or factual confidence."""
import argparse
from collections import Counter
from pathlib import Path
import re
from common import read_json, stamp, write_json, write_text

def flags(segment):
    result = []
    if segment.get('avg_logprob', 0) < -1:
        result.append('low_logprob')
    if segment.get('no_speech_prob', 0) > .6:
        result.append('no_speech')
    if segment.get('compression_ratio', 0) > 2.4:
        result.append('compression')
    tokens = re.findall(r'\w+', segment['text'].casefold())
    ngrams = Counter(tuple(tokens[i:i+4]) for i in range(len(tokens)-3))
    if ngrams and max(ngrams.values()) >= 3:
        result.append('repetition')
    return result

def analyze(raw):
    rows = [{**s, 'flags': flags(s)} for s in raw['segments']]
    minutes = {}
    for s in rows:
        key = int(s['start'] // 60)
        bucket = minutes.setdefault(key, {'segments': 0, 'flagged': 0})
        bucket['segments'] += 1
        bucket['flagged'] += bool(s['flags'])
    flagged = [s for s in rows if s['flags']]
    gaps, cursor = [], 0
    for s in rows:
        if s['start'] - cursor >= 30:
            gaps.append({'start': cursor, 'end': s['start']})
        cursor = max(cursor, s['end'])
    if raw['duration_s'] - cursor >= 30:
        gaps.append({'start': cursor, 'end': raw['duration_s']})
    return {'segments': len(rows), 'flagged': len(flagged), 'flagged_pct': round(100 * len(flagged) / max(1, len(rows)), 2),
        'minutes': minutes, 'review_segments': sorted(flagged, key=lambda s: s.get('avg_logprob', 0)),
        'untranscribed_gaps': gaps, 'status': 'needs_listening' if rows else 'no_usable_speech'}

def report(raw, directory):
    q = analyze(raw)
    directory = Path(directory)
    write_json(directory / 'quality.json', q)
    lines = ['# Kiểm tra chất lượng', '', f"{q['segments']} đoạn; {q['flagged_pct']}% có tín hiệu cần kiểm tra.",
        '', 'Các chỉ số dưới đây chỉ để chọn đoạn nghe lại; không phải WER hoặc bằng chứng nội dung đúng.',
        'Khoảng chưa có transcript có thể là im lặng hoặc lời nói bị bỏ sót. Chưa được nghe duyệt.', '',
        '| Phút | Số đoạn | Cần kiểm tra |', '|---|---:|---:|']
    for minute, stats in q['minutes'].items():
        lines.append(f"| {stamp(int(minute)*60)} | {stats['segments']} | {stats['flagged']} |")
    lines += ['', '## Tối đa 20 đoạn ưu tiên nghe lại', '']
    for s in q['review_segments'][:20]:
        lines.append(f"- {s['id']} [{stamp(s['start'])}–{stamp(s['end'])}] {', '.join(s['flags'])}: {s['text']}")
    lines += ['', '## Khoảng chưa có transcript ≥30 giây', '']
    lines += [f"- {stamp(g['start'])}–{stamp(g['end'])}" for g in q['untranscribed_gaps']]
    write_text(directory / 'quality_report.md', '\n'.join(lines) + '\n')
    return q

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('raw', type=Path)
    args = parser.parse_args()
    report(read_json(args.raw), args.raw.parent)
