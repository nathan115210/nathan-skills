---
"nathan-skills": patch
---

code-review no longer ships the inert `readonly-guard.md` command-guard
prototype. Its warning is now stated directly in `SKILL.md`: the skill ships no
hook and no command guard, read-only must be enforced outside the model, and a
command allowlist is not that guarantee because it misses write operands and
fails open on unknown payloads.
