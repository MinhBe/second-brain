#!/usr/bin/env bash
set -Eeuo pipefail

# One-pass repair + validation:
#   provider -> fallback/fast-fail -> authenticated ChatGPT browser bridge
#
# Usage:
#   bash Collection/WORKFLOW/repair_test_provider_and_browser.sh \
#     'https://chatgpt.com/c/<conversation-id>'
#
# If the primary provider is unhealthy, this script opens the official
# 'hermes fallback add' picker in the SAME run, then retests and continues.

TARGET_URL="${1:-}"
if [[ ! "$TARGET_URL" =~ ^https://chatgpt\.com/c/[A-Za-z0-9-]+/?$ ]]; then
  echo "Usage: $0 'https://chatgpt.com/c/<conversation-id>'" >&2
  exit 2
fi
TARGET_URL="${TARGET_URL%/}"

HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
CONFIG="$HERMES_HOME/config.yaml"
REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
BROWSER_FLOW="$REPO_ROOT/Collection/WORKFLOW/repair_and_test_chatgpt_browser.sh"
STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP="$HERMES_HOME/backups/provider-browser-onepass-$STAMP"
MODEL_LOG="$HERMES_HOME/logs/provider-onepass-last-test.log"

mkdir -p "$HERMES_HOME/backups" "$HERMES_HOME/logs"

banner() {
  echo
  echo "================================================================"
  echo "$1"
  echo "================================================================"
}

banner "HERMES PROVIDER + CHATGPT BROWSER — ONE PASS"

[[ -f "$CONFIG" ]] || { echo "[FAIL] Missing $CONFIG"; exit 1; }
[[ -x "$BROWSER_FLOW" || -f "$BROWSER_FLOW" ]] || {
  echo "[FAIL] Missing browser workflow: $BROWSER_FLOW"
  exit 1
}

cp -a "$CONFIG" "$BACKUP"
echo "[PASS] Config backup: $BACKUP"

banner "1. CURRENT PRIMARY ROUTE (SECRETS HIDDEN)"

python3 - "$CONFIG" <<'PY'
import sys, yaml
cfg=yaml.safe_load(open(sys.argv[1],encoding="utf-8")) or {}
m=cfg.get("model") or {}
if isinstance(m,str):
    print("model:", m)
else:
    print("provider:", m.get("provider","<auto>"))
    print("model:", m.get("default") or m.get("model") or m.get("name") or "<unset>")
    if m.get("base_url"):
        print("base_url:", m.get("base_url"))
fb=cfg.get("fallback_providers") or []
print("fallback_count:", len(fb) if isinstance(fb,list) else 0)
agent=cfg.get("agent") or {}
print("api_max_retries:", agent.get("api_max_retries","<default=3>"))
print("auto_recovery_cycles:", agent.get("auto_recovery_cycles","<default=5>"))
PY

banner "2. FAST FAILOVER SETTINGS"

python3 - "$CONFIG" <<'PY'
import sys, yaml
p=sys.argv[1]
cfg=yaml.safe_load(open(p,encoding="utf-8")) or {}
agent=cfg.setdefault("agent", {})
# One Hermes-level attempt before fallback; avoid stacking 3 full provider waits.
agent["api_max_retries"]=1
# Do not sit through the 15/30/60/60/60 post-fallback recovery ladder.
# If no provider works, fail quickly and visibly instead of looking like endless typing.
agent["auto_recovery_cycles"]=0
with open(p,"w",encoding="utf-8") as f:
    yaml.safe_dump(cfg,f,allow_unicode=True,sort_keys=False)
print("[PASS] agent.api_max_retries=1")
print("[PASS] agent.auto_recovery_cycles=0")
PY

hermes config check >/dev/null
echo "[PASS] Hermes config valid"

provider_test() {
  local marker="ANNA_PROVIDER_OK_$RANDOM$RANDOM"
  rm -f "$MODEL_LOG"
  set +e
  timeout 120s hermes chat \
    --oneshot \
    -Q \
    --max-turns 2 \
    -q "Reply with exactly: $marker" \
    >"$MODEL_LOG" 2>&1
  local rc=$?
  set -e
  cat "$MODEL_LOG"
  if grep -Fq "$marker" "$MODEL_LOG"; then
    echo "[PASS] Provider turn completed"
    return 0
  fi
  echo "[FAIL] Provider turn failed (exit=$rc)"
  return 1
}

banner "3. PRIMARY/FALLBACK RUNTIME TEST"

if ! provider_test; then
  banner "4. PROVIDER FAILED — ADD/SELECT FALLBACK IN THIS SAME RUN"
  echo "Current fallback chain:"
  hermes fallback list || true
  echo
  echo "The primary endpoint did not complete a minimal turn."
  echo "Choose a backup provider/model for which this Hermes host already has credentials."
  echo "The script will immediately retest after the picker closes."
  echo
  hermes fallback add

  banner "5. RETEST WITH FALLBACK ENABLED"
  if ! provider_test; then
    echo
    echo "[FAIL] No healthy inference route after fallback setup."
    echo "Browser automation was NOT attempted because an agent cannot issue tools without a working model."
    echo "Model log: $MODEL_LOG"
    exit 1
  fi
else
  echo "[PASS] Primary/fallback route is healthy"
fi

banner "6. FALLBACK CHAIN"
hermes fallback list || true

banner "7. AUTHENTICATED CHATGPT BROWSER REPAIR + END-TO-END TEST"
chmod +x "$BROWSER_FLOW"
bash "$BROWSER_FLOW" "$TARGET_URL"

banner "FINAL"
echo "[PASS] Provider route and ChatGPT browser workflow completed."
echo "Primary outages now fail over/fail fast instead of waiting through 3 retries + 5 recovery cycles."
