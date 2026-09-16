# Tri thức — Voice 010 — câu hỏi nghiên cứu, đánh giá deepfake và giải thích adaptive routing

## Raw Inbox

[Transcript đầy đủ](voice-010_TRANSCRIPT.md) · [Báo cáo chất lượng](_work/voice-010/quality_report.md)

Nguồn là hội thoại được ASR nhận dạng và chưa nghe duyệt. Confidence dưới đây phản ánh mức chắc chắn của diễn giải từ văn bản, không chứng minh lời nói đúng về mặt thực tế.

## Knowledge Nodes

<a id="N1"></a>
### N1 — Đặt câu hỏi trước khi chọn kỹ thuật

- **Câu hỏi tổng hợp:** Một bài tổng quan hoặc đề xuất mô hình cần dẫn đến điều gì?
- **Cốt lõi:** Câu hỏi nghiên cứu cụ thể và cấu hình có thể kiểm tra; giải thích lý do dùng phương pháp thay vì chỉ liệt kê chúng.
- **Ví dụ/ngữ cảnh:** Phần đầu bàn tổng quan phương pháp giải thích và yêu cầu báo cáo cấu hình thực nghiệm.
- **Điều kiện áp dụng:** Các tên SHAP/LIME/Grad-CAM có nhiều lỗi ASR; không dùng đoạn này như hướng dẫn kỹ thuật chính xác.
- **Liên kết:** C1, C2; Voice 009 N1 về giữ đúng bài toán; Voice 018 N1 về diễn đạt đầu ra và lợi ích.

<a id="N2"></a>
### N2 — Đánh giá khả năng khái quát và ổn định

- **Câu hỏi tổng hợp:** Một kết quả tốt cần được thử thách như thế nào?
- **Cốt lõi:** Kiểm trên dữ liệu chưa thấy, chạy lại với điều kiện được ghi rõ và xem phân bố kết quả thay vì chọn một lần cao nhất.
- **Ví dụ/ngữ cảnh:** Báo cáo deepfake có thử nghiệm liên tập và một cấu hình giảm tham số mất ổn định khi chạy lại.
- **Điều kiện áp dụng:** Chưa kiểm các số AUC/ACC, cách chia dữ liệu và seed; không xác nhận SOTA hay nguyên nhân suy giảm.
- **Liên kết:** C3, C4; Voice 011 N2/N3 về tái lập và các lần chạy độc lập.

<a id="N3"></a>
### N3 — Giải thích kết quả âm và cơ chế định tuyến

- **Câu hỏi tổng hợp:** Nếu thêm nhánh hoặc routing chưa tốt hơn thì cần làm gì?
- **Cốt lõi:** Báo cáo kết quả, phân tích ảnh hưởng và logic chọn đặc trưng/nhánh. Mô hình dự báo tham số là một giả thuyết cần thử, không phải bảo đảm kết hợp sẽ tốt hơn.
- **Ví dụ/ngữ cảnh:** Người trình bày và người góp ý thảo luận khác nhau về lợi ích hai nhánh và cách điều chỉnh tham số.
- **Điều kiện áp dụng:** Lời tin rằng kết hợp luôn có lợi không được xem là kết luận khoa học. Ký hiệu tham số và routing mềm/cứng cần đối chiếu sơ đồ.
- **Liên kết:** C5, C6, C7; Voice 012 N2 về ablation; bản thầy Lâm N4 về ổn định baseline.

<a id="N4"></a>
### N4 — Phân biệt khác cấu trúc với đóng góp đã xác nhận

- **Câu hỏi tổng hợp:** Có thể coi một nhánh mô hình là hoàn toàn mới chỉ từ lời báo cáo không?
- **Cốt lõi:** Chưa: phải mô tả khác biệt với công trình liên quan và so sánh trong điều kiện tương thích; cuộc trao đổi vẫn đang chất vấn điều này.
- **Ví dụ/ngữ cảnh:** Có lời khẳng định mới, sau đó xuất hiện một mô hình liên quan cũng dùng thông tin thời gian.
- **Điều kiện áp dụng:** Không xác nhận tính mới, xếp hạng tạp chí hay khả năng được chấp nhận; tên bài báo trong ASR chưa chắc.
- **Liên kết:** C8, C5; Voice 011 N4 về giới hạn tuyên bố; Voice 013 N1 về phản hồi phản biện.

## Claim Ledger

| ID | Nội dung được diễn giải | Bằng chứng | Confidence | Kiểm chứng |
|---|---|---|---|---|
| C1 | Phần mở đầu yêu cầu đưa tham số chạy và máy sử dụng vào báo cáo để người đọc kiểm tra được cấu hình. (người nói chưa xác định) | [00:01:16](voice-010_TRANSCRIPT.md#S00009): «Tham số mình chạy là gì, máy mình chạy là gì mình đưa ra cho báo cáo» | vừa: Có lời trực tiếp trong văn bản; chưa nghe duyệt hoặc kiểm chứng bên ngoài. | chưa kiểm chứng |
| C2 | Góp ý về tổng quan nhấn mạnh đặt câu hỏi nghiên cứu; tìm lời giải hoặc ghép phương pháp chưa đủ nếu chưa rõ vấn đề cần trả lời. (người nói chưa xác định) | [00:12:33](voice-010_TRANSCRIPT.md#S00103): «Quan trọng nhất là nghiên cứu là ta phải đặt ra câu hỏi nghiên cứu»; [00:15:21](voice-010_TRANSCRIPT.md#S00140): «Làm nghiên cứu không chỉ là lời giải mà nó còn biết cách đặt câu hỏi» | vừa: Có lời trực tiếp trong văn bản; chưa nghe duyệt hoặc kiểm chứng bên ngoài. | chưa kiểm chứng |
| C3 | Trong báo cáo deepfake, người trình bày nhấn mạnh đánh giá trên bộ dữ liệu chưa thấy, thay vì chỉ theo đuổi chênh lệch nhỏ trong nội tập. (người nói chưa xác định) | [00:37:32](voice-010_TRANSCRIPT.md#S00403): «Quan trọng là test ở những cái bộ dữ liệu mà chưa nhìn thấy» | vừa: Có lời trực tiếp trong văn bản; chưa nghe duyệt hoặc kiểm chứng bên ngoài. | chưa kiểm chứng |
| C4 | Một cấu hình giảm tham số cho kết quả cao ở lần đầu nhưng giảm mạnh ở các lần thử sau; người trình bày coi lần đầu là may mắn và cần xét độ ổn định. (người nói chưa xác định) | [00:43:39](voice-010_TRANSCRIPT.md#S00465): «Tuy nhiên là sau đấy thì em thử lại vài lần nữa»; [00:43:49](voice-010_TRANSCRIPT.md#S00468): «Cái AUC nó không còn được như thế này»; [00:43:55](voice-010_TRANSCRIPT.md#S00470): «Nên là cái này nó chỉ là 1 cái lần thử may mắn» | vừa: Có lời trực tiếp trong văn bản; chưa nghe duyệt hoặc kiểm chứng bên ngoài. | chưa kiểm chứng |
| C5 | Góp ý chỉ ra báo cáo thiếu phân tích ảnh hưởng và giải thích vì sao kết quả thay đổi; kết quả cao không thay thế những phần đó. (người nói chưa xác định) | [00:57:44](voice-010_TRANSCRIPT.md#S00636): «Cái vấn đề của Tuấn nhất là vấn đề giải thích»; [00:58:04](voice-010_TRANSCRIPT.md#S00641): «Thì thấy là nó không có những cái phân tích ảnh hưởng»; [00:58:15](voice-010_TRANSCRIPT.md#S00644): «Rồi tại sao nó lại như thế thì gần như là không giải thích» | vừa: Có lời trực tiếp trong văn bản; chưa nghe duyệt hoặc kiểm chứng bên ngoài. | chưa kiểm chứng |
| C6 | Khi adaptive chưa tốt hơn, vẫn cần báo cáo kết quả này; đây là một phần của quá trình lập luận trong luận án. (người nói chưa xác định) | [01:10:24](voice-010_TRANSCRIPT.md#S00795): «còn nếu sử dụng nó không tốt hơn»; [01:10:26](voice-010_TRANSCRIPT.md#S00796): «thì quản án mình vẫn phải report nó» | vừa: Có lời trực tiếp trong văn bản; chưa nghe duyệt hoặc kiểm chứng bên ngoài. | chưa kiểm chứng |
| C7 | Để xây routing có căn cứ, cần giải thích logic chọn tham số/đặc trưng và thử mô hình dự báo tham số từ video; đây là đề xuất, chưa phải kết quả đã đạt. (người nói chưa xác định) | [01:22:39](voice-010_TRANSCRIPT.md#S00889): «Nhưng mà mình phải có cái logic của chọn tham số, chọn đặc trưng nó như thế nào»; [01:25:40](voice-010_TRANSCRIPT.md#S00919): «Thì em hãy đưa ra một mô hình dự báo, đầu vào nó là cái video, đầu ra nó là giá trị tàu» | thấp: Lời đề xuất tương đối rõ nhưng ký hiệu tau/T bị ASR viết thành tàu/tao; cần nghe và xem sơ đồ để xác định đại lượng chính xác. | chưa kiểm chứng |
| C8 | Tính mới của nhánh thời gian vẫn cần đối chiếu công trình liên quan: cuộc nói chuyện có cả khẳng định chưa ai làm và chỉ ra đã có cách làm khác. (người nói chưa xác định) | [00:52:39](voice-010_TRANSCRIPT.md#S00594): «Đấy, và đây là Tuấn đã khẳng định là chưa từng ai làm như này cả»; [01:06:06](voice-010_TRANSCRIPT.md#S00726): «Không, có người làm rồi nhưng mà khác à.»; [01:06:08](voice-010_TRANSCRIPT.md#S00727): «Khác thế nào?» | vừa: Có lời trực tiếp trong văn bản; chưa nghe duyệt hoặc kiểm chứng bên ngoài. | chưa kiểm chứng |

## Câu hỏi mở và giới hạn

- Cần slide gốc để xác định tau/T là số frame, ngưỡng định tuyến hay tham số khác và tách routing mềm/cứng.
- AUC/ACC, số frame/video, số tham số và tên bộ DFDC/Celeb-DF/FaceForensics bị ASR ghi nhiều biến thể; chưa dùng làm bảng kết quả chuẩn.
- Phát biểu chọn/bỏ một phương pháp deepfake và các lời giải thích do độ phủ dữ liệu chỉ là lời báo cáo; cần kiểm mã chia tập và thử nghiệm.
- Lịch nộp bài, tên hội thảo, ngày tháng và hạng tạp chí có nhiều lỗi ASR; không tạo deadline thật từ các đoạn này.
- Phần cuối chuyển sang tin giả tiếng Việt và dừng giữa kiến trúc; không đủ để đánh giá kết quả hoặc kết luận của đề tài đó.
- Không gán mọi góp ý trong buổi cho cùng một người hoặc cùng luận văn.

## Practice Log — đề xuất của trợ lý

- [ ] Viết một câu hỏi nghiên cứu có phép đo và mô tả cấu hình tái lập được.
- [ ] Tạo bảng nội tập/liên tập và nhiều lần chạy, kèm ablation, độ phân tán và cả kết quả không cải thiện.
- [ ] Vẽ routing mềm/cứng đúng mã, ghi giả thuyết tác dụng của từng đặc trưng trước khi chọn mô hình dự báo tham số.

## Lịch ôn đề xuất

2026-09-10, 2026-09-13, 2026-09-21, 2026-10-09
