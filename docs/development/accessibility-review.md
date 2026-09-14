# accessibility-review

[Execution instructions](../../skills/development/accessibility-review/SKILL.md)

## What it does

Reviews supplied designs, local UI code, or both. The design path uses seven
illustrative personas to expose barriers and identify real-user testing needs.
The code path inspects source for evidenced accessibility findings and separates
those from questions that require a running interface.

For a combined review it presents design and code reports, then reconciles their
agreement, differences and coverage gaps. It makes no changes or publications.

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

## It's working if

- It identifies which artifact/path and which scope were actually reviewed.
- Simulated voices are labelled and grounded in visible elements.
- Code findings name the barrier, location and correct criterion/version/level.
- A normal native button is not flagged for lacking an explicit keyboard handler.
- Unobservable behaviour is listed as a runtime/manual check, not a confirmed bug.

## Known limitations

The supplied Nordea snapshot and persona provenance have not been independently
verified. The design path cannot infer interaction behaviour from a still image.
Static code analysis is not an exhaustive accessibility audit. One bounded
Codex source-review example completed; design, combined, Claude Code and agy
runtime paths remain untested.

## Where it fits

Available for a focused design or code review, independently of the development
chain. See the [workflow overview](./README.md).
