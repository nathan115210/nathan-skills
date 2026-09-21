---
"nathan-skills": patch
---

`to-spec` now keeps each acceptance criterion's concrete values (the literal
outputs, amounts and messages) instead of paraphrasing, and carries a test
name's precondition, expected result and observable under it when the PRD states
them. `to-tickets` copies test-name lines and those detail lines character for
character. Found in an agy run where a spec dropped `HI ANN` and `HI WORLD` into
"prints the greeting in uppercase" and the template had no place for the rest.
Also removes a stale `to-spec` check that a PRD's identity line matches the
project, which no longer exists now that the PRD lives in the project.
