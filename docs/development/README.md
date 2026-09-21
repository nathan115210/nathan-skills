# The development workflow

A chain of skills for taking one piece of work from "I have an idea" to
"reviewed and verified". Each step is started by hand, in its own session, and
hands over an **artifact** — a file, then an issue, then a branch — never a
conversation.

That constraint is the whole design. A planning session ends with its context
spent and partly compacted, and compaction silently drops the exact wording you
meant to carry forward. So nothing important is allowed to live only in a
session.

## Install, and check it took

From the repository root:

```bash
cd ~/dev/nathan-skills   # wherever the clone lives
./scripts/relink.sh
python3 scripts/instructions.py install
```

`./` means "the file at this path", not a command on your `PATH` — the leading
dot is required. The script derives every path from `$HOME` and its own
location, and is safe to run again at any time.

Run it after **adding a skill folder** or **setting up a new machine**. Editing
an existing skill needs no rerun: the tools already point at these files, so a
save is live everywhere at once.

**Updating a clone is `git pull`, then `relink.sh`** — see
[Update](../../README.md#update). The same run links what is new and prunes this
clone's links for skills that no longer exist, so a rename leaves nothing behind.
Verified 2026-09-21 in an isolated `HOME`: a renamed skill and a removed skill
each left the tool folders holding exactly the current set with no dangling
links, while a real directory, a link into another source, and a dangling link
pointing outside the clone were all left untouched. Covered by
`scripts/test_relink.py`.

### Reading the output

```
  link  /Users/you/.claude/skills/nathan-grill-me
  SKIP  /Users/you/.claude/skills/code-review -> symlink points outside this repo (...)

central: /Users/you/dev/nathan-skills
linked: 9   pruned: 0   skipped: 6
```

| Line | Means |
| --- | --- |
| `link` | Installed. Every skill is relinked on every run, so these always appear. |
| `prune` | A link this clone created whose skill no longer exists — left by a rename or a removal — has been removed. |
| `SKIP` | Something already holds that name and this script did not create it. Nothing was touched. |
| `exit 1` | At least one `SKIP`. Not a crash — the signal that something did not install. |
| `ERROR` | Refused before touching anything. The only cause today is running it from a linked git worktree — see below. |
| `WARN` | Linking from a worktree on purpose (`--force`). |

**A `SKIP` means the tools are running someone else's copy of that skill.** The
name is taken, so your version never gets linked. Read the path in the message:
it says what owns the name. Either it is a real directory that is not managed
here (the Cloudflare pack), or it is a stale link from another clone or
worktree — in which case delete just that link and rerun:

```bash
rm ~/.claude/skills/<name> ~/.codex/skills/<name> ~/.gemini/config/skills/<name>
./scripts/relink.sh
```

Never make the script overwrite a target instead. It refuses by design, and that
refusal is the only thing standing between a rerun and someone else's work.

### Run it from the main checkout, not a worktree

`relink.sh` works out which repository to link from **its own location**. Run it
inside a linked `git worktree` and every tool ends up pointing at that branch's
skills — the links are valid, nothing looks wrong, and the tools quietly run
that branch instead of your main checkout, including versions of a skill that
were superseded there.

It now refuses, naming both paths, and links nothing:

```
ERROR relink.sh is running from a linked git worktree, not the main checkout.
      worktree: /Users/you/dev/nathan-skills-some-branch (branch some-branch)
      main:     /Users/you/dev/nathan-skills
```

Run it from the main checkout instead. `--force` overrides the refusal when you
genuinely want every tool to run a worktree's version — useful for trying a
skill out before merging it, and worth undoing afterwards by relinking from the
main checkout. `--list` is read-only and is never blocked.

A worktree checks out its own copy of `scripts/relink.sh`, so the refusal only
exists in worktrees whose branch already contains it. An older worktree will
still link happily — the guard stops the next one, not the ones already sitting
on your disk.

What such a run can actually take is narrower than it sounds. A link that
already points at your main checkout is **protected**: the script sees a target
outside its own root, prints `SKIP`, and exits non-zero. Only a **name nothing
has claimed yet** gets captured — which in practice means a skill that is new on
that branch. That is exactly how it happens: a branch adds a skill, a relink run
inside its worktree claims the name first, and from then on the main checkout
cannot take it back on its own, because the name is no longer free and `SKIP` is
the script refusing to overwrite work it did not create. Delete that one link
and relink from the main checkout.

### Confirming what a tool will actually run

```bash
readlink ~/.claude/skills/nathan-grill-me
```

The answer must be a path inside this repository. If it points anywhere else,
that other copy is what runs — and an edit here changes nothing. Check all three
tools, since they can disagree:

```bash
for d in ~/.claude/skills ~/.codex/skills ~/.gemini/config/skills; do
  readlink "$d/nathan-grill-me"
done
```

agy reads `~/.gemini/config/skills`, not `~/.gemini/skills`. A link in the
second is invisible to it.

The last check is the tool itself: type `/nathan-grill-me` and see whether it offers
the skill. A link can be perfect while the frontmatter keeps the tool from
loading it — a skill's `name:` must equal its folder name.

Global response style is installed separately through the
[communication preferences](../communication.md). It applies without invoking
any skill; skill discovery alone does not install it.

## Uninstall

Run from the clone you want to disconnect:

```bash
./scripts/unlink.sh --dry-run
./scripts/unlink.sh
python3 scripts/instructions.py remove --dry-run
python3 scripts/instructions.py remove
```

Both commands inspect direct symlinks in `~/.claude/skills`, `~/.codex/skills`
and `~/.gemini/config/skills`. They do not recurse into installed directories.
The preview makes no changes. The actual run removes links whose targets can
be confirmed inside this clone, including dangling links to removed skills;
it does not depend on the current skill catalog.

| Output | Meaning |
| --- | --- |
| `WOULD REMOVE` | A link the preview would remove. |
| `REMOVE` | A link was removed; its source is still in the clone. |
| `KEEP` | A link points elsewhere or its ownership is uncertain. Inspect it if you expected it to be removed. |
| `FAIL` / nonzero exit | Removal failed, or the command arguments were invalid. |

Kept links are expected when other skill collections are installed and do not
cause failure. Real files and directories are preserved without being listed.
Missing tool directories are left absent. Repeating uninstall is safe; run
`./scripts/relink.sh` to reinstall.

### What remains

The clone, Codex built-ins, Cloudflare directories, and links from other sources
remain. `~/.gemini/skills` and `~/.copilot/skills` are outside the managed scope.
Project rules or configuration created by `nathan-setup`, and artifacts produced
by skills, remain too: global uninstall does not undo project setup. For project
cleanup, see [nathan-setup’s remove behaviour](./nathan-setup.md).

Unlink before deleting or moving the clone. After moving it, reinstall from the
new location. If it has already moved or disappeared, inspect the old links
with `readlink` and remove only those you can confirm belong to the old clone;
the new location cannot claim them by skill name alone.

### It's working if

The removal summary matches the preview and confirmed links are gone while
source files remain. Isolated script tests passed on macOS with Bash 3.2.57:
install, preview, uninstall, repeat, reinstall, stale and relative links,
foreign and ambiguous targets, missing tool directories, invalid arguments,
and a moved clone. These checks exercise filesystem behaviour, not skill
execution inside Claude Code, Codex or agy.

### Known limitations

There is no per-tool uninstall option. Ambiguous dangling targets containing
path traversal or symlink ancestors are kept for manual inspection. Targets
outside the current clone, including old absolute paths after a move, are kept.
Refreshing skills already loaded into a running tool session is unverified;
use a fresh session to check discovery after uninstall.

## The chain

```
nathan-setup ─── once per project, before anything else
      │
      ▼
  nathan-grill-me ─► .nathan-skills/prd/<topic>-<date>.md
      │                        │
      ▼                        ▼
   to-spec ──────────────► one spec issue  (+ the test seams, chosen once)
      │
      ▼
  to-tickets ──────► sub-issues + blocking relations
      │
      ▼
     dev ────────────► a task worktree + verification status
      │
      └──► code-review ──► findings per axis → your call
```

| Step | Skill | Hands over | Built |
| --- | --- | --- | --- |
| Connect a project | [`nathan-setup`](./nathan-setup.md) | Project rules all three tools read | ✅ |
| Decide what to build | [`nathan-grill-me`](./nathan-grill-me.md) | A topic PRD in `.nathan-skills/prd/` | ✅ |
| Write it down once | [`to-spec`](./to-spec.md) | One spec issue, and the test seams | ✅ |
| Split it | [`to-tickets`](./to-tickets.md) | Sub-issues and blocking relations | ✅ |
| Build it | [`dev`](./dev.md) | A task worktree and verification status | ✅ |
| Review it | [`code-review`](./code-review.md) | Separate Standards, Spec and optional Accessibility findings | ✅ |

`to-tickets` hands buildable issues to `dev`; missing criteria still block
implementation. It also writes the board's order, so the chain ends where it
began: the next thing to build is the top of the board.

The chain has no QA step, and no step is planned. Integration QA is done by
hand, outside these skills.

## Where documents are saved

Three skills leave a document behind. They all save it inside the project, in a
folder git ignores, so nothing collides with another project's files:

```
<project root>/.nathan-skills/
  .gitignore                     contains *
  prd/                           nathan-grill-me              <topic>-<YYYY-MM-DD>.md
  code-scan/                     codebase-scan         <scope>-<YYYY-MM-DD>.md
  accessibility-audit/           accessibility-review  <topic>-<YYYY-MM-DD>.md
```

- **Self-ignoring.** The first write creates the folder and a `.gitignore`
  containing `*`, so no tracked file changes. An existing `.gitignore` is never
  overwritten, and a symlinked `.nathan-skills` is refused.
- **Shared steps.** The steps above are written once, in `nathan-grill-me`'s
  `save-folder-protocol.md`. `nathan-grill-me` and `codebase-scan` point to it; each
  states only its own subfolder, filename key and replace-or-resume rule.
  `accessibility-review` still carries its own copy.
- **Name.** The topic comes first, then the creation date in local time. A later
  run on the same topic reuses the existing file whatever its date; `to-spec` takes
  the latest date when one topic has several files.
- **One checkout only.** Another worktree or a fresh clone does not have these
  files, and they are not backed up with the project. Copy one across by hand if
  you plan in one checkout and specify in another.
- **No migration.** Files an earlier version wrote to `~/Downloads` are not moved.
  Copy one into the matching folder to keep using it.
- **Runtime status.** Checked on agy only, with one small scenario each:
  `nathan-grill-me` (early-end save), `to-spec` (finding that PRD) and
  `codebase-scan` (saving its report). `to-spec` (publishing) and `to-tickets`
  (sub-issues and blocking) were then run end to end against a private scratch
  repository. `dev` and `code-review` were run on a scratch ticket. The first time, `dev`
  also wrote a sibling ticket's command-line parsing and `code-review` called it
  compliant; the ticket's criterion was worded at the wrong level. After `to-spec`
  and `to-tickets` began carrying the observable with each test name, `dev` on the
  regenerated ticket changed only the function. `code-review` was not re-run on
  that. `accessibility-review` is unverified. See
  each skill's page.

## Where to start

| You have | Start with |
| --- | --- |
| A project that has never used these skills | `nathan-setup`, once |
| An idea, a proposal, or a vague requirement | `nathan-grill-me` |
| A finished discussion whose decisions are settled | `to-spec` |
| An existing issue that is missing acceptance criteria | `nathan-grill-me`, then `to-spec` writes back into that issue |
| A spec issue too big for one session | [`to-tickets`](./to-tickets.md) |
| A buildable ticket or small unsplit spec issue | [`dev`](./dev.md) |

Planning is allowed to stop at the PRD. Not every piece of work needs an issue,
and nothing in `nathan-grill-me` forces you onward.

## The one rule that decides readiness

An issue is ready to be built when it carries **a list of concrete test names**,
not when it carries a label:

```
Rejects an order whose total is negative
  → it('rejects order with negative total')     ✓

Handles invalid orders
  → it('handles invalid order')                 ✗ which ones? what is correct for each?
```

A requirement that cannot produce a specific test name is not specific enough
yet, and that is the signal to go back to `nathan-grill-me`. This is a necessary check,
not a sufficient one: names can be specific while the preconditions and expected
results still live only in the conversation that produced them.

There is deliberately no `ready-for-agent` label anywhere in this workflow. A
label would be a second copy of a fact the issue already states, and the two
would drift.

## Seams are chosen once

A **seam** is the boundary at which the work's behaviour can be observed by a
test. `to-spec` picks them — for the whole spec, once — and asks you to confirm
before publishing.

They are settled there rather than per ticket because seam count is a property
of the whole codebase: choosing per ticket multiplies them by construction. The
target across a change is one.

## Current state, honestly

- All six steps of the chain exist. `dev` implements one GitHub issue,
  respecting `to-tickets` test allocations and native dependencies. Integration
  QA is not part of the chain and is not planned as a skill; it is done by hand.
- Runtime coverage and remaining checks are recorded on each skill's page.
  An implemented step is not necessarily verified end to end on every tool;
  sharing source files does not establish identical runtime behaviour.
- Development hooks that mechanically restrict writes do not exist. `dev`
  supplies a worktree workflow and project validation, not a sandbox. A project
  requiring missing protections cannot treat that absence as a passed prerequisite.

Each skill's page below carries its own known limitations.

- [nathan-setup](./nathan-setup.md)
- [nathan-grill-me](./nathan-grill-me.md)
- [to-spec](./to-spec.md)
- [to-tickets](./to-tickets.md)
- [dev](./dev.md)
- [code-review](./code-review.md)
- [accessibility-review](./accessibility-review.md) — off-chain
- [codebase-scan](./codebase-scan.md) — off-chain

## Focused accessibility review

[accessibility-review](./accessibility-review.md) is also implemented as an
independent design/code review. It is not a replacement for QA. code-review
uses its shared static criteria for applicable UI diffs. Each skill page states
its current runtime coverage and limitations.

It needs no prior step and it can stop at its report, which it saves to
`.nathan-skills/accessibility-audit/<topic>-<date>.md`. When the barriers it finds should
be fixed and tracked, that file joins the chain at the top:

```
accessibility-review ──► .nathan-skills/accessibility-audit/<topic>-<date>.md
                                        │
                                        ▼
                                   nathan-grill-me ──► ... (the chain above)
```

It enters at `nathan-grill-me`, not at `to-spec`, because a findings list is not a set
of decisions: which barriers are in scope, in what order, and what "fixed" means
for each are the user's calls, and `to-spec` only transcribes calls already made.

## Whole-codebase scan

[codebase-scan](./codebase-scan.md) is **not a step of the chain above**. No
piece of work passes through it, nothing waits on it, and nothing in `dev`,
`code-review` or `to-tickets` refers to it. It is run by hand, occasionally,
against a codebase as a whole — "it has been a while, what state is this in?"

It reviews three axes separately — architecture, security and accessibility —
each with its own coverage rule, and each declaring what it did not look at. Its
report, like `accessibility-review`'s, joins the chain at the top:

```
codebase-scan ──► .nathan-skills/code-scan/<scope>-<date>.md
                                 │
              ┌──────────────────┴──────────────────┐
              ▼                                     ▼
         to-tickets                            nathan-grill-me ──► ... (the chain above)
   (same session, findings you
    name; all not buildable)
```

Unlike `accessibility-review`, it has a second exit, and it is the short one.
When the findings themselves are not in dispute and you only want them on the
board, `to-tickets` takes the confirmed list **in the same session** — one
tracking parent for the scan, one child per finding, every child marked not
buildable, ordered by the scan's severity. That writes down what was found
without an interview, and leaves what to do about it open.

It still enters at `nathan-grill-me` when the open question is *which* findings are
worth fixing, in what order, and what "fixed" means for each — those are the
user's calls and everything downstream only transcribes calls already made. And
a ticket the short path produced is not buildable: `nathan-grill-me` then `to-spec` on
that one issue is what makes it so. Either way anything that reaches the tracker
reaches it through `to-tickets`, which is also where it gets its backlog place.
