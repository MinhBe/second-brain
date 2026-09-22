#!/usr/bin/env bash
set -Eeuo pipefail

# Deploy the repository's chatgpt-thread-controller skill to the seven Hermes profiles.
# Usage:
#   ./deploy_chatgpt_thread_controller.sh history https://chatgpt.com/c/<conversation-id>
#
# The registry is local-only under ~/.hermes/chatgpt-threads.yaml.
# The script never writes ChatGPT conversation URLs back to this Git repository.

ALIAS="${1:-}"
THREAD_URL="${2:-}"

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
SKILL_SRC="$REPO_ROOT/Collection/SKILL/chatgpt-thread-controller"

HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
REGISTRY="$HERMES_HOME/chatgpt-threads.yaml"
BACKUP_ROOT="$HERMES_HOME/backups/chatgpt-thread-controller-$(date +%Y%m%d-%H%M%S)"

PROFILES=(anna dan amy tom cody nick tim)

profile_root() {
  local p="$1"
  if [[ "$p" == "anna" ]]; then
    printf '%s\n' "$HERMES_HOME"
  else
    printf '%s\n' "$HERMES_HOME/profiles/$p"
  fi
}

hermes_cmd() {
  local p="$1"
  shift
  if [[ "$p" == "anna" ]]; then
    hermes "$@"
  else
    hermes -p "$p" "$@"
  fi
}

echo "============================================================"
echo "DEPLOY CHATGPT THREAD CONTROLLER"
echo "============================================================"

[[ -f "$SKILL_SRC/SKILL.md" ]] || {
  echo "ABORT: skill source not found: $SKILL_SRC/SKILL.md" >&2
  exit 1
}

mkdir -p "$BACKUP_ROOT"

echo
echo "=== 1. BACKUP + SYNC SKILL TO ALL PROFILES ==="

for p in "${PROFILES[@]}"; do
  root="$(profile_root "$p")"
  [[ -d "$root" ]] || {
    echo "ABORT: missing Hermes profile root: $root" >&2
    exit 1
  }

  mkdir -p "$root/skills"
  dst="$root/skills/chatgpt-thread-controller"

  if [[ -e "$dst" ]]; then
    cp -a "$dst" "$BACKUP_ROOT/$p-chatgpt-thread-controller"
  fi

  rm -rf "$dst"
  mkdir -p "$dst"
  cp -a "$SKILL_SRC/." "$dst/"

  echo "[PASS] $p -> $dst"
done

echo
echo "=== 2. OPTIONAL LOCAL THREAD REGISTRY ==="

if [[ -n "$ALIAS" || -n "$THREAD_URL" ]]; then
  [[ -n "$ALIAS" && -n "$THREAD_URL" ]] || {
    echo "ABORT: provide both alias and URL, or neither." >&2
    exit 1
  }

  case "$THREAD_URL" in
    https://chatgpt.com/c/*) ;;
    *)
      echo "ABORT: expected https://chatgpt.com/c/<conversation-id>" >&2
      exit 1
      ;;
  esac

  python3 - "$REGISTRY" "$ALIAS" "$THREAD_URL" <<'PY'
from pathlib import Path
import sys
import yaml

path = Path(sys.argv[1])
alias = sys.argv[2].strip()
url = sys.argv[3].strip()

data = {}
if path.exists():
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
if not isinstance(data, dict):
    raise SystemExit("Invalid registry root")

threads = data.setdefault("threads", {})
if not isinstance(threads, dict):
    raise SystemExit("Invalid threads mapping")

threads[alias] = {
    "url": url,
    "reuse_existing_tab": True,
    "keep_open": True,
}

path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(
    yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
    encoding="utf-8",
)
path.chmod(0o600)
print(f"[PASS] local alias registered: {alias}")
PY
else
  echo "[SKIP] no alias/URL supplied; registry unchanged"
fi

echo
echo "=== 3. CONFIG CHECK ==="

for p in "${PROFILES[@]}"; do
  if hermes_cmd "$p" config check >/tmp/hermes-config-check-"$p".log 2>&1; then
    echo "[PASS] $p config"
  else
    echo "[FAIL] $p config"
    tail -n 40 /tmp/hermes-config-check-"$p".log || true
    exit 1
  fi
done

echo
echo "=== 4. SKILL DISCOVERY CHECK ==="

for p in "${PROFILES[@]}"; do
  if hermes_cmd "$p" skills list 2>&1 | grep -qi 'chatgpt-thread-controller'; then
    echo "[PASS] $p sees chatgpt-thread-controller"
  else
    echo "[WARN] $p skill not visible yet; gateway/session reload may be required"
  fi
done

echo
echo "=== 5. CHROME-REAL MCP CHECK ==="

MCP_PASS=0
MCP_FAIL=0

for p in "${PROFILES[@]}"; do
  out="/tmp/hermes-mcp-test-$p.log"
  if timeout 50s hermes_cmd "$p" mcp test chrome-real >"$out" 2>&1; then
    echo "[PASS] $p chrome-real"
    MCP_PASS=$((MCP_PASS+1))
  else
    echo "[WARN] $p chrome-real unavailable or not configured"
    grep -E 'list_pages|take_snapshot|fill_form|press_key|error|Error|not found|missing' "$out" | tail -n 12 || true
    MCP_FAIL=$((MCP_FAIL+1))
  fi
done

echo
echo "chrome-real PASS=$MCP_PASS FAIL=$MCP_FAIL"

echo
echo "=== 6. RESTART GATEWAY ONCE ==="

export XDG_RUNTIME_DIR="/run/user/$(id -u)"
export DBUS_SESSION_BUS_ADDRESS="unix:path=$XDG_RUNTIME_DIR/bus"

systemctl --user restart hermes-gateway.service

echo "Waiting for multiplexed gateway startup..."
sleep 130

systemctl --user is-active hermes-gateway.service || true
hermes gateway list || true

echo
echo "============================================================"
echo "DEPLOYMENT COMPLETE"
echo "Backup: $BACKUP_ROOT"
echo "Registry: $REGISTRY"
echo "============================================================"

if [[ -n "$ALIAS" ]]; then
  echo
  echo "Suggested Telegram test:"
  echo "Use ChatGPT thread '$ALIAS' and send: CHATGPT-BRIDGE-TEST-$(date +%s)"
fi
