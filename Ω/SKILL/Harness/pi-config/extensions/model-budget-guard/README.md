# Model Budget Guard

Pi extension for two separate problems that should not be confused:

1. **Quota / allowance**: how much of a subscription or provider limit is left.
2. **Price / billing risk**: whether the selected model can create pay-per-token charges.

The extension keeps those concepts separate because a subscription model can have a non-zero API list price while costing **$0 extra** through the subscription allowance.

## Default policy

The default policy matches the current setup this extension was created for:

| Provider | Pi auth/use | Default guard |
|---|---|---|
| `openai-codex` | ChatGPT subscription | allowed |
| `xai` | Grok/X subscription | allowed |
| `github-copilot` | Copilot subscription | allowed |
| `google` | Gemini API key | allowed, billing tier cannot be verified from the key |
| `opencode` | OpenCode Zen API key | **free-only, fail-closed** |

For OpenCode Zen, a model is allowed only when Pi's current model catalog reports all token price fields as zero. A paid model, or a model with missing price metadata when `failClosed=true`, is immediately rejected and Pi switches back to a safe model.

This avoids maintaining a brittle hard-coded list of Zen free models. OpenCode changes temporary free models often enough that a static list would age like milk left beside a GPU exhaust.

## Install

Copy the directory into the global Pi extension directory:

```powershell
New-Item -ItemType Directory -Force "$HOME\.pi\agent\extensions\model-budget-guard" | Out-Null
Copy-Item -Recurse -Force ".\Ω\SKILL\pi-config\extensions\model-budget-guard\*" "$HOME\.pi\agent\extensions\model-budget-guard\"
```

Then restart Pi or run:

```text
/reload
```

No config file is required for the default policy.

## Commands

### `/ai-usage`

Shows one combined quota/billing snapshot:

- OpenAI Codex subscription windows from the ChatGPT usage endpoint.
- GitHub Copilot plan/quota snapshots when the account endpoint exposes them.
- xAI Grok subscription pool, reset, on-demand cap and prepaid balance when the consumer OAuth endpoint exposes them.
- Gemini safety status and why exact remaining RPM/TPM/RPD cannot be recovered from an ordinary API-key response.
- OpenCode Zen free/paid catalog counts and whether free-only enforcement is active.
- Current Pi session token usage and **API-equivalent** cost estimate.

Provider quota endpoints are best-effort and can change upstream. Errors are displayed instead of silently inventing a number.

### `/ai-models`

Shows every currently available model, its Pi price metadata, and whether the guard allows it.

```text
/ai-models
/ai-models opencode
/ai-models google
```

Prices are USD per 1M tokens as supplied by Pi's current model catalog.

### `/ai-policy`

Shows the effective provider policy and allowed/blocked counts.

### `/ai-budget-clear`

Clears the usage/model widget.

## Config

Copy `model-budget-guard.example.json` to either:

```text
~/.pi/agent/model-budget-guard.json
```

or, for one project only:

```text
<project>/.pi/model-budget-guard.json
```

Project config overrides global config.

Useful rules:

```json
{
  "providers": {
    "opencode": {
      "mode": "free-only"
    },
    "google": {
      "allow": ["gemini-3.5-flash", "gemini-3.1-flash-lite"]
    },
    "github-copilot": {
      "deny": ["some-expensive-model*"]
    }
  }
}
```

`allow` and `deny` accept `*` and `?` wildcards and can use either a model id or `provider/model`.

## What is actually enforceable

### OpenCode Zen

**Strong enforcement.** `free-only` checks Pi's current per-token pricing metadata and blocks non-zero or unknown prices. Also disable OpenCode Zen auto-reload in the OpenCode console. The extension cannot change account-side billing settings.

### Gemini API

**Model allowlisting is enforceable; billing tier is not verifiable from an API key alone.** Google applies Gemini limits at the project level and exposes the authoritative live limits/usage in AI Studio. If the project is meant to stay at $0, keep that project on the Free tier / without paid billing and optionally add an explicit model allowlist here.

### Subscription providers

Codex, xAI and Copilot are treated as subscription providers. Their model catalog may still contain non-zero API-equivalent prices; those are not interpreted as an extra charge. `/ai-usage` instead reports subscription allowance / credits where available.

If a provider account enables paid overage, that is an account billing setting. The extension warns when Copilot's quota response explicitly says overage is permitted, but it does not alter GitHub/xAI/OpenAI billing settings.

## Security

The extension resolves credentials through Pi's model registry. It does not read or print `auth.json` directly and never writes credentials.

Quota requests are restricted in code to provider-owned hosts:

- `chatgpt.com`
- `api.github.com`
- `cli-chat-proxy.grok.com`

The Codex, Copilot and xAI consumer usage routes are provider/client integration endpoints and may change. A failure only disables the quota read; it does not disable the model guard.

## Why this lives beside `analyze-sessions`

`skills/analyze-sessions/scripts/cost.py` already answers the historical question: **what did past Pi sessions cost according to recorded message usage?**

This extension answers the runtime questions instead:

- what is left now?
- what is this model's listed price?
- is this model permitted before the next request is sent?
