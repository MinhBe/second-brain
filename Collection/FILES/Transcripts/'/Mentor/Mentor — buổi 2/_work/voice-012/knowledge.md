# Tri thức — Voice 012 — định nghĩa phép đo, chứng minh cải tiến và giới hạn thử nghiệm qua WAF

## Raw Inbox

[Transcript đầy đủ](../../voice-012_TRANSCRIPT.md) · [Báo cáo chất lượng](../../_work/voice-012/quality_report.md)

Nguồn là hội thoại được ASR nhận dạng và chưa nghe duyệt. Confidence dưới đây phản ánh mức chắc chắn của diễn giải từ văn bản, không chứng minh lời nói đúng về mặt thực tế.

## Knowledge Nodes

<a id="N1"></a>
### N1 — Định nghĩa quy ước và thước đo trước khi đưa kết quả

- **Câu hỏi tổng hợp:** Điều gì phải rõ trước khi so sánh các tỷ lệ và bảng số liệu?
- **Cốt lõi:** Nêu căn cứ của cách chia mức mất cân bằng và định nghĩa chỉ số, đặc biệt dấu và mốc so sánh của Delta Recall.
- **Ví dụ/ngữ cảnh:** Người nghe hỏi lại cả quy ước nhẹ/trung bình/cao lẫn ký hiệu đánh giá.
- **Điều kiện áp dụng:** Cách tính Delta Recall trong ASR chưa rõ chiều trừ; không tự sửa hoặc suy công thức.
- **Liên kết:** C1, C2; Bản thầy Lâm N2 về công thức diversity.

<a id="N2"></a>
### N2 — Chứng minh thay đổi thay vì liệt kê tên cải tiến

- **Câu hỏi tổng hợp:** Làm sao người nghe thấy được phần đóng góp?
- **Cốt lõi:** Đưa từng thay đổi vào mô hình và đối chiếu trước/sau bằng thử nghiệm; giải thích mô hình gốc trước phần cải tiến.
- **Ví dụ/ngữ cảnh:** Các mã cấu hình trên slide chưa giúp người nghe hiểu phần được sửa.
- **Điều kiện áp dụng:** Cần bảng thí nghiệm gốc và sơ đồ đúng với mã; không suy hiệu quả từ tên kịch bản.
- **Liên kết:** C3, C4; Voice 011 N3 về ablation; Voice 009 N3 về thứ tự chứng minh.

<a id="N3"></a>
### N3 — Giới hạn kết luận từ phản hồi WAF

- **Câu hỏi tổng hợp:** Kết quả HTTP 200 trong thử nghiệm này chứng minh được gì?
- **Cốt lõi:** Nó chưa chứng minh khai thác SQL injection thành công: môi trường được mô tả chỉ có bộ lọc, có thể cho dữ liệu nhiễu đi qua và không có database để kiểm chứng tác động.
- **Ví dụ/ngữ cảnh:** Phần hỏi đáp làm rõ khác biệt giữa qua ruleset, có cấu trúc SQL và tấn công thực tế.
- **Điều kiện áp dụng:** Giới hạn này áp dụng cho thử nghiệm đang được mô tả; không khái quát mọi hệ WAF. Đây là nhận định về phạm vi bằng chứng, không hướng dẫn khai thác.
- **Liên kết:** C5, C6; Liên hệ Voice 009 N4 về kết quả phải hỗ trợ đúng tuyên bố.

## Claim Ledger

| ID | Nội dung được diễn giải | Bằng chứng | Confidence | Kiểm chứng |
|---|---|---|---|---|
| C1 | Các mức mất cân bằng nhẹ/trung bình/cao trong báo cáo là cách tự phân loại của người trình bày; được yêu cầu tìm căn cứ từ công trình trước. (người nói chưa xác định) | [00:05:40](../../voice-012_TRANSCRIPT.md#S00044): «nhẹ trung bình cao là em tự phân loại»; [00:05:44](../../voice-012_TRANSCRIPT.md#S00046): «Em tự phân loại»; [00:06:20](../../voice-012_TRANSCRIPT.md#S00055): «Các em có bài báo nào đang chia như thế này không?» | vừa: Có lời trực tiếp trong văn bản; chưa nghe duyệt hoặc kiểm chứng bên ngoài. | chưa kiểm chứng |
| C2 | Tên chỉ số và ký hiệu Delta Recall cần được giải thích nhất quán; người nghe đã phải hỏi lại định nghĩa phép đo. (người nói chưa xác định) | [00:07:15](../../voice-012_TRANSCRIPT.md#S00062): «và cuối cùng là tính Recall»; [00:07:38](../../voice-012_TRANSCRIPT.md#S00066): «Delta Recon là gì? Mọi người biết không?» | vừa: Có lời trực tiếp trong văn bản; chưa nghe duyệt hoặc kiểm chứng bên ngoài. | chưa kiểm chứng |
| C3 | Mỗi cải tiến cần có thử nghiệm so sánh với bản cũ và thể hiện kết quả trước/sau; chỉ nêu tên cấu hình tổng hợp chưa giúp người nghe thấy đóng góp. (người nói chưa xác định) | [00:28:33](../../voice-012_TRANSCRIPT.md#S00286): «cải tiến thứ nhất thì có thử và ra kết quả nó hơn so với phía cũ không?»; [00:28:40](../../voice-012_TRANSCRIPT.md#S00287): «Cải tiến thứ 2 thì có thử và ra kết quả nó hơn so với phía cũ không?»; [00:29:20](../../voice-012_TRANSCRIPT.md#S00300): «Trước cải thiện như thế này và sau cải thiện kết quả như thế nào.» | vừa: Có lời trực tiếp trong văn bản; chưa nghe duyệt hoặc kiểm chứng bên ngoài. | chưa kiểm chứng |
| C4 | Báo cáo phải trình bày nền tảng và phần chính rõ trước khi đi vào cải tiến; lần sửa slide được nhận xét là chưa phản ánh đủ góp ý trước. (người nói chưa xác định) | [00:32:25](../../voice-012_TRANSCRIPT.md#S00327): «Slide này cũng chưa phản ánh được cái góp ý lần trước.»; [00:33:57](../../voice-012_TRANSCRIPT.md#S00342): «Mình trình bày cái mặt chính luôn, tốt đi đã.»; [00:34:20](../../voice-012_TRANSCRIPT.md#S00345): «Tại sao dùng gan để xin dữ liệu?» | vừa: Có lời trực tiếp trong văn bản; chưa nghe duyệt hoặc kiểm chứng bên ngoài. | chưa kiểm chứng |
| C5 | Trong thử nghiệm đang báo cáo, không có database để xác nhận khai thác thành công; HTTP 200 có thể là qua bộ lọc hoặc chỉ là dữ liệu nhiễu, sau đó mới xem cấu trúc payload. (người nói chưa xác định) | [00:37:55](../../voice-012_TRANSCRIPT.md#S00381): «trong chính cái kịch bản của em ạ, nó cũng không có database»; [00:37:55](../../voice-012_TRANSCRIPT.md#S00381): «nếu như trả về kết quả 200 thì em sẽ biết là một là nó đã vượt qua hoặc là noise» | vừa: Có lời trực tiếp trong văn bản; chưa nghe duyệt hoặc kiểm chứng bên ngoài. | chưa kiểm chứng |
| C6 | Người trình bày thừa nhận phần triển khai thực tế phức tạp và lệch mục tiêu nên đã thu nhỏ phạm vi; cần viết rõ giới hạn này trong cả báo cáo và slide. (người nói chưa xác định) | [00:41:36](../../voice-012_TRANSCRIPT.md#S00409): «Trong lúc triển khai thì phải tự nhiên nó phức tạp hơi nhiều so với mục tiêu ban đầu»; [00:41:43](../../voice-012_TRANSCRIPT.md#S00410): «Và cảm giác nó hơi lệch nên là mới thu nhỏ xuống»; [00:42:17](../../voice-012_TRANSCRIPT.md#S00414): «Mình về trình bày lại cho rõ trong văn lẫn, trong slide nhé» | vừa: Có lời trực tiếp trong văn bản; chưa nghe duyệt hoặc kiểm chứng bên ngoài. | chưa kiểm chứng |

## Câu hỏi mở và giới hạn

- Các mã DV7/DV8 và nhóm Union/Boolean xuất hiện không nhất quán; cần bảng gốc trước khi xác định cấu hình thắng.
- Phần chọn vùng giữa có câu 'bỏ 25% đầu và 75% cuối' nhưng lại nói giữ 50%; giữ nguyên nghi vấn và đối chiếu quy tắc lấy mẫu thực tế.
- Các tỷ lệ 70%/3%, số mẫu và tên bộ lọc/ruleset cần xác nhận; không dùng như thống kê đã kiểm chứng.
- Cần xác định Delta Recall là sau trừ trước hay trước trừ sau, bộ phát hiện và tập đánh giá cố định là gì.
- Các câu quảng cáo/kết thúc quanh đầu file và 24–26 phút có dấu hiệu hallucination; phần đầu gần ba phút chưa nhận dạng được đáng tin cậy.

## Practice Log — đề xuất của trợ lý

- [ ] Tạo bảng thuật ngữ/chỉ số có định nghĩa và công thức, kèm nguồn hoặc ghi rõ đây là quy ước tự chọn.
- [ ] Vẽ lại mô hình gốc và đánh dấu từng phần thay đổi, nối mỗi thay đổi với một dòng kết quả ablation.
- [ ] Viết mục giới hạn thực nghiệm, phân biệt qua bộ lọc, cấu trúc hợp lệ và khai thác thành công; sửa mọi tuyên bố vượt quá phép thử hiện có.

## Lịch ôn đề xuất

2026-09-10, 2026-09-13, 2026-09-21, 2026-10-09
