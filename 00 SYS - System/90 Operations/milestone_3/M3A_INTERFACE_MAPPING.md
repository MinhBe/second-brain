# M3A Interface Mapping
## Overview
This file defines the interface contracts for Milestone 3A Integration.

## Modules
1. **ProfileLockManager**: Manages browser profile access locks with TTL and heartbeat.
2. **ConversationArchiver**: Handles transcript persistence to staging.
3. **TaskOrchestrator**: Central management for multi-agent workflows via SQLite.

## Interface Contracts
- **ProfileLockManager.renew_lease**: Accepts `task_id` and `extend_seconds`. Modifies lock timestamp and TTL in place.
- **ConversationArchiver**: Interface for batching transcripts into `task_orchestrator.db`.
