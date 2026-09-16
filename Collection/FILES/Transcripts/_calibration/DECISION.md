# Cấu hình chạy lô

Chọn large-v3, CUDA/int8_float16, không afftdn, không initial_prompt chuyên ngành.
Đã chạy đủ 2 nguồn × 2 model × 2 biến thể trên 300 giây đầu; xem comparison.csv/json.

Mẫu thầy Lâm: large-v3 baseline và denoise đều 0% đoạn vượt ngưỡng triage, nhưng
baseline giữ được "SQL Injection" tại 02:40 trong khi denoise nhận thành "SPM Jackson".
Không có bản chuẩn do người nghe tạo nên không báo WER hay kết luận chắc chắn về độ chính xác.
Medium có 10,34% (baseline) / 45,61% (denoise) đoạn bị cờ trên cùng mẫu.

Voice 016: large-v3 baseline chỉ có 5 đoạn; denoise chỉ có 3 đoạn và cả ba giống
câu quảng cáo thường gặp trong hallucination. Medium có 100% đoạn bị cờ ở cả hai biến thể.
Đây không phải căn cứ coi những câu quảng cáo có thật trong nguồn. Cần nghe đối chiếu;
không rút tri thức từ các câu này. Bộ lô vẫn xử lý đầy đủ và giữ raw làm dấu vết.

Suy luận CUDA đã thành công sau đăng ký DLL cublas/cudnn có sẵn trong tiến trình;
không cài thêm package, không sửa torch hay PATH hệ thống.

Thời gian large-v3 trên mẫu 5 phút khoảng 57–74 giây gồm tải model, nên dự trù
khoảng 2 giờ cho cả lô; sẽ cập nhật bằng run_log thực tế, không coi đây là cam kết.
