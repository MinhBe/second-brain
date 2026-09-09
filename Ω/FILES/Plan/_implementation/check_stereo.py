"""Inspect stereo channel cancellation and prepare A/B listening clips, without choosing by loudness."""
from pathlib import Path
import subprocess
import sys
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'Skills/Domain/content-production/personal-content-workflow/audio-transcribe-local/scripts'))
from common import read_json, write_json, write_text, stamp

def main():
    output=ROOT/'Data/Transcripts'
    source=next(r for r in read_json(output/'_reports/inventory.json') if r['slug']=='recording-2')
    review=output/'_review'
    review.mkdir(exist_ok=True)
    rows=[]
    for start in [0,1800]:
        result=subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-ss',str(start),
            '-i',source['path'],'-t','30','-ar','16000','-ac','2','-f','f32le','pipe:1'],capture_output=True,check=True)
        samples=np.frombuffer(result.stdout,dtype='<f4').reshape(-1,2)
        rms=np.sqrt(np.mean(samples.astype('float64')**2,axis=0))
        mix=np.sqrt(np.mean(np.mean(samples.astype('float64'),axis=1)**2))
        corr=float(np.corrcoef(samples.T)[0,1]) if min(rms)>0 else None
        rows.append({'start_s':start,'duration_s':len(samples)/16000,'rms_left':float(rms[0]),
            'rms_right':float(rms[1]),'rms_mix':float(mix),'channel_correlation':corr})
        for channel in [0,1]:
            clip=review/f'recording-2_{start:04}_channel{channel}.wav'
            if not clip.exists():
                subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-n','-ss',str(start),
                    '-i',source['path'],'-t','30','-af',f'pan=mono|c0=c{channel}','-ar','16000',
                    '-c:a','pcm_s16le',str(clip)],check=True)
    write_json(review/'stereo.json',{'source_sha256':source['sha256'],'measurements':rows,'listening':'pending'})
    lines=['# Recording (2) — kiểm tra hai kênh', '',
        'Đây là đo tín hiệu và chuẩn bị mẫu nghe, chưa đánh giá độ rõ bằng tai. Tương quan/RMS không cho biết ai nói hoặc kênh nào hiểu được lời tốt hơn.', '',
        '| Khoảng nguồn | RMS trái | RMS phải | RMS trộn | Tương quan | Mẫu |', '|---|---:|---:|---:|---:|---|']
    for r in rows:
        start=r['start_s']
        lines.append(f"| {stamp(start)}–{stamp(start+30)} | {r['rms_left']:.5f} | {r['rms_right']:.5f} | {r['rms_mix']:.5f} | {r['channel_correlation']:.5f} | [Trái](recording-2_{start:04}_channel0.wav) / [Phải](recording-2_{start:04}_channel1.wav) |")
    lines += ['', 'Lô hiện tại dùng trộn mono cả hai kênh. Nếu nghe thấy một kênh rõ hơn hoặc hai kênh là hai luồng lời riêng, cần tạo biến thể kênh và so sánh trước khi đổi transcript.', '']
    write_text(review/'STEREO_REVIEW.md','\n'.join(lines))
    print(rows)

if __name__=='__main__': main()
