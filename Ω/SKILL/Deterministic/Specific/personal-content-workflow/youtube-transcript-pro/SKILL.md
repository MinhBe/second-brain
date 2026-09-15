---
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
`--no-gpu`. Tải media theo video đã chọn rồi gọi [audio-transcribe-local](../audio-transcribe-local/SKILL.md)
thông qua script Python; giữ cấu trúc Markdown và báo cáo của workflow kênh.
`--model` hiện là tên model faster-whisper đã cache (mặc định large-v3), không nhận ggml .bin.
Nếu thiếu model, báo rõ cần chuẩn bị cache; không sửa torch hoặc dùng ffmpeg whisper filter.

Lỗi riêng tư/xóa/rate limit phải được báo đúng; không biến lỗi tải thành "không có phụ đề".
Chỉ tóm tắt khi người dùng yêu cầu; mọi câu trích hoặc kết luận cần truy về transcript.
