# Tri thức — Voice 002 — hội thoại về AI trong an toàn thông tin, WAF mã nguồn mở và kế hoạch bảo vệ đề tài

## Raw Inbox

[Transcript đầy đủ](../../voice-002_TRANSCRIPT.md) · [Báo cáo chất lượng](../../_work/voice-002/quality_report.md)

Nguồn là hội thoại được ASR nhận dạng và chưa nghe duyệt. Confidence dưới đây phản ánh mức chắc chắn của diễn giải từ văn bản, không chứng minh lời nói đúng về mặt thực tế.

## Knowledge Nodes

<a id="N1"></a>
### N1 — Giảm chi phí AI khi phân tích log

- **Câu hỏi tổng hợp:** Làm sao để giảm chi phí token khi dùng AI phân tích log bảo mật?
- **Cốt lõi:** Không ném toàn bộ log vào AI chính: dùng mô-đun nhỏ lọc bớt trước, đồng thời sinh thêm dữ liệu cho những trường hợp khó (mẫu tấn công hiếm) thay vì để mô hình học theo số đông bỏ sót.
- **Ví dụ/ngữ cảnh:** Phần đầu bản ghi — mô tả bài toán và 2 hướng tiếp cận của người nói.
- **Điều kiện áp dụng:** Con số 80/20 và hiệu quả chưa kiểm chứng; chờ nghe duyệt.
- **Liên kết:** C1, C2, C4; Phần sinh dữ liệu GAN ở cuối bản ghi (N?); liên quan đề tài luận văn của người nói.

<a id="N2"></a>
### N2 — Chọn mô hình AI và WAF mã nguồn mở cho an toàn thông tin

- **Câu hỏi tổng hợp:** Nên chọn mô hình AI bản nào và WAF mã nguồn mở nào trong tác vụ bảo mật?
- **Cốt lõi:** Cân nhắc giữa bản mô hình rẻ (vài trăm USD, tiêu chuẩn an toàn bị lược bớt) với bản giữ tiêu chuẩn; so sánh được 2 WAF mã nguồn mở dùng chung rule set CRS — giống nhau cơ bản, khác ở độ tùy chỉnh.
- **Ví dụ/ngữ cảnh:** Phần trao đổi giữa hai người về công cụ và WAF (S00027–S00105).
- **Điều kiện áp dụng:** Tên 'Cora-Za', 'Fable' và giá cả từ ASR chưa đối chiếu; mở rộng bằng tài liệu gốc.
- **Liên kết:** C3, C5; Cùng chủ đề công cụ an toàn thông tin với bản ghi anh-minh.

<a id="N3"></a>
### N3 — Kinh nghiệm bảo vệ trước hội đồng

- **Câu hỏi tổng hợp:** Bảo vệ luận văn thế nào để hội đồng ít hỏi và đạt điểm cao?
- **Cốt lõi:** Từ câu chuyện của anh Hải: thuyết trình trọn phần trình bày (40 phút) giúp hội đồng không hỏi thêm và được 8.6; các điểm 8 trở xuống rất hiếm trong thang điểm của trường.
- **Ví dụ/ngữ cảnh:** Phần chia sẻ kinh nghiệm bảo vệ (S00176–S00191).
- **Điều kiện áp dụng:** Con số 40 phút/8.6/0.13 cần nghe lại trước khi trích.
- **Liên kết:** C6; Hồ sơ, tiêu chí trình bày đề cập thêm ở phần cuối (S00333+).

<a id="N4"></a>
### N4 — Xử lý alert trong SOC: tự làm nội bộ hay dùng sản phẩm hãng

- **Câu hỏi tổng hợp:** Có thể tự xử lý alert SOC nội bộ thay vì dùng sản phẩm hãng không?
- **Cốt lõi:** Có; nước ngoài và cả MISA đang làm nội bộ. Người nói dự kiến bổ sung keyword quét mạnh hơn và một mô-đun AI nhỏ giữa tường lửa và AI chính để sàng lọc theo dữ liệu threat intelligence.
- **Ví dụ/ngữ cảnh:** Phần hỏi-đáp về SOC, alert, evidence, endpoint (S00280–S00440).
- **Điều kiện áp dụng:** Đoạn ba tiếng về MISA bootcamp (21:00–21:28) và IOC/imphash (30:50–32:10) bị no_speech; kiểm chứng riêng.
- **Liên kết:** C7, C8; Quy trình điều tra sự kiện tương tự phần Splunk trong bản ghi anh-minh.

<a id="N5"></a>
### N5 — AI trong pen test và yêu cầu sau khóa đào tạo

- **Câu hỏi tổng hợp:** AI ở mức nào là đủ trong an toàn thông tin và sau khóa học có ràng buộc gì?
- **Cốt lõi:** Với AI, chỉ cần ném 'mindset' để AI tự chủ động làm, case study là quan trọng nhất; mặt khác môi trường học viện yêu cầu 5 năm cống hiến sau khi học.
- **Ví dụ/ngữ cảnh:** Phần trao đổi về pen test, case study và chế độ đào tạo (S00228–S00253).
- **Điều kiện áp dụng:** Thông tin học viện/khóa học chưa định danh được; cần hỏi làm rõ.
- **Liên kết:** C9, C10; Góc nhìn 'AI làm chủ động' liên hệ mô-đun lọc sớm ở N1.

## Claim Ledger

| ID | Nội dung được diễn giải | Bằng chứng | Confidence | Kiểm chứng |
|---|---|---|---|---|
| C1 | Dữ liệu log đang dùng bị outdated; dùng AI thì chỉ học được khoảng 80%, phần mẫu đặc biệt hơn hoặc dài hơn dễ bị bỏ qua. (người nói chưa xác định) | [00:00:10](../../voice-002_TRANSCRIPT.md#S00003): «Cái data em bị outdated.»; [00:00:18](../../voice-002_TRANSCRIPT.md#S00006): «Nghĩa là nếu dùng AI thì nó chỉ học được khoảng 80% thôi.»; [00:00:23](../../voice-002_TRANSCRIPT.md#S00007): «kiểu mẫu dài hơn hoặc là» | vừa: Ba câu nối mạch rõ chủ đề; con số 80/20 chưa nghe duyệt. | chưa kiểm chứng |
| C2 | Để giảm chi phí, không gửi toàn bộ log vào AI; tạo một mô-đun nhỏ lọc bớt trước, dùng một mô hình nhỏ hơn, chuyên biệt hơn — sau đó mới tới mô hình chính. (người nói chưa xác định) | [00:00:57](../../voice-002_TRANSCRIPT.md#S00016): «Để cho là AI không phải đưa toàn bộ tất cả các Log qua AI nữa»; [00:01:23](../../voice-002_TRANSCRIPT.md#S00024): «thì bây giờ phải tạo một cái mô đun nhỏ để nó giảm hiểu cái đồng đấy trước khi đi tiếp»; [00:01:28](../../voice-002_TRANSCRIPT.md#S00025): «kiểu đưa qua một con AI đần hơn nhưng mà nhỏ hơn và chuyên biệt hơn» | vừa: Các câu mô tả luồng xử lý nhất quán; chưa nghe duyệt. | chưa kiểm chứng |
| C3 | Khi làm Bounty, có cân nhắc dùng bản mô hình ~200 USD (ASR: 'con Fable'); bản này được mô tả là đã loại bỏ bớt tiêu chuẩn về an toàn thông tin. (người nói chưa xác định) | [00:01:38](../../voice-002_TRANSCRIPT.md#S00027): «nếu mà anh dùng con 200$ cho anh, con đấy nó có con Fable»; [00:01:51](../../voice-002_TRANSCRIPT.md#S00028): «con đấy là nó được loại bỏ bớt những cái tiêu chuẩn về an toàn thông tin» | thấp: Tên mô hình 'Fable', giá 200$ và đánh giá chi tiết bị ngắt giữa câu bởi đoạn no_speech; cần nghe lại. | chưa kiểm chứng |
| C4 | Với bộ dữ liệu nhỏ (50 câu, chỉ 2 câu tấn công đặc biệt), mô hình học theo số đông sẽ lờ 2 câu đó đi; thay vào đó nên sinh 50 câu từ 2 câu mẫu rồi mới huấn luyện. (người nói chưa xác định) | [00:04:49](../../voice-002_TRANSCRIPT.md#S00086): «Ví dụ như là bây giờ em có 50 câu, trong đó chỉ có 2 câu tấn công rất là đặc biệt, rất là kiểu chuyên biệt»; [00:04:57](../../voice-002_TRANSCRIPT.md#S00087): «thì đưa vào mô hình thì nó chỉ học 48 câu còn lại, 2 câu kia nó cho rằng là thứ yếu nên nó sẽ bỏ qua.»; [00:05:04](../../voice-002_TRANSCRIPT.md#S00088): «sinh ra được 50 câu rồi đưa vào thì nó sẽ chỉ tập trung vào» | vừa: Ba câu trình bày vấn đề và giải pháp mạch lạc. | chưa kiểm chứng |
| C5 | So sánh hai WAF mã nguồn mở (ASR: 'Cora-Za' và 'Mod'): dùng chung rule set (CRS), cơ bản giống nhau, bên này tùy chỉnh nhiều hơn, triển khai ban đầu dễ hơn nhưng cần cấu hình thêm. (người nói chưa xác định) | [00:06:02](../../voice-002_TRANSCRIPT.md#S00098): «Em và các em có thử Cora-Za với Mod là nó phải dùng rule set chung»; [00:06:07](../../voice-002_TRANSCRIPT.md#S00100): «Còn về cơ bản là hai thằng như nhau mà thằng này được tùy chỉnh nhiều hơn»; [00:06:15](../../voice-002_TRANSCRIPT.md#S00101): «Nếu mà chuyển khai ban đầu thì dễ hơn nhưng mà nhiều cái phải setting nha» | thấp: Tên dự án ASR chưa chắc ('Cora-Za', 'Mod', 'MDX'); so sánh là lời nói trực tiếp. | chưa kiểm chứng |
| C6 | Chia sẻ kinh nghiệm bảo vệ: có người (nói về anh Hải) thuyết trình trọn 40 phút nên hội đồng không hỏi thêm và được điểm 8.6; còn các điểm 8 ở trường chỉ chiếm rất ít (ASR: 0.13). (người nói chưa xác định) | [00:11:30](../../voice-002_TRANSCRIPT.md#S00177): «Anh ấy thuyết trình hết 40 phút»; [00:11:34](../../voice-002_TRANSCRIPT.md#S00179): «Cho 8-6 đi về»; [00:12:10](../../voice-002_TRANSCRIPT.md#S00191): «Còn mấy cái điểm 8 chấm ở trên trường chỉ chiếm 0.13» | thấp: Các con số (40 phút, 8.6, 0.13) cần nghe duyệt; bối cảnh trường/khóa chưa rõ. | chưa kiểm chứng |
| C7 | Phần xử lý alert trong SOC có thể làm 'nội bộ' được, và công ty MISA đang làm theo hướng đó. (người nói chưa xác định) | [00:20:52](../../voice-002_TRANSCRIPT.md#S00298): «không, mình làm nội bộ vẫn được»; [00:20:54](../../voice-002_TRANSCRIPT.md#S00299): «MISA đang làm đấy rồi» | vừa: Câu khẳng định và ví dụ trực tiếp rõ nghĩa. | chưa kiểm chứng |
| C8 | Khi bảo vệ dự kiến làm 2 việc: thêm keyword để tường lửa quét mạnh hơn, và đặt một mô-đun AI nhỏ giữa tường lửa với AI chính để sàng lọc thêm; mô-đun này dựa trên nguồn threat intelligence (TI). (người nói chưa xác định) | [00:29:02](../../voice-002_TRANSCRIPT.md#S00432): «Mục tiêu của em là khi bảo vệ thì sẽ làm 2 cái»; [00:29:07](../../voice-002_TRANSCRIPT.md#S00433): «Một là thêm cái keyword để cho thằng tượng lửa nó quét mạnh hơn»; [00:29:11](../../voice-002_TRANSCRIPT.md#S00434): «Hai là sẽ ném một thằng AI vào giữa thằng tượng lửa với cả thằng AI chính»; [00:29:28](../../voice-002_TRANSCRIPT.md#S00439): «Cái con mô đun bé của em là nó phải dựa trên TI» | vừa: Chuỗi câu S00433–S00440 trình bày mục tiêu và 2 việc rõ; thuật ngữ 'tượng lửa' chỉ ASR. | chưa kiểm chứng |
| C9 | Quan điểm về AI trong an toàn thông tin: chỉ cần cung cấp 'mindset', phần còn lại AI sẽ chủ động làm; và case study được xem là quan trọng nhất. (người nói chưa xác định) | [00:17:33](../../voice-002_TRANSCRIPT.md#S00253): «bây giờ chỉ ném cái mindset là thôi, còn lại là nó sẽ chủ động.»; [00:17:41](../../voice-002_TRANSCRIPT.md#S00254): «Và cái quan trọng nhất là cái case study là cái quan trọng nhất.» | vừa: Câu chuyển đạt lại ý của người khác, nghĩa rõ; chưa rõ chủ thể gốc. | chưa kiểm chứng |
| C10 | Sau khi học xong, học viện yêu cầu 5 năm cống hiến; thời gian chỉ được tính khi thực sự được mời về làm việc, khiến một số người bị kẹt giữa chừng. (người nói chưa xác định) | [00:16:14](../../voice-002_TRANSCRIPT.md#S00237): «Sau khi học xong rồi phải có 5 năm»; [00:16:16](../../voice-002_TRANSCRIPT.md#S00238): «Cống hiến cho học viện» | thấp: Chuyện cá nhân chưa xác định được bối cảnh (học viện/công ty nào); cần nghe duyệt trước khi dùng. | chưa kiểm chứng |

## Câu hỏi mở và giới hạn

- Phần giới thiệu WAF (05:13–06:02), MISA bootcamp (21:00–21:28) và phần IOC/imphash (30:50–32:10) bị cờ no_speech; cần nghe lại trước khi dùng.
- Thuật ngữ 'Fable', giá '200$', 'Cora-Za', 'MDX', 'wow' chưa chắc; cần nghe nguồn.
- Đoạn 28:45–29:20 (mối lo nhóm 'khách intelligent' có AI) và 33:01–33:30 (CVE/GAN) bị cờ no_speech; chưa đủ căn cứ để ghi nhận.
- Hai vai 'em' (học viên chuẩn bị bảo vệ) và 'anh' (người làm bảo mật, biết về SOC/bootcamp) chưa định danh; không gán trùng với người ở bản ghi khác khi chưa kiểm chứng.

## Practice Log — đề xuất của trợ lý

- [ ] Nghe lại các đoạn no_speech trước khi dùng nội dung SOC/MISA/IOC cho báo cáo; ghi kèm khoảng thời gian khi trích con số.
- [ ] Lập bảng tóm tắt 2 hướng (mô-đun nhỏ lọc sớm và sinh dữ liệu khó bằng GAN) để trình lại chủ đề chính của cuộc trò chuyện.

## Lịch ôn đề xuất

2026-09-14, 2026-09-17, 2026-09-25, 2026-10-13
