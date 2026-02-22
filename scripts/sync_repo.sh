#!/usr/bin/env bash
set -euo pipefail

# Sync ONLY lambda/ from one git remote to another without hardcoding URLs.
# Keeps all non-lambda files on target (e.g. skill-package/, ask-resources.json).
# Usage:
#   scripts/sync_repo.sh <from-remote> <to-remote> [branch]
# Example:
#   scripts/sync_repo.sh origin codecommit main

if [[ ${1:-} == "-h" || ${1:-} == "--help" || $# -lt 2 || $# -gt 3 ]]; then
  cat <<'USAGE'
Sync only the lambda/ directory from source remote to destination remote.

Usage:
  scripts/sync_repo.sh <from-remote> <to-remote> [branch]

Arguments:
  from-remote  Source remote name already configured in local git
  to-remote    Destination remote name already configured in local git
  branch       Optional branch name to sync (defaults to current branch)

Behavior:
  - Copies only lambda/ from <from-remote>/<branch>.
  - Preserves all other files in destination branch (skill-package/, ask-resources.json, etc.).
  - Creates a commit on destination branch only when lambda/ changed.

Notes:
  - Remote URLs are never embedded; only remote names are used.
USAGE
  exit 1
fi

FROM_REMOTE="$1"
TO_REMOTE="$2"
BRANCH="${3:-$(git rev-parse --abbrev-ref HEAD)}"

# Validate remotes exist.
git remote get-url "$FROM_REMOTE" >/dev/null
git remote get-url "$TO_REMOTE" >/dev/null

# Ensure working tree is clean before sync.
if [[ -n "$(git status --porcelain)" ]]; then
  echo "Error: working tree is not clean. Commit or stash changes before syncing." >&2
  exit 2
fi

# Ensure source and destination branch refs are available locally.
git fetch "$FROM_REMOTE" "$BRANCH"
git fetch "$TO_REMOTE" "$BRANCH"

if ! git ls-tree -d --name-only "${FROM_REMOTE}/${BRANCH}" lambda >/dev/null 2>&1; then
  echo "Error: source branch '${FROM_REMOTE}/${BRANCH}' not found." >&2
  exit 3
fi

if [[ -z "$(git ls-tree -d --name-only "${FROM_REMOTE}/${BRANCH}" lambda)" ]]; then
  echo "Error: source branch '${FROM_REMOTE}/${BRANCH}' has no lambda/ directory." >&2
  exit 4
fi

TMP_DIR="$(mktemp -d)"
cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

# Create temporary repo based on destination branch.
git -C "$TMP_DIR" init -q
git -C "$TMP_DIR" remote add dest "$(git remote get-url "$TO_REMOTE")"
git -C "$TMP_DIR" fetch -q dest "$BRANCH"
git -C "$TMP_DIR" checkout -q -b "$BRANCH" "dest/$BRANCH"

# Replace only lambda/ with source lambda/ content.
rm -rf "$TMP_DIR/lambda"
mkdir -p "$TMP_DIR/lambda"
git archive "${FROM_REMOTE}/${BRANCH}" lambda | tar -x -C "$TMP_DIR"

# Commit only if lambda changed.
if [[ -z "$(git -C "$TMP_DIR" status --porcelain -- lambda)" ]]; then
  echo "No lambda/ changes to sync. Destination unchanged."
  exit 0
fi

git -C "$TMP_DIR" add lambda
git -C "$TMP_DIR" commit -q -m "chore(sync): update lambda from ${FROM_REMOTE}/${BRANCH}"
git -C "$TMP_DIR" push -q dest "$BRANCH"

echo "Sync completed: lambda/ from ${FROM_REMOTE}/${BRANCH} -> ${TO_REMOTE}/${BRANCH}"
