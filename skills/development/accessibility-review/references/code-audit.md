# Accessibility audit: code path

Use for the code branch of accessibility-review, or as criteria for the
Accessibility axis of code-review. Paths mentioned by the caller define scope.
For a diff, report only newly introduced or worsened barriers. For an audit of a
path, existing barriers are in scope. Never silently substitute one for the other.

## Discover and inspect

Read the applicable parts of [accessibility-checklist.md](./accessibility-checklist.md).
Find UI source: web HTML, JSX/TSX, Vue, Svelte and templates; CSS and preprocessors;
iOS Swift, storyboards and XIB; Android layout XML, Kotlin/Java UI and Compose.
An extension is a search hint, not proof a file renders UI. Follow component and
style definitions where needed. Exclude generated/vendor files and report any
unreadable or omitted scope. Count files actually read, not just search matches.

Default to WCAG 2.1 AA unless the project specifies another target. The supplied
Nordea checklist is a project-specific snapshot, not a universal legal standard.
Use it only where applicable and cite the actual rule for organization-specific
findings. Do not label any pattern a Finnish-law or EAA violation from this scan.

## Check barriers in context

| Area | Inspect | Candidate criteria, subject to applicability |
| --- | --- | --- |
| Images and media | Meaningful images need equivalent text; decorative images can be ignored. Check SVG accessible names, media alternatives and captions appropriate to the media. | 1.1.1; 1.2.1 audio-only/video-only; 1.2.2 prerecorded synchronized captions |
| Controls | Accessible name, semantic role and actual keyboard operation. Native controls may already provide role and keyboard behaviour. | 2.1.1, 4.1.2 |
| Forms | Visible instructions, programmatic label association, identification of input purpose, errors and recovery. Trace labels and descriptions through components. | 1.3.1, 1.3.5, 3.3.1, 3.3.2 |
| Structure | Meaningful headings, lists, tables, reading order, page title, page language and a way to bypass repeated content. | 1.3.1, 1.3.2, 2.4.1, 2.4.2, 3.1.1 |
| Visual presentation | Focus indication, use of colour, contrast, resizing and reflow. Resolve applicable styles before alleging a missing focus treatment. | 1.4.1, 1.4.3, 1.4.4, 1.4.10, 2.4.7 |
| Dynamic behaviour | Status communication, dialog behaviour, focus restoration, time limits and pause controls for applicable moving content. | 4.1.3, 2.4.3, 2.2.1, 2.2.2 |
| Native mobile | Platform-provided semantics, labels, scaling, orientation, traversal and alternatives to gestures. Inspect actual native behaviour rather than requiring web ARIA attributes. | State the applicable platform/project requirement and verify any WCAG mapping |

A missing attribute is a candidate, not a verdict. Check native semantics,
aria-labelledby, wrapping labels, shared components, visually hidden text,
platform defaults and alternative techniques before reporting a failure.
Do not demand onKeyDown on native buttons, extra semantics on every Compose
clickable, aria-disabled on every native disabled control, aria-live on every
update, or aria-busy on every loading state. Explain the missing user capability.
A heading-level gap, multiple h1 elements, or absence of a main element alone
is not enough to establish a WCAG failure; inspect structure and alternatives.

## Avoid incorrect thresholds

- A 44 CSS pixel target is WCAG 2.1 **AAA** criterion 2.5.5, with exceptions;
  it is not a blanket 2.1 AA requirement. Mobile platform recommendations and
  other WCAG versions must be labelled separately.
- Resize Text 1.4.4 concerns resizing text to 200% without loss, with exceptions;
  it does not mandate a minimum 16px base font or ban px units.
- Text Spacing 1.4.12 tests whether user-adjusted spacing causes loss of content
  or function; it does not require default line-height to be 1.5.
- Focus Not Obscured (Minimum) 2.4.11 is a **WCAG 2.2** AA criterion. Do not list
  it as part of 2.1 or describe its minimum as requiring the whole target visible.
- Visual Presentation 1.4.8 is AAA; recommendations such as line length and
  avoiding justified text must not be relabelled as AA failures.

Official references checked when adapting the supplied checklist:
[Target Size](https://www.w3.org/WAI/WCAG21/Understanding/target-size.html),
[Resize Text](https://www.w3.org/WAI/WCAG21/Understanding/resize-text.html),
[Text Spacing](https://www.w3.org/WAI/WCAG21/Understanding/text-spacing.html),
[Focus Not Obscured](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html).
Consult the relevant official criterion when the mapping is uncertain. If the
source is unavailable, report uncertainty instead of inventing a conformance finding.

## Findings and limits

Rank by demonstrated impact: Critical blocks a task; Major creates a significant
barrier; Minor leaves the task usable with friction; Suggestion is advisory.
Severity is not implied by the category heading or an unverified legal claim.
Do not assign release approval or a sprint deadline on the user's behalf.

Return a report in the conversation:

1. Scope, fixed revisions if supplied, actual files read and omitted coverage.
2. Standard version/level and any applicable project rules.
3. Findings grouped by severity: file and line, observed code, concrete barrier,
   criterion or project rule, evidence, and a suggested fix. Include snippets
   only when they make the finding clearer; do not apply them.
4. Needs runtime or manual check: unobserved focus/announcement behaviour,
   rendered contrast, zoom/reflow and assistive-technology interaction. Describe
   the task to test and expected outcome. Static suspicion is not confirmed failure.
5. Counts per severity and practical next checks. An empty result means no
   evidenced findings in the inspected scope, not complete accessibility.

When used as a code-review axis, follow the caller's concise report format and
word limit while preserving evidence and omitted coverage. Do not run a whole
repository audit in a diff review. Tests/builds or browser interactions require
a separately authorized task; reading source does not require running them.

Where useful, suggest a screen reader check and an appropriate runtime audit
such as axe. Do not install tools. This is static analysis and is not certification,
legal advice, or a substitute for testing with disabled users.
