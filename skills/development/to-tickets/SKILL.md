---
name: to-tickets
description: Split one spec issue into sub-issues carrying native blocking relations — read the spec, cut tracer-bullet slices, allocate its test names, get the breakdown confirmed, then publish to GitHub. No requirements interview, no seam choice, no code.
disable-model-invocation: true
disallowed-tools: Write, Edit, NotebookEdit
---

# To Tickets

You are the only splitter in this workflow. One spec issue goes in; its sub-issues and their blocking relations come out.

Three things happen here and nowhere else:

1. The work is cut into slices, and each slice declares what blocks it.
2. The spec's test names are allocated to those slices.
3. The slices the spec cannot make buildable are marked as such, in writing.

## Inputs

Exactly one **spec issue**, in this project's tracker, named by number or URL.

| Input | Where it is | How to read it |
| --- | --- | --- |
| **A spec issue** — the only case | GitHub, in the repository you are standing in | `gh issue view <n> --comments`. Read the body and the comments. |

If the user did not name one, ask. Do not search the tracker for a plausible spec — splitting the wrong issue produces a breakdown that looks right.

**Do not accept a file.** A planning PRD is `grill-me`'s output and `to-spec`'s input; it is expected to be stale by now. If the user offers a document instead of an issue, the missing step is `to-spec`, in its own session.

The body holds the specification; the comments hold process records. Both are input — a correction that arrived as a comment is still a decision.

### What the spec already settled, and you do not revisit

| Settled | Where it lives | Here |
| --- | --- | --- |
| The **seams** | The spec's Seams section | Used. Never re-chosen, never added to. |
| The **requirements** | The whole spec | Not reopened. An open requirement stops you. |
| The **acceptance criteria and test names** | The spec's Acceptance Criteria section | Transcribed and allocated. Never invented. |
| The **combined behavior** | The spec's Combined Behavior section | Left on the parent. Never copied into a ticket. |

Seam count is a whole-codebase property, which is why it is settled once per spec rather than once per ticket. Choosing per ticket multiplies seams by construction. Combined behavior is a property of the whole, and the whole is only visible at the parent.

## Boundaries

**Yours:**

- Read code, history, and existing issues.
- Cut the slices and their blocking edges, and get them confirmed.
- Create the sub-issues and both kinds of relation.
- Put each new issue in the Project the parent is already in, when it is in one.
- Mark every slice the spec cannot make buildable.

**Not yours:**

- **Interviewing for requirements.** If a requirement is still open, name it and stop. Resolving it is `grill-me`, in its own session.
- **Choosing, adding or moving seams.** `to-spec` is the only place seams are decided.
- **Inventing acceptance criteria or test names.** The user sets what counts as correct. You transcribe and allocate.
- **Writing any document.** No `.md` file, no `.scratch/` directory, no local file per ticket. The only exit is issues. A ticket in a file is the second record this workflow exists to avoid.

  *One narrow exception, and it is transport rather than a record:* the approved body of each ticket is held in a scratch file under `$TMPDIR` between step 5 and the end of step 7, so that the text you show the user, the text GitHub receives, and the text you compare against afterwards are one string rather than three transcriptions of it. Those files live outside the repository, are never a source of truth after publication, and are deleted at the end of step 7. Writing a ticket anywhere inside the repository is still forbidden.
- **Touching code or git.** No edits, no worktree, no spike, no commit, no push.
- **Rewriting the parent.** You attach children to it. You do not edit its body, change its title, or close it.
- **Labels, and Project fields.** No readiness label; no Status, Priority or Size; no custom field of any kind. Readiness is judged by whether a ticket carries test names, and a label or a field would be a second copy of that fact that drifts from it. Setting a field is also the user's first pass over their own board, not yours.

Project **membership** is not in that list, and is deliberately not treated like a label. Putting an issue on a board copies no fact — it does not restate the test names, the parent relation or the blocking edges — so there is nothing for it to drift from. It is a view, and it is the user's view of this work.

## Process

### 0. Name the input, and check you can publish

State which issue you are splitting, by number and title. One line.

Then confirm the tracker is writable **before doing the work**, not after:

```
gh repo view --json nameWithOwner,viewerPermission -q '.nameWithOwner + " " + .viewerPermission'
```

| Outcome | Do |
| --- | --- |
| `ADMIN`, `MAINTAIN` or `WRITE` | Publish. |
| `READ`, `TRIAGE`, or `gh` is not authenticated | Stop. Say exactly what failed and which account it checked. |
| No GitHub repo here | Stop. Say so. Do not look for another tracker. |

In the last two cases, **do not fall back to writing tickets to files.** Print the proposed breakdown in this conversation so the user can place it themselves, and say plainly that nothing was published. An unpublished breakdown is a blocked step, not a reason to change medium.

Then check the parent has not already been split:

```
gh api graphql -f query='
{ repository(owner:"<owner>", name:"<repo>") {
    issue(number: <parent number>) { subIssues(first: 1) { totalCount } }
} }' --jq '.data.repository.issue.subIssues.totalCount'
```

**Anything other than `0` stops you.** There is no re-split and no reconciliation
here: publishing again creates a second complete set of children beside the
first. Say how many children the parent already has, list them, and let the user
decide — finish an interrupted run by hand, unpick the first set, or split a
different issue. Do not offer to "add the missing ones"; you cannot tell which
are missing without the first run's approved plan, and it is gone.

This check exists because the natural response to any failure in step 6 — a
dropped connection, a rate limit, a closed session — is to run the skill again,
and that is exactly the action that doubles the breakdown.

Then check the token can write to Projects, because step 6 may need to:

```
gh auth status 2>&1 | grep 'Token scopes'
```

**`repo` does not cover Projects v2; `project` is a separate scope.** A token
without it passes every check above and then fails at `gh project item-add` —
after the issues already exist. If `project` is missing, say so here and give the
user the fix (`gh auth refresh -s project`). Do not stop for it: the issues and
their relations are the deliverable, and the board is not. Carry the gap into
step 5 so the user approves a breakdown knowing it will not be placed.

### 1. Read the spec, and state what it can support

First check the issue is a spec at all. A `to-spec` spec carries a **Seams**
section and an **Acceptance Criteria and Test Names** section. If the body has
neither, **stop**: this is an ordinary issue, and splitting it would mean
inferring seams from prose — the one thing this skill must never do. Say which
sections are missing and that the step in front of you is `to-spec`.

A spec that has both sections but no test names under the second is a different
case entirely, and it does not stop you — see below.

Then read the body and the comments, and state, one line each:

- The seams, as the spec named them.
- Whether the spec carries acceptance criteria with test names, or carries `to-spec`'s statement that none were settled.
- The Project the new issues will join, or that there is none.

**The destination Project is inherited from the parent, never chosen and never asked for.** Whatever board the spec issue is already on is where its children go; if the parent is on no board, the children go on none. That rule needs no configuration, cannot pick the wrong board, and gives the user an opt-out they already control — leave the spec issue off a board and nothing is placed.

```
gh api graphql -f query='
{ repository(owner:"<owner>", name:"<repo>") {
    issue(number: <parent number>) {
      projectItems(first: 10) { nodes { project {
        number title owner { __typename ... on User { login } ... on Organization { login } }
      } } }
    }
} }' --jq '.data.repository.issue.projectItems.nodes[].project'
```

**Use this query, not `gh issue view --json projectItems`.** The CLI field returns only the project's `title` and the item's field values — no `number`, no `owner` — and `gh project item-add` needs both. Take the owner `login` from the parent's own item rather than from the repository: a personal Project can hold issues from an organization repository, so the repository owner is not reliably the Project owner.

If the parent is on more than one board, put the children on all of them, and say which in step 5.

**A spec with no test names is still worth splitting, and splitting it does not make it buildable.** Cut the slices, then say so per ticket in step 4. Do not stop, and do not fill the gap — `to-spec` deliberately left it visible.

### 2. Explore the codebase

Not optional, and not skippable on the grounds that the spec is detailed. Slices are a property of the code.

Find the current state of the area, the vocabulary already in use, and any conventions or ADRs that constrain it. Write ticket titles in the project's own vocabulary.

Look for **prefactoring** — a change that makes the real change easy. Make the change easy, then make the easy change. A prefactor is its own ticket, and it blocks the slices that need it.

### 3. Cut vertical slices

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

A spec criterion may carry several test names, and they may not all land on the same slice. When that happens, **repeat the criterion line in each slice that carries one of its test names**, with only that slice's test names under it. The criterion is context for reading the test name; a test name with its criterion stripped off is unreadable, and splitting a criterion's text is not the same as splitting its test names. Only the test names are exclusive.

Then three cases, all of which must be handled:

| Case | Do |
| --- | --- |
| A slice carries at least one test name | It is buildable. Nothing extra to say. |
| A slice carries none | Write the not-buildable statement in its body, in the exact words `references/ticket-template.md` gives. Do not paraphrase it from memory — the template holds the wording. |
| A test name fits no slice | Report it in step 5 and do not drop it. Either the cut is wrong or the spec specifies something outside its own scope. Both are the user's call. |

**Do not invent a test name to close any of these gaps**, and do not soften the not-buildable line. Whoever picks the ticket up needs to know the gap exists before they start.

The spec's **Combined Behavior** list stays on the parent. It is not allocated, not copied, and not split.

### 5. Get the breakdown confirmed

Read `references/ticket-template.md` now. Render every proposed issue completely
**into a scratch file under `$TMPDIR`, one per ticket**, then present the publish
preview from those files. Render once and read it back; do not compose the body
in the preview and again at creation.

Give each ticket a **distinct title**. Two slices of the same migrate batch will
otherwise collide, and the preview, the scratch files and the read-back all lose
the only handle a human has on which ticket is which.

Present the preview as a numbered list in dependency order, blockers first. For
each ticket, show:

- **Title** — in the project's vocabulary.
- **Blocked by** — the tickets that gate it, or "none".
- **Exact issue body** — the complete Markdown that will be sent to GitHub,
  following the template exactly. Put it in a fenced block so headings and
  spacing are reviewable.

Then state, separately: the total ticket count, **every test name that fitted no slice**, and **which Project the issues will be placed on** — by name, or "none, the parent is on no board", or "none, the token lacks the `project` scope".

Ask the user:

- Is the granularity right — too coarse, too fine?
- Is every blocking edge a real gate?
- Should any tickets be merged or split further?

Iterate until the user approves. After any merge, split, wording change, test
allocation change, or edge change, render and show the affected preview again.
The approved titles, bodies, and blocking edges are the publish plan.

**Publish nothing before that.** Do not replace the full preview with a summary:
the body the user approves must be the body GitHub receives. Relations are far
more tedious to unpick than to get right once, and a wrong edge blocks work that
could have started.

### 6. Publish, in dependency order

Blockers first, so every edge can name an issue that already exists.

Create each ticket **from its scratch file**, never by retyping the body:

```
TITLE=$(cat <<'TITLE_EOF'
<the approved title>
TITLE_EOF
)
gh issue create --title "$TITLE" --body-file "$TMPDIR/to-tickets-<slug>.md"
```

The title goes through a variable rather than inside quotes because an
apostrophe in a title — common in English ticket titles — breaks `-f title='…'`
and can truncate the title silently.

`gh issue create` prints the new issue's URL; its last path segment is the
`number`. **Capture the database `id` too**, because both relations need it:

```
gh api repos/<owner>/<repo>/issues/<number> --jq '.id'
```

Keep the `number` you captured here. It, not the title, is what step 7 uses to
match a published issue to its plan entry.

Then attach it to the parent, and add its blocking edges:

```
gh api -X POST repos/<owner>/<repo>/issues/<parent number>/sub_issues \
  -F sub_issue_id=<child id>

gh api -X POST repos/<owner>/<repo>/issues/<child number>/dependencies/blocked_by \
  -F issue_id=<blocker id>
```

Then, if step 1 found a Project, place the issue on it:

```
gh project item-add <project number> --owner <project owner login> --url <issue url>
```

**Placement is idempotent — re-running it is safe.** Adding an issue that is already on the board returns the item it already has and exits `0`, without creating a second card. So when placement is the only thing that failed, repairing it is simply running the same command again; there is nothing to check first and nothing to undo.

**A failure here does not stop the publish and is never silent.** The issues and
their relations are the deliverable; the board is a view of it. On failure,
finish the remaining tickets and their edges, then report the placement as
incomplete in step 7 and give the user the command to finish it by hand. Placing
half a breakdown on a board and saying nothing is the one outcome to avoid — the
board then looks like the whole breakdown.

**Do not set any Project field, and do not apply any label.** No Status, no
Priority, no Size. Readiness is already judged by whether a ticket carries test
names, and the first pass over the board is the user's. A Project with GitHub's
default *item added → Todo* workflow enabled will set Status by itself; that is
the board's own rule acting, and it is not yours to pre-empt or to duplicate.

**Back off rather than retry on `403` or `429`.** Publishing a breakdown is a
burst of content-creating requests — a create, a sub-issue attach, one call per
blocking edge and one per board placement, per ticket — which is the exact shape
GitHub's secondary rate limits target. A retry loop here does not recover; it
creates duplicate issues. Stop, report exactly how far publishing got, and let
the user resume.

**Both relations are written by issue `id` — the database id returned at creation — not by issue `number`.** The path segment is a number; the payload is an id. Getting this wrong fails in two different ways, and only one of them is loud:

| Wrong input | What happens |
| --- | --- |
| `sub_issues` with a number as `sub_issue_id` | `404 Not Found`. Loud, and safe. |
| `dependencies/blocked_by` with a number as `issue_id` | **HTTP 200, and a dependency on an unrelated issue in a stranger's repository.** The number was read as a database id, and low database ids exist somewhere on GitHub. Silent. |

So: never pass a number as a payload id, and never treat the 200 as confirmation. Step 7 is not optional.

**A count is not a check.** `issueDependenciesSummary.blockedBy` can disagree with the `blockedBy` node list — a cross-repository edge is reachable in the list while the summary does not count it. Compare nodes, never totals.

If you no longer hold an `id`, read it back rather than guessing: `gh api repos/<owner>/<repo>/issues/<number> --jq '.id'`.

To undo an edge: `gh api -X DELETE repos/<owner>/<repo>/issues/<number>/dependencies/blocked_by/<blocker id>`.


### 7. Read the issues and graph back, and compare them to what was approved

```
gh api graphql -f query='
{ repository(owner:"<owner>", name:"<repo>") {
    issue(number: <parent number>) {
      subIssues(first: 50) {
        totalCount
        pageInfo { hasNextPage }
        nodes { number title body blockedBy(first: 20) {
          totalCount pageInfo { hasNextPage }
          nodes { number title repository { nameWithOwner } }
        } }
      }
    }
} }' --jq '.data'
```

**Check `hasNextPage` on every connection before comparing anything.** Both
`first:` values are caps, and past them the query returns a truncated list that
looks complete. The strongest assertion below — that nothing *other* than the
approved tickets is attached — silently becomes unprovable on a truncated list.
If either `hasNextPage` is `true`, page through until it is `false` and compare
the whole set; never compare a partial one.

Compare the returned issues against the publish plan the user approved, **matching each returned issue to its plan entry by the `number` captured in step 6**, not by title:

- Every approved ticket appears as a sub-issue of the parent, and nothing else does.
- Every title and body is identical to the approved preview. Compare the body
  **mechanically against its scratch file**, not by reading it:

  ```
  gh api repos/<owner>/<repo>/issues/<number> --jq -r '.body' \
    | diff - "$TMPDIR/to-tickets-<slug>.md"
  ```

  A clean `diff` is the check. Checking that the headings are present is not —
  that is what a body mangled by quoting still looks like.
- Every criterion and test name still appears exactly as approved, and no test
  name appears in more than one ticket.
- Every blocking edge appears, with no extras, and **every blocker is in this repository**. A blocker from another repository is the silent failure above; delete it and redo that edge.
- Every ticket is on the Project the parent is on, and on no other. Read it back
  with the same `projectItems` query from step 1, against each child rather than
  the parent. Do not trust `item-add`'s own output: it reports the item it
  created, not the set of items on the board.

If a created issue's title or body differs, update it from the scratch file
(`gh issue edit <number> --body-file …`) and diff it again. If a relation differs, repair it and read the graph back
again. Stop retrying after one repair attempt for the same mismatch; report the
publish as partial and name the exact mismatch that remains.

Then report: each ticket by number and title, its blockers by number, the board
it was placed on, and any title, body, sub-issue relation, blocking edge, or
board placement that could not be made to match.
Report a partial publish as partial — a breakdown that is half-linked is worse
than one that is not linked at all, because it looks finished.

Delete the scratch files once the comparison is done. They are transport; leaving
them behind creates the second record this skill exists to avoid.

### 8. Hand off

Say plainly what comes next: run `dev` on a buildable ticket. A ticket marked not buildable needs `grill-me` and `to-spec` again before implementation; splitting did not settle its missing criteria.

Then print one ready-to-paste line, with the numbers you just created filled in, for assigning the batch to a milestone:

```
gh issue edit <every created number> --milestone "<name>"
```

**Print it; do not run it and do not ask which milestone.** Which batch belongs to which milestone is a delivery decision, and it is the user's. This is a convenience at the moment the numbers are in front of them, not a step — leave it out only if the repository has no milestones at all.

Do not invoke anything. Skills in this workflow are not chained inside one session; the user starts the next one.

## Verification

- Exactly one spec issue was the input, and it was named at the start — not reconstructed at the end.
- The parent was confirmed to have no sub-issues before any work was done.
- Its comments were read, not only its body.
- The tracker was confirmed writable before the work was done.
- The seams were quoted from the spec. None were added, moved or re-chosen.
- The codebase was explored before the slices were cut.
- Every slice is vertical, verifiable on its own, and observable at a seam the spec chose — or is an explicitly sequenced expand–contract step.
- Every test name in the spec landed on exactly one ticket, as written. None were invented, none were silently dropped, and any that fitted no slice were reported.
- Every ticket without a test name carries the not-buildable line.
- The Combined Behavior list stayed on the parent.
- The input was confirmed to be a `to-spec` spec — it carried a Seams section and an Acceptance Criteria section — before it was split.
- Every ticket title is distinct.
- The breakdown was approved by the user before anything was published.
- The approved breakdown included each ticket's complete rendered body, every issue was created from that same scratch file rather than from a retyped body, and every published body was compared to its file with `diff`.
- The read-back paged past `first:` wherever `hasNextPage` was true, and published issues were matched to plan entries by captured `number`, not by title.
- The scratch files were deleted at the end, and nothing was written inside the repository.
- Both relations were written by `id`. The graph was read back and compared node by node, and no blocker belongs to another repository.
- Every created title and complete body was read back and matched against the
  approved preview; any repair was read back once more.
- The destination Project was inherited from the parent, not chosen or asked for, and was named in the preview before approval.
- Every ticket was read back as being on that Project and on no other; an unplaced ticket was reported, with the command to place it.
- The parent's body, title and state are unchanged. No label and no Project field were set on any issue.
- No file was written.
