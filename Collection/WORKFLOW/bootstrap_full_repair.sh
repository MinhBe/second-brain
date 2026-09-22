#!/usr/bin/env bash
set -Eeuo pipefail

# Safe bootstrap for the full Hermes repair/test workflow.
# Handles a dirty/diverged local second-brain checkout without losing work:
#   - stashes tracked + untracked changes
#   - creates a backup branch at the previous HEAD
#   - resets local main to origin/main
#   - runs provider + fallback + authenticated ChatGPT browser repair/test
#
# Stashed local edits are intentionally NOT auto-applied after the run because
# reapplying an old workflow edit can reintroduce the bug that was just fixed.

TARGET_URL="${1:-}"
if [[ ! "$TARGET_URL" =~ ^https://chatgpt\.com/c/[A-Za-z0-9-]+/?$ ]]; then
  echo "Usage: $0 'https://chatgpt.com/c/<conversation-id>'" >&2
  exit 2
fi
TARGET_URL="${TARGET_URL%/}"

REPO="${SECOND_BRAIN_REPO:-$HOME/second-brain}"
STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_BRANCH="backup-before-hermes-$STAMP"
STASH_MESSAGE="hermes-auto-stash-$STAMP"

echo "================================================================"
echo "SECOND-BRAIN SAFE SYNC + HERMES FULL REPAIR"
echo "================================================================"

if [[ ! -d "$REPO/.git" ]]; then
  git clone https://github.com/MinhBe/second-brain.git "$REPO"
else
  cd "$REPO"

  OLD_HEAD="$(git rev-parse HEAD)"
  git branch "$BACKUP_BRANCH" "$OLD_HEAD"
  echo "[PASS] Previous HEAD preserved: $BACKUP_BRANCH -> $OLD_HEAD"

  if [[ -n "$(git status --porcelain)" ]]; then
    git stash push -u -m "$STASH_MESSAGE"
    echo "[PASS] Local tracked/untracked changes stashed: $STASH_MESSAGE"
  else
    echo "[PASS] Working tree already clean"
  fi

  git fetch origin main
  git checkout -B main origin/main
  echo "[PASS] Local main synchronized exactly to origin/main"
fi

cd "$REPO"

FLOW="$REPO/Collection/WORKFLOW/repair_test_provider_and_browser.sh"
[[ -f "$FLOW" ]] || {
  echo "[FAIL] Missing workflow: $FLOW" >&2
  exit 1
}

chmod +x "$FLOW"

echo
echo "================================================================"
echo "RUN PROVIDER + FALLBACK + CHATGPT BROWSER REPAIR/TEST"
echo "================================================================"

bash "$FLOW" "$TARGET_URL"

echo
echo "================================================================"
echo "BOOTSTRAP COMPLETE"
echo "================================================================"
echo "Repository: $REPO"
if git show-ref --verify --quiet "refs/heads/$BACKUP_BRANCH"; then
  echo "Backup branch: $BACKUP_BRANCH"
fi
if git stash list | grep -Fq "$STASH_MESSAGE"; then
  echo "Preserved stash: $STASH_MESSAGE"
  echo "Note: it was NOT auto-applied."
fi
