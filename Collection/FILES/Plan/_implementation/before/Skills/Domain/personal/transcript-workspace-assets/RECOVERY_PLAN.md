# RECOVERY PLAN: TẠO YOUTUBE TRANSCRIPT SKILL CHUẨN

## MỤC TIÊU

Tạo 1 skill YouTube transcript + phân tích chuẩn nhất, kết hợp điểm mạnh từ các mẫu đã nghiên cứu.

---

## TỔNG KẾT CÁC MẪU ĐÃ HỌC

### 1. youtube-transcript-basic (gốc của bạn)
- **Công cụ**: youtube-transcript-api
- **Ưu điểm**: Đơn giản, dễ hiểu
- **Nhược điểm**: Chỉ lấy transcript thô, không có phân tích

### 2. youtube-transcript (tapestry)
- **Công cụ**: yt-dlp
- **Ưu điểm**: 3 tùy chọn download (manual → auto → whisper), post-processing tốt
- **Nhược điểm**: Không có phân tích/summary

### 3. video-lens (kar2phi) - THAM KHẢO
- **Công cụ**: youtube-transcript-api + yt-dlp
- **Ưu điểm**: Executive summary, key points, takeaway, timestamped outline, HTML report đẹp, gallery
- **Nhược điểm**: Phức tạp, cần nhiều script

---

## SKILL MỤC TIÊU

Skill cần đạt:
1. ✅ Download transcript từ YouTube (yt-dlp)
2. ✅ Làm sạch text (deduplicate VTT)
3. ✅ Tạo executive summary (3-5 câu)
4. ✅ Trích xuất key points (5-10 bullets)
5. ✅ Timestamp outline (các chủ đề theo thời gian)
6. ✅保存 file với tên đúng

---

## CÁC BƯỚC THỰC HIỆN

### Bước 1: Nghiên cứu các mẫu
```
Đọc youtube-transcript/SKILL.md (tapestry)
Đọc youtube-transcript-basic/SKILL.md
Tham khảo video-lens (https://github.com/kar2phi/video-lens)
```

### Bước 2: Tạo cấu trúc folder mới
```
youtube-transcript-pro/
├── SKILL.md           # Skill chuẩn mới
├── scripts/
│   ├── fetch_transcript.py
│   ├── clean_transcript.py
│   ├── generate_summary.py
│   └── render_html.py  # Optional
└── template.html       # Optional
```

### Bước 3: Viết SKILL.md
Nội dung cần có:
- Front-matter: name, description với trigger words
- Steps: Extract ID → Fetch → Clean → Summary → Output
- Error handling đầy đủ

### Bước 4: Viết scripts
- `fetch_transcript.py`: Download với yt-dlp
- `clean_transcript.py`: Deduplicate và làm sạch
- `generate_summary.py`: Tạo summary + key points (nếu cần)

### Bước 5: Test
```bash
# Test thử với 1 URL
uv run scripts/fetch_transcript.py "YOUTUBE_URL"
```

### Bước 6: Hoàn thiện
Cập nhật SKILL.md dựa trên kết quả test

---

## TRIỂN KHAI

### File cần tạo:
1. `C:\Projects\Collection\Skill\DownloadTranscriptyYtb\youtube-transcript-pro\SKILL.md`
2. `C:\Projects\Collection\Skill\DownloadTranscriptyYtb\youtube-transcript-pro\scripts\fetch.py`
3. `C:\Projects\Collection\Skill\DownloadTranscriptyYtb\youtube-transcript-pro\scripts\clean.py`

### Reference files:
- `C:\Projects\Collection\Skill\DownloadTranscriptyYtb\youtube-transcript\SKILL.md`
- `C:\Projects\Collection\Skill\DownloadTranscriptyYtb\youtube-transcript-basic\SKILL.md`

---

## CHECKLIST

- [ ] Đọc và phân tích 2 mẫu có sẵn
- [ ] Xác định cấu trúc skill mới
- [ ] Tạo folder youtube-transcript-pro
- [ ] Viết SKILL.md (front-matter + nội dung)
- [ ] Viết scripts cần thiết
- [ ] Test thử
- [ ] Hoàn thiện

---

## LINK THAM KHẢO

- Tapestry skills: https://github.com/michalparkola/tapestry-skills-for-claude-code
- Video lens: https://github.com/kar2phi/video-lens
- Hướng dẫn gốc: `C:\Projects\Collection\Skill\SkillCreate\Huong_dan_xay_dung_Skill_Cho_Claude.txt`

---

*Ngày tạo: 2026-05-05*
*Người tạo: Claude*