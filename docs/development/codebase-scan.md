# codebase-scan

[Execution instructions](../../skills/development/codebase-scan/SKILL.md)

## What it does

Reviews an existing codebase as a whole, as a Principal Software Architect and
Security Auditor plus a global accessibility pass. Three axes run separately —
architecture, security, accessibility — each with its **own** coverage rule, and
each declaring what it did not look at. The report opens with a severity-ordered
candidate list, cross-referenced against the open issues, and is saved to
`~/Downloads/code-scan-<project>.md`.

The three coverage rules differ on purpose:

| Axis | Covers | Why that rule |
| --- | --- | --- |
| Security | Authentication, input boundaries, secrets, dependencies — exhaustively, regardless of churn | Risk settles in old, rarely-touched code. Ranking by recent change would miss exactly that. |
| Architecture | Hotspots first, over a window the report names | Structural cost is paid where the code changes most. |
| Accessibility | Every file that renders or styles UI, enumerated | Sampling UI is indistinguishable from not checking it. |

## When to reach for it

Occasionally, by hand, when you want to know the standing state of a codebase —
not as part of building anything. Nothing in the development workflow requires
it and nothing waits on it.

- `Run codebase-scan on this repository.`
- `Use codebase-scan on ~/dev/<project>, security axis especially.`

Reach for `code-review` instead when you have a change to review; it is
diff-scoped and this is not. Reach for `accessibility-review` instead when
accessibility is the whole question and you want its persona path or a focused
UI audit — this skill's accessibility axis reads that skill's static criteria
but runs no personas and produces no second report.

## Prerequisites

Local source, and git history for the architecture axis — a shallow clone gives
it a short window, which the report then names. `gh` authentication for the
issue cross-reference; without it the candidate list is unannotated rather than
guessed. The accessibility axis needs `accessibility-review`'s reference files
to be installed; if they are missing, that axis reports as not assessed rather
than inventing a checklist.

Nothing needs to be installed, built or run. The scan never executes the code.

## Common questions

**Does it fix anything?**
No. It reports. Every finding names a described fix without applying one.

**Will it write into my repository?**
No. The only file it writes is its own report, in `~/Downloads`. That is also
the reason the report carries an identity header: nothing in a scratch directory
says which project it came from.

**Does it create issues?**
No, and it sets no field on the board. It reads the open issues once, to
annotate each candidate as *likely already tracked as #N* or *no matching
issue*. The annotation is a suspicion — matching a finding to an issue title is
fuzzy — and it is phrased as one. Findings reach the tracker the way everything
else does: `grill-me`, then `to-spec`, then `to-tickets`.

**Can I make it use a stronger model?**
Not from the skill. `SKILL.md` has no model field, and naming a provider's model
would fork the workflow across Claude Code, Codex and agy. What the skill does
instead is oblige every axis to declare its coverage and its gaps, so a weak
model fails visibly — the report fills with *not covered* and *unknown* rather
than looking thin and confident. Run it with the most capable model you have;
the report tells you when you didn't.

**It found almost nothing. Did it work?**
Read the not-covered lists. A short findings list with honest, specific gaps is
a real result. A short findings list with an empty not-covered list is the
failure to distrust.

## It's working if

- The report names the project, the revision, and what was excluded.
- Each axis appears separately, with its own not-covered declaration in its own
  terms — surfaces for security, a named commit window for architecture, an
  enumerated file list for accessibility.
- The candidate list is severity-ordered and every entry carries a suspected
  issue number or "no matching issue".
- Nothing inside the scanned repository changed, and the tracker is untouched.
- An axis with nothing to scan (a repository with no UI) says so rather than
  passing silently.

**Not yet verified at runtime.** No end-to-end run has been recorded on Claude
Code, Codex or agy. The criteria above are the skill's stated completion
conditions, not observed results.

## Known limitations

Static review only: it never runs the code, a build, a test suite or a scanner,
and it queries no vulnerability database — a dependency judged against
remembered advisories is labelled a judgement call, not a verdict. It cannot
establish runtime behaviour, real contrast values, focus or announcement order.

Coverage is bounded by one session. A repository large enough to exhaust it
gets a partially-covered axis with the boundary named, never a clean one.

The three axes need different targets to be exercised at all. A run against a
repository with no UI leaves the accessibility axis reporting *not applicable*,
which is the correct outcome there but exercises nothing. A repository with real
UI, authentication and dependencies is what tests all three.

This is not QA, not a penetration test, not an accessibility certification, and
not sign-off on anything.

## Where it fits

Outside the chain. It has no input artifact and no predecessor, and its output
flows back to the top: `grill-me` on the saved report, in a new session, when
the findings are worth acting on. See the [overview](./README.md) for the chain
it is deliberately not part of.
