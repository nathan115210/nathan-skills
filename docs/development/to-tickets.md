# to-tickets

[SKILL.md](../../skills/development/to-tickets/SKILL.md)

## What it does

Takes **one** spec issue and turns it into sub-issues, each carrying native
blocking relations, on GitHub.

Three things happen here that happen nowhere else in the chain: the work gets
cut into slices, the spec's test names get allocated to those slices, and the
slices the spec cannot make buildable get marked as such in writing.

It writes no files. The only exit is issues — and, when the spec issue is on a
GitHub Project, the same board the spec issue is on.

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
- The **`project`** token scope, but only if you keep your issues on a GitHub
  Project. `repo` does not cover Projects v2, so a token with `repo` alone passes
  every other check and then fails at placement — after the issues exist. The
  skill checks this up front and tells you to run `gh auth refresh -s project`.
  Missing it costs you the board, not the breakdown.
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

Nothing is published until you approve the breakdown. It presents each title,
its native blockers, and the complete rendered Markdown body in dependency
order. What you review is the actual issue content, not a summary that gets
rewritten during publication. Any change to the cut, wording, test allocation,
or edges produces a revised preview before approval.

**The body you approve is literally the bytes GitHub receives.** Each body is
rendered once into a scratch file outside the repository; the preview is that
file, `gh issue create --body-file` publishes that file, and afterwards the
published body is `diff`ed against it. So "the body matches" is a command rather
than a judgment, and a body mangled by shell quoting cannot slip through looking
plausible. The scratch files are deleted when verification finishes.

It then reads the issues and dependency graph back from GitHub and compares the
titles, bodies, test allocation, parent relations, blocking edges and board
placement with the approved plan, matching issues to plan entries by the number
captured at creation rather than by title. A mismatch gets one repair and another
read-back; a remaining mismatch is reported as a partial publish.

## What the tickets deliberately do not contain

- **No "Parent" section and no "Blocked by" section.** Both relations are
  native GitHub state, which is queryable. A line of prose naming them is a
  second copy that drifts, and when the body and the graph disagree somebody
  acts on the wrong one.
- **No label, no status line, and no Project field** — no Status, Priority or
  Size. Whether a ticket is buildable is judged by whether it carries test names,
  so a label or a field would be a second copy of that fact. The first pass over
  your board is yours.
- **No file paths and no code snippets**, with the same prototype exception the
  spec has.
- **Nothing invented.** A slice no test name covers says so outright: *"No test
  name in the spec covers this slice. Not buildable — the gap is in the spec,
  not in this ticket."*

## Which Project the tickets land on

Whatever board the **parent spec issue** is already on. The skill never chooses
one and never asks — it reads the parent's `projectItems` and places every child
on the same boards. Parent on no board, children on no board.

That is a deliberate non-choice. Asking would produce the same answer every time;
storing the answer in a config file would be a second copy that drifts from the
board you actually use. Inheriting needs no setup and cannot pick the wrong one,
and it gives you an opt-out you already control: leave the spec issue off a board
and nothing gets placed.

Membership is not treated like a label, and the distinction is the whole reason
this is allowed at all. Putting an issue on a board copies no fact — it does not
restate the test names, the parent link or the blocking edges — so there is
nothing for it to drift from. A Status field would restate readiness, which the
test names already carry, so fields stay out.

It sets no fields, and on a board with GitHub's default *item added → Todo*
workflow it does not need to — the board sets Status itself. Verified.

If placement fails, the publish still finishes. The issues and their native
relations are the deliverable; the board is a view of it. You get the placement
reported as incomplete, with the command to finish it by hand — because a board
showing half a breakdown looks like the whole breakdown.

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

**I already split this spec. What happens if I run it again?**
It stops before doing any work. The first thing it checks, after naming the
issue, is whether the parent already has sub-issues — because re-running is the
natural reaction to a failure during publishing, and it is also the action that
creates a second complete set of children. It tells you what is already attached
and leaves the decision to you. It will not offer to "add the missing ones": the
first run's approved plan is gone, so it cannot tell which are missing.

**Publishing failed halfway. What state am I in?**
It reports a partial publish as partial and names the edges it could not create.
A half-linked breakdown is worse than an unlinked one because it looks finished,
so this is the one outcome worth reading carefully. Individual edges are
removable (`DELETE .../dependencies/blocked_by/<id>`) and the skill gives the
command.

**Which Project do the tickets go into?**
The one the spec issue is already on. See
[Which Project the tickets land on](#which-project-the-tickets-land-on). If you
want a breakdown kept off the board, keep the spec issue off it.

**I don't use Projects at all. Does this get in the way?**
No. The parent is on no board, so nothing is placed and nothing is asked. The
`project` scope is only checked, never required.

**Does it set a milestone?**
No, and it does not ask. Which delivery batch a set of tickets belongs to is
your call, not a property of how the work was cut. What it does do is print the
command with the new issue numbers already filled in, so assigning the whole
batch is one paste:

```
gh issue edit 20 21 22 23 --milestone "v1"
```

That is deliberately a convenience rather than a step. Inheriting the milestone
from the spec issue the way the Project is inherited would save exactly one
command — `gh issue edit` takes a list — which does not pay for the rule it
would add. If you want the board grouped by milestone, set `Group by:
Milestone` on the view once; that outlives any single breakdown.

**What happens after splitting?**
Run [dev](./dev.md) on one buildable ticket in a fresh session. It reads the
native dependencies and parent spec before implementing; it does not start a
ticket marked not buildable.

## It's working if

- It names the issue it is splitting up front, and checks write access before
  doing the work rather than after.
- It quotes the spec's seams back at you instead of proposing its own.
- It puts the numbered breakdown to you and waits, rather than publishing and
  then asking. Each proposed ticket includes the exact body GitHub will receive.
- Every test name you remember deciding lands on exactly one ticket, unchanged.
- It names the destination board in the preview, before you approve — or says
  there is none, and why.
- Afterwards, the parent shows its sub-issues and each ticket shows its blockers
  in GitHub's own UI, every title and body matches the approved preview, and
  every ticket is on the parent's board with no field set — while the parent's
  body is untouched.
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

**Verified, Projects** — 2026-09-20, `gh` 2.80.0. A throwaway Project, a parent
issue and a child issue were created, the child attached as a sub-issue by `id`,
the parent placed on the board, the step 1 inheritance query run against the
parent, the child placed from what that query returned, and the placement read
back from the child. All succeeded. The Project and both issues were deleted
afterwards; raw output was kept outside this repository.

Four things that run confirmed and design alone would not have:

- The step 1 query returns the project's `number`, `title` and owner `login` —
  exactly what placement needs. `gh issue view --json projectItems` is **not** a
  substitute: it returns only the project `title` and the item's field values,
  with no `number` and no owner. The skill uses GraphQL for this reason.
- **Placement is idempotent.** Adding an issue already on the board returned the
  same item id and exit `0`, and the board's item count did not change. Repairing
  a failed placement is just running the command again.
- **Items landed with Status `Todo` by themselves**, from the Project's default
  *item added → Todo* workflow — without the skill setting any field. Not setting
  fields does not leave tickets in a "No Status" limbo on a board that has that
  workflow enabled.
- A wrong `--owner` fails loudly with `unknown owner type`, not silently.

Still unverified: an **organization**-owned Project (only a user-owned one was
exercised), and the failure text when the token lacks the `project` scope.

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
- Projects **v2** only. Classic project boards are not handled and not detected.
- A parent on several boards puts every child on all of them. There is no way to
  pick a subset short of taking the parent off a board first.
- There is no re-split or resume. Running it twice on the same spec issue is now
  refused up front rather than silently duplicating, but nothing reconciles a
  partial first run — unpick it by hand if you need to start over.
- The read-back pages past 50 sub-issues and 20 blockers when GitHub says there
  is more, but GitHub caps a parent at 100 sub-issues regardless; a breakdown
  that large is beyond what this skill has been designed around.
- The handoff to `dev` has not been runtime-verified end to end.

## Where it fits

Upstream is [to-spec](./to-spec.md), which settles the seams and the test names
this skill only allocates. Downstream is [dev](./dev.md), which implements one
buildable GitHub issue. See
[the workflow overview](./README.md).
