# Kế hoạch triển khai ghi âm → transcript → tri thức PKM

Lập 2026-09-08, cập nhật triển khai 2026-09-09. Phạm vi đã được duyệt gồm cả pipeline audio và sửa/dọn kho skill trong [SKILL_AUDIT.md](SKILL_AUDIT.md). Bản kế hoạch trước thực hiện được giữ trong [_implementation/before](./_implementation/before/).

**Hoàn tất phần kỹ thuật:** 12/12 file khác hash được xử lý bằng large-v3/CUDA, 6.363 segment đã rà văn bản, 67 claim và 33 node. Tổng thời gian processing ghi trong raw là 92,5 phút. 51 test đạt; kiểm hash nguồn, checkpoint, độ phủ biên tập, dẫn chứng, liên kết và mẫu nghe không có lỗi. Xem [kiểm chứng cuối](./_implementation/FINAL_VERIFICATION.json) và [báo cáo chất lượng](../Transcripts/_reports/SUMMARY.md). Phần nghe nghiệm thu vẫn chờ người dùng; không coi đây là transcript đã xác nhận bằng tai.

## Đầu vào và đầu ra

- 13 file M4A trong `Data/Recording`; 12 nguồn khác nhau, tổng khoảng 10,37 giờ.
- `Voice 010 (2).m4a` trùng SHA-256 với `Voice 010.m4a`: bỏ lượt nhận dạng lặp, giữ nguyên cả hai file nguồn.
- `Voice 017` và `Recording (2)` khác hash nhưng có nhiều nội dung tương ứng; giữ riêng hai timeline, không coi là hai nguồn xác nhận độc lập. 10,37 giờ là tổng thời lượng file khác hash.
- Mỗi nguồn có raw JSON/SRT/TXT, WAV trung gian, checkpoint chunk, báo cáo chất lượng, transcript phân chủ đề và tri thức có dẫn chứng.
- [INDEX](../Transcripts/INDEX.md) phản ánh trạng thái từng nguồn; [Schema Map](../Transcripts/SCHEMA_MAP.md) nối các chủ đề xuyên file.
- [Bộ nghe duyệt](../Transcripts/_review/LISTENING_REVIEW.md) gồm ba mẫu 2 phút ngắn/vừa/dài và Voice 016 cần ưu tiên. **Chưa nghe nghiệm thu**, theo quyết định nghe đối chiếu sau khi xử lý lô.

## Quyết định đã thực hiện

| Hạng mục | Cấu hình/chính sách thực tế |
|---|---|
| ASR | faster-whisper large-v3, CUDA, int8_float16; model đã có cache, local_files_only |
| Fallback | Chỉ khi OOM: worker mới, medium/int8/beam 3; lỗi khác được ghi và lô tiếp tục |
| Tiền xử lý | WAV 16 kHz mono, loudnorm; giữ timeline, không cắt im lặng khỏi nguồn |
| Khử nhiễu | Không bật afftdn trong lô; đã so sánh 8 lượt hiệu chỉnh, không đủ lợi ích để bật mặc định |
| Giải mã | tiếng Việt, beam 5, best_of 5, temperature 0/0,2/0,4, VAD silence 500 ms/pad 200 ms, word timestamps, không dùng previous text |
| Prompt | Không dùng initial_prompt ngành chung vì nguồn có nhiều chủ đề và chưa biết trước; không áp từ điển thay hàng loạt |
| Chạy dài | Chunk 600 giây, overlap 2 giây, gán từ theo midpoint vào core; checkpoint atomic sau mỗi chunk |
| GPU Windows | Đăng ký DLL cuBLAS/cuDNN có sẵn bằng os.add_dll_directory và PATH của tiến trình; đã suy luận thật, không chỉ load model |
| Môi trường | Không cài package, không đổi torch/torchaudio hay PATH hệ thống; không gọi API LLM bên ngoài |
| Biên tập | Trợ lý trong phiên đọc toàn bộ segment từng nguồn; chia chủ đề, giữ dấu vết raw, đánh dấu nghi lỗi thay vì đoán nghĩa |
| Người nói | Giữ [Người nói?]; không gán vai trò chỉ vì đó là câu hỏi hay câu trả lời |
| PKM | Raw Inbox, SLIM Knowledge Nodes, Claim Ledger, Schema Map, Practice Log đề xuất và lịch ôn +1/+4/+12/+30 |
| Tin cậy | Confidence diễn giải thấp/vừa/cao có lý do; mọi claim chưa kiểm chứng ngoài, trạng thái nghe riêng biệt |

Kết quả hiệu chỉnh và giới hạn nằm trong [DECISION](../Transcripts/_calibration/DECISION.md), [comparison.csv](../Transcripts/_calibration/comparison.csv). Không có transcript chuẩn do người nghe tạo nên không báo WER hoặc coi điểm ASR là độ đúng của kiến thức.

Khác với đề xuất ban đầu, không tự suy người nói, không nhét thuật ngữ ngành vào mọi file, không bật denoise mặc định và không xóa câu nghi hallucination khỏi raw. Các đoạn nhiễu vẫn có timestamp để đối chiếu. Các tên mô hình, con số hoặc phủ định chưa chắc không được tự sửa.

## Cấu trúc đã tạo

```text
Data/Transcripts/
  _work/<slug>/
    audio_16k.wav, audio_16k.meta.json
    chunks/0000.json ... , progress.json
    raw.json, raw.srt, raw.txt
    quality.json, quality_report.md, worker.log
    editorial.json, knowledge.json, assembly.json
    clean.md, knowledge.md
  _editorial/<slug>.json             ghi chú biên tập thủ công, gắn hash raw
  _calibration/                     so sánh hai model × hai tiền xử lý × hai mẫu
  _reports/                        inventory, run_log, checkpoint
  _review/                         mẫu nghe và phiếu chờ duyệt
  <slug>_TRANSCRIPT.md
  <slug>_KNOWLEDGE.md
  INDEX.md, SCHEMA_MAP.md
Skills/Domain/content-production/personal-content-workflow/audio-transcribe-local/
  SKILL.md, scripts/, references/, tests/
Data/Plan/_implementation/
  before/, tests/, moves.json, moves.executed.jsonl
  maintain_collection.py, reorganize.ps1, verify_collection.py
  publish_editorial.py, prepare_listening.py
```

Raw được gắn SHA-256 nguồn, cấu hình và content hash. Gate xuất bản yêu cầu biên tập bao phủ mọi segment, quote khớp chính xác raw và node trỏ đến claim tồn tại. Khi raw đổi, biên tập cũ bị từ chối. Không đủ lời nói rõ vẫn có bộ tài liệu ghi rõ chưa đủ căn cứ, không sinh tri thức cho đủ số lượng.

## Chạy lại và sử dụng

Từ `C:\Users\Admin\Documents\Collection`:

```powershell
# Tiếp tục lô: cache hợp lệ được dùng lại, nguồn/config thay đổi được xử lý lại.
python -X utf8 -u -B Skills\Domain\content-production\personal-content-workflow\audio-transcribe-local\scripts\transcribe.py --batch

# Nhận dạng một nguồn khác; thư mục output riêng cho mỗi nguồn.
python -X utf8 -B Skills\Domain\content-production\personal-content-workflow\audio-transcribe-local\scripts\transcribe.py --input "Data\Recording\Voice 014.m4a" --output "Data\Transcripts\_work\voice-014"

# Xuất lại những nguồn đã có editorial.json và knowledge.json hợp lệ.
python -X utf8 -B Skills\Domain\content-production\personal-content-workflow\audio-transcribe-local\scripts\assemble.py --all

# Kiểm đủ đầu ra, hash và bộ test.
python -X utf8 -B Data\Plan\_implementation\verify_collection.py --tests --final
```

`--force` chạy lại ASR; `--denoise` chỉ khi có bằng chứng cải thiện; `--seconds` dùng cho hiệu chỉnh một file. Nguồn mới chưa có biên tập sẽ chỉ có ASR; cần đọc, soạn editorial/knowledge rồi mới assemble. Không tự đánh dấu đã hiểu chỉ vì script chạy xong.

## Sửa và sắp xếp skill

Đã tạo skill audio và nối vào cả `.agents/skills` và `.claude/skills`. `learn-this` điều phối audio trước. YouTube fallback dùng lại ASR local; fetch phụ đề sửa chọn ngôn ngữ/file và caption cuốn. PDF converter và organizer dùng đường dẫn theo vị trí file.

Giữ 11 skill trong Skills, chuyển 1.123 skill tham khảo cùng package gốc sang Reference. 26 mục di chuyển đã xác nhận toàn vẹn 26.550 file thường. Không xóa source, lịch sử Git, license hoặc model. Có manifest/journal, dry-run và rollback chống ghi đè. [Audit](SKILL_AUDIT.md) và [Skills README](../../Skills/README.md) phân biệt rõ fixture test, kiểm cấu trúc và runtime chưa nghiệm thu.

## Nghiệm thu

| Điều kiện | Bằng chứng/trạng thái |
|---|---|
| 13 nguồn, một bản trùng | [inventory.csv](../Transcripts/_reports/inventory.csv), SHA-256 |
| CUDA suy luận thật | [run_log.csv](../Transcripts/_reports/run_log.csv), worker.log từng nguồn |
| Raw và báo cáo mỗi nguồn | `_work/<slug>`; kiểm bởi verify_collection |
| Transcript/PKM đủ 12 nguồn khác nhau | [INDEX](../Transcripts/INDEX.md); không đếm bản trùng thành tri thức mới |
| Gate bằng chứng và tests | `_implementation/test_*.log`, `FINAL_VERIFICATION.json` sau lần kiểm cuối |
| Toàn vẹn sau di chuyển | [move_verification.json](./_implementation/move_verification.json): không lỗi |
| Nghe đối chiếu ba mẫu | **Chờ người dùng** trong [phiếu duyệt](../Transcripts/_review/LISTENING_REVIEW.md) |

Kết thúc xử lý kỹ thuật không đồng nghĩa transcript đã được nghe xác nhận. Giữ trạng thái này rõ ở mọi đầu ra. Sau phản hồi nghe, sửa đúng segment trong editorial, bổ sung căn cứ rồi xuất lại tài liệu; không sửa đè raw.

## Backlog tùy chọn

Diarization thật, môi trường torch riêng, OCR đủ phụ thuộc, nghe so sánh hai kênh stereo và kiểm thử tải phụ đề trực tiếp. Không chặn lô hiện tại và không tự thay môi trường nghiên cứu đang dùng.
