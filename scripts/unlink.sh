#!/usr/bin/env bash
# Remove only tool-directory symlinks whose targets belong to this clone.
set -uo pipefail
LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)/lib/links.sh"
[ -r "$LIB" ] || { echo "ERROR: missing helper library: $LIB" >&2; exit 1; }
. "$LIB"

dry_run=false
case "${1:-}" in
  --dry-run) dry_run=true ;;
  '') ;;
  *) echo "Usage: $0 [--dry-run]" >&2; exit 1 ;;
esac
[ "$#" -le 1 ] || { echo "Usage: $0 [--dry-run]" >&2; exit 1; }

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
