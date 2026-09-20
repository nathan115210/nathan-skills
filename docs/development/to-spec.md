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
| Requirements are still open | [grill-me](./grill-me.md) first |
| Decisions settled, you want them tracked | `to-spec` |
| An issue exists but is missing its spec | `to-spec` — it writes back into that issue |
| You want the work split into tickets | [to-tickets](./to-tickets.md) |

Normally you run it in a **fresh session**, pointed at the PRD
[grill-me](./grill-me.md) wrote. Reading a settled document is the normal input;
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
- The PRD is not in your project — it is in `~/Downloads`, under whatever name
  you confirmed when it was written. Nothing in the repository points at it, so
  expect to be asked which file to read.

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

- **No file paths and no code snippets.** They go stale faster than anything
  else, and a stale spec is worse than a missing one. The exception is a snippet
  that encodes a decision more precisely than prose can — a state machine, a
  schema, a type shape.
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
nobody agreed to. The gap is real: go back to [grill-me](./grill-me.md) and
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
- Every criterion in the issue is one you remember deciding.
- Exactly one issue exists afterwards, and no new file appeared anywhere.

## Known limitations

- **Codex has partial runtime coverage (2026-09-14, CLI 0.154.0-alpha.6.2).**
  Discovery, one implicit-invocation scenario and full template reading were
  checked. Normal explicit runs checked the PRD identity line, rejected a
  different project, and stopped without writing files when the required
  `gh repo view --json nameWithOwner,viewerPermission` check found no Git
  repository. Successful permission checks, seam confirmation and issue
  publication remain untested. agy runtime behaviour remains untested.
- **The `disallowed-tools` field is not a Codex hard write barrier.** A separate
  diagnostic explicitly overrode the skill's prose prohibition and successfully
  created a canary using `apply_patch`. This proves that tool was available; it
  does not show a normal spec run violating the rule or establish how every
  frontmatter field is parsed. The skill body carries the no-file-write rule.
- GitHub only. No Linear, no local-file tracker, no detection of either.
- The downstream step, [to-tickets](./to-tickets.md), has runtime evidence only
  for the GitHub APIs it depends on, not for an end-to-end run.
- Large documents are read in parts; a PRD without stable section headings is
  hard to read selectively, which is why `grill-me` is required to write them.

## Where it fits

Upstream is [grill-me](./grill-me.md), which does the deciding this skill only
records. Downstream is [to-tickets](./to-tickets.md). See
[the workflow overview](./README.md).
