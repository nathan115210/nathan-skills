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
docs/
  <category>/README.md     workflow overview and implementation status
  <category>/<skill>.md    human-facing skill guide
CONTEXT.md                shared vocabulary and document responsibilities
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
- **Runtime claims need runtime evidence.** Record the tool/version, tested
  scenario, actual command and raw output in the verification record; summarize
  only that coverage in the docs. Separate expected behaviour from observed
  results, and distinguish passed, failed and untested checks. Parsing YAML,
  finding a symlink, or a model saying it succeeded is not runtime verification.
  An environment or usage-limit failure does not prove a skill failed or passed.
- **Do not commit unless explicitly asked.** Leave work staged and say what's
  pending.

## Renaming a skill

1. `git mv skills/<category>/old-name skills/<category>/new-name`
2. Update `name:` in the moved skill’s `SKILL.md` to match
3. Move `docs/<category>/old-name.md` to the new name and update references in
   the docs, category overview, and repository README where present
4. Delete the stale `old-name` symlink from all three tool folders
5. `./scripts/relink.sh`

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

`scripts/relink.sh` already refuses to overwrite anything it did not create — it warns,
skips, and exits non-zero. Never work around that guard by deleting the target.

## New machine

Clone anywhere, run `./scripts/relink.sh`. It derives every path from `$HOME` and its
own location, so no editing is needed.

## Note for agents

`CLAUDE.md` and `GEMINI.md` are symlinks to this file. Keep the content
tool-neutral — one file is read by Claude Code, Codex and agy alike (Codex and
agy both read `AGENTS.md` natively; Claude Code needs `CLAUDE.md`). `GEMINI.md`
is now redundant but harmless — it is a symlink, so it cannot drift.
Tool-specific config belongs in that tool's own settings file.
