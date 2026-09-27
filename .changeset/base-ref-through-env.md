---
"nathan-skills": patch
---

Pass the pull request's base branch to the changeset check through `env:` instead of expanding it into the shell script, and fail the scripts test suite when any workflow `run:` block contains a `${{ }}` expression
