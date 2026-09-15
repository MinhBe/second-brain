import re

# Read the original file
with open(r"C:\Projects\Collection\Skill\DownloadTranscriptyYtb\all_transcripts.txt", "r", encoding="utf-8") as f:
    content = f.read()

# Split by transcript sections
transcripts = re.split(r'(=== Transcript: [^=]+ ===)', content)
transcripts = [t for t in transcripts if t.strip()]

# Pair headers with content
paired = []
for i in range(0, len(transcripts)-1, 2):
    if transcripts[i].startswith("=== Transcript:"):
        paired.append((transcripts[i], transcripts[i+1]))

# Summaries for each video
summaries = {
    "uGouKEuej4k": "Video chia sẻ lộ trình 6 tháng tự học Data Analytics với AI năm 2026. Tác giả Mask giới thiệu 4 trụ cột: kiến thức DA, công cụ (SQL, Python), AI/Machine Learning, và kỹ năng mềm. Chi tiết từng tháng: tháng 1-2 học Excel/SQL, tháng 3 học tư duy phân tích/Power BI, tháng 4 học Python, tháng 5 học Machine Learning, tháng 6 xây dựng portfolio với các dự án Marketing/Sales/Risk analytics.",
    
    "m9yayKNK7yw": "Video chia sẻ 5 kỹ năng để trở thành Data Analyst giỏi: (1) Tư duy phân tich (Analytical thinking) sử dụng MECE Framework, IC Scoring; (2) Kiến thức thống kê kinh doanh (descriptive/inferential statistics, hypothesis testing); (3) Hiểu luồng ETL và data modeling; (4) Kỹ năng trình bày slide chuyên nghiệp (SCQA, Pyramid principle); (5) Khả năng tự học và thích nghi với AI tools (ChatGPT, Claude, Perplexity, Zapier).",
    
    "VIyK8Tq3YRw": "Video nhấn mạnh tầm quan trọng của thống kê trong phân tích dữ liệu và cuộc sống. Tác giả giải thích các ngụy biện thống kê (survivor bias), cách áp dụng descriptive statistics (min, max, median, standard deviation) và percentile để ra quyết định kinh doanh (ví dụ: hạn mức chuyển tiền ngân hàng). Video cung cấp danh sách kiến thức thống kê cần nắm: loại dữ liệu, chỉ số mô tả, chọn mẫu, kiểm định giả thuyết, hồi quy.",
    
    "qkATC8JO3lM": "Video giới thiệu 9 quyển sách tâm đắc cho người học Data Analytics: (1) Data Science for Business - tổng quan nghề nghiệp; (2) HP Data Analytics Basic for Managers - cho nhà quản lý; (3) Think with Data - tư duy 'Why before house'; (4) Problem Solving 101 - kỹ năng giải quyết vấn đề; (5) Statistics for Data Scientists; (6) Storytelling with Data - trình bày trực quan; (7) SQL for Data Analytics; (8) Python for Data Analysis. Tác giả nhấn mạnh DA giỏi cần cả tư duy, thống kê, và kỹ năng mềm.",
    
    "TbCTOBKv1P4": "Video phân tích chi tiết về nghề Data Analyst: vai trò trong doanh nghiệp, cấu trúc team (Data Analyst, Data Scientist, Data Engineer, Data Architect), mức lương (12-40 triệu VND tùy kinh nghiệm), và các vị trí phù hợp với từng background (Kinh tế, IT, Data Science). Tác giả khuyên nên chọn công ty có hệ thống data tốt (ngân hàng, fintech, e-commerce) để học hỏi nhanh.",
    
    "lqkocF3j2f0": "Video chia sẻ 5 thử thách lớn nhất của Data Analyst: (1) Thiếu kiến thức chuyên ngành (domain knowledge); (2) Công ty chưa có database/system chuẩn chỉnh, phải tốn nhiều thời gian thu thập/xử lý dữ liệu; (3) Thiếu tài liệu mô tả dữ liệu (data dictionary); (4) Không có quyền truy cập dữ liệu, phải chờ đợi phê duyệt; (5) Chỉ 10-20% thời gian dành cho phân tích, còn lại là xử lý dữ liệu. Tác giả khuyên nên hỏi Google/ChatGPT/đồng nghiệp để làm việc hiệu quả hơn.",
    
    "0O0iHqK2fh4": "Video so sánh 2 chứng chỉ Google Data Analytics Professional Certificate và IBM Data Analyst Professional Certificate. Google: 240 giờ, tập trung vào Excel, SQL, Tableau, phù hợp người mới bắt đầu, có các chuyên gia Google hướng dẫn. IBM: 140 giờ, tập trung vào Excel, SQL, Python (Pandas, Matplotlib, Seaborn), phù hợp người muốn học sâu Python. Cả hai đều có thể học free qua tài trợ từ Coursera.",
    
    "CoY8145FxFE": "Video giải thích chi tiết nghề Data Analyst: quá trình phân tích dữ liệu (xác định vấn đề → thu thập → chuẩn bị → phân tích → trình bày), các nhóm kỹ năng cần có (technical skill: SQL/Python/BI tools, domain knowledge, soft skills: communication/problem solving/presentation). So sánh DA vs Data Scientist (DS thiên về nghiên cứu/mô hình dự báo) vs Business Analyst (BA thiên về nghiệp vụ/business requirements)."
}

# Build new content
new_content = ""

for header, body in paired:
    # Extract video ID
    match = re.search(r'=== Transcript: ([^=]+) ===', header)
    if match:
        video_id = match.group(1).strip()
        
        # Add transcript
        new_content += header + "\n"
        new_content += body.strip() + "\n\n"
        
        # Add summary
        new_content += "=== Summary ===\n"
        if video_id in summaries:
            new_content += summaries[video_id] + "\n\n"
        else:
            new_content += "Summary not available\n\n"

# Add overall summary
new_content += "=" * 50 + "\n"
new_content += "=== OVERALL SUMMARY ===\n"
new_content += """
Tất cả 8 video đều được tạo bởi tác giả Mask - một Data Analyst với 6 năm kinh nghiệm tại VNG, Techbank. 

Nội dung chính xoay quanh:
1. Lộ trình tự học Data Analytics 6 tháng với AI (Excel → SQL → Power BI → Python → Machine Learning → Portfolio)
2. Các kỹ năng cốt lõi: Tư duy phân tích (Analytical thinking), Thống kê kinh doanh, Trực quan hóa dữ liệu, Kỹ năng trình bày
3. Giới thiệu tài liệu học tập: 9 quyển sách tâm đắc (Data Science for Business, Storytelling with Data, Statistics for Data Scientists...)
4. Thực trạng nghề nghiệp: Mức lương DA (12-40 triệu), cấu trúc team data, các vị trí (DA, DS, DE, BA)
5. Thử thách: Xử lý dữ liệu không chuẩn, thiếu domain knowledge, quy trình phức tạp
6. Chứng chỉ: So sánh Google Data Analytics vs IBM Data Analyst Professional Certificate
7. Ứng dụng AI trong công việc: ChatGPT, Claude, Perplexity để hỗ trợ code, research, tự động hóa

Thông điệp xuyên suốt: DA giỏi không chỉ giỏi công cụ mà còn cần tư duy logic, kiến thức thống kê vững chắc và kỹ năng mềm tốt.
"""

# Write new file
with open(r"C:\Projects\Collection\Skill\DownloadTranscriptyYtb\all_transcripts.txt", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Da tai to chuc file thanh cong!")
print(f"So luong transcript: {len(paired)}")
