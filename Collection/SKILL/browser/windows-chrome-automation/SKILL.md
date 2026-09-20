---
name: "windows-chrome-automation"
description: "Use when automating Chrome profiles on Windows."
metadata:
  hermes:
    tags: [browser, chrome, windows, automation]
    category: browser
    phase: browser-task
    role: guide
    quality_tier: workflow-surface-gated
---

# Windows Chrome Automation

## Mapping Display Names to Directories
Chrome on Windows maps profile display names (e.g., "65aminh2001") to directory names (e.g., `Profile 10`).

To map these programmatically:
1. Locate user data: `%LOCALAPPDATA%\Google\Chrome\User Data`.
2. Iterate directories starting with `Profile ` or `Default`.
3. Parse `Preferences` file in each directory.
4. Read JSON key `$.profile.name`.

## Launching Specific Profiles
To launch a specific profile in a new window:
```bash
"C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile X" --new-window
```

## Automation Pitfalls
- **Port Conflict**: Launching Chrome with `--remote-debugging-port` fails if another instance already has an open browser session with the same user data directory.
- **Daemon Hijacking**: Chrome will often connect to an existing session if one is already running, ignoring a new port flag.
- **Workaround**: If automation requires a clean browser, ensure no other instances of Chrome are running, or launch with a distinct `--user-data-dir`.
