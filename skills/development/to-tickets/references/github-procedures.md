# GitHub procedures

The exact commands and failure modes behind `SKILL.md`'s steps. `SKILL.md` says what
state each step must reach and what the user must approve; this file says how to
read and write GitHub without corrupting the result. Read the section for the step
you are on. Nothing here changes a decision `SKILL.md` makes.

## Step 0 — writable, unsplit, Project scope

Confirm the tracker is writable before doing the work:

```
gh repo view --json nameWithOwner,viewerPermission -q '.nameWithOwner + " " + .viewerPermission'
```

| Outcome | Do |
| --- | --- |
| `ADMIN`, `MAINTAIN` or `WRITE` | Publish. |
| `READ`, `TRIAGE`, or `gh` is not authenticated | Stop. Say exactly what failed and which account it checked. |
| No GitHub repo here | Stop. Say so. Do not look for another tracker. |

In the last two cases, **do not fall back to writing tickets to files.** Print the
proposed breakdown in this conversation so the user can place it themselves, and say
plainly that nothing was published. An unpublished breakdown is a blocked step, not a
reason to change medium.

Check the parent has not already been split:

```
gh api graphql -f query='
{ repository(owner:"<owner>", name:"<repo>") {
    issue(number: <parent number>) { subIssues(first: 1) { totalCount } }
} }' --jq '.data.repository.issue.subIssues.totalCount'
```

**Anything other than `0` stops you.** There is no re-split and no reconciliation:
publishing again creates a second complete set of children beside the first. Say how
many children the parent already has, list them, and let the user decide — finish an
interrupted run by hand, unpick the first set, or split a different issue. Do not
offer to "add the missing ones"; you cannot tell which are missing without the first
run's approved plan, and it is gone.

This check exists because the natural response to any failure in step 6 — a dropped
connection, a rate limit, a closed session — is to run the skill again, and that is
exactly the action that doubles the breakdown.

Check the token can write to Projects:

```
gh auth status 2>&1 | grep 'Token scopes'
```

**`repo` does not cover Projects v2; `project` is a separate scope.** A token without
it passes every check above and then fails at `gh project item-add` — after the issues
already exist. If `project` is missing, give the user the fix
(`gh auth refresh -s project`). Do not stop for it.

## Step 1 — the parent's Project

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

**Use this query, not `gh issue view --json projectItems`.** The CLI field returns
only the project's `title` and the item's field values — no `number`, no `owner` — and
`gh project item-add` needs both. Take the owner `login` from the parent's own item
rather than from the repository: a personal Project can hold issues from an
organization repository, so the repository owner is not reliably the Project owner.

## Step 5 — read the board and the open issues

```
gh project view <project number> --owner <owner login> --format json --jq '.id'

gh api graphql -f query='
query($project: ID!, $cursor: String) {
  node(id: $project) { ... on ProjectV2 {
    items(first: 100, after: $cursor, orderBy: {field: POSITION, direction: ASC}) {
      pageInfo { hasNextPage endCursor }
      nodes { id content { __typename
        ... on Issue { number title state
          blockedBy(first: 20) { nodes { number } } }
        ... on PullRequest { number state } } }
    }
  } }
}' -f project='<project id>' --jq '.data.node.items'
```

`POSITION` is the board's manual order and the only order GitHub stores. **Page until
`hasNextPage` is `false`**, adding `-f cursor='<endCursor>'` from the previous page —
omit `cursor` entirely on the first call rather than passing an empty string. A
truncated list silently drops the tail of the backlog, and everything you then insert
lands above issues you never saw. Ignore closed issues and pull-request items.

`blockedBy` comes back with each item so the blocker-first rule can be checked against
the board as it is, not only against the edges this breakdown adds.

Then list the repository's open issues, to find the ones the board does not hold:

```
gh issue list --state open --limit 200 --json number,title
```

## Step 6 — publish

Create each ticket **from its scratch file**, never by retyping the body:

```
TITLE=$(cat <<'TITLE_EOF'
<the approved title>
TITLE_EOF
)
gh issue create --title "$TITLE" --body-file "$TMPDIR/to-tickets-<slug>.md"
```

The title goes through a variable rather than inside quotes because an apostrophe in a
title — common in English ticket titles — breaks `-f title='…'` and can truncate the
title silently.

`gh issue create` prints the new issue's URL; its last path segment is the `number`.
**Capture the database `id` too**, because both relations need it:

```
gh api repos/<owner>/<repo>/issues/<number> --jq '.id'
```

Keep the `number` you captured. It, not the title, is what step 8 uses to match a
published issue to its plan entry.

Attach it to the parent, and add its blocking edges:

```
gh api -X POST repos/<owner>/<repo>/issues/<parent number>/sub_issues \
  -F sub_issue_id=<child id>

gh api -X POST repos/<owner>/<repo>/issues/<child number>/dependencies/blocked_by \
  -F issue_id=<blocker id>
```

If step 1 found a Project, place the issue on it:

```
gh project item-add <project number> --owner <project owner login> --url <issue url>
```

**Placement is idempotent — re-running it is safe.** Adding an issue that is already on
the board returns the item it already has and exits `0`, without creating a second
card. Repairing a failed placement is running the same command again.

**A placement failure does not stop the publish and is never silent.** Finish the
remaining tickets and their edges, then report the placement as incomplete in step 8
and give the user the command to finish it by hand. Placing half a breakdown on a
board and saying nothing is the one outcome to avoid.

**Do not set any Project field, and do not apply any label.** A Project with GitHub's
default *item added → Todo* workflow enabled will set Status by itself; that is the
board's own rule acting, and it is not yours to pre-empt or to duplicate. A Priority
field is not how the order is written: it would be a second statement of the ranking,
kept in step by hand. Step 7 writes the item's position.

**Back off rather than retry on `403` or `429`.** Publishing is a burst of
content-creating requests — a create, a sub-issue attach, one call per blocking edge
and one per board placement, per ticket — which is the shape GitHub's secondary rate
limits target. A retry loop does not recover; it creates duplicate issues. Stop, report
exactly how far publishing got, and let the user resume.

**Both relations are written by issue `id` — the database id returned at creation — not
by issue `number`.** The path segment is a number; the payload is an id.

| Wrong input | What happens |
| --- | --- |
| `sub_issues` with a number as `sub_issue_id` | `404 Not Found`. Loud, and safe. |
| `dependencies/blocked_by` with a number as `issue_id` | **HTTP 200, and a dependency on an unrelated issue in a stranger's repository.** The number was read as a database id, and low database ids exist somewhere on GitHub. Silent. |

Never pass a number as a payload id, and never treat the 200 as confirmation. Step 8
is not optional.

**A count is not a check.** `issueDependenciesSummary.blockedBy` can disagree with the
`blockedBy` node list — a cross-repository edge is reachable in the list while the
summary does not count it. Compare nodes, never totals.

If you no longer hold an `id`, read it back rather than guessing:
`gh api repos/<owner>/<repo>/issues/<number> --jq '.id'`.

To undo an edge:
`gh api -X DELETE repos/<owner>/<repo>/issues/<number>/dependencies/blocked_by/<blocker id>`.

## Step 7 — write the board order

Re-read the board with the paged query from step 5. **Do not reuse the item ids from
the preview** — placement created the new items, and the board may have moved while the
user was reading. Compare what comes back to the approved order and act on the
difference, because the approval was for a board state, not for a list of numbers:

| What changed | Do |
| --- | --- |
| Nothing but the new tickets appearing | Write the order. |
| An open issue exists that the approved order does not mention | Write the approved order, then report that issue as unordered and where it ended up. Do not guess a position for it. |
| An issue in the approved order has closed | Write the order over what remains, skipping it, and say so. |
| An existing item has moved, or an issue in the approved order is gone from the board | **Stop.** Show the difference and let the user decide. The tickets are already published; leaving the board unordered is recoverable, and writing an order over someone else's change is not. |

Then position the items from the top down:

```
gh api graphql -f query='
mutation($project: ID!, $item: ID!, $after: ID) {
  updateProjectV2ItemPosition(input: {projectId: $project, itemId: $item, afterId: $after}) {
    items(first: 1) { totalCount }
  }
}' -f project='<project id>' -f item='<item id>' -f after='<the id of the item it goes below>'
```

**Omit `-f after` entirely for the first item** — with no `afterId`, the item moves to
the **top** of the board. Do not pass an empty string for it.

Walk the approved order from first to last: place the first item at the top, then each
following item after the one before it. Working top-down means each mutation's
`afterId` is an item already in its final position, so a failure halfway leaves a
correctly ordered head and an untouched tail, rather than an order interleaved with the
old one.

**Back off rather than retry on `403` or `429`**, exactly as in step 6. One mutation
per item is another burst against the same secondary rate limit. A half-written order
is recoverable — report where it stopped — but a retry loop against a rate limit is
not progress.

Position is a property of the **project**, not of a view. A view with its own sort
applied displays that sort instead, and the order written here will not be visible in
it until the sort is cleared.

## Step 8 — read back

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

**Check `hasNextPage` on every connection before comparing anything.** Both `first:`
values are caps, and past them the query returns a truncated list that looks complete.
The assertion that nothing *other* than the approved tickets is attached silently
becomes unprovable on a truncated list. If either `hasNextPage` is `true`, page through
until it is `false` and compare the whole set.

Compare the body **mechanically against its scratch file**, not by reading it:

```
gh api repos/<owner>/<repo>/issues/<number> --jq '.body' \
  | diff - "$TMPDIR/to-tickets-<slug>.md"
```

`--jq` appends a trailing newline of its own, so strip that one byte before diffing or
every rendered ticket reports a spurious mismatch. A clean `diff` is the check.
Checking that the headings are present is not — that is what a body mangled by quoting
still looks like.

Read each child's Project membership back with the step 1 `projectItems` query, run
against the child rather than the parent. Do not trust `item-add`'s own output: it
reports the item it created, not the set of items on the board. Read the whole board
back with the paged `POSITION` query and compare position by position. Do not trust the
mutation responses: each reports its own item, and the order is a property of the list.

If a created issue's title or body differs, update it from the scratch file
(`gh issue edit <number> --body-file …`) and diff it again. If a relation differs,
repair it and read the graph back again. Stop retrying after one repair attempt for the
same mismatch.
