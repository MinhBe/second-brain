# browser-use

A browser-automation skill for Claude Code and similar agent harnesses. It teaches the agent to drive a real browser through [`@playwright/cli`](https://www.npmjs.com/package/@playwright/cli): navigate, click, fill forms, run JS in-page, take ARIA snapshots, screenshots, and PDFs, manage tabs and storage, inspect and mock network requests, record traces and video, and run Playwright tests.

Not related to the [browser-use](https://github.com/browser-use/browser-use) Python library. The name describes what the skill does.

## What this is

A fork of the skill bundled with `@playwright/cli` (Microsoft, Apache-2.0), extended with guidance the stock skill doesn't cover:

- **Attach to the user's real Chrome** ([references/extension-attach.md](references/extension-attach.md)). Playwright-launched Chromium and WebKit get flagged by Google/OAuth as insecure browsers, so signed-in tasks attach to the user's own Chrome via the Playwright MCP Bridge extension instead of fighting a login wall. Covers token setup, stale-session recovery, and the CDP alternative.
- **House patterns.** One named session per task so parallel work never collides; snapshot-to-file plus grep for big pages instead of dumping them into context; exact-CSS-px resizing for pixel-accurate print capture; `--raw` for shell pipelines.
- **Web-component field notes.** Driving Polymer and shadow-DOM apps (the YouTube Studio class): ARIA snapshots over `querySelectorAll` (which doesn't pierce shadow roots), native keystrokes over synthetic events, chip/tag input handling, and recovering a wedged form.

## Install

The skill documents the CLI; you need both.

```bash
npm install -g @playwright/cli@latest
git clone https://github.com/Ilm-Alan/browser-use.git ~/.claude/skills/browser-use
```

Works in any harness that loads `SKILL.md` skills (`~/.codex/skills/`, etc.).

Do not also run `playwright-cli install --skills`: it installs the stock skill alongside this one as a near-duplicate. After upgrading the CLI, merge upstream skill changes by hand:

```bash
diff -r ~/.claude/skills/browser-use "$(npm root -g)/@playwright/cli/node_modules/playwright-core/lib/tools/cli-client/skill"
```

## License

Apache-2.0. Upstream skill content is from [Playwright](https://github.com/microsoft/playwright), Copyright (c) Microsoft Corporation. Modifications and additions Copyright (c) 2026 Alan. See [NOTICE](NOTICE).
