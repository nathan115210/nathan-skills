# nathan-skills

## 0.2.0

### Minor Changes

- [#6](https://github.com/nathan115210/nathan-skills/pull/6) [`370153f`](https://github.com/nathan115210/nathan-skills/commit/370153f1f3d18306ea98d2349bd5681cc058d47e) Thanks [@nathan115210](https://github.com/nathan115210)! - accessibility-review now saves its report to `~/Downloads/a11y-<topic>.md` with a
  project identity line and the scope it ran, and ends by pointing at `grill-me` in
  a new session. It still decides nothing about which findings get fixed, and it
  does not invoke or offer to run the next step.

- [#5](https://github.com/nathan115210/nathan-skills/pull/5) [`021d8f2`](https://github.com/nathan115210/nathan-skills/commit/021d8f2fcd3cc0a7c026c55fdad7fcd917a966c4) Thanks [@nathan115210](https://github.com/nathan115210)! - Add safe global skill uninstall with a dry-run preview, preserve foreign links and project configuration, and document uninstall and clone moves.

- [#10](https://github.com/nathan115210/nathan-skills/pull/10) [`6d0089c`](https://github.com/nathan115210/nathan-skills/commit/6d0089cef90c1bc9b765b278de8dcd91ca34a42d) Thanks [@nathan115210](https://github.com/nathan115210)! - `relink.sh` now refuses to run from a linked `git worktree` unless given
  `--force`.

  It derives the repository to link from its own location, so a run inside a
  worktree repointed all three tools at that branch's skills. Nothing looked
  wrong afterwards — the links were valid — while the tools quietly ran that
  branch, including versions of a skill that had been superseded on the main
  branch. The refusal happens before any tool directory is touched and names both
  the worktree and the main checkout. `--list` stays read-only and unguarded, and
  a directory that is not a git repository is unaffected.

  This is a minor bump because an invocation that previously succeeded now exits
  non-zero: anyone who relinks from a worktree must either run from the main
  checkout or pass `--force`.

- [#10](https://github.com/nathan115210/nathan-skills/pull/10) [`6d0089c`](https://github.com/nathan115210/nathan-skills/commit/6d0089cef90c1bc9b765b278de8dcd91ca34a42d) Thanks [@nathan115210](https://github.com/nathan115210)! - Add the `to-tickets` skill: splits one spec issue into sub-issues carrying
  native GitHub blocking relations.

  It cuts tracer-bullet vertical slices (with expand–contract sequencing for wide
  refactors), allocates the spec's test names to those slices without inventing
  any, and marks every slice the spec cannot make buildable. Seams are quoted from
  the spec, never re-chosen. Nothing is published until the breakdown is approved,
  and the relation graph is read back and compared node by node afterwards.

  Both GitHub relations are written by issue `id`, not issue `number`. Passing a
  number to `dependencies/blocked_by` returns HTTP 200 and attaches an unrelated
  issue from another repository, so the read-back check is required rather than
  optional.

  Existing installs must re-run `./scripts/relink.sh` to pick the skill up.

- [#2](https://github.com/nathan115210/nathan-skills/pull/2) [`872f430`](https://github.com/nathan115210/nathan-skills/commit/872f4300334a988b8d9a1b9a2acfaa674c5e7ad7) Thanks [@nathan115210](https://github.com/nathan115210)! - Version the repository with changesets. `package.json` carries the version,
  `.changeset/` holds pending changes, and `CHANGELOG.md` is generated from them.
  A `Release` workflow on `master` opens a "chore: version skills" pull request
  and tags the commit once it merges.

### Patch Changes

- [#4](https://github.com/nathan115210/nathan-skills/pull/4) [`b595fc1`](https://github.com/nathan115210/nathan-skills/commit/b595fc1bf119f15a39e27d6e81df6871b2020a43) Thanks [@nathan115210](https://github.com/nathan115210)! - Add portable code-review and accessibility-review skills for Claude Code,
  Codex and agy, with shared human-facing documentation and safeguards that keep
  raw runtime evidence out of the docs tree.
