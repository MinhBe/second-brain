# Báo cáo xử lý ghi âm

Cập nhật UTC: 2026-09-13T14:02:14.825666+00:00

16/16 nguồn khác nhau hoàn tất ASR (17 file, gồm 1 bản trùng byte); 7157 segment, 88 claim và 43 node đã biên tập.
Thời lượng nguồn khác nhau: 12.84 giờ. Tổng processing ghi trong raw: 105.1 phút (gồm tải model; không gồm thời gian biên tập).

1096/7157 segment (15.31%) bị cờ âm học. 3228 segment được đánh dấu nghi lỗi khi rà văn bản. Hai tập có thể trùng nhau; không cộng thành tỷ lệ lỗi.
Không có bản chuẩn để tính WER. Ít cờ ASR không bảo đảm từ ngữ hay kiến thức đúng. Tất cả chờ nghe duyệt.

| Nguồn | Trạng thái | Segment | Cờ âm học | Cờ biên tập | Đã rà | Claim/node |
|---|---:|---:|---:|---:|---:|---:|
| [Voice 015.m4a](../voice-015_TRANSCRIPT.md) | asr_complete | 1 | 0 | 1 | 1 | 0/0 |
| [Voice 014.m4a](../voice-014_TRANSCRIPT.md) | asr_complete | 13 | 0 | 6 | 13 | 2/1 |
| [Voice 001.m4a](../voice-001_TRANSCRIPT.md) | asr_complete | 1 | 0 | 1 | 1 | 0/0 |
| [Voice 016.m4a](../voice-016_TRANSCRIPT.md) | asr_complete | 5 | 1 | 5 | 5 | 0/0 |
| [Record thầy Lâm (2).m4a](../Thầy Lâm\record-thay-lam-2_TRANSCRIPT.md) | asr_complete | 245 | 0 | 49 | 245 | 7/4 |
| [Voice 009.m4a](../Mentor\Mentor — buổi 1\voice-009_TRANSCRIPT.md) | asr_complete | 451 | 0 | 102 | 451 | 7/4 |
| [Voice 002.m4a](../voice-002_TRANSCRIPT.md) | asr_complete | 525 | 0 | 137 | 525 | 10/5 |
| [Voice 011.m4a](../Mentor\Mentor — buổi 7\voice-011_TRANSCRIPT.md) | asr_complete | 403 | 140 | 163 | 403 | 8/4 |
| [Voice 012.m4a](../Mentor\Mentor — buổi 2\voice-012_TRANSCRIPT.md) | asr_complete | 450 | 52 | 134 | 450 | 6/3 |
| [Anh Minh.m4a](../anh-minh_TRANSCRIPT.md) | asr_complete | 63 | 0 | 33 | 63 | 4/2 |
| [Anh Hải.m4a](../anh-hai_TRANSCRIPT.md) | asr_complete | 205 | 0 | 116 | 205 | 7/3 |
| [Voice 013.m4a](../Mentor\Mentor — buổi 3\voice-013_TRANSCRIPT.md) | asr_complete | 541 | 6 | 111 | 541 | 7/3 |
| [Voice 018.m4a](../Anh Tuấn Anh\voice-018_TRANSCRIPT.md) | asr_complete | 1124 | 174 | 151 | 1124 | 7/3 |
| [Voice 010.m4a](../Mentor\Mentor — buổi 6\voice-010_TRANSCRIPT.md) | asr_complete | 1052 | 126 | 366 | 1052 | 8/4 |
| [Recording (2).m4a](../Mentor\Mentor — buổi 5 (hội đồng)\recording-2_TRANSCRIPT.md) | asr_complete | 951 | 185 | 833 | 951 | 7/3 |
| [Voice 017.m4a](../Mentor\Mentor — buổi 4\voice-017_TRANSCRIPT.md) | asr_complete | 1127 | 412 | 1020 | 1127 | 8/4 |

[Nghe đối chiếu](../_review/LISTENING_REVIEW.md) · [Mục lục](../INDEX.md) · [Run log](run_log.csv)

Bản Voice 010 (2) trùng byte được giữ nguyên ở Recording và không xử lý lại. Voice 001 hầu như không có lời nói (ASR bắt được một câu quảng cáo lặp lại) và Voice 015/016 hiện không đủ căn cứ rút tri thức; các bản này vẫn có transcript và ghi chú giới hạn.

Voice 017 và Recording (2) có nội dung tương ứng dù khác hash; tổng giờ file không phải tổng nội dung độc nhất. [Xem đối chiếu](../CROSS_SOURCE_REVIEW.md).
