# Đối chiếu giữa các nguồn

Các liên hệ dưới đây do trợ lý tổng hợp từ văn bản ASR chưa nghe duyệt. Không có căn cứ xác định thứ tự thời gian của các file chỉ từ số Voice; chưa xác định người nói. Việc nhiều bản lặp một ý không phải kiểm chứng độc lập.

| Chủ đề | Liên hệ có thể dùng để học | Nguồn |
|---|---|---|
| Câu chuyện nghiên cứu | Nêu bài toán và vai trò bộ sinh/bộ phát hiện, mô tả đầu ra được dùng ở đâu rồi mới trình bày cải tiến | [Thầy Lâm N1](record-thay-lam-2_KNOWLEDGE.md#N1), [Voice 009 N1](voice-009_KNOWLEDGE.md#N1), [Voice 018 N1](voice-018_KNOWLEDGE.md#N1) |
| Chứng minh đóng góp | Ổn định baseline, tái lập và thử riêng từng thay đổi; giải thích tác động thay vì chỉ nêu tên cấu hình | [Thầy Lâm N4](record-thay-lam-2_KNOWLEDGE.md#N4), [Voice 011 N2/N3](voice-011_KNOWLEDGE.md#N3), [Voice 012 N2](voice-012_KNOWLEDGE.md#N2) |
| Định nghĩa phép đo | Tách cấu trúc, tính mới, đa dạng và hiệu quả phát hiện; ghi rõ công thức, tập đánh giá và mốc so sánh | [Thầy Lâm N2](record-thay-lam-2_KNOWLEDGE.md#N2), [Voice 012 N1](voice-012_KNOWLEDGE.md#N1), [Voice 013 N2](voice-013_KNOWLEDGE.md#N2) |
| Giới hạn kết luận | Phân biệt qua WAF, chuỗi hợp lệ và khả năng thực thi; kiểm tra tiêu chí đánh giá có độc lập với hàm thưởng hay không | [Voice 012 N3](voice-012_KNOWLEDGE.md#N3), [Voice 013 N3](voice-013_KNOWLEDGE.md#N3), [Voice 018 N2](voice-018_KNOWLEDGE.md#N2) |
| Trình bày cho người khác | Slide đọc được, có ví dụ và chọn minh chứng phù hợp; rút thời lượng bằng lựa chọn nội dung | [Voice 009 N2](voice-009_KNOWLEDGE.md#N2), [Voice 014 N1](voice-014_KNOWLEDGE.md#N1), [Voice 018 N1](voice-018_KNOWLEDGE.md#N1) |

## Những điểm chưa được giải quyết

1. **Khả năng khai thác thực tế.** [Voice 013 S00477–S00478](voice-013_TRANSCRIPT.md#S00477) có lời nhận xét về một mẫu có khả năng khai thác, trong khi [Voice 012 S00381](voice-012_TRANSCRIPT.md#S00381) nói môi trường không có database và [Voice 018 S00814–S00816](voice-018_TRANSCRIPT.md#S00814) thừa nhận mẫu qua bộ lọc có thể chỉ là nhiễu. Có thể khác phiên bản thí nghiệm hoặc khác cách dùng từ; chưa kết luận bên nào đúng. Cần mã, môi trường và kết quả thử gắn với từng mẫu.
2. **Tiêu chí học và đánh giá.** [Voice 018 S00817–S00819](voice-018_TRANSCRIPT.md#S00817) thuật lại phản biện dùng cùng bộ rule. Cần đối chiếu code và tập test; chưa biết mức trùng lặp thực tế.
3. **Con số và thuật ngữ.** Tỷ lệ dữ liệu, trọng số reward, mã DV7/DV8, tên họ payload, số token/ký tự và tên bộ dữ liệu có nhiều biến thể trong ASR. Không lấy số ở một file để tự sửa file khác.
4. **Đối tượng của lời khuyên.** Các buổi có thể chứa nhiều đề tài và người trình bày. Không biến mọi góp ý thành yêu cầu riêng cho cùng một luận văn.
5. **Nội dung chồng lặp dù hash khác.** `Recording (2)` và `Voice 017` có nhiều đoạn tương ứng, chẳng hạn [Recording S00331](recording-2_TRANSCRIPT.md#S00331) và [Voice 017 S00330](voice-017_TRANSCRIPT.md#S00330) về vấn đề điểm thưởng, cùng chuỗi chủ đề kế tiếp. Đây là dấu hiệu có thể ghi cùng buổi; chưa căn chỉnh toàn bộ bằng âm thanh. Giữ timestamp và nguồn riêng, không cộng hai lời tương ứng thành bằng chứng độc lập. Con số 10,37 giờ là tổng thời lượng các file khác hash, không phải thời lượng nội dung độc nhất đã xác nhận.

## Thứ tự áp dụng đề xuất

- [ ] Chốt một sơ đồ bài toán và bảng thuật ngữ từ mã/slide gốc.
- [ ] Lập ma trận thí nghiệm: giả thuyết, baseline, thay đổi, nguồn dữ liệu, phép đo, bằng chứng và giới hạn.
- [ ] Nghe những đoạn đang dùng làm claim quan trọng, sửa transcript qua editorial rồi mới dùng lại số liệu hoặc trích lời.

[Schema Map](SCHEMA_MAP.md) · [Mẫu nghe duyệt](_review/LISTENING_REVIEW.md)
