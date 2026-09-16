# Tri thức — Recording (2) — báo cáo nghiên cứu, giới hạn phép đánh giá và góp ý về bài báo

## Raw Inbox

[Transcript đầy đủ](../../recording-2_TRANSCRIPT.md) · [Báo cáo chất lượng](../../_work/recording-2/quality_report.md)

Nguồn là hội thoại được ASR nhận dạng và chưa nghe duyệt. Confidence dưới đây phản ánh mức chắc chắn của diễn giải từ văn bản, không chứng minh lời nói đúng về mặt thực tế.

## Knowledge Nodes

<a id="N1"></a>
### N1 — Kiểm dữ liệu sinh và tính độc lập của phép đo

- **Câu hỏi tổng hợp:** Cần kiểm tra gì trước khi dùng kết quả sinh dữ liệu làm bằng chứng?
- **Cốt lõi:** Làm rõ điểm thưởng có trùng với tiêu chí đánh giá hay không, kiểm mẫu trùng và lưu đầu ra từng lần chạy để có thể đối chiếu.
- **Ví dụ/ngữ cảnh:** Đây là tổng hợp hai phần báo cáo kế tiếp; chưa xác nhận chúng cùng đề tài hoặc cùng người trình bày.
- **Điều kiện áp dụng:** Chưa xác minh mã, CSV, công thức chỉ số hoặc tính đúng của kết quả; các thuật ngữ bị ASR làm sai cần nghe lại.
- **Liên kết:** C1, C2, C3; Voice 018 N2 về tiêu chí đánh giá; Voice 009 N4 về lưu minh chứng.

<a id="N2"></a>
### N2 — Đưa đúng bài toán vào tiêu đề và phép thử

- **Câu hỏi tổng hợp:** Làm sao thể hiện đóng góp về dữ liệu chưa thấy?
- **Cốt lõi:** Nêu rõ bài toán khái quát sang dữ liệu khác trong tiêu đề và nội dung, đồng thời gắn nó với thiết kế đánh giá phù hợp.
- **Ví dụ/ngữ cảnh:** Phần báo cáo deepfake và góp ý về tiêu đề chưa làm nổi bật trọng tâm.
- **Điều kiện áp dụng:** Không xác nhận mô hình hơn SOTA; chưa kiểm split, bảng số liệu và tên bộ dữ liệu.
- **Liên kết:** C4, C5; Voice 010 N2/N4 về liên tập và tính mới.

<a id="N3"></a>
### N3 — Hiểu mô hình và cập nhật căn cứ so sánh

- **Câu hỏi tổng hợp:** Điều gì cần làm trước khi kết luận hướng cải tiến có đóng góp?
- **Cốt lõi:** Nắm rõ cơ chế mô hình và khảo sát công trình mới sát thời điểm viết để xác định vấn đề còn lại.
- **Ví dụ/ngữ cảnh:** Góp ý cho các báo cáo cuối buổi, gồm tin giả tiếng Việt và sinh dữ liệu.
- **Điều kiện áp dụng:** Mốc tháng/năm là lời nói trong bản ghi, không tự chuyển thành deadline hiện tại; chưa tìm hay kiểm các bài báo được nhắc.
- **Liên kết:** C6, C7; Voice 010 N1 về câu hỏi nghiên cứu; Voice 018 N3 về hiểu hệ thống trước khi sửa.

## Claim Ledger

| ID | Nội dung được diễn giải | Bằng chứng | Confidence | Kiểm chứng |
|---|---|---|---|---|
| C1 | Trong báo cáo sinh dữ liệu SQL, người trình bày nêu vấn đề ở điểm thưởng: mô hình có xu hướng học các thành phần để được điểm cao; cần làm rõ quan hệ giữa điểm thưởng và phép đánh giá. (người nói chưa xác định) | [00:35:36](../../recording-2_TRANSCRIPT.md#S00331): «Thì các thầy hội đồng cũng đã nhận ra là em có một vấn đề khá lớn với phần điểm thưởng ạ»; [00:35:57](../../recording-2_TRANSCRIPT.md#S00341): «học những cái thành phần để điểm cao» | thấp: Lời nói về điểm thưởng và học lấy điểm khá rõ, nhưng câu giải thích hai hàm bị ASR lặp; cần mã và nghe lại để kết luận chính xác. | chưa kiểm chứng |
| C2 | Một báo cáo tiếp theo mô tả yêu cầu kiểm tra trùng lặp ở dữ liệu sinh và loại mẫu trùng trước khi tính chỉ số; tên mô hình và công thức trong ASR chưa đủ rõ. (người nói chưa xác định) | [00:39:04](../../recording-2_TRANSCRIPT.md#S00353): «và cũng kiểm tra xem độ trùng lọc của các mẫu hoạt động sinh ra bởi mô hình»; [00:39:09](../../recording-2_TRANSCRIPT.md#S00354): «đồng thời sẽ tính loại bỏ những mẫu hoạt động trùng lọc» | thấp: Ý loại trùng có lời trực tiếp; thuật ngữ, đối tượng và tên chỉ số xung quanh bị lỗi nhận dạng. | chưa kiểm chứng |
| C3 | Người trình bày nói đã lưu các file CSV của lần chạy đầu làm bằng chứng và đang kiểm tra lại; chưa coi lời báo cáo này là xác nhận độc lập về chất lượng dữ liệu. (người nói chưa xác định) | [00:42:03](../../recording-2_TRANSCRIPT.md#S00381): «Hiện tại thì với lần 1 thì những kết quả này của em thì em đã có tất cả các file CSV sinh ra» | vừa: Có lời trực tiếp trong văn bản; chưa nghe duyệt hoặc kiểm chứng bên ngoài. | chưa kiểm chứng |
| C4 | Phần deepfake nhấn mạnh đánh giá trên dữ liệu khác hoặc chưa nhìn thấy; đây là trọng tâm cần được thể hiện nhất quán trong bài báo. (người nói chưa xác định) | [01:20:47](../../recording-2_TRANSCRIPT.md#S00758): «Và nó chủ yếu là so sánh đối với các huấn luyện ở trên tập dữ liệu tầng và kiểm tưởng trên tập dữ liệu khác.»; [01:27:35](../../recording-2_TRANSCRIPT.md#S00820): «đánh giá trên một dữ liệu khác, một dữ liệu chưa nhìn thấy» | vừa: Có lời trực tiếp trong văn bản; chưa nghe duyệt hoặc kiểm chứng bên ngoài. | chưa kiểm chứng |
| C5 | Người trình bày đồng ý sửa tiêu đề vì trọng tâm đã có trong nội dung nhưng chưa được nêu rõ ở tiêu đề. (người nói chưa xác định) | [01:27:18](../../recording-2_TRANSCRIPT.md#S00819): «Nhưng mà trong cái phần tiêu đề chưa đẩy, thì anh sẽ phải sửa lại cái phần tiêu đề.» | vừa: Có lời trực tiếp trong văn bản; chưa nghe duyệt hoặc kiểm chứng bên ngoài. | chưa kiểm chứng |
| C6 | Góp ý yêu cầu khảo sát công trình mới sát thời điểm viết, thay vì chỉ so sánh với tài liệu cũ hoặc với bài tạo ra bộ dữ liệu. (người nói chưa xác định) | [01:33:48](../../recording-2_TRANSCRIPT.md#S00860): «Trong tất cả những công trình, nếu game vào năm 2026 thì em phải thảo sát đến tận tháng 9 2026.»; [01:36:26](../../recording-2_TRANSCRIPT.md#S00888): «Vì năm nay 26 mà em không so sánh với những cái công trình 6 tháng trở về trước, năm 1 năm trước thì không ai tìm.» | vừa: Có lời trực tiếp trong văn bản; chưa nghe duyệt hoặc kiểm chứng bên ngoài. | chưa kiểm chứng |
| C7 | Phần góp ý cuối vẫn yêu cầu người làm hiểu mô hình trước khi chọn cách cải thiện. (người nói chưa xác định) | [01:40:08](../../recording-2_TRANSCRIPT.md#S00908): «Thầy có nhiều cách cải thiện nó, nhưng mà thầy muốn em phải hiểu về nó.» | vừa: Có lời trực tiếp trong văn bản; chưa nghe duyệt hoặc kiểm chứng bên ngoài. | chưa kiểm chứng |

## Câu hỏi mở và giới hạn

- Nguồn có rất nhiều lỗi ASR và đoạn lặp; cần nghe trước khi trích trực tiếp thuật ngữ hoặc dùng số liệu. Hai kênh giống nhau ở hai mẫu đo không chứng minh lời nói rõ trên toàn file.
- Phần đầu chưa xác định chắc tên phương pháp, dữ liệu và chỉ số; không dựng kiến thức kỹ thuật từ các câu méo nghĩa.
- Các thứ tự nhóm payload tốt/kém có thể khác Voice 012/013/018; cần phiên bản thí nghiệm và bảng gốc, không tự hòa giải bằng đổi tên nhóm.
- S00370 ghi 'true positive càng thấp càng tốt' nhưng ngữ cảnh chỉ số bị lỗi; chưa thể coi là định nghĩa chuẩn.
- Chuyện tổ chức, thuế, sản phẩm, bản quyền và cá nhân giữa buổi là trao đổi chưa xác minh; không biến thành tư vấn pháp lý, tài chính hay kết luận về người được nhắc.
- Tên hội thảo và hạn nộp xuất hiện nhiều biến thể; chưa có căn cứ tạo lịch nộp bài.

## Practice Log — đề xuất của trợ lý

- [ ] Đối chiếu hàm thưởng, hàm đánh giá và dữ liệu dùng cho chúng; lưu mẫu sinh và kết quả loại trùng theo từng lần chạy.
- [ ] Viết lại một câu nêu vấn đề khái quát sang dữ liệu chưa thấy, rồi kiểm tiêu đề, tóm tắt và bảng thí nghiệm có cùng trọng tâm.
- [ ] Cập nhật bảng nghiên cứu liên quan từ tài liệu gốc và ghi rõ khác biệt cơ chế, dữ liệu, phép đo; nghe xác nhận các claim cần dùng.

## Lịch ôn đề xuất

2026-09-10, 2026-09-13, 2026-09-21, 2026-10-09
