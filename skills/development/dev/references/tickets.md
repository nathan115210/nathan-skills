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
implementation untouched. Requirements and spec gaps return to `grill-me` /
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
