# Hợp đồng knowledge.json

- created: ngày ISO làm mốc ôn; giữ nguyên ngày khi lắp ghép lại.
- claims: id, text (diễn giải có giới hạn), confidence (thấp/vừa/cao), confidence_reason,
  evidence (danh sách segment_id/quote; quote phải là chuỗi nguyên văn có trong raw),
  verification (mặc định "chưa kiểm chứng"). Nếu kiểm chứng bên ngoài, thêm verification_source.
- nodes: id, title, question, answer, context, conditions, claim_ids, connections, tags.
  Chỉ tạo node có claim thật hỗ trợ. Các node có thể chia sẻ tag để Schema Map nối xuyên file.
- open_questions: câu hỏi còn thiếu thông tin, thuật ngữ cần nghe lại và giới hạn diễn giải.
- practice: 1–3 việc cụ thể do trợ lý đề xuất, phù hợp nội dung thực tế, không mặc định luận văn.

Không bắt buộc đủ số claim/node khi audio nghèo thông tin. Confidence cao chỉ nên dùng
cho cách diễn giải trực tiếp, rõ trong văn bản; nghe chưa duyệt vẫn phải ghi rõ. Nó không
là sự chứng thực kiến thức chuyên ngành. Không tìm trên web nội dung riêng của bản ghi.

Assembler sinh Raw Inbox, SLIM 5 mục, Claim Ledger, câu hỏi mở, Practice Log, lịch ôn.
Các quote được giữ ngắn, đủ chứng minh claim. Tổng hợp xuyên file phải phân biệt đồng
chủ đề với đồng thuận; không tự gán các người chưa xác định thành cùng một người.
