# Trạng thái phục hồi workflow YouTube

Tài liệu kế hoạch cũ được lưu trong Data/Plan/_implementation/before trước khi sửa.
Workflow đang được duy trì tại `Skills/Domain/content-production/personal-content-workflow`.

- youtube-transcript-pro/scripts/fetch.py: một URL/ID, lựa chọn ngôn ngữ và làm sạch phụ đề.
- youtube-transcript-pro/scripts/channel_to_markdown.py: lựa chọn video trong kênh, báo cáo và Markdown.
- youtube-transcript-pro/scripts/audio_fallback_to_markdown.py: ASR media qua audio-transcribe-local.
- audio-transcribe-local/scripts/transcribe.py: faster-whisper, CUDA DLL discovery, resume.

Không còn dùng các đường dẫn C:\Projects cũ hoặc tên script dự kiến fetch_transcript.py,
clean_transcript.py, generate_summary.py để chạy workflow. Các file workspace tại đây là
tài liệu lịch sử, không phải skill được kích hoạt và không được coi là bản triển khai hiện hành.
Xem `Skills/README.md` từ gốc Collection để tra vị trí và bằng chứng kiểm tra mới nhất.
