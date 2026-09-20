# Worktree lifecycle

## Resolve the starting state

Inspect before creating anything:

```text
git -C SOURCE rev-parse --show-toplevel
git -C SOURCE status --short
git -C SOURCE rev-parse HEAD
git -C SOURCE branch --show-current
git -C SOURCE worktree list --porcelain
```

Resolve SOURCE from the user's project, not from the skill's installed directory.
Read relevant source-root instructions before creation and the selected checkout's
instructions before editing. If this is not a Git repository, report that a Git
worktree cannot be created; do not initialize a repository as an implicit step.

For a new task branch, resolve an explicit start ref to a commit and record it;
otherwise use the current source HEAD and say so. For an existing task branch or
worktree, follow the reuse checks below rather than applying the source HEAD as
a new default. Do not guess `main`, `master`, a remote's freshness or a default
feature branch. Fetch only if obtaining remote state is within the requested
task; record the resulting commit instead of trusting a moving ref throughout
the run.

A new worktree contains committed state only. If the requested change depends on
source WIP, preserve it and clarify how that state should be carried over before
creating a misleading clean checkout. Do not auto-commit, stash or copy all dirty
files. Unrelated WIP can stay in the original checkout while work starts from the
recorded commit. A request to use the current working state needs an explicitly
scoped transfer, including relevant untracked files, with both copies preserved.

## Create or resume

Use the user's exact branch and directory when supplied. Otherwise follow project
branch conventions and pick a descriptive branch; without one, use the runtime's configured branch prefix, or `feature/<topic>` if none is configured. Directory placement follows project
policy or defaults to a sibling of SOURCE with a filesystem-safe task name.

Check both branch and path collisions. Reuse only when the user's request or this
session establishes that the existing worktree belongs to this task. In that
case retain its current HEAD and WIP, record the baseline, and apply the starting
state checks below before resuming.
An existing branch alone does not prove task ownership. For a collision with an
explicit user choice, explain it rather than inventing a different choice; for
an unclaimed generated name, choose a fresh suffix.

Before opening an existing task branch or resuming its worktree, compare any
explicit request to start from a commit with the branch's current tip. If they
differ, report both commits and resolve whether the user wants to resume existing
progress or start again from the requested commit before creation or implementation.
Do not silently ignore the requested ref, reset/rebase the branch, or transfer WIP.
An ordinary resume preserves current progress: a recorded original starting commit
is historical context, not an instruction to rewind. Record that original commit
when known and the current resume baseline separately; do not invent missing history.

For a new branch:

```text
git -C SOURCE worktree add -b TASK_BRANCH WORKTREE START_COMMIT
```

For an existing, confirmed task branch not checked out elsewhere, omit `-b` and
use that branch as the final argument only after the starting-state checks above.
Never use force flags to bypass ownership or checkout checks. Quote real arguments or use argument arrays; placeholders in
these examples are not shell variables to paste verbatim.

Confirm from the worktree itself:

```text
git -C WORKTREE rev-parse --show-toplevel
git -C WORKTREE branch --show-current
git -C WORKTREE rev-parse HEAD
git -C WORKTREE status --short
```

Use Git's resolved paths and worktree inventory, not only `test -f .git`:
subdirectories and other Git layouts invalidate that shortcut. A wrong path or
branch must be resolved before edits. Confirm HEAD equals the resolved start
commit for a new branch or the agreed current tip for a reuse/resume. Do not
switch the original checkout's branch.

## Dependencies and runtime state

Give the worktree its own dependency installation. Do not symlink another
checkout's `node_modules` or virtual environment; package links and install hooks
can resolve into or modify that other checkout. Package-manager download stores
may be shared according to the project's supported setup.

Inspect lifecycle scripts before installation. Preserve lockfiles unless the
task requires dependency changes. Worktree creation does not copy ignored env
files: use the project's documented setup and scoped test credentials, without
printing secrets or blindly copying the original checkout's environment.

Identify services and ports before starting them. Do not kill arbitrary listeners
to free a port; use a project-supported alternate port or report the conflict.
Stop only processes this run owns. A shared local database can still change data
used by other worktrees: use project-supported isolated fixtures and cleanup.

## Handoff and later integration

Leave the worktree, branch and uncommitted result intact. Record the branch and
HEAD again at handoff. If concurrent changes alter the baseline or overlap your
files, reassess the diff and rerun checks affected by those changes.

No automatic merge or worktree removal follows a successful test run. Uncommitted
changes are not included in a branch merge; do not present a merge command as if
it transfers WIP. A later user request to integrate must first resolve how the
changes are recorded and recheck the destination state and authorization.
