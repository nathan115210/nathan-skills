---
"nathan-skills": patch
---

Clarify `to-tickets` body read-back in step 8 and its docs page: keep the valid
`gh api --jq '.body'` form, and note that `--jq` appends a trailing newline of
its own, which otherwise makes every rendered ticket body diff as mismatched.