---
title: 9Router - Chuyển sang Ubuntu VM
date: 2026-09-21
tags: [9router, hermes, vm, ubuntu]
---

# 9Router - Chuyển sang Ubuntu VM

Mục tiêu: Hermes chạy trong VM Ubuntu (VMware Workstation) dùng được toàn bộ API key và OAuth token đã có trong 9Router trên Windows, **không copy tay từng key**.

## Dữ liệu 9Router nằm ở đâu trên Windows

Toàn bộ trong một thư mục:

```
C:\Users\Admin\AppData\Roaming\9Router\
  db\data.sqlite        ← tất cả provider, API key, OAuth token
  db\data.sqlite-wal    ← thay đổi chưa gộp vào DB (chỉ có khi 9Router đang chạy)
  jwt-secret
  machine-id
  auth\cli-secret
  model-catalog.json    ← cache, không cần
  logs\, runtime\       ← không cần
```

## Cách 1 (khuyên dùng): giữ 9Router ở Windows, VM gọi sang

9Router chỉ là HTTP proxy, đặt ở đâu cũng được. Một nguồn key duy nhất, thêm key ở Windows là VM dùng được ngay.

1. Trong 9Router bật listen trên `0.0.0.0` thay vì `127.0.0.1` (settings hoặc flag khởi chạy tùy bản).
2. Mở firewall Windows cho cổng 9Router (PowerShell quyền admin, đổi `20128` thành cổng thật):

   ```powershell
   New-NetFirewallRule -DisplayName "9Router VM" -Direction Inbound -Protocol TCP -LocalPort 20128 -RemoteAddress 192.168.0.0/16 -Action Allow
   ```

3. Lấy IP LAN của Windows bằng `ipconfig`.
4. Cấu hình Hermes trong VM:

   ```yaml
   base_url: http://<IP_Windows>:20128/v1
   api_key: <API key của 9Router>
   ```

Nhược điểm: VM phụ thuộc máy thật đang bật, nhưng VM cũng chạy trên chính máy đó nên không thành vấn đề.

## Cách 2: copy thư mục dữ liệu sang Ubuntu

Chỉ khi muốn VM chạy 9Router độc lập.

1. **Tắt 9Router trên Windows trước** để `data.sqlite-wal` được gộp vào DB.
2. Cài 9Router trên Ubuntu, chạy một lần rồi tắt, để biết thư mục dữ liệu của nó (thường `~/.config/9Router` hoặc `~/.9router`).
3. Từ Windows đẩy sang VM:

   ```powershell
   scp -r "C:\Users\Admin\AppData\Roaming\9Router\db" "C:\Users\Admin\AppData\Roaming\9Router\jwt-secret" "C:\Users\Admin\AppData\Roaming\9Router\machine-id" "C:\Users\Admin\AppData\Roaming\9Router\auth" user@IP_VM:~/.config/9Router/
   ```

4. Khởi động lại 9Router trong VM.

**Bắt buộc copy cả `jwt-secret` và `machine-id` cùng với DB.** Key trong sqlite nhiều khả năng được mã hóa dựa trên hai file đó. Thiếu thì DB mở được nhưng key rỗng. OAuth token của Claude, Codex, Gemini cũng nằm trong DB nên đi theo luôn, không phải login lại.

## Liên quan

- Hermes trong VM kết nối Chrome qua CDP `127.0.0.1:9222`, không dùng GUI automation (AppActivate, SendKeys, bring_to_front).
- VM: Ubuntu Server 24.04 LTS, 2 vCPU, 4 GB RAM, 30 GB, Chrome thật chạy trong Xvfb.
