# Changesets

This folder holds the pending changes for the next release. Each file describes
one change in a human sentence; `changeset version` folds them into
`CHANGELOG.md`, bumps the version in `package.json`, and deletes them.

Add one with `npm run changeset` whenever you add, rename, or change the
behaviour of a skill, or change `relink.sh`. Choose the bump:

- **patch** — wording, docs, a fix inside an existing skill
- **minor** — a new skill, or a skill whose inputs or outcomes change
- **major** — a change that breaks an existing setup (a rename, a removed skill,
  a relink that existing installs must re-run)

Docs-only edits that change nothing a tool runs need no changeset.

See [the changesets docs](https://github.com/changesets/changesets) for the
full format.
