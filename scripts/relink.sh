#!/usr/bin/env bash
# Symlink every personal skill in this repo into each AI tool's skills folder.
# Idempotent: safe to run repeatedly. Never deletes anything it did not create.
set -uo pipefail

# The repository root is the parent of this script directory.
CENTRAL="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"

# One entry per managed tool. agy (Antigravity CLI) reads ~/.gemini/config/,
# not ~/.gemini/ — linking into ~/.gemini/skills leaves the skill invisible.
TOOL_DIRS=(
  "$HOME/.claude/skills"         # Claude Code
  "$HOME/.codex/skills"          # Codex
  "$HOME/.gemini/config/skills"  # agy (Antigravity CLI)
)

linked=0
skipped=0

# Absolute physical path of a symlink's target, or empty if it dangles.
resolve() {
  local link="$1" dest
  dest="$(readlink "$link")" || return 1
  case "$dest" in
    /*) ;;
    *) dest="$(dirname "$link")/$dest" ;;
  esac
  [ -e "$dest" ] || return 1
  (cd "$dest" 2>/dev/null && pwd -P) || return 1
}

# Absolute target path of a symlink without requiring it to exist (for
# dangling links, so we can still tell whether they point into this repo).
raw_target_abs() {
  local link="$1" dest
  dest="$(readlink "$link")" || return 1
  case "$dest" in
    /*) printf '%s\n' "$dest" ;;
    *) printf '%s\n' "$(cd "$(dirname "$link")" 2>/dev/null && pwd -P)/$dest" ;;
  esac
}

# Discover skill roots recursively, without linking category/resource folders.
# Stop at SKILL.md so a skill's bundled resources are never separate skills.
skill_sources=()
skill_names=()
shopt -s nullglob
collect_skills() {
  local folder="$1" child name existing
  if [ -f "$folder/SKILL.md" ]; then
    name="$(basename "$folder")"
    for existing in "${skill_names[@]-}"; do
      if [ "$existing" = "$name" ]; then
        echo "ERROR duplicate skill name: $name" >&2
        return 1
      fi
    done
    skill_sources+=("$folder")
    skill_names+=("$name")
    return 0
  fi
  for child in "$folder"/*/; do
    [ -L "${child%/}" ] && continue
    collect_skills "${child%/}" || return 1
  done
}
[ -d "$CENTRAL/skills" ] || { echo "Missing skills directory" >&2; exit 1; }
# Preflight names before mutating any tool directory.
collect_skills "$CENTRAL/skills" || exit 1
if [ "${1:-}" = "--list" ]; then
  for src in "${skill_sources[@]-}"; do
    [ -n "$src" ] && printf '%s\0' "$src"
  done
  exit 0
fi
if [ "$#" -ne 0 ]; then
  echo "Usage: $0 [--list]" >&2
  exit 1
fi
for src in "${skill_sources[@]-}"; do
  [ -n "$src" ] || continue
  name="$(basename "$src")"

  for dir in "${TOOL_DIRS[@]}"; do
    mkdir -p "$dir"
    target="$dir/$name"

    if [ -L "$target" ]; then
      if current="$(resolve "$target")"; then
        if [ "$current" = "$src" ]; then
          : # already correct, but relink anyway so a moved repo self-heals
        else
          echo "  SKIP  $target -> symlink points outside this repo ($current)"
          skipped=$((skipped + 1))
          continue
        fi
      else
        # Dangling link: fall back to the raw (unresolved) target path,
        # since we can't cd into something that no longer exists. Only
        # links dangling *inside this repo* (e.g. a renamed/removed skill)
        # are ours to clean up; a dangling link into someone else's path
        # is still protected.
        raw="$(raw_target_abs "$target")"
        case "$raw" in
          "$CENTRAL"/*)
            case "$raw" in */../*|*/..|*/./*)
              echo "  SKIP  $target -> ambiguous dangling target ($raw)"
              skipped=$((skipped + 1))
              continue
              ;;
            esac
            ;;
          *)
            echo "  SKIP  $target -> dangling symlink points outside this repo ($raw)"
            skipped=$((skipped + 1))
            continue
            ;;
        esac
      fi
      rm -f "$target"
    elif [ -e "$target" ]; then
      echo "  SKIP  $target -> a real file/directory already exists here"
      skipped=$((skipped + 1))
      continue
    fi

    if ln -s "$src" "$target"; then
      echo "  link  $target"
      linked=$((linked + 1))
    else
      echo "  FAIL  $target -> could not create symlink"
      skipped=$((skipped + 1))
    fi
  done
done

echo
echo "central: $CENTRAL"
echo "linked: $linked   skipped: $skipped"
[ "$skipped" -eq 0 ]
