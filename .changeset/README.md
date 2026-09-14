# Changesets

This folder holds the pending changes for the next release. Each file describes
one change in a human sentence; `changeset version` folds them into
`CHANGELOG.md`, bumps the version in `package.json`, and deletes them.

Add one with `npm run changeset` whenever you add, rename, or change the
behaviour of a skill, or change `relink.sh`. Choose the bump:

- **patch** — wording, docs, a fix inside an existing skill
- **minor** — a new skill, a skill whose inputs or outcomes change, **or a change
  that breaks an existing setup** (a rename, a removed skill, a relink that
  existing installs must re-run)
- **major** — not used before 1.0. See below.

Docs-only edits that change nothing a tool runs need no changeset.

## Before 1.0, never pick `major`

Changesets does not soften a major bump on a `0.x` version: one major changeset
takes `0.1.0` straight to `1.0.0` (verified on changesets 2.31.1). This repo is
pre-1.0 and its workflow is unfinished, so breaking changes are recorded as
**minor** and `1.0.0` is released deliberately — not as the side effect of a
skill rename.

The version moves one step per release however many changesets have piled up:
the highest pending level wins, ten patches still make one patch bump. Every
entry appears in the changelog regardless.

`scripts/check_changeset.py` enforces this — on every pull request, and locally
before you open one. The **allow-major** label waives it for the deliberate
1.0.0 release; the **skip-changeset** label waives the requirement to add a
changeset at all, for a change no tool runs.

See [the changesets docs](https://github.com/changesets/changesets) for the
full format.
