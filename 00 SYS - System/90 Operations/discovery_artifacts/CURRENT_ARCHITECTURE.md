# CURRENT ARCHITECTURE (AS-IS)

```
[ Owner (Telegram / Desktop) ]
               │
               ▼
   [ Hermes Agent (Single Soul) ] ── (Python 3.11 / venv)
               │
   ┌───────────┼───────────────────────────┐
   ▼           ▼                           ▼
[ SQLite DB ] [ Built-in Tools ]   [ Custom Provider (low) ]
- state.db    - execute_code       - localhost:20128/v1
- kanban.db   - delegate_task      - gemini-3.8-flash (Active)
- cron.db     - computer_use       - Ollama / local models
              - web_search
              - browser_exec (daemon)
```

## Characteristics
- **Orchestration**: Single centralized agent loop with ad-hoc subagent spawning (`delegate_task`).
- **Team Structure**: Roles (Laura, Drew, Cody, Greg, Tim, Marie...) do not exist as persistent configurations yet.
- **Second Brain**: Unstructured file collection (48,989 files, 20.45 GB) with raw skills, inbox, and files mixed together.
- **Browser Interaction**: Either browser daemon on port 9222 or OS-level UI automation.
