#!/usr/bin/env bash
# Auto-commit watcher for second-brain repository
# Checks every 30 seconds for uncommitted changes, commits them with a timestamp, and pushes to origin main.
REPO_DIR="/home/ubuntu/Documents/second-brain"
cd "$REPO_DIR" || exit 1
while true; do
  # Update index
  git add -A
  # Check if there is anything to commit
  if ! git diff --cached --quiet; then
    # There are staged changes
    COMMIT_MSG="Auto-commit: $(date '+%Y-%m-%d %H:%M:%S')"
    git commit -m "$COMMIT_MSG"
    git push origin main
  fi
  sleep 30
done
