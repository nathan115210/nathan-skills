<!-- skills/accessibility-review/references/persona-review.md -->

# Accessibility persona review — design path

> Reference doc of the `accessibility-review` skill. Followed when the review
> scope is **Design only** or the design half of **Both**. Paths below are
> relative to the skill root.

Label this as a simulated review using illustrative personas, not customer research. Reveal the barriers a design creates for disabled customers that the design team has not accounted for. Two voices do this together: a collective persona that speaks for the group, and named individuals who make the abstraction concrete. Teams dismiss guideline violations; they rarely dismiss a named person telling them they can't pay their bill.

## Before reviewing

Read these for the design path, with paths relative to the skill root:

- `references/group-voice.md` — how the collective "we" persona speaks
- `references/personas.md` — the seven individuals, their setups, and how each one sounds
- `references/flag-map.md` — design features mapped to who they break for, plus the banking-specific traps

If no design has been supplied, ask for one: a screenshot, Figma link, exported frame, PDF, flow description, or just the copy and field list. Don't review an imaginary design. If a Figma connection is available, read the actual frame rather than working from a description of it.

## How to look at the design

Walk the journey in order, as a customer would, not as a checklist auditor. At each step ask: what does this step demand of a person, and who cannot supply it? Demands include seeing something, hearing something, reading fluent Danish or Swedish, using a mouse, using a smartphone, answering a phone, remembering what was on the previous screen, working fast, or already knowing bank vocabulary.

Ground every finding in something actually present. Quote the label, name the button, cite the step. "Step 3 asks for the payment reference but the field has no visible label" is useful; "labels may be missing" is noise.

Separate three states honestly, because credibility depends on it:

- **Broken** — the evidence is in front of you
- **Can't tell from this** — plausible failure the artefact doesn't show (focus order in a static image, caption quality in a storyboard). Say so and say what you'd need.
- **Fine** — if a design genuinely works for a persona, say that. Manufacturing complaints to fill the template teaches the team to ignore the whole review.

## Choosing which individuals speak

All seven are considered internally. Surface the **2 to 4** whose problems are most severe and most specific to this design, ordered worst first. Consult `flag-map.md` to pick. A persona earns a slot by having something particular to say about this artefact, not by representing a category worth covering.

Some near-automatic slots: audio or video content → the Deaf and hard-of-hearing voices; anything app-only or SMS-dependent → the two who have no usable smartphone; any form of more than three fields → a screen reader user and a keyboard user; dense text or unexplained banking vocabulary → the dyslexic and autistic voices; anything requiring a phone call → the Deaf and hard-of-hearing voices, and it is almost always a blocker.

## Output format

Use this structure. Keep it tight — a review nobody finishes changes nothing.

```
## What we looked at
[One or two sentences: the artefact and the journey it covers.]

## The group view
[Collective "we" voice, 4–7 sentences. Lead with the barrier that stops the most
people. Name where the group splits, since designs usually break by trying to serve
an average customer who doesn't exist.]

## Where it breaks for some of us

### [Name], [tagline] — [Blocker / Serious friction / Wears us down]
[First person, 2–4 sentences, about THIS design. Concrete elements, concrete
consequence. Their own voice, not a generic accessibility complaint.]
**What would fix it:** [One or two specific changes.]

[Repeat for each surfaced persona.]

## Fix these first
1. [Change, and who it unblocks. Order by people blocked, not by effort.]

## We can't tell from this
- [Open question, and what would answer it.]

## Test this with real customers
[Which user groups to recruit, and the specific tasks to watch them attempt.]
```

## Voice discipline

The collective voice is "we", "some of us", "those of us who…" — never a single individual, never a case study.

The individuals speak as themselves, in "I". They should be distinguishable with the names removed: one is a 24-year-old expert screen reader user who is precise and slightly impatient; another is an 82-year-old who quietly gives up and phones instead. Give them their own vocabulary, their own tolerance for hassle, and their own stakes. Frustration is allowed. So is noticing when something has been done well.

For a banking journey, keep money in frame: so the cost of a bad screen is not a lost purchase but a missed rent payment, a frozen card abroad, a fraud check nobody can complete, or dependence on a relative who can now see everything. Guessing at an unlabelled field is a risk none of us take with a transfer.

## Closing note

End every review by stating that this panel consists of supplied illustrative personas whose research provenance has not been verified, not a replacement for testing with disabled customers — and that the last section names who to recruit. A persona review that gets treated as sign-off has done net harm.
