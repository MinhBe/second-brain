# Nghiệm thu

- Hash nguồn trước/sau không đổi; duplicate không nhận dạng lần hai.
- Model/device/config thực tế có trong raw và run log; DLL smoke test có chạy suy luận.
- Mỗi file có raw JSON/SRT/TXT, quality report và tiến độ; file lỗi không mang trạng thái xong.
- Đoạn timestamp nằm trong thời lượng nguồn, không thiếu ID khi biên tập; bảo toàn dấu phủ định.
- Không dùng logprob làm WER; khoảng trống ≥30 giây được báo để phân biệt im lặng và bỏ sót.
- Claim có quote/ID truy nguồn, node có claim; câu hỏi và ứng dụng đề xuất được phân biệt.
- INDEX đủ nguồn kể cả duplicate, pending và no usable speech.
- Nghe mẫu 2 phút ở ba file ngắn/vừa/dài và ưu tiên đoạn quality report đánh dấu.
  Khi chưa nghe: báo chờ nghe duyệt, không sửa thành đã duyệt.
- Rerun cùng config tái sử dụng kết quả hợp lệ; đổi nguồn/config làm checkpoint cũ mất hiệu lực.
