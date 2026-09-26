# nathan-skills

## 0.2.0

### Minor Changes

- [#6](https://github.com/nathan115210/nathan-skills/pull/6) [`370153f`](https://github.com/nathan115210/nathan-skills/commit/370153f1f3d18306ea98d2349bd5681cc058d47e) Thanks [@nathan115210](https://github.com/nathan115210)! - accessibility-review now saves its report to
  `~/Downloads/accessibility-audit-<topic>.md`, with a project identity line and
  the scope it ran, and ends by pointing at `grill-me` in
  a new session. It still decides nothing about which findings get fixed, and it
  does not invoke or offer to run the next step.

- [#15](https://github.com/nathan115210/nathan-skills/pull/15) [`a0955a8`](https://github.com/nathan115210/nathan-skills/commit/a0955a8fa0a1827a70e4dc05d7a17eb8bbf35f14) Thanks [@nathan115210](https://github.com/nathan115210)! - Harden to-tickets against the failures that need manual GitHub cleanup: refuse to split a parent that already has sub-issues, stop on an issue that is not a to-spec spec, publish each body from the scratch file the preview was rendered from and diff the published body against it, match read-back issues by captured number rather than title, page past the read-back's `first:` caps, require distinct titles, and back off instead of retrying on 403/429. The ticket template now states the issue skeleton as a fenced block and carries two fully rendered example bodies.

- [#5](https://github.com/nathan115210/nathan-skills/pull/5) [`021d8f2`](https://github.com/nathan115210/nathan-skills/commit/021d8f2fcd3cc0a7c026c55fdad7fcd917a966c4) Thanks [@nathan115210](https://github.com/nathan115210)! - Add safe global skill uninstall with a dry-run preview, preserve foreign links and project configuration, and document uninstall and clone moves.

- [#16](https://github.com/nathan115210/nathan-skills/pull/16) [`26097b3`](https://github.com/nathan115210/nathan-skills/commit/26097b3a5d8ce1884fa0dc309c9f1ace8d232b31) Thanks [@nathan115210](https://github.com/nathan115210)! - Add the `codebase-scan` skill, remove `integrate-review` from the workflow, and
  let `to-tickets` order the backlog.

  `codebase-scan` reviews a whole existing codebase as a Principal Software
  Architect and Security Auditor plus a global accessibility pass. It runs
  occasionally, by hand, and is **not** a step of the development workflow —
  nothing waits on it and nothing passes through it. The three axes stay separate
  and each has its own coverage rule: security is exhaustive by risk surface
  (authentication, input boundaries, secrets, dependencies) regardless of churn,
  architecture is hotspot-first over a commit window the report names, and
  accessibility enumerates every file that renders or styles UI. Every axis must
  declare what it did not cover, so a weak model produces a visibly thin report
  rather than a confidently clean one. The report opens with a severity-ordered
  candidate list annotated with suspected existing issue numbers, is saved to
  `~/Downloads/code-scan-<project>.md`, and hands off to `grill-me` in a new session.
  It writes nothing inside the scanned repository, makes no tracker write, and
  invokes no other skill.

  `integrate-review` is removed from `docs/development/README.md`. It was never
  built and will not be; integration QA is done by hand, outside these skills.

  `to-tickets` now reads every open issue on the parent's board, builds one total
  order with the new tickets inserted, shows that complete order in its **existing**
  approval preview, and writes it back as the board's item position after
  publishing. A blocker always precedes what it blocks; existing issues keep their
  relative order unless an edge forces a move, and every such move is named.
  Setting Priority is no longer forbidden as ordering — order has no native source
  to drift from — but it is written as item position rather than a Priority field,
  and readiness labels, Status and Size remain forbidden.

  Existing installs must re-run `./scripts/relink.sh` to pick up `codebase-scan`.

- [#12](https://github.com/nathan115210/nathan-skills/pull/12) [`8914a08`](https://github.com/nathan115210/nathan-skills/commit/8914a082d3f6eea108f60f82583a45bcd69a041b) Thanks [@nathan115210](https://github.com/nathan115210)! - Add always-on shared communication preferences for Codex, Claude Code and agy; install with python3 scripts/instructions.py install. Remove duplicate style guidance from grill-me and version instruction changes.

- [#15](https://github.com/nathan115210/nathan-skills/pull/15) [`a0955a8`](https://github.com/nathan115210/nathan-skills/commit/a0955a8fa0a1827a70e4dc05d7a17eb8bbf35f14) Thanks [@nathan115210](https://github.com/nathan115210)! - Place to-tickets sub-issues on the GitHub Project the parent spec issue is already on, inherited rather than chosen or configured. Project fields and labels remain prohibited; placement never blocks the publish and is read back in verification. Adds a `project` scope check before the work and a rate-limit backoff rule at publish.

- [#17](https://github.com/nathan115210/nathan-skills/pull/17) [`46bdb97`](https://github.com/nathan115210/nathan-skills/commit/46bdb97f1c96449bfb1e3c14de790bb497401068) Thanks [@nathan115210](https://github.com/nathan115210)! - relink.sh now removes this clone's links for skills that no longer exist, so a renamed or removed skill no longer leaves a dangling link behind. Updating an existing install is `git pull` then `relink.sh`; running `unlink.sh` first is no longer needed, and the rename procedure loses its manual cleanup step. Only links this clone owns are removed — real directories and links pointing outside the clone are untouched, using the same ownership test as unlink.sh.

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

- [#39](https://github.com/nathan115210/nathan-skills/pull/39) [`dd456b1`](https://github.com/nathan115210/nathan-skills/commit/dd456b1f20d8aaf5e5b2d7efa275b0ecaac98078) Thanks [@nathan115210](https://github.com/nathan115210)! - Rename the `grill-me` skill to `nathan-grill-me`. In agy, `/grill-me` resolves to
  a command of the same name that is built into agy and never reads this skill, so the skill could not be invoked by name there. Everything that referred
  to the old name now uses the new one; the skill's behaviour is unchanged. Existing
  installs must re-run `./scripts/relink.sh`, which links `nathan-grill-me` and
  prunes the stale `grill-me` link, and invoke `/nathan-grill-me` from now on.

- [#39](https://github.com/nathan115210/nathan-skills/pull/39) [`dd456b1`](https://github.com/nathan115210/nathan-skills/commit/dd456b1f20d8aaf5e5b2d7efa275b0ecaac98078) Thanks [@nathan115210](https://github.com/nathan115210)! - `grill-me`, `codebase-scan` and `accessibility-review` now save their documents
  inside the project instead of `~/Downloads`: `.nathan-skills/prd/`,
  `.nathan-skills/code-scan/` and `.nathan-skills/accessibility-audit/`, each file
  named `<topic>-<YYYY-MM-DD>.md`. The first write creates the folder and a
  `.nathan-skills/.gitignore` containing `*`, so no tracked file changes. `grill-me`
  no longer asks you to confirm a filename and resumes an existing PRD by topic
  whatever its date; its PRD no longer carries an identity header. `to-spec` reads
  the PRD from `.nathan-skills/prd/` and no longer checks an identity line.
  `nathan-setup`'s project workflow block now says PRDs go in `.nathan-skills/prd/`
  (projects set up earlier keep the old wording until `nathan-setup` refreshes them).
  Existing files in `~/Downloads` are not migrated; move them by hand to keep using
  them.

- [#17](https://github.com/nathan115210/nathan-skills/pull/17) [`46bdb97`](https://github.com/nathan115210/nathan-skills/commit/46bdb97f1c96449bfb1e3c14de790bb497401068) Thanks [@nathan115210](https://github.com/nathan115210)! - `to-tickets` gains a second input mode, and `codebase-scan` stops forcing an
  interview before anything can be tracked.

  A `codebase-scan` findings list confirmed in the same session can now go
  straight into `to-tickets`. That path creates one tracking parent
  (`Codebase scan: <project> @ <revision>`) holding the report's identity header,
  scope line and not-covered declarations, then one child per finding — unmerged,
  unsubdivided, in the scan's own words and at the location it named. Every child
  carries a new canonical not-buildable statement, because a findings list has no
  seams and no test names; `grill-me` then `to-spec` on one issue is what makes it
  buildable. The spec path is unchanged, including its Seams/Acceptance Criteria
  gate, which the scan path skips.

  Two rules are relaxed on the scan path only: the destination Project is asked
  once about the tracking parent, since a just-created issue has no board to
  inherit from, and a ticket may carry the finding's file, line and revision.

  `codebase-scan` now ends by offering both exits — `to-tickets` here, or
  `grill-me` in a new session when which findings matter is itself the question —
  instead of mandating the second. It still makes no tracker write of its own.

- [#48](https://github.com/nathan115210/nathan-skills/pull/48) [`6bec314`](https://github.com/nathan115210/nathan-skills/commit/6bec314f63a780eb5a33fccd0da7d789b6ef52a9) Thanks [@nathan115210](https://github.com/nathan115210)! - The `.nathan-skills` save-folder protocol (project root, filename shape, self-ignoring `.gitignore`, symlink refusal, path announcement, write failures and the working-document disclaimer) is now stated once, in `nathan-grill-me/references/save-folder-protocol.md`. `nathan-grill-me` points to it through the runtime's skill catalogue and keeps only its own rules: the `prd` subfolder, the topic key, resume-by-topic and a creation date that never changes. Saving a PRD behaves as before. A new `scripts/test_save_protocol.py` checks the skill text; `codebase-scan` and `accessibility-review` are switched over in the changesets that follow.

- [#12](https://github.com/nathan115210/nathan-skills/pull/12) [`8914a08`](https://github.com/nathan115210/nathan-skills/commit/8914a082d3f6eea108f60f82583a45bcd69a041b) Thanks [@nathan115210](https://github.com/nathan115210)! - Stop creating nathan-setup-report.md; show setup results in conversation and remove the report helper command. Preserve local retry metadata and existing reports.

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

- [#11](https://github.com/nathan115210/nathan-skills/pull/11) [`c7d0a7e`](https://github.com/nathan115210/nathan-skills/commit/c7d0a7ebe56aa7be2af19d2ab5e5d35ec5f03b8c) Thanks [@nathan115210](https://github.com/nathan115210)! - Add dev for GitHub issue tickets, with task worktrees, allocated behavior tests, native dependency checks, and explicit verification status. Preserve to-tickets parent spec seams and integration obligations.

  Define an optional coordinator/developer handoff sharing the same implementation rules, including scoped review repairs and structured escalation, without requiring a native agent or fixed model.

- [#2](https://github.com/nathan115210/nathan-skills/pull/2) [`872f430`](https://github.com/nathan115210/nathan-skills/commit/872f4300334a988b8d9a1b9a2acfaa674c5e7ad7) Thanks [@nathan115210](https://github.com/nathan115210)! - Version the repository with changesets. `package.json` carries the version,
  `.changeset/` holds pending changes, and `CHANGELOG.md` is generated from them.
  A `Release` workflow on `master` opens a "chore: version skills" pull request
  and tags the commit once it merges.

### Patch Changes

- [#50](https://github.com/nathan115210/nathan-skills/pull/50) [`c016ad9`](https://github.com/nathan115210/nathan-skills/commit/c016ad9bc93bec90070eb1b27010b8f380bdb6f6) Thanks [@nathan115210](https://github.com/nathan115210)! - `accessibility-review` no longer restates the `.nathan-skills` save steps. It points to the shared save-folder protocol in `nathan-grill-me/references/` through the runtime's skill catalogue and keeps only its own rules: the `accessibility-audit` subfolder, the `<topic>` filename key, that a same-day re-review of the same topic replaces the file, that the user may decline the file, and the identity header and scope line it adds to the saved file. Saving a report behaves as before; `nathan-grill-me` must be installed, which `relink.sh` already does.

- [#59](https://github.com/nathan115210/nathan-skills/pull/59) [`8b0c03b`](https://github.com/nathan115210/nathan-skills/commit/8b0c03b11bb8d245ebe37052eaa1bbf1afba81d4) Thanks [@nathan115210](https://github.com/nathan115210)! - Run all unit test suites across scripts and skills in CI changeset check workflow

- [#49](https://github.com/nathan115210/nathan-skills/pull/49) [`a14b89c`](https://github.com/nathan115210/nathan-skills/commit/a14b89ce86ab9fe25fd1d495be8cfed6b5c79c39) Thanks [@nathan115210](https://github.com/nathan115210)! - `codebase-scan` no longer restates the `.nathan-skills` save steps. It points to the shared save-folder protocol in `nathan-grill-me/references/` through the runtime's skill catalogue and keeps only its own rules: the `code-scan` subfolder, the `<scope>` filename key, that a same-day rescan of the same scope replaces the file, and that the user may decline the file. Saving a report behaves as before; `nathan-grill-me` must be installed, which `relink.sh` already does.

- [#52](https://github.com/nathan115210/nathan-skills/pull/52) [`08496ce`](https://github.com/nathan115210/nathan-skills/commit/08496ce361ec2860380a3156c26241e166624a3c) Thanks [@nathan115210](https://github.com/nathan115210)! - `code-review` and `codebase-scan` no longer restate rules that `references/reviewer.md` already carries. Both read that file on every run, so the read-only enforcement disclaimer ("a role name is not enforcement; disclose a behavioural-only boundary") and "do not manufacture findings to look thorough" are now stated once there. `code-review` keeps the part that is its own — that it ships no hook and no command guard. `codebase-scan` also drops three paragraphs that restated its own coverage table and `references/coverage.md`: why the security axis is not churn-ranked, the weak-model rationale and the not-covered rationale. Both skills behave as before and neither has been re-run in any tool.

- [#17](https://github.com/nathan115210/nathan-skills/pull/17) [`46bdb97`](https://github.com/nathan115210/nathan-skills/commit/46bdb97f1c96449bfb1e3c14de790bb497401068) Thanks [@nathan115210](https://github.com/nathan115210)! - code-review no longer ships the inert `readonly-guard.md` command-guard
  prototype. Its warning is now stated directly in `SKILL.md`: the skill ships no
  hook and no command guard, read-only must be enforced outside the model, and a
  command allowlist is not that guarantee because it misses write operands and
  fails open on unknown payloads.

- [#57](https://github.com/nathan115210/nathan-skills/pull/57) [`09e1318`](https://github.com/nathan115210/nathan-skills/commit/09e13180d46a85f99f14c8505b363dcafdf2e2cc) Thanks [@nathan115210](https://github.com/nathan115210)! - Extract shared link-ownership and tool-directory definitions from `scripts/relink.sh` and `scripts/unlink.sh` into `scripts/lib/links.sh`.
  Both scripts source `scripts/lib/links.sh` with explicit readability guards and report missing library files on stderr before exiting with code 1.

- [#15](https://github.com/nathan115210/nathan-skills/pull/15) [`a0955a8`](https://github.com/nathan115210/nathan-skills/commit/a0955a8fa0a1827a70e4dc05d7a17eb8bbf35f14) Thanks [@nathan115210](https://github.com/nathan115210)! - Remind at to-spec's handoff that the spec issue must be on its GitHub Project before to-tickets runs, since to-tickets inherits the board from it. to-spec still places nothing itself — the spec issue's placement is the user's switch for the whole breakdown.

- [#4](https://github.com/nathan115210/nathan-skills/pull/4) [`b595fc1`](https://github.com/nathan115210/nathan-skills/commit/b595fc1bf119f15a39e27d6e81df6871b2020a43) Thanks [@nathan115210](https://github.com/nathan115210)! - Add portable code-review and accessibility-review skills for Claude Code,
  Codex and agy, with shared human-facing documentation and safeguards that keep
  raw runtime evidence out of the docs tree.

- [#61](https://github.com/nathan115210/nathan-skills/pull/61) [`2cb0aa0`](https://github.com/nathan115210/nathan-skills/commit/2cb0aa03a44e42ef42176606466ba395ab78c0f1) Thanks [@nathan115210](https://github.com/nathan115210)! - Remove dated prompt wording found by a prompt audit. code-review's reviewer
  discipline refers to a denied or blocked command instead of a guard the skill
  does not ship, and reviewer prompts ask for location, rule and consequence per
  finding instead of a 400-word cap. accessibility-review's persona template drops
  its fixed sentence counts. nathan-setup states that setup writes no report file
  without restating the removed report behaviour.

- [#51](https://github.com/nathan115210/nathan-skills/pull/51) [`9b9276b`](https://github.com/nathan115210/nathan-skills/commit/9b9276b5adf51a8d54a14e7e1547ac28a920cbb2) Thanks [@nathan115210](https://github.com/nathan115210)! - `scripts/test_save_protocol.py` now also checks, across `nathan-grill-me`, `codebase-scan` and `accessibility-review`, that each names its own subfolder, filename key and replace-or-resume rule, and that none reaches the shared save-folder protocol through a cross-skill relative path. The docs pages and the development README record that saving through the shared protocol is untested at runtime.

- [#52](https://github.com/nathan115210/nathan-skills/pull/52) [`08496ce`](https://github.com/nathan115210/nathan-skills/commit/08496ce361ec2860380a3156c26241e166624a3c) Thanks [@nathan115210](https://github.com/nathan115210)! - Follow-ups to the shared save-folder protocol. `nathan-grill-me`, `codebase-scan` and `accessibility-review` now say what to do when the protocol file cannot be found (present the result unsaved, never save from memory), since that rule could not fire from inside the missing file. The protocol constrains the filename key to lowercase letters, digits and hyphens. `scripts/test_save_protocol.py` now scans every skill file for restated steps, covers both additions, and runs in the `Changeset` workflow. The earlier changesets no longer claim the other skills still carry their own copies.

- [#11](https://github.com/nathan115210/nathan-skills/pull/11) [`c7d0a7e`](https://github.com/nathan115210/nathan-skills/commit/c7d0a7ebe56aa7be2af19d2ab5e5d35ec5f03b8c) Thanks [@nathan115210](https://github.com/nathan115210)! - Fix dev readiness to check native blockers for every issue and reject already-split specs as standalone tasks. Resolve explicit starting-commit conflicts before reusing task branches or worktrees, while preserving normal resume progress.

  Classify approved expand–contract intermediate failures as implemented-unverified, retain actual failed check outcomes, and keep unexpected regressions blocking. Carry the resolved baseline and exception evidence through the developer handoff and synchronize the user guide.

- [#15](https://github.com/nathan115210/nathan-skills/pull/15) [`a0955a8`](https://github.com/nathan115210/nathan-skills/commit/a0955a8fa0a1827a70e4dc05d7a17eb8bbf35f14) Thanks [@nathan115210](https://github.com/nathan115210)! - Print a ready-to-paste `gh issue edit <numbers> --milestone` line at to-tickets' handoff, with the new issue numbers filled in. The skill still sets no milestone and does not ask which one — assigning a delivery batch stays the user's decision.

- [#39](https://github.com/nathan115210/nathan-skills/pull/39) [`dd456b1`](https://github.com/nathan115210/nathan-skills/commit/dd456b1f20d8aaf5e5b2d7efa275b0ecaac98078) Thanks [@nathan115210](https://github.com/nathan115210)! - `to-spec` may now list file paths, but only in one optional line,
  `Code locations (as of <short revision>)`, so debugging has a starting point and a
  stale path is visibly tied to the revision it described. Paths stay out of every
  other section, and code snippets are still not allowed. `to-tickets` is unchanged.

- [#39](https://github.com/nathan115210/nathan-skills/pull/39) [`dd456b1`](https://github.com/nathan115210/nathan-skills/commit/dd456b1f20d8aaf5e5b2d7efa275b0ecaac98078) Thanks [@nathan115210](https://github.com/nathan115210)! - `to-spec` now keeps each acceptance criterion's concrete values (the literal
  outputs, amounts and messages) instead of paraphrasing, and carries a test
  name's precondition, expected result and observable under it when the PRD states
  them. `to-tickets` copies test-name lines and those detail lines character for
  character. Found in an agy run where a spec dropped `HI ANN` and `HI WORLD` into
  "prints the greeting in uppercase" and the template had no place for the rest.
  Also removes a stale `to-spec` check that a PRD's identity line matches the
  project, which no longer exists now that the PRD lives in the project.

- [#15](https://github.com/nathan115210/nathan-skills/pull/15) [`a0955a8`](https://github.com/nathan115210/nathan-skills/commit/a0955a8fa0a1827a70e4dc05d7a17eb8bbf35f14) Thanks [@nathan115210](https://github.com/nathan115210)! - Make to-tickets preview complete issue bodies before approval, publish the approved rendering unchanged, and verify titles, bodies, test allocation, and native relations after creation.

- [#54](https://github.com/nathan115210/nathan-skills/pull/54) [`e7fe1e9`](https://github.com/nathan115210/nathan-skills/commit/e7fe1e9b70df945351308c259151451f607ca3b6) Thanks [@nathan115210](https://github.com/nathan115210)! - The shared save-folder protocol gains a reader-side section — where the folder is, the `<key>-<YYYY-MM-DD>.md` shape, that the files are git-ignored and that they belong to one checkout — for a skill opening a file it did not write, and its opening paragraph widens from saving skills to cover a reader too. `to-spec` stops restating the filename shape and the project-root definition and points at that section through the runtime's skill catalogue, keeping only its own rules: the `prd` subfolder, latest trailing date wins, ask when several topics could be meant, say which file it took, and ask for a path when the folder is missing or empty. The read is conditional — only on the branch where no path was handed over and `to-spec` has to locate the PRD itself — and a missing protocol does not stop it: it lists the folder anyway, says the protocol was unavailable and names the file it took. Nothing changes about what any skill does with a saved file.

- [#52](https://github.com/nathan115210/nathan-skills/pull/52) [`08496ce`](https://github.com/nathan115210/nathan-skills/commit/08496ce361ec2860380a3156c26241e166624a3c) Thanks [@nathan115210](https://github.com/nathan115210)! - `to-tickets` `SKILL.md` is about 27% shorter (7,008 to 5,098 words). The exact `gh` commands and their failure modes (writable check, split check, board reads, publish by `id`, position writes, read-back and `diff`) moved to a new `references/github-procedures.md`; `SKILL.md` keeps every decision, approval and verification rule. The intended behaviour is unchanged, but the trimmed skill has not been run in any tool.

- [#17](https://github.com/nathan115210/nathan-skills/pull/17) [`46bdb97`](https://github.com/nathan115210/nathan-skills/commit/46bdb97f1c96449bfb1e3c14de790bb497401068) Thanks [@nathan115210](https://github.com/nathan115210)! - Clarify `to-tickets` body read-back in step 8 and its docs page: keep the valid
  `gh api --jq '.body'` form, and note that `--jq` appends a trailing newline of
  its own, which otherwise makes every rendered ticket body diff as mismatched.
