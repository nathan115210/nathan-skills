---
"nathan-skills": minor
---

`to-tickets` no longer creates an issue that only restates or contains another.

When a spec's cut yields exactly one slice, no sub-issue is created: the spec
issue itself is the ticket. The preview says so and shows the complete board
order with the spec issue placed in it, under one approval; the only write is
the spec issue's board position, and nothing at all is written when it is on no
board or the token lacks the `project` scope. The read-back confirms zero
sub-issues and an unchanged spec title and body, and the hand-off is `dev` on the
spec issue — or, for a spec without test names, `nathan-grill-me` then `to-spec`.

On the scan path, findings are counted before anything is created. Exactly one
confirmed finding becomes one issue carrying the scan's provenance, the finding
and the not-buildable statement, with no tracking parent. Two or more slices or
findings behave as before.
