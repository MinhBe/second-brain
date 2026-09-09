"""Task-specific, backed-up maintenance and reproducible inventory for Collection."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
CONTENT = Path('Skills/Domain/content-production/personal-content-workflow')
KEEP = {'personal-content-workflow', 'personal-session-workflow', 'personal-action-workflow', 'ChangePdfToText'}
SKIP = {'.git', '.venv', 'venv', '.npm-cache', 'node_modules', '__pycache__', 'cassettes', 'models'}

def sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def save(path, body):
    p = ROOT / path
    if p.exists():
        backup = HERE/'before'/path
        if not backup.exists():
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, backup)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding='utf-8')

def replace(path, old, new):
    p = ROOT / path
    text = p.read_text(encoding='utf-8-sig')
    if old not in text:
        if new in text:
            return
        raise ValueError(f'expected text missing: {path}: {old[:80]}')
    save(path, text.replace(old, new))

def docs():
    save(CONTENT/'learn-this/SKILL.md', '''---
name: learn-this
description: Điều phối học từ sách, URL hoặc file ghi âm local để tạo tri thức và hành động. Dùng khi người dùng yêu cầu learn-this, học và áp dụng, trích nội dung rồi lập kế hoạch.
---

# Learn this

Xác định nguồn trước khi chọn workflow; dùng PowerShell/Python trên Windows.
Đọc skill đích theo liên kết, không sao chép lại các script của nó vào đây.

| Nguồn | Workflow |
|---|---|
| File audio hoặc thư mục chứa audio local | [audio-transcribe-local](../audio-transcribe-local/SKILL.md) |
| Tên sách hoặc văn bản sách | [book-insight](../book-insight/SKILL.md) |
| YouTube URL/video ID | [youtube-transcript-pro](../youtube-transcript-pro/SKILL.md) |
| Bài viết HTTP(S) | [article-extractor](../article-extractor/SKILL.md) |
| PDF local hoặc URL PDF | [ChangePdfToText](../../../personal/ChangePdfToText/SKILL.md) |

Ưu tiên kiểm tra đường dẫn local tồn tại trước khi suy đoán đó là tên sách/URL.
Nếu nguồn không có thật hoặc chưa xác định được loại nội dung, hỏi đúng thông tin còn thiếu.
Với URL PDF, tải vào thư mục làm việc của lần xử lý, giữ nguồn và gọi converter bằng
`--input`/`--output` tường minh. Không chạy converter mặc định cả thư viện khi chỉ nhận một PDF.

Audio trả transcript, PKM và lịch ôn; sách trả Book Insight với ứng dụng sẵn có.
Các nhánh bài viết/YouTube/PDF sau trích xuất dùng [ship-learn-next](../ship-learn-next/SKILL.md)
khi yêu cầu gồm học và áp dụng. Không tạo thêm kế hoạch trùng với đầu ra audio/sách.
Chỉ lập hành động từ nội dung đã lấy được; báo rõ nguồn rỗng, lỗi mạng hoặc thiếu phụ thuộc.

Không tự cài công cụ bằng brew/apt, không dùng script bash tương tác trong PowerShell.
Kiểm tra phụ thuộc theo skill đích; đưa kết quả cùng đường dẫn và trạng thái kiểm tra thật.
''')
    save(CONTENT/'youtube-transcript-pro/SKILL.md', '''---
name: youtube-transcript-pro
description: Lấy phụ đề YouTube theo ngôn ngữ, chuyển thành văn bản và tùy chọn nhận dạng audio khi không có phụ đề. Dùng cho URL/video ID hoặc báo cáo video đã chọn của workflow kênh.
---

# YouTube Transcript Pro

Chạy Python từ thư mục skill hoặc dùng đường dẫn tuyệt đối tới script. Giữ ngôn ngữ gốc
được yêu cầu; phân biệt phụ đề thủ công, tự động và ASR. Không gọi dịch máy là lời gốc.

## Một video

```powershell
python -X utf8 scripts/fetch.py "YOUTUBE_URL" --lang vi --clean --output-dir "OUTPUT_DIR"
```

`fetch.py` nhận URL hoặc ID 11 ký tự, `--lang/-l`, `--auto/-a`, `--clean/-c`, `--output-dir`.
Ưu tiên phụ đề thủ công, sau đó tự động của cùng ngôn ngữ; `--auto` chỉ lấy tự động.
Khi không chỉ định ngôn ngữ, ưu tiên vi rồi en, sau đó ngôn ngữ có sẵn.
VTT từng video được chọn theo ID và thông tin tải, không lấy một VTT bất kỳ ở cwd.
Cleaner chỉ khử phần lặp cuộn ở các cue kế tiếp chồng thời gian; giữ câu lặp ở chỗ khác.

## Kênh / danh sách video

`python -X utf8 scripts/channel_to_markdown.py --help` mô tả các bộ lọc và tham số thật.
Chỉ truyền `--channel-url` của nguồn người dùng yêu cầu; script cũ có giá trị mặc định
là kênh Bao Brian, không dùng mặc định đó để suy rộng yêu cầu một video.
Workflow sinh `_reports/selected_videos.csv` và các mục Speaking/Writing theo bộ lọc.

## Audio fallback

```powershell
python -X utf8 scripts/audio_fallback_to_markdown.py --output-root "OUTPUT_DIR" --model large-v3 --language vi
```

Đọc báo cáo selected_videos hiện có; nhận `--selected-report`, `--max-videos`, `--force`,
`--no-gpu`. Tải media theo video đã chọn rồi gọi [audio-transcribe-local](../../audio-transcribe-local/SKILL.md)
thông qua script Python; giữ cấu trúc Markdown và báo cáo của workflow kênh.
`--model` hiện là tên model faster-whisper đã cache (mặc định large-v3), không nhận ggml .bin.
Nếu thiếu model, báo rõ cần chuẩn bị cache; không sửa torch hoặc dùng ffmpeg whisper filter.

Lỗi riêng tư/xóa/rate limit phải được báo đúng; không biến lỗi tải thành "không có phụ đề".
Chỉ tóm tắt khi người dùng yêu cầu; mọi câu trích hoặc kết luận cần truy về transcript.
'''.replace('../../audio-transcribe-local/', '../audio-transcribe-local/'))
    replace(CONTENT/'youtube-transcript-basic/SKILL.md', 'name: youtube-transcript\n', 'name: youtube-transcript-basic\n')
    pdf = Path('Skills/Domain/personal/ChangePdfToText')
    replace(pdf/'pdf_to_text.py', 'Path(r"C:\\Users\\Admin\\Documents\\Language")', "Path(__file__).resolve().parents[4] / 'Data' / 'Language'")
    path = pdf/'SKILL.md'
    replace(path, r'C:\Users\Admin\Documents\Collection\Skills\ChangePdfToText', r'C:\Users\Admin\Documents\Collection\Skills\Domain\personal\ChangePdfToText')
    replace(path, r'C:\Users\Admin\Documents\Language', r'C:\Users\Admin\Documents\Collection\Data\Language')
    replace(Path('Data/Language/_tools/language_library_organizer.py'), 'Path(r"C:\\Users\\Admin\\Documents\\Language")', 'Path(__file__).resolve().parents[1]')
    replace(Path('Data/Language/_catalog/SCAN_WORKFLOW.md'), r'C:\Users\Admin\Documents\Language', r'C:\Users\Admin\Documents\Collection\Data\Language')
    save(Path('Skills/Domain/personal/transcript-workspace-assets/RECOVERY_PLAN.md'), '''# Trạng thái phục hồi workflow YouTube

Tài liệu kế hoạch cũ được lưu trong Data/Plan/_implementation/before trước khi sửa.
Workflow đang được duy trì tại `Skills/Domain/content-production/personal-content-workflow`.

- youtube-transcript-pro/scripts/fetch.py: một URL/ID, lựa chọn ngôn ngữ và làm sạch phụ đề.
- youtube-transcript-pro/scripts/channel_to_markdown.py: lựa chọn video trong kênh, báo cáo và Markdown.
- youtube-transcript-pro/scripts/audio_fallback_to_markdown.py: ASR media qua audio-transcribe-local.
- audio-transcribe-local/scripts/transcribe.py: faster-whisper, CUDA DLL discovery, resume.

Không còn dùng các đường dẫn C:\\Projects cũ hoặc tên script dự kiến fetch_transcript.py,
clean_transcript.py, generate_summary.py để chạy workflow. Các file workspace tại đây là
tài liệu lịch sử, không phải skill được kích hoạt và không được coi là bản triển khai hiện hành.
Xem `Skills/README.md` từ gốc Collection để tra vị trí và bằng chứng kiểm tra mới nhất.
''')
    save(Path('.ignore'), '# Operational search; use rg --no-ignore Reference explicitly for upstream research.\nReference/\nData/Plan/_implementation/before/\n**/.git/\n**/.venv/\n**/venv/\n**/.npm-cache/\n**/node_modules/\n**/__pycache__/\n**/models/\n**/cassettes/\n*.bin\n*.mp4\n*.m4a\n*.wav\n')
    save(Path('.gitignore'), '# Collection has no root git repository; defaults if initialized later.\n**/.venv/\n**/venv/\n**/.npm-cache/\n**/node_modules/\n**/__pycache__/\n**/models/\n**/cassettes/\n*.bin\n*.mp4\nData/Transcripts/_work/*/audio_16k.wav\nData/Transcripts/_calibration/\n')

def files(root, skip=False):
    for directory, dirs, names in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if (not skip or d not in SKIP) and not (Path(directory, d).lstat().st_file_attributes & 0x400))
        for name in sorted(names):
            p = Path(directory, name)
            if not (p.lstat().st_file_attributes & 0x400):
                yield p

def prepare_moves():
    manifest_path = HERE/'moves.json'
    if manifest_path.exists():
        raise SystemExit('moves.json already exists; use existing manifest, do not replace baseline')
    moves = []
    for domain in sorted((ROOT/'Skills/Domain').iterdir()):
        if not domain.is_dir():
            continue
        for package in sorted(domain.iterdir()):
            if not package.is_dir() or package.name in KEEP:
                continue
            src = package.relative_to(ROOT)
            dest = Path('Reference/Domain') / domain.name / package.name
            entries = [{'path': str(p.relative_to(package)), 'bytes': p.stat().st_size, 'sha256': sha(p)} for p in files(package)]
            moves.append({'source': str(src), 'destination': str(dest), 'files': entries})
            print(f'INVENTORIED {src}: {len(entries)} files', flush=True)
    catalog = ROOT/'Data/Language/_catalog'
    keep = {'SCAN_WORKFLOW.md', 'inventory_20260908_193532.csv', 'move_plan_20260908_193510.csv', 'move_plan_20260908_193510.json',
        'conflicts_20260908_193510.csv', 'pre_move_inventory_20260908_193516.csv', 'post_move_inventory_20260908_193516.csv'}
    for p in sorted(catalog.iterdir()):
        if p.is_file() and p.name not in keep:
            moves.append({'source': str(p.relative_to(ROOT)), 'destination': str(Path('Data/Language/_catalog/_archive/20260908')/p.name),
                'files': [{'path': '.', 'bytes': p.stat().st_size, 'sha256': sha(p)}]})
    manifest_path.write_text(json.dumps({'root': str(ROOT), 'moves': moves}, ensure_ascii=False, indent=2), encoding='utf-8')

def verify_moves():
    data = json.loads((HERE/'moves.json').read_text(encoding='utf-8'))
    errors = []
    for move in data['moves']:
        base = ROOT/move['destination']
        if (ROOT/move['source']).exists():
            errors.append('source remains: '+move['source'])
        for entry in move['files']:
            p = base if entry['path']=='.' else base/entry['path']
            if not p.is_file() or p.stat().st_size!=entry['bytes'] or sha(p)!=entry['sha256']:
                errors.append(str(p))
    result = {'checked_moves': len(data['moves']), 'checked_files': sum(len(m['files']) for m in data['moves']), 'errors': errors}
    (HERE/'move_verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False))
    return bool(errors)

def skill_index():
    import yaml
    records = []
    for base in ['Skills/Domain', 'Reference/Domain']:
        for path in files(ROOT/base, skip=True):
            if path.name != 'SKILL.md':
                continue
            text = path.read_text(encoding='utf-8-sig', errors='replace')
            frontmatter_error = ''
            try:
                meta = yaml.safe_load(text.split('---', 2)[1]) if text.startswith('---') else {}
                meta = meta if isinstance(meta, dict) else {}
            except Exception as exc:
                meta = {}
                frontmatter_error = str(exc)[:400]
            stripped = text.strip()
            pointer = stripped if len(stripped.splitlines()) == 1 and stripped.startswith('../') and stripped.endswith('.md') else None
            records.append({'name': meta.get('name', path.parent.name), 'description': str(meta.get('description', '')).replace('\n',' '),
                'path': str(path.relative_to(ROOT)), 'status': 'reference, not runtime-tested' if base.startswith('Reference') else 'local, see validation log',
                'frontmatter_valid': bool(meta.get('name') and meta.get('description')),
                'frontmatter_error': frontmatter_error, 'kind': 'text_pointer' if pointer else 'document',
                'pointer_target': pointer, 'pointer_target_exists': (path.parent/pointer).exists() if pointer else None,
                'frontmatter_checked_at': datetime.now(timezone.utc).isoformat()})
    (HERE/'skill_inventory.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
    active = [r for r in records if r['path'].startswith('Skills')]
    lines = ['# Skill đang duy trì và kho tham khảo', '',
        f"Kiểm kê {datetime.now().date()}: {len(active)} skill trong Skills; {len(records)-len(active)} file SKILL.md trong kho tham khảo. Số file gồm cả con trỏ văn bản và hướng dẫn, không phải số skill độc lập đã chạy được.", '',
        '| Skill | Mục đích | Vị trí | Trạng thái | Kiểm cuối |', '|---|---|---|---|---|']
    for r in active:
        link = '../'+r['path'].replace('\\','/')
        description = r['description'].replace('|','/').strip()
        description = {'article-extractor':'Trích nội dung bài viết từ URL',
            'audio-transcribe-local':'Ghi âm local → transcript và tri thức có dẫn chứng',
            'book-insight':'Phân tích sách từ văn bản, ghi chú và review',
            'learn-this':'Điều phối nguồn học đến skill phù hợp',
            'ship-learn-next':'Chuyển nội dung học thành kế hoạch áp dụng',
            'youtube-transcript-basic':'Lấy phụ đề một video YouTube',
            'youtube-transcript-pro':'Lấy phụ đề và fallback nhận dạng audio local',
            'session-log':'Ghi kết quả phiên vào nhật ký tuần',
            'change-pdf-to-text':'PDF → Markdown/TXT, OCR khi đủ phụ thuộc',
            'scrum-sage':'Hỗ trợ Scrum và cải tiến cách làm việc',
            'unblock-action':'Làm rõ việc đang mắc và bước tiếp theo'}.get(r['name'],description)
        status = {'book-insight':'27 test đạt; nguồn hiện có đã kiểm tra', 'audio-transcribe-local':'15 test đạt; 12 file ASR/PKM; chờ nghe duyệt',
            'learn-this':'điều phối Windows; link đã kiểm tra', 'youtube-transcript-pro':'fixture test; live/network chưa nghiệm thu',
            'change-pdf-to-text':'xem kiểm thử PDF; OCR phụ thuộc môi trường'}.get(r['name'],'chưa kiểm thử runtime')
        lines.append(f"| {r['name']} | {description} | [SKILL]({link}) | {status} | {datetime.now().date()} |")
    lines += ['', '## Kích hoạt', '', 'Junction tại .agents/skills và .claude/skills: book-insight, learn-this, audio-transcribe-local.', '',
        '## Kho tham khảo', '', '[Inventory đầy đủ](../Data/Plan/_implementation/skill_inventory.json) gồm đường dẫn, mô tả và trạng thái từng skill.',
        'Các repo upstream và tài liệu lưu ở Reference/Domain, giữ license, lịch sử và cấu trúc. Tìm có chủ đích bằng `rg --no-ignore Reference/Domain/<nhóm>`.', '',
        '[Manifest di chuyển](../Data/Plan/_implementation/moves.json) và [kiểm chứng hash](../Data/Plan/_implementation/move_verification.json).',
        'Khôi phục vị trí bằng Data/Plan/_implementation/reorganize.ps1 -Mode Rollback; không ghi đè đích đã có.', '']
    save(Path('Skills/README.md'), '\n'.join(lines))
    print(f'Indexed {len(records)} skills; {len(active)} maintained', flush=True)

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('action', choices=['docs', 'prepare-moves', 'verify-moves', 'index'])
    args = p.parse_args()
    result = {'docs': docs, 'prepare-moves': prepare_moves, 'verify-moves': verify_moves, 'index': skill_index}[args.action]()
    raise SystemExit(int(bool(result)))
