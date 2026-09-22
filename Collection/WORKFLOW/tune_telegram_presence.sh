#!/usr/bin/env bash
set -Eeuo pipefail

# Make Hermes Telegram presence less robotic:
# - no continuous "typing..." bubble for the entire tool/model turn
# - keep one edit-in-place long-running heartbeat
# - keep tool breadcrumbs off on Telegram
# - keep real interim assistant commentary enabled
#
# Applies to Anna/default plus dan, amy, tom, cody, nick, tim.
# Backs up every config before writing, validates every profile, then restarts gateway once.

HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
PROFILES=(anna dan amy tom cody nick tim)
STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_ROOT="$HERMES_HOME/backups/telegram-presence-$STAMP"
mkdir -p "$BACKUP_ROOT"

profile_root() {
  if [[ "$1" == "anna" ]]; then
    printf '%s\n' "$HERMES_HOME"
  else
    printf '%s\n' "$HERMES_HOME/profiles/$1"
  fi
}

check_profile() {
  if [[ "$1" == "anna" ]]; then
    hermes config check >/dev/null
  else
    hermes -p "$1" config check >/dev/null
  fi
}

echo "================================================================"
echo "HERMES TELEGRAM PRESENCE — FIX + VALIDATE"
echo "================================================================"

for p in "${PROFILES[@]}"; do
  root="$(profile_root "$p")"
  cfg="$root/config.yaml"

  [[ -f "$cfg" ]] || {
    echo "[FAIL] Missing config for $p: $cfg" >&2
    exit 1
  }

  cp -a "$cfg" "$BACKUP_ROOT/$p-config.yaml"

  python3 - "$cfg" <<'PY'
from pathlib import Path
import sys, yaml

p=Path(sys.argv[1])
cfg=yaml.safe_load(p.read_text(encoding="utf-8")) or {}

gateway=cfg.setdefault("gateway", {})
platforms=gateway.setdefault("platforms", {})
telegram=platforms.setdefault("telegram", {})
telegram["typing_indicator"]=False

display=cfg.setdefault("display", {})
dplats=display.setdefault("platforms", {})
dtg=dplats.setdefault("telegram", {})
dtg["tool_progress"]="off"
dtg["busy_ack_detail"]=False
dtg["interim_assistant_messages"]=True
dtg["long_running_notifications"]=True

p.write_text(
    yaml.safe_dump(cfg, allow_unicode=True, sort_keys=False),
    encoding="utf-8"
)
PY

  check_profile "$p"
  echo "[PASS] $p: typing_indicator=false; heartbeat=on; tool_progress=off"
done

export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"
export DBUS_SESSION_BUS_ADDRESS="${DBUS_SESSION_BUS_ADDRESS:-unix:path=$XDG_RUNTIME_DIR/bus}"

systemctl --user restart hermes-gateway.service
sleep 5

if systemctl --user is-active --quiet hermes-gateway.service; then
  echo "[PASS] hermes-gateway.service active"
else
  echo "[FAIL] gateway did not become active" >&2
  systemctl --user status hermes-gateway.service --no-pager -l || true
  exit 1
fi

echo
echo "=== EFFECTIVE CONFIG CHECK ==="
for p in "${PROFILES[@]}"; do
  root="$(profile_root "$p")"
  python3 - "$p" "$root/config.yaml" <<'PY'
import sys, yaml
name,path=sys.argv[1],sys.argv[2]
cfg=yaml.safe_load(open(path,encoding="utf-8")) or {}
tg=((cfg.get("gateway") or {}).get("platforms") or {}).get("telegram") or {}
dtg=((cfg.get("display") or {}).get("platforms") or {}).get("telegram") or {}
print(
    f"{name}: typing_indicator={tg.get('typing_indicator')} | "
    f"long_running_notifications={dtg.get('long_running_notifications')} | "
    f"tool_progress={dtg.get('tool_progress')} | "
    f"busy_ack_detail={dtg.get('busy_ack_detail')}"
)
PY
done

echo
echo "================================================================"
echo "PASS — Telegram will no longer show continuous typing for turns."
echo "Long tasks still keep the edit-in-place Working heartbeat."
echo "Backup: $BACKUP_ROOT"
echo "================================================================"
