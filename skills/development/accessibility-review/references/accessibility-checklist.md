<!-- skills/accessibility-review/references/accessibility-checklist.md -->

# Accessibility Checklist — supplied Nordea snapshot

The source and capture dates below are supplied metadata, not independently
verified provenance. Use organization-specific items only for an applicable
project. This checklist mixes WCAG requirements and advisory practices; confirm
criterion version, level and exceptions before reporting a violation. The
[code-audit guidance](./code-audit.md) explains common false positives.

> Source: nordea.design, "Accessibility checklist" page (via WP REST API,
> `wp-json/wp/v2/accessibility?slug=accessibility-checklist`). Captured
> 2026-07-21, page last modified 2026-03-04. This is a snapshot — re-verify
> against the live page if this file is old.
>
> References WCAG 2.1. Each item below links to the relevant WCAG success
> criterion or technique for further detail.

## Non-text content and colour
- Images need alt text ([1.1 Text Alternatives](https://www.w3.org/TR/WCAG21/#text-alternatives))
- Charts/infographics need a text description of what they show
- Purely decorative content must be ignorable by assistive tech
- Videos need subtitles; other media needs transcripts ([1.2 Time-based Media](https://www.w3.org/TR/WCAG21/#time-based-media))
- Instructions can't rely on sensory traits alone (e.g. "the round button") ([1.3 Sensory Characteristics](https://www.w3.org/TR/WCAG21/#sensory-characteristics))
- Relationships between elements can't rely on colour or position alone ([1.4.1 Use of Color](https://www.w3.org/WAI/WCAG21/Understanding/use-of-color.html))
- Colour contrast must meet the minimum ratio ([1.4.3 Contrast](https://www.w3.org/TR/WCAG21/#contrast-minimum))
- Anything conveyed by colour must also be conveyed in text

## Structure and relationships
- Group related content together ([1.3.1 Info and Relationships](https://www.w3.org/WAI/WCAG21/Understanding/info-and-relationships))
- Content order must make sense when read linearly ([1.3.2 Meaningful Sequence](https://www.w3.org/WAI/WCAG21/Understanding/meaningful-sequence.html))
- Relationships between elements need to be explicit, not just visual
- Pages/sections need real headings ([2.4.2 Page Titled](https://www.w3.org/WAI/WCAG21/Understanding/page-titled.html), [2.4.6 Headings and Labels](https://www.w3.org/WAI/WCAG21/Understanding/headings-and-labels.html))
- Every form input / interactive element needs a real label ([3.3.2 Labels or Instructions](https://www.w3.org/WAI/WCAG21/Understanding/labels-or-instructions))

## Function and navigation
- Everything must be operable by keyboard alone ([2.1 Keyboard Accessible](https://www.w3.org/TR/WCAG21/#keyboard-accessible))
- Keyboard focus must be visible ([2.4.7 Focus Visible](https://www.w3.org/TR/WCAG21/#focus-visible))
- Focus order must follow the logical order of the content ([2.4.3 Focus Order](https://www.w3.org/WAI/WCAG21/Understanding/focus-order))
- Links and buttons need real text labels, not icon-only with no accessible name ([4.1.2 Name, Role, Value](https://www.w3.org/WAI/WCAG21/Understanding/name-role-value.html))
- Links should follow Nordea Design System styling conventions
- Navigation needs to stay consistent across views ([3.2.3 Consistent Navigation](https://www.w3.org/WAI/WCAG21/Understanding/consistent-navigation.html))
- Users need more than one way to find content ([2.4.5 Multiple Ways](https://www.w3.org/WAI/WCAG21/Understanding/multiple-ways.html))
- Provide a way to skip repeated content blocks ([2.4.1 Bypass Blocks](https://www.w3.org/TR/WCAG21/#bypass-blocks))
- Design must be responsive ([1.3.4 Orientation](https://www.w3.org/WAI/WCAG21/Understanding/orientation.html), [1.4.10 Reflow](https://www.w3.org/WAI/WCAG21/Understanding/reflow.html))
- Text must remain usable when resized to 200% ([1.4.4 Resize Text](https://www.w3.org/WAI/WCAG21/Understanding/resize-text.html))
- Users need control over content that changes on input ([3.2.2 On Input](https://www.w3.org/WAI/WCAG21/Understanding/on-input.html))
- Final form submissions need a confirmation step ([3.3.4 Error Prevention](https://www.w3.org/TR/WCAG21/#error-prevention-legal-financial-data))
- Time limits need a way to be notified, extended, or turned off ([2.2.1 Timing Adjustable](https://www.w3.org/WAI/WCAG21/Understanding/timing-adjustable.html))
- Auto-playing content needs a pause/stop/hide control ([2.2.2 Pause, Stop, Hide](https://www.w3.org/WAI/WCAG21/Understanding/pause-stop-hide.html))

## Content
- Lead with the most important information first
- Use plain, clear language — short words over formal/long ones
- Keep sentences and paragraphs short
- Write in active voice
- Every page/section needs a clear heading
- Follow Nordea's date/time formatting guidelines
- Prefer bulleted/numbered lists where they fit
- Use terminology consistently across the product
- Avoid jargon and metaphors
- Link text should be clear and meaningful on its own ([2.4.4 Link Purpose](https://www.w3.org/WAI/WCAG21/Understanding/link-purpose-in-context.html))
- Validation errors and error states should follow Nordea's content patterns ([3.3.1 Error Identification](https://www.w3.org/WAI/WCAG21/Understanding/error-identification.html), [3.3.2 Labels or Instructions](https://www.w3.org/WAI/WCAG21/Understanding/labels-or-instructions.html))

## Additional resources (internal, may need Nordea network access)
- Accessibility Requirements as part of Definition of Done (Confluence)
- Accessibility Home (Confluence)
- [Common WAI-ARIA practices and patterns](https://www.w3.org/WAI/ARIA/apg/patterns/) (public)
