# Nghiệm thu

- [ ] R1 luận đề mệnh đề, có người/điều kiện có thể phản bác; provisional nếu cần.
- [ ] R2 <=5 ý xếp hạng, foundational/derived, không ép đồng thuận khi thiếu nguồn.
- [ ] R3 quote ngắn có chú giải, đúng chủ thể; đối chiếu câu thật trong nguồn.
- [ ] R4 ít nhất một ứng dụng theo domain trong 7 ngày, có cách quan sát kết quả.
- [ ] R5 mode và evidence scale từng ý; không nhầm confidence với độ đúng của sách.
- [ ] R6 survivorship/selection bias được xét cụ thể, không né bằng N/A.
- [ ] R7 trạng thái đọc đúng, bảng nguồn đầy đủ, thesis_source_cap đúng.
- [ ] R8 đồng thuận/phản bác/lân cận có nguồn hoặc gap rõ ràng.
- [ ] R9 bốn recall checks và lịch +1/+4/+12/+30 từ created, gắn Q ID.
- [ ] R10 dịch giả hoặc chưa rõ.
- [ ] R11 mỗi câu factual 1-3 và câu trả lời/table row nguồn 7-8 có locator thực.
- [ ] R12 không nâng ý riêng reviewer thành nguyên văn tác giả hoặc đồng thuận giả.
- [ ] R13 không quote/new term dịch máy; unknown không bị nâng confidence.
- [ ] R14 lỗi sự kiện có bằng chứng kiểm chứng ở 8.9, không lan vào luận đề.
- [ ] Validator exit 0, errors=[], unverified_snippets=[], lowconf được giữ riêng.
- [ ] Fingerprint khớp raw và clean; không append vào file clean; QA không bịa snippet.
- [ ] Core idea có BOOK hoặc >=2 nhóm reviewer độc lập; mỗi rid có evidence riêng.
- [ ] Thuật ngữ có alias kiểm chứng; frequency là số đoạn, không phải số nhắc phỏng đoán.
- [ ] Index <=40 dòng, chapter block <=15 dòng; skim từng khối so với nguồn.
- [ ] Mọi chapter block là paraphrase, không tái tạo đoạn dài; ghi chú dùng riêng.
- [ ] Mục 9 và ứng dụng suy luận đánh [mở rộng]; không giả citation cho phần thêm.
- [ ] 13 main headings 0-12, không placeholder; QA 12-20 câu, 3-5 mỗi vòng.
- [ ] 600-1000 từ sections 1-5 +10-11; thiếu dữ liệu ghi rõ.
- [ ] Test regression pass; tests nguồn tổng hợp không được báo như đọc thật cả sách.
- [ ] Nếu --anki: ID ổn định qua reorder/edit; chưa nhập Anki thì không báo đã kiểm scheduling.

Validator chứng minh sự hiện diện của snippet, không chứng minh entailment, factual truth,
tính đại diện hoặc chất lượng ứng dụng. Người viết report phải làm bước này khi đọc nguồn.
