# Exit codes

Every script prints exactly one JSON line on stdout and exits with one of these codes.
The JSON always has `ok`, `verb`, `code`, `exit`, and `next`. On failure it also has `error`.
Read `next` and do exactly that. Never improvise a different recovery.

| exit | code | meaning | what you do next |
|---|---|---|---|
| 0 | OK | success | follow `next` |
| 1 | INTERNAL | a bug in the skill | report `error` and `log_path` to the user; stop |
| 2 | USAGE | wrong or missing arguments, unknown verb, unsupported provider | fix the command exactly as `next` says; run it again once |
| 3 | PRECONDITION | dependency, directory, ACL, or version pin problem; or (`attach`) the user's Chrome has remote debugging off | do what `next` says: for `attach`, ask the user to tick `chrome://inspect/#remote-debugging` and run once more; otherwise run `node C:/Users/Admin/.claude/skills/browser/scripts/doctor.mjs` and report its output |
| 4 | NOT_FOUND | session, profile, run, or file does not exist | run the `list` or `inspect` command named in `next` |
| 5 | TARGET | element ref is stale, not found, or ambiguous | run `snapshot` (or `find`) once, retry the action once with the new ref, then report |
| 6 | TIMEOUT | a wait or an AI generation ran out of time | report; never loop or retry automatically |
| 7 | POLICY | blocked by the allowlist, a reserved host, or a Tier-2 action | tell the user what was refused and why; ask them to do it themselves |
| 8 | HUMAN | LOGIN_REQUIRED, USAGE_EXHAUSTED, RATE_LIMITED, CAPTCHA, VERIFICATION_REQUIRED | report `evidence` and the screenshot path; stop. Never fill credentials, never touch a CAPTCHA |
| 9 | UNKNOWN | the page state could not be classified (fail-closed) | report the evidence paths; stop |
| 10 | PROVIDER | the provider showed ERROR or UNAVAILABLE | report; stop |
| 11 | TOOL | playwright-cli or Chrome failed | run `bw.mjs kill-all`, then `doctor.mjs`; report |
| 12 | BUSY | profile locked, in cooldown, or pacing gap not elapsed | report the time in the JSON; stop |
| 13 | AUDIT | run files, hash chain, or push could not be written | report; stop |

Rules of thumb:

- Exit 5 is the only code where you retry on your own, and only once.
- Exit 8, 9, 10 mean a human must look. Do not "try another way".
- Exit 7 is not an error to work around. It is the boundary doing its job.
