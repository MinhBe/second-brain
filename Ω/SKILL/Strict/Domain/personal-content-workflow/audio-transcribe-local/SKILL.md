---
name: audio-transcribe-local
description: Chuyển file hoặc thư mục ghi âm local thành transcript có timestamp, báo cáo chất lượng và tri thức PKM có bằng chứng. Dùng cho m4a, wav, mp3 và các định dạng ffmpeg đọc được; YouTube URL cần tải nguồn bằng skill YouTube trước.
---

# Audio local → transcript → PKM

ASR dùng faster-whisper/CTranslate2 và model cache local. Biên tập, nhận định chủ đề và
tri thức do trợ lý thực hiện trong phiên; script không gọi API LLM và không tự suy diễn tri thức.
Dùng Python 3.11 và PowerShell. Các lệnh `scripts/...` bên dưới chạy từ thư mục chứa
SKILL.md này. Nếu đang ở Collection, thêm tiền tố
`Skills/Domain/content-production/personal-content-workflow/audio-transcribe-local/`
trước đường dẫn script. Đường dẫn mặc định được tính từ vị trí script.

## Nhận dạng

1. `python -X utf8 scripts/inventory.py --input <file-hoặc-thư-mục> --output <output>`:
   kiểm kê ffprobe và SHA-256; bản trùng được ghi lại, không xóa nguồn.
2. `python -X utf8 scripts/calibrate.py`: so sánh hai mẫu Recording đã định trong kế hoạch.
   Với bộ audio khác, gọi `transcribe.py --seconds 300` trên mẫu đại diện; không bắt buộc
   các tên file của bộ hiện tại phải tồn tại.
3. `python -X utf8 -u scripts/transcribe.py --batch --input <folder> --output <output>`:
   mặc định large-v3/CUDA/int8_float16, tiếng Việt, không prompt chuyên ngành, không denoise.
   Chỉ bật `--denoise` hoặc prompt khi có căn cứ. `--chunk-seconds 600` lưu checkpoint theo
   đoạn, overlap 2 giây được phân bổ theo trung điểm từng từ để giữ trục thời gian nguồn.
4. Mỗi file có raw JSON/SRT/TXT, quality report, progress và worker log. Không coi lời
   nhận dạng ở vùng im lặng là nội dung chắc chắn. Đọc quality report để chọn đoạn nghe lại.

`transcribe.py --input <file> --output <work-dir>` xử lý một file. `--model`, `--compute-type`,
`--beam-size`, `--language`, `--device`, `--prompt` cấu hình engine; `--force` chạy lại.
Batch dùng worker riêng mỗi file; chỉ lỗi OOM mới thử medium/int8/beam 3. Lỗi khác được
ghi rồi tiếp tục file kế tiếp; exit code khác 0 nếu có lỗi. Model chỉ đọc từ cache local.

## Biên tập và tri thức

- Đọc [cleanup-rules-vi.md](references/cleanup-rules-vi.md) trước khi sửa transcript.
- Đọc hết segment theo thứ tự, ghi `editorial.json`: title, raw_content_hash,
  reviewed_segment_ids, corrections (ID → text), unclear_segments và chapters
  (start_id/title). Giữ nguyên câu đã ổn; không xóa các đoạn để làm transcript có vẻ sạch.
- Tạo `knowledge.json` theo [knowledge-template.md](references/knowledge-template.md).
- `python -X utf8 scripts/assemble.py --dir <work-dir> --output <output>` kiểm tra độ phủ,
  hash nguồn và bằng chứng, rồi xuất transcript, PKM, INDEX và SCHEMA_MAP.
- `--all` lắp ghép các file đã có editorial/knowledge; không tự điền các file còn thiếu.
- Theo [quality-checklist.md](references/quality-checklist.md), phân biệt hoàn tất ASR,
  rà văn bản, nghe duyệt và kiểm chứng nội dung. Không tự ghi người dùng đã duyệt.

## Windows và lỗi

DLL cuBLAS/cuDNN có thể đã cài nhưng chưa nằm trong đường dẫn nạp. `common.setup_cuda()`
đăng ký các thư mục nvidia/*/bin của Python hiện tại và giữ handles; không cần sửa PATH
toàn máy hoặc torch. Smoke test phải thực sự duyệt generator ASR, không chỉ load model.
Không sửa torch hệ thống để bật diarization; phần đó cần môi trường riêng và chỉ làm khi
được yêu cầu. Tên người nói luôn chưa xác định khi chỉ có phỏng đoán từ nội dung.

## Kiểm tra

`python -X utf8 -B -m unittest discover -s tests -v`

Chỉ số avg_logprob/no_speech_prob và lặp n-gram là tín hiệu triage, không phải WER,
confidence của khẳng định hoặc bằng chứng âm thanh đã được nghe rõ.
