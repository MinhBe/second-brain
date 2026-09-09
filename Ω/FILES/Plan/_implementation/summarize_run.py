"""Report measured batch progress, acoustic flags and editorial coverage separately."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'Skills/Domain/content-production/personal-content-workflow/audio-transcribe-local/scripts'))
from common import read_json, write_json, write_text, stamp, now

def main():
    output=ROOT/'Data/Transcripts'
    inventory=read_json(output/'_reports/inventory.json',[])
    checkpoint=read_json(output/'_reports/checkpoint.json',{}).get('files',{})
    rows=[]
    for source in inventory:
        if source['duplicate_of']: continue
        work=output/'_work'/source['slug']
        raw=read_json(work/'raw.json')
        quality=read_json(work/'quality.json',{})
        editorial=read_json(work/'editorial.json',{})
        knowledge=read_json(work/'knowledge.json',{})
        rows.append({'slug':source['slug'],'source':source['file'],'duration_s':source['duration_s'],
            'status':checkpoint.get(source['slug'],{}).get('status','pending'),
            'model':raw['config']['model'] if raw else None, 'device':raw['config']['device'] if raw else None,
            'processing_s':raw['processing_s'] if raw else 0,'segments':len(raw['segments']) if raw else 0,
            'acoustic_flags':quality.get('flagged',0),'editorial_flags':len(editorial.get('unclear_segments',[])),
            'reviewed_segments':len(editorial.get('reviewed_segment_ids',[])),
            'claims':len(knowledge.get('claims',[])),'nodes':len(knowledge.get('nodes',[])),
            'listening':'pending'})
    total_segments=sum(r['segments'] for r in rows)
    report={'created':now(),'sources':len(inventory),'unique_sources':len(rows),
        'completed':sum(r['status']=='asr_complete' for r in rows),
        'source_hours':sum(r['duration_s'] for r in rows)/3600,
        'processing_minutes':sum(r['processing_s'] for r in rows)/60,
        'segments':total_segments,'acoustic_flags':sum(r['acoustic_flags'] for r in rows),
        'editorial_flags':sum(r['editorial_flags'] for r in rows),'claims':sum(r['claims'] for r in rows),
        'nodes':sum(r['nodes'] for r in rows),'rows':rows}
    report['acoustic_flag_pct']=round(100*report['acoustic_flags']/max(1,total_segments),2)
    write_json(output/'_reports/summary.json',report)
    lines=['# Báo cáo xử lý ghi âm', '', f"Cập nhật UTC: {report['created']}", '',
        f"{report['completed']}/{len(rows)} nguồn khác nhau hoàn tất ASR; {total_segments} segment, {report['claims']} claim và {report['nodes']} node đã biên tập.",
        f"Thời lượng nguồn khác nhau: {report['source_hours']:.2f} giờ. Tổng processing ghi trong raw: {report['processing_minutes']:.1f} phút (gồm tải model; không gồm thời gian biên tập).", '',
        f"{report['acoustic_flags']}/{total_segments} segment ({report['acoustic_flag_pct']}%) bị cờ âm học. {report['editorial_flags']} segment được đánh dấu nghi lỗi khi rà văn bản. Hai tập có thể trùng nhau; không cộng thành tỷ lệ lỗi.",
        'Không có bản chuẩn để tính WER. Ít cờ ASR không bảo đảm từ ngữ hay kiến thức đúng. Tất cả chờ nghe duyệt.', '',
        '| Nguồn | Trạng thái | Segment | Cờ âm học | Cờ biên tập | Đã rà | Claim/node |', '|---|---|---:|---:|---:|---:|---:|']
    for r in rows:
        lines.append(f"| [{r['source']}](../{r['slug']}_TRANSCRIPT.md) | {r['status']} | {r['segments']} | {r['acoustic_flags']} | {r['editorial_flags']} | {r['reviewed_segments']} | {r['claims']}/{r['nodes']} |")
    lines += ['', '[Nghe đối chiếu](../_review/LISTENING_REVIEW.md) · [Mục lục](../INDEX.md) · [Run log](run_log.csv)', '',
        'Bản Voice 010 (2) trùng byte được giữ nguyên ở Recording và không xử lý lại. Voice 015/016 hiện không đủ căn cứ rút tri thức; vẫn có transcript và ghi chú giới hạn.', '']
    lines += ['Voice 017 và Recording (2) có nội dung tương ứng dù khác hash; tổng giờ file không phải tổng nội dung độc nhất. [Xem đối chiếu](../CROSS_SOURCE_REVIEW.md).', '']
    write_text(output/'_reports/SUMMARY.md','\n'.join(lines))
    print({k:v for k,v in report.items() if k!='rows'})

if __name__=='__main__': main()
