# Đối chiếu — Mentor — buổi 2

| Tên đối chiếu | Tên gọi mới | Thời lượng | Chủ đề |
|---|---|---|---|
| voice-012 | Mentor — buổi 2 | 00:47:33 | GAN SQLi — reward function, pretraining, thử qua WAF |

## Nội dung cuộc hội thoại

Cũng về đề tài GAN SQLi (phần reward function, pretraining, thử qua WAF). Yêu cầu định nghĩa rõ chỉ số Delta Recall, chứng minh từng cải tiến bằng thử nghiệm trước/sau thay vì chỉ nêu tên. Có phần quan trọng: HTTP 200 khi thử qua WAF không chứng minh khai thác thành công, vì kịch bản không có database để kiểm chứng — chỉ nói lên là qua được bộ lọc hoặc là nhiễu.

## Ý nghĩa / điểm rút ra

N1 — Định nghĩa quy ước và thước đo trước khi đưa kết quả: căn cứ chia mức mất cân bằng, định nghĩa và mốc so sánh của Delta Recall.
N2 — Chứng minh thay đổi thay vì liệt kê tên cải tiến: thử trước/sau từng thay đổi, giải thích mô hình gốc trước.
N3 — Giới hạn kết luận từ phản hồi WAF: HTTP 200 không chứng minh khai thác thành công nếu không có database; phân biệt qua bộ lọc, có cấu trúc SQL và tấn công thực tế.

## Files trong thư mục

- `DOI_CHIEU.md`
- `DOI_CHIEU.xlsx`
- `_editorial`
- `_work`
- `voice-012_KNOWLEDGE.md`
- `voice-012_TRANSCRIPT.md`
