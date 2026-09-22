#!/usr/bin/env bash
set -Eeuo pipefail

# Adopt the user's EXISTING logged-in Chrome profile for Hermes using Tencent BrowserSkill.
# This intentionally avoids Chrome DevTools --autoConnect and avoids launching a fresh Chrome profile.
#
# One-time browser-side requirement:
#   Install BrowserSkill in the exact Chrome profile the user already uses.
#   In the extension popup, turn OFF "Confirm before borrowing tabs".
# Those extension settings persist in that Chrome profile.
#
# Usage:
#   bash adopt_existing_chrome_browserskill.sh 'https://chatgpt.com/c/<conversation-id>'

TARGET_URL="${1:-https://chatgpt.com/}"
TARGET_URL="${TARGET_URL%/}"
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
STATE="$HERMES_HOME/browser-main.json"
TABS_STATE="$HERMES_HOME/browser-last-tabs.json"
SESSION_STATE="$HERMES_HOME/browser-active-session.json"
WEBSTORE='https://chromewebstore.google.com/detail/hhcmgoofomhgciiibhipgmgkgnoenaoi'

mkdir -p "$HERMES_HOME"

banner() {
  echo
  echo "================================================================"
  echo "$1"
  echo "================================================================"
}

banner "1. CHECK CURRENT CHROME — NO NEW PROFILE"

if pgrep -u "$(id -u)" -f '[g]oogle-chrome|[c]hromium' >/dev/null 2>&1; then
  echo "[PASS] Chrome/Chromium is already running."
  ps -u "$(id -u)" -o pid=,etime=,args= |
    grep -E '[g]oogle-chrome|[c]hromium' |
    grep -v -- '--type=' |
    sed -E 's/(--password-store=)[^ ]+/\1[hidden]/g' || true
else
  echo "[FAIL] No Chrome/Chromium process is running."
  echo "Open the Chrome profile that is already signed into ChatGPT, then rerun this same script."
  exit 1
fi

banner "2. LOCAL CHROME PROFILE / ACCOUNT INVENTORY"

python3 <<'PY'
from pathlib import Path
import json

roots=[
    Path.home()/".config/google-chrome",
    Path.home()/".config/chromium",
]
root=next((p for p in roots if (p/"Local State").is_file()), None)
if root is None:
    print("[WARN] Chrome Local State not found.")
    raise SystemExit(0)

try:
    state=json.loads((root/"Local State").read_text(encoding="utf-8"))
except Exception as e:
    print("[WARN] Could not parse Local State:", e)
    raise SystemExit(0)

profile=state.get("profile") or {}
print("Chrome data root:", root)
print("last_used:", profile.get("last_used"))
print("last_active_profiles:", profile.get("last_active_profiles"))

cache=profile.get("info_cache") or {}
for key,val in cache.items():
    if not isinstance(val,dict):
        continue
    # Only identity/routing fields. Never print auth tokens/cookies.
    print()
    print("PROFILE", key)
    for field in ("name","user_name","gaia_name","given_name","is_using_default_name","active_time"):
        v=val.get(field)
        if v not in (None,""):
            print(f"  {field}: {v}")
PY

banner "3. INSTALL / UPDATE BROWSERSKILL CLI + HERMES SKILL"

export PATH="$HOME/.local/bin:$PATH"

if ! command -v bsk >/dev/null 2>&1; then
  curl -fsSL https://raw.githubusercontent.com/Tencent/BrowserSkill/main/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi

bsk --version
bsk install-skill --harness hermes --force --json
echo "[PASS] Official browser-skill installed into Hermes."

# Start daemon / inspect extension connection.
set +e
BROWSERS_JSON="$(bsk browsers --json 2>/tmp/bsk-browsers.err)"
BROWSERS_RC=$?
set -e

browser_count() {
  python3 -c 'import json,sys
try:
    x=json.load(sys.stdin)
    print(len(x) if isinstance(x,list) else 0)
except Exception:
    print(0)'
}

COUNT="$(printf '%s' "$BROWSERS_JSON" | browser_count)"

if [[ "$BROWSERS_RC" != "0" || "$COUNT" == "0" ]]; then
  banner "4. ONE-TIME EXTENSION CONNECTION"

  echo "BrowserSkill is not connected to a Chrome profile yet."
  echo
  echo "ONE TIME ONLY, in the Chrome window/profile that is ALREADY logged into ChatGPT:"
  echo "  1. Install BrowserSkill from Chrome Web Store:"
  echo "     $WEBSTORE"
  echo "  2. Open the BrowserSkill extension popup in THAT SAME profile."
  echo "  3. Confirm it is connected."
  echo "  4. Automation settings -> turn OFF: Confirm before borrowing tabs."
  echo "     This setting is saved by the extension for this Chrome profile."
  echo "  5. Optional but recommended: set Browser name = HermesMain"
  echo
  echo "This replaces repeated Chrome remote-debugging consent."
  echo "We will NOT use --autoConnect and will NOT launch another Chrome profile."
  echo
  read -r -p "After doing that once, press ENTER here... " _

  READY=0
  for _ in $(seq 1 30); do
    set +e
    BROWSERS_JSON="$(bsk browsers --json 2>/tmp/bsk-browsers.err)"
    rc=$?
    set -e
    COUNT="$(printf '%s' "$BROWSERS_JSON" | browser_count)"
    if [[ "$rc" == "0" && "$COUNT" -gt 0 ]]; then
      READY=1
      break
    fi
    sleep 1
  done

  if [[ "$READY" != "1" ]]; then
    echo "[FAIL] BrowserSkill extension is still not connected."
    cat /tmp/bsk-browsers.err || true
    echo
    bsk doctor || true
    exit 1
  fi
fi

banner "5. CONNECTED REAL CHROME INSTANCES"
printf '%s\n' "$BROWSERS_JSON" | python3 -m json.tool

# Prefer already-saved instance if it is still online.
SAVED_INSTANCE=""
if [[ -f "$STATE" ]]; then
  SAVED_INSTANCE="$(python3 - "$STATE" <<'PY'
import json,sys
try:
    print(json.load(open(sys.argv[1],encoding="utf-8")).get("browser_instance_id",""))
except Exception:
    print("")
PY
)"
fi

INSTANCE="$(printf '%s' "$BROWSERS_JSON" | python3 - "$SAVED_INSTANCE" <<'PY'
import json,sys
saved=sys.argv[1]
arr=json.load(sys.stdin)
ids=[str(x.get("instance_id","")) for x in arr if isinstance(x,dict)]
if saved and saved in ids:
    print(saved)
elif len(ids)==1:
    print(ids[0])
PY
)"

if [[ -z "$INSTANCE" ]]; then
  echo
  echo "More than one BrowserSkill Chrome instance is connected."
  echo "Use the Instance ID shown above for the exact Chrome profile already logged into ChatGPT."
  read -r -p "Instance ID to permanently bind Hermes to: " INSTANCE
fi

# Validate explicit binding.
printf '%s' "$BROWSERS_JSON" | python3 - "$INSTANCE" <<'PY'
import json,sys
instance=sys.argv[1]
arr=json.load(sys.stdin)
if not any(str(x.get("instance_id",""))==instance for x in arr if isinstance(x,dict)):
    raise SystemExit("[FAIL] Selected BrowserSkill instance is not connected")
PY

banner "6. START SESSION PINNED TO THAT EXACT CHROME INSTANCE"

SESSION_JSON="$(bsk session start --browser "$INSTANCE" --name "Hermes ChatGPT" --json)"
printf '%s\n' "$SESSION_JSON" | python3 -m json.tool

SESSION_ID="$(printf '%s' "$SESSION_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["session_id"])')"
BROWSER_INSTANCE="$(printf '%s' "$SESSION_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["browser_instance_id"])')"

[[ "$BROWSER_INSTANCE" == "$INSTANCE" ]] || {
  echo "[FAIL] BrowserSkill returned a different browser instance."
  exit 1
}

banner "7. LIST WHAT IS CURRENTLY OPEN IN THAT REAL CHROME PROFILE"

bsk tab list --scope user --session "$SESSION_ID" --json | tee "$TABS_STATE" | python3 -m json.tool

banner "8. CREATE A NEW TAB USING THAT SAME LOGGED-IN PROFILE"

TAB_JSON="$(bsk tab create --url "$TARGET_URL" --session "$SESSION_ID" --json)"
printf '%s\n' "$TAB_JSON" | python3 -m json.tool

TAB_ID="$(printf '%s' "$TAB_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["tab_id"])')"

# Give ChatGPT a moment to load.
sleep 4

banner "9. READ CHATGPT ACCOUNT IDENTITY — NEVER READ OR SAVE TOKENS"

ACCOUNT_JSON="$(bsk evaluate '(async()=>{try{const r=await fetch("/api/auth/session",{credentials:"include"});const s=await r.json();return {authenticated:!!s?.user,name:s?.user?.name??null,email:s?.user?.email??null,expires:s?.expires??null,url:location.href,title:document.title};}catch(e){return {authenticated:false,error:String(e),url:location.href,title:document.title};}})()' --session "$SESSION_ID" --tab-id "$TAB_ID" --json)"

printf '%s\n' "$ACCOUNT_JSON" | python3 -m json.tool

# Save only non-secret routing + identity info. Browser login state remains inside Chrome itself.
python3 - "$STATE" "$SESSION_STATE" "$INSTANCE" "$SESSION_ID" "$TAB_ID" "$TARGET_URL" "$BROWSERS_JSON" "$ACCOUNT_JSON" <<'PY'
import json,sys,datetime
state_path,session_path,instance,session_id,tab_id,target,browsers_raw,account_raw=sys.argv[1:]
browsers=json.loads(browsers_raw)
account_wrap=json.loads(account_raw)
account=account_wrap.get("value") if isinstance(account_wrap,dict) else None
selected=next((x for x in browsers if str(x.get("instance_id",""))==instance),{})
state={
  "browser_instance_id": instance,
  "browser_label": selected.get("label") or None,
  "browser_name": selected.get("browser_name") or None,
  "browser_version": selected.get("browser_version") or None,
  "target_url": target,
  "chatgpt_account": account if isinstance(account,dict) else None,
  "saved_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
  "auth_storage": "existing Chrome profile managed by BrowserSkill extension",
  "never_save": ["cookies","access_token","refresh_token","passwords"],
}
session={
  "browser_instance_id": instance,
  "session_id": session_id,
  "tab_id": int(tab_id),
  "target_url": target,
  "saved_at": state["saved_at"],
}
for path,obj in ((state_path,state),(session_path,session)):
    with open(path,"w",encoding="utf-8") as f:
        json.dump(obj,f,ensure_ascii=False,indent=2)
print("[PASS] Persistent browser binding saved:", state_path)
print("[PASS] Current browser session saved:", session_path)
PY

chmod 600 "$STATE" "$SESSION_STATE" "$TABS_STATE" 2>/dev/null || true

AUTHED="$(printf '%s' "$ACCOUNT_JSON" | python3 -c 'import json,sys; j=json.load(sys.stdin); v=j.get("value") or {}; print("yes" if v.get("authenticated") else "no")')"

banner "RESULT"
echo "Chrome instance pinned: $INSTANCE"
echo "BrowserSkill session:    $SESSION_ID"
echo "New tab:                 $TAB_ID"
echo "Target:                  $TARGET_URL"
echo "ChatGPT authenticated:   $AUTHED"
echo "Persistent mapping:      $STATE"
echo
echo "IMPORTANT:"
echo "- Hermes must use browser-skill + this saved BrowserSkill instance from now on."
echo "- Do not use chrome-real --autoConnect for this ChatGPT workflow."
echo "- The actual ChatGPT login stays in your existing Chrome profile."
echo "- We intentionally never copy/export auth tokens."
echo "- If 'Confirm before borrowing tabs' was switched OFF once in the extension popup,"
echo "  BrowserSkill persists that preference for this Chrome profile."
echo
echo "The BrowserSkill session is intentionally left open so you can see/use the new tab."
