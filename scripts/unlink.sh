#!/usr/bin/env bash
# Remove only tool-directory symlinks whose targets belong to this clone.
set -uo pipefail
CENTRAL="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
dry_run=false
case "${1:-}" in
  --dry-run) dry_run=true ;;
  '') ;;
  *) echo "Usage: $0 [--dry-run]" >&2; exit 1 ;;
esac
[ "$#" -le 1 ] || { echo "Usage: $0 [--dry-run]" >&2; exit 1; }
TOOL_DIRS=("$HOME/.claude/skills" "$HOME/.codex/skills" "$HOME/.gemini/config/skills")

# Existing directory targets can be resolved physically. For dangling targets,
# require a literal path inside this clone with no traversal or symlink ancestor.
owned() {
  local link="$1" dest resolved part
  dest="$(readlink "$link")" || return 1
  case "$dest" in
    /*) ;;
    *) dest="$(cd "$(dirname "$link")" && pwd -P)/$dest" ;;
  esac
  if resolved="$(cd "$dest" 2>/dev/null && pwd -P)"; then
    case "$resolved" in "$CENTRAL"/*) return 0 ;; *) return 1 ;; esac
  fi
  [ ! -e "$dest" ] || return 1
  case "$dest" in "$CENTRAL"/*) ;; *) return 1 ;; esac
  case "$dest" in */../*|*/..|*/./*|*/.|*//*) return 1 ;; esac
  part="$dest"
  while [ "$part" != "$CENTRAL" ]; do
    [ ! -L "$part" ] || return 1
    part="$(dirname "$part")"
  done
  return 0
}

removed=0
kept=0
failed=0
shopt -s nullglob dotglob
for dir in "${TOOL_DIRS[@]}"; do
  [ -d "$dir" ] || continue
  for link in "$dir"/*; do
    [ -L "$link" ] || continue
    if ! owned "$link"; then
      echo "  KEEP  $link -> outside this clone or ownership uncertain"
      kept=$((kept + 1))
      continue
    fi
    if "$dry_run"; then
      echo "  WOULD REMOVE  $link"
      removed=$((removed + 1))
    elif rm -- "$link"; then
      echo "  REMOVE  $link"
      removed=$((removed + 1))
    else
      echo "  FAIL  $link" >&2
      failed=$((failed + 1))
    fi
  done
done
echo "central: $CENTRAL"
if "$dry_run"; then
  echo "would remove: $removed   kept: $kept   failed: $failed"
else
  echo "removed: $removed   kept: $kept   failed: $failed"
fi
[ "$failed" -eq 0 ]
