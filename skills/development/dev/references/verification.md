# Verification and handoff

## Establish behavior and gate coverage

Map the task's acceptance criteria to existing or changed checks. Keep the map
small enough to explain what a pass proves. For each required check record:

| Field | Record |
| --- | --- |
| Command and directory | The actual invocation inside the task worktree |
| Scope | Behavior, files, suites or packages selected |
| Prerequisites | Test identities, services, environment and fixtures |
| Owner | This implementation run, a project hook, or CI |
| Outcome | Passed, failed, environment-blocked, not run, or not applicable |

Use the project's real scripts, task graph and configuration. Do not assume an
installed linter covers a rule, a test file belongs to the invoked suite, or a
workspace runner includes root scripts and every package. Check file selection
and meaningful test counts; zero selected tests is not a successful behavior
check. A missing check remains a gap even when the parent command exits zero.

Existing tests can establish a refactor or a narrow configuration change without
new tests. Add regression cases for new or changed behavior where they materially
protect the contract. Avoid snapshots or assertions that merely repeat the new
implementation. Do not invent full test infrastructure for a reversible wording
change. Honor stronger project or spec requirements.

For UI changes, use available browser tooling to exercise the affected interaction
and inspect relevant rendering and errors. Static code inspection and a passing
build do not prove keyboard operation, responsive layout or real authentication.
If the necessary browser, account or service is unavailable, record the specific
unobserved behavior. Prefer project test helpers for accounts, data, messages and
cleanup; do not install test infrastructure or contact real users implicitly.

For schema or state changes, validate the relevant transition and existing-data
behavior against an authorized local/test environment. Generated SQL alone does
not prove a migration applies or preserves data.

## Trust only current evidence

Run required local gates yourself unless current evidence for the final state
already exists or the project assigns them exclusively to another stage. A hook
that would run on push has not run if no push occurred. If a required gate is
owned by a later push or CI, record it as not run; do not push merely to trigger
it or claim the implementation fully verified. Reuse evidence only when its
source state, environment and scope still apply.

Use supported task caching. A cache hit is not inherently invalid, but check
whether the relevant inputs and environment are represented before relying on it.
When that cannot be established, rerun the affected check without cache if safe,
or report the gap. Do not invalidate the whole repository's cache by default.

After the last edit, run affected checks and inspect the final diff, including
staged files and relevant untracked artifacts. Passing results from before a
material edit are stale. Record the exact checked state as HEAD plus the WIP
scope when uncommitted; HEAD alone does not identify a tested working tree.

A baseline failure needs evidence from the baseline or a traceable pre-existing
cause. Do not infer it merely because the failing file was untouched. Preserve
unrelated user work when investigating; no checkout resets to reproduce a baseline.

## Approved intermediate-state failures

For an expand–contract step explicitly permitted to remain non-green by ticket
readiness, identify the approval source, covered failing checks and failure causes,
and the final integrate-and-verify ticket responsible for resolution. A general
migration plan does not excuse unrelated failures. Keep each actual check outcome
as failed, separate covered failures from unexpected ones, and identify which
integration evidence is still deferred. Do not relabel a covered failure as a
baseline failure or expand this ticket to implement later steps merely to go green.

If the assigned step is complete, its own contract checks pass, and the only
remaining failures are covered by that approval, return `implemented-unverified`.
An uncovered introduced failure or an incomplete assigned step remains `blocked`.
If coverage by the exception is unclear, resolve it before claiming the exception.
The developer and coordinator use this same classification and include the approval
and integration obligation in their handoff.

## Completion states

- **verified**: the scoped implementation is complete and all required checks
  for that scope passed on the final state. State what was tested; this is not
  an independent review or whole-product QA verdict.
- **implemented-unverified**: the implementation appears complete, but a required
  check is not run, deferred, blocked, has an evidenced baseline failure, or
  fails only within the approved intermediate-state exception above.
  Name the missing evidence and what would resolve it.
- **blocked**: requirements, implementation or an introduced failure outside
  that approved exception remain unresolved, or safe task checkout/prerequisites
  cannot be established. State what is complete and preserve it for resumption.

Partial checks do not upgrade the whole task to verified. For multiple criteria,
show completed and unresolved portions without dropping any from the denominator.
