# Tri thức — Voice 011 — nhiều đề tài nghiên cứu và yêu cầu giải thích, tái lập thực nghiệm

## Raw Inbox

[Transcript đầy đủ](../../voice-011_TRANSCRIPT.md) · [Báo cáo chất lượng](../../_work/voice-011/quality_report.md)

Nguồn là hội thoại được ASR nhận dạng và chưa nghe duyệt. Confidence dưới đây phản ánh mức chắc chắn của diễn giải từ văn bản, không chứng minh lời nói đúng về mặt thực tế.

## Knowledge Nodes

<a id="N1"></a>
### N1 — Giải thích đóng góp theo bài toán và cơ chế

- **Câu hỏi tổng hợp:** Làm sao để mô hình không chỉ trông như ghép các khối có sẵn?
- **Cốt lõi:** Làm rõ khoảng trống của bài toán/ngôn ngữ và logic từng thành phần quan trọng; nối sơ đồ với lập luận và kết quả.
- **Ví dụ/ngữ cảnh:** Phần đầu phản biện báo cáo fake news tiếng Việt và các khối multi-scale/fusion.
- **Điều kiện áp dụng:** Không áp nguyên cấu trúc mô hình này sang đề tài khác; cần đọc công trình thật để biết khác biệt ngôn ngữ.
- **Liên kết:** C1, C2; Liên hệ góp ý slide trong Voice 009.

<a id="N2"></a>
### N2 — Tái lập trước khi đánh giá cải tiến

- **Câu hỏi tổng hợp:** Cần kiểm tra gì khi kết quả chạy lại khác bài gốc?
- **Cốt lõi:** Đối chiếu cấu hình trước và đánh giá cải tiến trên các tập được chọn, có tiêu chí tổng hợp rõ; không lấy việc tốt hơn một tập để kết luận tốt hơn toàn bộ.
- **Ví dụ/ngữ cảnh:** Báo cáo thử nghiệm âm thanh thay cấu hình, codec, encoder và nhánh tần số.
- **Điều kiện áp dụng:** Các số liệu trong audio chưa xác minh; bảng log và cấu hình của nghiên cứu mới là nguồn để so sánh.
- **Liên kết:** C3, C8; Kết hợp N3 về thí nghiệm có kiểm soát.

<a id="N3"></a>
### N3 — Ablation và độc lập của lần chạy

- **Câu hỏi tổng hợp:** Bằng chứng nào hỗ trợ lựa chọn thành phần và độ ổn định?
- **Cốt lõi:** Thiết kế ablation cho các thành phần/tham số được hỏi và báo seed thực tế; không gọi các lần giữ nguyên seed là các thí nghiệm độc lập chỉ vì đã chạy lại.
- **Ví dụ/ngữ cảnh:** Phần trả lời reviewer của bài âm thanh.
- **Điều kiện áp dụng:** Định nghĩa biến được thay, cấu hình giữ nguyên, cách chọn checkpoint và các seed; không suy từ bản ghi một quy trình thống kê hoàn chỉnh.
- **Liên kết:** C4, C6; Liên hệ ma trận thí nghiệm ở Voice 009.

<a id="N4"></a>
### N4 — Tách chọn tham số khỏi đánh giá cuối và giữ đúng mức tuyên bố

- **Câu hỏi tổng hợp:** Cần sửa gì khi reviewer nghi ngờ phép so sánh?
- **Cốt lõi:** Đối chiếu việc chọn tham số với tập phát triển/đánh giá, kiểm tra nguồn số liệu so sánh và điều chỉnh tuyên bố SOTA về đúng bằng chứng.
- **Ví dụ/ngữ cảnh:** Review nêu chọn lớp/siêu tham số và một kết quả cạnh tranh tốt hơn.
- **Điều kiện áp dụng:** Hai claim có confidence thấp vì tên tập và một số câu bị ASR làm méo; cần review gốc trước khi áp dụng chi tiết.
- **Liên kết:** C5, C7; N2 về tiêu chí so sánh nhiều tập.

## Claim Ledger

| ID | Nội dung được diễn giải | Bằng chứng | Confidence | Kiểm chứng |
|---|---|---|---|---|
| C1 | Phần nghiên cứu fake news tiếng Việt cần đặt trong bối cảnh công trình chung và giải thích khác biệt so với tiếng Anh, không chỉ nêu việc huấn luyện bằng dữ liệu tiếng Việt. (người nói chưa xác định) | [00:00:02](../../voice-011_TRANSCRIPT.md#S00001): «Đầu tiên em phải nói về các khu vực phát hiện fake news nói chung»; [00:00:14](../../voice-011_TRANSCRIPT.md#S00004): «giữa phát hiện fake news tiếng Việt với tiếng Anh có gì khác nhau»; [00:02:12](../../voice-011_TRANSCRIPT.md#S00021): «Người ta làm cái gì để mà tạo ra sự khác biệt?» | vừa: Có lời trực tiếp trong văn bản; chưa nghe duyệt hoặc kiểm chứng bên ngoài. | chưa kiểm chứng |
| C2 | Sơ đồ mô hình phải đi kèm giải thích logic, vai trò multi-scale/fusion và lý do hai nhánh; có sơ đồ lắp ghép chưa đủ chứng minh hiểu phương pháp. (người nói chưa xác định) | [00:05:50](../../voice-011_TRANSCRIPT.md#S00065): «mình phải nói rõ được cái logic đó là cái gì»; [00:05:55](../../voice-011_TRANSCRIPT.md#S00067): «ý nghĩa của những cái multi-scale»; [00:07:49](../../voice-011_TRANSCRIPT.md#S00081): «Tại sao lại là 2 nhánh fusion?» | vừa: Có lời trực tiếp trong văn bản; chưa nghe duyệt hoặc kiểm chứng bên ngoài. | chưa kiểm chứng |
| C3 | Trong phần âm thanh, mục tiêu được bàn là cải thiện kết quả tổng hợp trên hai tập dữ liệu, tránh chỉ tối ưu một tập; chỉ số và cách tổng hợp cần được định nghĩa rõ. (người nói chưa xác định) | [00:20:25](../../voice-011_TRANSCRIPT.md#S00194): «cho cộng trung bình hai cái data set này là tốt nhất»; [00:20:28](../../voice-011_TRANSCRIPT.md#S00195): «Chứ không chỉ là một bộ data set» | vừa: Có lời trực tiếp trong văn bản; chưa nghe duyệt hoặc kiểm chứng bên ngoài. | chưa kiểm chứng |
| C4 | Việc giải thích lựa chọn tham số và codec được gắn với yêu cầu làm ablation study thay vì chỉ khẳng định bằng lý thuyết. (người nói chưa xác định) | [00:29:10](../../voice-011_TRANSCRIPT.md#S00314): «tại sao lại chọn các tham số này»; [00:29:14](../../voice-011_TRANSCRIPT.md#S00315): «chạy Appliation Study»; [00:29:25](../../voice-011_TRANSCRIPT.md#S00320): «Codec này thì mình cũng phải chạy Appliation Study thôi» | vừa: Có lời trực tiếp trong văn bản; chưa nghe duyệt hoặc kiểm chứng bên ngoài. | chưa kiểm chứng |
| C5 | Một góp ý phản biện yêu cầu không chọn tham số bằng tập đánh giá cuối, mà dùng tập phát triển; tên tập và lớp cụ thể trong ASR cần nghe lại. (người nói chưa xác định) | [00:30:23](../../voice-011_TRANSCRIPT.md#S00328): «không được chọn cái chỉ số»; [00:30:36](../../voice-011_TRANSCRIPT.md#S00330): «trên tập đầy giá mà phải chạy trên tập Depth» | thấp: Ý phân tách tập được nhắc nhưng ASR làm méo tên tập/thuật ngữ; cần nghe và đối chiếu review gốc. | chưa kiểm chứng |
| C6 | Báo cáo ba lần chạy là độc lập bị chất vấn vì vẫn cố định cùng random seed; trao đổi thừa nhận cần khác seed để hỗ trợ tuyên bố này. (người nói chưa xác định) | [00:34:23](../../voice-011_TRANSCRIPT.md#S00365): «mình đã chạy trên 3 lần chạy độc lập»; [00:34:30](../../voice-011_TRANSCRIPT.md#S00366): «mình lại cố định cái random seed»; [00:34:39](../../voice-011_TRANSCRIPT.md#S00368): «Đúng rồi, phải khác nhau chứ.» | vừa: Có lời trực tiếp trong văn bản; chưa nghe duyệt hoặc kiểm chứng bên ngoài. | chưa kiểm chứng |
| C7 | Khi tuyên bố SOTA bị đối chiếu với kết quả tốt hơn, hướng xử lý được trao đổi là bỏ/giảm tuyên bố và giải thích trung thực tiêu chí so sánh. (người nói chưa xác định) | [00:31:04](../../voice-011_TRANSCRIPT.md#S00334): «mình nhận SOTA nó cũng chưa đúng»; [00:31:25](../../voice-011_TRANSCRIPT.md#S00338): «không nhận SOTA nữa đoạn này» | thấp: Ý sửa tuyên bố rõ; các tên công trình, trị số và câu ASR quanh đó chưa chắc chắn. | chưa kiểm chứng |
| C8 | Người báo cáo cho biết kiểm tra khác biệt cấu hình với tác giả và sửa cấu hình đã cải thiện kết quả tái lập, nhưng chưa chứng minh tái lập được mức công bố. (người nói chưa xác định) | [00:13:40](../../voice-011_TRANSCRIPT.md#S00126): «cấu hình của tác giả»; [00:14:16](../../voice-011_TRANSCRIPT.md#S00130): «em có sửa lại các cái cấu hình trên thế thì kết quả em ra được tốt hơn» | vừa: Có lời trực tiếp trong văn bản; chưa nghe duyệt hoặc kiểm chứng bên ngoài. | chưa kiểm chứng |

## Câu hỏi mở và giới hạn

- Tên mô hình, pretrained encoder, loss, tập LA/DF và các trị số cần đối chiếu slide hoặc bài gốc; không dùng transcript làm bảng benchmark.
- Phần fake news nhắc mô hình tiếng Việt nhưng tên bị nhận dạng méo; cần nghe trước khi điền tên cụ thể.
- Phần cuối về bypass và mẫu sinh thuộc một đề tài khác, quá nhiều đoạn chưa rõ để rút kết luận kỹ thuật.
- Các câu đăng ký kênh/kết thúc video ở khoảng 35:01 và 39:45 có dấu hiệu hallucination; chưa có nghe xác nhận.

## Practice Log — đề xuất của trợ lý

- [ ] Tạo bảng đối chiếu cấu hình bài gốc và lần tái lập: dữ liệu, learning rate, batch size, checkpoint, seed và augmentation.
- [ ] Lập ma trận câu hỏi reviewer → thí nghiệm/nguồn chứng minh → thay đổi trong bài; phân biệt kết quả đã có và cần chạy.
- [ ] Rà mọi tuyên bố tốt nhất/SOTA cùng bảng so sánh, tên tập và quy trình chọn tham số trước khi sửa bản thảo.

## Lịch ôn đề xuất

2026-09-10, 2026-09-13, 2026-09-21, 2026-10-09
