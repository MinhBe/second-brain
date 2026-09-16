# pi-interactive-subagents on Windows — scout report

## Goal

Make `./Ω/SKILL/pi-interactive-subagents` usable on Windows.

## Finding

The local fork is **tmux-only**:

- entry uses `./Ω/SKILL/pi-interactive-subagents/pi-extension/subagents/tmux.ts`
- availability requires both:
  - `$TMUX` env var
  - `tmux` binary on PATH

So native Windows without a multiplexer will not work.

## Best route: WSL2

Most reliable path: run pi inside WSL2, not native Windows.

Why:

- real Linux `tmux`
- extension can stay close to original design
- shell scripts, signals, panes, `bash`, `$?` all work normally
- fewer Windows path/shell translation bugs

Setup shape:

```bash
# inside WSL2
sudo apt update
sudo apt install -y tmux nodejs npm git ripgrep fd-find python3 python3-venv
npm install -g @earendil-works/pi-coding-agent
cd ./Second\ Brain
pi install git:github.com/amosblomqvist/pi-interactive-subagents

tmux new -A -s pi 'pi'
```

If using repo-local copy:

```bash
mkdir -p ~/.pi/agent/extensions
cp -r ./Ω/SKILL/pi-interactive-subagents/pi-extension/subagents ~/.pi/agent/extensions/subagents
```

Then in pi:

```text
/reload
/subagents_list
```

## Second route: MSYS2

Possible, but less reliable than WSL2.

Setup shape:

```bash
pacman -Syu
pacman -S tmux nodejs npm git ripgrep fd python python-pip
npm install -g @earendil-works/pi-coding-agent
cd ./Second\ Brain
tmux new -A -s pi 'pi'
```

Risk:

- Windows Node reports `process.platform === "win32"`
- MSYS2 shell paths and Windows paths may mix
- tmux panes may run bash while pi/npm tooling may resolve Windows-style paths

Use MSYS2 only if WSL2 is not acceptable.

## GitHub scout

Found relevant forks/issues:

### 1. Psmux Windows fork

`https://github.com/LowOnContext/pi-interactive-subagents-windows`

Claims support for:

- Windows
- PowerShell 7+ / `pwsh`
- Psmux, a tmux-compatible Windows multiplexer

Important implementation ideas from that fork:

- detect Windows shell: `pwsh` → `powershell` → `bash`
- create `.ps1` scripts on Windows instead of `.sh`
- translate bash launch syntax to PowerShell syntax
- use `where.exe` for command detection on Windows
- keep the extension logic mostly tmux-compatible through Psmux

This is the best source if we want **native Windows** instead of WSL.

### 2. WezTerm fork

`https://github.com/pedritojr1209/pi-interactive-subagents-for-wezterm`

Claims support for:

- native Windows 10/11
- WezTerm panes
- PowerShell 7+

Important implementation ideas:

- add a mux abstraction layer: `mux.ts`
- select backend by `PI_SUBAGENT_MUX=wezterm|tmux|auto`
- detect `$WEZTERM_PANE`
- use `wezterm cli split-pane`, `send-text`, `get-text`, `kill-pane`
- use `.ps1` scripts for pwsh

This is likely cleaner than Psmux long-term, but bigger patch.

### 3. Upstream HazAT fork

`https://github.com/HazAT/pi-interactive-subagents`

Supports multiple multiplexers:

- cmux
- tmux
- zellij
- WezTerm

Useful as upstream reference, but larger/different feature surface.

## Recommendation

Use this order:

1. **WSL2 + tmux** — fastest path to working subagents.
2. **WezTerm backend** — best native Windows UX if we want to patch code.
3. **Psmux fork** — useful compatibility reference, but depends on Psmux behavior.
4. **MSYS2 + tmux** — possible, but only after WSL2 is tested.

## Patch strategy for local repo

Minimum for WSL2:

- no major code patch needed
- run pi from inside WSL2 tmux
- install extensions in WSL pi config, not Windows pi config

Minimum for native Windows:

- copy mux ideas from the WezTerm fork
- add `mux.ts`, `wezterm.ts`, `command-available.ts`
- change imports from `./tmux.ts` to `./mux.ts`
- add PowerShell-safe long-command script generation
- test `subagent`, `subagent_message`, `subagents_list`

## Decision

For your stated target “WSL/MSYS2”, start with **WSL2**.

Do not spend time forcing native Windows tmux first. The extension was designed for Unix tmux; WSL2 gives it that environment directly.
