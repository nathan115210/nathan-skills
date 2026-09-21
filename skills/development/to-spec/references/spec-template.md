# Spec template

The body of the spec issue. Sections marked *required* always appear, even if the answer is "none". Omit an optional section rather than filling it with filler.

Write from the user's perspective where the section says so — not from the implementation's.

---

## Problem Statement *(required)*

The problem being solved, from the perspective of whoever has it. What is currently wrong, who it affects, and what it costs them.

Not: what will be built.

## Solution *(required)*

What changes for that person once this is done, from their perspective.

Not: how it is built.

## User Stories *(optional)*

A numbered list, each in the form:

> As an `<actor>`, I want `<capability>`, so that `<benefit>`.

Include this only when the work has several distinct actors or flows and enumerating them adds something the Solution section does not. It is not a substitute for the Acceptance Criteria section — a user story is looser than a test name, and only test names are evidence that a requirement is specific enough to build against.

## Scope *(required)*

**In scope** — the boundary of this spec, in one short list.

**Out of scope** — what a reader would reasonably assume is included but is not, and why. This section earns its place by what it prevents, so name the assumptions you are cutting off rather than listing everything the system does not do.

## Seams *(required)*

The boundary or boundaries at which this work's behavior will be observed by tests.

For each seam:

- Where it is, named in the project's own vocabulary.
- Whether it already exists or is new.
- If new: why no existing seam could observe the behavior.

State the total count. One is the target. If there is more than one, say why the extras are unavoidable.

This section is the reason this spec exists as a single document rather than as a pile of tickets: the seam count is a whole-codebase property, so it is settled once, here.

## Implementation Decisions *(required)*

The decisions that are already made, one per entry. Draw on:

- Which modules get built or changed
- The interfaces of those modules
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions
- Technical clarifications the user gave

**No code snippets, and file paths in one place only.** They go stale faster than anything else here.

**Code locations (optional).** After the decisions, one line: `Code locations (as of <short revision>): <path>, <path>`. Paths only — no line numbers, no snippets, and no path anywhere else in the spec. Take the revision from `git rev-parse --short HEAD` when you explored the code, and list only paths you actually read. Omit the line if you did not explore or would be guessing. It is a hint from that revision; whoever builds reads the current source.

*Snippet exception:* a snippet that encodes a decision more precisely than prose can — a state machine, a reducer, a schema, a type shape — may be inlined in the decision it belongs to. Note that it came from a prototype. Keep only the decision-dense part; this is not a working demo.

**No breakdown into tickets and no dependency ordering.** Both are expressed later as native sub-issue and blocking relations, which are queryable state. Prose here would be a second copy that drifts from it.

## Testing Decisions *(required)*

- What makes a good test for this work: external behavior only, never implementation detail.
- Which modules get tested, at the seams named above.
- Prior art — existing tests in this codebase of the same kind, referred to by what they cover rather than by path.

## Acceptance Criteria and Test Names *(required)*

Each acceptance criterion, followed by at least one **specific** test name it maps to.

```
Rejects an order whose total is negative
→ it('rejects order with negative total')
  Given an order with total -1, it is rejected with the reason "negative total"; observed in the submit response.
```

Keep each criterion's concrete values exactly as the input states them — the literal outputs, amounts and messages — not a paraphrase such as "rejects it". When the input also gives a test name's precondition, expected result or how it is observed, carry that under the name as one indented line, in the input's own words. When it gives none, write no line.

A criterion that cannot produce a specific test name is not specific enough:

```
Handles invalid orders
→ it('handles invalid order') ✗ which invalid ones? what is correct for each?
```

**Transcribe only.** Every criterion, every concrete value and every test name here comes from the input. If the input has none, write:

> No acceptance criteria were settled in the input. This spec is not yet buildable.

Do not invent criteria to fill the gap, and do not soften the statement. Whoever reads this issue needs to know the gap exists.

## Combined Behavior *(required)*

The behavior that must still hold once every part of this work is in place — the thing no single part is responsible for and that therefore nobody tests unless it is written down here.

Like acceptance criteria, it is a list of **test names**, not prose. It lives here rather than in any later ticket for the same reason the seams do: it is a property of the whole, and the whole is only visible at this level.

**Transcribe only.** If the input settled no combined behavior, write:

> No combined behavior was settled in the input.

Do not invent it. If the work plainly has interacting parts and this list is empty, that absence is itself worth stating in one line.

## Rejected Alternatives *(required)*

Each approach that was considered and dropped, with the reason it was dropped.

This section is the most expensive one to reconstruct later and the one most often left out. Without it, the same alternative gets re-proposed, re-argued, and sometimes adopted — and the reason it failed the first time is gone.

Write "none — no alternatives were considered" if that is the truth. It is a useful thing for a reader to know.

## Further Notes *(optional)*

Anything load-bearing that has no home above: constraints from outside the codebase, accepted risks, open questions that do not block the work.