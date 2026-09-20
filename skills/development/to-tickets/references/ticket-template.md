# Ticket template

The body of one sub-issue. Sections marked *required* always appear, even if the answer is "none". Omit an optional section rather than filling it with filler.

One ticket per issue. Never a combined issue holding several tickets.

---

## What to build *(required)*

The end-to-end behavior this ticket makes work, from the perspective of whoever gets it — not a layer-by-layer implementation list.

A reader who has not seen the spec should be able to tell from this section what will be true once the ticket is done.

Not: which files change. Not: the order to write the code in.

## Acceptance criteria and test names *(required)*

The criteria this slice is responsible for, in the spec's own shape — each criterion followed by the specific test name it maps to:

```
Rejects an order whose total is negative
→ it('rejects order with negative total')
```

**Transcribe only.** Every criterion and every test name here is copied from the spec, unchanged. If no test name in the spec covers this slice, write exactly:

> No test name in the spec covers this slice. Not buildable — the gap is in the spec, not in this ticket.

Do not invent a criterion to fill the gap, and do not soften the statement.

Do not copy the spec's **Combined Behavior** list here. It belongs to the whole and stays on the parent.

## Notes *(optional)*

Anything load-bearing with no home above: a constraint from outside the codebase, an accepted risk, a prefactor this slice assumes has landed.

---

## What this template deliberately does not have

**No "Parent" section.** The parent is a native sub-issue relation, which is queryable state. A line of prose naming it is a second copy that drifts.

**No "Blocked by" section.** Blocking edges are native issue dependencies, for the same reason. If the body and the graph disagree, someone acts on the wrong one.

**No status, and no readiness marker.** Whether a ticket is buildable is judged by whether it carries test names. A label or a status line would be a second copy of that fact.

**No file paths and no code snippets.** They go stale faster than anything else in a ticket.

*Exception:* a snippet that encodes a decision more precisely than prose can — a state machine, a reducer, a schema, a type shape — may be inlined in the section it belongs to. Note that it came from a prototype, and keep only the decision-dense part. This is not a working demo.
