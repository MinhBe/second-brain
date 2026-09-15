# Attaching to the user's real Chrome (`attach --extension`)

`attach --extension` connects playwright to the user's **own running Chrome** through the
Playwright MCP Bridge browser extension, instead of launching a fresh playwright browser. Use it
when the task needs the user's existing signed-in session — Google/YouTube, SSO, banking, anything
where a fresh automated browser would hit a login wall or bot challenge.

## When to use it vs `open`

- `open` / `open --headed`: fresh playwright-managed browser, isolated profile. Default for
  scripted automation and tests.
- `attach --extension`: drives the user's real Chrome + real profile (their cookies and logins).
  Use for "log into my account and do X" tasks. The user must have the extension installed.

## One-time setup

1. Install the **Playwright MCP Bridge** extension in the user's Chrome and pin it.
2. Grab its connection token (shown in the extension popup) and set it so attach skips the
   interactive "Share this tab" dialog:
   ```bash
   export PLAYWRIGHT_MCP_EXTENSION_TOKEN=<token-from-extension-popup>
   ```
   Persist it in the shell profile the Bash tool actually sources. On macOS, login shells read
   `~/.bash_profile` (which often sources `~/.bashrc`); a non-interactive tool shell may not have
   re-sourced it yet — if `echo $PLAYWRIGHT_MCP_EXTENSION_TOKEN` is empty, export it inline on the
   same command line as the attach.

## Attaching

```bash
# token set → connects immediately, no dialog
PLAYWRIGHT_MCP_EXTENSION_TOKEN=<token> playwright-cli -s=work attach --extension=chrome
```

- `--extension=chrome` targets Chrome; bare `--extension` lets the bridge pick the browser.
- Use a **named session** (`-s=work`) so you don't disturb the `default` (often in-memory) browser.
  Pass the same `-s=work` to every follow-up command.
- **Without the token**, attach blocks ~30s waiting for the user to click the extension icon →
  **Share this tab** / Connect, and errors with `Timeout 30000ms exceeded` if they don't. A
  websocket that *connects* and then times out is the signature of "token missing / tab not shared."

## After attaching

- The bridge exposes **one controllable tab** (it opens on the extension's `connect.html`). Just
  `goto` where you need — it navigates within the user's real profile, so their logins/cookies are
  live.
- `tab-list` shows only the shared tab, not every tab in their Chrome.
- You are driving the user's actual browser. Be conservative: confirm before destructive or
  outward-facing actions, don't navigate away from their work without reason, and prefer a
  dedicated session name.
- `playwright-cli -s=<name> detach` ends the playwright session and leaves Chrome running
  (`detach` is the verb for attach-created sessions; `close` is for `open`-created ones).
  Re-attaching later is trivial. If a session goes stale, `close` it and re-attach:
  ```bash
  playwright-cli -s=<name> close 2>/dev/null
  PLAYWRIGHT_MCP_EXTENSION_TOKEN=<token> playwright-cli -s=<name> attach --extension=chrome
  ```

## Alternative: CDP attach (`attach --cdp=chrome`)

`attach --cdp=chrome` connects to a running Chrome over the DevTools protocol instead of the
bridge extension — no extension or token needed, and it sees **all** tabs, not one shared tab.
The catch: the user must first enable it in that Chrome via `chrome://inspect/#remote-debugging`
→ "Allow remote debugging for this browser instance", which usually requires a browser restart.
Prefer the extension route once it's set up; reach for CDP if the extension is
unavailable or you genuinely need multi-tab visibility.

## Driving complex web apps (Polymer / shadow DOM, e.g. YouTube Studio)

- **Read state with the ARIA `snapshot`, not `eval` + `querySelectorAll`.** `querySelectorAll`
  does **not** pierce shadow roots, so buttons/fields inside web components come back `null`; the
  ARIA snapshot pierces them and gives stable refs.
- **Prefer NATIVE interactions over `fill` + synthetic events.** Click real option/radio refs and
  type real keystrokes (`click <fieldRef>` then `type "..."`). Native input reliably trips the
  framework's dirty-tracking so Save/Publish enables.
- **`fill` may not register, and synthetic `dispatchEvent` can *wedge* the form.** Setting `.value`
  doesn't fire the `input` event the framework wants, so Save stays disabled. Dispatching
  `input`/`change`/`blur` yourself sometimes works — but on **chip/tag inputs** (e.g. Studio's
  channel Keywords) it can throw JS errors, discard the text on blur, and leave the section showing
  *"There seems to be an issue. Please review and try again."* with Save permanently disabled. If a
  section gets wedged, **Cancel/discard the dialog and reopen** — don't try to patch it live.
  Last-resort dispatch (use only if native typing is impossible):
  ```bash
  playwright-cli -s=<name> eval "el => { el.dispatchEvent(new Event('input',{bubbles:true})); el.dispatchEvent(new Event('change',{bubbles:true})); }" e509
  ```
- **Chip/tag inputs** (comma-separated keywords): `type` the value with a trailing comma to commit
  the last chip; each comma makes a chip, so `el.value` ends up holding only the uncommitted tail.
  Watch for **duplicate chip sets** if a reload's "Leave site?" prompt was dismissed instead of
  accepted — the old chips survive and you blow the char limit.
  - **To clear existing chips, find the chip-bar's "Delete all" control** (Studio renders a
    per-chip "Remove" icon-button plus one "Delete all" — `getByRole('button', {name:'Delete all'})`).
    Backspace-to-delete is unreliable here: it takes two presses per chip (highlight, then delete)
    and stalls after one, even from `run-code` with waits. "Delete all" clears them in one click.
  - Enter the value with the **stable role locator** `getByRole('textbox', {name:'Keywords'})` and
    drive it from a `run-code` script (`input.type(text, {delay: 18})`) — shell-loop keystrokes fire
    faster than the component re-renders and get dropped.
  - `run-code --filename` can only read files **inside the session's allowed roots** (the project /
    `.playwright-cli` dir), not `/tmp`.
- **Verify Save's real state**, not just the ARIA tag: `eval "el => el.disabled" <saveRef>`.
- **Reloads on a dirty form** fire a native "Leave site?" dialog that blocks `snapshot`/`eval`
  ("does not handle the modal state"); clear it with `dialog-accept` (to leave) or `dialog-dismiss`
  (to stay) before continuing.
- **Contenteditable fields** report `el.value === undefined`; read `el.innerText` instead. Note
  `.length` counts UTF-16 units, so emoji (🎬) count as 2 and may differ from a codepoint count.
- Refs go **stale** after the panel re-renders (tab switch, dropdown select). Re-snapshot before
  the next interaction.
