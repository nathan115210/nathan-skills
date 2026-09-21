---
"nathan-skills": patch
---

`scripts/test_save_protocol.py` now also checks, across `nathan-grill-me`, `codebase-scan` and `accessibility-review`, that each names its own subfolder, filename key and replace-or-resume rule, and that none reaches the shared save-folder protocol through a cross-skill relative path. The docs pages and the development README record that saving through the shared protocol is untested at runtime. The earlier `nathan-grill-me` changeset says the other two skills still carry their own copies; they no longer do.
