# codebase-scan

[Execution instructions](../../skills/development/codebase-scan/SKILL.md)

## What it does

Reviews an existing codebase as a whole, as a Principal Software Architect and
Security Auditor plus a global accessibility pass. Three axes run separately —
architecture, security, accessibility — each with its **own** coverage rule, and
each declaring what it did not look at. The report opens with a severity-ordered
candidate list, cross-referenced against the open issues, and is saved to
`.nathan-skills/code-scan/<scope>-<YYYY-MM-DD>.md` (git-ignored, inside the project).

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
Not into anything git tracks. The only file it writes is its own report, in the
git-ignored `.nathan-skills/code-scan/` folder (see
[Where documents are saved](./README.md#where-documents-are-saved)). The shared
save steps live in `nathan-grill-me`'s save-folder protocol, so `nathan-grill-me`
must be installed (`relink.sh` links every skill). The report keeps its identity header — project and
revision — because `to-tickets` reads it and it still says what was scanned once
the file is copied out.

**Does it create issues?**
Not while scanning, and it sets no field on the board. It reads the open issues
once, to annotate each candidate as *likely already tracked as #N* or *no
matching issue*. The annotation is a suspicion — matching a finding to an issue
title is fuzzy — and it is phrased as one.

Afterwards, it offers to. See [After the report](#after-the-report).

**Do I have to run `nathan-grill-me` on the report before anything can be tracked?**
No. That was the old single exit and it made tracking a finding cost a whole
interview. Say which findings you want tracked and run
[to-tickets](./to-tickets.md) in the same session; the interview moves to the
one ticket you later decide to start.

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

## After the report

The report ends by offering two ways forward and then stopping. It picks
neither for you.

| You want | Run | You get |
| --- | --- | --- |
| These findings on the board now | [to-tickets](./to-tickets.md), here in this session | A tracking parent for this scan, one child per finding you named, all marked not buildable, ordered by severity |
| To decide what is worth fixing first | [nathan-grill-me](./nathan-grill-me.md) on the report, in a **new** session | The normal chain: `nathan-grill-me` → `to-spec` → `to-tickets` |

The first is cheap and writes nothing down that the scan did not already find —
no ticket from it is buildable, and it says so in every body. Reach for the
second when the open question is which findings matter, not where they live.

The scan itself never writes to the tracker either way: on the short path the
writes happen inside `to-tickets`, after the report is saved and after you have
named the findings.

## It's working if

- The report names the project, the revision, and what was excluded.
- Each axis appears separately, with its own not-covered declaration in its own
  terms — surfaces for security, a named commit window for architecture, an
  enumerated file list for accessibility.
- The candidate list is severity-ordered and every entry carries a suspected
  issue number or "no matching issue".
- Nothing inside the scanned repository changed, and the tracker is untouched
  by the scan itself — it ends by offering, not by creating issues.
- An axis with nothing to scan (a repository with no UI) says so rather than
  passing silently.

**Verified end-to-end, once** — 2026-09-20, Claude Code 2.1.278, `gh` 2.80.0,
git 2.50.1, against this repository at `d61a154` (96 files; 60 `.md`, 9 `.py`,
8 `.yaml`, 4 `.json`, 2 `.yml`, 2 `.sh`; working tree dirty, which the report
recorded). The three axes ran as parallel subagents inheriting the session
model. Every criterion above held: each axis returned findings **and** its own
not-covered declaration, the candidate list came back severity-ordered with an
annotation on all 17 entries, the accessibility axis reported *not applicable*
with its enumeration rather than passing silently, and `git status --porcelain`
in the target repository was byte-identical before and after. The tracker
cross-reference ran against an authenticated `gh` with 0 open issues, so every
annotation was *no matching issue* as a fact. Cost: 191k subagent tokens, 57
tool calls, 6m48s. Raw output was kept outside this repository.

What that run did **not** establish, and it is most of the skill's range:

- **The accessibility axis only exercised its empty path.** This repository
  renders no UI, so the axis confirmed it enumerates and reports not-applicable
  correctly, and nothing about auditing an actual UI file.
- **The architecture axis's hotspot rule was not meaningfully exercised.** 21
  commits, max churn 8, median 1, all in one compressed span — the ranking
  could not separate files, and the axis said so and read the structural
  surfaces instead. Hotspot-first against a real history is untested.
- **The truncation path is untested.** 96 files did not come close to exhausting
  a session, so no axis ever had to report itself partially covered.
- **Read-only enforcement was behavioural only** on all three axes, which the
  report disclosed. No genuinely read-only execution environment was available,
  so the boundary is the reviewers' own conduct, not a guarantee.
- **Codex and agy are untested.** Discovery, the subagent-delegation step and
  the report file are unverified there.

The 17 candidates it produced are issues #19-#34 and #18 in this repository, so
the run's output is inspectable rather than only described here.

## Known limitations

Static review only: it never runs the code, a build, a test suite or a scanner,
and it queries no vulnerability database — a dependency judged against
remembered advisories is labelled a judgement call, not a verdict. It cannot
establish runtime behaviour, real contrast values, focus or announcement order.

Coverage is bounded by one session. A repository large enough to exhaust it
gets a partially-covered axis with the boundary named, never a clean one.

The three axes need different targets to be exercised at all, and the one run
on record proved the point rather than escaping it: against a repository with no
UI, no authentication and two dependencies, the accessibility axis correctly
reported *not applicable* and exercised nothing, and the architecture axis found
its churn ranking degenerate. A repository with real UI, authentication and a
dependency tree is what tests all three.

Subagent delegation is verified on Claude Code only. Where delegation is
unavailable the skill falls back to three sequential passes and must disclose
that context isolation was lost; that fallback has not been run.

**A run in agy (2026-09-21, agy 1.2.7)** on a small scratch project with an
`index.html` containing known accessibility barriers and a GitHub remote with no
issues. It saved `.nathan-skills/code-scan/full-2026-09-21.md` and a
`.nathan-skills/.gitignore` containing `*`; `git status` showed only the ignored
folder. The report carried the identity header, the scope line, a severity-ordered
candidate list of 13 findings (each marked "no matching issue"), all three axes and
a not-covered declaration per axis. It found the planted accessibility barriers.
Not tested: a repository with authentication and a real dependency tree, a rescan
on the same day, and any run in Claude Code or Codex. This run predates moving the
save steps into `nathan-grill-me`'s shared save-folder protocol; a save through the
shared file has not been run in any tool.

This is not QA, not a penetration test, not an accessibility certification, and
not sign-off on anything.

## Where it fits

Outside the chain. It has no input artifact and no predecessor, and its output
has two exits: `to-tickets` in the same session to track the findings as-is, or
`nathan-grill-me` on the saved report in a new session when what to fix is still open.
See [After the report](#after-the-report), and the [overview](./README.md) for
the chain it is deliberately not part of.
