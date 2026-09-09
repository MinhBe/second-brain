# KẾ HOẠCH: Transcribe 13 file ghi âm hỏi thầy cô/anh chị → tri thức PKM

> Ngày lập: 2026-09-08. Nguồn khảo sát: ffprobe 13 file, pip list Python 3.11, ctranslate2 CUDA check, quét 1133 SKILL.md trong Collection.

## 0. Bối cảnh

- **Đầu vào:** 13 file `.m4a` tại `C:\Users\Admin\Documents\Collection\Data\Recording\` (12,06 giờ; 10,37 giờ nếu bỏ bản trùng). Nội dung: hội thoại hỏi thầy cô, anh chị về kiến thức; nhiều nhiễu (ghi âm điện thoại, nhiều người, môi trường ồn).
- **Đầu ra mong muốn:** transcript sạch tiếng Việt + tri thức rút ra, đưa được vào hệ PKM của user (Capture → Distill → Connect → Verify → Apply → Review; 5 artifact: Raw Inbox · Knowledge Node · Schema Map · Claim Ledger · Practice Log; confidence 3 mức).
- **Yêu cầu kèm theo:** kiểm kê và đánh giá **khắc nghiệt** bộ skill trong `C:\Users\Admin\Documents\Collection`.
- **Ràng buộc máy:** RTX 3050 6 GB, Python 3.11 hệ thống, **không có API key nào** (OpenAI/Gemini/HF) → toàn bộ chạy local; phần "hiểu nghĩa" do Claude trong phiên làm.

## 1. Kết quả khảo sát (đã xác minh)

### 1.1 File ghi âm

| File | Phút | Kênh/SR | Ghi chú |
|---|---|---|---|
| Record thầy Lâm (2).m4a | 21,8 | mono 44,1k | tên gợi ý: hỏi thầy Lâm |
| Recording (2).m4a | 108,7 | **stereo 48k** | file duy nhất stereo |
| Voice 009.m4a | 33,7 | mono | |
| Voice 010.m4a | 101,2 | mono | |
| Voice 010 (2).m4a | 101,2 | mono | **trùng byte với Voice 010** → bỏ |
| Voice 011.m4a | 40,1 | mono | |
| Voice 012.m4a | 47,6 | mono | |
| Voice 013.m4a | 57,7 | mono | |
| Voice 014.m4a | 1,8 | mono | rất ngắn |
| Voice 015.m4a | 0,6 | mono | rất ngắn, có thể rác |
| Voice 016.m4a | 5,1 | mono | |
| Voice 017.m4a | 123,7 | mono | dài nhất |
| Voice 018.m4a | 80,3 | mono | |

### 1.2 Công cụ trên máy

- ffmpeg 8.1 full (có `afftdn`, `arnndn`, `loudnorm`, `silenceremove`).
- Python 3.11: `faster-whisper 1.2.1`, `ctranslate2 4.7.2` (**thấy CUDA, hỗ trợ int8_float16**), `openai-whisper`, `silero-vad`, `noisereduce`, `librosa`, `soundfile`, `pydub`, `transformers`, `onnxruntime`.
- Model đã cache tại `~\.cache\huggingface\hub`: `Systran/faster-whisper-large-v3`, `-medium`, `-base`; `pyannote/speaker-diarization-community-1`; `speechbrain/spkrec-ecapa-voxceleb`; `nguyenvulebinh/wav2vec2-base-vi-vlsp2020`.
- **Hỏng:** `torch 2.11.0+cpu` trộn với `torchaudio/torchvision +cu128` → `import torchaudio` lỗi ngay. Ảnh hưởng: openai-whisper, pyannote, demucs. **Không ảnh hưởng faster-whisper** (đi qua ctranslate2, không qua torch).
- Chưa cài: `whisperx`, `pyannote.audio`, `demucs`, `deepfilternet`.

### 1.3 Skill hiện có (tóm tắt, chi tiết ở mục 6)

- ~1133 SKILL.md nhưng chỉ **2 skill được nối vào `.claude\skills`**: `book-insight`, `learn-this`.
- **Không có skill nào transcribe file audio local.** Whisper duy nhất nằm trong `youtube-transcript-pro/scripts/audio_fallback_to_markdown.py`, khóa sau đầu vào CSV YouTube, dùng `ggml-base.bin` qua ffmpeg whisper filter (bản ffmpeg hiện tại **không có** filter này).
- Không có khử nhiễu, VAD, diarization ở bất kỳ đâu.

## 2. Quyết định thiết kế (kèm giả định)

| # | Quyết định | Lý do |
|---|---|---|
| D1 | Engine: **faster-whisper large-v3, device=cuda, compute_type=int8_float16**, fallback `medium` nếu OOM | Chính xác nhất cho tiếng Việt trong số model có sẵn; int8 vừa 6 GB; không cần sửa torch |
| D2 | Tiền xử lý **nhẹ**: ffmpeg → 16 kHz mono WAV, `loudnorm`, `afftdn` mức vừa; **không** dùng `noisereduce`/demucs ở pass 1 | Whisper huấn luyện trên audio ồn; khử nhiễu mạnh làm mất phụ âm tiếng Việt và tăng hallucination. Chỉ thử khử mạnh cho các đoạn WER cao ở pass 2 |
| D3 | VAD: `vad_filter=True` (silero tích hợp), `min_silence_duration_ms=500`; `condition_on_previous_text=False`; `beam_size=5`; `language="vi"`; `initial_prompt` chứa thuật ngữ ngành | Giảm lặp/hallucination trên đoạn im lặng, giảm trôi ngữ cảnh |
| D4 | Diarization: **giai đoạn 2, tùy chọn**. Cần (a) sửa torch sang cu128, (b) `pip install pyannote.audio`, (c) HF token vì model gated. Nếu không làm: gán người nói thủ công theo timestamp | User không có HF token; không chặn việc chính |
| D5 | Xử lý trùng: bỏ `Voice 010 (2).m4a`; giữ nguyên file gốc, không xóa | Tránh mất dữ liệu |
| D6 | Làm sạch ngôn ngữ + rút tri thức: **Claude trong phiên** theo template có gate (mượn kiến trúc G0–G4 của `book-insight`) | Không có API key, nhất quán với cách user đã làm với book-insight |
| D7 | Đóng gói thành skill mới `audio-transcribe-local` trong `personal-content-workflow` + symlink vào `.claude\skills` | Tái sử dụng cho đợt ghi âm sau; đúng ưu tiên "đóng gói · chuyển giao" của user |
| D8 | Thứ tự chạy: file ngắn trước (014, 015, 016, Record thầy Lâm) để hiệu chỉnh tham số, rồi mới chạy lô dài | Fail fast |

**Giả định cần user xác nhận sau (không chặn):** (a) tên người nói/chủ đề từng file; (b) domain thuật ngữ (dự đoán: GAN, SQL injection, WAF, luận văn) để đưa vào `initial_prompt`; (c) có muốn làm diarization thật hay gán tay.

## 3. Cấu trúc thư mục sẽ tạo

```
Data\Recording\                      (giữ nguyên, chỉ đọc)
Data\Transcripts\
  _work\<slug>\
    audio_16k.wav                    (tiền xử lý)
    raw.json                         (segments + timestamps + avg_logprob + no_speech_prob)
    raw.srt / raw.txt
    quality_report.md                (thống kê tin cậy theo đoạn)
    clean.md                         (transcript đã sửa tiếng Việt, gắn [Người nói?] + mm:ss)
    knowledge.md                     (Knowledge Node + Claim Ledger + câu hỏi mở)
  _reports\
    inventory.csv                    (file, thời lượng, hash, trùng?)
    run_log.csv                      (file, model, thời gian chạy, RTF, %đoạn tin cậy thấp)
    checkpoint.json
  <slug>_TRANSCRIPT.md               (bản chốt)
  <slug>_KNOWLEDGE.md                (bản chốt)
  INDEX.md                           (mục lục + trạng thái + confidence)
Data\Plan\
  PLAN_transcribe_recordings.md      (file này)
  SKILL_AUDIT.md                     (đánh giá khắc nghiệt bộ skill, mục 6)
Skills\Domain\content-production\personal-content-workflow\audio-transcribe-local\
  SKILL.md
  scripts\{inventory.py, preprocess.py, transcribe.py, quality_report.py, assemble.py, common.py}
  references\{cleanup-rules-vi.md, knowledge-template.md, quality-checklist.md}
  tests\test_pipeline.py
```

Slug: `record-thay-lam-2`, `recording-2`, `voice-009` … (không dấu, không khoảng trắng).

## 4. Các giai đoạn thực thi

### Giai đoạn 0 — Chuẩn bị (≈30 phút)

0.1 Ghi kế hoạch này ra `Data\Plan\PLAN_transcribe_recordings.md`; ghi `SKILL_AUDIT.md`.
0.2 Smoke test GPU (đọc-chỉ, không cài gì):
```
python -c "from faster_whisper import WhisperModel; m=WhisperModel('large-v3',device='cuda',compute_type='int8_float16'); print('ok')"
```
   - Nếu lỗi cuDNN/cuBLAS DLL: cài `pip install nvidia-cublas-cu12 nvidia-cudnn-cu12` và thêm thư mục DLL vào PATH trong `transcribe.py` (`os.add_dll_directory`). Đây là lỗi phổ biến nhất của faster-whisper trên Windows.
   - Nếu OOM: hạ xuống `medium` + `int8`.
0.3 **Không** sửa torch ở giai đoạn này (rủi ro phá môi trường luận văn GAN). Ghi vào backlog G2.
0.4 `inventory.py`: ffprobe từng file → `inventory.csv` (duration, sr, channels, sha256, cờ trùng). Xác nhận `Voice 010 (2)` trùng.

### Giai đoạn 1 — Tiền xử lý (≈15 phút máy chạy)

`preprocess.py --in <m4a> --out _work/<slug>/audio_16k.wav`:
```
ffmpeg -i in.m4a -ac 1 -ar 16000 -af "highpass=f=80,lowpass=f=7800,afftdn=nf=-25:nt=w,loudnorm=I=-16:TP=-1.5:LRA=11" -c:a pcm_s16le out.wav
```
- Stereo (`Recording (2)`): thử thêm biến thể chỉ lấy 1 kênh (`-af "pan=mono|c0=c0"` và `c1`) nếu hai kênh là hai mic khác nhau; chọn kênh rõ hơn qua nghe 30 giây đầu.
- Xuất thêm bản **không khử nhiễu** (chỉ resample + loudnorm) để so sánh ở 1.2.

### Giai đoạn 2 — Hiệu chỉnh trên mẫu nhỏ (≈45 phút)

2.1 Chạy `transcribe.py` trên `Voice 016` (5 phút) và 5 phút đầu của `Record thầy Lâm` với 4 cấu hình: {large-v3, medium} × {có afftdn, không afftdn}.
2.2 So sánh bằng: (a) tỉ lệ đoạn `avg_logprob < -1.0`, (b) tỉ lệ đoạn `no_speech_prob > 0.6`, (c) số đoạn lặp vô nghĩa (hallucination), (d) user nghe đối chiếu 2 phút và chấm.
2.3 Chốt cấu hình + viết `initial_prompt` tiếng Việt (ví dụ: "Cuộc trao đổi về luận văn thạc sĩ, GAN, SQL injection, WAF, dataset, học sâu, mô hình sinh.") sau khi biết chủ đề thực của từng file.

### Giai đoạn 3 — Chạy lô (≈1,5–3 giờ máy chạy, chạy nền)

- `transcribe.py --batch --checkpoint _reports/checkpoint.json`: chạy tuần tự theo thứ tự thời lượng tăng dần, ghi `raw.json/srt/txt` + `run_log.csv` sau mỗi file (resume được).
- Tham số chốt: `beam_size=5, best_of=5, temperature=[0,0.2,0.4], vad_filter=True, vad_parameters={min_silence_duration_ms:500, speech_pad_ms:200}, condition_on_previous_text=False, word_timestamps=True, language='vi'`.
- Ước lượng RTF trên RTX 3050 int8: ~0,15–0,25 → 10,4 giờ audio ≈ 1,5–2,5 giờ.
- `quality_report.py` sau mỗi file: bảng theo phút (% tin cậy thấp), danh sách đoạn cần nghe lại (top 20 theo logprob thấp), phát hiện lặp n-gram.

### Giai đoạn 4 — Làm sạch transcript (Claude trong phiên, theo gate)

Mỗi file đi qua 3 gate, ghi ở `clean.md`:
- **C1 Chuẩn hóa:** sửa chính tả/dấu tiếng Việt, bỏ từ đệm ("ờ", "à", "kiểu như"), gộp câu ngắt; giữ nguyên nghĩa, **không thêm ý**. Đoạn không chắc ghi `[nghe không rõ 12:34]`, không đoán.
- **C2 Gắn người nói:** heuristic từ nội dung (câu hỏi = user, trả lời = thầy/anh chị) + timestamp; đánh dấu `[Người nói?]` khi không chắc. Tái dùng quy tắc trong `Skills\Domain\content-production\baoyu-skills-main\...\baoyu-youtube-transcript\prompts\speaker-transcript.md` (gán người nói theo văn bản, khung `[HH:MM:SS → HH:MM:SS]`, không dịch, giữ nguyên lời). Nếu bật diarization ở G7 thì thay bằng nhãn tự động.
- **C3 Phân đoạn chủ đề:** chia theo câu hỏi; mỗi khối có tiêu đề + mm:ss bắt đầu.
- Quy tắc viết trong `references/cleanup-rules-vi.md`; checklist trong `quality-checklist.md`.

### Giai đoạn 5 — Rút tri thức theo hệ PKM của user

Mỗi file → `knowledge.md` với template cố định (`references/knowledge-template.md`):
1. **Raw Inbox:** liên kết tới transcript + timestamp.
2. **Knowledge Node (SLIM 5 mục):** câu hỏi đã hỏi · câu trả lời cốt lõi · ví dụ/ngữ cảnh · điều kiện áp dụng · liên kết node khác.
3. **Claim Ledger:** mỗi khẳng định của thầy cô/anh chị 1 dòng: nội dung · ai nói · timestamp · confidence (thấp/vừa/cao) · trạng thái kiểm chứng (chưa/đã, nguồn).
4. **Câu hỏi mở / mâu thuẫn** giữa các nguồn (thầy A nói khác anh B).
5. **Practice Log gợi ý:** 1–3 việc cụ thể để áp dụng vào luận văn.
6. **Lịch ôn:** +1/+4/+12/+30 ngày (đồng bộ với book-insight).

Cuối cùng `assemble.py` gộp thành `<slug>_TRANSCRIPT.md`, `<slug>_KNOWLEDGE.md`, cập nhật `INDEX.md`; tạo `Schema Map` tổng hợp liên kết chủ đề xuyên các file.

### Giai đoạn 6 — Đóng gói skill `audio-transcribe-local`

- SKILL.md theo chuẩn `skill-creator` (tiếng Việt, có frontmatter, allowed tools `Bash,Read,Write`), mô tả 6 gate, tham số, lỗi thường gặp (cuDNN DLL, OOM, hallucination).
- `tests/test_pipeline.py`: test inventory (phát hiện trùng), test quality_report trên `raw.json` giả, test assemble.
- Symlink vào `Collection\.claude\skills\audio-transcribe-local` (giống 2 skill hiện có).
- Cập nhật `learn-this` để route "file audio local" → skill mới.

### Giai đoạn 7 (tùy chọn, backlog) — Diarization thật

- Sửa torch: `pip uninstall torch && pip install torch --index-url https://download.pytorch.org/whl/cu128` (khớp torchaudio 2.11.0+cu128). **Làm trong venv riêng** `C:\Users\Admin\ai_env` (đang rỗng) để không đụng môi trường luận văn.
- `pip install pyannote.audio`; xin HF token, accept điều khoản model `pyannote/speaker-diarization-community-1` (đã cache nhưng gated).
- Ghép nhãn người nói vào `raw.json` theo overlap timestamp; chạy lại C2.

## 5. Rủi ro và cách xử lý

| Rủi ro | Dấu hiệu | Xử lý |
|---|---|---|
| faster-whisper không load CUDA | lỗi `cudnn_ops64_9.dll`/`cublas64_12.dll` | cài `nvidia-cudnn-cu12`, `nvidia-cublas-cu12`; `os.add_dll_directory` |
| OOM 6 GB | CUDA out of memory | `medium` + `int8`; giảm `beam_size=3` |
| Hallucination đoạn im lặng/ồn | lặp câu, "Hãy subscribe…" | VAD chặt hơn, `no_speech_threshold=0.5`, `compression_ratio_threshold=2.0`; cắt bỏ theo quality report |
| Nhiều người nói chồng tiếng | logprob thấp cục bộ | đánh dấu `[nghe không rõ]`, không đoán; user nghe lại |
| Khử nhiễu làm hỏng giọng | pass có afftdn kém hơn pass không | dùng bản không khử nhiễu (đã xuất song song) |
| Thuật ngữ chuyên ngành/tiếng Anh xen lẫn | "GAN" → "gan", "WAF" → "oáp" | `initial_prompt` + bảng thay thế trong C1 |
| Sửa torch phá môi trường luận văn | import lỗi ở project GAN | chỉ làm trong venv riêng (G7) |

## 6. Đánh giá khắc nghiệt bộ skill trong Collection (tóm tắt; bản đầy đủ ghi `SKILL_AUDIT.md`)

**Kết luận chung:** bộ sưu tập là **kho tham khảo chưa vận hành**, không phải hệ skill đang dùng. 1133 SKILL.md nhưng chỉ 2 được nối; ~99,8 % là code người khác vendored nguyên repo (kể cả `.git`, `.venv`, `.npm-cache`, model 141 MB) làm ripgrep timeout. Không có lộ trình nào từ "kho" đến "dùng".

**Skill tự viết (6 cái trong `personal-content-workflow`):**
- `book-insight` — **tốt nhất**, có gate, test, references, provenance. Là mẫu nên nhân bản. Điểm trừ: chỉ chạy được với YouTube, chưa có test chạy lại gần đây.
- `learn-this` — orchestrator nhưng nhúng bash macOS (`brew`, `read -r`) → **không chạy được trên máy này**. Sai nền tảng cơ bản.
- `youtube-transcript-pro` — SKILL.md **mô tả 3 script không tồn tại** và bỏ qua 3 script thật; whisper path cần ffmpeg có filter whisper mà máy không có. Tài liệu và code lệch nhau = skill chết.
- `youtube-transcript-basic` — tên trong frontmatter (`youtube-transcript`) khác tên thư mục.
- `article-extractor`, `ship-learn-next` — chấp nhận được, chưa có test.

**Skill cá nhân khác:** `ChangePdfToText` đường dẫn cứng đã sai sau khi di chuyển thư mục; `transcript-workspace-assets` là bãi rác workspace tự nhận "không phải skill"; `RECOVERY_PLAN.md` trỏ tới `C:\Projects\...` không tồn tại.

**Lỗ hổng so với nhu cầu hiện tại:** không có skill nào cho audio local, khử nhiễu, VAD, diarization, hay đưa transcript vào Claim Ledger/PKM. Đây chính là thứ giai đoạn 6 lấp.

**Khuyến nghị dọn (ngoài phạm vi kế hoạch này, cần user quyết):** tách `Skills\Domain\*` vendored ra `Reference\`, thêm `.gitignore`/`.ignore` để loại `.venv/.git/models`; sửa 4 SKILL.md sai đường dẫn/nền tảng; giữ chỉ những skill có test chạy xanh trong `.claude\skills`.

## 7. Kiểm chứng (Definition of Done)

1. `inventory.csv` có 13 dòng, 1 dòng cờ trùng.
2. Smoke test GPU in ra `ok`; `run_log.csv` ghi `device=cuda` cho mọi file.
3. 12 file có `raw.json` + `raw.srt`; `quality_report.md` cho từng file; tổng % đoạn tin cậy thấp được báo cáo.
4. User nghe đối chiếu 2 phút ngẫu nhiên trên 3 file (ngắn/vừa/dài) và chấm transcript đạt mức dùng được.
5. Mỗi file có `_TRANSCRIPT.md` và `_KNOWLEDGE.md` đúng template; `INDEX.md` liệt kê đủ 12 file với confidence.
6. `python -m unittest discover -s Skills\...\audio-transcribe-local\tests -v` xanh.
7. `Data\Plan\` chứa `PLAN_transcribe_recordings.md` và `SKILL_AUDIT.md`.

## 8. Ước lượng thời gian

| Giai đoạn | Máy chạy | Người/Claude |
|---|---|---|
| 0–2 chuẩn bị + hiệu chỉnh | 20 phút | 1,5 giờ |
| 3 chạy lô | 1,5–2,5 giờ (nền) | 10 phút theo dõi |
| 4 làm sạch 12 file | — | 3–5 giờ (Claude), user nghe đối chiếu 30 phút |
| 5 rút tri thức | — | 2–3 giờ |
| 6 đóng gói skill | — | 1,5 giờ |
| 7 diarization (tùy chọn) | 1 giờ | 1 giờ |
