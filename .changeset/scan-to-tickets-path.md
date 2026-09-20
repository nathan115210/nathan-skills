---
"nathan-skills": minor
---

`to-tickets` gains a second input mode, and `codebase-scan` stops forcing an
interview before anything can be tracked.

A `codebase-scan` findings list confirmed in the same session can now go
straight into `to-tickets`. That path creates one tracking parent
(`Codebase scan: <project> @ <revision>`) holding the report's identity header,
scope line and not-covered declarations, then one child per finding — unmerged,
unsubdivided, in the scan's own words and at the location it named. Every child
carries a new canonical not-buildable statement, because a findings list has no
seams and no test names; `grill-me` then `to-spec` on one issue is what makes it
buildable. The spec path is unchanged, including its Seams/Acceptance Criteria
gate, which the scan path skips.

Two rules are relaxed on the scan path only: the destination Project is asked
once about the tracking parent, since a just-created issue has no board to
inherit from, and a ticket may carry the finding's file, line and revision.

`codebase-scan` now ends by offering both exits — `to-tickets` here, or
`grill-me` in a new session when which findings matter is itself the question —
instead of mandating the second. It still makes no tracker write of its own.
