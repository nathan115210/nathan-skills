---
"nathan-skills": patch
---

`code-review` and `codebase-scan` no longer restate rules that `references/reviewer.md` already carries. Both read that file on every run, so the read-only enforcement disclaimer ("a role name is not enforcement; disclose a behavioural-only boundary") and "do not manufacture findings to look thorough" are now stated once there. `code-review` keeps the part that is its own — that it ships no hook and no command guard. `codebase-scan` also drops three paragraphs that restated its own coverage table and `references/coverage.md`: why the security axis is not churn-ranked, the weak-model rationale and the not-covered rationale. Both skills behave as before and neither has been re-run in any tool.
