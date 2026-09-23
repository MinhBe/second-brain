# Second Brain — Hệ thống tri thức có thể truy nguyên (thử nghiệm)

> **Trạng thái:** PROTOTYPE — chỉ thử nghiệm kiến trúc lưu kiến thức, chưa thay thế quy trình cũ.
> **Mục tiêu:** Khi phát biểu một điều, Minh có thể trả lời: *Mình biết điều này từ đâu? Ai thực sự nói? Bằng chứng nằm ở đâu? Đâu là diễn giải hoặc suy luận của mình? Nên diễn đạt thế nào cho từng người nghe?*

## 1. Đọc file này như thế nào?

- Mới bắt đầu: đọc mục **2 → 5**; xem thẻ ví dụ trong `00 SYS - System/Templates/examples/`.
- Khi muốn lưu một ý mới: sao chép `00 SYS - System/Templates/knowledge-card.template.md`; không sửa template gốc.
- Khi đã có transcript/video/review nhưng chưa có sách: lưu được **nguồn thứ cấp**, song tuyệt đối không ghi “tác giả viết nguyên văn” khi chưa tra nguyên tác.
- Muốn thử nghiệm: tạo 3–5 thẻ nhỏ, tự hỏi lại sau vài ngày và đối chiếu nguồn; chưa tự động nhập toàn bộ kho cũ.

## 2. Một câu nói có “địa chỉ nhận thức” là gì?

Một kết luận cần nối được ngược về **nguồn → vị trí chính xác trong nguồn → bằng chứng → mệnh đề → cách hiểu → suy luận**. Đừng biến tên sách thành vật trang trí cho quan điểm riêng.

**Chuỗi tổ chức (không phải mỗi bước đều cần một file riêng):**

```text
SOURCE → EVIDENCE → CLAIM → CONCEPT → ARGUMENT → EXPRESSION
  sách    đoạn/trang    ý đơn    khái niệm   lập luận    cách nói
```

- **SOURCE:** tác giả, tác phẩm, ấn bản, năm, URL/DOI/ISBN khi có.
- **EVIDENCE:** đúng chương/trang/đoạn hoặc timestamp; đoạn trích ngắn nếu được phép; bằng chứng có thể phản biện.
- **CLAIM:** một mệnh đề đủ nhỏ để kiểm chứng và tái dùng độc lập.
- **CONCEPT:** thuật ngữ/mô hình/lý thuyết kết nối nhiều mệnh đề. *Khái niệm không tự động là bằng chứng.*
- **ARGUMENT:** tiền đề, suy luận, phản ví dụ, kết luận và giới hạn.
- **EXPRESSION:** lời trình bày phù hợp đối tượng, sinh ra **từ cùng một claim**, không tạo ra “sự thật” mới.

## 3. Giữ năm vùng hiện tại; không di chuyển kho cũ

| Vùng trong repo | Vai trò | Ví dụ |
|---|---|---|
| `Collection/` | Nguồn được thu thập, bản ghi, PDF được phép lưu, metadata, review, transcript | `Collection/FILES/BookReviews/` đang có nguồn R1–R7 |
| `Domain/` | Kiến thức **đã tách thành thẻ**, liên kết theo lĩnh vực | sau giai đoạn thử: `Domain/PHILOSOPHY/Claims/` |
| `Thought/` | Quan sát, câu hỏi, phản tư, **suy luận riêng của Minh** | ghi rõ `self-inference`, không giả danh lời tác giả |
| `Project/` | Nơi áp dụng kiến thức để ra kết quả | nghiên cứu, bài nói, phỏng vấn, Hermes |
| `00 SYS - System/` | Luật lưu trữ, schema, template, kiểm tra, hoạt động agent | template trong PR này |

**Hiện trạng quan trọng:** bộ `amusing_INSIGHT.md` có `source_quality: reconstructed-from-reviews` và `book_text: false`; dữ liệu tốt để thử truy xuất qua reviewer nhưng **không phải** xác minh nguyên văn Neil Postman. File `_work/VERIFICATION.md` cũng ghi kiểm tra snippet không chứng minh phần diễn giải là đúng.

## 4. Luật ghi nhận một ý tưởng

1. **Một thẻ = một mệnh đề chính**. Ý quá rộng thì chia; tránh một file chép lại nguyên cuốn sách.
2. **Phân biệt bốn tầng:** `QUOTE` (nguyên văn đã đối chiếu), `PARAPHRASE` (diễn đạt lại điều nguồn nói), `INTERPRETATION` (cách hiểu của người đọc), `INFERENCE` (kết luận tự suy ra). Không chuyển `INFERENCE` thành lời tác giả.
3. **Ưu tiên sách nguyên tác:** tác giả + tên sách + năm + **ấn bản** + chương + trang/vị trí. Số trang có thể khác giữa bản in/bản dịch/ebook; ghi ấn bản khi dùng số trang.
4. **Nếu chỉ có review/video:** lưu tên người review và timestamp, gắn `secondary-review`, `pending-primary`; chỉ viết “reviewer X diễn giải…” thay vì “sách khẳng định…”.
5. **Không bịa trích dẫn.** Thiếu câu nguyên văn thì để trống. Câu tiếng Việt do mình dịch phải gắn `translation-by-me` và đính nguyên bản ngắn đã đối chiếu nếu có.
6. **“Verified” là trạng thái có phạm vi:** kiểm tra đoạn xuất hiện ≠ kiểm tra lời thuật đúng tác giả ≠ chứng minh claim đúng thực nghiệm. Thẻ ghi chính xác đã xác minh tầng nào.
7. **Nguồn có thể là quan sát cá nhân:** đánh dấu `self-observation`, nêu thời gian và bối cảnh. Không buộc mọi suy nghĩ phải có một danh ngôn hoặc “định lý”.
8. **Gắn giới hạn và phản ví dụ:** “đúng với ai, ở đâu, lúc nào, điều kiện nào?”; nguồn bất đồng cần được giữ, không tự ép thành một kết luận đồng thuận.

**Trạng thái gợi ý:** `captured` → `source-located` → `attribution-checked` → `evidence-reviewed`; `needs-correction` khi thấy sai. Cờ `primary-checked: false` luôn thắng mọi điểm confidence khi quyết định có được trích trực tiếp từ sách không. Không gán 90/100 chỉ vì có ba reviewer đồng ý.

## 5. Một cuộc trò chuyện sẽ dùng kho này thế nào?

Khi Minh nhắn: **“Con người ngày nay cần giải trí đi kèm thông tin; tôi dựa vào Postman.”**

Agent nên:
1. **Tách mệnh đề:** xu hướng hiện tại là một claim thực nghiệm; luận điểm về môi trường truyền thông là một khung giải thích.
2. **Tìm thẻ/nguồn:** trả về `source_id`, chapter/page hoặc reviewer + timestamp; nếu chưa có, nói chưa có.
3. **Phân loại lời nói:** Postman thực sự được trích chưa? Reviewer diễn giải thế nào? Phần áp dụng sang TikTok/AI là suy luận của ai?
4. **Kiểm tra độ rộng:** từ ví dụ cá nhân không suy ra toàn thể con người; nếu thiếu nghiên cứu mới, ghi giả thuyết thay vì sự thật được chứng minh.
5. **Trả lời với dẫn nguồn và giới hạn**, sau đó mới đề xuất diễn đạt theo người nghe.

**Bốn chế độ diễn đạt, chung một cơ sở tri thức:**

| Đối tượng | Nội dung cần giữ |
|---|---|
| Người mới | Ý một câu + ví dụ dễ hiểu; không giả vờ ví dụ là bằng chứng |
| Biết sơ | Ý + khái niệm + nguồn + cơ chế ngắn |
| Ngang hàng | Claim + xuất xứ + tiền đề + giới hạn |
| Người chuyên sâu/phỏng vấn | Ấn bản/vị trí + tranh luận khác + bằng chứng/thiếu bằng chứng + điều kiện áp dụng |

Nguyên tắc: **thay đổi ngôn ngữ và độ sâu, không thay đổi sự thật hoặc mức chắc chắn.**

## 6. Quy trình thử 7 bước cho 1 Knowledge Card

```text
1. Chọn một câu/ý đáng giữ.
2. Tìm nguồn gần nhất và tạo source_id ổn định.
3. Kiểm tra vị trí; phân biệt sách thật với transcript nói VỀ sách.
4. Viết một claim ngắn, độc lập.
5. Tách quotation / paraphrase / interpretation / inference.
6. Ghi phản ví dụ, giới hạn, việc cần xác minh.
7. Diễn giải thử cho người mới và người chuyên sâu rồi so lại claim gốc.
```

**Đạt thử nghiệm** khi người khác có thể mở thẻ, tìm lại được đúng đoạn nguồn, phân biệt được phát biểu của tác giả với ý Minh và diễn đạt lại không phóng đại. Nếu làm thẻ quá tốn công, rút bớt trường tùy chọn; không bỏ `source`, `locator`, `attribution`, `verification`.

## 7. Template và ví dụ

- [Template Knowledge Card](00%20SYS%20-%20System/Templates/knowledge-card.template.md)
- [Ví dụ: phương tiện và cách hiểu — nhãn nguồn thứ cấp, KHÔNG có quote sách](00%20SYS%20-%20System/Templates/examples/K-MEDIA-0001.example.md)
- [Book insight đã có của repo](Collection/FILES/BookReviews/amusing_INSIGHT.md)
- [Verification notes đã có của repo](Collection/FILES/BookReviews/_work/VERIFICATION.md)

**Phạm vi thử nghiệm:** ba file mới trên nhánh `experiment/epistemic-knowledge-architecture-20260923`; không thay file BookReviews, không tự thêm ghi chú chưa kiểm vào `Domain`, không sửa cấu trúc dữ liệu / SQLite / Hermes. Đây là đề xuất kiến trúc, **không phải một skill tự động đã hoạt động**.

**Lưu ý GitHub:** repo hiện công khai. Không commit thông tin gia đình/cá nhân nhạy cảm, private transcript, API key, cookie; không đưa nguyên văn dài hoặc toàn bộ sách có bản quyền lên repo công khai. Lưu bibliographic metadata và trích đoạn ngắn cần thiết, kèm chỉ dẫn đến bản sách bạn có quyền truy cập.
