#!/usr/bin/env bash
# Symlink every personal skill in this repo into each AI tool's skills folder,
# and remove this clone's own links for skills that no longer exist.
# Idempotent: safe to run repeatedly. Never deletes anything it did not create.
set -uo pipefail

LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)/lib/links.sh"
[ -r "$LIB" ] || { echo "ERROR: missing helper library: $LIB" >&2; exit 1; }
. "$LIB"

linked=0
skipped=0
pruned=0

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
force=0
if [ "${1:-}" = "--force" ]; then
  force=1
  shift
fi
if [ "$#" -ne 0 ]; then
  echo "Usage: $0 [--list|--force]" >&2
  exit 1
fi

# CENTRAL is derived from this script's own location, so running relink from a
# linked git worktree points every tool at that branch's copy of the skills.
# Nothing looks wrong afterwards: the links are valid and the tools silently run
# the branch instead of the main checkout. Refuse unless that is the intent.
linked_worktree_common_dir() {
  command -v git >/dev/null 2>&1 || return 1
  local gitdir common
  gitdir="$(git -C "$CENTRAL" rev-parse --absolute-git-dir 2>/dev/null)" || return 1
  common="$(git -C "$CENTRAL" rev-parse --git-common-dir 2>/dev/null)" || return 1
  case "$common" in
    /*) ;;
    *) common="$CENTRAL/$common" ;;
  esac
  gitdir="$(cd "$gitdir" 2>/dev/null && pwd -P)" || return 1
  common="$(cd "$common" 2>/dev/null && pwd -P)" || return 1
  [ "$gitdir" != "$common" ] || return 1
  printf '%s\n' "$common"
}

if common_dir="$(linked_worktree_common_dir)"; then
  branch="$(git -C "$CENTRAL" rev-parse --abbrev-ref HEAD 2>/dev/null)" || branch=""
  main_worktree="$common_dir"
  [ "$(basename "$common_dir")" = ".git" ] && main_worktree="$(dirname "$common_dir")"
  if [ "$force" -eq 1 ]; then
    echo "  WARN  linking from a linked git worktree (--force): $CENTRAL${branch:+ on $branch}"
    echo "        every tool will run this worktree's skills, not $main_worktree"
  else
    {
      echo "ERROR relink.sh is running from a linked git worktree, not the main checkout."
      echo "      worktree: $CENTRAL${branch:+ (branch $branch)}"
      echo "      main:     $main_worktree"
      echo
      echo "Linking from here would point all three tools at this branch's skills."
      echo "They would keep working while quietly running this branch instead of the"
      echo "main checkout, including versions of a skill that were superseded there."
      echo
      echo "Run ./scripts/relink.sh from $main_worktree instead, or pass --force if"
      echo "you really want every tool to run this worktree."
    } >&2
    exit 1
  fi
fi

# Prune first: a skill that was renamed or removed upstream leaves a link under
# its old name, and the linking loop below never visits it — that loop walks the
# skills that exist now. Only links this clone owns and is not about to relink
# are removed, so a real directory, another source's link, and the Cloudflare
# pack are all untouched.
shopt -s dotglob
for dir in "${TOOL_DIRS[@]}"; do
  [ -d "$dir" ] || continue
  for link in "$dir"/*; do
    [ -L "$link" ] || continue
    name="$(basename "$link")"

    still_a_skill=0
    for existing in "${skill_names[@]-}"; do
      if [ "$existing" = "$name" ]; then still_a_skill=1; break; fi
    done
    [ "$still_a_skill" -eq 0 ] || continue

    owned "$link" || continue

    if rm -f "$link"; then
      echo "  prune $link"
      pruned=$((pruned + 1))
    else
      echo "  FAIL  $link -> could not remove orphaned link"
      skipped=$((skipped + 1))
    fi
  done
done
shopt -u dotglob

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
echo "linked: $linked   pruned: $pruned   skipped: $skipped"
[ "$skipped" -eq 0 ]
