# Ticket template

The canonical body of every sub-issue. Render it into the ticket's scratch file
during breakdown confirmation, show that file's contents as the preview, then
publish that same file unchanged. Do not compose the body for the first time
while creating the issue.

One ticket per issue. Never a combined issue holding several tickets.

## The skeleton

An issue body is exactly this, in this order — nothing above `## What to build`,
nothing between the sections, and no heading not listed here:

```markdown
## What to build

<the observable end-to-end result>

## Acceptance criteria and test names

<criterion/test-name pairs from the spec, or the not-buildable statement>

## Notes

<load-bearing context; omit this heading entirely when there is none>
```

**Everything outside that block is instruction to you, not content for the
issue.** The headings below explain the three sections; they are not part of
them. If a heading of this file ever reaches an issue body, the render was
wrong.

## What to build

The end-to-end behavior this ticket makes work, from the perspective of whoever gets it — not a layer-by-layer implementation list.

A reader who has not seen the spec should be able to tell from this section what will be true once the ticket is done.

Not: which files change. Not: the order to write the code in.

## Acceptance criteria and test names

The criteria this slice is responsible for, in the spec's own shape — each criterion followed by the specific test name it maps to:

```
Rejects an order whose total is negative
→ it('rejects order with negative total')
```

**Transcribe only.** Every criterion and every test name here is copied from the spec, unchanged. If no test name in the spec covers this slice, write exactly:

> No test name in the spec covers this slice. Not buildable — the gap is in the spec, not in this ticket.

That sentence is canonical here. Other steps point at this file for its wording rather than restating it, so it has one copy and cannot drift.

Do not invent a criterion to fill the gap, and do not soften the statement.

A spec criterion carrying several test names may have them split across slices. Repeat the criterion line in each slice that carries one of its test names, with only that slice's test names under it. The criterion is context for reading the test name; only the test names are exclusive to one slice.

Do not copy the spec's **Combined Behavior** list here. It belongs to the whole and stays on the parent.

## Notes

Anything load-bearing with no home above: a constraint from outside the codebase, an accepted risk, a prefactor this slice assumes has landed.

This section is optional. When there is nothing load-bearing to add, omit both
the heading and its body.

## A rendered ticket, start to finish

This is what a finished body looks like — everything between the fences, and
nothing else:

```markdown
## What to build

Order totals are validated when an order is submitted. Submitting an order whose
total is negative or exceeds the account limit is rejected with the reason, and
the order is not created. Submitting a valid order behaves exactly as it does
today.

## Acceptance criteria and test names

Rejects an order whose total is negative
→ it('rejects order with negative total')

Rejects an order whose total exceeds the account limit
→ it('rejects order above account limit')

Accepts an order at exactly the account limit
→ it('accepts order at account limit')

## Notes

The account limit is set by the billing system and is not editable here; treat
it as read-only input. Blocked on the validation seam added by the prefactor
ticket, which must land first.
```

Note what is absent: no parent, no blocker list, no labels, no file paths, no
checklist, and no heading from this file. The blocker is mentioned in Notes only
because the *constraint* is load-bearing — the edge itself is native state.

And a not-buildable slice, in full:

```markdown
## What to build

Submitted orders are written to the audit log with their computed total, so a
rejected order can be traced back to the value that caused it.

## Acceptance criteria and test names

No test name in the spec covers this slice. Not buildable — the gap is in the spec, not in this ticket.
```

## Rendering contract

Before publication, every preview and final issue body must satisfy all of these:

- `## What to build` appears once and contains the observable end-to-end result.
- `## Acceptance criteria and test names` appears once and contains only exact
  criterion/test-name pairs from the spec, or the exact not-buildable statement.
- `## Notes`, when present, comes last and contains only load-bearing context.
- No template instructions, placeholder text, parent prose, blocker prose,
  labels, status, file paths, or implementation checklist appears in the body.
- The body read back from GitHub is byte-identical to the scratch file it was
  published from, confirmed with `diff` rather than by reading it.

---

## What this template deliberately does not have

**No "Parent" section.** The parent is a native sub-issue relation, which is queryable state. A line of prose naming it is a second copy that drifts.

**No "Blocked by" section.** Blocking edges are native issue dependencies, for the same reason. If the body and the graph disagree, someone acts on the wrong one.

**No status, and no readiness marker.** Whether a ticket is buildable is judged by whether it carries test names. A label, a status line or a Project field would be a second copy of that fact.

**No file paths and no code snippets.** They go stale faster than anything else in a ticket.

*Exception:* a snippet that encodes a decision more precisely than prose can — a state machine, a reducer, a schema, a type shape — may be inlined in the section it belongs to. Note that it came from a prototype, and keep only the decision-dense part. This is not a working demo.
