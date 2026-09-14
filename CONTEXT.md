# nathan-skills

Nathan's personal AI skills share one source across Claude Code, Codex and agy.
This file defines vocabulary used when maintaining that collection. Read the
[development overview](./docs/development/README.md) for the workflow and its
current implementation status.

## Shared terms

| Term | Meaning here |
| --- | --- |
| Workflow | A set of related stages, their responsibilities, and the artifacts passed between them. A workflow may include stages that are not implemented yet. |
| Skill | One reusable set of agent instructions, rooted at a `SKILL.md`. A skill is not the whole workflow. |
| Category | A source-tree grouping such as `development`. Installed skill names remain flat across tools. |
| Source repository | This repository, which maintains skills, shared helpers and their human-facing documentation. |
| Target project | The project a skill is planning, setting up or developing. Its files and rules are separate from this repository's maintenance files and rules. |
| Topic PRD | The planning document produced by `grill-me` in the user's Downloads folder, under a confirmed filename and with a project identity header. |
| Spec | Settled requirements and decisions recorded in one GitHub issue by `to-spec`. It is content in an issue, not a second local specification file. |
| Issue | A GitHub work item. A spec issue can later have sub-issues; it is not declared a parent merely because it contains a spec. |
| Seam | A boundary at which a test can observe behaviour. `to-spec` proposes the seams for the whole spec and obtains the user's confirmation. |
| Verification evidence | Actual commands, outputs and observed artifacts for a stated environment and scenario. Evidence supports only the behaviour exercised. |
| Changeset | One file in `.changeset/` describing a pending change and its bump. Written per change; consumed and deleted when a release is versioned. |
| Release | A version bump, a changelog entry and a git tag on `master`. Nothing is published to a package registry. |

## Document responsibilities

| Source | Responsibility |
| --- | --- |
| [AGENTS.md](./AGENTS.md) | Rules for working in this source repository. `CLAUDE.md` and `GEMINI.md` link to this same file. |
| [README.md](./README.md) | Human entry point: what this repository is, installation, uninstall and navigation. |
| `CONTEXT.md` | Shared vocabulary and the responsibilities of these documents. Update when their meaning changes. |
| `skills/<category>/<name>/SKILL.md` | Instructions for executing that skill, including its inputs, boundaries and completion conditions. |
| `docs/<category>/README.md` | The workflow map, entry choices and which stages are implemented. |
| `docs/<category>/<name>.md` | How a person uses one skill, recognizes a good run, and handles known limitations. |
| `.changeset/<name>.md` | One pending change and the bump it earns, in the words that will appear in the changelog. |
| `CHANGELOG.md` | The released history, generated from changesets. Never edited by hand. |
| `scripts/relink.sh` / `scripts/unlink.sh` | Install and remove this clone’s global skill links; preserve project configuration and other sources. |
| `scripts/check_changeset.py` | The enforced form of the changeset rules: what CI rejects, and what a waiver label means. |

Once `to-spec` publishes a topic's specification, the issue is the maintained
record and that topic PRD is expected to become stale. The human-facing skill
guide documents how this handoff works; it does not store the project's spec.

## Reading status accurately

Implemented means the skill exists. Discovered means a tool can find it.
Runtime-verified means a stated scenario was actually exercised on a stated
tool. These are separate claims: shared files and matching metadata do not
establish identical behaviour across tools, and a successful scenario does not
verify an entire workflow.
