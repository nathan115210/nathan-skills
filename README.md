# nathan-skills

One source of truth for a personal set of AI coding skills, shared across
Claude Code, Codex and agy (Antigravity CLI).

Every skill lives in this repository exactly once. Each tool's skills folder
holds a **symlink** back here, so editing a file updates it for all three tools
at the same time — there is no copy to keep in sync, and no tool that quietly
runs an older version.

```bash
git clone <this repo>
cd nathan-skills
./scripts/relink.sh
```

`relink.sh` derives every path from `$HOME` and its own location, so nothing
needs editing on a new machine. It refuses to overwrite anything it did not
create: it warns, skips, and exits non-zero.

## Layout

```
skills/
  development/
    grill-me/SKILL.md
    nathan-setup/SKILL.md
    to-spec/SKILL.md
scripts/
  relink.sh          links every skill into all three tools
  test_relink.py     isolated tests for the above
.changeset/          pending changes for the next release
docs/
  development/       how to use the workflow: one page per skill, plus an overview
```

Categories organise the source tree; the tool folders stay flat, so a skill is
called the same thing everywhere. Skill folder names must be globally unique,
and a skill's `name:` frontmatter must equal its folder name.

Helpers that belong to one skill live inside that skill (`scripts/`,
`references/`, `agents/`); only repository-wide scripts live in the root
`scripts/`.

## The skills

These are pieces of one development workflow, not a toolbox of unrelated
commands. Each step hands over an artifact — a file, then an issue, then a
branch — rather than a conversation, and skills are never chained inside one
session.

| Skill | Does |
| --- | --- |
| `nathan-setup` | Connects a project to this workflow across all three installed tools |
| `grill-me` | Planning interview; resolves decisions and writes a topic PRD |
| `to-spec` | Turns settled decisions into one spec issue; chooses the test seams |

The workflow continues past `to-spec` — splitting, implementation, review, QA —
but those skills are not built yet. Where a skill hands off to one that does not
exist, it says so rather than pretending the chain is complete.

**[How to use it → `docs/development/`](./docs/development/README.md)** — the
chain, where to start, and a page per skill covering when to reach for it, the
questions it raises in use, and what it does not do.

## Conventions

- **After adding a skill folder, run `./scripts/relink.sh`.** A new skill is
  invisible to every tool until you do. This is the step that gets forgotten.
- Editing an existing skill needs no relink — the symlinks already point here.
- Skills in this workflow are invoked explicitly, never auto-invoked, and never
  chained inside one session.
- `AGENTS.md` is the real file; `CLAUDE.md` and `GEMINI.md` are symlinks to it,
  so the operating rules cannot drift between tools.
- Every change a tool runs ships with a changeset — see below.

## Versioning

The repository is versioned as a whole with
[changesets](https://github.com/changesets/changesets); nothing is published to
npm. A change that a tool runs comes with a note describing it:

```bash
npm install          # once, for the changesets CLI
npm run changeset    # describe the change, pick patch / minor / major
```

Commit the generated file in `.changeset/` with the change. On merge to
`master`, the `Release` workflow opens a **chore: version skills** pull request
carrying the version bump and the new [`CHANGELOG.md`](./CHANGELOG.md) entry;
merging it tags the release.

Bump for the effect on someone whose tools already link to this repo: **patch**
for wording and fixes, **minor** for a new skill or changed inputs and outcomes,
**major** for anything that breaks an existing setup — a rename, a removed
skill, or a relink that has to be re-run.

## Not managed here

- `~/.codex/skills/.system/` — Codex built-ins.
- The 13 Cloudflare skills present as real directories in each tool folder
  (`cloudflare`, `wrangler`, `sandbox-*`, and the rest). They are a separate
  distributed pack.

`relink.sh` will not touch either.

## A note on the design record

The reasoning behind these skills — every decision, what was rejected and why —
is kept in a decision log that is deliberately not published, because it quotes
private project details. What survives publication is the rules themselves, in
`AGENTS.md` and in each `SKILL.md`. Where a rule looks arbitrary, it usually is
not; it is just that the argument for it lives elsewhere.
