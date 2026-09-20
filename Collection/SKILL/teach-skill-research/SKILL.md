---
name: teach-skill-research
description: "Use parallel subagents to research AI learning mindsets."
version: 1.0.0
author: Admin (user preference)
license: MIT
category: research
---

# Teach Skill Research Workflow

## When to use

Use when you need to investigate teaching philosophies, extract YouTube transcripts, audit existing Hermes skills, and locate implementation details for a stateful `/teach` skill – all in a single, reproducible run.

## Procedure (always-on steps)

1. **Prepare output directory** – ensure the target folder exists (e.g. `C:\Users\Admin\Documents\Second Brain\Ω\TESTING`).
   ```bash
   mkdir -p "C:/Users/Admin/Documents/Second Brain/Ω/TESTING"
   ```
2. **Set parallelism** – verify `delegation.max_concurrent_children` is >= the number of sub‑tasks you plan (default 10 is fine). If not, run:
   ```bash
   hermes config set delegation.max_concurrent_children 10
   ```
3. **Define each sub‑task** as a JSON object with `context`, `goal`, and an absolute `Output path`. Typical tasks:
   - Retrieve a YouTube transcript and analyze it (`youtube-content` skill).
   - Search for related videos and summarize philosophies.
   - Audit installed Hermes skills for teaching‑related capabilities.
   - Locate the official `/teach` repository and document install steps.
   - (Optional) Research technical patterns for spaced‑repetition, workspace memory, or learning‑by‑teaching.
4. **Dispatch in parallel** using `delegate_task`:
   ```python
   delegate_task(tasks=[{...}, {...}, ...])
   ```
   The call runs up to `max_concurrent_children` agents simultaneously; excess tasks are queued automatically.
5. **Wait for completion** – the parent agent receives each sub‑agent's result as a new turn. No polling required.
6. **Consolidate (optional)** – if you need a single summary, run a final `delegate_task` that reads the generated markdown files and produces an aggregated document.
7. **Clean up** – remove temporary files if you created any inside the workspace.

## Pitfalls & Mitigations

- **Truncation of parallel tasks** – If you exceed `max_concurrent_children`, Hermes will log a truncation warning and drop excess tasks. *Fix*: increase the config value before dispatch.
- **Protected skill edit attempts** – Do not attempt to patch Bundled or Hub‑installed skills (e.g., `hermes-agent`). Instead, recommend `hermes curator adopt <skill>` if you need to modify them.
- **Missing output folder** – Sub‑agents fail silently if the target directory does not exist. *Mitigation*: always create the folder in step 1.
- **File-system timestamps for spacing** – When implementing spaced-repetition without a DB, rely on file modification times (`stat`), not on external services. See `references/parallel-research.md` for a concrete pattern.
- **Assuming instant results** – Background children may finish out-of-order; never chain a sub-task on another's result within the same `delegate_task` call.

## References

- `references/parallel-research.md` – detailed patterns for spaced-repetition, ZPD tracking, and workspace-based state.

---

*This skill encodes the user's preference for concise markdown output, explicit step ordering, and proactive parallelism.*