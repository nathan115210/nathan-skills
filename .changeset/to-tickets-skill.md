---
"nathan-skills": minor
---

Add the `to-tickets` skill: splits one spec issue into sub-issues carrying
native GitHub blocking relations.

It cuts tracer-bullet vertical slices (with expand–contract sequencing for wide
refactors), allocates the spec's test names to those slices without inventing
any, and marks every slice the spec cannot make buildable. Seams are quoted from
the spec, never re-chosen. Nothing is published until the breakdown is approved,
and the relation graph is read back and compared node by node afterwards.

Both GitHub relations are written by issue `id`, not issue `number`. Passing a
number to `dependencies/blocked_by` returns HTTP 200 and attaches an unrelated
issue from another repository, so the read-back check is required rather than
optional.

Existing installs must re-run `./scripts/relink.sh` to pick the skill up.
