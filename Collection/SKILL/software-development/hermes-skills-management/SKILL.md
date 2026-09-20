---
name: hermes-skills-management
description: Use when managing Hermes skills.
---
# Hermes Skills Management & Verification

## Goal
Standardised workflow to verify, install, and maintain Hermes Agent skills safely.

## Steps

1. **Check current skill status**
```bash
hermes skills list | grep enabled | wc -l   # total enabled
npx skills list -g                        # hub‑installed
hermes skills list                         # all loaded
hermes skills inspect <skill>             # detail view
```
2. **Search for new skills**
```bash
npx skills search <keyword>
skill_view('<skill>')   # view SKILL.md, references, scripts
```
3. **Install safely**
```bash
# Hub install
npx skills add <owner>/<repo>[@tag] -g -y
# Direct install
hermes skills install <path> -y
```
4. **Security scan outcomes**
| Result | Action |
|---|---|
| SAFE | Install automatically |
| DANGEROUS / BLOCKED | Review manually before install |
5. **Interpret "PromptScript does not support global skill installation"**
- Not an error; skill is still installed under `~/.agents/skills/` and symlinked.
6. **Fix missing pip**
```bash
python -m ensurepip --upgrade
```

## Red flags
- **Oh My Hermes BLOCKED** – critical findings, must be reviewed.
- **Snyk Critical Risk** – evaluate before production use.
- Multiple symlinks are normal; they show which agents can use the skill.
