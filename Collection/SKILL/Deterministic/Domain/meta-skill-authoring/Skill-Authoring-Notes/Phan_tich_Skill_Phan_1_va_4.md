# Phân Tích Hướng Dẫn Xây Dựng Skill Cho Claude

## PHẦN 1: SKILL LÀ GÌ?

### Định nghĩa

Skill = **thư mục chứa hướng dẫn** giúp Claude xử lý tác vụ/quy trình cụ thể một cách nhất quán

### Cấu trúc file/thư mục

```
skill-name/
├── SKILL.md          # BẮT BUỘC - markdown + YAML frontmatter
├── scripts/         # TÙY CHỌN - code thực thi
│   ├── process.py
│   └── validate.sh
├── references/     # TÙY CHỌN - tài liệu tham khảo
│   └── api-guide.md
└── assets/          # TÙY CHỌN - template, hình ảnh
```

### 3 nguyên tắc cốt lõi

| Nguyên tắc | Ý nghĩa |
|-----------|---------|
| **Tiết lộ dần** | Claude chỉ đọc phần cần thiết (frontmatter → hướng dẫn → tài liệu) |
| **Kết hợp được** | Skill của bạn nên hoạt động với các skill khác, không giả định là duy nhất |
| **Di chuyển được** | Hoạt động trên cả Claude.ai, Claude Code, API mà không cần sửa đổi |

### Skill vs MCP - Khi nào dùng?

| MCP | Skill |
|-----|-------|
| Kết nối Claude với công cụ (Notion, Linear, Figma...) | Dạy Claude cách SỬ DỤNG công cụ đó |
| Cung cấp truy cập dữ liệu thời gian thực | Nắm bắt quy trình & best practices |
| Claude có thể làm gì | Claude nên làm như thế nào |

---

## PHẦN 4: YAML FRONT MATTER (QUAN TRỌNG NHẤT)

Đây là cách Claude **quyết định** có nhận ra skill hay không

### Cấu trúc bắt buộc

```yaml
---
name: ten-skill-kebab-case
description: Skill làm gì. Dùng khi người dùng yêu cầu [cụm từ kích hoạt].
---
```

### Trường bắt buộc

| Trường | Yêu cầu | Ví dụ |
|--------|---------|-------|
| `name` | kebab-case, không khoảng trắng, không chữ hoa | `frontend-design` |
| `description` | PHẢI bao gồm CẢ: (1) Skill làm gì + (2) Khi nào dùng | Xem bên dưới |

### Ví dụ description ĐÚNG & SAI

#### ✅ TỐT - mô tả rõ ràng có trigger words

```yaml
description: Phân tích tập thiết kế Figma và tạo tài liệu bàn giao 
cho nhà phát triển. Dùng khi người dùng tải lên tập .fig, 
yêu cầu "đọc thiết kế" hoặc "design-to-code".
```

#### ✅ TỐT - bao gồm trigger words

```yaml
description: Quản lý quy trình dự án Linear bao gồm lập kế hoạch 
sprint, tạo task và theo dõi trạng thái. Dùng khi người dùng 
đề cập "sprint", "Linear tasks", hoặc yêu cầu "tạo tickets".
```

#### ❌ SAI - quá mơ hồ

```yaml
description: Giúp đở với các dự án.
```

#### ❌ SAI - thiếu điều kiện kích hoạt

```yaml
description: Tạo hệ thống tài liệu nhiều trang phức tạp.
```

### Các trường tùy chọn

```yaml
---
name: ten-skill
description: Mô tả ngắn

# Tùy chọn
license: MIT
metadata:
  author: Tên công ty
  version: 1.0.0
  mcp-server: ten-server-mcp
  category: nang-suat
  tags: [quan-ly-du-an, tu-dong-hoa]
---
```

### Hạn chế bảo mật

- KHÔNG dùng dấu ngoặc nhọn XML (`<` hoặc `>`)
- Không dùng từ "claude" hoặc "anthropic" trong tên skill (đã đặt trước)