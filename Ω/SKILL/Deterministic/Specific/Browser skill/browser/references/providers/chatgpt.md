# Provider: ChatGPT (chatgpt.com) — Phase 6 stub

- Entry URL: `https://chatgpt.com/`
- Allowlisted host: `chatgpt.com` (exact)
- Status: `implemented: false`. `aiweb ask chatgpt` exits 2 until the adapter data (state rules, composer/send/stop ladders, assistant container) is captured from a live sanitized snapshot, the same way as `claude.md` describes.
- Known difference to plan for: Cloudflare Turnstile appears more often under automation → expect more `CAPTCHA` stops (exit 8); they are never solved.
