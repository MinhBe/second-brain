"""Create reproducible listening samples; human acceptance always stays pending."""
from pathlib import Path
import random
import subprocess
import sys
import wave
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT/'Skills/Domain/content-production/personal-content-workflow/audio-transcribe-local/scripts'))
from common import read_json, write_json, write_text, digest, stamp

def main():
    output = ROOT/'Data/Transcripts'
    review = output/'_review'
    review.mkdir(parents=True, exist_ok=True)
    rows = {r['slug']:r for r in read_json(output/'_reports/inventory.json')}
    rng = random.Random(20260908)
    samples = []
    for group, slug in [('ngắn','record-thay-lam-2'),('vừa','voice-012'),('dài','voice-017'),('ưu tiên nhiễu','voice-016')]:
        row = rows[slug]
        length = 120 if slug != 'voice-016' else row['duration_s']
        start = rng.randrange(max(1, int(row['duration_s']-length))) if slug != 'voice-016' else 0
        name = f'{slug}_{start:04}.wav'
        clip = review/name
        if not clip.exists():
            subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-n','-ss',str(start),
                '-i',row['path'],'-t',str(length),'-ar','16000','-ac','1','-c:a','pcm_s16le',str(clip)],check=True)
        with wave.open(str(clip),'rb') as audio:
            measured = audio.getnframes()/audio.getframerate()
        if abs(measured-length) > .1: raise ValueError('Unexpected sample duration: '+name)
        raw = read_json(output/'_work'/slug/'raw.json',{})
        segments = [s['id'] for s in raw.get('segments',[]) if s['end'] > start and s['start'] < start+length]
        samples.append({'group':group,'slug':slug,'source':row['path'],'source_sha256':row['sha256'],
            'start_s':start,'duration_s':measured,'file':name,'clip_sha256':digest(clip),
            'segment_ids':segments,'listening_status':'pending'})
    write_json(review/'samples.json',samples)
    lines = ['# Nghe đối chiếu — chờ người dùng duyệt', '',
        'Ba mẫu 2 phút được chọn bằng seed 20260908 ở nguồn ngắn/vừa/dài. Voice 016 được thêm toàn bộ vì ASR quá ít và nghi nhận dạng nhầm tiếng ồn.',
        'Chưa có mẫu nào được xác nhận đã nghe. Mẫu giữ âm thanh nguồn, chỉ đổi sang WAV 16 kHz mono; không khử nhiễu.', '',
        '| Nhóm | Mẫu nghe | Thời gian trong nguồn | Transcript | Trạng thái |', '|---|---|---|---|---|']
    for s in samples:
        anchor = '#'+s['segment_ids'][0] if s['segment_ids'] else ''
        lines.append(f"| {s['group']} | [{s['slug']}]({s['file']}) | {stamp(s['start_s'])}–{stamp(s['start_s']+s['duration_s'])} | [Đối chiếu](../{s['slug']}_TRANSCRIPT.md{anchor}) | chờ nghe |")
    lines += ['', 'Sau khi nghe, ghi lỗi đổi nghĩa, phủ định, thuật ngữ, con số và người nói; đánh dấu đạt/cần sửa cho từng mẫu.',
        'Một mẫu đạt không xác nhận toàn bộ file. Các đoạn nghi lỗi khác vẫn nằm trong quality_report.md và transcript.', '',
        '## Phiếu duyệt', '', '| Mẫu | Người duyệt/ngày | Đạt hoặc cần sửa | Timestamp và nội dung cần sửa |', '|---|---|---|---|']
    lines += [f"| {s['slug']} | | chờ nghe | |" for s in samples]
    if (review/'STEREO_REVIEW.md').exists():
        lines += ['', '[So sánh hai kênh Recording (2)](STEREO_REVIEW.md)', '']
    write_text(review/'LISTENING_REVIEW.md','\n'.join(lines)+'\n')
    print('Prepared',len(samples),'samples; listening remains pending')

if __name__ == '__main__': main()
