# to-spec

[SKILL.md](../../skills/development/to-spec/SKILL.md)

## What it does

Turns decisions that are already settled into **one** spec issue on GitHub, and
chooses the seams the work will be tested at.

It does not interview you. By the time you reach for it the deciding is done, so
it synthesises what the input already says rather than opening a fresh round of
questions. Anything in the issue that you never actually decided is a defect.

It writes no files. The only exit is an issue.

## When to reach for it

You type it. It will not fire on its own.

| Where you are | What to run |
| --- | --- |
| Requirements are still open | [nathan-grill-me](./nathan-grill-me.md) first |
| Decisions settled, you want them tracked | `to-spec` |
| An issue exists but is missing its spec | `to-spec` — it writes back into that issue |
| You want the work split into tickets | [to-tickets](./to-tickets.md) |

Normally you run it in a **fresh session**, pointed at the PRD
[nathan-grill-me](./nathan-grill-me.md) wrote. Reading a settled document is the normal input;
synthesising the current conversation is the exception, for a short discussion
that never produced a document.

That ordering is deliberate. A real interview ends with its context compacted,
and compaction drops exactly what this skill transcribes word for word — the
precise test names, the reason each alternative was rejected. The file survives
that; the conversation does not.

## Prerequisites

- A GitHub repository you have **write** access to. The check is explicit
  (`viewerPermission`), because read access alone makes a repository look usable
  right up to the moment it isn't.
- Settled decisions, in a document or in this conversation.
- The PRD is in `.nathan-skills/prd/` under the project root, git-ignored. The
  skill lists that folder and reads the match; it asks only if several topics
  could be meant. The folder belongs to one checkout, so from a different
  worktree or a fresh clone expect to be asked for the file's path.

## Seams, before any prose is written

A **seam** is the boundary at which the work's behaviour can be observed by a
test. Before writing, the skill reads the code — not the discussion — and
proposes the seams, then waits for you to confirm.

The rules, in order: prefer an existing seam to a new one; use the highest seam
that can still observe the behaviour; keep the total across the codebase as low
as possible, ideally one.

They are chosen here, once for the whole spec, rather than per ticket, because
seam count is a whole-codebase property — choosing per ticket multiplies them by
construction. "No interview" covers requirements, which are yours; seams are
proposed by the skill and approved by you.

## What the issue deliberately does not contain

- **No code snippets, and file paths in one place only.** They go stale faster
  than anything else, and a stale spec is worse than a missing one. Paths appear
  in a single optional "Code locations (as of `<revision>`)" line, so a reader can
  see which version of the code they describe; the builder reads current source.
  The snippet exception is a snippet that encodes a decision more precisely than
  prose can — a state machine, a schema, a type shape.
- **No breakdown and no dependency ordering in the body.** Both are expressed
  later as native sub-issue and blocking relations, which are queryable state.
  Prose would be a second copy that drifts from it.
- **No readiness label.** Whether an issue is ready is judged by whether it
  carries a list of test names — a label would be a second copy of that fact.
- **Nothing invented.** If the input has no test names, the issue says so
  outright: *"No acceptance criteria were settled in the input. This spec is not
  yet buildable."*

## Common questions

**Can I skip it and go straight to building?**
Often, yes. This step earns its place when the work is too big for one session
and has to survive being split. For a change you will finish in one sitting, the
spec is an extra synthesis step where meaning can drift. What it buys on larger
work is that tickets are disposable and the spec is not.

**It says my spec "is not yet buildable". Why won't it just fill in the gaps?**
Because inventing acceptance criteria is how a spec ends up asserting things
nobody agreed to. The gap is real: go back to [nathan-grill-me](./nathan-grill-me.md) and
settle it. The line stays in the issue so whoever reads it next knows.

**Publishing failed. Where did my spec go?**
It prints the finished body in the conversation and tells you plainly that it
was not published. It will not fall back to writing a file — a spec in a file is
the drifting second record this workflow exists to avoid — but it will not throw
the work away either. Copy it out, or fix the access and re-run.

**Does it add the issue to a GitHub Project?**
No, and it sets no Project fields — but **you should**, before running
[to-tickets](./to-tickets.md). That skill places every sub-issue on whatever
board this spec issue is already on, and it inherits rather than asks. Place the
spec afterwards and you get the spec on the board and none of its tickets.

This is deliberate rather than an oversight: the spec issue's placement is the
single switch controlling the whole breakdown's. Leave the spec off a board and
nothing from it reaches one. `to-spec` does not flip that switch for you, and it
reminds you at handoff.

**It told me to run `to-tickets`. What does that do?**
It splits this issue into sub-issues with native blocking relations, and marks
any ticket the spec cannot make buildable. See
[to-tickets](./to-tickets.md).

**Is the issue for me to read, or for the agent?**
Mostly for whoever builds it. The parts worth your eyes are the seams and the
scope section — those are where a wrong decision is cheapest to catch now and
most expensive to discover later.

**Will it keep the PRD in sync afterwards?**
No. Once the spec is in the issue, the issue is the maintained record and the
PRD is expected to go stale.

## It's working if

- It starts reading code and writing, rather than asking you a fresh round of
  requirement questions.
- It puts the seams to you before it writes, proposes as few as it can, and
  states the total.
- It names its input up front — which document, which sections it read and which
  it skipped.
- Every criterion in the issue is one you remember deciding, and it still carries
  the concrete values you settled on (the exact output, amount or message), not a
  paraphrase. Under each test name sits its precondition, expected result and how
  it is observed, when the PRD gave them.
- Exactly one issue exists afterwards, and no new file appeared anywhere.

## Known limitations

- **Codex has partial runtime coverage (2026-09-14, CLI 0.154.0-alpha.6.2).**
  Discovery, one implicit-invocation scenario and full template reading were
  checked. Normal explicit runs checked the PRD identity line (a check the skill
  no longer makes, now that the PRD lives in the project), and stopped without
  writing files when the required
  `gh repo view --json nameWithOwner,viewerPermission` check found no Git
  repository. Successful permission checks, seam confirmation and issue
  publication remain untested.
- **agy finds the PRD in `.nathan-skills/prd/` (2026-09-21, agy 1.2.7).** In an
  isolated scratch repository holding one PRD written by `nathan-grill-me`,
  `/to-spec` read `add-verbose-flag-2026-09-21.md` in full without being given a
  path, reported that the PRD still had open requirements, and stopped without
  writing anything; the repository had no GitHub remote, and it said publishing was
  blocked. Not tested: several topics or several dates in the folder, a missing
  folder and permission checks.
- **agy published a spec issue (2026-09-21, agy 1.2.7).** With a settled PRD in
  `.nathan-skills/prd/` and a private GitHub remote, `/to-spec` read the PRD in
  full, proposed two seams (`greet` return value; CLI standard output), asked for
  confirmation, and published issue #1. The issue carried the seams, all four
  acceptance criteria with their test names spelled exactly as in the PRD, and a
  "Combined Behavior" section stating none was settled. No file was written to the
  repository and nothing was staged. The PRD was written by hand rather than by
  `nathan-grill-me`, so this does not show that `nathan-grill-me`'s own output
  is accepted.
- **After the template fix, the same PRD kept its concrete values (2026-09-21, agy
  1.2.7).** Re-run on a fresh clone, `/to-spec` published issue #4 with each
  criterion in the PRD's own words (`prints HI ANN`, `prints hi ann`, `prints HI
  WORLD`) and, under each test name, a line giving the precondition, expected
  result and observable (for example `greet("ann", upper=True) == "HI ANN"`,
  observed as the return value of `greet`). It marked the CLI seam as new. That
  seam was first proposed as "existing"; it changed only because the user asked,
  so treat the label as something to check at the confirmation step. The prose
  sections still name `cli.py`, which the template's no-file-paths rule forbids;
  the commands inside the criteria are transcribed from the PRD.
- **The `disallowed-tools` field is not a Codex hard write barrier.** A separate
  diagnostic explicitly overrode the skill's prose prohibition and successfully
  created a canary using `apply_patch`. This proves that tool was available; it
  does not show a normal spec run violating the rule or establish how every
  frontmatter field is parsed. The skill body carries the no-file-write rule.
- GitHub only. No Linear, no local-file tracker, no detection of either.
- The downstream step, [to-tickets](./to-tickets.md), has runtime evidence only
  for the GitHub APIs it depends on, not for an end-to-end run.
- Large documents are read in parts; a PRD without stable section headings is
  hard to read selectively, which is why `nathan-grill-me` is required to write them.

## Where it fits

Upstream is [nathan-grill-me](./nathan-grill-me.md), which does the deciding this skill only
records. Downstream is [to-tickets](./to-tickets.md). See
[the workflow overview](./README.md).
