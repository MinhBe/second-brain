# GAP ANALYSIS (AS-IS vs. TO-BE)

| Dimension | Current State (As-Is) | Target State (To-Be) | Gap & Remediation |
|---|---|---|---|
| **Multi-Agent Team** | Single soul Hermes Agent; subagent spawning via `delegate_task` only. | 11 specialized agent personas coordinated by Laura. | Need to create agent definition manifests, system prompts, and dispatch routing. |
| **Second Brain Vault** | Legacy layout: `Collection` (`SKILL`, `FILES`, `INBOX`), `.git`, `.obsidian` (48,989 files). | 4-pillar Hybrid Vault (`00 SYS`, `10 KNW`, `20 THO`, `30 PRJ`). | Migration plan with snapshot backup, link validation, and path rewriting. |
| **Browser Gateway** | Direct OS control / CDP port 9222 daemon. | Dedicated profile gateway managing Profile 1 (ChatGPT) & Profile 8 (Claude). | Scripted session controller that respects active user sessions. |
| **Claude Rotation** | Manual usage on Profile 8. | Round-robin pool with `last_used_at`, `rate_limit` logging, never falling back to Plus. | Claude rotation state tracker module. |
| **Skill Management** | 2,374 skills in SB, 1,192 in Hermes; many duplicates, no automated test suite. | Validated, deduped, staged skill catalog with manifest inspection. | Automated skill auditor script to categorize verified vs. experimental. |
| **Conversation Memory**| SQLite `state.db` (1,863 messages) with FTS5 search. | 3-tier memory (Log -> Working Memory -> Knowledge Notes in Obsidian). | Automated sync pipeline from session DB into Second Brain Markdown notes. |
