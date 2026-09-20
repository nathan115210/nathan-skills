---
"nathan-skills": minor
---

relink.sh now removes this clone's links for skills that no longer exist, so a renamed or removed skill no longer leaves a dangling link behind. Updating an existing install is `git pull` then `relink.sh`; running `unlink.sh` first is no longer needed, and the rename procedure loses its manual cleanup step. Only links this clone owns are removed — real directories and links pointing outside the clone are untouched, using the same ownership test as unlink.sh.
