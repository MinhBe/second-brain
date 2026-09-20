---
name: "open-chrome-profiles"
description: "Open multiple Chrome profiles with --profile-directory flag."
metadata:
  hermes:
    tags: [browser, chrome, profiles, automation]
    category: browser
    phase: setup
    role: tool
    quality_tier: verified
---

# Open Chrome Profiles

## Overview
Launch Chrome with specific user profiles using the `--profile-directory` switch to run several isolated sessions.

## Prerequisites
- Chrome installed at `C:\Program Files\Google\Chrome\Application\chrome.exe`.
- Profiles exist under `%LOCALAPPDATA%\Google\Chrome\User Data`.

## Profile Mapping (this machine)
| Directory | Display Name |
|-----------|--------------|
| Default   | Your Chrome |
| Profile 1 | 165 |
| Profile 3 | 65Be |
| Profile 5 | 65aminh |
| **Profile 10** | **65aminh2001** |
| Profile 11 | 465 |

## Commands
### Single profile (new window, shares debugging port 9222)
```bash
"C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" --new-window
```

### Isolated profile (dedicated debugging port)
```bash
"C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" --remote-debugging-port=9223 --no-first-run --no-default-browser-check
```

### Multiple profiles simultaneously
```bash
"C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" --new-window
"C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" --new-window
"C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" --new-window
```

## Verification
After launch, query CDP (default port 9222) to list tabs:
```bash
curl http://localhost:9222/json
```
Open `chrome://version/` in each window to confirm the active profile.

## Notes
- `--new-window` reuses the existing Chrome debugging session (port 9222).
- `--remote-debugging-port=N` creates a separate debugging endpoint.
- Use the directory name, not the display name, with `--profile-directory`.

## Related Skills
- `omh-browser` – policy overlay for browser tasks.
- `browser-operator` – native automation harness.
