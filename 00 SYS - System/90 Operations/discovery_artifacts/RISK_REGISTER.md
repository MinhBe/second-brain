# RISK REGISTER

| Risk ID | Description | Severity | Impact | Mitigation Strategy |
|---|---|---|---|---|
| **RSK-001** | Massive file migration (48,989 files, 20.45 GB) breaking Obsidian wikilinks or hard-coded paths. | **High** | Knowledge base corruption or broken references. | Complete full backup snapshot before migration; batch migration with link checking and rollback script. |
| **RSK-002** | Chrome profile conflict when Hermes accesses profiles currently open by owner. | **High** | Session lock, Chrome crash, or disruption of user work. | Use non-disruptive desktop automation or distinct user-data-dir copies; never force kill user Chrome. |
| **RSK-003** | Malicious or unverified community skills running arbitrary Windows commands. | **High** | System instability or security compromise. | Staging environment with sandbox inspection before activating skills. |
| **RSK-004** | Rate limits or session expiration on Claude Free rotation. | **Medium** | Temporary unavailability of auxiliary reasoning. | Record `last_used_at` and `retry_after`; fall back to local/other free models, never user Claude Plus. |
| **RSK-005** | Context overflow when sending large vault context to ChatGPT. | **Medium** | API errors, high latency, diluted responses. | Enforce Context Package standard: send goal, constraints, and relevant excerpts only. |
