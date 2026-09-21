---
"nathan-skills": minor
---

`grill-me`, `codebase-scan` and `accessibility-review` now save their documents
inside the project instead of `~/Downloads`: `.nathan-skills/prd/`,
`.nathan-skills/code-scan/` and `.nathan-skills/accessibility-audit/`, each file
named `<topic>-<YYYY-MM-DD>.md`. The first write creates the folder and a
`.nathan-skills/.gitignore` containing `*`, so no tracked file changes. `grill-me`
no longer asks you to confirm a filename and resumes an existing PRD by topic
whatever its date; its PRD no longer carries an identity header. `to-spec` reads
the PRD from `.nathan-skills/prd/` and no longer checks an identity line.
`nathan-setup`'s project workflow block now says PRDs go in `.nathan-skills/prd/`
(projects set up earlier keep the old wording until `nathan-setup` refreshes them).
Existing files in `~/Downloads` are not migrated; move them by hand to keep using
them.
