# Optional developer handoff

Use this contract only when delegation is requested by the user or applicable
project workflow and supported by the runtime. Otherwise the current agent
executes `dev` directly. This reference is shared workflow guidance, not a native
agent definition or an installed adapter.

## Coordinator responsibilities

Resolve the ticket, native dependencies and authoritative spec using the ticket
readiness reference. Establish the assigned worktree, branch and starting state
using the worktree lifecycle reference. Resolve missing requirements and unsafe
prerequisites before dependent implementation.

Give the developer a self-contained brief containing:

- Ticket URL, repository identity and title; authoritative spec URL when separate.
- Allocated criteria/test names and the spec's confirmed seams, or readable
  sources for those decisions. Include relevant comments and dependency evidence.
- Absolute assigned worktree path, task branch, starting commit, current HEAD,
  and the existing WIP/staging baseline. For a resume, distinguish the original
  starting commit (when known) from the agreed current baseline. Resolve explicit
  starting-state conflicts before delegation. Identify existing work to preserve.
- Bounded implementation scope, applicable project instructions, validation
  requirements and prerequisites, plus known deferred integration checks. Include
  any approved intermediate-state exception, its source, covered failures and
  responsible integration ticket as required by the verification reference.
- The absolute installed `dev/SKILL.md` path and any supplied findings paths.
  Tell it to read the skill and relevant references, execute implementation and
  verification in the assigned checkout, and skip coordinator-owned setup.
- The actual resource and action permissions for this run. Do not forward
  credentials or imply a broader grant than the user's request.

Do not copy the implementation workflow into a second agent prompt maintained
elsewhere. A provider-specific developer definition, if a project has one, should
route to this shared skill and carry only native configuration and this role's
input/output contract. Use the session model unless a different choice is
explicitly requested or required by applicable instructions.

## Developer responsibilities

Read the assigned project's rules and confirm the actual root, branch and HEAD
before edits. If they differ from the brief, or the expected WIP changed, report
the discrepancy before dependent writes. Work only in the assigned checkout;
do not inspect other task worktrees for missing context.

Apply `dev`'s implementation, testing, failure handling and verification rules.
Do not create/switch branches, create/remove worktrees, stash or reset work.
Branch lifecycle and integration remain with the coordinator. Do not stage,
commit, publish, operate CI or deploy as part of this executor role; separately
authorized lifecycle actions are handled by the coordinator.

Do not invoke independent review, aggregate other reviewers' verdicts or spawn
additional agents merely because delegation tools are available. Research or
advisor delegation needs the same applicable authorization as any delegation.
Neither the role name nor its declared tools prove a filesystem sandbox; inspect
the effective environment before claiming enforcement.

## Findings and escalation

For implementation follow-up, the coordinator passes report paths or inline
findings, the reviewed source state, the affected ticket scope and the caller's
blocker definitions. The developer reads all supplied findings, verifies them
against current source, fixes supported in-scope blockers and maps each to its
disposition and checks. Medium blockers remain blockers when the caller defines
them that way. Stale, unsupported or decision-dependent findings need an explicit
explanation; they are not silently omitted.

If stuck after distinct attempts or facing an unresolved design decision, provide:

```text
Problem: the concrete failure or decision, with a relevant location
What I tried: distinct attempts and observed results
Hypothesis: the current explanation, or none
Specific question: the missing answer needed to proceed
```

Send this to the coordinator, or an advisor explicitly assigned for this task.
Advice does not override the spec or observed behavior. The developer still owns
its implementation and verification. Without an advisor, report the blocker;
do not launch an unrequested model pipeline. Product decisions return to the user.

## Return and coordinator verification

Return `dev`'s normal handoff: status, ticket identity, worktree/branch/revisions,
actual changed files and staging state, checks and coverage, unresolved criteria
and risks. Add findings dispositions when this was a repair pass. Prefer a short
summary with a detailed report path when needed and permitted; raw artifacts stay
outside the source tree. If the executor cannot write a report, return it inline.

The coordinator checks the returned checkout identity, actual diff and supporting
evidence before presenting completion. It may read full findings, logs and source
when needed; summary-only routing must not prevent evidence verification. Reuse
valid checks rather than rerunning them merely because another agent ran them.
If the final state changed, rerun affected checks or report stale coverage.

A developer's `verified` status is scoped implementation evidence, not an
independent review. The user starts review in a separate step. Do not add a
mandatory reviewer chain or automatically open a PR after the executor returns.
