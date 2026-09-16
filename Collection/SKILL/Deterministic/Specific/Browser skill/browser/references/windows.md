# Windows notes

## Invoking the scripts

Always use the canonical ASCII path: `node C:/Users/Admin/.claude/skills/browser/scripts/<script>.mjs ...`.
Forward slashes work in PowerShell 5.1, cmd.exe and Git Bash. The junction resolves to the authoring folder under Second Brain (whose path contains `Ω` and spaces); outputs will show that longer path. That is normal.

## PowerShell vs Git Bash

| Situation | PowerShell 5.1 | Git Bash |
|---|---|---|
| Quote a value with spaces | `"Ask confirm"` | `"Ask confirm"` |
| Regex pattern with `|` | `--pattern "set state|submit"` | same |
| Pattern starting with `/` | avoid; the wrapper adds `/.../i` itself | **Git Bash rewrites a leading `/` into `C:/Program Files/Git/...`** (MSYS path conversion). The wrapper spawns Node directly so its own arguments are safe, but never pass raw `/regex/` strings from a Git Bash prompt. `MSYS_NO_PATHCONV=1` disables the rewrite for one command |
| Feed a value on stdin | `"value" \| node ... fill e5 --stdin -s x` | `printf '%s' "value" \| node ... fill e5 --stdin -s x` |
| Chain commands | do not; one command per step | do not |

Never use `&&` between skill commands. Run one, read its JSON, then run the next.

## What the wrapper does for you

- Spawns `node_modules/@playwright/cli/playwright-cli.js` from the skill folder with cwd `state/pwcli/`, so `.playwright-cli/` and session data never land in the user's project.
- Uses the installed Google Chrome (`channel: chrome`) by default. Set `BROWSER_SKILL_CHANNEL=chromium` after `npx playwright install chromium` to use the bundled Chromium instead.
- Restricts ACLs on `state/storage/*.json` with `icacls` after `state-save`.

## Chrome 136 and later

Chrome ignores `--remote-debugging-port` / `--remote-debugging-pipe` on the default user data directory. Automation cannot *launch* on the user's real `%LOCALAPPDATA%\Google\Chrome\User Data` profiles, so launched sessions use separate automation profiles (`profiles/<id>/user-data`, see `profiles.md`). Attaching to an *already running* Chrome is possible once the human enables it (next section).

## Attaching to the user's running Chrome (`bw.mjs attach`)

General browsing only, never observer runs. One human step per Chrome session: open `chrome://inspect/#remote-debugging`, tick "Allow remote debugging for this browser instance". Chrome then writes `User Data\DevToolsActivePort`; `doctor.mjs` reports `chrome_remote_debugging: ok`. The box stays ticked until Chrome restarts and lets **any local process** drive that Chrome, so ask the user to untick it when the task is done.

Then:
```
node C:/Users/Admin/.claude/skills/browser/scripts/bw.mjs attach <url> -s live
```
opens one new tab in their Chrome and marks it as the skill's. Every page verb checks that mark first: the user's own tabs are never selected, navigated, closed or read (exit 7). `tabs` lists their tabs only as `owned:false` with no title or URL. `state-save`/`state-load` are refused. `close -s live` closes the skill's tabs and detaches; Chrome keeps running. The agent never calls `playwright-cli attach` directly.

`BROWSER_SKILL_CDP_ENDPOINT=http://127.0.0.1:<port>` (evals only) points `attach` at a throwaway Chrome started with `--remote-debugging-port` instead of the real one.

## Junctions (no admin needed)

```powershell
New-Item -ItemType Junction -Path "$env:USERPROFILE\.claude\skills\browser" -Target "C:\Users\Admin\Documents\Second Brain\Ω\SKILL\Deterministic\Specific\Browser skill\browser"
New-Item -ItemType Junction -Path "$env:USERPROFILE\.codex\skills\browser"  -Target "<same target>"
New-Item -ItemType Junction -Path "$env:USERPROFILE\.gemini\skills\browser" -Target "<same target>"
New-Item -ItemType Junction -Path "$env:USERPROFILE\.pi\agent\skills\browser" -Target "<same target>"
```

opencode also reads `~/.claude/skills`, so it needs no extra junction.

## ACLs

`doctor.mjs --fix` runs `icacls <dir> /inheritance:r /grant:r <you>:(OI)(CI)F *S-1-5-18:(OI)(CI)F *S-1-5-32-544:(OI)(CI)F` on `profiles/` and `state/`. Secret files passed to `fill --secret` must already be owner-only or the command exits 3.

## First launch

Windows SmartScreen or an antivirus may prompt the first time Chrome is launched under automation or when `node_modules` is unpacked. If Chrome fails to start, the JSON has `code: TOOL`; run `doctor.mjs` and read `report_path`.

## Known harmless noise

`playwright-cli --version` can print `Assertion failed: !(handle->flags & UV_HANDLE_CLOSING)` on exit. It does not affect any verb.
