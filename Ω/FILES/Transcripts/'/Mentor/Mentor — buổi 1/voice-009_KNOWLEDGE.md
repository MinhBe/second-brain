# Tri thức — Voice 009 — góp ý báo cáo GAN, lựa chọn thí nghiệm và minh chứng trên slide

## Raw Inbox

[Transcript đầy đủ](voice-009_TRANSCRIPT.md) · [Báo cáo chất lượng](_work/voice-009/quality_report.md)

Nguồn là hội thoại được ASR nhận dạng và chưa nghe duyệt. Confidence dưới đây phản ánh mức chắc chắn của diễn giải từ văn bản, không chứng minh lời nói đúng về mặt thực tế.

## Knowledge Nodes

<a id="N1"></a>
### N1 — Giữ nhất quán giữa đề cương và câu chuyện nghiên cứu

- **Câu hỏi tổng hợp:** Mở đầu báo cáo cần giúp người nghe hiểu điều gì?
- **Cốt lõi:** Nêu đúng mục tiêu đã đăng ký và nối nó với bài toán, dữ liệu, đặc trưng; không để cách diễn đạt khiến trọng tâm GAN biến thành một việc khác.
- **Ví dụ/ngữ cảnh:** Người trình bày được yêu cầu sửa mục tiêu cho khớp tên đề tài và đề cương.
- **Điều kiện áp dụng:** Đối chiếu văn bản đề cương thật; bản ghi không chứa toàn bộ đề cương.
- **Liên kết:** C1; Bản thầy Lâm N1 cũng nhấn mạnh vai trò bộ sinh và bộ phát hiện.

<a id="N2"></a>
### N2 — Làm slide đọc được và có ví dụ

- **Câu hỏi tổng hợp:** Làm sao để sơ đồ và dữ liệu giúp người nghe hiểu?
- **Cốt lõi:** Dùng bố trí sơ đồ quen thuộc, cỡ chữ đọc được, ví dụ ngắn và gạch đầu dòng giải thích lý do xử lý.
- **Ví dụ/ngữ cảnh:** Một số hình được chuyển từ tài liệu hoặc AI nên chữ nhỏ và thiếu giải thích.
- **Điều kiện áp dụng:** Kiểm tra trên thiết bị trình chiếu; không suy rằng một kiểu bố trí luôn đúng cho mọi sơ đồ.
- **Liên kết:** C2, C3; Liên hệ Voice 014 về giới hạn thời lượng.

<a id="N3"></a>
### N3 — Đưa bằng chứng thử nghiệm trước giải pháp cải tiến

- **Câu hỏi tổng hợp:** Thứ tự nào giúp người nghe thấy lý do nâng cấp mô hình?
- **Cốt lõi:** So sánh baseline trước, nhận xét vấn đề quan sát được, rồi mới nối mỗi vấn đề với hướng cải tiến.
- **Ví dụ/ngữ cảnh:** Báo cáo đang liệt kê nhiều thay đổi về tokenization, độ dài, pretraining và reward.
- **Điều kiện áp dụng:** Thông số và hiệu quả các thay đổi chưa được kiểm chứng từ audio; cần đối chiếu bảng thí nghiệm.
- **Liên kết:** C4; Bản thầy Lâm N4 về làm cơ bản chạy ổn trước.

<a id="N4"></a>
### N4 — Quản lý ma trận thí nghiệm và chọn minh chứng

- **Câu hỏi tổng hợp:** Trình bày nhiều kịch bản mà vẫn rõ ràng bằng cách nào?
- **Cốt lõi:** Chuẩn bị đầy đủ bảng kết quả, giải thích nhóm/mã kịch bản, rồi chọn các con số và ví dụ trực tiếp hỗ trợ nhận định trên slide.
- **Ví dụ/ngữ cảnh:** Có nhóm sáu kịch bản chọn dữ liệu và nhóm tám kịch bản thay đổi mô hình; báo cáo bỏ sót định nghĩa và bảng.
- **Điều kiện áp dụng:** Không coi các số sáu/tám/mười một là mâu thuẫn cùng một tập hợp khi chưa kiểm tra bảng gốc.
- **Liên kết:** C5, C6, C7; Bản thầy Lâm N2 về minh bạch dữ liệu và phép đo.

## Claim Ledger

| ID | Nội dung được diễn giải | Bằng chứng | Confidence | Kiểm chứng |
|---|---|---|---|---|
| C1 | Mục tiêu báo cáo phải khớp tên đề tài và đề cương; nội dung mở đầu cần làm rõ bài toán, dữ liệu và đặc trưng. (người nói chưa xác định) | [00:01:52](voice-009_TRANSCRIPT.md#S00027): «thế này nó phải thể hiện được tên đề tài»; [00:02:13](voice-009_TRANSCRIPT.md#S00033): «nó lại bị lệch nhau»; [00:02:54](voice-009_TRANSCRIPT.md#S00055): «Bài toán nó là cái gì, dữ liệu là cái gì, đặc trưng là gì» | vừa: Có lời trực tiếp trong văn bản; chưa nghe duyệt hoặc kiểm chứng bên ngoài. | chưa kiểm chứng |
| C2 | Phần trình bày về họ dữ liệu/tấn công cần có chuỗi ví dụ ngắn, và sơ đồ tiền xử lý cần kèm lý do thực hiện, không chỉ hình quy trình. (người nói chưa xác định) | [00:06:41](voice-009_TRANSCRIPT.md#S00108): «em luôn cho luôn cái chuỗi ví dụ ở đây»; [00:08:24](voice-009_TRANSCRIPT.md#S00139): «trước này là 1 ví dụ, trước này là gạch 1 số đầu dòng là lý do tại sao» | vừa: Có lời trực tiếp trong văn bản; chưa nghe duyệt hoặc kiểm chứng bên ngoài. | chưa kiểm chứng |
| C3 | Góp ý ưu tiên sơ đồ GAN theo cách bố trí quen thuộc từ trái sang phải và yêu cầu kiểm tra cỡ chữ; slide do AI sinh vẫn cần điều chỉnh để người ở xa đọc được. (người nói chưa xác định) | [00:13:46](voice-009_TRANSCRIPT.md#S00202): «Chạy từ trái sang phải.»; [00:14:41](voice-009_TRANSCRIPT.md#S00212): «nếu dùng AI sinh slide thì phải chú ý»; [00:14:46](voice-009_TRANSCRIPT.md#S00213): «Nó còn sinh bé xíu, tức là mình phải cố gắng nhìn và điều chỉnh» | vừa: Có lời trực tiếp trong văn bản; chưa nghe duyệt hoặc kiểm chứng bên ngoài. | chưa kiểm chứng |
| C4 | Nên trình bày thử nghiệm giữa các họ GAN và SMOTE trước, rồi mới nhận xét vấn đề và đề xuất cải tiến. (người nói chưa xác định) | [00:16:16](voice-009_TRANSCRIPT.md#S00230): «Và em sẽ trình bày luôn phần thử nghiệm»; [00:16:20](voice-009_TRANSCRIPT.md#S00231): «Thử nghiệm giữa các hộ gan với nhau»; [00:16:23](voice-009_TRANSCRIPT.md#S00232): «Và với SMOTE»; [00:16:25](voice-009_TRANSCRIPT.md#S00233): «Sau đó em sẽ đi sang phần nhận xét về vấn đề của nó và các cải tiến» | vừa: Có lời trực tiếp trong văn bản; chưa nghe duyệt hoặc kiểm chứng bên ngoài. | chưa kiểm chứng |
| C5 | Khi kết quả có nhiều bảng/kịch bản, góp ý là chuẩn bị đầy đủ trước rồi mới chọn nội dung trình bày; không dùng việc quá nhiều bảng để bỏ bước chuẩn bị số liệu. (người nói chưa xác định) | [00:28:02](voice-009_TRANSCRIPT.md#S00381): «nó sẽ có rất nhiều bảng»; [00:28:19](voice-009_TRANSCRIPT.md#S00384): «Trước mắt em chỉ phải đầy đủ hết đã, sau đó người ta quyết định chọn cái nào.» | vừa: Có lời trực tiếp trong văn bản; chưa nghe duyệt hoặc kiểm chứng bên ngoài. | chưa kiểm chứng |
| C6 | Kết quả đưa lên slide phải hỗ trợ quan điểm, đồng thời cần ví dụ đầu ra thực tế bên cạnh thống kê. (người nói chưa xác định) | [00:31:06](voice-009_TRANSCRIPT.md#S00422): «mình đưa lên cái gì nó phải hỗ trợ ra cái quan điểm của mình»; [00:31:19](voice-009_TRANSCRIPT.md#S00424): «Em vẫn muốn em có một ví dụ về kết quả thực tế của em.» | vừa: Có lời trực tiếp trong văn bản; chưa nghe duyệt hoặc kiểm chứng bên ngoài. | chưa kiểm chứng |
| C7 | Trong báo cáo có các nhóm kịch bản khác nhau: chọn dữ liệu và thay đổi mô hình. Cần giải thích rõ các mã và số lượng vì phần trình bày đã có chỗ thiếu thông tin. (người nói chưa xác định) | [00:23:45](voice-009_TRANSCRIPT.md#S00307): «tổng cộng là 6 kịch bản»; [00:25:57](voice-009_TRANSCRIPT.md#S00356): «ở đây em sẽ có tổng cộng là 8 kịch bản»; [00:29:44](voice-009_TRANSCRIPT.md#S00401): «Đây em đang bị đưa thiếu khá nhiều thông tin» | vừa: Có lời trực tiếp trong văn bản; chưa nghe duyệt hoặc kiểm chứng bên ngoài. | chưa kiểm chứng |

## Câu hỏi mở và giới hạn

- Cần đối chiếu tên SeqGAN/các biến thể, thư viện SQL và thuật ngữ tokenization vì ASR ghi nhiều dạng khác nhau.
- Các con số về số mẫu, độ dài chuỗi, phần trăm trùng lặp, tỷ lệ vượt tường lửa và tham số pretraining phải kiểm tra bằng slide/code; bản ghi không chứng minh chúng đúng.
- Phân biệt sáu kịch bản lấy dữ liệu, tám kịch bản thay đổi mô hình và các cấu hình được chọn cuối cùng bằng một bảng gốc.
- Cần nghe lại các khoảng gián đoạn, các câu dang dở cuối bản ghi và phần nói về độ dài 20/160/1.600 trước khi sửa số.

## Practice Log — đề xuất của trợ lý

- [ ] Sắp lại outline thành mục tiêu → dữ liệu/ví dụ → baseline/thử nghiệm → vấn đề → cải tiến → kết quả có minh chứng.
- [ ] Tạo bảng mã kịch bản duy nhất, nêu nhóm, thay đổi, cấu hình giữ nguyên và đường dẫn kết quả.
- [ ] Kiểm tra slide ở kích thước trình chiếu và đưa một chuỗi đầu ra thật cạnh mỗi nhận định cần minh họa.

## Lịch ôn đề xuất

2026-09-10, 2026-09-13, 2026-09-21, 2026-10-09
