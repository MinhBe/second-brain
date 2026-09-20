# SYSTEM INVENTORY (DISCOVERY STAGE)

## 1. Host & Operating System
- **Host OS**: Windows 11 Pro 64-bit (Build 26100 / AMD64)
- **Hostname Domain**: DESKTOP-5ETCV8R
- **Current User**: Admin (`C:\Users\Admin`)
- **GPU**: NVIDIA GPU with CUDA Toolkit v13.1 installed

## 2. Runtimes & Tooling
- **Python**: 3.11.16 (`C:\Users\Admin\AppData\Local\hermes\hermes-agent\venv\Scripts\python.EXE`)
- **Node.js**: v24.14.1 (`C:\Program Files\nodejs\node.EXE`)
- **Git**: 2.53.0.windows.2 (`C:\Program Files\Git\cmd\git.EXE`)
- **Docker**: 29.5.3 (`C:\Program Files\Docker\Docker\resources\bin\docker.EXE`)
- **Rust / Cargo**: 1.87.0 (`C:\Program Files\Rust stable MSVC 1.87\bin\rustc.EXE`)
- **FFmpeg**: 8.1 full build (`C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg...\ffmpeg.EXE`)
- **Ollama**: 0.34.2 (`C:\Users\Admin\AppData\Local\Programs\Ollama\ollama.EXE`)
- **GitHub CLI**: 2.89.0 (`C:\Program Files\GitHub CLI\gh.EXE`)
- **PostgreSQL**: Not installed / not found in PATH

## 3. Hermes Agent Runtime
- **Hermes Home**: `C:\Users\Admin\AppData\Local\hermes`
- **Config Version**: 45 (`config.yaml`)
- **Active Model (Current Session)**: `gemini/gemini-3.8-flash`
- **Default Configured Model**: `Reasoning` via custom local provider `http://localhost:20128/v1`
- **Subagent / Delegation**: `delegate_task` tool supporting up to 10 parallel subagents (`delegation.max_iterations: 250`)
- **Database Backend**: SQLite WAL mode
  - `state.db`: 28 sessions, 1,863 messages, full FTS5 search index
  - `kanban.db`: 0 tasks initialized
  - `projects.db`: 0 projects initialized
  - `cron/executions.db`: Scheduled jobs active
- **Gateway & Channels**: Telegram gateway active (`@Minhbe_test_bot_Bot`, user ID `5877423498`, group `-5321810546`)
- **Memory System**:
  - `MEMORY.md`: 1,170 / 2,200 chars utilized
  - `USER.md`: 1,126 / 1,375 chars utilized
