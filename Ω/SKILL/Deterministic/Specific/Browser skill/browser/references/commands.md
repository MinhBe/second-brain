# bw.mjs command reference (general browsing)

`$S` below means `node C:/Users/Admin/.claude/skills/browser/scripts/bw.mjs`.
Every command prints one JSON line (`ok, verb, code, exit, ..., next`) and nothing else on stdout.
`-s <session>` is required on every page verb. Session names: lowercase letters, digits, dashes (max 24).
Provider hosts (`claude.ai`, `chatgpt.com`, `meta.ai` and subdomains) are refused with exit 7. Use `aiweb.mjs` for them.

| Verb | Command | Guarantees | Extra JSON fields |
|---|---|---|---|
| open | `$S open <url> -s <n> [--headless] [--persistent] [--state <name>]` | http(s) only; refuses reserved hosts (7); refuses if session already open (12, use goto); headed window by default; `--persistent` keeps cookies in `profiles/general/<n>/user-data`; `--state` loads `state/storage/<name>.json` then reloads | `url, title, snapshot_path, refs, pid, headless, persistent, state_loaded` |
| attach | `$S attach <url> -s <n>` | joins the user's **already running** Chrome and opens ONE new tab there (their logins apply); needs the human to have ticked "Allow remote debugging for this browser instance" at `chrome://inspect/#remote-debugging` (else 3); provider hosts (claude.ai …) are allowed here and in later `goto`/`tabs --new` of the same session, because it is the user's own signed-in browser (temporary R4 relaxation); refuses if the session is open (12). From then on the session may only act in tabs it opened: any verb on a user tab exits 7; `state-save`/`state-load` exit 7; `close` detaches | `url, title, snapshot_path, refs, attached, endpoint, port, baseline_tabs, tab_index, tabs` |
| goto | `$S goto <url> -s <n>` | same host rules; auto-snapshot to file; attached session: current tab must be one the skill opened (else 7) | `url, title, snapshot_path, refs` |
| snapshot | `$S snapshot -s <n> [--depth N] [--ref eN]` | writes the accessibility tree to `state/snapshots/`; never inline | `snapshot_path, refs, bytes, url, title` |
| find | `$S find -s <n> --pattern "<text or regex>" [--max 20]` | fresh search of the live page, case-insensitive; returns only lines that carry a ref | `total, matches:[{ref,line}], context_path` |
| click | `$S click <eN> -s <n>` or `$S click --role <role> --name "<text>" -s <n>` or `$S click --css "<selector>" -s <n>` | exactly one target form; auto-snapshot after; reports an open dialog in `modal` | `target, target_kind, url, title, snapshot_path, refs, modal?` |
| fill | `$S fill <eN or css> "<text>" -s <n> [--submit]` / `$S fill <target> --stdin -s <n>` / `$S fill <target> --secret <file>:<KEY> -s <n>` | value never appears in output or logs; `--secret` file must be readable by the owner only (else 3); `--submit` presses Enter after filling | `target, filled_chars, submitted, source` |
| press | `$S press <Key> -s <n>` | Key from the allowed list: Enter, Tab, Escape, Backspace, Delete, Space, Home, End, PageUp, PageDown, ArrowUp/Down/Left/Right, F1..F12, a single letter or digit, Shift+Tab, Control+a (and other modifier+key) | `key, url, title, snapshot_path` |
| select | `$S select <eN or css> "<value>" -s <n>` | picks an option by value or label | `target, selected` |
| check / uncheck | `$S check <eN or css> -s <n>` | checkbox or radio | `target, checked` |
| wait | `$S wait -s <n> --text "<t>"` / `--css "<sel>"` / `--url "<glob>"` / `--idle` / `--ms N` `[--timeout ms]` | max 30000 ms; exit 6 when it does not happen; never loops | `kind, waited_ms, matched` |
| screenshot | `$S screenshot -s <n> [--full] [--target eN]` | PNG to `state/screenshots/`; prefer find/extract over reading images | `screenshot_path, full` |
| extract | `$S extract -s <n> --mode text\|md\|links\|table [--ref eN \| --css "<sel>"] [--out <file>]` | fixed extractors, no custom JS; inline when <= 1500 bytes else written to `state/extracts/` (or `--out`) | `mode, target, bytes, text` or `items, count` or `extract_path, preview` |
| dialog | `$S dialog -s <n> --accept [--text "<prompt answer>"]` / `$S dialog -s <n> --dismiss` | handles alert/confirm/prompt | `action, url, title` |
| state-save | `$S state-save <name> -s <n>` | cookies + localStorage to `state/storage/<name>.json`, ACL restricted; contents never printed; refused on attached sessions (7) | `state, state_path, cookies, origins, acl_restricted` |
| state-load | `$S state-load <name> -s <n>` | loads then reloads the page; refused on attached sessions (7) | `state, loaded, url, title, snapshot_path` |
| tabs | `$S tabs -s <n> [--select i \| --new <url> \| --close i]` | at most one operation, then lists tabs. Attached session: `--select`/`--close` on a tab the skill did not open exits 7; user tabs are listed with `owned:false` and `title`/`url` null | `tabs:[{i,current,title,url,owned?}], op, attached?` |
| ports | `$S ports` | probes common local dev-server ports on 127.0.0.1 | `open_ports, probed` |
| list | `$S list` | sessions known to playwright-cli | `sessions:[{name,status,browser,headed,persistent,attached}], count` |
| close | `$S close -s <n>` | closes the session's browser. Attached session: closes only the tabs the skill opened (never the last tab), then detaches; the user's Chrome stays open | `closed, message` / attached: `closed:false, detached, closed_tabs, message` |
| kill-all | `$S kill-all` | maintenance only: kills every playwright-cli browser | `message` |

## Typical sequences

Read a page:
```
$S open https://example.com/ -s read --headless
$S extract -s read --mode md
$S close -s read
```

Click something by text:
```
$S find -s dash --pattern "sign in"
$S click e12 -s dash
```

Fill a form (value from a secret file; never paste passwords into the command):
```
$S find -s dash --pattern "textbox"
$S fill e5 "user@example.com" -s dash
$S fill e6 --secret C:/Users/Admin/secrets.env:SITE_PASSWORD -s dash --submit
$S wait -s dash --url "**/dashboard**"
$S state-save dash-login -s dash
```

Reuse a saved login later:
```
$S open https://example.com/dashboard -s dash --state dash-login
```

Log in by hand (when the site blocks automated sign-in): open headed, ask the user to sign in, then `wait --text` for something that only appears after login, then `state-save`.

Use a site the user is already logged in to, in their own running Chrome:
```
$S attach https://example.com/account -s live      (exit 3 → ask the user to tick chrome://inspect/#remote-debugging, then run once more)
$S find -s live --pattern "..."                     (all verbs work, but only in the tab attach opened)
$S tabs -s live --new https://example.com/other     (more tabs of your own)
$S close -s live                                    (closes your tabs, detaches; their Chrome and tabs stay)
```
Exit 7 from any verb on an attached session means the current tab is the user's (they closed yours): run `tabs --new`, never ask them to lift the guard. Remind the user to untick the remote-debugging box when done.

## Not available on purpose

`eval`, `run-code`, `cookie-*`, `localstorage-*`, `route`, `attach --extension`. `attach --cdp` exists only as `$S attach`, which is confined to tabs it opened. The agent never writes JavaScript. If a task cannot be done with the verbs above, say so and ask the user; do not call `playwright-cli` directly.
