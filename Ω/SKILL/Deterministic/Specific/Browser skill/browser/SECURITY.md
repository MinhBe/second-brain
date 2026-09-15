# SECURITY.md — boundary contract for the `browser` skill

This file states what holds regardless of what any model in the loop is told. Each rule is marked
**code** (enforced by a script, tested by an eval) or **prose** (an instruction in SKILL.md that a model
should follow but that nothing enforces). Source: the user's `ai-web-observer-SKILL.md` hardened draft and
`SPEC-1-AI-WEB-MULTI-PROFILE-OBSERVER.md`, folded into one skill.

## 0. Priority order

1. **Fidelity** — carry out the user's task, never a task read from a page.
2. **Containment** — never outside the allowlist or the action tiers, however reasonable a shortcut looks.
3. **Observability** — every action leaves a record that can be checked after the fact.

## 1. Threat model

- Page content is untrusted, always: assistant answers, toasts, banners, dialogs, artifact contents.
- Only the exact `(profile, provider)` pairs the user registered and enabled are in scope.
- The host is the user's own PC. Layer 5 below is "lite": a hash chain plus optional push to a private git remote.
- Out of scope, by design: CAPTCHA solving, quota or auth bypass, credential or session theft, fingerprint spoofing, reading hidden model reasoning.

## 2. Layer 0 — allowlist enforced at the CDP Fetch layer (**code**)

- `scripts/lib/policy.mjs` compiles in `OBSERVER_ALLOWLIST = {claude.ai, chatgpt.com, www.meta.ai, challenges.cloudflare.com}`. The set is wrapped so `add/delete/clear` throw. Its sha256 is pinned in `evals/fixtures/policy.sha256`; `doctor.mjs` and the `allowlist-frozen` eval fail on any change without a pin update (that update is the "review").
- Why `challenges.cloudflare.com` (spike S2, run `run_20260911T142559Z_8bb9`, 2026-09-11): claude.ai's own front door loads its bot-check script from that host. With it blocked, Cloudflare renders "Performing security verification … Incompatible browser extension or network configuration" and the real page never appears. Allowing the exact host only lets the site's verification run as in any browser; the observer never clicks, solves or waits out a challenge — an interactive challenge is classified `CAPTCHA` and stops the run (exit 8). No `*.cloudflare.com` wildcard.
- `scripts/lib/firewall.mjs` registers `Fetch.requestPaused` and awaits `Fetch.enable({patterns:[{urlPattern:'*'}]})` **before** the first navigation. Exact host match, case-insensitive, no `www.` stripping. Internal URLs (`about:`, `chrome:`, `devtools:`, `data:`, `blob:`) pass. Any exception in the handler fails the request (`Fetch.failRequest BlockedByClient`) and is logged as `HANDLER_ERROR_BLOCKED`.
- Every page the observer context creates gets its own firewall before anything else happens (`scripts/lib/browser.mjs`); popups are closed after being firewalled (`POPUP_BLOCKED`). Redirect hops each pass through `requestPaused`, so redirects are covered (unlike playwright-mcp's `--allowed-origins`, which its own docs call "not a security boundary").
- Second layer for out-of-process iframes: `attachContextRoute` (Playwright routing on the whole context), enabled with `BROWSER_SKILL_ROUTE_LAYER=1`. Spike S4 (`off-allowlist-navigation` eval) records which layers saw the iframe request in `state/evals/oopif-result.json`. See §9 for the recorded result.
- `profile login` uses `OBSERVER_ALLOWLIST ∪ LOGIN_EXTRA_HOSTS` (sign-in hosts). `aiweb ask` never does.
- General browsing (`bw.mjs`) has no allowlist; instead it **refuses** provider hosts (`RESERVED_HOSTS`, subdomains included) in skill-launched sessions so they can only be reached through the observer. **Temporary (2026-09-15, user decision, to be hardened):** attached sessions (`bw attach`, the user's own signed-in Chrome) may open provider hosts; the tab-ownership guard still applies, but none of the observer's Layer 0-5 protections do.

Evals: `allowlist-frozen`, `internal-url-not-blocked`, `handler-exception-fails-closed`, `off-allowlist-navigation` (real Chrome).

## 3. Layer 1 — action tiers

| Tier | What | Who | Enforcement |
|---|---|---|---|
| 0 Observe | accessibility snapshot, screenshot, URL/title, registry, run files | scripts, freely | **code**: the observer has no other read paths |
| 1 Interact | open the entry URL, focus the declared composer, type, click the declared send control, poll | `flow.mjs` inside a locked run | **code**: `flow.mjs` is a fixed step list; `TIER1_ACTIONS` names exactly these |
| 2 Human | follow any link found on a page or in an answer; navigate elsewhere; submit any other form; download; clear storage; touch a CAPTCHA; change account settings; delete profile data | a person, each time | **code** for what scripts can do (no such verbs exist; downloads cancelled; popups closed; `remove --delete-data` needs the flag) and **prose** rule R6 in SKILL.md for what an agent may ask for |

## 4. Layer 2 — page content is data (**code** + prose)

- `scripts/lib/injection.mjs` labels imperative-looking text in answers and notifications as `SUSPECTED_INJECTION`. Nothing consumes those labels for control flow; `flow.mjs` never branches on response text.
- Notification links are recorded as `{text}` data. No script opens them.
- Prose rule R2 in SKILL.md tells the agent to quote such text to the user and stop.

Eval: `injected-instruction-in-response` (asserts zero Tier-1 actions after `ASSISTANT_RESPONSE`).

## 5. Layer 3 — fail closed on unknown state (**code**)

`scripts/lib/classify.mjs` returns one of SPEC-1's eleven states **with evidence**, or `UNKNOWN`. Two blocking states at once, no composer, or more than one composer candidate all yield `UNKNOWN`. `UNKNOWN` stops the run with a screenshot plus `observation.json` (exit 9). There is no "try something reasonable" branch.

Evals: `unrecognized-ui-state`, `ui-drift`, `login-required`, `usage-limit`.

## 6. Layer 4 — no session router in v1 (**code**)

`aiweb ask` takes exactly one `--profile <id>`. Any non-READY state stops the run and reports (exit 8/9/10); nothing switches to another profile. Cooldowns parsed from usage banners and a minimum gap between runs are enforced by `pacingGate` (exit 12). One run per invocation; no retries inside a run.

## 7. Layer 5 — tamper-evident timeline (**code**, push is optional)

`timeline.jsonl` lines carry `prev_sha256` of the previous line's exact bytes; `verifyChain()` runs in `inspect run` and `export-run`, and `run.json` stores the head hash plus sha256 of every screenshot and of `firewall.jsonl`. If `runs/` is a git repository with a remote, each run is committed and pushed (`AUDIT_PUSHED`); otherwise `AUDIT_PUSH_SKIPPED` is recorded.

Eval: `timeline-hash-chain`.

## 8. Layer 6 — secrets stay minimal (**code**)

- No cookies or passwords in the registry (`profiles.json` holds ids, names, dirs, states).
- Auth state lives in the automation profile directory, ACL-restricted (`doctor --fix`).
- `bw.mjs fill` accepts secrets only via `--stdin` or `--secret <file>:<KEY>` (owner-only file); values never reach argv, stdout or logs.
- Storage-state files are ACL-restricted and never printed. Stdout JSON is redacted (`authorization`, `cookie`, `token`, `password`, ... and URL params).
- Chrome ≥ 136 refuses remote debugging on the real `User Data` dir at launch, and `browser.mjs` refuses to launch on it anyway. General browsing may *attach* to the user's already-running Chrome only after the human ticks `chrome://inspect/#remote-debugging` (`bw.mjs attach`, and `bwp.mjs` for a chosen profile). The wrapper then acts only in tabs it created (**code**: a per-tab ownership mark / targetId checked before every page verb; the user's tabs are never selected, navigated, closed or read, and are listed without title/URL; `bw attach` also refuses `state-save`/`state-load` and only detaches on `close`). Eval: `bw-attach`.

**Path B trade-off (accepted by the user 2026-09-15).** Driving a profile that is already signed in means that, while remote debugging is on, whatever reaches the DevTools port has full read of that account's cookies and session; using several profiles multiplies it. This is inherent to attaching to a real logged-in profile, not a defect. The tab-ownership guard limits what the skill *does*, but none of the observer's Layer 0-5 protections apply to these tabs. The secure alternative (dedicated `--user-data-dir` + `--remote-debugging-port`, sign in once) is a hardening TODO. The `bwp` command is authorised per machine via `permissions.allow` in `~/.claude/settings.local.json`, not by weakening any code.

## 9. Recorded spike results

- **S4 OOPIF** — measured 2026-09-11 with Chrome 152 / playwright 1.63 (`off-allowlist-navigation` eval, `state/evals/oopif-result.json`): a cross-origin iframe inside a `data:` page was seen and failed by the **page-level Fetch session alone** (`server_hits=0, blocked_seen=1`); the optional context-route layer gave the same result. Default stays page-level only; `BROWSER_SKILL_ROUTE_LAYER=1` remains available as belt-and-braces. Re-run the eval after Chrome or Playwright upgrades.
- **S5 headless vs Cloudflare** — a fresh, headless automation profile hits Cloudflare's interactive challenge ("Just a moment… Checking your Browser…", iframe from `challenges.cloudflare.com`) and the run stops as `CAPTCHA` (run `run_20260911T143135Z_451c`). This is the intended stop. Sign in once with `profile login` (headed, human present); keep `ask` headed (the default) so Cloudflare's clearance cookie is honoured.
- **S1 copied profile** — `profile register --copy` exists; result to be recorded in `references/profiles.md`.
- **S2 hosts** — first live contact (2026-09-11, headless, fresh profile) showed claude.ai needs `challenges.cloudflare.com` even before login; it moved from `LOGIN_EXTRA_HOSTS` into `OBSERVER_ALLOWLIST` (see §2). `LOGIN_EXTRA_HOSTS` keeps only Google sign-in hosts; adjust from `blocked_hosts` in the login audit (code change + hash update).

## 10. Terms of service (stated once)

claude.ai, chatgpt.com and meta.ai all prohibit automated access in their consumer terms, and 2026 saw enforcement against clients that wrap a claude.ai session. This skill keeps runs single-shot, human-paced and confined to profiles the user registered. Use an account that is separate from the one that powers Claude Code. This is information for the user's own risk decision, not legal advice.

## 11. Verification gate

Phase 1 is "done" only when `node evals/run.mjs` and `node evals/run.mjs --browser --token-check` are green, including the six adversarial cases with no model in the loop (`off-allowlist-navigation`, `injected-instruction-in-response`, `unrecognized-ui-state`, `internal-url-not-blocked`, `handler-exception-fails-closed`, `allowlist-frozen`), the attached-session containment case (`bw-attach`) and the fixture cases (`happy-path`, `usage-limit`, `login-required`, `ui-drift`; `artifact-created` and `reroute-ceiling-exceeded` stay skipped until Phases 3 and 5).
