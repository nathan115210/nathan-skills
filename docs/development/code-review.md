# code-review

[Execution instructions](../../skills/development/code-review/SKILL.md)

## What it does

Reviews a specified change against repository standards, the originating spec,
and accessibility criteria when UI is involved. It reports each axis separately
and proposes fixes without applying them. It can review a PR, a branch since a
fixed point, or explicitly requested staged/unstaged/untracked work.

## When to reach for it

Invoke explicitly, for example:

- `Use code-review to review this branch against origin/main.`
- `Use code-review for this PR URL and its linked issue.`
- `Use code-review on my uncommitted changes, including these untracked files.`

Specify the scope and known issue or PRD. Explicit references win over inference.
This is a change review; use accessibility-review for an existing UI audit.

## Prerequisites

The relevant source and git revisions must be accessible. A missing PR checkout
is a coverage gap, not permission to review an unrelated local branch. The skill
uses local refs and reports their freshness rather than fetching during review.

A Spec assessment needs an authoritative requirement source. Without one, it
can still review standards but must mark Spec as not assessed. The optional
Accessibility axis reads the sibling skill's shared criteria without invoking
another workflow session.

## Common questions

**Will it review my uncommitted changes?**
Yes, when that is the requested scope. Committed, staged, unstaged and untracked
changes are different inputs; the report must identify what it included.

**Are independent reviewers required?**
The skill uses separate parallel reviewers where supported. Otherwise it performs
separate passes and discloses the lack of context isolation. It inherits the
session model and does not require a separately installed Claude agent type.

**Does it enforce read-only access?**
The instructions prohibit mutations. A platform sandbox can enforce restrictions,
but a Markdown file cannot supply that guarantee. No global agent or hook is
installed. The supplied command-guard prototype is retained as an inert reference
because it admits known writing commands; do not use it as protection.

**Will it post findings on GitHub or fix them?**
No. Reports remain in the conversation. Publication and implementation require
separate user requests.

## It's working if

- It states exactly which revisions or working-tree changes it reviewed.
- Each finding points to an actual changed location and its governing criterion.
- Missing specs, unavailable criteria and unrun tests remain visible gaps.
- Standards, Spec and Accessibility results stay separate.
- It makes no project or tracker changes.

## Known limitations

Static review does not establish runtime correctness or replace QA. The skill
cannot guarantee identical isolation or tool restrictions across providers.
Codex runtime review was not completed because the test account reached its
usage limit. Claude Code runtime behaviour also remains untested.

**A run in agy (2026-09-21, agy 1.2.7)** on uncommitted changes in a task
worktree, with the ticket's spec issue as input. `/code-review` was the only
command of that name in agy's list. It resolved the revision, named the spec
source (issue #2), ran Standards and Spec as independent subagents, and reported
Standards, Spec and Accessibility separately, with Accessibility marked not
assessed because no UI file changed. It wrote nothing. **It missed a real
problem:** the change also implemented behaviour that belonged to a sibling
ticket, and the Spec axis called it fully compliant. Part of the cause was
upstream: the ticket's acceptance criterion had been paraphrased at the CLI level
while its test name was at the function level, so the extra code looked required.
Not tested: whether the Spec axis flags such an addition once the ticket carries
the concrete criterion and its observable, and any run in Claude Code.

## Where it fits

Use after a change is ready for inspection, or explicitly on WIP. The overall
workflow and implemented stages are in the [overview](./README.md).
