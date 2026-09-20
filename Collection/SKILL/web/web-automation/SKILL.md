---
name: web-automation
description: "Use when automating browsers via browser-harness."
---

# Web Automation Workflow

For any task requiring interactive browser control (clicking, typing, navigation), use `browser-harness`.

## Workflow

1. **Verify daemon:** `browser-harness --doctor`. If Chrome/Edge isn't running, it will launch or prompt you.
2. **First interaction:** When the browser launches, check for the "Allow remote debugging?" prompt in the browser GUI and click "Allow".
3. **Execution:** Use `browser-harness <<'PY'` with heredocs.
4. **Navigation:** 
   - First tab: `new_tab('url')`
   - Existing task: Reuse the current tab. Use `current_tab()` and `switch_tab()` to reuse, do not leave duplicate tabs.
5. **Stability:** Always call `wait_for_load()` before `page_info()` or `js()`. Timeouts often mean the page is not yet ready.

## Pitfalls

- **'Allow remote debugging':** If the `browser-harness` command times out or fails to connect, the browser is likely waiting for your confirmation in its GUI. Check the browser window.
- **`wait_for_load()`:** Essential. `page_info()` or `js()` will fail with `TypeError` on `null` (e.g., `documentElement` or `body`) if the page hasn't finished loading.
- **Paths:** When saving files from within browser scripts, use forward slashes and absolute Windows paths (`C:/Users/...`) to avoid path resolution errors.
- **Screenshots:** If `capture_screenshot()` timeouts occur, the daemon or page might be stuck. Ensure the page is active and visible if `scroll()` also fails.
- **Helpers:** Use `js()`, `page_info()`, `fill_input()`. Do not invent `screenshot()` or `browser_navigate()`.

## References
- Tool: `browser-harness` (CLI + Daemon).
- Diagnostics: `browser-harness --doctor`.
