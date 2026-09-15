# bwp.mjs — one tab in a chosen profile of the user's running Chrome

`$P` below means `node C:/Users/Admin/.claude/skills/browser/scripts/bwp.mjs`.
Every command prints one JSON line (`ok, verb, code, exit, ..., next`). `-s <session>` names the tab.

## Why it exists

Chrome runs every open profile inside one process; each profile is a CDP browser context. `bw.mjs attach`
(playwright-cli) can only use the default context, so it cannot choose a profile. `bwp.mjs` asks Chrome itself
to open a tab in the wanted profile (`chrome.exe --profile-directory=<dir> <marker-url>`, which also opens the
profile's window if needed), recognises that tab by a one-time nonce in its URL, and then drives only that tab
through Playwright `connectOverCDP`. The user's own tabs and windows are never selected, navigated, closed or read.

## Risk (read before use)

This drives a Chrome profile that is already signed in. While remote debugging is on, anything that can
reach the DevTools port has full read of that account's cookies and session. That is inherent to driving a
real logged-in profile, not a bug; "I know what I'm doing" does not change what the command does. Use it only
for the account the user asked for, and prefer `bwp close` + untick remote debugging when done. Accepted by the
user on 2026-09-15 as the chosen trade-off (see SECURITY.md).

## Two separate "allow" prompts

- **Claude Code asking permission to run the `bwp` Bash command** — removed by an allowlist entry in
  `~/.claude/settings.local.json`: `"Bash(node C:/Users/Admin/.claude/skills/browser/scripts/bwp.mjs:*)"`
  (same shape as the `bw.mjs` entry already there). The user adds this themselves; an agent cannot grant
  itself permissions.
- **Chrome's own "Allow remote debugging for this browser instance" dialog** — settings.local.json cannot
  suppress it. The daemon keeps one connection so it appears at most once per Chrome session. Removing it
  entirely means persisting `devtools.remote_debugging.user-enabled=true` in Local State while Chrome is
  closed (a user-run command, below); a Chrome update may reset it.

### Persist the toggle (user runs this, Chrome fully closed)

```
node -e "const fs=require('fs');const p=process.env.LOCALAPPDATA+'/Google/Chrome/User Data/Local State';const j=JSON.parse(fs.readFileSync(p));(j.devtools=j.devtools||{}).remote_debugging={'user-enabled':true};fs.writeFileSync(p,JSON.stringify(j));console.log('persisted')"
```

Google deliberately dropped a supported "always allow" on the default profile (Chrome 136+; the persist-approval
request was closed "not planned"). The only truly zero-prompt path is a Chrome launched with
`--remote-debugging-port` on a dedicated `--user-data-dir` (sign in once there) — a hardening TODO.

## One human step per Chrome session

Chrome ≥ 136 ignores `--remote-debugging-port` on the real profile dir. The user must tick
"Allow remote debugging for this browser instance" at `chrome://inspect/#remote-debugging` once per Chrome
process (it resets when Chrome restarts). Chrome ≥ 144 additionally asks the user to allow **every new DevTools
client**, so `bwp.mjs` runs a small daemon (`scripts/lib/bwp-daemon.mjs`) that keeps one connection open:
the first command after Chrome starts triggers one "Allow" prompt; later commands reuse the connection
(the daemon exits after 60 min idle; `$P daemon --stop` ends it early).

## Verbs

| Verb | Command | Notes | JSON fields |
|---|---|---|---|
| profiles | `$P profiles` | Chrome profiles with directory, display name and signed-in e-mail | `profiles:[{directory,name,account}], count` |
| open | `$P open <url> -s <n> --account <email>` or `--profile "<Default|Profile N|display name>"` | opens ONE tab in that profile (window opened if needed); provider hosts allowed (user's own browser); 12 if the session exists | `session, profile_dir, url, title, snapshot_path, refs, opened_window, attached` |
| goto | `$P goto <url> -s <n>` | navigates the session's tab | `url, title, snapshot_path, refs` |
| snapshot | `$P snapshot -s <n> [--depth N]` | aria snapshot with refs to `state/snapshots/` | `snapshot_path, refs, bytes, url, title` |
| find | `$P find -s <n> --pattern "<text or regex>" [--max 20]` | lines of a fresh snapshot that carry a ref | `total, matches:[{ref,line}], context_path` |
| click | `$P click <eN or css> -s <n>` | refs are re-bound with a fresh snapshot before the click | `target, url, title, snapshot_path, refs` |
| fill | `$P fill <eN or css> "<text>" -s <n> [--submit]` / `--stdin` | value never printed | `target, filled_chars, submitted` |
| press | `$P press <Key> -s <n>` | same key list as bw.mjs | `key, url, title, snapshot_path` |
| wait | `$P wait -s <n> --text "<t>" \| --css "<sel>" \| --ms N [--timeout ms]` | max 30 s; exit 6 | `kind, waited_ms, matched` |
| extract | `$P extract -s <n> --mode text\|md\|links\|table [--css "<sel>"] [--out <file>]` | same extractors as bw.mjs | `mode, target, bytes, text` or `items, count` or `extract_path, preview` |
| screenshot | `$P screenshot -s <n> [--full]` | PNG to `state/screenshots/` | `screenshot_path, full` |
| tabs | `$P tabs -s <n>` | the session's tab plus a count of the user's other tabs (never their titles or URLs) | `own_tab:{title,url}\|null, other_tabs` |
| list | `$P list` | sessions and daemon state | `sessions:[{name,profile_dir,created_at}], count, daemon` |
| close | `$P close -s <n>` | closes only the session's tab | `closed, profile_dir` |
| daemon | `$P daemon [--stop]` | shows or stops the connection daemon | `pid, connected` |

Exit 7 from any verb means the session's tab is gone (the user closed it): run `open` again; never use another tab.

## Typical sequence

```
$P open https://claude.ai/new -s p365 --account 365aminh2001@gmail.com
$P find -s p365 --pattern "Write your prompt"
$P fill e380 "<prompt>" -s p365 --submit
$P wait -s p365 --text "<expected>" --timeout 30000
$P extract -s p365 --mode md
$P close -s p365
```

Several accounts at once: repeat `open` with different `-s` and `--account`; each gets its own tab in its own profile window.

## State

`state/bwp/<session>.json` = `{ session, profile_dir, browser_context_id, target_id, opened_window, created_at }`;
`state/bwp/daemon.json` = `{ port, token, pid, started_at }` (loopback only, random token). No cookies or page data.

## Status (2026-09-15)

Working prototype, tested live with profiles `Default` (365) and `Profile 6` (665). Not yet covered by evals; R4 (provider
hosts) is deliberately not enforced here (user decision, see CHANGELOG 0.2.0). Hardening TODO: eval with a throwaway
Chrome, audit trail for provider tabs, decide whether `bw.mjs attach` should be retired in favour of this driver.
