---
"nathan-skills": patch
---

`codebase-scan` now names `code-review`'s `references/reviewer.md` and locates it through the skill catalogue, instead of linking it by the relative path `../code-review/references/reviewer.md`. The scan behaves as before, including saying so in the report when the file cannot be found. A new test, `scripts/test_cross_skill_references.py`, fails when any skill file reaches into another skill's folder by relative path, and the rename procedure in `CLAUDE.md` gains a step to search other skills for the old name, with a matching "Removing a skill" note.
