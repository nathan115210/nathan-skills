# to-tickets

[SKILL.md](../../skills/development/to-tickets/SKILL.md)

## What it does

Takes **one** spec issue and turns it into sub-issues, each carrying native
blocking relations, on GitHub.

Three things happen here that happen nowhere else in the chain: the work gets
cut into slices, the spec's test names get allocated to those slices, and the
slices the spec cannot make buildable get marked as such in writing.

It writes no files. The only exit is issues.

## When to reach for it

You type it. It will not fire on its own.

| Where you are | What to run |
| --- | --- |
| Requirements are still open | [grill-me](./grill-me.md) first |
| Decisions settled, nothing tracked yet | [to-spec](./to-spec.md) first |
| A spec issue exists and the work is too big for one session | `to-tickets` |
| A spec issue exists and you will finish it in one sitting | Nothing — splitting buys you nothing here |

Run it in a **fresh session**, pointed at the issue number. It re-reads the
issue rather than trusting a conversation, because the spec is the maintained
record and the planning session that produced it is gone.

## Prerequisites

- A GitHub repository you have **write** access to. The check is explicit
  (`viewerPermission`), because read access alone makes a repository look usable
  right up to the moment it isn't.
- One spec issue, named by number or URL. It will ask rather than guess.
- Nothing else. There is no setup step and no configuration.

## What it does not decide

The spec already settled four things, and this skill treats all four as closed:

| Settled | Here |
| --- | --- |
| The **seams** | Used, quoted from the spec. Never re-chosen and never added to — seam count is a whole-codebase property, so it is decided once per spec. |
| The **requirements** | Not reopened. An open requirement stops the skill and sends you back to [grill-me](./grill-me.md). |
| The **test names** | Transcribed and allocated. Never invented. |
| The **combined behavior** | Left on the parent. It belongs to the whole, and the whole is only visible there. |

A slice whose behavior no chosen seam can observe is treated as a bad cut, not
as a reason to add a seam. That is the constraint most likely to send it back to
redrawing the breakdown, and it is deliberate.

## How it cuts

Each ticket is a **tracer bullet**: a narrow but complete path through every
layer it touches, verifiable on its own, sized to fit one fresh context window.
Vertical, never a horizontal slice of one layer. Prefactors — changes that make
the real change easy — come first and block what needs them.

**Wide refactors are the stated exception.** A mechanical change whose blast
radius fans across the codebase cannot land green as a tracer bullet, so it is
sequenced as expand–contract instead: add the new form beside the old, migrate
the call sites in batches each blocked by the expand, then delete the old form
in a ticket blocked by every batch. If even the batches cannot be green alone,
it says so and makes them all block a final integrate-and-verify ticket.

Nothing is published until you approve the breakdown. It presents the numbered
list — title, blockers, what it delivers, the test names it carries — and
iterates.

## What the tickets deliberately do not contain

- **No "Parent" section and no "Blocked by" section.** Both relations are
  native GitHub state, which is queryable. A line of prose naming them is a
  second copy that drifts, and when the body and the graph disagree somebody
  acts on the wrong one.
- **No label, no status line, no Project.** Whether a ticket is buildable is
  judged by whether it carries test names. Nothing in this workflow reads
  Projects.
- **No file paths and no code snippets**, with the same prototype exception the
  spec has.
- **Nothing invented.** A slice no test name covers says so outright: *"No test
  name in the spec covers this slice. Not buildable — the gap is in the spec,
  not in this ticket."*

## The trap it exists to avoid

Both relations are written by issue **`id`** — the database id returned when the
issue is created — while the URL path uses the issue **`number`**. Mixing them
up fails in two different ways, and only one is loud:

| Wrong input | What happens |
| --- | --- |
| `sub_issues` with a number | `404 Not Found`. Loud, and safe. |
| `dependencies/blocked_by` with a number | **HTTP 200, and a dependency on an unrelated issue in a stranger's repository.** Low database ids exist somewhere on GitHub, so the number resolves to a real issue that is not yours. |

This is why the skill reads the whole graph back and compares node lists rather
than counts, and why it checks that every blocker lives in this repository.

## Common questions

**Can I point it at the PRD instead of the issue?**
No. It takes an issue. If you only have a document, the missing step is
[to-spec](./to-spec.md), in its own session.

**My spec has no test names. Will it refuse?**
No. It splits anyway and marks every ticket not buildable. Splitting an
unbuildable spec is still useful — you see the shape of the work — but no ticket
from it should be started. Settle the criteria in
[grill-me](./grill-me.md), re-run [to-spec](./to-spec.md), then re-run this.

**What if a test name fits none of the slices?**
It reports it and does not drop it. Either the cut is wrong or the spec
specifies something outside its own scope. Both are your call, not the skill's.

**Will it edit or close the parent issue?**
No. It attaches children to the parent and leaves the parent's body, title and
state alone.

**Publishing failed halfway. What state am I in?**
It reports a partial publish as partial and names the edges it could not create.
A half-linked breakdown is worse than an unlinked one because it looks finished,
so this is the one outcome worth reading carefully. Individual edges are
removable (`DELETE .../dependencies/blocked_by/<id>`) and the skill gives the
command.

**It told me to run `dev` and that skill doesn't exist.**
Correct, and this is now the live gap in the chain. The tickets stand on their
own until `dev` is built.

## It's working if

- It names the issue it is splitting up front, and checks write access before
  doing the work rather than after.
- It quotes the spec's seams back at you instead of proposing its own.
- It puts the numbered breakdown to you and waits, rather than publishing and
  then asking.
- Every test name you remember deciding lands on exactly one ticket, unchanged.
- Afterwards, the parent shows its sub-issues and each ticket shows its blockers
  in GitHub's own UI — and the parent's body is untouched.
- No new file appeared anywhere.

## Known limitations

What has runtime evidence here, and what does not, in three tiers.

**Verified against a real repository** — 2026-09-15, `gh` 2.80.0. Creating a
parent and two children, attaching both as sub-issues by `id`, adding a
`blocked_by` edge, reading the graph back through both REST and GraphQL,
deleting an edge, and deleting the issues all succeeded. Both failure modes in
the table above were reproduced deliberately: `sub_issues` with a number
returned `404`, and `dependencies/blocked_by` with a number returned `200`
while attaching an issue from an unrelated public repository. The temporary
issues were deleted; raw output was kept outside this repository.

Also verified in that run: `issueDependenciesSummary.blockedBy` reported `1`
while `blockedBy` returned two nodes — the cross-repository edge was reachable
in the list but not counted in the summary. **A count is not a check**, which is
why the skill compares node lists.

**Valid, but never run against data.** The read-back query in step 7 nests
`blockedBy` inside `subIssues.nodes`. Both connections returned real nodes
separately in the verified run, and the nested query passes GitHub's schema
validation — it reaches execution and fails only on a missing issue number — but
no run has seen that exact query return a populated graph. Low risk, and not
zero.

**Untested.** No end-to-end run of the skill has been recorded in any tool.
Discovery, the input check, the codebase exploration, the cut, the allocation of
test names, the confirmation step and the handoff are unverified in Claude Code,
Codex and agy. Only the API mechanics the skill depends on have evidence, and a
skill can fail for reasons that have nothing to do with its API calls — a
frontmatter field a tool parses differently, a step the model skips, a
confirmation it does not actually wait for. The cheapest part of this gap to
close is discovery: open a fresh session and see whether the tool offers
`/to-tickets`.

The rest of this section is design, not evidence.

- **`disallowed-tools` is not a hard write barrier**, at least on Codex, where a
  diagnostic overrode the equivalent prose rule in [to-spec](./to-spec.md) and
  created a file. The no-file-write rule lives in the skill body too, but treat
  it as a convention rather than an enforced sandbox.
- GitHub only. No Linear, no local-file tracker, no detection of either.
- There is no re-split. Running it twice on the same spec issue creates a second
  set of children rather than reconciling with the first; unpick the first set
  by hand if you need to start over.
- The downstream step (`dev`) does not exist, so the handoff at the end points
  at nothing.

## Where it fits

Upstream is [to-spec](./to-spec.md), which settles the seams and the test names
this skill only allocates. Downstream is `dev`, which is not built yet. See
[the workflow overview](./README.md).
