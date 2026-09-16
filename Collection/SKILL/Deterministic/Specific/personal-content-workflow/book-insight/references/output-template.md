# Hợp đồng report

Đầu ra có 12 mục nội dung (1-12) và bảng nguồn (0): tổng 13 heading `##`.
Frontmatter YAML do script sinh, một khóa mỗi dòng, giá trị dùng JSON hợp lệ trong YAML.
book là object title_vi/title_orig/author/year/translator_vi; metadata khác gồm
source_quality, source_quality_note, thesis_source_cap, sources, book_text, notes,
purpose, domain, created, chunks, extractions, new_terms, extractions_by_type,
status và review_dates. Mọi ngày ôn tính từ created, không cộng dồn các khoảng.

## Phân công ba part

part1_summary.md có các heading chính sau, không thêm frontmatter:

```markdown
## 1. Luận đề trung tâm
{Luận đề tuyên bố/chứng minh; contestability test; locator từng câu factual.}
## 2. Ý chính
{3-5 ý xếp hạng: tiêu đề, 2-3 câu, evidence, Strong/Moderate/Weak + lý do,
foundational/derived, locator. Thiếu bằng chứng: ít hơn, ghi rõ provisional.}
## 3. Trích dẫn có chú giải
{3-5 quote ngắn, đúng người nói, nguồn và chú giải; thiếu thì ghi nguồn không đủ.}
## 4. Phương pháp của tác giả
{Mode, evidence base, strength, limitation, survivorship check, reviewer phản biện,
Subsequent Evidence Update hoặc chưa có nguồn cập nhật đã xác minh.}
## 5. Liên hệ trí tuệ
{Đồng thuận, phản bác, lĩnh vực lân cận; phân loại và nguồn/[mở rộng].}
## 10. Ứng dụng có thời hạn và nơi tôi không đồng ý
{Ý -> domain -> hành vi trong <=7 ngày; phản đối thay đổi cách áp dụng ra sao.}
## 11. Kết luận, tự kiểm và lịch ôn
{Verdict 2-3 câu, bốn ô tự kiểm, gaps; +1/+4/+12/+30 gắn Q ID.}
## 12. Đọc tiếp
{5-8 tài liệu với foundational/derivative/applied, lý do, nguồn kiểm chứng hoặc gap.}
```

part2_map.md chỉ có `## 6. Bản đồ sách`, với 6.1-6.4 theo tier2.
part3_extractions.md có `## 8. Bảng trích xuất` với 8.7 Bất đồng, 8.8 Một nguồn,
8.9 Lỗi nguồn; tiếp theo `## 9. Mở rộng` có `[mở rộng]` cho từng core idea.
Không viết 8.1-8.6 trong part: script sinh theo dữ liệu clean. Section 0 tự sinh từ
manifest; section 7 tự sinh từ qa.clean.jsonl. Không cần viết part rỗng giữ chỗ.

## Ràng buộc xuất bản

Các placeholder trong template chỉ để hướng dẫn, không xuất trong report.
Thiếu dữ liệu ghi nguồn không đủ, không chế tạo thêm mục. Raw JSONL luôn giữ nguyên.
Assembler từ chối dữ liệu lỗi hoặc bị sửa sau validation, nhãn không có trong nguồn,
trích dẫn dùng nguồn dịch máy/unknown/NOTE, phần tự sinh bị viết trùng.
Thiếu section, QA không đủ mỗi vòng, thiếu citation cấp đoạn, độ dài ngoài khoảng
hoặc placeholder sẽ chặn report final; --draft chỉ bỏ các lỗi biên tập này.
Human check từng câu, chất lượng diễn giải, quyền quote, giới hạn index/chapter.
Độ dài máy đếm whitespace: sections 1-5 + 10-11, 600-1000 từ; số token không tương đương.
