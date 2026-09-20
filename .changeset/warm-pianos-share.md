---
"nathan-skills": patch
---

Clarify `to-tickets` body read-back in step 8 and its docs page: use the valid
`gh api --jq '.body'` form, and note that the CLI adds one transport newline to
stdout when diffing a published body against the scratch file.