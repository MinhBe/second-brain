# BASELINE VERIFICATION & EVIDENCE AUDIT (MILESTONE 1)

## 1. Skill Loading & Priority Precedence
Inspected `C:\Users\Admin\AppData\Local\hermes\hermes-agent\agent\skill_utils.py` function `get_scan_ordered_skills_dirs()`.
The verified resolution order is:
1. **Project Skills** (Highest priority): `.hermes/skills` or `.agents/skills` under trusted repo root (`get_project_skills_dirs()`).
2. **Profile-Local Skills**: `C:\Users\Admin\AppData\Local\hermes\skills` (`get_skills_dir()`).
3. **Creation Directory**: `skills.create_dir` if defined in `config.yaml`.
4. **External Directories**: `skills.external_dirs` if defined in `config.yaml`.

**Key Finding**: In `config.yaml`, `skills.external_dirs` is currently unset. Therefore, Hermes currently loads skills ONLY from `AppData\Local\hermes\skills` (1,192 skills). The 2,374 skills located in `Second Brain\Collection\SKILL` are dormant and not indexed by Hermes until configured.

## 2. Delegation & Concurrency Limits
- Verified configuration: `delegation.max_iterations: 250`.
- Runtime limit: `delegation.max_concurrent_children` defaults to 10 parallel subagents.
- Execution isolation: Each subagent receives an isolated conversation session, terminal environment, and toolset.

## 3. Active Cron Jobs & Schedulers
- Verified via `C:\Users\Admin\AppData\Local\hermes\cron\jobs.json`:
  - 2 one-time notification jobs recorded (`4cea94eb9b0a`, `2b925fefed13`), both marked `state: completed`.
  - Cron scheduler engine is active with lockfile tracking (`.jobs.lock`, `.tick.lock`).

## 4. Storage & Filesystem Capacity
- Drive `C:\`: 475.86 GB total, 79.23 GB free (83.3% used).
- Drive `G:\`: 15.0 GB total, 14.94 GB free.
- Drive `H:\`: 15.0 GB total, 14.92 GB free.
- Vault size: 20.45 GB (48,989 files). Sufficient headroom on C: (79.23 GB free) to accommodate a compressed backup snapshot (estimated 8-12 GB) during migration.
