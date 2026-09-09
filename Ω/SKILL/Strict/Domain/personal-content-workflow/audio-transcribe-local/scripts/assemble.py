"""Validate editorial coverage and claim provenance, then publish reviewable Markdown."""
from __future__ import annotations
import argparse
from datetime import date, timedelta
from pathlib import Path
from common import DEFAULT_OUTPUT, digest, fingerprint, read_json, stamp, validate_segments, write_json, write_text
from quality_report import flags

def validate_editorial(raw, editorial, knowledge):
    ids = validate_segments(raw)
    if editorial.get('raw_content_hash') != fingerprint(raw['segments']):
        raise ValueError('editorial source changed')
    if set(editorial.get('reviewed_segment_ids', [])) != ids:
        raise ValueError('editorial coverage incomplete')
    overrides = editorial.get('corrections', {})
    if not set(overrides) <= ids or any(not isinstance(v, str) or not v.strip() for v in overrides.values()):
        raise ValueError('invalid correction')
    if not set(editorial.get('unclear_segments', [])) <= ids:
        raise ValueError('unknown unclear segment')
    for chapter in editorial.get('chapters', []):
        if chapter['start_id'] not in ids or not chapter['title'].strip():
            raise ValueError('invalid chapter')
    by_id = {s['id']: s for s in raw['segments']}
    claim_ids = set()
    for claim in knowledge.get('claims', []):
        if claim['id'] in claim_ids or not claim['text'].strip():
            raise ValueError('duplicate or empty claim')
        claim_ids.add(claim['id'])
        if claim.get('confidence') not in ['thấp', 'vừa', 'cao'] or not claim.get('confidence_reason'):
            raise ValueError('claim confidence needs level and reason')
        if not claim.get('evidence'):
            raise ValueError('claim requires evidence')
        for evidence in claim['evidence']:
            segment = by_id.get(evidence['segment_id'])
            if not segment or not evidence['quote'].strip() or evidence['quote'] not in segment['text']:
                raise ValueError('claim evidence does not match source')
        if claim.get('verification', 'chưa kiểm chứng') != 'chưa kiểm chứng' and not claim.get('verification_source'):
            raise ValueError('verified claim requires an external source')
    node_ids = set()
    for node in knowledge.get('nodes', []):
        if node['id'] in node_ids:
            raise ValueError('duplicate node')
        node_ids.add(node['id'])
        if not node.get('claim_ids') or not set(node['claim_ids']) <= claim_ids:
            raise ValueError('node requires valid claims')
    return by_id

def assemble(directory, output):
    directory, output = Path(directory), Path(output)
    raw = read_json(directory/'raw.json')
    editorial = read_json(directory/'editorial.json')
    knowledge = read_json(directory/'knowledge.json')
    if not all(x is not None for x in [raw, editorial, knowledge]):
        raise ValueError('raw.json, editorial.json and knowledge.json are required')
    by_id = validate_editorial(raw, editorial, knowledge)
    slug = directory.name
    title = editorial['title']
    chapters = {c['start_id']: c['title'] for c in editorial.get('chapters', [])}
    lines = [f'# {title}', '', f"Nguồn: [{Path(raw['source']).name}]({Path(raw['source']).as_uri()})", '',
        f"Thời lượng: {stamp(raw['duration_s'])}. ASR: {raw['config']['model']} / {raw['config']['device']}.",
        '', 'Trạng thái: đã rà văn bản; chờ nghe đối chiếu. Người nói chưa được xác định nếu không có ghi chú riêng.',
        'Bản này bảo toàn thứ tự và nội dung nhận dạng; các đoạn nghi lỗi được giữ dấu vết để nghe lại.', '']
    for segment in raw['segments']:
        sid = segment['id']
        if sid in chapters:
            lines += [f'## {chapters[sid]}', '']
        text = editorial.get('corrections', {}).get(sid, segment['text']).strip()
        uncertain = sid in editorial.get('unclear_segments', [])
        marker = f"[nghe không rõ {stamp(segment['start'])}; cần đối chiếu] " if uncertain else ('[ASR cần nghe lại] ' if flags(segment) else '')
        lines += [f'<a id="{sid}"></a>', f"**[{stamp(segment['start'])} → {stamp(segment['end'])}] [Người nói?]** {marker}{text}", '']
    if not raw['segments']:
        lines += ['Không có lời nói nhận dạng sử dụng được; cần nghe nguồn để xác định nguyên nhân.', '']
    transcript = '\n'.join(lines)
    write_text(directory/'clean.md', transcript)
    write_text(output/f'{slug}_TRANSCRIPT.md', transcript)
    created = knowledge.get('created', date.today().isoformat())
    dates = [date.fromisoformat(created)+timedelta(days=d) for d in [1,4,12,30]]
    lines = [f'# Tri thức — {title}', '', '## Raw Inbox', '',
        f'[Transcript đầy đủ]({slug}_TRANSCRIPT.md) · [Báo cáo chất lượng](_work/{slug}/quality_report.md)', '',
        'Nguồn là hội thoại được ASR nhận dạng và chưa nghe duyệt. Confidence dưới đây phản ánh mức chắc chắn của diễn giải từ văn bản, không chứng minh lời nói đúng về mặt thực tế.', '', '## Knowledge Nodes', '']
    for node in knowledge.get('nodes', []):
        lines += [f'<a id="{node["id"]}"></a>', f"### {node['id']} — {node['title']}", '', f"- **Câu hỏi tổng hợp:** {node['question']}",
            f"- **Cốt lõi:** {node['answer']}", f"- **Ví dụ/ngữ cảnh:** {node['context']}",
            f"- **Điều kiện áp dụng:** {node['conditions']}", f"- **Liên kết:** {', '.join(node['claim_ids'])}; {node.get('connections', 'Xem Schema Map')}", '']
    if not knowledge.get('nodes'):
        lines += ['Chưa đủ lời nói rõ để rút tri thức đáng tin cậy.', '']
    lines += ['## Claim Ledger', '', '| ID | Nội dung được diễn giải | Bằng chứng | Confidence | Kiểm chứng |', '|---|---|---|---|---|']
    esc = lambda text: str(text).replace('|', '\\|').replace('\n', ' ')
    for claim in knowledge.get('claims', []):
        citations = '; '.join(f"[{stamp(by_id[e['segment_id']]['start'])}]({slug}_TRANSCRIPT.md#{e['segment_id']}): «{esc(e['quote'])}»" for e in claim['evidence'])
        lines.append(f"| {claim['id']} | {esc(claim['text'])} (người nói chưa xác định) | {citations} | {claim['confidence']}: {esc(claim['confidence_reason'])} | {esc(claim.get('verification', 'chưa kiểm chứng'))} |")
    lines += ['', '## Câu hỏi mở và giới hạn', '']
    lines += ['- '+s for s in knowledge.get('open_questions', [])]
    lines += ['', '## Practice Log — đề xuất của trợ lý', '']
    lines += ['- [ ] '+s for s in knowledge.get('practice', [])]
    lines += ['', '## Lịch ôn đề xuất', '', ', '.join(str(d) for d in dates), '']
    text = '\n'.join(lines)
    work_text = text.replace(f']({slug}_', f'](../../{slug}_').replace('](_work/', '](../../_work/')
    write_text(directory/'knowledge.md', work_text)
    write_text(output/f'{slug}_KNOWLEDGE.md', text)
    write_json(directory/'assembly.json', {'raw_content_hash': fingerprint(raw['segments']),
        'editorial_sha256': digest(directory/'editorial.json'), 'knowledge_sha256': digest(directory/'knowledge.json'),
        'status': 'editorially_reviewed', 'listening_status': 'pending', 'segments': len(raw['segments']),
        'claims': len(knowledge.get('claims', []))})

def index(output):
    output = Path(output)
    inventory = read_json(output/'_reports/inventory.json', [])
    lines = ['# Ghi âm — transcript và tri thức', '',
        'ASR local, biên tập văn bản và tri thức trong phiên trợ lý. Chưa có bản nào được người dùng nghe duyệt.', '',
        '| Nguồn | Thời lượng | Trạng thái | Confidence diễn giải | Kết quả |', '|---|---|---|---|---|']
    nodes = []
    for row in inventory:
        slug = row['slug']
        d = output/'_work'/slug
        meta = read_json(d/'assembly.json')
        raw = read_json(d/'raw.json')
        confidence = 'chưa đánh giá'
        if row['duplicate_of']:
            result = f"Trùng [{row['duplicate_of']}]({row['duplicate_of']}_TRANSCRIPT.md)"
            status = 'bản trùng, giữ nguyên nguồn'
        elif meta:
            result = f'[Transcript]({slug}_TRANSCRIPT.md) · [Tri thức]({slug}_KNOWLEDGE.md)'
            status = 'đã rà văn bản; chờ nghe duyệt'
            claims = read_json(d/'knowledge.json', {}).get('claims', [])
            confidence = min((c['confidence'] for c in claims), key=['thấp','vừa','cao'].index) if claims else 'chưa đủ nguồn'
            if not claims:
                status = 'chưa đủ căn cứ rút tri thức; chờ nghe duyệt'
        elif raw:
            result = f'[ASR](_work/{slug}/raw.txt) · [Chất lượng](_work/{slug}/quality_report.md)'
            status = 'chờ biên tập'
        else:
            result, status = '', row.get('error') or 'chờ ASR'
        lines.append(f"| {row['file']} | {stamp(row['duration_s'] or 0)} | {status} | {confidence} | {result} |")
        if meta:
            knowledge = read_json(d/'knowledge.json', {})
            nodes += [(slug, node) for node in knowledge.get('nodes', [])]
    lines += ['', '[Schema Map](SCHEMA_MAP.md)', '', 'Confidence từng claim nằm trong Claim Ledger; không dùng điểm ASR làm độ đúng của tri thức.', '']
    for relative, title in [('_reports/SUMMARY.md','Báo cáo xử lý'),('_review/LISTENING_REVIEW.md','Mẫu nghe và phiếu duyệt')]:
        if (output/relative).exists():
            lines += [f'[{title}]({relative})', '']
    write_text(output/'INDEX.md', '\n'.join(lines))
    topics = {}
    for slug, node in nodes:
        for tag in node.get('tags', ['chưa phân loại']):
            topics.setdefault(tag, []).append((slug, node))
    lines = ['# Schema Map', '', 'Liên kết chủ đề dưới đây do trợ lý tổng hợp; cùng chủ đề không có nghĩa các lời nói kiểm chứng lẫn nhau.', '']
    if (output/'CROSS_SOURCE_REVIEW.md').exists():
        lines += ['[Đối chiếu và những điểm chưa giải quyết](CROSS_SOURCE_REVIEW.md)', '']
    for tag, matches in sorted(topics.items()):
        lines += ['## '+tag, '']
        lines += [f"- [{node['id']} — {node['title']}]({slug}_KNOWLEDGE.md#{node['id']}) ({slug})" for slug, node in matches]
        lines.append('')
    write_text(output/'SCHEMA_MAP.md', '\n'.join(lines))

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--dir', type=Path)
    p.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    p.add_argument('--all', action='store_true')
    args = p.parse_args()
    if args.all:
        for d in sorted((args.output/'_work').iterdir()):
            if (d/'editorial.json').exists() and (d/'knowledge.json').exists():
                assemble(d, args.output)
    elif args.dir:
        assemble(args.dir, args.output)
    index(args.output)
