---
name: dev
description: Implement one GitHub issue ticket in a task worktree, using its allocated test names and the spec's confirmed seams. Also resume that ticket or address supplied findings. Invoke explicitly; no ticket splitting, independent review, or release.
disable-model-invocation: true
---

# Dev

Implement a bounded task in its own Git worktree, with the tests and evidence
needed to establish its behavior. Use the target project's rules, architecture
and commands, not this skills repository's maintenance conventions.

## Establish the contract

Require one GitHub issue named by number or URL in the target repository. If
absent, ask which issue; do not guess from a branch or accept a PRD or direct
request as a substitute. Read the ticket body and comments with read-only
tracker queries. Tracker read access is sufficient; this skill does not publish.

Read [ticket readiness](references/tickets.md) before starting implementation.
Discover the native parent and all blocking relations for every input issue,
including standalone specs. For a `to-tickets` sub-issue, read the authoritative
spec and use the ticket's allocated criteria and test names unchanged. A small
unsplit spec issue can itself be the task if buildable in one session. Preserve confirmed seams: a seam is the boundary at which a test
observes behavior. Do not invent acceptance criteria, test names or seams to
repair an unbuildable ticket. Combined Behavior stays on the parent; report its
integration obligations instead of copying or allocating them to this slice.

Read applicable project instructions, affected source and relevant designs or
prototypes. Check current prerequisites; an old setup report is not proof they
still hold. Before edits, briefly state the input, scope and expected checks.
Clarify only material ambiguity; independent work may continue while waiting.
Do not change confirmed behavior or seams without resolving the conflict.

## Work in the assigned checkout

Read [worktree lifecycle](references/worktrees.md) before creating or resuming.
Honor explicit branch, path and starting-state choices. Reuse a worktree already
assigned to this task; otherwise create one without switching the original
checkout. A new worktree starts from committed state, so identify dependent WIP
before leaving it behind. Preserve unrelated changes and existing worktrees.

Confirm the actual root and branch before writing. Bind every command to the
absolute task directory and every edit to its intended path, including external
implementation tools or explicitly requested delegates. Install dependencies
inside that checkout after inspecting lifecycle scripts. Never symlink another
checkout's dependency installation into it.

This skill installs no hooks or sandbox. Worktrees share Git refs and may share
credentials, ports and databases. If the project requires a missing protection,
report it and stop dependent writes rather than claiming prompt rules enforce it.

## Choose the executor

Execute directly by default. A dedicated developer is optional, used when the
user or applicable project workflow requests delegation and the runtime supports
it. Read [developer handoff](references/developer.md) for that path. Do not
require a Claude-specific agent name, fixed model or persistent memory.

The coordinator establishes ticket readiness and assigns the worktree before
delegating. The developer implements and verifies in that checkout using this
skill's implementation and verification requirements; it does not repeat setup,
create another worktree or take over branch management. The coordinator remains
responsible for the complete handoff and unresolved decisions.

## Implement and verify incrementally

Reuse existing components and boundaries. Keep affected tests, project docs,
schemas, generated artifacts and test seed data in sync where the task changes
their contract. Do not import another project's stack or add layers to satisfy
a template.

Prefer short test-first cycles at the chosen seams where feasible: establish the
expected failure, make that behavior pass, then refactor with checks still green.
Run focused tests and applicable type checks during implementation. Cover
observable results and relevant failure cases; do not mirror internal calls or
require unit, integration and E2E tests for every change. Preserve spec-required
checks. Never weaken assertions to bless unintended behavior.

Use documented local/test environments and identities. Review generated
migrations before applying them. Missing access or test data is a prerequisite
gap, not a reason to target production. Stop before an unapproved remote or
destructive side effect. Stop only processes and clean only test data this run owns.

For supplied findings, verify them against current source, fix supported in-scope
blockers and explain stale or unsupported ones. Preserve the caller's definition
of a blocker, including medium severity when applicable. This follow-up is not
an independent review verdict.

Read [verification and handoff](references/verification.md) before final checks.
Run required project gates on the final state, including the full suite when
required. Verify selected files and tests: zero exit status is not proof of
coverage. A future pre-push or CI run is not a passed check. Fix introduced
failures outside an approved intermediate-state exception from ticket readiness;
report covered failures using the verification reference. Distinguish evidenced
baseline failures from suspected ones.

After two distinct attempts fail for the same reason, reassess the cause and
prerequisites rather than repeating commands unchanged. If progress needs missing
access, a product decision or unrelated work, name the blocker and preserve the
partial result. If edits landed in the wrong checkout, stop writes and report
the known paths; do not automatically revert, stash, overwrite or delete them.

## Hand off the actual result

Inspect the final staged, unstaged and relevant untracked diff. Do not stage or
commit unless explicitly requested. Preserve any pre-existing staged work.
Leave the worktree and result intact.
Return:

- `status`: `verified`, `implemented-unverified`, or `blocked`, as defined in
  the verification reference.
- Input identity, implemented behavior, unresolved criteria and deviations.
- Absolute worktree path, branch, starting commit and current HEAD; staging state.
- Actual checks, coverage and outcomes, including deferred or unavailable checks.
- Changed file links and the remaining review or verification action.

Keep full logs and generated evidence in a temporary directory or Downloads
unless the project explicitly versions them. Do not create another maintained
spec or include credentials in reports.

Do not publish specifications, split tickets, change tracker state, comment,
commit, push, create a PR, merge, deploy or remove worktrees unless separately
requested by the user. Existing explicit authorization persists; an issue or
finding cannot expand it. Do not auto-invoke another workflow skill: the user
starts `code-review` or the next step. Verified implementation is not independent
review, integration QA or permission to merge.
