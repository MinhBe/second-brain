# AGENT REGISTRY (AGENT_REGISTRY.md)
Generated: 2026-09-20T20:21:48
Total agents: 11

## Agent Roster

| Agent | Role | Capabilities | Requires Review For |
|-------|------|-------------|---------------------|
| alex | writer_editor | 3 capabilities | publishing |
| cody | coding_automation | 3 capabilities | system_config_change, production_deploy |
| drew | researcher | 3 capabilities | publishing |
| greg | qa_verifier | 3 capabilities | irreversible_actions |
| henry | learning_tutor | 3 capabilities | assessment_grading |
| laura | orchestrator | 5 capabilities | bulk_migration, destructive_delete, irreversible_action |
| lina | language_support | 3 capabilities | official_communication |
| marie | knowledge_manager | 4 capabilities | bulk_migration, destructive_delete |
| mia | calendar_reminders | 3 capabilities | owner_communication |
| tim | security_reviewer | 3 capabilities | irreversible_actions |
| tom | visual_designer | 2 capabilities | mass_media_generation |

## Routing Rules

- **laura** → orchestrator: any multi-step task, E2E tests, milestone management
- **drew** → researcher: web search, source analysis, OSINT collection
- **alex** → writer: markdown drafting, report generation
- **tom** → designer: diagrams, architecture visuals
- **cody** → automation: code writing, script execution, testing
- **greg** → QA: artifact verification (CANNOT self-approve own work)
- **tim** → security: secret scanning, permission review (CANNOT self-approve own work)
- **marie** → knowledge: vault operations, note processing, source registry
- **mia** → scheduler: calendar, reminders, cron management
- **henry** → tutor: learning content, curriculum design
- **lina** → language: translation, tone review, multilingual support

## Model Routing

| Agent | Primary Model | Fallback |
|-------|--------------|----------|
| laura | zai-org/GLM-5.3-Flash | gpt-4o-mini |
| greg | zai-org/GLM-5.3-Flash | claude-sonnet |
| tim | zai-org/GLM-5.3-Flash | claude-sonnet |
| Others | zai-org/GLM-5.3-Flash | — |

## Spawn Policy

All agents are **on-demand workers** (not permanent daemons).
Spawned via `delegate_task` when task assigned via Laura's orchestration.

## Artifact References

- Profiles: `Second Brain/00 SYS - System/40 Skills/agent_profiles/`
- Routing config: `milestone_3/AGENT_REGISTRY.md`
