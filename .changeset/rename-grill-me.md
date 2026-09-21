---
"nathan-skills": minor
---

Rename the `grill-me` skill to `nathan-grill-me`. In agy, `/grill-me` resolves to
a command of the same name that is built into agy and never reads this skill, so the skill could not be invoked by name there. Everything that referred
to the old name now uses the new one; the skill's behaviour is unchanged. Existing
installs must re-run `./scripts/relink.sh`, which links `nathan-grill-me` and
prunes the stale `grill-me` link, and invoke `/nathan-grill-me` from now on.
