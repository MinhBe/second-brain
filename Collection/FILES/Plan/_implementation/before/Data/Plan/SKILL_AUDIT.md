# SKILL AUDIT — Đánh giá khắc nghiệt bộ skill trong `C:\Users\Admin\Documents\Collection`

> Ngày: 2026-09-08. Phạm vi: toàn bộ `Skills\Domain\` (26.600 file, 1.133 SKILL.md), `.claude\skills`, `.agents\skills`, `Data\`. Tiêu chí: **chạy được trên máy này hôm nay** > tài liệu khớp code > có test > có provenance. Không chấm điểm theo "trông có vẻ hay".

## 1. Phán quyết tổng

**Đây là kho sưu tầm, không phải hệ skill.**

| Chỉ số | Giá trị | Ý nghĩa |
|---|---|---|
| SKILL.md trong cây | 1.133 | |
| Skill được nối vào `.claude\skills` | **2** (`book-insight`, `learn-this`) | 0,18 % được dùng |
| Skill tự viết | 6 + 3 cá nhân | phần còn lại là repo người khác vendored |
| Skill tự viết chạy được trên Windows không sửa | **1** (`book-insight`) + 2 không cần code (`ship-learn-next`, `article-extractor` nửa chừng) | |
| Skill có test | 1 (`book-insight`) | |
| Skill xử lý được audio local | **0** | đúng thứ đang cần |

Ba lỗi cấu trúc:
1. **Không có tầng "kích hoạt".** 1.131 skill nằm im, không index, không README ở gốc `Skills\`. Không ai (kể cả Claude) tìm được thứ cần khi cần.
2. **Vendored nguyên repo kèm rác.** `.git`, `.venv`, `.npm-cache`, `__pycache__`, model 141 MB, mp4 11,5 MB, ~40 MB VCR cassette nằm trong cây skill. Hệ quả thực tế: ripgrep/find timeout khi quét `Skills\Domain\personal\`. Kho càng to càng vô dụng.
3. **Tài liệu lệch code ở chính skill tự viết.** Ít nhất 4 SKILL.md mô tả file không tồn tại hoặc đường dẫn đã chết.

## 2. Skill tự viết — `content-production\personal-content-workflow\`

### 2.1 `book-insight` — ĐẠT, là chuẩn mực nội bộ
- Có: 4 gate G0–G4, 8 script, 7 reference, `tests/test_pipeline.py`, `_upstream/` ghi provenance + license, output template, quality checklist, spaced review +1/+4/+12/+30.
- Đã sinh sản phẩm thật: `Data\BookReviews\amusing_INSIGHT.md`, `attached_INSIGHT.md`.
- Trừ: chỉ nhận YouTube; `extractions.rejected.jsonl` và `_lowconf.jsonl` đều 0 B ở cả hai lần chạy → **hoặc pipeline không bao giờ loại gì, hoặc gate validate không có tác dụng thật**. Cần kiểm tra lại. Chưa có bằng chứng test chạy xanh gần đây.
- Kết luận: nhân bản kiến trúc này cho skill audio mới.

### 2.2 `learn-this` — KHÔNG CHẠY ĐƯỢC
- Orchestrator 13 KB nhúng bash macOS: `brew install`, `[[ =~ ]]`, `read -r` tương tác. Máy là Windows 11 + PowerShell.
- Đã được symlink vào `.claude\skills` → skill "đang bật" nhưng thực thi là hỏng. Tệ hơn skill tắt.
- Sửa: viết lại phần script bằng Python thuần hoặc bỏ script, chỉ giữ logic route; thêm nhánh "file audio local".

### 2.3 `youtube-transcript-pro` — CHẾT VÌ DOC LỆCH CODE
- SKILL.md nêu `fetch_transcript.py`, `clean_transcript.py`, `generate_summary.py`: **không tồn tại**.
- Ba script thật (`audio_fallback_to_markdown.py`, `channel_to_markdown.py`, `fetch.py`) **không được nhắc**.
- Whisper path: `ffmpeg -af whisper=...` cần ffmpeg build có filter whisper.cpp; ffmpeg 8.1 gyan trên máy **không có filter này** → path này chưa từng chạy được ở máy hiện tại. Sink `NUL` hardcode Windows-only.
- Chỉ có `ggml-base.bin` (yếu với tiếng Việt).
- Sửa: viết lại SKILL.md khớp 3 script; loại whisper path (thay bằng skill audio mới).

### 2.4 `youtube-transcript-basic` — LỆCH TÊN
- Frontmatter `name: youtube-transcript`, thư mục `youtube-transcript-basic`. Không có fallback khi thiếu caption.

### 2.5 `article-extractor` — CHẤP NHẬN ĐƯỢC, PHỤ THUỘC NGOÀI
- reader-cli (npm) / trafilatura (pip): chưa xác nhận cái nào cài. Không test.

### 2.6 `ship-learn-next` — CHẤP NHẬN ĐƯỢC
- Không phụ thuộc, chỉ Read/Write. Nhưng thiết kế ghi plan ra file mà `Data\Plan\` rỗng trước hôm nay → chưa dùng bao giờ, hoặc ghi chỗ khác.

## 3. Skill cá nhân khác

| Skill | Trạng thái | Lỗi |
|---|---|---|
| `personal\ChangePdfToText` | chạy được nếu Tesseract+Poppler có trong PATH (chưa kiểm) | SKILL.md hardcode `Skills\ChangePdfToText\...`, thư mục đã dời sang `Skills\Domain\personal\` |
| `personal\transcript-workspace-assets` | không phải skill (README tự nhận) | chứa `.venv`, `.git`, model 141 MB, mp4, 8 URL hardcode trong `download_transcript.py`; `RECOVERY_PLAN.md` trỏ `C:\Projects\...` không tồn tại |
| `personal\notebooklm-api` | cần Google OAuth, RPC không tài liệu, hay bị rate-limit | không dùng được offline; `[cookies]` extra không build trên Python 3.13 |
| `memory-orchestration\personal-session-workflow\session-log` | chưa kiểm | |

## 4. Kho vendored (tham khảo, không phải skill của user)

| Repo | SKILL.md | Nhận xét |
|---|---|---|
| `business\claude-skills-business-suite` | 752 | 66 % toàn kho; hầu như không liên quan luận văn/PKM |
| `science\scientific-agent-skills-main` | 147 | có `literature-review`, `markitdown`, `pdf` hữu ích cho luận văn |
| `technical\claude-skills-dev-experts` | 66 | |
| `technical\oh-my-openagent-dev` | 44 | |
| `productivity\skills-personal-workflow` | 29 | `obsidian-vault`, `teach` liên quan PKM |
| `content-production\baoyu-skills-main` | 22 | `speaker-transcript.md` prompt tái dùng được cho gate C2 |
| `memory-orchestration\claude-mem-main` | 19 | |
| `technical\skills-anthropic-official` | 18 | `skill-creator` nên dùng làm chuẩn viết skill |
| `memory-orchestration\planning-with-files-master` | 17 | 34 file .ps1, hợp Windows |
| `technical\Understand-Anything-main` | 8 | |

Thứ duy nhất chạm tới audio/diarization trong 1.133 skill: 1 prompt LLM (baoyu) và 1 chuỗi prompt (memU). **Không có xử lý âm thanh thật ở đâu cả.**

## 5. Lỗ hổng so với nhu cầu hiện tại (13 file ghi âm)

| Nhu cầu | Có sẵn? | Lấp bằng |
|---|---|---|
| Transcribe audio local tiếng Việt | Không | skill `audio-transcribe-local` (faster-whisper large-v3, GPU qua ctranslate2) |
| Khử nhiễu / VAD | Không | ffmpeg afftdn + silero VAD tích hợp |
| Diarization | Không (model pyannote đã cache nhưng torch hỏng + cần HF token) | gán tay theo timestamp; G7 backlog |
| Báo cáo tin cậy theo đoạn | Không | `quality_report.py` |
| Đưa transcript vào Claim Ledger / Knowledge Node | Không | `knowledge-template.md` theo hệ PKM 5 artifact |

## 6. Việc phải làm với bộ skill (ưu tiên giảm dần)

1. **Xây `audio-transcribe-local`** theo mẫu `book-insight` (đang làm trong PLAN_transcribe_recordings.md).
2. **Sửa `learn-this`**: bỏ bash macOS, thêm route audio. Nếu không sửa thì **gỡ symlink** để không có skill hỏng đang bật.
3. **Viết lại SKILL.md `youtube-transcript-pro`** khớp 3 script thật; xóa whisper path cũ.
4. **Sửa đường dẫn** `ChangePdfToText\SKILL.md`, `RECOVERY_PLAN.md`.
5. **Tách kho**: dời `Skills\Domain\{business,science,technical,...}` vendored sang `Reference\`; thêm `.ignore`/`.gitignore` loại `.git .venv .npm-cache __pycache__ *.bin *.mp4 cassettes`. Giữ trong `Skills\` chỉ skill tự viết + skill đã kiểm chạy được.
6. **Thêm `Skills\README.md`** làm index: tên · mục đích · trạng thái (chạy được/hỏng/tham khảo) · lần kiểm cuối.
7. **Điều tra `book-insight`**: vì sao `rejected.jsonl` và `_lowconf.jsonl` luôn 0 B.
8. Chạy lại `python -m unittest discover -s book-insight\tests -v` để có bằng chứng xanh.

## 7. Dữ liệu (`Data\`)

- `Recording\`: 13 m4a, `Voice 010 (2).m4a` trùng byte với `Voice 010.m4a`.
- `Plan\`: rỗng trước 2026-09-08 → giờ có 2 file này.
- `BookReviews\`: đầy đủ, là bằng chứng book-insight hoạt động.
- `Language\_catalog`: 4 bộ move_plan/conflicts cùng ngày 2026-09-08 19:32–19:35 → có thể là lần chạy thử lặp, nên dọn bớt.
