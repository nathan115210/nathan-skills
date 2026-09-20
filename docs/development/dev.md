# dev

[SKILL.md](../../skills/development/dev/SKILL.md)

## When to reach for it

Invoke `dev` to implement one GitHub issue, including its allocated behavior
checks. Supply the issue number or URL. You can resume the same ticket's worktree
or ask it to address supplied review findings for that issue.

Examples:

- “Use dev to implement ticket 42 in this repository.”
- “Use dev to implement spec issue 17; it is small enough for one session.”
- “Use dev in ticket 42's existing worktree to address these review blockers.”

For a `to-tickets` child, criteria and test names come from the ticket, seams
from its native parent spec, and dependencies from GitHub's native graph. The
parent's Combined Behavior stays on the parent. An unsplit spec issue can be the
task when it is buildable in one session. A file or direct request is not a
substitute for the issue.

An issue marked not buildable or carrying no concrete test names cannot start.
Open blockers stop dependent work; closed blockers still need their required
implementation available in the chosen starting state. The skill reports gaps
without editing issue relations or merging another task's branch. Dependency
checks apply even when the issue has no parent. Failed or incomplete graph reads
stop implementation. A spec with existing sub-issues requires choosing an
implementation ticket rather than repeating the parent's work.

## What you get

A task worktree containing production changes, the necessary tests and a report
of what was verified. An existing worktree for this task can be resumed. A new
task branch starts from the specified commit or the source checkout's current
HEAD; uncommitted source changes do not come along automatically. Reusing an
existing branch preserves its current tip. If an explicit request to start from
another commit conflicts with existing progress, the skill resolves whether you
want to resume or restart before proceeding. Normal resume does not rewind to
the task's historical starting commit.

The handoff names the absolute path, branch, starting commit, current HEAD,
changed files, staging state and check results. Keep using that worktree to
inspect the result. The original checkout stays on its original branch.

| Status | What it tells you |
| --- | --- |
| `verified` | The implementation and its required checks are complete for the stated scope |
| `implemented-unverified` | The change appears complete, but a required check is unavailable, deferred, affected by an evidenced baseline failure or fails within an approved intermediate-state exception |
| `blocked` | Implementation, requirements, an introduced failure outside that exception or safe prerequisites remain unresolved |

For an approved expand–contract intermediate step, passing its own contract checks
while covered integration checks still fail yields `implemented-unverified`. The
report retains failed outcomes, names the approval and responsible integration
ticket, and separates unexpected regressions, which still block completion.

No status means permission to merge. Changes remain unstaged and uncommitted
unless you explicitly request those actions; existing staged work is preserved.

## Optional developer agent

The current agent can execute the skill directly. If you or the project's workflow
requests delegation, a coordinator can assign implementation to a developer after
checking the issue and establishing its worktree.

The developer receives the issue/spec, allocated tests, seams, exact checkout
identity and validation requirements. It implements and verifies there; the
coordinator owns workspace setup and later integration. It does not create a
second worktree, switch branches or launch its own review pipeline.

Review repairs use report paths or inline findings and the caller's blocker
definitions. A stuck developer returns the problem, attempts, hypothesis and
specific question. The coordinator checks the actual diff and evidence before
reporting completion, and can read full reports when necessary.

This contract reuses the same `dev` requirements across tools. It does not install
a Claude developer definition, prescribe a model or require persistent memory.
See [developer handoff](../../skills/development/dev/references/developer.md).

## What it does not do

It does not conduct a planning interview, publish a spec, split issues, perform
an independent code review or run whole-product QA. It does not automatically
commit, push, publish a PR, merge, deploy or remove its worktree. You start the
next step; a successful implementation does not automatically invoke another skill.

It uses your project's architecture, test framework and package manager. It does
not require a particular web stack or unit, integration and E2E tests for every
change. Existing checks can establish a refactor; new behavior needs meaningful
coverage at the agreed boundary.

A worktree is filesystem organization, not a sandbox. Credentials, Git refs,
ports and databases may still be shared. This skill installs no hooks and does
not pretend a missing project-required protection exists.

## What a bad run looks like

- It edits your original checkout or switches its branch while claiming to use
  a worktree.
- It silently loses source WIP, reuses another task's branch or creates another
  worktree every time you resume.
- It skips dependency checks because the issue has no parent, or implements a
  split spec as though it had no child tickets.
- It silently ignores your requested starting commit when reusing a branch.
- It calls an approved intermediate failure passed, or treats an unrelated
  regression as covered by the migration exception.
- It tests a committed revision while handing you materially different WIP.
- It calls a gate passed because the command returned zero, despite selecting
  zero tests or skipping the changed directory.
- It says pre-push tests passed when nothing was pushed.
- It adds a new testing seam to each layer instead of respecting the spec.
- It says to merge the branch as though that would transfer uncommitted files.
- It turns a review finding into permission to change product scope or publish.
- Its delegated developer creates a second checkout, hides unresolved findings
  or reports success that the coordinator accepts without checking the actual diff.

## It's working if

You can locate the complete diff in the reported worktree, match behavior to the
reported checks, and see every unresolved criterion. Resuming the task preserves
its existing changes. An unavailable service produces a concrete verification gap,
not a success claim or an attempt against production.

## Known limitations

- Standalone-issue blockers, already-split spec rejection, explicit-start conflicts
  on reuse and approved intermediate-failure classification have been statically
  reviewed but not runtime-verified.
- The optional coordinator/developer contract has not been runtime-verified.
  No native agent adapter ships with this skill; effective tools and isolation
  depend on the runtime and project configuration.
- A temporary Python fixture passed worktree creation, regression tests and
  original-checkout WIP preservation through an independent agent run. That
  exercised an earlier draft's direct-request mode, now removed; it does not
  verify the current GitHub-ticket workflow. The follow-up run was blocked by
  a usage limit, so resume behavior and deferred-CI handling remain unverified.
- Native parent/dependency discovery, closed-blocker code availability and
  allocated-test tracing have not been runtime-verified in this skill. The API
  mechanics exercised by `to-tickets` do not establish `dev` executes them correctly.
- The initial skill has not yet been verified through the independent Claude
  Code, Codex CLI and agy runtimes. Shared source and explicit-invocation metadata
  do not prove runtime discovery or identical behavior.
- Git is required. A non-Git folder is reported as a prerequisite gap; `dev`
  does not silently initialize it.
- Copying source WIP into a new checkout needs an explicit, scoped decision.
  It does not automatically stash or commit work to transfer it.
- Browser checks, authenticated flows, migrations and CI depend on the target
  project's tools and test infrastructure. A locally verified function does
  not establish those capabilities.
- Hook enforcement and isolation from remote services are not provided by this
  skill. A project that requires missing protections remains blocked for the
  dependent operations.
