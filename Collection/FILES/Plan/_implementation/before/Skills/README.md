# Skill đang duy trì và kho tham khảo

Kiểm kê: 11 skill trong Skills; 1123 skill tham khảo. Không suy từ số lượng rằng đã chạy được.

| Skill | Mục đích | Vị trí | Trạng thái |
|---|---|---|---|
| article-extractor | Extract clean article content from URLs (blog posts, articles, tutorials) and save as readable text. Use when user wants to download, extract, or save an article/blog post from a U | [SKILL](../Skills/Domain/content-production/personal-content-workflow/article-extractor/SKILL.md) | chưa kiểm thử runtime |
| audio-transcribe-local | Chuyển file hoặc thư mục ghi âm local thành transcript có timestamp, báo cáo chất lượng và tri thức PKM có bằng chứng. Dùng cho m4a, wav, mp3 và các định dạng ffmpeg đọc được; YouT | [SKILL](../Skills/Domain/content-production/personal-content-workflow/audio-transcribe-local/SKILL.md) | xem log pipeline và Data/Transcripts/INDEX.md |
| book-insight | Hiểu sâu sách phi hư cấu từ review YouTube, text sách và ghi chú, xuất một file Markdown tiếng Việt với luận đề, đánh giá bằng chứng, bản đồ sách, vấn đáp, keyword, core idea và lị | [SKILL](../Skills/Domain/content-production/personal-content-workflow/book-insight/SKILL.md) | 27 test đạt; nguồn hiện có đã kiểm tra |
| learn-this | Điều phối học từ sách, URL hoặc file ghi âm local để tạo tri thức và hành động. Dùng khi người dùng yêu cầu learn-this, học và áp dụng, trích nội dung rồi lập kế hoạch. | [SKILL](../Skills/Domain/content-production/personal-content-workflow/learn-this/SKILL.md) | điều phối Windows; link đã kiểm tra |
| ship-learn-next | Transform learning content (like YouTube transcripts, articles, tutorials) into actionable implementation plans using the Ship-Learn-Next framework. Use when user wants to turn adv | [SKILL](../Skills/Domain/content-production/personal-content-workflow/ship-learn-next/SKILL.md) | chưa kiểm thử runtime |
| youtube-transcript-basic | Extract transcripts from YouTube videos. Use when the user asks for a transcript, subtitles, or captions of a YouTube video and provides a YouTube URL (youtube.com/watch?v=, youtu. | [SKILL](../Skills/Domain/content-production/personal-content-workflow/youtube-transcript-basic/SKILL.md) | chưa kiểm thử runtime |
| youtube-transcript-pro | Lấy phụ đề YouTube theo ngôn ngữ, chuyển thành văn bản và tùy chọn nhận dạng audio khi không có phụ đề. Dùng cho URL/video ID hoặc báo cáo video đã chọn của workflow kênh. | [SKILL](../Skills/Domain/content-production/personal-content-workflow/youtube-transcript-pro/SKILL.md) | fixture test; live/network chưa nghiệm thu |
| session-log | Summarize the current conversation session and append results to the weekly agent-log. Use when user says "log this", "session log", "summarize this session", or asks to write resu | [SKILL](../Skills/Domain/memory-orchestration/personal-session-workflow/session-log/SKILL.md) | chưa kiểm thử runtime |
| change-pdf-to-text | Convert PDF files or folders of PDFs into Markdown and plain text, with direct text extraction first and OCR fallback for scanned documents when OCR dependencies are available. | [SKILL](../Skills/Domain/personal/ChangePdfToText/SKILL.md) | xem kiểm thử PDF; OCR phụ thuộc môi trường |
| scrum-sage | AI-powered Scrum Master and Enterprise Agility Coach based on Jeff Sutherland, Taiichi Ohno, and First Principles thinking. Use when user needs help with Scrum, sprint analysis, ba | [SKILL](../Skills/Domain/productivity/personal-action-workflow/scrum-sage/SKILL.md) | chưa kiểm thử runtime |
| unblock-action | Help the user unblock a vague or stuck action item by clarifying the intended output, scoping it to today, and identifying the concrete next action. Use when user says "unblock", " | [SKILL](../Skills/Domain/productivity/personal-action-workflow/unblock-action/SKILL.md) | chưa kiểm thử runtime |

## Kích hoạt

Junction tại .agents/skills và .claude/skills: book-insight, learn-this, audio-transcribe-local.

## Kho tham khảo

[Inventory đầy đủ](../Data/Plan/_implementation/skill_inventory.json) gồm đường dẫn, mô tả và trạng thái từng skill.
Các repo upstream và tài liệu lưu ở Reference/Domain, giữ license, lịch sử và cấu trúc. Tìm có chủ đích bằng `rg --no-ignore Reference/Domain/<nhóm>`.

[Manifest di chuyển](../Data/Plan/_implementation/moves.json) và [kiểm chứng hash](../Data/Plan/_implementation/move_verification.json).
Khôi phục vị trí bằng Data/Plan/_implementation/reorganize.ps1 -Mode Rollback; không ghi đè đích đã có.
