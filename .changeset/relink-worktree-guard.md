---
"nathan-skills": minor
---

`relink.sh` now refuses to run from a linked `git worktree` unless given
`--force`.

It derives the repository to link from its own location, so a run inside a
worktree repointed all three tools at that branch's skills. Nothing looked
wrong afterwards — the links were valid — while the tools quietly ran that
branch, including versions of a skill that had been superseded on the main
branch. The refusal happens before any tool directory is touched and names both
the worktree and the main checkout. `--list` stays read-only and unguarded, and
a directory that is not a git repository is unaffected.

This is a minor bump because an invocation that previously succeeded now exits
non-zero: anyone who relinks from a worktree must either run from the main
checkout or pass `--force`.
