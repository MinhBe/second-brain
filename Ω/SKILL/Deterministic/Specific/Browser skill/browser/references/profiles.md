# Profiles

## Two kinds of "profile"

| | Real Chrome profile | Logical (automation) profile |
|---|---|---|
| Where | `%LOCALAPPDATA%\Google\Chrome\User Data\<Default|Profile N>` | `profiles/<id>/user-data/` inside the skill |
| Identified by | directory name (`Profile 12`) and a display name (`TAnh`) | a stable `id` you choose (`p001`) |
| Used by | the human, in Chrome | `profile.mjs login` and `aiweb.mjs ask` |
| Can automation drive it? | **No.** Chrome ≥ 136 ignores remote debugging on the default User Data dir, and `browser.mjs` refuses it anyway | Yes |

Display names are labels, not identifiers (SPEC-1). The registry keeps both: `id` for scripts, `display_name` for people, `chrome_profile_directory` as a note of which real profile it mirrors.

## Registry — `profiles/profiles.json`

```json
{ "version": 1, "profiles": [ {
  "id": "p001", "display_name": "165", "chrome_profile_directory": "Profile 1",
  "automation_user_data_dir": "C:/.../browser/profiles/p001/user-data", "copied_from": null,
  "enabled": true, "created_at": "...", "updated_at": "...",
  "providers": { "claude": { "state": "READY", "evidence": {...}, "last_checked_at": "...", "last_success_at": "...", "cooldown_until": null } }
} ] }
```
No cookies, no passwords, no e-mail addresses. Auth state lives only inside the automation user-data-dir (ACL restricted).

## Procedure: first profile

```
node C:/Users/Admin/.claude/skills/browser/scripts/discover-profiles.mjs
node C:/Users/Admin/.claude/skills/browser/scripts/profile.mjs register --id p001 --name "165" --from-chrome "Profile 1"
node C:/Users/Admin/.claude/skills/browser/scripts/profile.mjs login --id p001 --provider claude
```
`login` opens a **headed** Chrome on the automation dir with the firewall set to the provider hosts plus sign-in hosts
(`LOGIN_EXTRA_HOSTS` in `scripts/lib/policy.mjs`). A person signs in. The script polls the page every 3 s and returns
`READY` once the composer is visible; it never types. If sign-in needs a host that was blocked, the JSON lists it under
`blocked_hosts` — adding it is a code change to `policy.mjs` plus a hash re-pin, not a runtime setting.

## Locks, cooldown, pacing

- `profiles/<id>/.lock` = `{run_id, pid, acquired_at, expires_at}`. A live lock (pid alive, not expired) makes `ask`/`login` exit 12. Stale locks are taken over.
- `cooldown_until` comes from a parsed usage-limit reset time and blocks `ask` until then.
- `--min-gap-sec` (default 60 s) keeps runs human-paced.

## Spike S1 — copying a real profile (`register --copy`)

`register --id <id> --name "<n>" --from-chrome "<Profile N>" --copy` copies `Local State` + the profile directory
(minus caches) into the automation dir and launches Chrome with `--profile-directory=<Profile N>`. Chrome must be closed.
Whether cookies survive depends on Chrome's App-Bound Encryption. **Result: not yet recorded** — run it once and note here
whether `profile login` reports READY without a manual sign-in. If it does not, keep the default: a fresh automation profile
and one manual sign-in.

## Which account?

Use a profile whose provider account is **not** the account that powers Claude Code. See SECURITY.md §10.
