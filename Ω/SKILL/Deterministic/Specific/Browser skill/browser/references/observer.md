# AI Web Observer — reference

One `aiweb ask` = one run: one provider, one registered profile, one prompt, one browser, one audit folder.
The flow is a fixed list of steps (`scripts/lib/flow.mjs`). Nothing in it reads the model's answer to decide anything.

## Run lifecycle

```
ask ─ validate args ─ load profile ─ pacing gate ─ acquire lock ─ create run dir ─ RUN_STARTED
    ─ launch Chrome on profiles/<id>/user-data (firewall on BEFORE navigation) ─ BROWSER_LAUNCHED
    ─ PAGE_OPENED entry URL ─ screenshot 001 ─ classify
    ─ READY? no → stop with that state (screenshot, observation.json, notifications.json)
    ─ AUTH_VERIFIED ─ screenshot 002
    ─ composer ladder: exactly one match, else ADAPTER_DRIFT → UNKNOWN
    ─ COMPOSER_FOCUSED ─ PROMPT_TYPED ─ read back ─ COMPOSER_VERIFIED ─ screenshot 003   (--dry-run stops here)
    ─ send (button, else Enter) ─ PROMPT_SUBMITTED ─ screenshot 004
    ─ GENERATION_STARTED within 20 s (stop button or assistant node) ─ screenshot 005
    ─ poll every 1 s: progress every 5 s; a blocking banner mid-way stops the run with a partial response
    ─ complete = stop control gone AND text unchanged twice ─ GENERATION_COMPLETED
    ─ ASSISTANT_RESPONSE (response.md, sha256) ─ SUSPECTED_INJECTION labels ─ notifications ─ artifacts detected (not opened)
    ─ screenshot 006 ─ browser-state.json ─ registry update ─ RUN_COMPLETED / RUN_FAILED ─ lock released
    ─ run.json ─ report.md ─ AUDIT_PUSHED / AUDIT_PUSH_SKIPPED
```

## Exit code by terminal status

| status | exit | code |
|---|---|---|
| COMPLETED, DRY_RUN | 0 | OK |
| LOGIN_REQUIRED, SESSION_EXPIRED, USAGE_EXHAUSTED, RATE_LIMITED, CAPTCHA, VERIFICATION_REQUIRED | 8 | HUMAN |
| UNKNOWN (unclassified page, composer drift, no generation signal) | 9 | UNKNOWN |
| ERROR, UNAVAILABLE | 10 | PROVIDER |
| TIMEOUT (partial response saved) | 6 | TIMEOUT |
| profile locked, cooldown, pacing gap | 12 | BUSY |

## Provider states (SPEC-1)

`UNKNOWN READY LOGIN_REQUIRED SESSION_EXPIRED USAGE_EXHAUSTED RATE_LIMITED VERIFICATION_REQUIRED CAPTCHA ERROR UNAVAILABLE BUSY`

Every state except UNKNOWN comes with evidence `{type: url|visible_text|aria|alert|dialog|iframe, text, rule}`.
UNKNOWN is the default whenever rules disagree, nothing matches, or the composer is not exactly one element.

## Timeline events

SPEC-1: `PAGE_OPENED AUTH_VERIFIED AUTH_FAILED PROMPT_SUBMITTED GENERATION_STARTED GENERATION_PROGRESS GENERATION_COMPLETED ASSISTANT_RESPONSE NOTIFICATION WARNING ERROR USAGE_LIMIT RATE_LIMIT LOGIN_REQUIRED SESSION_EXPIRED CAPTCHA ARTIFACT_DISCOVERED ARTIFACT_OPENED ARTIFACT_READ DOWNLOAD_STARTED DOWNLOAD_COMPLETED NAVIGATION SCREENSHOT_CAPTURED RUN_COMPLETED RUN_FAILED`

Added by this skill: `RUN_STARTED PROFILE_SELECTED PROFILE_LOCK_ACQUIRED PROFILE_LOCK_RELEASED BROWSER_LAUNCHED BLOCKED_NAVIGATION HANDLER_ERROR_BLOCKED POPUP_BLOCKED DOWNLOAD_BLOCKED SUSPECTED_INJECTION ADAPTER_DRIFT COMPOSER_FOCUSED PROMPT_TYPED COMPOSER_VERIFIED STATE_CLASSIFIED DRY_RUN_STOP TIMEOUT AUDIT_PUSHED AUDIT_PUSH_SKIPPED`

Each line: `{seq, ts, event, tier (0 observe | 1 interact | 2 human | null), data, prev_sha256}`. Tier 1 events are the only actions the observer takes: `PAGE_OPENED, COMPOSER_FOCUSED, PROMPT_TYPED, PROMPT_SUBMITTED`.

## Run directory

```
runs/YYYY-MM-DD/run_<YYYYMMDDTHHMMSSZ>_<4hex>/
  run.json            ids, prompt + sha256, status, terminal_state, evidence, exit, policy_sha256, chrome, provider state before/after,
                      screenshots[{file,sha256,event}], firewall_summary, firewall_sha256, timeline_head_sha256, chain_ok, audit
  timeline.jsonl      hash-chained events
  firewall.jsonl      every Layer-0 decision {ts, requestId, url, host, resourceType, verdict, cdpDecision}
  response.md         the answer (or the partial answer on TIMEOUT / mid-run stop)
  notifications.json  [{source, raw_text, normalized_type, blocking, parsed{reset_time, cooldown_until}, observed_at, page_url}]
  browser-state.json  url, title, viewport, page_count, cookie_count (never cookie values)
  observation.json    the last observation (aria snapshot + alerts + dialogs + iframes) — always present on a stop
  report.md           export-run output with the 14 answers
  screenshots/        001-page-opened.png ... 006-final.png, or 0NN-<state>.png on a stop
  artifacts/          empty until Phase 3
```

## The 14 audit answers (`export-run`)

1 profile · 2 provider state before → after · 3 URLs opened · 4 Tier-1 actions · 5 prompt · 6 generation started? · 7 answer · 8 notifications · 9 raw usage-limit text · 10 reset time · 11 artifacts detected · 12 artifact contents (Phase 3) · 13 evidence paths + chain status · 14 terminal state.

## Pacing and cooldown

- `--min-gap-sec` (default 60) between two runs on the same (provider, profile). Enforced from `state/last-run/`.
- A usage-limit banner with "until 5:40 AM" sets `cooldown_until` on the profile's provider state; `ask` refuses until then (exit 12).
- Schedules are the user's decision; the skill never loops.

## What Phases 2–7 add (no layout change)

P2 toast/dialog polling generalized · P3 artifact reader (`artifacts/`, `aiweb artifacts` real) · P4 registry on `node:sqlite` · P5 session router (`--profile any-of:`), `PROFILE_REROUTED` · P6 ChatGPT + Meta adapters · P7 HTML reports and a cross-run index.
