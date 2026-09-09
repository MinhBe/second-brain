# Kế hoạch: Skill `audio-course-to-anki` — chuyển Glossika GMS (audio + sách scan) thành deck Anki

## 1. Bối cảnh

Bạn có bộ **Glossika Chinese (Mandarin) Complete Fluency Course 1–3 (2014)**, mỗi tập gồm:

- PDF sách (**bản scan, không có lớp text** → muốn lấy text từ sách phải OCR).
- Thư mục `GMS` (mã `ENZS` = Trung đại lục, **giản thể**) — **bộ bạn chọn dùng**.
- Thư mục `GMS-UPDATE` (mã `ENZH` = Đài Loan, phồn thể) — bỏ qua.

Mỗi thư mục audio có 60 file = 20 nhóm × 3 phiên bản. Quy ước tên file đã xác minh:

| Phần tên | Ý nghĩa |
|---|---|
| `GLOSSIKA-ENZS-F1-GMS-0051C.mp3` | `F1` = tập 1; `0051` = **câu bắt đầu** của nhóm 50 câu (51–100); `C` = phiên bản |
| Phiên bản `A` | mỗi câu: EN → ZH → ZH (~153 khoảng lặng/file) |
| Phiên bản `B` | mỗi câu: EN → ZH (~105 khoảng lặng/file) |
| Phiên bản `C` | **chỉ ZH, 1 lần/câu, đúng 50 câu + intro + outro = 52 khoảng lặng/file** — nguồn cắt audio sạch nhất |

Tập 2 đánh số 1001–2000, tập 3 đánh số 2001–3000 → toàn khoá **3000 câu**, ID câu toàn cục = số trong tên file + chỉ số trong nhóm (0-based).

Audio: mp3 mono 44.1 kHz 64 kbps. Đã kiểm tra `silencedetect noise=-35dB d=0.6` tách đúng 52 khoảng lặng trên cả file đầu và file cuối tập 1 → thuật toán cắt theo khoảng lặng là khả thi, không cần Whisper để **định vị** câu; Whisper chỉ để **đọc nội dung**.

Quyết định của bạn (đã chốt):
- Chỉ giản thể (thư mục `GMS`).
- Nguồn text = transcript audio **đối chiếu** với OCR PDF, câu lệch thì gắn cờ để duyệt tay.
- 3 kiểu thẻ, **chỉ Anh–Trung, không pinyin, không tiếng Việt** (cột Vietnamese để trống, điền sau).
- Skill viết theo chuẩn Anthropic Agent Skills (`SKILL.md` + `scripts/` + `references/`), hỗ trợ transcript vi / en (US) / zh / ko / ja.

## 2. Môi trường máy bạn (đã kiểm tra)

| Thành phần | Trạng thái |
|---|---|
| Python 3.11 (`python`) | có; `whisper`, `faster-whisper`, `ctranslate2` thấy **1 GPU CUDA** (RTX 3050 6 GB) → chạy faster-whisper `large-v3` int8_float16 được |
| `torch` | bản CPU — không sao, faster-whisper không cần torch |
| `ffmpeg` / `ffprobe` 8.1 | có (winget) |
| `PyMuPDF (fitz)`, `pypdf`, `pdftotext` | có → render trang PDF ra ảnh để OCR |
| `paddleocr`, `pytesseract` | có paddleocr (dùng cho zh/en); tesseract binary **chưa có** → dùng PaddleOCR |
| `genanki`, `pypinyin`, `opencc` | **chưa cài** → `pip install genanki opencc-python-reimplemented` (pypinyin tuỳ chọn, bạn không dùng pinyin) |
| Anki desktop | chưa cài → xuất `.apkg` bằng genanki, không dùng AnkiConnect |

## 3. Cấu trúc skill (chuẩn Anthropic Agent Skills)

Đặt tại `C:\Users\Admin\.claude\skills\audio-course-to-anki\`:

```
audio-course-to-anki/
├── SKILL.md                      # frontmatter name + description; hướng dẫn ngắn gọn cho Claude, < 500 dòng
├── scripts/
│   ├── segment_audio.py          # cắt file theo khoảng lặng → N đoạn, kiểm tra N == kỳ vọng, ghi manifest
│   ├── transcribe.py             # faster-whisper theo từng đoạn, nhận language, initial_prompt theo ngôn ngữ
│   ├── ocr_pdf.py                # PaddleOCR trang sách → text có số câu
│   ├── align_sources.py          # ghép transcript ↔ OCR theo số câu, tính độ giống, gắn cờ lệch
│   ├── build_anki.py             # genanki: note type 3 template, media, .apkg
│   └── verify_deck.py            # kiểm tra đếm câu, media thiếu, ID trùng, HTML rác
├── references/
│   ├── anki-note-schema.md       # đặc tả field, template, CSS, quy tắc GUID/ID
│   ├── languages.md              # bảng ngôn ngữ: mã Whisper, model khuyên dùng, initial_prompt, chuẩn hoá text
│   ├── file-naming.md            # regex tên file Glossika + cách mở rộng cho khoá khác
│   └── qa-checklist.md           # checklist duyệt tay
└── assets/
    └── card.css                  # CSS dùng chung cho template
```

Quy tắc trong `SKILL.md` (theo spec): frontmatter chỉ có `name: audio-course-to-anki` và `description` nêu **làm gì + khi nào dùng** ("Use when the user has a language-course audio set (Glossika-style numbered mp3 + book PDF) and wants a numbered, timestamped transcript and an Anki .apkg…"); thân file nêu quy trình 6 bước, mỗi bước gọi 1 script bằng lệnh cụ thể, chi tiết nằm trong `references/` (progressive disclosure). Không XML trong frontmatter, tên thư mục kebab-case, file đúng tên `SKILL.md`.

## 4. Pipeline 6 bước

Thư mục làm việc: `<khoá>/anki_build/` (không ghi vào thư mục audio gốc).

### Bước 1 — Quét & lập danh mục (`segment_audio.py --scan`)
- Regex tên file: `^GLOSSIKA-(?P<pair>[A-Z]{4})-F(?P<vol>\d)-GMS-(?P<start>\d{4})(?P<ver>[ABC])\.mp3$`.
- Sinh `manifest.json`: mỗi file → `volume`, `start_id`, `end_id = start+49`, `version`, `expected_sentences=50`, `expected_repeats` (A=3, B=2, C=1), thời lượng (ffprobe).
- Cảnh báo nếu thiếu nhóm nào trong dãy 0001…0951.

### Bước 2 — Cắt audio theo khoảng lặng (`segment_audio.py --cut`)
- Chạy `ffmpeg silencedetect noise=-35dB d=0.6` lên **file C** (ZH-only). Lấy các điểm giữa của khoảng lặng làm ranh giới → danh sách đoạn `[start,end]`.
- Bỏ đoạn đầu (intro "Glossika… Fluency 1…") và đoạn cuối (outro) → phải còn **đúng 50 đoạn**. Nếu không: tự thử lại lưới tham số (`-30/-35/-40 dB` × `0.4/0.6/0.8 s`), chọn tổ hợp cho đúng 50; vẫn sai → ghi vào `needs_review.csv`, không đoán.
- Thêm padding 80 ms hai đầu, xuất `media/ZS_F1_00051.mp3` (mp3 64k mono, giữ nguyên codec để không giảm chất lượng) bằng `-ss/-to -c copy` hoặc re-encode nếu cắt lệch frame.
- Ghi `segments_C.csv`: `sentence_id, file, seg_idx, t_start, t_end, duration, media_file`.
- File **A**: cắt tương tự nhưng kỳ vọng 150 đoạn, gán mẫu (EN, ZH, ZH) lặp → lấy đoạn EN làm `audio_en` (tuỳ chọn, thẻ 3 có thể phát EN) và làm nguồn transcript tiếng Anh. File B không cần.
- Đây là "nhãn thời gian chính xác" bạn yêu cầu: mọi câu đều có `t_start/t_end` trong file gốc + số câu toàn cục.

### Bước 3 — Transcript từng đoạn (`transcribe.py`)
- `faster-whisper large-v3`, `device=cuda`, `compute_type=int8_float16` (vừa 6 GB), `beam_size=5`, `vad_filter=False` (đã cắt sẵn), `condition_on_previous_text=False` (tránh lặp nhiễm giữa đoạn).
- **Transcript theo đoạn đã cắt, không transcript cả file** → không bao giờ dính 2 câu vào 1, và số câu luôn khớp với số đoạn.
- Tham số `--language` bắt buộc, không để auto-detect (đoạn 3–4 s detect hay sai). Bảng trong `references/languages.md`:

| Ngôn ngữ | mã | model | initial_prompt (mồi dấu câu/chữ viết) | chuẩn hoá |
|---|---|---|---|---|
| zh (giản thể) | `zh` | large-v3 | "以下是普通话的句子。" | OpenCC `t2s` ép giản thể, dấu câu toàn角 `，。？！` |
| zh (phồn thể) | `zh` | large-v3 | "以下是繁體中文的句子。" | OpenCC `s2twp` |
| en (US) | `en` | large-v3 / medium.en | "The following are American English sentences." | NFKC, sửa curly quotes |
| vi | `vi` | large-v3 | "Sau đây là các câu tiếng Việt." | NFC (Unicode tổ hợp dấu) |
| ko | `ko` | large-v3 | "다음은 한국어 문장입니다." | NFC, giữ khoảng trắng gốc |
| ja | `ja` | large-v3 | "以下は日本語の文です。" | NFKC, dấu câu 。、 |

- Xuất `transcript_<lang>.csv`: `sentence_id, text_raw, text_norm, avg_logprob, no_speech_prob, t_start, t_end`. Câu có `avg_logprob < -0.8` hoặc `no_speech_prob > 0.5` → cờ `LOW_CONF`.
- Ước lượng thời gian: 1000 đoạn ZH × ~4 s + 1000 đoạn EN ≈ 2 giờ audio → large-v3 trên 3050 ≈ 15–25 phút/tập.

### Bước 4 — OCR sách để đối chiếu (`ocr_pdf.py`)
- PyMuPDF render trang ở 200 dpi → PaddleOCR `lang=ch` (nhận cả Hán + Latin).
- Chỉ OCR vùng trang có câu (dò bằng regex số thứ tự `^\d{1,4}\b` ở đầu dòng; sách Glossika in mỗi câu: số, EN, 简体, 繁體, pinyin, IPA). Tách theo số câu → `book_sentences.csv`: `sentence_id, en_ocr, zh_ocr, pinyin_ocr, page`.
- Chấp nhận OCR nhiễu: mục đích là **đối chiếu**, không phải nguồn duy nhất.

### Bước 5 — Ghép & gắn cờ (`align_sources.py`)
- Khoá ghép = `sentence_id`. Với ZH: so `transcript_zh.text_norm` vs `zh_ocr` bằng tỉ lệ ký tự chung (`difflib.SequenceMatcher`, bỏ dấu câu). Với EN: so token-level sau lowercase.
- Quy tắc chọn text cuối:
  - giống ≥ 0.9 → lấy transcript (dấu câu tốt hơn OCR).
  - 0.6–0.9 → lấy transcript, cờ `CHECK`.
  - < 0.6 hoặc thiếu 1 bên → cờ `MISMATCH`, đưa cả 2 phiên bản vào `needs_review.csv`.
- Xuất `master.csv` (nguồn duy nhất để build Anki): `sentence_id, volume, group, en, zh_simp, zh_trad(opencc), pinyin(tuỳ chọn), vi(trống), audio_zh, audio_en, t_start, t_end, src_file, confidence, flags`.
- Bạn duyệt `needs_review.csv` trong Excel/VS Code, sửa trực tiếp `master.csv` rồi build.

### Bước 6 — Build Anki (`build_anki.py`) + kiểm tra (`verify_deck.py`)
Chi tiết ở mục 5. Đầu ra `Glossika_ZS_F1.apkg` (và F2, F3 hoặc gộp 1 deck có subdeck `Glossika ZS::F1`).

## 5. Cấu trúc Anki chuẩn

### Note type `Glossika Sentence (EN-ZS)` — 1 note = 1 câu, sinh 3 card
Field (thứ tự cố định, field đầu là sort field/unique):

| # | Field | Nội dung |
|---|---|---|
| 1 | `ID` | `ZS-F1-0051` (đúng số câu, zero-pad 4) — sort field, dùng làm GUID |
| 2 | `Hanzi` | câu giản thể |
| 3 | `English` | câu tiếng Anh |
| 4 | `Audio_ZH` | `[sound:ZS_F1_0051.mp3]` |
| 5 | `Audio_EN` | `[sound:ZS_F1_0051_en.mp3]` (từ file A; nếu bạn không cần thì để trống, template bỏ qua) |
| 6 | `Vietnamese` | trống, điền sau |
| 7 | `Pinyin` | trống hoặc tự sinh, **không hiển thị** trên card |
| 8 | `Source` | `F1-GMS-0051C 00:12.34–00:16.67` (truy vết) |
| 9 | `Notes` | trống |

Tags: `glossika`, `zs`, `f1`, `g0051` (nhóm 50 câu — để bạn học/treo theo nhóm như sách).

### 3 card template (đúng yêu cầu của bạn, không pinyin)

| Card | Mặt trước | Mặt sau |
|---|---|---|
| 1 `Listen ZH` | `{{Audio_ZH}}` (tự phát) | Hanzi + English (+ Audio_ZH phát lại) |
| 2 `Read ZH` | `{{Hanzi}}` | Audio_ZH + English |
| 3 `Read EN` | `{{English}}` | Hanzi + Audio_ZH |

Mọi template dùng `{{FrontSide}}<hr id=answer>` ở mặt sau (chuẩn Anki), CSS trong `assets/card.css` (font `Noto Sans SC`, cỡ Hán 40 px, English 22 px, hỗ trợ `.night_mode`). Điều kiện `{{#Vietnamese}}…{{/Vietnamese}}` để dòng tiếng Việt tự hiện khi bạn điền sau.

### Quy tắc ID để cập nhật không mất tiến độ ôn (quan trọng)
- `model_id` và `deck_id` là hằng số cố định trong script (random 1 lần, ghi vào `references/anki-note-schema.md`).
- `guid = genanki.guid_for(ID)` → build lại `.apkg` sau khi sửa text, import vào Anki sẽ **cập nhật note cũ**, không tạo trùng, giữ lịch ôn.
- Tên media không dấu, không khoảng trắng, độc nhất toàn cầu (`ZS_F1_0051.mp3`) để không đè media của deck khác.
- Không HTML trong field ngoài `[sound:]`; kiểm tra bằng `verify_deck.py`.

### Deck
- Deck cha `Glossika ZS`, con `Glossika ZS::F1`, `::F2`, `::F3`. Mỗi tập 1 lần chạy pipeline, 1 file `.apkg`.

## 6. Kiểm chứng (verify_deck.py + duyệt tay)

Tự động:
- Mỗi tập: 1000 note, 3000 card, 1000 (hoặc 2000) media; không ID trùng; không media tham chiếu mà không tồn tại.
- Mọi đoạn ZH có duration 1–12 s; đoạn ngoài khoảng → cờ.
- Tỉ lệ `MISMATCH` < 5 % thì coi pipeline ổn; cao hơn → xem lại ngưỡng cắt hoặc OCR.
- Mở `.apkg` bằng `sqlite3` đọc `notes/cards` đếm lại (apkg là zip chứa `collection.anki2`).

Thử nghiệm theo thứ tự (rollout):
1. Chạy bước 1–3 chỉ với nhóm `0001` (50 câu) → nghe thử 5 đoạn ngẫu nhiên, so transcript.
2. OCR đúng các trang chứa câu 1–50 → align → xem `needs_review.csv`.
3. Build `.apkg` 50 câu → import Anki (cần cài Anki desktop hoặc AnkiDroid) → kiểm tra 3 card hiển thị, audio phát, sửa CSS.
4. Chạy cả tập 1 (20 nhóm). Sau đó tập 2, 3 chỉ đổi tham số `--volume`.
5. Ghi lại các tham số đã chọn (dB, d, ngưỡng giống) vào `references/` để khoá khác (ko/ja/vi) tái dùng.

## 7. Tổng quan việc bạn sẽ làm sau khi duyệt kế hoạch

1. `pip install genanki opencc-python-reimplemented` (paddleocr, faster-whisper đã có).
2. Tạo skill bằng `/skill-creator` theo cấu trúc mục 3; viết 6 script theo mục 4.
3. Chạy thử nhóm 0001 → sửa ngưỡng → chạy cả khoá.
4. Duyệt `needs_review.csv`, build lại `.apkg`, import Anki.

Giả định đã nêu: bỏ pinyin & tiếng Việt khỏi card nhưng vẫn giữ field trống; audio EN từ file A là tuỳ chọn; không dùng thư mục `GMS-UPDATE`.
