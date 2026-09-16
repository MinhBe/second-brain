---
name: youtube-transcript-pro
description: Download YouTube video transcripts and generate analysis. Use when user provides a YouTube URL and asks for transcript, subtitles, captions, summary, key points, or TL;DR of a YouTube video. Supports multiple languages and provides clean text with optional summary.
allowed-tools: Bash,Read,Write
metadata:
  author: Pro
  version: 1.0.0
---

# YouTube Transcript Pro

Kết hợp download transcript + phân tích cơ bản từ YouTube videos.

## When to Activate

Kích hoạt khi user:
- Cung cấp YouTube URL và muốn transcript
- Yêu cầu "download transcript", "get captions", "get subtitles"
- Yêu cầu "summarize", "summary", "TL;DR", "key points" từ video
- Muốn "transcribe" một YouTube video

## How It Works

### 3 Tùy Chọn Download (theo thứ tự ưu tiên):

1. **Manual Subtitles** (ưu tiên cao nhất)
2. **Auto-Generated Subtitles** (thường có sẵn)
3. **Whisper Transcription** (last resort - cần xác nhận user)

### Quy Trình 5 Bước:

```
Bước 1: Extract video ID từ URL
Bước 2: Check subtitles available
Bước 3: Download transcript
Bước 4: Clean + Deduplicate
Bước 5: Tạo summary + key points (tùy chọn)
```

## Steps

### Bước 1: Extract Video ID

Từ các định dạng URL:
| Format | Cách lấy |
|--------|----------|
| `youtube.com/watch?v=VIDEO_ID` | `v=` parameter |
| `youtu.be/VIDEO_ID` | path segment |
| `youtube.com/embed/VIDEO_ID` | path segment |
| 11-char ID | dùng trực tiếp |

### Bước 2: Check Available Subtitles

```bash
yt-dlp --list-subs "YOUTUBE_URL"
```

### Bước 3: Download

```bash
# Thử manual trước
yt-dlp --write-sub --skip-download --output "transcript" "URL"

# Fallback to auto
yt-dlp --write-auto-sub --skip-download --output "transcript" "URL"
```

### Bước 4: Clean Transcript

Loại bỏ duplicate VTT lines:

```bash
python3 -c "
import sys, re
seen = set()
with open('transcript.en.vtt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('WEBVTT') and not line.startswith('Kind:') and not line.startswith('Language:') and '-->' not in line:
            clean = re.sub('<[^>]*>', '', line)
            clean = clean.replace('&amp;', '&').replace('&gt;', '>').replace('&lt;', '<')
            if clean and clean not in seen:
                print(clean)
                seen.add(clean)
" > output.txt
```

### Bước 5: Generate Summary (Optional)

Nếu user yêu cầu summary, phân tích transcript:

**Summary (3-5 câu):**
- Câu 1: Video về gì? (main topic)
- Câu 2: Key insight chính
- Câu 3-5: Takeaway quan trọng

**Key Points (5-10 bullets):**
- Mỗi bullet: 1 concept/claim + tại sao quan trọng

## Installation

### Check yt-dlp:

```bash
which yt-dlp || command -v yt-dlp
```

### Install nếu cần:

```bash
# macOS
brew install yt-dlp

# Linux
sudo apt update && sudo apt install -y yt-dlp

# pip (all systems)
pip3 install yt-dlp
```

## Output

- **Transcript**: Plain text, cleaned, deduplicated
- **Summary**: 3-5 câu (nếu yêu cầu)
- **Key Points**: 5-10 bullets (nếu yêu cầu)
- **Filename**: `{video_title}.txt`

## Error Handling

| Lỗi | Xử lý |
|-----|-------|
| Captions disabled | Thông báo, gợi ý video khác |
| Private/removed video | Thông báo lỗi cụ thể |
| No subtitles | Offer Whisper transcription |
| Invalid URL | Yêu cầu URL đúng format |
| yt-dlp not installed | Gợi ý cài đặt |

## Best Practices

- ✅ Always check `--list-subs` trước
- ✅ Deduplicate VTT output
- ✅ Ask user trước khi dùng Whisper (tốn time + storage)
- ✅ Clean filename (thay `/`, `:`, `?` bằng `-`)
- ✅ Provide feedback rõ ràng mỗi step

---

*Skill được tạo dựa trên nghiên cứu tapestry + video-lens + hướng dẫn chuẩn*