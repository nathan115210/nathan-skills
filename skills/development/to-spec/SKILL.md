---
name: to-spec
description: Turn settled decisions — normally a document such as a planning PRD, read in a fresh session — into one spec issue, and choose the test seams. No interview, no ticket splitting.
disable-model-invocation: true
disallowed-tools: Write, Edit, NotebookEdit
---

# To Spec

You are the only writer of specs in this workflow. A spec lands in exactly one issue in the project's tracker. It never lands in a file.

Two things happen here and nowhere else:

1. Decisions that are already settled become a spec issue.
2. The **seams** the work will be tested at get chosen — once, for the whole spec.

## Inputs

Exactly one of:

| Input | Where it is | How to read it |
| --- | --- | --- |
| **A document whose decisions are settled** — the normal case | Typically a planning PRD in `~/Downloads`, named whatever the user confirmed when it was written; may also be someone else's spec, a design doc, meeting notes — format is not assumed | Read it in parts. See below. |
| A discussion that just finished — the exception | Already in this conversation | Read nothing. Synthesize what is here. |

If neither is present, stop and say so. Do not run an interview to manufacture one.

**The document is the normal input, and this skill normally starts in a fresh session.** A real planning interview ends with its context spent and partly compacted, and compaction drops exactly what this skill transcribes word for word — the precise test names, the reason each alternative was rejected. Whoever ran it wrote the decisions to a file for that reason; read the file.

The second mode is for a short discussion held right here that never produced a document. If a document exists, read it rather than the conversation, even when you were present for the conversation — the file is what the next reader will have.

**The document is not in the project.** Planning PRDs are written to `~/Downloads`, so nothing in the repository points at one and no search of the project will find it, and its filename follows no rule — it is whatever the user confirmed at the time. Ask which file to read, or list `~/Downloads` for `prd-*.md` and confirm the match before reading.

Then **check the file's identity line** — its first line names the project and repository it plans. If it names a different project, or has no identity line at all, stop and ask rather than specifying the wrong work. Several projects share that folder, and transcribing the wrong document produces a spec that looks right.

### Reading a settled document

A settled document can be far larger than one read. Before reading any of it:

1. Measure it (`wc -c`).
2. Above roughly 50KB, do not read it whole — the read will fail or crowd out the spec you are about to write. Find its index (a table of contents, a decision table, numbered headings) and read only the sections this spec needs.
3. A spec built from part of a document must say which part — that is step 0 below.

## Boundaries

**Yours:**

- Read code, history, and existing issues.
- Choose seams, and get them confirmed.
- Write the spec issue, or write back into an existing one.

**Not yours:**

- **Interviewing for requirements.** If a requirement is still open, name it and stop. Resolving it is `grill-me`, in its own session.
- **Splitting the work into tickets.** `to-tickets` is the only splitter.
- **Inventing acceptance criteria or test names.** The user sets what counts as correct. You transcribe.
- **Writing any document.** No `.md` file, no `.scratch/` directory, no local copy of the spec. The only exit is an issue. The planning PRD that may have fed this spec is an *input*; it is not maintained afterwards and is expected to go stale.
- **Touching code or git.** No edits, no worktree, no spike, no commit, no push.

"No interview" means no interview *about requirements*. It does not silence you: confirming the seams with the user is a required step, and so is naming a gap you found.

## Process

### 0. Name the input, and check you can publish

State which of the two input modes you are using, and — for a settled document — which sections you read and which you skipped. One line. This is the only thing that tells a later reader what the spec was built from.

Then confirm the tracker is usable **before doing the work**, not after. The check and its three outcomes are in step 4; run it here. A spec has nowhere to land if this fails, and finding that out at the end wastes the whole session.

### 1. Explore the codebase

Not optional, and not skippable on the grounds that the discussion was thorough. Seams are a property of the code, not of the discussion — you cannot pick one without reading the code.

Find the current state of the area being touched, the vocabulary already in use, and any conventions or ADRs that constrain it. Write the spec in the project's own vocabulary; if the project has none, use the vocabulary in the code rather than inventing a parallel set of terms.

### 2. Choose the seams, then confirm them

A **seam** is the boundary at which the work's behavior can be observed by a test.

Apply in order:

1. Prefer an existing seam to a new one.
2. Use the highest seam that can still observe the behavior.
3. Keep the total number across the codebase as low as possible. **The ideal number is one.**
4. If a new seam is genuinely needed, propose it at the highest point you can.

Rule 3 is why seams are chosen here — once per spec — rather than per ticket. Seam count is a whole-codebase property; choosing per ticket multiplies seams by construction, which is the opposite of the goal.

Then present the seams and get the user's confirmation before publishing. Requirements are not yours to ask about; seams are yours to propose and the user's to approve.

### 3. Write the spec

Read `references/spec-template.md` and follow it.

Four hard constraints:

- **No file paths and no code snippets.** They go stale faster than anything else in a spec, and a stale spec is worse than a missing one. *Exception:* when a snippet encodes a decision more precisely than prose can — a state machine, a reducer, a schema, a type shape — inline it inside the decision it belongs to, note that it came from a prototype, and keep only the decision-dense part. Not a working demo.
- **No breakdown and no dependency ordering.** Do not write "this splits into three parts" or "A must land before B" in the body. Both get expressed later as native sub-issue and blocking relations, which are queryable state. Prose would be a second copy of that state, and it would drift from it.
- **Note discrepancies.** Where the spec departs from the input — a decision the codebase has already overtaken, two sections of the document that contradict each other, a requirement that cannot be expressed at the chosen seams — say so in the issue, with the reason. Do not silently reconcile.
- **Transcribe; do not invent.** If the discussion produced a list of test names, it goes into the issue as written. That list is the workflow's only evidence that the requirements are specific enough to build against, and it dies with the session if you leave it in the conversation. If the input has no test names, write none — and do not triage the gap; `to-tickets` marks which tickets are missing a list.

### 4. Publish

**GitHub is the only tracker this skill publishes to.** This is the check from step 0 — reachable, authenticated, and writable by this account:

```
gh repo view --json nameWithOwner,viewerPermission -q '.nameWithOwner + " " + .viewerPermission'
```

`ADMIN`, `MAINTAIN` or `WRITE` means publish. `READ`, `TRIAGE`, an auth error, or no repo means stop. Three outcomes, all of which must be reported:

| Outcome | Do |
| --- | --- |
| Repo resolves and permission is writable | Publish. |
| Repo resolves but permission is read-only, or `gh` is not authenticated | Stop. Say exactly what failed and which account it checked. |
| No GitHub repo here | Stop. Say so. Do not look for another tracker. |

In the last two cases, **do not fall back to writing the spec to a file.** A spec in a file is the second record this workflow exists to avoid. An unpublished spec is a blocked step, not a reason to change medium.

But do not throw the work away either: **print the finished spec body in this conversation** so the user can place it themselves, and say plainly that it was not published. The conversation is not a second record — it dies with the session, which is exactly why the spec must still reach an issue.

**Do not add the issue to a GitHub Project and do not set any Project field.** Nothing in this workflow reads them.

**New spec → create one issue.** Do not decide whether it is a "parent". It becomes a parent if and when `to-tickets` attaches sub-issues to it; if the work turns out to be a single ticket, it has no children and never was one. That count is only knowable at splitting time, so it is not a judgment you make here.

**Existing issue that needs completing → write back into that issue.** Read it first, including comments. Add the missing parts to the body and leave what is already correct alone. Do not open a second issue, and do not put the spec in a comment — the body holds the specification; comments hold process records.

**No readiness label.** Whether an issue is ready to build is judged by its contents — whether it carries a list of test names — not by a label. A label would be a second copy of that fact, and it would drift from it.

### 5. Hand off

Say plainly what comes next: run `to-tickets` on this issue.

Do not invoke it. Skills in this workflow are not chained inside one session; the user starts the next one.

## Verification

- One input mode was used, and it was named at the start — not reconstructed at the end.
- If the input was a document, its identity line was checked and it names this project.
- The tracker was confirmed usable before the work was done.
- The codebase was explored before seams were chosen.
- The seam count is stated, is as low as the work allows, and was confirmed by the user.
- No file paths or code snippets, except prototype snippets marked as such.
- No breakdown and no dependency ordering in the body.
- Every acceptance criterion and every test name in the issue — including the combined-behavior list — traces to the input. None were invented.
- The spec exists as an issue. No file was written.
- If the input document was read in part, the sections read and skipped are named.
- Any discrepancies between the spec and the input are noted and justified.