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
- Mark every slice the spec cannot make buildable.

**Not yours:**

- **Interviewing for requirements.** If a requirement is still open, name it and stop. Resolving it is `grill-me`, in its own session.
- **Choosing, adding or moving seams.** `to-spec` is the only place seams are decided.
- **Inventing acceptance criteria or test names.** The user sets what counts as correct. You transcribe and allocate.
- **Writing any document.** No `.md` file, no `.scratch/` directory, no local file per ticket. The only exit is issues. A ticket in a file is the second record this workflow exists to avoid.
- **Touching code or git.** No edits, no worktree, no spike, no commit, no push.
- **Rewriting the parent.** You attach children to it. You do not edit its body, change its title, or close it.
- **Labels and Projects.** No readiness label, no Project, no Project field. Readiness is judged by whether a ticket carries test names; a label would be a second copy of that fact and would drift from it.

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

### 1. Read the spec, and state what it can support

Read the body and the comments. Then state, one line each:

- The seams, as the spec named them.
- Whether the spec carries acceptance criteria with test names, or carries `to-spec`'s statement that none were settled.

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

Then three cases, all of which must be handled:

| Case | Do |
| --- | --- |
| A slice carries at least one test name | It is buildable. Nothing extra to say. |
| A slice carries none | Write one line in its body: *No test name in the spec covers this slice. Not buildable — the gap is in the spec, not in this ticket.* |
| A test name fits no slice | Report it in step 5 and do not drop it. Either the cut is wrong or the spec specifies something outside its own scope. Both are the user's call. |

**Do not invent a test name to close any of these gaps**, and do not soften the not-buildable line. Whoever picks the ticket up needs to know the gap exists before they start.

The spec's **Combined Behavior** list stays on the parent. It is not allocated, not copied, and not split.

### 5. Get the breakdown confirmed

Present it as a numbered list in dependency order, blockers first. For each ticket:

- **Title** — in the project's vocabulary.
- **Blocked by** — the tickets that gate it, or "none".
- **What it delivers** — the end-to-end behavior this ticket makes work.
- **Test names it carries** — transcribed, or the not-buildable line.

Then state, separately: the total ticket count, and **every test name that fitted no slice**.

Ask the user:

- Is the granularity right — too coarse, too fine?
- Is every blocking edge a real gate?
- Should any tickets be merged or split further?

Iterate until the user approves. **Publish nothing before that.** Relations are far more tedious to unpick than to get right once, and a wrong edge blocks work that could have started.

### 6. Publish, in dependency order

Blockers first, so every edge can name an issue that already exists.

Read `references/ticket-template.md` for the issue body, and follow it.

Create each ticket and **capture its `id` as well as its `number`**:

```
gh api repos/<owner>/<repo>/issues \
  -f title='<title>' \
  -f body="$(cat <<'BODY'
<the body from the template>
BODY
)" \
  --jq '{number, id}'
```

Then attach it to the parent, and add its blocking edges:

```
gh api -X POST repos/<owner>/<repo>/issues/<parent number>/sub_issues \
  -F sub_issue_id=<child id>

gh api -X POST repos/<owner>/<repo>/issues/<child number>/dependencies/blocked_by \
  -F issue_id=<blocker id>
```

**Both relations are written by issue `id` — the database id returned at creation — not by issue `number`.** The path segment is a number; the payload is an id. Getting this wrong fails in two different ways, and only one of them is loud:

| Wrong input | What happens |
| --- | --- |
| `sub_issues` with a number as `sub_issue_id` | `404 Not Found`. Loud, and safe. |
| `dependencies/blocked_by` with a number as `issue_id` | **HTTP 200, and a dependency on an unrelated issue in a stranger's repository.** The number was read as a database id, and low database ids exist somewhere on GitHub. Silent. |

So: never pass a number as a payload id, and never treat the 200 as confirmation. Step 7 is not optional.

**A count is not a check.** `issueDependenciesSummary.blockedBy` can disagree with the `blockedBy` node list — a cross-repository edge is reachable in the list while the summary does not count it. Compare nodes, never totals.

If you no longer hold an `id`, read it back rather than guessing: `gh api repos/<owner>/<repo>/issues/<number> --jq '.id'`.

To undo an edge: `gh api -X DELETE repos/<owner>/<repo>/issues/<number>/dependencies/blocked_by/<blocker id>`.

**Do not add the issues to a GitHub Project, do not set any Project field, and do not apply any label.** Nothing in this workflow reads them.

### 7. Read the graph back, and compare it to what was approved

```
gh api graphql -f query='
{ repository(owner:"<owner>", name:"<repo>") {
    issue(number: <parent number>) {
      subIssues(first: 50) { nodes { number title blockedBy(first: 20) { nodes { number title repository { nameWithOwner } } } } }
    }
} }' --jq '.data'
```

Compare the **node lists**, name by name, against the breakdown the user approved:

- Every approved ticket appears as a sub-issue of the parent, and nothing else does.
- Every blocking edge appears, with no extras, and **every blocker is in this repository**. A blocker from another repository is the silent failure above; delete it and redo that edge.

Then report: each ticket by number and title, its blockers by number, and any edge you could not create. Report a partial publish as partial — a breakdown that is half-linked is worse than one that is not linked at all, because it looks finished.

### 8. Hand off

Say plainly what comes next: run `dev` on a buildable ticket. A ticket marked not buildable needs `grill-me` and `to-spec` again before implementation; splitting did not settle its missing criteria.

Do not invoke anything. Skills in this workflow are not chained inside one session; the user starts the next one.

## Verification

- Exactly one spec issue was the input, and it was named at the start — not reconstructed at the end.
- Its comments were read, not only its body.
- The tracker was confirmed writable before the work was done.
- The seams were quoted from the spec. None were added, moved or re-chosen.
- The codebase was explored before the slices were cut.
- Every slice is vertical, verifiable on its own, and observable at a seam the spec chose — or is an explicitly sequenced expand–contract step.
- Every test name in the spec landed on exactly one ticket, as written. None were invented, none were silently dropped, and any that fitted no slice were reported.
- Every ticket without a test name carries the not-buildable line.
- The Combined Behavior list stayed on the parent.
- The breakdown was approved by the user before anything was published.
- Both relations were written by `id`. The graph was read back and compared node by node, and no blocker belongs to another repository.
- The parent's body, title and state are unchanged. No label, no Project.
- No file was written.
