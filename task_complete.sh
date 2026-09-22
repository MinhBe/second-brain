#!/bin/bash
# Auto-stage, commit, and push changes after a completed task.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
git add -A
# Only commit if there are changes
if ! git diff --cached --quiet; then
  COMMIT_MSG="Task completed: $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
  git commit -m "$COMMIT_MSG"
  git push origin main
fi
