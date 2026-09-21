#!/usr/bin/env bash
# Shared link-ownership and tool-directory definitions for relink.sh and unlink.sh.

CENTRAL="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)"

TOOL_DIRS=(
  "$HOME/.claude/skills"         # Claude Code
  "$HOME/.codex/skills"          # Codex
  "$HOME/.gemini/config/skills"  # agy (Antigravity CLI)
)

# Does this symlink belong to this clone? Existing targets are resolved
# physically; a dangling target must be a literal path inside this clone with no
# traversal and no symlinked ancestor.
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
