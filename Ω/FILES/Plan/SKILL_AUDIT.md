# Skill audit — kết quả kiểm tra và sửa chữa

Kiểm tra 2026-09-08–09, tại `C:\Users\Admin\Documents\Collection`. Phạm vi gồm skill cá nhân, kho upstream, đường dẫn kích hoạt và catalog dữ liệu. Bản audit ban đầu được giữ trong [_implementation/before](./_implementation/before/).

## Kết quả cấu trúc

| Hạng mục | Kết quả có bằng chứng |
|---|---|
| Tổng SKILL.md | 1.134, gồm 1 skill audio mới |
| Skill giữ trong Skills | 11, có mục đích và trạng thái riêng trong [README](../../Skills/README.md) |
| Skill tham khảo | 1.123, trong Reference/Domain; chưa được coi là đã kiểm thử runtime |
| Kích hoạt | book-insight, learn-this, audio-transcribe-local qua junction ở cả .agents/skills và .claude/skills |
| Di chuyển | 15 package upstream/workspace và 11 file catalog lịch sử |
| Toàn vẹn | 26 mục, 26.550 file thường, 726.494.607 byte đã đối chiếu SHA-256; không có lỗi |

[Inventory đầy đủ](./_implementation/skill_inventory.json) ghi đường dẫn, frontmatter và trạng thái từng skill. [Manifest](./_implementation/moves.json), [journal](./_implementation/moves.executed.jsonl) và [kết quả đối chiếu](./_implementation/move_verification.json) cho phép kiểm tra việc di chuyển. Hash file không đồng nghĩa mọi chương trình upstream vẫn chạy tại vị trí mới; chúng được lưu làm tài liệu tham khảo.

**Số file không phải số định nghĩa skill độc lập:** 420 file là con trỏ văn bản một dòng đến Markdown khác (phần lớn trong `.gemini/skills`); 11 con trỏ có đích không tồn tại trong checkout. Ngoài chúng, 4 tài liệu không qua kiểm tra frontmatter name/description (gồm mẫu/hướng dẫn và một lỗi parse). Inventory ghi loại file, đích con trỏ và lỗi parse. Không tự sửa các bản upstream trong kho tham khảo hoặc biến mọi con trỏ thành skill đang bật.

`.ignore` loại kho tham khảo, cache và file nhị phân khỏi tìm kiếm mặc định; `.gitignore` ngăn đưa cache/audio sinh ra vào Git. Không xóa `.git`, license, môi trường hoặc model của upstream. Catalog cũ được lưu trong `Data/Language/_catalog/_archive/20260908`, giữ bộ kế hoạch mới nhất tại chỗ.

## Kiểm tra và sửa skill đang duy trì

| Skill | Đã làm | Giới hạn nghiệm thu |
|---|---|---|
| audio-transcribe-local | Thêm inventory/hash, tiền xử lý, CUDA DLL setup, VAD, checkpoint từng chunk, fallback OOM, báo cáo chất lượng, gate biên tập và PKM | Kết quả từng nguồn nằm trong [INDEX](../Transcripts/INDEX.md); tất cả chờ nghe duyệt |
| learn-this | Thay phần điều phối bash/macOS bằng hướng dẫn Windows; thêm route audio local; sửa link | Đã kiểm đường dẫn; việc trích nội dung phụ thuộc skill được gọi |
| youtube-transcript-pro | Sửa fetch theo URL/ngôn ngữ, chọn đúng file phụ đề của video, ưu tiên phụ đề thủ công; loại trùng caption cuốn; fallback audio dùng pipeline local | 4 fixture test đạt; chưa nghiệm thu tải phụ đề trực tiếp qua mạng |
| youtube-transcript-basic | Đồng nhất name trong frontmatter với thư mục | Đã đọc API fetch hiện có; chưa chạy tải mạng |
| book-insight | Chạy 27 test và kiểm bằng chứng hai bộ đầu ra hiện có | Không cần sửa pipeline; xem đính chính bên dưới |
| ChangePdfToText | Sửa đường dẫn tài liệu và thư mục mặc định theo vị trí file | CLI trích text PDF fixture đạt; OCR chưa sẵn sàng vì thiếu pdf2image, Tesseract/Poppler executable |
| article-extractor | Kiểm phụ thuộc | Chưa có trafilatura/reader; chưa kiểm runtime, chưa tự cài |
| ship-learn-next, session-log, scrum-sage, unblock-action | Giữ nội dung, kiểm kê rõ | Chưa nghiệm thu workflow bằng tác vụ thực tế |

`RECOVERY_PLAN.md` trong workspace lưu trữ đã được sửa để chỉ đến các script đang duy trì trước khi chuyển sang Reference. Đường dẫn mặc định trong công cụ tổ chức `Data/Language/_tools/language_library_organizer.py` cũng đã được sửa theo vị trí file.

## Đính chính kết luận ban đầu

- **book-insight không chỉ nhận YouTube.** Nó hỗ trợ text sách và ghi chú; bộ test hiện tại chạy xanh 27/27.
- Hai file rejected/lowconf rỗng **không chứng minh gate vô tác dụng**. Hai bộ đầu ra được kiểm có 32 claim mỗi bộ, quote khớp nguồn và confidence nằm trong khoảng 70–87 sau cap; không có trường hợp bắt buộc phải loại trong dữ liệu đó.
- Ba tên script không tồn tại `fetch_transcript.py`, `clean_transcript.py`, `generate_summary.py` nằm trong **RECOVERY_PLAN cũ**, không phải trong SKILL.md của youtube-transcript-pro như audit ban đầu ghi. Lỗi fallback `ffmpeg whisper` là có thật và đã thay.
- Số skill được nối không cho biết số skill thực sự được dùng. Không suy lịch sử sử dụng từ symlink hoặc thư mục Plan rỗng.
- Không kết luận toàn bộ 1.123 skill upstream hỏng. Chúng được kiểm kê cấu trúc, không được chạy toàn bộ hoặc cài mọi phụ thuộc.

## Kiểm thử và vận hành

Bốn suite hiện có: audio 15 test, YouTube 4, bảo trì/di chuyển/PDF 5, book-insight 27 (**51 test**). Suite bảo trì kiểm dry-run, apply, chạy lại, rollback, xung đột, thoát khỏi root và đích junction; suite audio kiểm OOM/fallback, tiếp tục chunk sau gián đoạn, resume và provenance, lỗi input, timestamp trên một giờ, chất lượng và gate bằng chứng.

Chạy kiểm tra từ Collection:

```powershell
python -X utf8 -B Data\Plan\_implementation\verify_collection.py --tests
# Sau khi toàn bộ transcript và biên tập hoàn tất:
python -X utf8 -B Data\Plan\_implementation\verify_collection.py --tests --final
```

Log từng suite ở [_implementation](./_implementation/); kết quả `verification.json` phản ánh lần chạy gần nhất, `FINAL_VERIFICATION.json` là kiểm tra đủ bộ sau cùng. Các log/test là bằng chứng kỹ thuật, không thay thế nghe nghiệm thu.

[Kiểm chứng cuối](./_implementation/FINAL_VERIFICATION.json) đã đạt: 51 test, 12 nguồn hoàn tất ASR và biên tập, 13 file gốc giữ nguyên hash, không lỗi provenance hoặc liên kết. Nghe duyệt vẫn pending.

Khôi phục vị trí từ manifest nếu cần:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File Data\Plan\_implementation\reorganize.ps1 -Mode Rollback
```

Script chỉ xử lý đường dẫn bên trong Collection và từ chối ghi đè khi có xung đột. `ExecutionPolicy Bypass` chỉ áp dụng tiến trình gọi script, không đổi chính sách hệ thống. Bản sao trước sửa tài liệu/mã nằm trong `_implementation/before`.

## Phần còn lại có chủ đích

Nghe đối chiếu và xác định người nói chờ người dùng. Không tự sửa torch, cài diarization, xin token, cài OCR hoặc đăng nhập dịch vụ ngoài. Đây là những khả năng bổ sung; pipeline ASR hiện tại đã dùng được CUDA mà không thay môi trường torch của dự án khác.
