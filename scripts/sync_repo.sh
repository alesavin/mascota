#!/usr/bin/env bash
set -euo pipefail

# Sync lambda/ and skill-package/interactionModels from one local repo directory to another.
# Keeps all non-synced files on target.
# Usage:
#   scripts/sync_repo.sh <from-repo-dir> <to-repo-dir> [source-branch] [target-branch] [from-dir] [to-dir]
# Example:
#   scripts/sync_repo.sh ~/src/repo-a ~/src/repo-b main master
#   scripts/sync_repo.sh ~/src/repo-a ~/src/repo-b main master services/source services/target

if [[ ${1:-} == "-h" || ${1:-} == "--help" || $# -lt 2 || $# -gt 6 ]]; then
  cat <<'USAGE'
Sync lambda/ and skill-package/interactionModels directories from source repo to destination repo.

Usage:
  scripts/sync_repo.sh <from-repo-dir> <to-repo-dir> [source-branch] [target-branch] [from-dir] [to-dir]

Arguments:
  from-repo-dir Source repository directory path
  to-repo-dir   Destination repository directory path
  source-branch Optional source branch/ref to sync (defaults to current branch in source repo)
  target-branch Optional destination branch to sync into (defaults to source-branch)
  from-dir      Optional source repo subdirectory prefix (defaults to repository root)
  to-dir        Optional destination repo subdirectory prefix (defaults to from-dir)

Behavior:
  - Copies lambda/ and skill-package/interactionModels from <from-dir> in <source-branch>.
  - Writes them into <to-dir> on destination branch.
  - Preserves all other files in destination branch.
  - Creates a commit in destination repo only when synced paths changed.
USAGE
  exit 1
fi

FROM_REPO_DIR="$1"
TO_REPO_DIR="$2"

if ! FROM_REPO_DIR="$(cd "$FROM_REPO_DIR" && pwd)"; then
  echo "Error: source repo directory '$1' does not exist." >&2
  exit 2
fi

if ! TO_REPO_DIR="$(cd "$TO_REPO_DIR" && pwd)"; then
  echo "Error: destination repo directory '$2' does not exist." >&2
  exit 2
fi

SOURCE_BRANCH="${3:-$(git -C "$FROM_REPO_DIR" rev-parse --abbrev-ref HEAD)}"
TARGET_BRANCH="${4:-$SOURCE_BRANCH}"
FROM_DIR_RAW="${5:-}"
TO_DIR_RAW="${6:-${5:-}}"

trim_slashes() {
  local value="${1:-}"
  value="${value#/}"
  value="${value%/}"
  printf '%s' "$value"
}

FROM_DIR="$(trim_slashes "$FROM_DIR_RAW")"
TO_DIR="$(trim_slashes "$TO_DIR_RAW")"

source_path() {
  local part="$1"
  if [[ -n "$FROM_DIR" ]]; then
    printf '%s/%s' "$FROM_DIR" "$part"
  else
    printf '%s' "$part"
  fi
}

target_path() {
  local part="$1"
  if [[ -n "$TO_DIR" ]]; then
    printf '%s/%s' "$TO_DIR" "$part"
  else
    printf '%s' "$part"
  fi
}

SOURCE_LAMBDA_PATH="$(source_path lambda)"
SOURCE_SKILL_PACKAGE_PATH="$(source_path skill-package/interactionModels)"
TARGET_LAMBDA_PATH="$(target_path lambda)"
TARGET_SKILL_PACKAGE_PATH="$(target_path skill-package/interactionModels)"

# Validate both directories are git repos.
git -C "$FROM_REPO_DIR" rev-parse --is-inside-work-tree >/dev/null
git -C "$TO_REPO_DIR" rev-parse --is-inside-work-tree >/dev/null

# Ensure source and destination working trees are clean before sync.
if [[ -n "$(git -C "$FROM_REPO_DIR" status --porcelain)" ]]; then
  echo "Error: source working tree is not clean. Commit or stash changes before syncing." >&2
  exit 3
fi

if [[ -n "$(git -C "$TO_REPO_DIR" status --porcelain)" ]]; then
  echo "Error: destination working tree is not clean. Commit or stash changes before syncing." >&2
  exit 3
fi

if ! git -C "$FROM_REPO_DIR" rev-parse --verify --quiet "${SOURCE_BRANCH}^{commit}" >/dev/null; then
  echo "Error: source branch/ref '${SOURCE_BRANCH}' not found in source repository." >&2
  exit 4
fi

if [[ -z "$(git -C "$FROM_REPO_DIR" ls-tree -d --name-only "$SOURCE_BRANCH" "$SOURCE_LAMBDA_PATH")" ]]; then
  echo "Error: source branch '${SOURCE_BRANCH}' has no ${SOURCE_LAMBDA_PATH}/ directory." >&2
  exit 5
fi

if [[ -z "$(git -C "$FROM_REPO_DIR" ls-tree -d --name-only "$SOURCE_BRANCH" "$SOURCE_SKILL_PACKAGE_PATH")" ]]; then
  echo "Error: source branch '${SOURCE_BRANCH}' has no ${SOURCE_SKILL_PACKAGE_PATH}/ directory." >&2
  exit 6
fi

# Checkout destination branch (create from origin/<branch> when available, else create new).
if git -C "$TO_REPO_DIR" show-ref --verify --quiet "refs/heads/$TARGET_BRANCH"; then
  git -C "$TO_REPO_DIR" checkout -q "$TARGET_BRANCH"
elif git -C "$TO_REPO_DIR" show-ref --verify --quiet "refs/remotes/origin/$TARGET_BRANCH"; then
  git -C "$TO_REPO_DIR" checkout -q -b "$TARGET_BRANCH" "origin/$TARGET_BRANCH"
else
  git -C "$TO_REPO_DIR" checkout -q -b "$TARGET_BRANCH"
fi

# Remove synced target dirs and rehydrate from source archive.
rm -rf "$TO_REPO_DIR/$TARGET_LAMBDA_PATH" "$TO_REPO_DIR/$TARGET_SKILL_PACKAGE_PATH"
mkdir -p "$TO_REPO_DIR/$(dirname "$TARGET_LAMBDA_PATH")" "$TO_REPO_DIR/$(dirname "$TARGET_SKILL_PACKAGE_PATH")"
git -C "$FROM_REPO_DIR" archive "$SOURCE_BRANCH" "$SOURCE_LAMBDA_PATH" | tar -x -C "$TO_REPO_DIR"
git -C "$FROM_REPO_DIR" archive "$SOURCE_BRANCH" "$SOURCE_SKILL_PACKAGE_PATH" | tar -x -C "$TO_REPO_DIR"

if [[ "$SOURCE_LAMBDA_PATH" != "$TARGET_LAMBDA_PATH" ]]; then
  mkdir -p "$TO_REPO_DIR/$(dirname "$TARGET_LAMBDA_PATH")"
  mv "$TO_REPO_DIR/$SOURCE_LAMBDA_PATH" "$TO_REPO_DIR/$TARGET_LAMBDA_PATH"
fi

if [[ "$SOURCE_SKILL_PACKAGE_PATH" != "$TARGET_SKILL_PACKAGE_PATH" ]]; then
  mkdir -p "$TO_REPO_DIR/$(dirname "$TARGET_SKILL_PACKAGE_PATH")"
  mv "$TO_REPO_DIR/$SOURCE_SKILL_PACKAGE_PATH" "$TO_REPO_DIR/$TARGET_SKILL_PACKAGE_PATH"
fi

# Commit only if synced paths changed.
if [[ -z "$(git -C "$TO_REPO_DIR" status --porcelain -- "$TARGET_LAMBDA_PATH" "$TARGET_SKILL_PACKAGE_PATH")" ]]; then
  echo "No synchronized directory changes to sync. Destination unchanged."
  exit 0
fi

git -C "$TO_REPO_DIR" add "$TARGET_LAMBDA_PATH" "$TARGET_SKILL_PACKAGE_PATH"
git -C "$TO_REPO_DIR" commit -q -m "chore(sync): update lambda and skill-package interaction models from ${SOURCE_BRANCH}"

echo "Sync completed: ${SOURCE_LAMBDA_PATH}/, ${SOURCE_SKILL_PACKAGE_PATH}/ from ${FROM_REPO_DIR}:${SOURCE_BRANCH} -> ${TO_REPO_DIR}:${TARGET_BRANCH} (${TARGET_LAMBDA_PATH}/, ${TARGET_SKILL_PACKAGE_PATH}/)"
