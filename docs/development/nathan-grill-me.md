# nathan-grill-me

[SKILL.md](../../skills/development/nathan-grill-me/SKILL.md)

## What it does

Interviews you about what you are building until the requirements are specific
enough to build against, and writes the result to a topic PRD in the project's git-ignored
`.nathan-skills/prd/` folder.

It asks one decision question at a time, with a recommendation and the trade-off
behind it. It will not invent agreement: what you decided, what it merely
proposed, and what is still open stay visibly separate in the file.

Response style comes from the [global communication preferences](../communication.md),
installed independently of skills. This skill retains the interview decisions
and PRD requirements; it does not duplicate the global formatting rules.

The interview ends when every acceptance criterion can produce a concrete test
name. That is the exit condition, not "we have talked enough".

## When to reach for it

You type it. It will not fire on its own.

Reach for it when you can feel the gap between what you want and what an agent
would build from your description — a new idea, a proposal you want stress-
tested, or an existing issue whose acceptance criteria are vague.

| Where you are | What to run |
| --- | --- |
| Requirements are still open | `nathan-grill-me` |
| Decisions are settled, and you want them in an issue | [to-spec](./to-spec.md) — it does not interview |
| An issue exists but says "handle errors properly" | `nathan-grill-me` first, then `to-spec` writes back into it |

Planning may stop here. Not every piece of work needs an issue, and nothing in
this skill pushes you onward.

## Prerequisites

The project should have been connected with
[nathan-setup](./nathan-setup.md) so the interview can read the project's own
rules and vocabulary. It is not a hard blocker: the skill can start from a bare
idea with no project at all.

## The PRD lands in `.nathan-skills/prd/`, ignored by git

The PRD is written to `<project root>/.nathan-skills/prd/<topic>-<YYYY-MM-DD>.md`,
a working document next to the project it plans but out of version control. The
folder layout, self-ignoring `.gitignore` and per-checkout limit are described in
[Where documents are saved](./README.md#where-documents-are-saved).

What is specific to this skill: it does not ask you to confirm a filename — the
folder is per project, so it states the full path once, when it first writes — and
a later session on the same topic reuses the existing file, keeping its name.

## Why the file has to stand alone

The next step runs in a **new session**, and by the end of a real interview this
one's context is spent and partly compacted. Compaction does not fail loudly —
it quietly drops the precise wording, which is exactly what the next step needs
to transcribe.

So before calling the PRD ready, the skill reads it as someone who was never in
the conversation: every decision with its reason, every rejected alternative
with why it was dropped, every test name spelled as agreed. Whatever stayed only
in the session is gone.

## Two things it will not do

**It does not choose the test seams.** Where tests observe the behaviour is one
decision made once for the whole specification, against the code, and it belongs
to [to-spec](./to-spec.md). A technical approach here says what gets built, not
where it is observed.

**It does not create or update GitHub issues.** That boundary is why planning
can stop at a file.

## Common questions

**When do I stop? The interview could go forever.**
When every acceptance criterion produces a concrete test name. `rejects order
with negative total` passes; `handles invalid orders` does not — which invalid
ones, and what is correct for each? If you cannot name the test, the requirement
is not settled yet. You can also stop early: it saves a partial PRD with its
open questions rather than pretending it is ready.

**A test-name list means the spec is complete, right?**
No — necessary, not sufficient. A name can be specific while the preconditions,
the expected result, or how you would observe it live only in the conversation.
That is what the stand-alone check is for.

**The work will span several issues. Where does the "do they still work
together" part go?**
In the PRD, as a **list of test names**, not as prose. The behaviour that must
hold once every part is in place is the one thing no single work item owns, so a
paragraph saying "check they still work together" gives the later QA step
nothing to check against.

**Can I keep editing the PRD after the issue is created?**
You can, but nothing reads it any more. Once the specification reaches an issue,
the issue is the record that is maintained and the PRD is expected to go stale.
There is no synchronisation between them, by design.

**It cannot write the file — permissions, or the tool is in a read-only mode.**
It will say so and show you the draft. It will not claim the file was saved and
will not quietly switch modes. Copy the draft out yourself.

## It's working if

- It asks one question at a time, with a recommendation attached, instead of
  dumping a checklist of concerns.
- It contradicts you when an answer conflicts with an earlier decision, and
  revisits what that breaks.
- The file grows during the conversation, not only at the end.
- Reading the finished PRD cold tells you *why* each decision was made, not just
  what it was.
- It hands you an absolute path and tells you to run `to-spec` in a **new**
  session.

## Known limitations

- **Codex has partial runtime coverage (2026-09-14, CLI 0.154.0-alpha.6.2).**
  Discovery and one implicit-invocation scenario were checked. That run tested
  the earlier `~/Downloads` behaviour (filename confirmation, identity header).
  The `.nathan-skills/prd/` location, the self-ignoring `.gitignore` and
  resume-by-topic are **unverified at runtime**. This does not verify a full
  interview, long-session behaviour or recovery after compaction.
- **agy's own `/grill-me` command took over the old name (2026-09-21, agy
  1.2.7).** With the skill still named `grill-me`, a minimal early-end scenario
  ("add a `--verbose` flag", then stop and save) ran twice in a scratch repository,
  once headless and once interactively. Both times agy wrote `prd_verbose_flag.md`
  to its own `~/.gemini/antigravity-cli/brain/` folder and created nothing under
  `.nathan-skills/`. In the interactive run, `/grill-me` expanded to a different,
  generic interview instruction and agy never read this skill's `SKILL.md`. That
  command is built into the agy binary (its description, "Interview me to align
  on a plan.", is in `~/.local/bin/agy` and in no file under `~/.gemini`), so it
  cannot be removed from configuration. The skill was renamed `nathan-grill-me` to
  avoid the clash.
- **`/nathan-grill-me` works on agy (2026-09-21, agy 1.2.7).** In an isolated
  scratch repository, the command was typed interactively, followed by "stop and
  save the partial PRD now". agy created
  `.nathan-skills/prd/add-verbose-flag-2026-09-21.md` and a `.nathan-skills/.gitignore`
  containing `*`; `git status` showed only the ignored folder. Its closing message
  gave the absolute path, the readiness status, the unresolved decisions and the
  next step (`to-spec` in a new session), as the skill requires.
- Not tested: a full interview, resume-by-topic on a later date, a refusal to
  overwrite an existing `.gitignore`, `to-spec` reading the folder, and any run in
  Claude Code or Codex.
- The PRD has no version history and is not backed up with the project. If you
  delete it, it is gone.

## Where it fits

Upstream is [nathan-setup](./nathan-setup.md), once per project. Downstream is
[to-spec](./to-spec.md), which turns this PRD into one issue — started by hand,
in a new session. See [the workflow overview](./README.md).
