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
```

`./` means "the file at this path", not a command on your `PATH` — the leading
dot is required. The script derives every path from `$HOME` and its own
location, and is safe to run again at any time.

Run it after **adding a skill folder** or **setting up a new machine**. Editing
an existing skill needs no rerun: the tools already point at these files, so a
save is live everywhere at once.

### Reading the output

```
  link  /Users/you/.claude/skills/grill-me
  SKIP  /Users/you/.claude/skills/code-review -> symlink points outside this repo (...)

central: /Users/you/dev/nathan-skills
linked: 9   skipped: 6
```

| Line | Means |
| --- | --- |
| `link` | Installed. Every skill is relinked on every run, so these always appear. |
| `SKIP` | Something already holds that name and this script did not create it. Nothing was touched. |
| `exit 1` | At least one `SKIP`. Not a crash — the signal that something did not install. |

**A `SKIP` means the tools are running someone else's copy of that skill.** The
name is taken, so your version never gets linked. Read the path in the message:
it says what owns the name. Either it is a real directory that is not managed
here (the Cloudflare pack), or it is a stale link from another clone — in which
case delete just that link and rerun:

```bash
rm ~/.claude/skills/<name> ~/.codex/skills/<name> ~/.gemini/config/skills/<name>
./scripts/relink.sh
```

Never make the script overwrite a target instead. It refuses by design, and that
refusal is the only thing standing between a rerun and someone else's work.

### Confirming what a tool will actually run

```bash
readlink ~/.claude/skills/grill-me
```

The answer must be a path inside this repository. If it points anywhere else,
that other copy is what runs — and an edit here changes nothing. Check all three
tools, since they can disagree:

```bash
for d in ~/.claude/skills ~/.codex/skills ~/.gemini/config/skills; do
  readlink "$d/grill-me"
done
```

agy reads `~/.gemini/config/skills`, not `~/.gemini/skills`. A link in the
second is invisible to it.

The last check is the tool itself: type `/grill-me` and see whether it offers
the skill. A link can be perfect while the frontmatter keeps the tool from
loading it — a skill's `name:` must equal its folder name.

## The chain

```
nathan-setup ─── once per project, before anything else
      │
      ▼
  grill-me ────────► ~/Downloads/prd-<topic>.md
      │                        │
      ▼                        ▼
   to-spec ──────────────► one spec issue  (+ the test seams, chosen once)
      │
      ▼
  to-tickets ✗ ──────► sub-issues + blocking relations
      │
      ▼
     dev ✗ ──────────► a worktree, implemented and verified
      │
      ├──► code-review
      └──► integrate-review ✗ ──► QA report → your call
```

| Step | Skill | Hands over | Built |
| --- | --- | --- | --- |
| Connect a project | [`nathan-setup`](./nathan-setup.md) | Project rules all three tools read | ✅ |
| Decide what to build | [`grill-me`](./grill-me.md) | A topic PRD in `~/Downloads` | ✅ |
| Write it down once | [`to-spec`](./to-spec.md) | One spec issue, and the test seams | ✅ |
| Split it | `to-tickets` | Sub-issues and blocking relations | ✗ |
| Build it | `dev` | A worktree, implemented and verified | ✗ |
| Review it | [`code-review`](./code-review.md) | Separate Standards, Spec and optional Accessibility findings | ✅ |
| Verify it | `integrate-review` | A pass / fail / unknown QA report | ✗ |

The unbuilt steps are genuinely unbuilt. `to-spec` will tell you to run
`to-tickets` next, and `to-tickets` does not exist yet — that is a real gap in
the chain today, not an oversight in this page.

## Where to start

| You have | Start with |
| --- | --- |
| A project that has never used these skills | `nathan-setup`, once |
| An idea, a proposal, or a vague requirement | `grill-me` |
| A finished discussion whose decisions are settled | `to-spec` |
| An existing issue that is missing acceptance criteria | `grill-me`, then `to-spec` writes back into that issue |
| An existing issue that already carries a test-name list | It is ready to build — but `dev` does not exist yet |

Planning is allowed to stop at the PRD. Not every piece of work needs an issue,
and nothing in `grill-me` forces you onward.

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
yet, and that is the signal to go back to `grill-me`. This is a necessary check,
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

- Four of seven steps exist. The planning chain still has a gap after `to-spec`;
  code-review can inspect separately prepared changes.
- Runtime coverage and remaining checks are recorded on each skill's page.
  An implemented step is not necessarily verified end to end on every tool;
  sharing source files does not establish identical runtime behaviour.
- The development gates (the hooks that would stop unsafe writes during `dev`)
  do not exist. `nathan-setup` reports them as unavailable rather than
  pretending they are installed.

Each skill's page below carries its own known limitations.

- [nathan-setup](./nathan-setup.md)
- [grill-me](./grill-me.md)
- [to-spec](./to-spec.md)
- [code-review](./code-review.md)
- [accessibility-review](./accessibility-review.md)

## Focused accessibility review

[accessibility-review](./accessibility-review.md) is also implemented as an
independent design/code review. It is not a replacement for QA. code-review
uses its shared static criteria for applicable UI diffs. Each skill page states
its current runtime coverage and limitations.
