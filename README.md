# nathan-skills

> **Pre-1.0 — not ready to depend on.** The development workflow is unfinished:
> ticket splitting, implementation and QA do not exist yet. Code and
> accessibility review can be used independently. Until there is a `1.0.0`
> release, skill names, their inputs and their outcomes can change without a
> deprecation path, and the way other people install this is still undecided —
> `relink.sh` is built for the author's own machine. Read it, copy from it, open
> an issue; just don't wire it into anything you rely on yet.

One source of truth for a personal set of AI coding skills, shared across
Claude Code, Codex and agy (Antigravity CLI).

Every skill lives in this repository exactly once. Each tool's skills folder
holds a **symlink** back here, so editing a file updates it for all three tools
at the same time — there is no copy to keep in sync, and no tool that quietly
runs an older version.

```bash
git clone https://github.com/nathan115210/nathan-skills
cd nathan-skills
./scripts/relink.sh
```

That is the whole install. `relink.sh` derives every path from `$HOME` and its
own location, so nothing needs editing on a new machine, and it is safe to run
again at any time. Rerun it after adding a skill; editing one needs no rerun.

It never overwrites anything it did not create — it warns, skips that name, and
exits non-zero. A skipped name means the tools are running some other copy of
that skill, so the exit code is worth reading. **[Installing, and checking it
took →](./docs/development/README.md#install-and-check-it-took)**

Keep the clone where it is: the links are absolute paths. If you move it, rerun
`relink.sh` and delete the links left pointing at the old location.

## Workflows

Skills here belong to a workflow — a chain whose steps hand over an artifact,
not a toolbox of unrelated commands. Each workflow has its own guide.

**[The development workflow →](./docs/development/README.md)** — idea to
reviewed and verified: the chain, where to start, and a page per skill covering
when to reach for it and what it does not do.

Focused review skills can also be used independently:

- [code-review](./docs/development/code-review.md) reviews a specified change
  against repository standards, its spec and applicable accessibility criteria.
- [accessibility-review](./docs/development/accessibility-review.md) reviews a
  supplied design, local UI code or both for accessibility barriers.

## Conventions

- Skills are invoked explicitly, never auto-invoked, and never chained inside
  one session.
- `AGENTS.md` is the real file; `CLAUDE.md` and `GEMINI.md` are symlinks to it,
  so the operating rules cannot drift between tools.
- Adding, renaming or changing a skill means running `./scripts/relink.sh` and
  writing a changeset. [`AGENTS.md`](./AGENTS.md) has the full rules.

## Versioning

Versioned as a whole with
[changesets](https://github.com/changesets/changesets) — `npm run changeset`
describes a change, [`CHANGELOG.md`](./CHANGELOG.md) is generated from those,
and a release is a version bump and a git tag. Nothing is published to npm.

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
