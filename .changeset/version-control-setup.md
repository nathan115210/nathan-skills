---
"nathan-skills": minor
---

Version the repository with changesets. `package.json` carries the version,
`.changeset/` holds pending changes, and `CHANGELOG.md` is generated from them.
A `Release` workflow on `master` opens a "chore: version skills" pull request
and tags the commit once it merges.
