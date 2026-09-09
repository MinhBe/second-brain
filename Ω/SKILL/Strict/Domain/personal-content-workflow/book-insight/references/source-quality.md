# Chất lượng nguồn

| Loại | Trần confidence | Trích nguyên văn | Ghi chú |
| --- | --- | --- | --- |
| manual | 100 | Có, như lời reviewer | Không tự coi là lời sách |
| auto_native | 90 | Có, kèm (auto-sub) | Đối chiếu tên riêng và chữ sai |
| auto_translated | 70 | Không | Chỉ decision/opinion; không tạo term mới |
| unknown | 60 | Không | Thiếu metadata; không suy từ đuôi file |
| book_text | 100 | Có | Xác minh edition và phạm vi đã đọc |
| note | 80 | Không | opinion, speaker=user |
| Review <5 phút | 60 | Không | Trần bổ sung, mặc định loại ở fetch |

Điểm là ceiling, không tự nâng mọi extraction lên mức này. Gộp evidence xong phải
tính lại ceiling theo nguồn yếu nhất. Nguồn không đủ chất lượng có thể chỉ nằm ở
phần ý kiến riêng, không thêm vào Core idea để tăng số reviewer.

Phân biệt subtitle manual/automatic bằng metadata subtitles/automatic_captions.
Kiểm tra tham số tlang của URL caption để phát hiện auto-translation. File vi.vtt
không chứng minh tiếng Việt gốc; en-orig là gợi ý, không thay thế metadata.
Ưu tiên vi manual, vi auto-native, en-orig, en native, rồi bản dịch. Ghi lựa chọn
vào manifest; ưu tiên này bổ sung vi auto-native mà draft bỏ sót.

source_quality mô tả chế độ đọc: reconstructed-from-reviews,
reconstructed-from-machine-translated-reviews, full-read, partial-read, highlights-only.
thesis_source_cap phản ánh ceiling yếu nhất trong các nguồn luận đề. Có toàn văn
trên đĩa chưa có nghĩa đã đọc hết; chỉ full-read khi thực sự hoàn tất.
unknown luôn hiện ở bảng nguồn và ceiling; không che dưới nhãn reconstructed chung.

BOOK ưu tiên khi xác định sách viết gì, không phủ quyết phản biện khoa học. Sách
nói tự động nhận dạng vẫn giữ trần auto_native/auto_translated, không nâng lên 100.
Không chuyển một video thành BOOK chỉ vì dài. Tách cập nhật bằng chứng bên ngoài,
ghi URL/tác giả/ngày kiểm chứng ở mục 4/8.9; không giả nhãn R cho web.
