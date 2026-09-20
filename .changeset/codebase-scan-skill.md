---
"nathan-skills": minor
---

Add the `codebase-scan` skill, remove `integrate-review` from the workflow, and
let `to-tickets` order the backlog.

`codebase-scan` reviews a whole existing codebase as a Principal Software
Architect and Security Auditor plus a global accessibility pass. It runs
occasionally, by hand, and is **not** a step of the development workflow —
nothing waits on it and nothing passes through it. The three axes stay separate
and each has its own coverage rule: security is exhaustive by risk surface
(authentication, input boundaries, secrets, dependencies) regardless of churn,
architecture is hotspot-first over a commit window the report names, and
accessibility enumerates every file that renders or styles UI. Every axis must
declare what it did not cover, so a weak model produces a visibly thin report
rather than a confidently clean one. The report opens with a severity-ordered
candidate list annotated with suspected existing issue numbers, is saved to
`~/Downloads/code-scan-<project>.md`, and hands off to `grill-me` in a new session.
It writes nothing inside the scanned repository, makes no tracker write, and
invokes no other skill.

`integrate-review` is removed from `docs/development/README.md`. It was never
built and will not be; integration QA is done by hand, outside these skills.

`to-tickets` now reads every open issue on the parent's board, builds one total
order with the new tickets inserted, shows that complete order in its **existing**
approval preview, and writes it back as the board's item position after
publishing. A blocker always precedes what it blocks; existing issues keep their
relative order unless an edge forces a move, and every such move is named.
Setting Priority is no longer forbidden as ordering — order has no native source
to drift from — but it is written as item position rather than a Priority field,
and readiness labels, Status and Size remain forbidden.

Existing installs must re-run `./scripts/relink.sh` to pick up `codebase-scan`.
