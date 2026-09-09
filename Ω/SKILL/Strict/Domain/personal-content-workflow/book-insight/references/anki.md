# Anki CSV

`assemble_insight.py --dir <out> --anki` sinh cards.csv UTF-8 và anki_ids.json.
Ba loại: giải thích Core idea, định nghĩa term VI/EN, câu Q&A đã có đáp án.
Câu chưa trả lời không xuất. Bản draft không xuất Anki.

Note type Book Insight có trường ID, Front, Back, Source, Book. Cột thứ sáu Tags
được ánh xạ tới tags hệ thống bằng header `#tags column:6`.
Front template: `{{Front}}`; back template: `{{FrontSide}}<hr id=answer>{{Back}}<br>{{Source}}`.
ID ở field đầu, không hiển thị trên mặt thẻ. Tạo note type trước khi import CSV.

ID ánh xạ từ slug/type/source-record-ID, được lưu ở anki_ids.json; không phụ thuộc
thứ tự bảng. Giữ ID khi sửa extraction/term/QA. Không xóa registry để đánh số lại.
Khi nhập chọn cập nhật note trùng field ID và cùng note type. Đây là điều chỉnh so
với draft guid_for: CSV dùng ID field đầu, không tự tạo GUID nội bộ Anki.
Theo [Anki manual](https://docs.ankiweb.net/importing/text-files.html#duplicates-and-updating),
cập nhật note tại chỗ giữ scheduling; test CSV đơn thuần không chứng minh đã import đúng UI.

Kiểm tra thực tế: nhập lần đầu, học một thẻ, đổi Back và reorder CSV, nhập cập nhật;
số note không tăng và lịch thẻ đã học giữ nguyên. Agent không đụng collection đang dùng
để thử; chỉ báo đã kiểm bước này nếu thực sự thực hiện trong profile thử riêng.
