# Tầng 2: bản đồ và vấn đáp

Viết section 6 vào part2_map.md; bốn thành phần nằm trong cùng report.

- 6.1 Index <=40 dòng: tên/tác giả, What it argues, một dòng/chương, liên kết nội bộ
  tới chapter blocks, techniques, glossary. Không có TOC: ghi "tái dựng từ review,
  chưa đối chiếu sách"; chapter_hint không đủ để bịa số chương. Dùng khối chủ đề
  khi không xác định được chương. Chương thiếu ghi "nguồn không nói đủ".
- 6.2 Mỗi chapter block <=15 dòng: Core Idea -> Nội dung khái niệm/kỹ thuật/mô hình
  -> Why This Matters -> Where This Sits. Tối thiểu hai extraction có evidence;
  không sao chép văn gốc liên tiếp hoặc độn nội dung cho đủ dòng.
- 6.3 Techniques & Patterns: Technique | What It Is | Source. Chỉ mô hình/kỹ thuật
  được nguồn thực sự mô tả; không coi mọi keyword là kỹ thuật.
- 6.4 Glossary: **term_vi (term EN)**: định nghĩa + nguồn, từ terms.clean.jsonl.

Giữ paraphrase, tham chiếu private, index ngắn và review nguồn từ book-to-skill.
Không sinh một skill riêng mỗi cuốn. Bỏ contradiction precedence của policy;
vẫn kiểm tra bất đồng giữa reviewer trong 8.7. Skim mọi chapter block so nguồn.

## Bốn vòng Q&A

Mỗi vòng 3-5 câu, tổng 12-20. Agent tự hỏi và trả lời, không bắt người đọc điền
trước khi tạo report. Tạo qa.jsonl với schema ở tier3; assembler sinh section 7.

| Vòng | Cần kiểm tra | Câu hỏi mẫu |
| --- | --- | --- |
| 1 Hiểu | Định nghĩa, cơ chế, ví dụ gốc | Tác giả dùng X khác nghĩa thông thường thế nào? Cơ chế nối X với Y? |
| 2 Phản biện | Evidence yếu, counterexample, giới hạn | Điều kiện nào làm luận điểm thất bại? Reviewer phản bác bằng gì? |
| 3 Chuyển giao | Domain của người đọc | Thí nghiệm 7 ngày nào kiểm tra ứng dụng? Chỉ báo thành công là gì? |
| 4 Nối kết | Sách/ghi chú thực có | Khác một lý thuyết đã đọc ở đâu? Hai thuật ngữ có thực sự tương đương? |

Không truy cập MEMORY.md tùy tiện để lấp chỗ trống: chỉ dùng nguồn người đọc đưa
hoặc nguồn liên quan trong workspace, đưa vào manifest/notes khi dùng như bằng chứng.
Nếu không có tài liệu so sánh, trả "Chưa có trong nguồn". Tách suy luận ứng dụng
origin=generated, answer có evidence_ids và được đánh [mở rộng]. Không mượn nhãn R
để làm ứng dụng của agent có vẻ là lời sách. Cập nhật method/application tầng 1
sau QA, rồi chạy validation lần cuối.
