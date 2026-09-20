---
name: open-terminal
description: "Run shell commands, manage files, and execute code remotely via OpenTerminal REST API. No SSH needed. Self-hosted lightweight server accessible over HTTP. Use when you need to: run a terminal command on a remote machine, execute scripts, manage files programmatically, run code in a sandboxed environment, install packages, check system state, or give AI agents a computer to work with. Triggers on: 'run command', 'execute script', 'run in terminal', 'shell command', 'open terminal', 'run bash', 'execute code', 'remote execution', 'sandbox', 'run python script', 'install package', 'computer use'."
---

# OpenTerminal

Run shell commands and manage files on a remote machine via a simple REST API. No SSH. Works with Docker (sandboxed) or bare metal (`pip install`).

**What it is:** A lightweight server that exposes your machine's terminal over HTTP. Ideal for AI agents that need a sandboxed computer to run code, manage files, or execute terminal workflows.

---

## Setup

### Docker (sandboxed — recommended for agents)

```bash
docker run -p 8000:8000 -e OPEN_TERMINAL_API_KEY=your-secret-key ghcr.io/open-webui/open-terminal
```

### pip (bare metal — runs on your actual machine)

```bash
pip install open-terminal
open-terminal run --host 0.0.0.0 --port 8000 --api-key your-secret-key
```

Configure environment:
```bash
export OPEN_TERMINAL_URL=http://localhost:8000
export OPEN_TERMINAL_API_KEY=your-secret-key
```

---

## Commands

### Execute a shell command

```bash
curl -X POST "$OPEN_TERMINAL_URL/execute" \
  -H "Authorization: Bearer $OPEN_TERMINAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command": "ls -la /workspace"}'
# → {"stdout": "...", "stderr": "", "exit_code": 0}
```

### List directory

```bash
curl "$OPEN_TERMINAL_URL/files/list?path=/workspace" \
  -H "Authorization: Bearer $OPEN_TERMINAL_API_KEY"
# → {"files": [{"name": "...", "path": "...", "type": "file|dir", "size": 0}]}
```

### Upload a file

```bash
curl -X POST "$OPEN_TERMINAL_URL/files/upload" \
  -H "Authorization: Bearer $OPEN_TERMINAL_API_KEY" \
  -F "file=@script.py" \
  -F "path=/workspace/script.py"
# → {"status": "ok", "path": "/workspace/script.py"}
```

### Download a file

```bash
curl "$OPEN_TERMINAL_URL/files/download?path=/workspace/output.txt" \
  -H "Authorization: Bearer $OPEN_TERMINAL_API_KEY" \
  -o output.txt
# → (raw file bytes written to output.txt)
```

### Interactive terminal (WebSocket)

```
ws://<host>:8000/terminal?token=$OPEN_TERMINAL_API_KEY
```

---

## Common agent workflows

```bash
# Install a package and run a script
curl -X POST "$OPEN_TERMINAL_URL/execute" \
  -H "Authorization: Bearer $OPEN_TERMINAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command": "pip install pandas && python3 -c \"import pandas; print(pandas.__version__)\""}'

# Clone a repo and run tests
curl -X POST "$OPEN_TERMINAL_URL/execute" \
  -H "Authorization: Bearer $OPEN_TERMINAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command": "git clone https://github.com/owner/repo /workspace/repo && cd /workspace/repo && npm test"}'

# Process a file
curl -X POST "$OPEN_TERMINAL_URL/execute" \
  -H "Authorization: Bearer $OPEN_TERMINAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command": "python3 /workspace/process.py /workspace/input.csv > /workspace/output.json"}'
```

---

## Rules

- **Always check `exit_code`.** Non-zero means failure — read `stderr` to diagnose.
- **Use `/workspace`** as the working directory. It persists for the session.
- **Sandbox with Docker** when running untrusted or agent-generated commands.
- **Never expose without `--api-key`.** Set it on startup and rotate if compromised.
- **Never embed credentials in command strings.** Pass them via environment variables or stdin to prevent exposure in logs and process listings.
- **Long commands:** Background with `command &` or use the process management API.
- **Interactive input needed:** Use the WebSocket endpoint, not `/execute`.
