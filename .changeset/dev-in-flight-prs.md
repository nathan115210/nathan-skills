---
"nathan-skills": minor
---

`dev` now checks the repository's open pull requests, read-only and drafts included, before creating its worktree. It names open PRs that touch the files the task is expected to change and continues; it stops with one question (wait, stack on the PR's head commit, or start as normal) when a PR closes a closed native blocker of the ticket (an open blocker still stops the run as before) or adds a required file missing from the starting commit. The start-time result is shown before the worktree is created and repeated at handoff, which re-queries open PRs and reports only those overlapping the actual diff. A failed or truncated query is reported as an incomplete check and does not stop the run.
