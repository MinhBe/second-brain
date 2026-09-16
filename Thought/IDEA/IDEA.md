# Pi Windows Migration Exercise

## Ground rule

- Second Brain root is `.`.
- Use relative links only: `./Ω/SKILL/...`, `./θ/IDEA/IDEA.md`.

## Duplicate cleanup

Deleted duplicate contents under:

- `./Ω/SKILL/amosblomqvist/*`

Remaining stub:

- `./Ω/SKILL/amosblomqvist/pi-config`

Reason: current agent process started inside that folder, so Windows keeps the empty directory locked. Delete it after restarting pi:

```bash
rmdir ./Ω/SKILL/amosblomqvist/pi-config
rmdir ./Ω/SKILL/amosblomqvist
```

## Windows patches done

Patched canonical skill source under `./Ω/SKILL/<repo>`:

- active imports: `@mariozechner/*` → `@earendil-works/*`
- deprecated imports also patched for safety
- `import.meta.url` path handling now uses `fileURLToPath()` where needed
- Python PDF render temp dir: `/tmp` → OS temp dir
- docs: `python3`/`brew`/Unix venv paths → Windows-friendly commands
- `pi-dictate`:
  - `pbcopy` → `clip.exe` on Windows
  - `rec` → `sox -d` on Windows
  - `/tmp` debug log → OS temp dir
- `visual-tools`:
  - PATH delimiter now uses `node:path.delimiter`
  - added Windows Chrome/ImageMagick paths
  - removed macOS-only `file:/Users/...` dev dependency
- `pi-interactive-subagents`:
  - `/tmp` sentinel path → OS temp dir
  - transcript basename now cross-platform

## Current readiness

| Item | Windows status |
|---|---|
| `prompt-snippets` | ready |
| `browser` | ready after `npm install` + `npx playwright install chromium` |
| `web-fetch` | ready after `npm install` |
| `web-search` | ready after API key setup |
| `ask-user-question` | ready |
| `bash-guard` | ready; shell behavior still needs live test |
| `pdf-reader` | patched; Python syntax checked |
| `youtube-transcript` | patched; needs `yt-dlp` |
| `analyze-sessions` | patched; Python syntax checked |
| `learn/teach` | ready |
| `learn/visualize` | patched; needs visual deps |
| `pi-dictate` | patched; needs SoX + Deepgram key |
| `pi-subagents` | patched; needs live subagent test |
| `pi-interactive-subagents` | code patched, but tmux-only; use WSL/MSYS2 or skip native Windows |
| `observational-memory` | likely ready; enable after basics |

## Windows deps

```powershell
winget install ChrisBagwell.SoX
winget install Gyan.FFmpeg
winget install yt-dlp.yt-dlp
```

For Python skills:

```powershell
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
```

## Verification done

```bash
python -m py_compile ./Ω/SKILL/pi-config/skills/pdf-reader/scripts/*.py ./Ω/SKILL/pi-config/skills/analyze-sessions/scripts/*.py ./Ω/SKILL/pi-config/skills/youtube-transcript/*.py
```

Result: OK.
