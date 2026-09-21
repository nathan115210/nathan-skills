---
"nathan-skills": patch
---

`codebase-scan` no longer restates the `.nathan-skills` save steps. It points to the shared save-folder protocol in `nathan-grill-me/references/` through the runtime's skill catalogue and keeps only its own rules: the `code-scan` subfolder, the `<scope>` filename key, that a same-day rescan of the same scope replaces the file, and that the user may decline the file. Saving a report behaves as before; `nathan-grill-me` must be installed, which `relink.sh` already does.
