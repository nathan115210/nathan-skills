# Ticket readiness

## Read the issue and its graph

Resolve the target GitHub repository from its remote and the user's project.
For a URL, verify owner/repository as well as issue number. Name the issue and
title. Use `gh issue view NUMBER --repo OWNER/REPO --comments` or an equivalent
read-only connector. If access fails, report it; do not implement from a guessed
issue, stale planning document or missing comments.

For every input issue, discover its native parent relation and read all native
`blocked_by` nodes with their repository identity and state. No parent does not
mean no blockers. If a parent exists, read its body and relevant comments.
Before treating a spec as unsplit, query its native sub-issues. If children exist,
report that it is already split and ask which implementation ticket to use;
do not implement the parent as an unsplit task. REST endpoints include:

```text
GET /repos/OWNER/REPO/issues/NUMBER/parent
GET /repos/OWNER/REPO/issues/NUMBER/dependencies/blocked_by
GET /repos/OWNER/REPO/issues/NUMBER/sub_issues
```

Use supported pagination to exhaust relation lists. An unsupported API, truncated
list or failed query is unresolved graph coverage, not an empty graph; resolve
it before implementation. Only an explicit no-parent response means there is
no parent. Relations are native state;
ticket prose and dependency summary counts are not substitutes. Do not add,
delete or repair relations during implementation. A cross-repository blocker in
a `to-tickets` graph is a discrepancy to report, not permission to edit that repo.

## Preserve the allocation

The ticket's What to build section defines its slice; its Acceptance criteria
and test names section carries the allocated criterion/name pairs. Compare them
to the spec. Keep names as written, using the project's test framework syntax.
Additional implementation checks may protect existing behavior, but do not
invent acceptance test names to make a missing allocation look complete.

A ticket carrying the not-buildable line, no concrete test names, an unresolved
requirement or a conflicting allocation cannot start. Name the gap and leave
implementation untouched. Requirements and spec gaps return to `nathan-grill-me` /
`to-spec`; allocation or slicing gaps return to `to-tickets`, each started by
the user. Do not rewrite the parent or ticket yourself.

Seams and testing decisions are read from the authoritative spec once for the
task. A ticket need not duplicate them. Never add a seam to rescue a slice that
cannot be observed at an agreed boundary. For an unsplit spec issue, use its
own criteria, seams and Combined Behavior checks; if too large for one context,
report the need for splitting rather than silently implementing only part.

For a sub-issue, Combined Behavior remains the parent's integration obligation.
Do not copy the list into the ticket or claim a slice pass verifies the whole.
A final integrate-and-verify ticket can run parent-level checks when explicitly
assigned that role; reference the parent as their authority.

## Verify dependencies are available

An open native blocker prevents dependent implementation. Report it by issue
identity and reason; do not close it or bypass the relation. Closed state alone
does not establish that its code is in the task's starting commit. Inspect linked
implementation evidence and the relevant source/tests to establish the required
contract is available. If not, report the missing integration or starting-state
decision; do not merge another task's branch or inspect its worktree implicitly.

With no blockers, check any other explicit prerequisites the spec requires.
Record the graph observed at start; recheck dependencies before final handoff if
they changed or the run was resumed. Do not silently combine stale issue decisions
with newer code.

`to-tickets` permits expand–contract sequences whose intermediate steps are
explicitly not independently green. Preserve that agreed exception, implement
only the assigned step, and run checks that can establish its contract. Mark
unavailable final green/integration evidence as deferred; keep checks actually
run and failing recorded as failed. Use the approved intermediate-state exception
and completion rules in [verification](verification.md) to classify the result.
A failure not covered by that exception remains an introduced failure to resolve,
not an expected intermediate result.

## Check in-flight pull requests

Work in flight may not appear in the issue graph. After reading the graph and
before creating the worktree, list the repository's open pull requests, drafts
included, read-only:

```text
gh pr list --repo OWNER/REPO --state open --limit 200 --json number,title,isDraft,headRefName,headRefOid,isCrossRepository,changedFiles,files,closingIssuesReferences
```

Skip this task's own PR: one from this repository whose head branch is the
task branch, as on a resume or review-fix run. A result as long as the limit may be truncated; raise
the limit or treat the check as incomplete. `files` is capped (100 per PR in
`gh` 2.80): when it lists fewer paths than `changedFiles`, that PR's overlap is
incomplete, not clean. Local branches without a PR, other worktrees and
uncommitted work are not enumerated.

Classify each remaining PR:

- **Suspected dependency** when (a) an issue in its `closingIssuesReferences`
  is a closed native `blocked_by` blocker of this ticket, or (b) a file or
  symbol the ticket or spec requires is absent from the starting commit and
  the PR's `files` add or modify that file. Only on a (b) match, read that PR's
  diff for the matched file to confirm. Read no other PR diff.
- **File overlap** when its `files` include a file this task is expected to
  touch, shared files such as README or changelogs included.
- Anything else is not reported.

Before creating the worktree, send the result to the user as a visible message,
not only in reasoning, then continue without waiting. Name each overlapping PR
with its overlapping files. A clean check is one line: "N open PRs checked, no
overlap". If the query fails or is incomplete, state "in-flight PR check
incomplete: REASON" there and at handoff, then continue; never report it as "no
open PRs". A failed
native-graph read still stops implementation, as above. So does an open native
blocker, whatever PR closes it; the choices below never override it.

On a suspected dependency, stop before creating the worktree. Name the PR and
the blocker or missing file, and ask one question with three choices:

1. **Wait**: do not start. Report `blocked`, naming the PR.
2. **Stack**: start the task branch from the PR's head commit as an explicit
   start ref under [worktree lifecycle](worktrees.md). Only after this choice,
   fetch the commit if absent from the remote that points at OWNER/REPO
   (`git fetch REMOTE pull/NUMBER/head` also serves a fork PR) and confirm it
   equals `headRefOid`. If it differs, the PR changed since the query: report
   both commits and ask again before creating the worktree. Record the
   confirmed commit as the starting commit. The handoff states that the PR
   must merge first, or the branch be rebased or retargeted afterwards.
3. **Start as normal**: use the usual start commit. The handoff names the PR
   and the missing contract.

Never stack unless the user chooses it, and never merge the PR's branch.

At handoff, first repeat the start-time result as one "At start:" line, since
a runtime may show only the final message. Then re-run the query instead of
reusing the start result, since PRs may open or merge during the session.
Compare the actual diff's file list with each open PR's `files` and report
every overlap by PR number and files. On a resume, the actual diff is the task
branch's whole change since its original starting commit, committed and
uncommitted, not only this session's edits. Apply the same exclusions and
incomplete-check rules. List no PR without overlap; a clean result is the same
one line. Do not comment on, label or otherwise change any PR or issue.
