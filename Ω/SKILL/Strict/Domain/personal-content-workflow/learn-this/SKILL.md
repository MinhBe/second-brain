---
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
