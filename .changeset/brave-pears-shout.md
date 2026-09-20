---
"nathan-skills": minor
---

Harden to-tickets against the failures that need manual GitHub cleanup: refuse to split a parent that already has sub-issues, stop on an issue that is not a to-spec spec, publish each body from the scratch file the preview was rendered from and diff the published body against it, match read-back issues by captured number rather than title, page past the read-back's `first:` caps, require distinct titles, and back off instead of retrying on 403/429. The ticket template now states the issue skeleton as a fenced block and carries two fully rendered example bodies.
