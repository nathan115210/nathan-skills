# to-tickets

[SKILL.md](../../skills/development/to-tickets/SKILL.md)

## What it does

Takes **one** spec issue and turns it into sub-issues, each carrying native
blocking relations, on GitHub. It also has a second, narrower entrance — a
[codebase-scan](./codebase-scan.md) findings list confirmed in the same session.
See [the scan path](#the-scan-path).

Four things happen here that happen nowhere else in the chain: the work gets
cut into slices, the spec's test names get allocated to those slices, the slices
the spec cannot make buildable get marked as such in writing, and the whole open
backlog gets put into one order with the new tickets inserted into it.

It writes no files. The only exit is issues — and, when the spec issue is on a
GitHub Project, the same board the spec issue is on, in an order you approved.

## When to reach for it

You type it. It will not fire on its own.

| Where you are | What to run |
| --- | --- |
| Requirements are still open | [grill-me](./grill-me.md) first |
| Decisions settled, nothing tracked yet | [to-spec](./to-spec.md) first |
| A spec issue exists and the work is too big for one session | `to-tickets` |
| A spec issue exists and you will finish it in one sitting | Nothing — splitting buys you nothing here |
| `codebase-scan` just finished and you want its findings on the board | `to-tickets`, right there in that session |

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
  Missing it costs you the board and the ordering, not the breakdown.
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
plausible. Step 8 does that read-back with `gh api ... --jq '.body' | diff - ...`:
`gh api --jq` already writes a scalar string as raw text, but it terminates
stdout with one transport newline, so a scratch file with no trailing newline
needs that one-byte difference accounted for rather than being treated as a body
mismatch. The scratch files are deleted when verification finishes.

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
- **No label, no status line, and no Project field** — no Status, no Size, and
  no Priority field either. Whether a ticket is buildable is judged by whether it
  carries test names, so a label or a field restating that would be a second copy
  of it. Order is set as the board's own item position, not as a field — see
  below.
- **No file paths and no code snippets**, with the same prototype exception the
  spec has.
- **Nothing invented.** A slice no test name covers says so outright: *"No test
  name in the spec covers this slice. Not buildable — the gap is in the spec,
  not in this ticket."* A scan ticket says the other version — no spec covers it
  at all — and carries the finding's file, line and revision, which is the one
  place a path is allowed in a body.

## The scan path

`codebase-scan` is not part of the chain and produces no spec. Its report used
to reach the tracker only through `grill-me` and `to-spec`, which meant a full
interview before anything was written down — expensive, and wrong when the
findings themselves are not in dispute and you just want them tracked.

So `to-tickets` takes that findings list directly, in the **same session that
produced it**, once you have said which findings count. It:

- creates **one tracking parent**, `Codebase scan: <project> @ <revision>`,
  holding the report's identity header, scope line and per-axis not-covered
  declarations, and the path of the saved report — and none of the findings;
- creates **one child per finding**, unmerged and unsubdivided, in the scan's
  own words and at the location it named;
- marks **every one of them not buildable**, because a findings list has no
  acceptance criteria and no test names;
- orders the board by the scan's own severity ranking, blockers first, in the
  same approval as the bodies.

Everything else — exploring the codebase, the approval gate, publication, the
`diff` read-back — is the same run as the spec path.

**Nothing published this way is buildable, and that is not a defect.** These
tickets record what was found and where it sits in the queue. To start one, run
`grill-me` on that issue in a new session and `to-spec` back into it; that is
where the interview happens, once, for the finding you actually decided to fix.

Two things it will not do: it will not take a scan report handed over in a fresh
session (that report's decisions were never made — it enters at `grill-me`), and
it will not ticket the whole candidate list because you approved something else.
You name the findings.

## Which Project the tickets land on

Whatever board the **parent spec issue** is already on. The skill never chooses
one and never asks — it reads the parent's `projectItems` and places every child
on the same boards. Parent on no board, children on no board.

**The scan path asks once**, and only about the tracking parent it just created,
which is on no board by definition. Answer with a board or with "none"; from
there the children inherit from the parent exactly as above. This is the single
question this skill asks about Projects, and it exists because inheriting nothing
would drop a whole scan's worth of tickets somewhere you never look.

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

## The order it puts your board in

You work down the board from the top, one issue at a time, and you do not
re-rank it by hand. So an issue nobody positioned is an issue you never reach.
The skill therefore reads every open issue on the parent's board, builds **one
total order** with the new tickets inserted, shows you that complete list in the
same approval as the ticket bodies, and writes it back after publishing.

Three rules build the order:

1. A blocker comes before everything it blocks. This is the only hard one.
2. Existing issues keep their relative order — the board as it stands is yours.
   An existing issue moves only when a blocking edge forces it, and every such
   move is called out with its old and new position.
3. New tickets are placed by technical risk and dependency: what they unblock,
   what stays broken until they are done, how far the blast radius reaches.

**The ranking evidence stops at the tracker.** A waiting customer or an
approaching deadline is not in the issues, so it cannot be in the order. If your
order depends on something the issues do not say, say it in the approval step;
the skill will ask rather than guess.

Order is written as the board's **item position**, the order GitHub actually
displays. Not a Priority field: that would be a second statement of the same
ranking to keep in step by hand, which is the drift this workflow refuses
everywhere else.

One consequence worth knowing before you go looking for the change: position is
a property of the project, not of a view. **A view with its own sort applied
shows that sort instead**, and the written order stays invisible there until the
sort is cleared.

If the parent is on no board, or the token lacks the `project` scope, nothing is
ordered and the skill says so — it does not substitute a label, a field or an
ordered list in a comment.

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
[to-spec](./to-spec.md), in its own session. A `codebase-scan` findings list is
the one exception, and only in the session that produced it — see
[the scan path](#the-scan-path).

**Do I have to run `grill-me` on every scan finding before it can be tracked?**
No, not any more. Tracking and deciding are separate: the scan path writes the
findings to the board as not-buildable tickets without an interview, and
`grill-me` happens later, on the one ticket you are about to start. Run
`grill-me` first only when *which* findings are worth fixing is itself the
question.

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
  there is none, and why. On the scan path it asks that once, about the tracking
  parent, and never again.
- On the scan path: one parent holding the report's header and gaps but no
  findings, one child per finding you named and no others, every child marked
  not buildable, and severity order preserved except where a blocker forced a
  move.
- The preview shows the complete post-insert order of every open issue on that
  board, not just where the new tickets landed, and names any existing issue it
  wants to move and the edge that moves it.
- Afterwards the board reads top-to-bottom in the order you approved, and no
  blocker sits below something it blocks.
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

**Schema-confirmed, not run** — the ordering API. 2026-09-21, `gh` against
GitHub's GraphQL API. Introspection showed `ProjectV2.items` accepting
`orderBy: {field: POSITION, direction: ASC}` (`POSITION` is the only value that
enum has) and `updateProjectV2ItemPosition` taking `projectId`, `itemId` and an
optional `afterId`. Both of the skill's actual queries were then sent and
reached execution, failing only on a deliberately fake node id (`NOT_FOUND`,
not a validation error), which establishes their shape and nothing else.

What that does **not** establish: that a top-down sweep of the mutation produces
the intended board order, that omitting `afterId` reliably moves an item to the
top, or how the sweep behaves against a large board. No ordering run has been
performed against a real Project. Treat the ordering step as the least verified
thing in this skill.

**Valid, but never run against data.** The read-back query in step 8 nests
`blockedBy` inside `subIssues.nodes`. Both connections returned real nodes
separately in the verified run, and the nested query passes GitHub's schema
validation — it reaches execution and fails only on a missing issue number — but
no run has seen that exact query return a populated graph. Low risk, and not
zero.

**Verified end-to-end, scan path only** — 2026-09-20, Claude Code 2.1.278,
`gh` 2.80.0, against this repository. A `codebase-scan` findings list confirmed
in the same session produced tracking parent #18 and 16 children, #19-#34, with
one blocking edge (#30 blocked by #20). Everything the scan path specifies held:
the parent carried the scan's header, scope and not-covered declarations and no
findings; each child is exactly one finding, unmerged and unsubdivided; all 16
carry the not-buildable statement; the Seams/Acceptance-Criteria gate was
skipped with the absence of a spec stated first; the board question was asked
once about the parent. The read-back returned 16 sub-issues with
`hasNextPage: false`, one edge whose blocker is in this repository, and all 17
titles and bodies byte-identical to the approved scratch files under `diff`. No
label, Status or other field was set on anything, and the target repository's
working tree was unchanged.

**Two defects in this page's own instructions, found by running them.** Both are
in step 8, the step that makes a publish verifiable:

- `gh api … --jq -r '.body'` fails with `accepts 1 arg(s), received 2`, because
  `--jq` takes one argument and `-r` is read as a second. It returns an empty
  body, which then "differs" from every scratch file — a total false alarm that
  looks exactly like a catastrophic publish failure. The working form is
  `--jq '.body'`.
- That form appends one trailing newline of its own, so a naive `diff` reports a
  spurious one-line difference on every ticket. The comparison has to strip it.

Both were hit verbatim, twice, in this run.

**Still untested.** The **spec path** — the normal one — has no end-to-end run:
reading a real `to-spec` spec, quoting its seams, cutting vertical slices and
allocating test names are all unverified. So is **board placement and the whole
of step 7's ordering**, because the run deliberately chose no board; that
remains the least verified part of this skill, now for the second reason. Codex
and agy are untested throughout, as is the handoff to `dev`. A skill can fail
for reasons that have nothing to do with its API calls — a frontmatter field a
tool parses differently, a step the model skips, a confirmation it does not
actually wait for.

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
- Ordering costs one mutation per item and reads the whole board twice. On a
  large backlog that is a long step, and `403`/`429` back-off leaves a partially
  written order — correct from the top down, untouched below the point it
  stopped, and reported as partial.
- Ordering is limited to issues **on the parent's board**. An open issue that is
  on no board cannot be positioned; the skill names those issues rather than
  ordering them, and putting them on the board is your call.
- The handoff to `dev` has not been runtime-verified end to end.
- The template has **no canonical wording for a ticket that records an open
  question** — one that is neither a spec gap nor a scan finding. Issues #35-#38
  in this repository were published with an invented third sentence, which is
  not sanctioned by `references/ticket-template.md`. Either that path gets a
  sanctioned form or it stays outside this skill; leaving it undecided invites
  the next person to copy whatever they find.

## Where it fits

Upstream is [to-spec](./to-spec.md), which settles the seams and the test names
this skill only allocates. Downstream is [dev](./dev.md), which implements one
buildable GitHub issue. See
[the workflow overview](./README.md).
