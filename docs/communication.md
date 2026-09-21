# Global communication preferences

[instructions/communication.md](../instructions/communication.md) is the only
maintained source of response-style rules. They apply to ordinary conversations
and every skill, including skills outside this repository. They do not need a
skill invocation. `nathan-grill-me` owns its interview and PRD requirements, not a
second copy of the communication rules.

## Install and remove

Run from the main checkout:

```bash
python3 scripts/instructions.py install --dry-run
python3 scripts/instructions.py install
```

The installer links the same file at each tool's global entry:

| Tool | Entry |
| --- | --- |
| Codex | `~/.codex/AGENTS.md` |
| Claude Code | `~/.claude/CLAUDE.md` |
| agy | `~/.gemini/config/rules/AGENTS.md` |

Edits to the source are visible through all links without reinstalling. Start a
fresh session to load changed instructions. Existing files and foreign links
are preserved with `SKIP` and a nonzero exit; inspect and deliberately merge
existing preferences instead of deleting them to make installation pass. Codex's
override file blocks installation, and a custom `CODEX_HOME` requires manual
configuration. Worktree installation is refused.

These links are separate from skill discovery. `relink.sh` and `unlink.sh`
manage skill links only. Before moving or deleting the clone, also run:

```bash
python3 scripts/instructions.py remove --dry-run
python3 scripts/instructions.py remove
```

Removal deletes only exact links to this clone's communication file, including
an exact dangling link. It preserves real files, other links and the source.
After moving, old links require inspection; the new clone cannot adopt them.

## It's working if

A fresh ordinary conversation gives an actionable answer without invoking a
skill. During ongoing work it makes the current state visible without replaying
history. A `nathan-grill-me` interview still asks one product decision at a time and
keeps the PRD complete. Concise presentation must not discard required findings
or replace the skill's completion conditions.

On macOS, isolated filesystem checks passed for install, repeat install, source
edits flowing through links, dry-run, removal, exact dangling links, preservation
of foreign files/links, and the Codex override guard. These are installer checks,
not model behavior checks.

Bounded runtime checks on 2026-09-20 used a fresh temporary working directory
and an advice-only request to organize 30 photos, without invoking a skill:

| Tool/version | Observed result |
| --- | --- |
| Codex CLI 0.154.0-alpha.6.2 | Passed this response-shape scenario: action first, four numbered steps, current state and one small next action. |
| Claude Code 2.1.278 | Partial / failed list-cap check: two runs produced seven and six steps, and the second added tangents. A separate no-tool recall probe reproduced a rule from the global file; recall alone does not prove compliance. |
| agy, installed runtime reporting 1.2.2 | Partial / failed action-first check: five steps and one next action, but a separate state preamble came first. The startup log also contained authentication warnings, so full discovery/runtime health remains unverified. |

## Known limitations

Instructions guide model behavior; they do not mechanically guarantee every
response. Higher-priority host instructions, project constraints and explicitly
requested formats can affect presentation. Existing sessions may retain old
context. Full multi-turn and cross-skill runtime coverage remains unverified.
The observed Claude and agy deviations above mean this installation must not be
described as guaranteed compliance. A subsequent wording clarification places
state alongside or after the action; it has not been runtime-retested.

The Codex and Claude Code entries follow their
[global instruction documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
and [user memory documentation](https://code.claude.com/docs/en/memory).
agy's installed binary documents `~/.gemini/config/` as its customization root
and `rules/` as the rule directory; web documentation may describe a different
release. A link or documentation lookup alone is not runtime verification.

## Source and adaptation

Inspired by [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd/blob/main/skills/i-have-adhd/SKILL.md).
The preferences are rewritten for always-on use: no activation command,
invented time estimates, mandatory follow-up after completion, or additional
permission gates. General style rules belong here; interview-specific decisions
and artifact requirements belong in the skill.
