# accessibility-review

[Execution instructions](../../skills/development/accessibility-review/SKILL.md)

## What it does

Reviews supplied designs, local UI code, or both. The design path uses seven
illustrative personas to expose barriers and identify real-user testing needs.
The code path inspects source for evidenced accessibility findings and separates
those from questions that require a running interface.

For a combined review it presents design and code reports, then reconciles their
agreement, differences and coverage gaps. It changes nothing in the project and
publishes nothing. The single file it writes is its own report, saved to
`~/Downloads/a11y-<topic>.md` so the findings survive the session that produced
them.

## When to reach for it

Invoke explicitly with an artifact or source scope, for example:

- `Use accessibility-review on this account-opening wireframe.`
- `Use accessibility-review to audit src/components for accessibility barriers.`
- `Use accessibility-review on this design and its implementation.`

A clear request starts directly. An ambiguous one prompts for design, code or
both. If one input is missing, the report names that gap instead of imagining it.

## Prerequisites

Provide something the agent can inspect: an image, accessible design link, flow
or copy, source file or directory. Missing connectors and inaccessible frames
limit coverage. No repository is cloned and no audit tools are installed.

WCAG 2.1 AA is the default technical baseline. A project can specify another
version/level. The supplied Nordea checklist and Nordic banking personas remain
available, but organization-specific requirements apply only to matching work.
They are not assumed to govern every project using this skill.

## Common questions

**Is the panel actual customer feedback?**
No. It is an explicitly labelled simulation. The supplied profiles have unverified
research provenance; generated quotations must never be presented as participant
observations. The report identifies who to recruit for real testing.

**Does a clean code report prove compliance?**
No. Focus order, announcements, rendered contrast and zoom behaviour commonly
need runtime or manual checks. This skill does not certify WCAG, EAA or national
legal compliance.

**Does every search match become a finding?**
No. Native controls may already supply semantics; labels and focus styles may
be defined elsewhere. The reviewer must check context and standards applicability
before asserting a failure. Advisory practices remain distinct from requirements.

**What does code-review use from this skill?**
Only the static criteria for its changed UI scope. It does not run the persona
panel or silently expand a small diff into a whole-repository audit.

**It found real bugs. How do they get fixed?**
Not here. The report names barriers; it does not decide which are in scope, in
what order, or what counts as fixed. Take the saved report to `grill-me` in a
new session — that is where findings become acceptance criteria and test names,
and `to-spec` turns those into an issue. The review session's context is spent
on the review, which is why the report is a file and not a conversation.

**Can I skip `grill-me` and go straight to `to-spec`?**
Only when you have already decided, yourself, which findings are in scope and
what each one's acceptance criteria are. `to-spec` transcribes settled
decisions; a findings list is not one. Nothing stops you — but the skill will
not propose it, because choosing what to fix is your call, not the reviewer's.

## It's working if

- It identifies which artifact/path and which scope were actually reviewed.
- Simulated voices are labelled and grounded in visible elements.
- Code findings name the barrier, location and correct criterion/version/level.
- A normal native button is not flagged for lacking an explicit keyboard handler.
- Unobservable behaviour is listed as a runtime/manual check, not a confirmed bug.
- The saved report opens with an identity line naming the project, states the
  scope that ran, and contains the report in full rather than a summary.
- It ends by pointing at `grill-me` in a new session, and stops there: it does
  not invoke the next skill, offer to run it, or start fixing anything.

## Known limitations

The supplied Nordea snapshot and persona provenance have not been independently
verified. The design path cannot infer interaction behaviour from a still image.
Static code analysis is not an exhaustive accessibility audit. One bounded
Codex source-review example completed; design, combined, Claude Code and agy
runtime paths remain untested. The report file and its handoff to `grill-me`
are unverified at runtime. A tool mode that forbids writes leaves the report in
the conversation only, and it is then lost with the session.

## Where it fits

Available for a focused design or code review, independently of the development
chain: it needs no prior step and planning may stop at its report. When the
findings should be fixed and tracked, its report is the input to `grill-me`,
which feeds `to-spec` as usual. See the [workflow overview](./README.md).
