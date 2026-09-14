# nathan-setup

[SKILL.md](../../skills/development/nathan-setup/SKILL.md)

## What it does

Connects one project to this workflow, across every tool you have installed at
once. It reads the project as it already is — existing instruction files,
README, manifests, CI, validation commands — and writes only what is missing,
into a managed block in the project's root `AGENTS.md` that Claude Code, Codex
and agy all read.

It never replaces what is already there. Existing rules and human edits are
preserved; a real conflict is brought to you rather than resolved silently.

## When to reach for it

You type it. It will not fire on its own.

Run it **once per project**, before using any other skill in this workflow — for
a new project and for an existing one being connected for the first time.
Linking skills globally (`scripts/relink.sh`) makes the skills visible to your
tools; it does not tell any tool anything about *this* project. That is what
this step is for.

Run it again when the project's rules or validation commands change materially,
or when you install a tool that was missing the first time. It is a refresh, not
a per-task step.

## Prerequisites

- Python 3 (macOS or Linux). The helper uses only the standard library.
- At least one of Claude Code, Codex or agy installed. Missing tools are skipped,
  not treated as failures.
- The skills themselves linked — run `./scripts/relink.sh` in this repository
  first.

## Four steps, and why they are separate

1. **Inspect** — inventory what exists: parent instruction files up to the git
   root, nested ones, the README, manifests, CI. Scan limits are reported as
   *unresolved scope*, never as proof that nothing is there.
2. **Write** — draft only the missing, *verified* content. Always with
   `--dry-run` first, which shows a diff without touching anything. The helper
   checks both the whole-file hash and the previous managed block, so a human
   edit made since the last run blocks the write until you have read the diff.
3. **Connect** — link each tool's entry point to the shared `AGENTS.md`. Codex
   and agy read it natively; Claude Code gets a relative `CLAUDE.md` symlink, or
   a reviewed `@AGENTS.md` import when it already has its own file.
4. **Verify** — ask each installed tool a real question about this project's
   rules and check the answer locally.

Step 4 is separate from step 3 on purpose. **A structural connection is not
proof that anything works.** A symlink can exist while the tool cannot run,
is not authenticated, or reads a different directory than you assume.

## Verification means one specific thing

The probe asks each tool to quote something only a tool that actually read this
project's rules could quote. What that establishes is **instruction and skill
discovery** — nothing more.

It does **not** establish that the three tools reason alike, that development
hooks are enforcing anything, or that the project's own validation commands run.
Those are separate claims and the report keeps them separate.

Results are three-state, and `pending` is never a pass:

| State | Means |
| --- | --- |
| `passed` | The tool answered from this project's rules, with evidence |
| `failed` | It answered, and the answer does not establish discovery |
| `pending` | It could not be asked — no CLI, not authenticated, timed out, quota exhausted |

One tool failing does not block the others. The project is marked **partially
ready**, with the failing tool and the reason named.

## Common questions

**It says my project is "partially ready". Is that broken?**
Usually not. It means at least one tool verified and at least one did not. The
report names which and why. A quota limit or a missing binary is an environment
problem, and it is deliberately recorded as `pending` rather than dressed up as
either success or failure.

**Codex shows `pending` and I know it is installed.**
The `codex` binary may not be on your `PATH` — on a Mac with the desktop app it
lives inside `/Applications/ChatGPT.app/Contents/Resources/`. Detection uses
`PATH`, so it records `unconfirmed` rather than guessing. Point `--tool codex` at
the real binary, or create a shim, then re-run with `--retry`.

**Why did it refuse to write my `AGENTS.md`?**
Because the file changed since it last wrote there. That is the guard working:
it means a human edited the block, or a block exists that it does not own.
Read the diff and merge. `--accept-edited-block` exists for after you have done
that review — never as a way to silence the refusal.

**Can it undo what it did?**
Yes: `remove` deletes only an *unchanged, owned* block and leaves surrounding
human text alone. A block you have edited is refused rather than force-deleted.
Report history is always preserved.

**Will it install the development gates / hooks?**
No, because they do not exist yet. It reports them as unavailable. It will never
install a placeholder hook — a gate that looks installed but does not fire is
worse than no gate.

## It's working if

- The dry-run diff shows only content you recognise as missing, and your own
  rules are untouched in it.
- After `connect`, `git status` in the project shows the instruction file and
  nothing else — no stray state directory (`.nathan-setup/` ignores itself).
- The verification evidence quotes *your* project's wording back at you. Generic
  plausible-sounding answers mean the tool did not actually read the file.
- Tools it cannot reach are `pending` with a stated reason, not silently absent.

## Known limitations

- Verified scope is instruction and skill discovery only. Hook enforcement,
  identical model behaviour, and runnable project validation are all unverified.
- agy must be invoked with `--add-dir PROJECT`; without it, it does not treat the
  project as its workspace and can answer from a previous session's leftovers.
- In headless mode a tool may auto-deny a permission prompt and return an empty
  answer. That is recorded as `pending`, not as a failure of the skill.
- Verified on macOS only.

## Where it fits

```
nathan-setup → grill-me → to-spec → to-tickets ✗ → dev ✗ → review ✗
```

Nothing comes before it. It is the project's entry into
[the workflow](./README.md); everything downstream assumes it has run.
