---
"nathan-skills": patch
---

`accessibility-review` no longer restates the `.nathan-skills` save steps. It points to the shared save-folder protocol in `nathan-grill-me/references/` through the runtime's skill catalogue and keeps only its own rules: the `accessibility-audit` subfolder, the `<topic>` filename key, that a same-day re-review of the same topic replaces the file, that the user may decline the file, and the identity header and scope line it adds to the saved file. Saving a report behaves as before; `nathan-grill-me` must be installed, which `relink.sh` already does.
