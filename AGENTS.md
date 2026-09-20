# nathan-skills

The single source of truth for Nathan's personal AI skills. Every skill lives
here exactly once; each AI tool's skills folder holds a **symlink** back into
this repo, so editing a file here updates it for all tools at once.

## Layout

```
skills/
  development/
    <skill-name>/SKILL.md   current development workflow skills
scripts/
  relink.sh                global skill-linking script
  unlink.sh                remove this clone’s global skill links
  check_changeset.py       guards the changeset rules, in CI and locally
docs/
  <category>/README.md     workflow overview and implementation status
  <category>/<skill>.md    human-facing skill guide
.changeset/
  <name>.md                pending change, folded into the next release
CONTEXT.md                shared vocabulary and document responsibilities
CHANGELOG.md              generated release history — never edit by hand
```

Skill-specific helpers stay inside their skill’s `scripts/` folder. Global scripts
live in the root `scripts/` folder. Categories organize the source repository;
tool skill directories remain flat. Skill folder names must be globally unique.
Keep skill names, shared instructions, inputs and outcomes consistent across
Claude Code, Codex and agy. Provider-specific metadata/adapters must not fork
the workflow; verify runtime differences rather than claiming identical execution.
`scripts/relink.sh` discovers skill roots under `skills/` and stops at each `SKILL.md`.

Linked into `~/.claude/skills` (Claude Code), `~/.codex/skills` (Codex) and
`~/.gemini/config/skills` (agy / Antigravity CLI). **agy reads `~/.gemini/config/`,
not `~/.gemini/`** — a link in `~/.gemini/skills` is invisible to it.
Gemini CLI and Copilot CLI are no longer managed.

## Context and documentation

Global response style lives only in `instructions/communication.md`, installed
with `python3 scripts/instructions.py install`. Do not duplicate these rules in
individual skills. Keep skill-specific questioning and artifact requirements in
their skills. See `docs/communication.md` for loading and verification limits.

Read [CONTEXT.md](./CONTEXT.md) when changing workflow terminology, skill
boundaries, or documentation. It defines shared terms and points to the relevant
sources; it does not duplicate the workflow or its current implementation status.

Use [README.md](./README.md) for installation and the repository entry point,
and [docs/development/README.md](./docs/development/README.md) for the development
workflow. A skill's `SKILL.md` defines its execution requirements; its docs page
explains their use. Resolve documentation drift against those requirements and
the user's confirmed decisions, rather than changing a skill to match stale docs.
Keep public context and guides self-contained without copying private project
details or personal history from the local decision record.

## Rules

- **After adding a skill folder, run `./scripts/relink.sh`.** A new skill is invisible
  to every tool until you do. This is the step that gets forgotten.
- **Run `relink.sh` from the main checkout, not a `git worktree`.** It derives the
  repository to link from its own location, so a worktree run would repoint every
  tool at that branch. It refuses and links nothing; `--force` overrides when that
  is genuinely the intent.
- The `name:` field in a skill's YAML frontmatter **must equal its folder name**.
  Renaming means changing both.
- Editing an existing skill needs no relink — the symlinks already point here.
- **Every skill has a docs page at `docs/<category>/<skill-name>.md`, and the
  category has a `README.md` overview.** Create or re-sync the page whenever a
  skill is added, renamed (move the file too), or changes behaviour. The page is
  **not** a copy of `SKILL.md`: `SKILL.md` tells the model what state to reach,
  the page tells a person when to reach for it, what it does not do, and what a
  bad run looks like. Keep the chain diagram and the built/unbuilt status in the
  category `README.md` only — repeating either per page is a second copy that
  will drift. Verification results belong in "It's working if" and "Known
  limitations"; unverified is stated as unverified.
- **Runtime claims need runtime evidence, but raw evidence stays outside this
  repository by default.** Keep commands, stdout/stderr, fixtures, schemas and
  generated test artifacts in a temporary directory or `~/Downloads`. The docs
  contain only the durable human-facing summary: tool/version, tested scenario,
  passed/failed/untested status, material limitation, and an external artifact
  path only when the user wants to retain it. Do not create `verification/`,
  `evidence/`, `fixtures/`, `logs/` or `test-results/` under `docs/`, and do not
  add raw `.jsonl` or `.log` files there, unless the user explicitly asks to
  version those artifacts. Run `python3 -m unittest scripts/test_docs.py` after
  changing docs. Parsing YAML, finding a symlink, or a model saying it succeeded
  is not runtime verification. An environment or usage-limit failure does not
  prove a skill failed or passed.
- **Every change a tool runs needs a changeset.** Run `npm run changeset` in the
  same change that adds, renames, or alters a skill, global script, or file in
  `instructions/`. No
  changeset means the change ships unversioned and unmentioned in the changelog.
  Docs-only edits that change nothing a tool runs need none.
- **Before 1.0, never pick `major`.** Changesets does not soften a major bump on
  a `0.x` version — one major changeset takes `0.1.0` straight to `1.0.0`
  (verified on changesets 2.31.1). Record breaking changes as **minor** until the
  development workflow is finished; `1.0.0` is a deliberate release, not a side
  effect of a rename.
- **Run `python3 scripts/check_changeset.py` before opening a pull request.** It
  enforces both rules above and is the same check CI runs, so a red build here
  is a red build there. `--base` picks the branch being merged into.
- **Never hand-edit `CHANGELOG.md` or the `version` in `package.json`.** Both are
  generated by `changeset version`; editing them makes the next release conflict.
- **Do not commit or stage unless explicitly asked.** Staging is the user's
  step: it is how they read a diff before it becomes a commit, and an agent that
  stages has already made that choice for them. Leave the work in the working
  tree, unstaged, and say what is pending.

## Versioning and releases

The repository is versioned as a whole with [changesets](https://github.com/changesets/changesets).
`package.json` holds the version; `CHANGELOG.md` is generated from the files in
`.changeset/`. Nothing is published to npm — the package is `private`, and a
release is a version bump, a changelog entry and a git tag.

1. Make the change, then `npm run changeset` and pick the bump:
   **patch** for wording, docs or a fix inside a skill; **minor** for a new skill,
   changed inputs/outcomes, **or anything that breaks an existing setup** (a
   rename, a removed skill, a relink existing installs must re-run). `major` is
   off the table until 1.0 — see the rule above.
2. Commit the generated `.changeset/<name>.md` alongside the change. The
   `Changeset` workflow fails a pull request that changes `skills/` or
   `scripts/` without one; a change no tool runs takes the **skip-changeset**
   label instead.
3. On merge to `master`, the `Release` workflow opens a **chore: version skills**
   pull request holding the version bump and changelog entry.
4. Merging that pull request tags the release (`npx changeset tag`).

Bump for the effect on someone whose tools already link to this repo, not for
the size of the diff. The version only ever moves one step per release, however
many changesets have piled up: ten patches make one patch bump, and the highest
pending level wins. Every entry still appears in the changelog.

`1.0.0` is released by hand, once the development workflow is complete and the
way other people install this is settled. That release is the one pull request
that carries a `major` changeset and the **allow-major** label; without the
label the guard rejects it. At the same time the pre-1.0 notice at the top of
`README.md` comes off.

## Renaming a skill

1. `git mv skills/<category>/old-name skills/<category>/new-name`
2. Update `name:` in the moved skill’s `SKILL.md` to match
3. Move `docs/<category>/old-name.md` to the new name and update references in
   the docs, category overview, and repository README where present
4. Delete the stale `old-name` symlink from all three tool folders
5. `./scripts/relink.sh`
6. `npm run changeset` — a rename breaks existing setups, so it is **minor**
   before 1.0 and `major` after; say both the old and the new name

## Do not touch

- `~/.codex/skills/.system/` — Codex built-ins.
- The 13 Cloudflare skills (`cloudflare`, `wrangler`, `workers-best-practices`,
  `turnstile-spin`, `sandbox-*`, `agents-sdk`, `durable-objects`, `web-perf`,
  `cloudflare-one*`, `cloudflare-email-service`) present as real directories in
  each tool folder. They are a distributed pack, not managed by this repo.
- `~/.gemini/skills/` and `~/.copilot/skills/` — no longer managed. They still
  hold the Cloudflare pack; leave it alone. (Note `~/.gemini/skills` is the old
  Gemini CLI path, so that copy of the pack is invisible to agy — not our
  problem to fix.)
- **Every other `git worktree` of this repository.** Work only in the checkout
  the session started in. Other worktrees hold parallel, often uncommitted work
  on their own branches, and nothing there is yours to read for context, edit,
  merge, rebase, remove, or relink from. If a problem's cause or fix appears to
  live in another worktree, say so and stop — the user decides what happens in
  it. `git worktree list` is a fact worth reporting; it is not an invitation.

`scripts/relink.sh` already refuses to overwrite anything it did not create — it warns,
skips, and exits non-zero. Never work around that guard by deleting the target.

## Uninstall or move

Run `./scripts/unlink.sh --dry-run` to preview, then `./scripts/unlink.sh` to
remove this clone's links from all three managed tool folders. Only confirmed
in-clone symlink targets are removed, including stale links. Real directories,
foreign or uncertain links, project configuration and the clone are preserved.
Do not remove targets based on a matching skill name alone.

Unlink before deleting or moving the clone; after moving, run `relink.sh` from
the new location. Already-moved clones require manual inspection of old links.
See [the uninstall guide](./docs/development/README.md#uninstall) for output,
verification and limitations. Test link-management changes with
`python3 -m unittest scripts/test_relink.py scripts/test_unlink.py` using isolated
homes; never verify uninstall by removing the user's active skill links.

## New machine

Clone anywhere, run `./scripts/relink.sh`. It derives every path from `$HOME` and its
own location, so no editing is needed.

## Note for agents

`CLAUDE.md` and `GEMINI.md` are symlinks to this file. Keep the content
tool-neutral — one file is read by Claude Code, Codex and agy alike (Codex and
agy both read `AGENTS.md` natively; Claude Code needs `CLAUDE.md`). `GEMINI.md`
is now redundant but harmless — it is a symlink, so it cannot drift.
Tool-specific config belongs in that tool's own settings file.
