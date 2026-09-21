---
name: to-tickets
description: Split one spec issue into sub-issues carrying native blocking relations — read the spec, cut tracer-bullet slices, allocate its test names, get the breakdown and the resulting backlog order confirmed, then publish to GitHub and write that order back to the Project. Also accepts a codebase-scan findings list confirmed in the same session, publishing it under a tracking parent as not-buildable tickets. No requirements interview, no seam choice, no code.
disable-model-invocation: true
disallowed-tools: Write, Edit, NotebookEdit
---

# To Tickets

You are the only splitter in this workflow. One spec issue goes in; its sub-issues and their blocking relations come out.

Four things happen here and nowhere else:

1. The work is cut into slices, and each slice declares what blocks it.
2. The spec's test names are allocated to those slices.
3. The slices the spec cannot make buildable are marked as such, in writing.
4. The open backlog is put into one order, with the new slices inserted into it.

The fourth is why this skill touches issues it did not create. Every path that
produces issues funnels through here, so this is the one place a total order can
be written without a second entry point to keep in step.

## Inputs

Exactly one of two, and they take different paths through this skill:

| Input | Where it is | How to read it |
| --- | --- | --- |
| **A spec issue** — the normal case | GitHub, in the repository you are standing in | `gh issue view <n> --comments`. Read the body and the comments. |
| **A confirmed `codebase-scan` findings list** — the scan path | In this conversation, where `codebase-scan` just produced it | Read nothing new. The findings are already here; the saved report in `.nathan-skills/code-scan/` is their record. |

If the user named neither, ask. Do not search the tracker for a plausible spec — splitting the wrong issue produces a breakdown that looks right.

**Do not accept a file as a spec.** A planning PRD is `nathan-grill-me`'s output and `to-spec`'s input; it is expected to be stale by now. If the user offers a document instead of an issue, the missing step is `to-spec`, in its own session.

The body holds the specification; the comments hold process records. Both are input — a correction that arrived as a comment is still a decision.

### The scan path

`codebase-scan` is not a step of this workflow and produces no spec. Its report
is a findings list, and a findings list has no seams and no test names — so every
ticket this path publishes is **not buildable**, by construction, and says so in
its own body. That is the honest result, not a gap to fill: the tickets record
what was found and where it sits in the backlog order, and `nathan-grill-me` then
`to-spec` is what makes any one of them buildable.

This path is available only when `codebase-scan` produced those findings **in
this same session** and the user has said which of them become tickets. A report
file handed over in a fresh session is not this input — its decisions were never
made, so it enters at `nathan-grill-me`.

Four things differ from the spec path. Nothing else does:

| | Spec path | Scan path |
| --- | --- | --- |
| The parent | The spec issue, already in the tracker | A tracking issue you create in step 0 |
| Step 1's gate | The body must carry Seams and Acceptance Criteria | Skipped — there is no spec to check |
| Cutting, step 3 | Slices cut from the spec | One finding, one ticket. Never merged, never subdivided |
| Test names, step 4 | Allocated from the spec | None exist; every ticket carries the not-buildable statement |

Step 2's codebase exploration, step 5's approval, step 7's ordering and steps
6–8's publication and read-back are identical. The proposed order follows the
scan's own severity ranking, adjusted so every blocker precedes what it blocks.

### What the spec already settled, and you do not revisit

| Settled | Where it lives | Here |
| --- | --- | --- |
| The **seams** | The spec's Seams section | Used. Never re-chosen, never added to. |
| The **requirements** | The whole spec | Not reopened. An open requirement stops you. |
| The **acceptance criteria and test names** | The spec's Acceptance Criteria section | Transcribed and allocated. Never invented. |
| The **combined behavior** | The spec's Combined Behavior section | Left on the parent. Never copied into a ticket. |

Seams are a whole-codebase property, settled once per spec, not once per ticket. Combined behavior is a property of the whole, visible only at the parent.

## Boundaries

**Yours:**

- Read code, history, and existing issues.
- Cut the slices and their blocking edges, and get them confirmed.
- Create the sub-issues and both kinds of relation.
- Put each new issue in the Project the parent is already in, when it is in one.
- Read every open issue on that Project and set the order of its items.
- Mark every slice the spec cannot make buildable.

**Not yours:**

- **Interviewing for requirements.** If a requirement is still open, name it and stop. Resolving it is `nathan-grill-me`, in its own session.
- **Choosing, adding or moving seams.** `to-spec` is the only place seams are decided.
- **Inventing acceptance criteria or test names.** The user sets what counts as correct. You transcribe and allocate.
- **Writing any document.** No `.md` file, no `.scratch/` directory, no local file per ticket. The only exit is issues. A ticket in a file is the second record this workflow exists to avoid.

  *One narrow exception, and it is transport rather than a record:* the approved body of each ticket is held in a scratch file under `$TMPDIR` between step 5 and the end of step 8, so that the text you show the user, the text GitHub receives, and the text you compare against afterwards are one string rather than three transcriptions of it. Those files live outside the repository, are never a source of truth after publication, and are deleted at the end of step 8. Writing a ticket anywhere inside the repository is still forbidden.
- **Touching code or git.** No edits, no worktree, no spike, no commit, no push.
- **Rewriting the parent.** You attach children to it. You do not edit its body, change its title, or close it.
- **Labels, readiness and Status.** No readiness label, no Status, no Size, no custom field of any kind. Readiness is judged by whether a ticket carries test names, and a label or a field restating it would be a second copy of that fact that drifts from it.

Two things are deliberately **not** in that list.

Project **membership** copies no fact — not the test names, the parent relation or the blocking edges — so there is nothing for it to drift from. It is a view, and it is the user's view of this work.

**Order** has no native source anywhere in GitHub, so it too copies no fact. And it cannot be left to the user's first pass over the board, because work is picked strictly top-down, one issue at a time: an unordered issue is an invisible issue, and creation order is not an order at all.

Ranking evidence stops at what the issues contain — severity, blocking relations, blast radius. Commercial priority (a waiting customer, a deadline) is not knowable from the tracker, so the order you propose is by technical risk and dependency. Say that when you present it. If the user wants it ordered on something else, ask; do not infer it.

## Process

Read `references/github-procedures.md` for the exact commands and failure modes of
steps 0, 1, 5, 6, 7 and 8. Read `references/ticket-template.md` at step 5. This file
holds the decisions; those files hold the mechanics.

### 0. Name the input, and check you can publish

State which issue you are splitting, by number and title. One line.

Before doing the work, confirm three things (commands in the procedures file):

- **The tracker is writable.** If not, or if there is no GitHub repo, stop and say
  exactly what failed. **Do not fall back to writing tickets to files.** Print the
  proposed breakdown in this conversation and say plainly that nothing was published.
- **The parent has no sub-issues.** Anything other than `0` stops you. There is no
  re-split and no reconciliation; publishing again doubles the breakdown. List the
  existing children and let the user decide. Do not offer to "add the missing ones".
- **The token has the `project` scope.** If not, say so and give the fix, but do not
  stop: the issues and their relations are the deliverable, and the board is not.
  Carry the gap into step 5 so the user approves knowing the issues will be neither
  placed nor ordered.

**On the scan path, create the tracking parent now** — after the writable check,
before anything else. It is one issue, and its body is the scan's own record:

- **Title** — `Codebase scan: <project> @ <short revision>`.
- **Body** — the report's identity header, its scope line and its per-axis
  not-covered declarations, verbatim; then the absolute path of the saved
  report, labelled as a git-ignored local file that is not version-controlled.
- **Nothing else.** The findings do not go in the body — each one is a child, and
  a copy of it here is the second record this skill exists to avoid.

Show that body and get it approved before creating the issue. The parent is a
container and a provenance record, not a ticket; `dev` never picks it up. Say its
number once it exists, and treat it as the parent everywhere below. Run the
no-sub-issues check after creating it.

### 1. Read the spec, and state what it can support

**Spec path only — skip this check on the scan path**, where there is no spec
to check, the seams are none and the test names are none. State those three
facts in one line instead, then go on to the Project question below.

First check the issue is a spec at all. A `to-spec` spec carries a **Seams**
section and an **Acceptance Criteria and Test Names** section. If the body has
neither, **stop**: this is an ordinary issue, and splitting it would mean
inferring seams from prose — the one thing this skill must never do. Say which
sections are missing and that the step in front of you is `to-spec`.

A spec that has both sections but no test names under the second is a different
case, and it does not stop you — see below.

Read the body and the comments, and state, one line each:

- The seams, as the spec named them.
- Whether the spec carries acceptance criteria with test names, or carries `to-spec`'s statement that none were settled.
- The Project the new issues will join, or that there is none.

**The destination Project is inherited from the parent, never chosen and never asked for.** Whatever board the spec issue is already on is where its children go; if the parent is on no board, the children go on none. If the parent is on more than one board, put the children on all of them, and say which in step 5. Read the parent's boards with the query in the procedures file; take the Project owner from the parent's own item, not from the repository.

**The scan path is the one exception, and it is asked once, about the parent.**
A tracking issue created moments ago is on no board, so there is nothing to
inherit, and inheriting nothing would put a whole scan's worth of tickets where
the user does not look. Ask which Project the tracking parent joins, or none,
place the parent there, and from that point the rule above applies unchanged.

**A spec with no test names is still worth splitting, and splitting it does not make it buildable.** Cut the slices, then say so per ticket in step 4. Do not stop, and do not fill the gap — `to-spec` deliberately left it visible.

### 2. Explore the codebase

Not optional, and not skippable on the grounds that the spec is detailed. Slices are a property of the code.

Find the current state of the area, the vocabulary already in use, and any conventions or ADRs that constrain it. Write ticket titles in the project's own vocabulary.

Look for **prefactoring** — a change that makes the real change easy. Make the change easy, then make the easy change. A prefactor is its own ticket, and it blocks the slices that need it.

### 3. Cut vertical slices

**On the scan path there is no cutting.** One finding is one ticket, in the
scan's own words and at the location it named. Do not merge two findings that
look related, do not subdivide one into layers, and do not invent a slice no
finding produced — re-cutting them silently rewrites the scan's result. Blocking
edges still apply where one finding genuinely gates another, and a prefactor is
still its own ticket. Then go to step 4.

Each ticket is a **tracer bullet**:

- It cuts a narrow but **complete** path through every layer it touches — schema, API, UI, tests. Vertical, never a horizontal slice of one layer.
- It is demoable or verifiable on its own.
- It fits in a single fresh context window.
- Its behavior is observable at a seam **the spec already chose**. A slice whose behavior no chosen seam can observe was cut wrong — re-cut it. Do not add a seam to rescue a cut.
- Prefactors come first.

Give each ticket its **blocking edges**: the tickets that must complete before it can start. A ticket with no blockers can start immediately. An edge is only real if the blocker genuinely gates the work — "it would be tidier in this order" is not a blocking edge.

**Wide refactors are the exception to vertical slicing.** A wide refactor is one mechanical change — rename a column, retype a shared symbol — whose blast radius fans across the codebase, so a single edit breaks thousands of call sites at once and no vertical slice can land green. Do not force it into a tracer bullet. Sequence it as **expand–contract**:

1. **Expand** — add the new form beside the old so nothing breaks.
2. **Migrate** — move the call sites in batches sized by blast radius (per package, per directory). Each batch is its own ticket, blocked by the expand, and stays green because the old form still exists.
3. **Contract** — delete the old form once no caller remains, in a ticket blocked by every migrate batch.

When even the batches cannot stay green alone, keep the sequence but say plainly that green is promised only at a final integrate-and-verify ticket, and make every batch block it.

### 4. Allocate the test names, and mark what is not buildable

Every test name in the spec's Acceptance Criteria section goes to **exactly one** slice, **as written**. Keep the spec's own shape — the criterion, then the test name it maps to — so the trace back to the spec stays visible.

A spec criterion may carry several test names, and they may not all land on the same slice. When that happens, **repeat the criterion line in each slice that carries one of its test names**, with only that slice's test names under it. The criterion is context for reading the test name; a test name with its criterion stripped off is unreadable. Only the test names are exclusive.

| Case | Do |
| --- | --- |
| A slice carries at least one test name | It is buildable. Nothing extra to say. |
| A slice carries none | Write the not-buildable statement in its body, in the exact words `references/ticket-template.md` gives. Do not paraphrase it from memory — the template holds the wording. |
| A test name fits no slice | Report it in step 5 and do not drop it. Either the cut is wrong or the spec specifies something outside its own scope. Both are the user's call. |
| **Scan path: no test names exist at all** | Every ticket carries the not-buildable statement, in the template's exact words. Say so once in step 5 as a property of the batch rather than repeating it per ticket, and do not treat it as a failure — a findings list cannot settle acceptance criteria. |

**Do not invent a test name to close any of these gaps**, and do not soften the not-buildable line. Whoever picks the ticket up needs to know the gap exists before they start.

The spec's **Combined Behavior** list stays on the parent. It is not allocated, not copied, and not split.

### 5. Get the breakdown confirmed

Render every proposed issue completely **into a scratch file under `$TMPDIR`, one per
ticket**, following the template, then present the publish preview from those files.
Render once and read it back; do not compose the body in the preview and again at
creation.

Give each ticket a **distinct title**. Two slices of the same migrate batch will
otherwise collide, and the preview, the scratch files and the read-back all lose
the only handle a human has on which ticket is which.

Present the preview as a numbered list in dependency order, blockers first. For
each ticket, show:

- **Title** — in the project's vocabulary.
- **Blocked by** — the tickets that gate it, or "none".
- **Exact issue body** — the complete Markdown that will be sent to GitHub,
  following the template exactly, in a fenced block so headings and spacing are
  reviewable.

Then state, separately: the total ticket count, **every test name that fitted no slice**, and **which Project the issues will be placed on** — by name, or "none, the parent is on no board", or "none, the token lacks the `project` scope".

#### The order, in the same preview

The user works strictly top-down, so the order the new tickets land in is as
much a part of this approval as their bodies. It is shown in this preview and
approved in the same breath. **No second approval gate is added**, and nothing
about the order is settled after the user has said yes.

Read the whole board in its `POSITION` order, paged to the end, and the repository's
open issues (queries in the procedures file). An open issue **on no board** cannot be
positioned: list those separately by number and title, say they are outside the order
until the user puts them on the board, and do not place them yourself — membership is
inherited from the parent, and these issues have no parent here.

Then build **one total order** over the open issues — the existing ones and the new
ones together:

1. **A blocker comes before everything it blocks.** This is the only hard rule,
   and it applies across the whole board, not just within this breakdown. If the
   existing order already violates it, fixing that is a move, and moves are
   declared below.
2. **Otherwise, keep the existing relative order of existing issues.** The board
   as it stands is the user's order, and rewriting it wholesale is not yours to do.
3. **Place each new ticket by technical risk and dependency** — what it unblocks,
   what breaks or stays broken until it is done, how far its blast radius
   reaches. Not by the order you cut the slices in. On the scan path, follow the
   scan's own severity ranking, adjusted so every blocker precedes what it blocks.

Show the result as a **complete numbered list of every open issue on the board,
after insertion**, top to bottom, marking each line `new` or its existing
number. A list of only the new tickets' positions is not reviewable.

Then state separately **every existing issue that moves**, with its old and new
position and the blocking edge that forced it. An existing issue moving is the
one thing in this preview the user did not ask for, so it is never left to be
noticed in the list.

Say in one line that the order is by technical risk and dependency only, and
that nothing outside the tracker — a waiting customer, a deadline — was
available to rank on.

If the parent is on no board, or the token lacks the `project` scope, say that
no order can be written and that the new issues will arrive wherever GitHub puts
them. Do not invent a substitute ordering surface: no label, no Priority field,
no ordered list in a comment.

Ask the user:

- Is the granularity right — too coarse, too fine?
- Is every blocking edge a real gate?
- Should any tickets be merged or split further?
- Is the order right, and is anything that should be near the top sitting low?

Iterate until the user approves. After any merge, split, wording change, test
allocation change, edge change or reordering, render and show the affected
preview again — and show the order list again whenever an edge changed, because
an edge change can move issues the user was not looking at. The approved titles,
bodies, blocking edges and order are the publish plan.

**Publish nothing before that.** Do not replace the full preview with a summary:
the body the user approves must be the body GitHub receives.

### 6. Publish, in dependency order

Blockers first, so every edge can name an issue that already exists. For each ticket:

1. Create it **from its scratch file**, never by retyping the body, and keep the
   `number` it gets — step 8 matches by number, not title.
2. Capture its database `id`.
3. Attach it to the parent, and add its blocking edges. **Both relations are written
   by `id`, never by `number`.** A number in the `blocked_by` payload returns HTTP 200
   and silently creates a dependency on an unrelated issue in someone else's
   repository. Never treat the 200 as confirmation; step 8 is not optional.
4. If step 1 found a Project, place the issue on it. Placement is idempotent, so a
   failed placement is repaired by running it again. A placement failure does not
   stop the publish and is never silent: finish the rest, then report it in step 8
   with the command to finish it by hand.

**Do not set any Project field, and do not apply any label.** No Status, no Size, no
Priority. Readiness is judged by whether a ticket carries test names. A Priority field
would be a second statement of the order, which step 7 writes as item position.

**Back off on `403` or `429`; never retry.** Publishing is a burst of writes, and a
retry loop creates duplicate issues. Stop, report exactly how far publishing got, and
let the user resume.

### 7. Write the board order

Only after every ticket exists and is on the board. Skip this step entirely, and say
so in step 8's report, if the parent was on no board or the `project` scope is missing.

Re-read the board and **do not reuse the item ids from the preview**; the board may
have moved while the user was reading. The approval was for a board state, not for a
list of numbers. If only the new tickets appeared, write the approved order. If an
existing item moved, or an issue in the approved order is gone from the board,
**stop**, show the difference and let the user decide — leaving the board unordered is
recoverable, and writing an order over someone else's change is not. The procedures
file covers the other two cases (a new unmentioned issue, a closed issue).

Position the items top-down, the first at the top and each next after the one before
it, so a failure halfway leaves a correctly ordered head. Back off on `403` or `429`
as in step 6. Say once in the report that position belongs to the project, and a view
with its own sort will not show it until the sort is cleared.

### 8. Read the issues and graph back, and compare them to what was approved

Read the parent's sub-issues back, paging past every `hasNextPage`, and compare them to
the approved plan, **matching each issue to its plan entry by the `number` captured in
step 6**, not by title:

- Every approved ticket appears as a sub-issue of the parent, and nothing else does.
- Every title and body is identical to the approved preview, **compared mechanically
  with `diff` against its scratch file**, not by reading it. A clean `diff` is the
  check; the presence of headings is not.
- Every criterion and test name still appears exactly as approved, and no test name
  appears in more than one ticket.
- Every blocking edge appears, with no extras, compared node by node (never totals),
  and **every blocker is in this repository**. A blocker from another repository is
  the silent failure above; delete it and redo that edge.
- Every ticket is on the Project the parent is on, and on no other, read back from the
  tracker rather than trusted from `item-add`'s output.
- The board's order matches the approved order, compared position by position over the
  whole board, not by spot-checking.

If something differs, repair it once and read it back again. Stop retrying after one
repair attempt for the same mismatch; report the publish as partial and name the exact
mismatch that remains.

Then report: each ticket by number and title, its blockers by number, the board it was
placed on, its final position, and anything that could not be made to match. If the
order was written, say which existing issues moved. Report a partial publish as
partial — a breakdown that is half-linked is worse than one that is not linked at all,
because it looks finished.

Delete the scratch files once the comparison is done. They are transport; leaving
them behind creates the second record this skill exists to avoid.

### 9. Hand off

Say plainly what comes next: work down the board from the top, and run `dev` on
the first buildable ticket on it. A ticket marked not buildable needs `nathan-grill-me` and `to-spec` again before implementation; splitting did not settle its missing criteria.

On the scan path that covers every ticket published, so say it once about the
batch: these are tracked and ordered, none is buildable, and the top one becomes
buildable by running `nathan-grill-me` on it in a new session and then `to-spec` back
into that same issue.

Then print one ready-to-paste line, with the numbers you just created filled in, for assigning the batch to a milestone:

```
gh issue edit <every created number> --milestone "<name>"
```

**Print it; do not run it and do not ask which milestone.** Which batch belongs to which milestone is a delivery decision, and it is the user's. Leave it out only if the repository has no milestones at all.

Do not invoke anything. Skills in this workflow are not chained inside one session; the user starts the next one.

## Verification

- Exactly one input was named at the start — a spec issue, or a `codebase-scan` findings list confirmed in this same session — not reconstructed at the end.
- The tracker was confirmed writable, and the parent confirmed to have no sub-issues, before any work was done. The parent's comments were read, not only its body.
- On the spec path, the input was confirmed to be a `to-spec` spec, and the seams were quoted from it; none were added, moved or re-chosen. On the scan path, the absence of a spec, of seams and of test names was stated before any ticket was cut.
- On the scan path, the tracking parent was created from the report's own header, scope line and not-covered declarations, carried no findings in its body, and was approved before creation; every child is exactly one finding, unmerged and unsubdivided, and carries the not-buildable statement.
- The codebase was explored before the slices were cut. Every slice is vertical, verifiable on its own, and observable at a seam the spec chose — or is an explicitly sequenced expand–contract step. Every ticket title is distinct.
- Every test name in the spec landed on exactly one ticket, as written. None were invented, none were silently dropped, and any that fitted no slice were reported. Every ticket without a test name carries the not-buildable line. The Combined Behavior list stayed on the parent.
- The breakdown was approved by the user before anything was published. The approval included each ticket's complete rendered body, and the destination Project (inherited from the parent, not chosen; on the scan path, the one board question was about the tracking parent).
- The whole board was read in `POSITION` order, paged to the end, before the order was proposed. The preview showed the complete post-insert order, and named every existing issue that moved and the edge that moved it. The user approved that order in the same approval as the bodies; no second gate was added.
- Every issue was created from its scratch file, not a retyped body, and every published body was compared to its file with `diff`. Published issues were matched to plan entries by captured `number`, and the read-back paged past `first:` wherever `hasNextPage` was true.
- Both relations were written by `id`. The graph was read back and compared node by node, and no blocker belongs to another repository. Any repair was read back once more.
- Every ticket was read back as being on that Project and on no other; an unplaced ticket was reported, with the command to place it.
- Every blocker precedes what it blocks in the written order, and the board was read back after positioning and compared position by position against the approved order.
- The parent's body, title and state are unchanged. No label, no Status, no Size and no Priority or other Project field were set on any issue; the only board write beyond membership was item position.
- The scratch files were deleted at the end, and nothing was written inside the repository.
