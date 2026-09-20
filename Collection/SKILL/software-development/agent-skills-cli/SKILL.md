---
name: agent-skills-cli
description: "Use npx skills to manage community agent-skills packages."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [skills-cli, agent-skills, npx, marketplace, installation]
    related_skills: [hermes-agent, hermes-agent-skill-authoring]
---

# Agent Skills CLI — Install and Verify Community Skill Packs

## What this skill covers

The `npx skills` CLI (aka "agent skills" / "skills.sh" ecosystem) installs reusable skill packs into `~/.agents/skills/` and symlinks them to compatible agent frameworks — including Hermes Agent. This skill covers the full workflow: search, inspect, install, verify Hermes picks them up, and apply.

## Step 1 — Search before installing

Always search the hub first to see what's available and check security ratings:

```bash
hermes skills search "<keyword>"
# or
npx -y skills@latest search "<keyword>"
```

Security ratings shown: Gen (AI safety audit), Socket (vuln scan), Snyk (package vuln). A "Critical Risk" on Snyk or Gen for a dependency-heavy package is expected — the skill itself may still be safe. Use judgment.

## Step 2 — Inspect before installing

```bash
npx -y skills@latest add <repo> --skill <name> --list
# shows all skills in the package, then exits without installing
```

Then install the specific skill you want:
```bash
npx -y skills@latest add <repo> --skill <name> -g -y
```

## Step 3 — Install

General form:
```bash
npx -y skills@latest add <owner>/<repo> --skill <skill-name> -g -y
```

Flags:
- `-g` / `--global`: install to the global agent skills directory (`~/.agents/skills/`)
- `-y` / `--yes`: auto-confirm without prompts
- `--skill <name>`: install a specific named skill from a multi-skill repo (use `--list` first to discover names)
- `--list`: preview all available skills in the repo, then exit

For single-skill repos, `--skill` may still be required:
```bash
npx -y skills@latest add <owner>/<repo>@<skill-name> --skill <skill-name> -g -y
```

## Step 4 — Verify Hermes loads the skill

After install, symlinks are created automatically. Check Hermes picks them up:
```bash
npx -y skills@latest list -g
# look for your skill under 'Global Skills'
hermes skills list
# Hermes count increases: verify it went from N → N+X enabled
```

**Expected Hermes behavior:** Skills in `~/.agents/skills/` are symlinked to Hermes Agent automatically. A skill is live when `hermes skills list` shows it and `npx skills list -g` confirms the `symlink → Hermes Agent` line.

**PromptScript warning is benign:** Every `npx skills add -g` install prints a line like:
```
Failed to install 1
  ✗ <skill> → PromptScript: PromptScript does not support global skill installation
```
This is NOT a failure. The skill is installed into `~/.agents/skills/` and symlinked successfully. The "PromptScript does not support global" line means the PromptScript backend doesn't handle global installs — but Hermes uses its own symlink mechanism, which works regardless. Ignore it.

## Step 5 — Use the skill

Reload Hermes or start a new session. Skills in `~/.agents/skills/` with a valid `SKILL.md` are automatically available — no manual reload needed. To trigger a skill in context, reference it by name when starting a related task.

## Step 6 — Keep skills up to date

```bash
# Check for updates
npx -y skills@latest check

# Update all global skills
npx -y skills@latest update -g -y
```

## Windows path pitfall for native CLI tools

Some skills produce standalone CLI binaries (e.g. `defuddle`, `browser-harness`). After `npm install -g <package>`, verify the binary is on PATH:
```bash
<command-name> --version
# or
npx <command-name> --version
```

For npm global packages that provide a binary, the MSYS/git-bash shell resolves the PATH correctly. For native tools that need a Python/Go install path (e.g. `go install` for `defuddle` from the Go package), prefer installing via the Go toolchain directly:
```bash
go install github.com/dotcommander/defuddle/cmd/defuddle@latest
```

For Node-based CLI tools, always verify with the bare command name — do not assume the PATH was updated without checking.

## Defuddle reference

The `npx skills` ecosystem points to `kepano/obsidian-skills/skills/defuddle` (npm package `defuddle` v0.19.3+). Correct usage:
```bash
npm install -g defuddle
# or
go install github.com/dotcommander/defuddle/cmd/defuddle@latest

# CLI syntax
defuddle parse <url>           # HTML output
defuddle parse <url> --markdown   # Markdown output
defuddle parse <url> --json    # JSON with metadata
defuddle parse <file.html>      # local file
defuddle parse <file.html> --markdown --output result.md
```

The older `npm install -g defuddle` path is Node-based. The newer `go install` path from `dotcommander/defuddle` is pure Go with WASM QuickJS — no Node.js needed.

## Markdown report format (user preference)

When producing multi-section reports for this user (Minh / Progrepcy):
- Output as `.md` files saved to `C:\Users\Admin\Documents\Second Brain\`
- Use clear headers (H1 for title, H2 for sections)
- Tables for structured data (skill name, path, security rating, symlink status)
- Bullet lists for multi-item inventory (not comma-separated prose)
- Avoid verbosity: state the command, state the result, done
- Split large reports into `PART1.md` / `PART2.md` when content exceeds readability; provide merge command at end
- The user can consume the file themselves — do not reprint the whole document in chat; give a summary + the path
