# browser — skill điều khiển Chrome cho mọi AI agent (Windows 11)

Một skill duy nhất, strict, chạy bằng script. Agent (Claude Code, Codex, Gemini CLI, opencode, pi) chỉ cần
copy đúng lệnh trong `SKILL.md`, đọc **một dòng JSON** trả về và làm theo trường `next`. Không cần MCP, không cần extension.

Hai phần trong cùng một skill:

| Phần | Script | Làm gì |
|---|---|---|
| Duyệt web tổng quát | `scripts/bw.mjs` | mở trang, tìm phần tử theo text, click, điền form, đọc nội dung (text/markdown/links/table), lưu và tái dùng trạng thái đăng nhập |
| AI Web Observer (Phase 1) | `scripts/profile.mjs`, `scripts/aiweb.mjs` | gửi **một** prompt tới Claude từ **một** Chrome profile đã đăng ký, quan sát trạng thái UI, lưu response + screenshot + timeline có hash-chain + firewall log |

Hợp nhất từ ba tài liệu gốc: skill Playwright tổng quát, `SPEC-1-AI-WEB-MULTI-PROFILE-OBSERVER.md`, `ai-web-observer-SKILL.md` (hardened). Bốn repo tải về chỉ là tham khảo (xem `SECURITY.md` và `references/`).

## Cài đặt (đã làm xong trên máy này)

```powershell
cd "C:\Users\Admin\Documents\Second Brain\Ω\SKILL\Deterministic\Specific\Browser skill\browser"
npm install                       # @playwright/cli 0.1.19 + playwright 1.63.0, pin exact
node scripts/doctor.mjs --fix     # kiểm tra môi trường, khoá ACL profiles/ và state/
```

Junction (không cần admin) đã trỏ về thư mục này:
`~\.claude\skills\browser`, `~\.codex\skills\browser`, `~\.gemini\skills\browser`, `~\.pi\agent\skills\browser`
(opencode đọc `~\.claude\skills` nên không cần thêm). Mọi lệnh dùng đường dẫn ASCII `C:/Users/Admin/.claude/skills/browser/...`.

Dùng Chrome 152 đã cài (`channel: chrome`). Muốn dùng Chromium riêng: `npx playwright install chromium` rồi đặt `BROWSER_SKILL_CHANNEL=chromium`.

## Dùng hằng ngày

```
node C:/Users/Admin/.claude/skills/browser/scripts/doctor.mjs
node C:/Users/Admin/.claude/skills/browser/scripts/bw.mjs open https://example.com/ -s demo --headless
node C:/Users/Admin/.claude/skills/browser/scripts/bw.mjs extract -s demo --mode md
node C:/Users/Admin/.claude/skills/browser/scripts/bw.mjs close -s demo
```

## Observer: đăng ký profile và đăng nhập (người làm, script chỉ chờ)

```
node C:/Users/Admin/.claude/skills/browser/scripts/discover-profiles.mjs
node C:/Users/Admin/.claude/skills/browser/scripts/profile.mjs register --id p001 --name "165" --from-chrome "Profile 1"
node C:/Users/Admin/.claude/skills/browser/scripts/profile.mjs login --id p001 --provider claude
node C:/Users/Admin/.claude/skills/browser/scripts/aiweb.mjs ask claude --profile p001 --prompt "Reply with exactly the word PONG."
node C:/Users/Admin/.claude/skills/browser/scripts/aiweb.mjs export-run <run_id> --format md
```

- `register` tạo thư mục automation riêng `profiles/p001/user-data`. Chrome ≥ 136 không cho điều khiển thư mục `User Data` thật, và skill cũng từ chối làm việc đó.
- `login` mở Chrome **có giao diện**, bật firewall, rồi **chờ bạn tự đăng nhập**. Script không gõ gì cả.
- `ask` chạy đúng một lần: READY → gõ prompt → gửi → chờ → lưu `response.md`. Gặp LOGIN_REQUIRED / USAGE_EXHAUSTED / RATE_LIMITED / CAPTCHA → dừng (exit 8), ảnh + evidence trong `runs/<ngày>/<run_id>/`.

Tài khoản dùng cho Observer **không** nên là tài khoản đang chạy Claude Code (xem `SECURITY.md` §10, đã nêu một lần).

## Kiểm tra

```
node evals/run.mjs                          # không cần browser, không LLM: 14 case
node evals/run.mjs --browser --token-check  # thêm smoke thật với Chrome + spike OOPIF; mọi dòng stdout ≤ 2 KB
```

## Cấu trúc

```
SKILL.md            hợp đồng cho agent (≤ 230 dòng)        SECURITY.md   Layer 0–6, cái gì code-enforced
scripts/            doctor, discover-profiles, profile, bw, aiweb + lib/
references/         commands, observer, profiles, providers/, exit-codes, gotchas, windows
schemas/            output, run, event, notification, artifact, profile, observation
evals/              run.mjs + cases/ + fixtures/ (raw playwright-cli output, observation thật đã sanitize)
profiles/ state/ runs/   dữ liệu runtime (gitignored; ACL owner-only)
```

## Layer 5 (tùy chọn): push `runs/` lên repo riêng tư

```
git init runs
git -C runs remote add origin <repo riêng tư của bạn>
```
Sau đó mỗi `ask` tự commit + push; không có remote thì ghi `AUDIT_PUSH_SKIPPED`. Hash-chain của timeline luôn bật.

## Việc còn lại cần người (Phase C)

1. Đăng nhập một profile thật (`profile login`) rồi chạy `aiweb ask ... --dry-run` để chụp accessibility snapshot thật của claude.ai.
2. Từ `observation.json` của run đó, xác nhận tên composer / nút Send / nút Stop / container assistant trong `scripts/lib/providers/claude.mjs` (các mục `TO_CAPTURE`) và thay fixture `evals/fixtures/observations/claude-ready.json` bằng bản đã sanitize.
3. Chạy `ask` thật với prompt "Reply with exactly the word PONG." và kiểm tra `export-run` trả lời đủ 14 câu (xem `references/observer.md`).
