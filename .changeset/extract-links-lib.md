---
"nathan-skills": patch
---

Extract shared link-ownership and tool-directory definitions from `scripts/relink.sh` and `scripts/unlink.sh` into `scripts/lib/links.sh`.
Both scripts source `scripts/lib/links.sh` with explicit readability guards and report missing library files on stderr before exiting with code 1.
