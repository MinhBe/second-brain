---
name: vercel-ai-gateway
description: "Routes OpenAI-compatible chat completions, embeddings, and image generation through Vercel's AI Gateway for cost-effective edge inference. Use when the user asks to 'use Vercel AI Gateway', 'Vercel AI proxy', 'route OpenAI calls through Vercel', 'set up Vercel AI', or 'cheaper OpenAI-compatible inference'. Reads the VERCEL_AI_GATEWAY_KEY environment variable — never hardcoded."
license: MIT
compatibility: "Claude Code, Cursor, Codex, Gemini CLI, VS Code, Copilot, Amp, Roo Code, Goose, Windsurf, Continue"
allowed-tools: Bash(python:*) Read
---

# Vercel AI Gateway

OpenAI-compatible proxy for cost-effective AI inference through Vercel's edge network.

## Quick Start

```python
import httpx
import os

client = httpx.Client(
    base_url="https://api.vercel.ai/v1",
    headers={"Authorization": f"Bearer {os.environ['VERCEL_AI_GATEWAY_KEY']}"}
)
response = client.post("/chat/completions", json={
    "model": "gpt-4o-mini",
    "messages": [{"role": "user", "content": "Hello!"}]
})
```

## Provider Details

- **API Base:** `https://api.vercel.ai/v1`
- **Auth:** `Bearer $VERCEL_AI_GATEWAY_KEY`
- **Format:** OpenAI-compatible (chat completions, embeddings, images)
- **Cost:** Pay-per-use through Vercel billing
- **Key stored in:** `.kortix/secrets/vercel-ai-gateway.env`
- **Owner:** muffy86

## Supported Models (via Vercel Gateway)

| Model | Input $/1K | Output $/1K | Vision |
|-------|-----------|-------------|--------|
| gpt-4o-mini | $0.00015 | $0.0006 | Yes |
| gpt-4o | $0.0025 | $0.01 | Yes |
| claude-3-5-sonnet | Varies | Varies | Yes |

## Integration Points

- **Kortix Brain Router:** Available as `vercel-gateway` model in `TASK_CHAINS` (default, fast, coding chains)
- **Env key:** `VERCEL_AI_GATEWAY_KEY`
- **Competitive advantage:** Cheaper than direct OpenAI for bulk inference; Vercel's edge = lower latency

## When To Use

- Bulk inference where cost matters (PDR estimates, data processing)
- Fallback when free tiers (Groq, NVIDIA, Venice) are rate-limited
- Vision tasks needing OpenAI-compatible API
- Replaces direct OpenAI calls for cost-sensitive workloads

## Related Skills
- `multi-model-router` — Uses Vercel Gateway as a tier in the routing chain
- `venice-ai-integration` — Alternative free provider stack