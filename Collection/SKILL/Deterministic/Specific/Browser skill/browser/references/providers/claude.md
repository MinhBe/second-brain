# Provider: Claude (claude.ai)

Data lives in `scripts/lib/providers/claude.mjs`. This page mirrors it for humans. Entries marked **TO_CAPTURE**
are best-known defaults that must be confirmed against a live, sanitized accessibility snapshot (see "Capturing").

- Entry URL: `https://claude.ai/new?incognito=` (Claude's incognito conversation mode, not Chrome incognito)
- Allowlisted host: `claude.ai` (exact)

## State rules (evaluated in order; first blocking match wins; two different blocking matches → UNKNOWN)

| rule | state | evidence source | pattern (summary) | provenance |
|---|---|---|---|---|
| captcha-turnstile | CAPTCHA | iframe title | cloudflare / security challenge / turnstile | best-known |
| cf-interstitial | CAPTCHA | visible text / title | "Just a moment..." / "Performing security verification" / "verifies you are not a bot" | **captured live 2026-09-11** (fixture `claude-cf-interstitial.json`) |
| captcha-text | CAPTCHA | visible text | verify you are human / security check / blocked from reaching challenges.cloudflare.com | best-known |
| verification | VERIFICATION_REQUIRED | visible text | verify your phone/email / enter the code / two-factor | best-known |
| login-url | LOGIN_REQUIRED | URL | `claude.ai/login`, `/magic-link`, `/oauth` | best-known |
| login-text | LOGIN_REQUIRED | visible text (not on /new or /chat) | continue with google / log in with / sign in to claude / create account | best-known |
| session-expired | SESSION_EXPIRED | visible text | session expired / you've been logged out / please log in again | best-known |
| usage-limit | USAGE_EXHAUSTED | visible text / alert | out of (free) messages / reached your usage limit / limit resets / until 5:40 AM | SPEC-1 example text |
| rate-limit | RATE_LIMITED | visible text | rate limit / too many requests / unusual activity / try again in a moment | best-known |
| unavailable | UNAVAILABLE | visible text | temporarily unavailable / under maintenance / 502 / 503 / experiencing an outage | best-known |
| error | ERROR | alert region | something went wrong / an error occurred / unable to / failed to | best-known |
| READY | READY | aria | exactly one composer candidate and no blocking rule | — |

## Locator ladders (exactly one match required, else ADAPTER_DRIFT → UNKNOWN)

| part | step | locator | provenance |
|---|---|---|---|
| composer | textbox-prompt | role `textbox`, name matches /prompt|message|help|reply|talk|ask/i | **TO_CAPTURE** |
| composer | contenteditable | css `div[contenteditable="true"][data-placeholder], div.ProseMirror[contenteditable="true"]` | **TO_CAPTURE** |
| send | send-button | role `button`, name /^send( message)?$/i ; fallback key Enter | **TO_CAPTURE** |
| generation started | stop-button | role `button`, name /^stop( response| generating)?$/i | **TO_CAPTURE** |
| generation started | assistant-node | css `[data-testid="assistant-message"], .font-claude-message, div[data-is-streaming]` | **TO_CAPTURE** |
| assistant message | assistant-testid / assistant-class / assistant-streaming-attr | same css candidates, last element read | **TO_CAPTURE** |
| artifact hint | artifact-button | role `button`, name /artifact|preview|open in|download/i (detected only) | best-known |

Reset time: `/until\s+(\d{1,2})(?::(\d{2}))?\s?([ap])\.?m\.?/i` → `HH:MM` local → next occurrence as `cooldown_until`.

## Live findings so far (2026-09-11)

- Fresh profile, headless, Cloudflare challenge host blocked → Cloudflare "Incompatible browser extension or network configuration" page. Fixed by allowlisting `challenges.cloudflare.com` (exact host).
- Fresh profile, headless, host allowed → Cloudflare interactive "Checking your Browser…" → classified `CAPTCHA`, exit 8. Expected: automation cannot and must not pass it. A human signs in once via `profile login` (headed); afterwards run `ask` **headed** (default) so the clearance cookie in the automation profile is honoured. `--headless` is for smoke tests only.

## Capturing a live snapshot (Phase C task, human present)

1. `profile login --id <id> --provider claude` until READY (human signs in).
2. `aiweb ask claude --profile <id> --prompt "Reply with exactly the word PONG." --dry-run` — the run dir gets `observation.json` with the real `aria_yaml`.
3. Read `aria_yaml`, note the exact composer / send / stop names and the assistant container selector; update `claude.mjs` and this table, set provenance to `captured <date>`.
4. Copy a **sanitized** version (no e-mails, names, conversation titles) over `evals/fixtures/observations/claude-ready.json`; run `node evals/run.mjs`.

## Terms of service (stated once)

claude.ai's consumer terms prohibit automated access; enforcement against session wrappers happened in 2026. Use a separate account from the one that powers Claude Code; keep runs human-paced and single-shot. SECURITY.md §10.
