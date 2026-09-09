# Tầng 1: phân tích sách

Đối chiếu upstream book-summary v1.0.0 trong _upstream. Giữ đủ 8 bước, 10 quy tắc,
7 edge case; các sửa đổi cho nguồn review ghi rõ dưới đây.

| Bước | Nội dung phải làm | Khi chỉ có review |
| --- | --- | --- |
| 1. Bối cảnh | Trạng thái đọc, tên/tác giả/năm/dịch giả; nguồn, mục đích, domain, mức quen thuộc | Ghi Reconstructed from N reviews, no direct read; không tự nhận đọc sách |
| 2. Luận đề | Mệnh đề có thể tranh luận; test ai có thể không đồng ý; lời tựa/kết; phân biệt luận đề tuyên bố/chứng minh | Dựa trên decision có evidence; nếu hai cách hiểu, trình bày cả hai; provisional khi thiếu |
| 3. Ý chính | 3-5 ý, xếp hạng; mỗi ý tiêu đề, 2-3 câu, bằng chứng cụ thể, foundational/derived, primary/secondary | Dùng core idea; thiếu thì ít hơn 3 với lý do, không bịa đồng thuận; ghi bằng chứng theo R# |
| 4. Trích dẫn | 3-5 câu ngắn diễn đạt luận đề, ý chính, hoặc đáng nhớ; chú giải và vị trí | Thiếu thì ghi nguồn không đủ; lời reviewer không trở thành lời tác giả vì hai người cùng thuật |
| 5. Phương pháp | Empirical/narrative/logical/authority; sample size, replication, correlation/causation; premises; >=1 hạn chế | Nêu reviewer phê bình; không suy cỡ mẫu; Subsequent Evidence Update nếu kiểm chứng được |
| 6. Liên hệ | >=1 đồng thuận, >=1 phản bác, >=1 lĩnh vực lân cận; foundational/derivative/applied và reading order | Reviewer nhắc hay [mở rộng] phải phân biệt; thiếu bằng chứng phản bác thì nêu gap |
| 7. Ứng dụng | Ý -> domain -> hành vi có thể kiểm; >=1 trong 7 ngày; nơi không đồng ý | Dùng action và kết quả QA vòng 3, giữ nhãn phần ứng dụng của agent |
| 8. Tổng hợp | 600-1000 từ; bốn tự kiểm, gaps, lịch +1/+4/+12/+30, bước tiếp | Tự kiểm: nói luận đề, nhớ 3 ý, ví dụ áp dụng, chỉ điểm yếu; Anki là bước tùy chọn |

Thang evidence: Strong = nhiều đường bằng chứng độc lập hội tụ; Moderate = một
nghiên cứu mạnh hoặc nhiều đường yếu; Weak = giai thoại/khẳng định chưa kiểm.
Số review không phải số nghiên cứu độc lập. Với nguồn review chưa đủ để đánh giá
method, ghi "nguồn không đủ" thay vì đánh giá mạnh chỉ do nhiều người đồng ý.
Survivorship check xem cả ví dụ thành công lẫn trường hợp thất bại; không dùng N/A
để né kiểm tra sách kinh doanh/self-help. Ngoại lệ và qualifier cần được giữ.

## Mười quy tắc upstream và bốn điều chỉnh

R1 luận đề là mệnh đề. R2 <=5 ý. R3 mỗi quote có chú giải. R4 ứng dụng cụ thể + hạn.
R5 không làm phẳng method. R6 survivorship bias. R7 Source Quality. R8 phản bác trong
liên hệ. R9 tự kiểm bắt buộc. R10 dịch giả hoặc chưa rõ.
R11 mỗi phát biểu factual ở 1-3 có locator. R12 lời một reviewer phải ghi qua reviewer,
không gán nguyên văn tác giả. R13 dịch máy <=70, không quote. R14 lỗi nguồn vào 8.9.

## Bảy edge case

1. Chưa đọc hết: Thesis (provisional), chỉ nói phần thực có.
2. Tuyển tập: Organizing Principle, không ép thành một luận đề.
3. Đồng ý hoàn toàn: hỏi điều gì bác bỏ được, điều kiện thất bại, giải thích thay thế.
4. Bằng chứng cũ: Subsequent Evidence Update dùng nguồn sơ cấp mới, hoặc ghi chưa kiểm.
5. Tiểu thuyết: chuyển phân tích chủ đề, không chạy khung luận đề phi hư cấu.
6. Giáo khoa: Core Conceptual Framework, Foundational Concepts, Prerequisites and Builds Toward.
7. Ghét sách: steel-man tác giả nhận ra được trước khi phản bác.

Thêm: tất cả dịch máy thì hạ chất lượng; reviewer mâu thuẫn thì giữ hai bên và Q;
audiobook lọt vào review phải xác minh trước khi phân loại lại, giữ ceiling transcript.
