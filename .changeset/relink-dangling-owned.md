---
"nathan-skills": patch
---

relink.sh now decides whether it may replace a dangling link named after a current skill with the same ownership test prune and unlink.sh use. A link into this clone through a path it will not trust — `..`, `//`, a trailing `/.`, a symlinked folder, or a file rather than a skill folder — is left in place and reported as `dangling target not provably owned by this clone`, and relink exits non-zero. This replaces the old "ambiguous dangling target" message.
