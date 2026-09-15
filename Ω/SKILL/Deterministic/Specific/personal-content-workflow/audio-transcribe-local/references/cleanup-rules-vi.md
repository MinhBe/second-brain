# Quy tắc biên tập tiếng Việt

Giữ lời gốc, phủ định, số, tên chưa xác định, điều kiện và thứ tự. Sửa dấu/chính tả
chỉ khi văn bản có căn cứ rõ; khi cần nghe âm thanh để quyết định thì giữ nghi vấn.
Không biến một câu ASR vô nghĩa thành lời khuyên có vẻ hợp lý.

Mỗi đoạn giữ ID và thời gian nguồn; corrections chỉ thay văn bản của ID đó.
Không xóa segment hoặc tự loại các câu quảng cáo quen thuộc nếu chưa xác minh đó là
hallucination. Đánh dấu đoạn nghi lỗi bằng unclear_segments, giữ raw để đối chiếu.
Chương/chủ đề là tổ chức biên tập, không phải tiêu đề người nói đã tuyên bố.

Nhãn Người nói? là mặc định. Tên file gợi người nói không đủ xác nhận người trong từng đoạn.
Chưa dùng diarization: không gán mã người nói nhất quán chỉ dựa vào câu hỏi/câu trả lời.
Đánh dấu nghe không rõ nghĩa là cần đối chiếu; không ghi đã nghe nếu chỉ rà văn bản.

reviewed_segment_ids chỉ được điền sau khi trợ lý thực sự đọc các đoạn tương ứng.
Không có API tự động biên tập: khi hết phiên, lưu tiến độ và tiếp tục từ ID chưa đọc.
