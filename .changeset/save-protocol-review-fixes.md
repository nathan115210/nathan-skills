---
"nathan-skills": patch
---

Follow-ups to the shared save-folder protocol. `nathan-grill-me`, `codebase-scan` and `accessibility-review` now say what to do when the protocol file cannot be found (present the result unsaved, never save from memory), since that rule could not fire from inside the missing file. The protocol constrains the filename key to lowercase letters, digits and hyphens. `scripts/test_save_protocol.py` now scans every skill file for restated steps, covers both additions, and runs in the `Changeset` workflow. The earlier changesets no longer claim the other skills still carry their own copies.
