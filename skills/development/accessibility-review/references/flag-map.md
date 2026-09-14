<!-- skills/accessibility-review/references/flag-map.md -->

# Flag map — what to look for and who it breaks

Use this to scan a design and to pick which individuals speak. Names in bold are the ones who feel it worst and should get the slot.

## Forms and input

| Feature in the design | Who it breaks for |
|---|---|
| Field with no programmatic label, or a placeholder used as the label | **Ebba** (can't identify it, won't guess on money), Beate |
| Labels beside fields rather than above, or fields side by side | **Beate** (misses the second field entirely when zoomed) |
| Cramped fields, small targets | Beate, **Svante**, Petri |
| Session or form timeout | **Petri**, **Tuija**, Svante, Ebba |
| No save-and-return on a long form | **Tuija**, **Andrzej**, Petri |
| Strict format validation, no spelling tolerance, no address lookup | **Tuija**, Samir, Petri |
| Error messages that appear without being announced | **Ebba** |
| Errors shown only by red text or a coloured border | Ebba, Svante, Beate |
| Vague errors ("invalid entry") | Tuija, **Andrzej**, Samir |
| Mandatory phone number with no contact-preference option | **Samir** |
| Multi-step flow where layout shifts between steps | **Beate**, Andrzej |

## Navigation and interaction

| Feature | Who it breaks for |
|---|---|
| Mouse-only control — hover menu, drag-and-drop, slider, custom date picker | **Petri**, **Ebba**, Svante |
| Keyboard trap, or focus staying behind an open modal | **Petri**, **Ebba** |
| Modal or toast appearing away from where the user is looking | **Beate** (outside the zoom), Ebba |
| Long tab sequence before main content, no skip link | **Petri**, Ebba |
| Missing or out-of-order headings, vague link text | **Ebba**, Andrzej, Tuija |
| Deep menus, many links, dense link clusters | **Andrzej**, Tuija |
| Illogical focus order | Ebba, Petri |

## Visual design

| Feature | Who it breaks for |
|---|---|
| Contrast below 4.5:1, grey-on-white, thin type | **Svante**, **Beate** |
| Small text, no reflow at 200–400% zoom | **Svante** (won't change settings — gives up), Beate |
| Horizontal layouts, wide tables, side-by-side columns | **Beate** |
| Bright, saturated or clashing colour | **Andrzej** |
| Carousels, animated banners, tickers, autoplay | **Andrzej**, **Tuija** |
| Information carried by colour alone | Svante, Beate, Ebba |
| Images with no alt text or no description of the thing itself | **Ebba** |
| PDF-only document | **Beate**, Ebba, Svante |
| Justified text, italics, long unbroken paragraphs | **Tuija**, Svante, Samir |

## Content and language

| Feature | Who it breaks for |
|---|---|
| Unexplained banking or legal vocabulary | **Samir**, **Tuija**, Andrzej, Svante |
| Long text with the key point buried | **Tuija**, **Samir**, Andrzej, Svante |
| Copy assuming prior knowledge of the process | **Andrzej**, Tuija |
| Uncaptioned video, or captions without speaker identification | **Samir** |
| Audio with no transcript | Samir, Svante |
| No sign language version of anything essential | **Samir** |
| Vague next steps, unclear what happens after submitting | **Andrzej** |

## Channels and service — the ones teams forget

| Feature | Who it breaks for |
|---|---|
| Phone as the only contact route, or a phone-verification step | **Samir** (impossible), **Svante** (noise, unclear speech), Andrzej (avoids calls) |
| No phone number offered at all | **Svante**, **Beate** (both prefer to call) |
| No chat or email option | **Andrzej**, **Samir** |
| Smartphone app required, or app-only feature | **Petri** (basic phone), **Svante** (tablet, no app skills) |
| SMS one-time code | **Svante** (refuses to text, doesn't read messages), Samir (fine — this one suits him) |
| Voice-menu phone tree | Svante, Samir |
| Branch or video appointment with no interpreter offered | **Samir** |
| Appointment with no hearing loop, or a loop nobody has tested | **Svante** |
| Intercom or door entry at a branch | **Samir** |
| Identity check requiring reading a code aloud or hearing a code | **Samir**, **Svante** |
| Queue system announcing numbers only by voice, or only on a screen | Samir, Svante, Ebba |

## Banking-specific traps worth checking every time

- **Anything irreversible behind an unlabelled control.** Guessing is survivable in a shop and not in a payment. Several of us abandon rather than risk it — that abandonment reads as disinterest in the funnel data.
- **Time limits on signing and authentication.** A person using speech recognition, a screen reader, or reading with difficulty needs several times longer than the timer assumes.
- **Statements and terms as PDF only.** This is the single most common way a bank makes its own information unreadable.
- **Transaction tables.** Wide, horizontally scrolling, often unlabelled columns, meaningless merchant strings — hard for magnification, screen readers and anyone reading slowly.
- **Fraud and card-block flows.** The highest-stakes, most time-critical journey in the bank, and often the most phone-dependent. Being unable to complete it is a different order of harm from a clumsy onboarding screen. Weight it accordingly.
- **Card readers, ATMs, and physical devices.** Small buttons, flat touchscreens, no tactile markers, no audio.
- **The relative as workaround.** When a design forces someone to hand over their phone or their passwords, it has created a safeguarding and fraud problem, not solved an access one.
- **Assisted digital and delegated access.** If the fallback is "ask us for help", check whether the help route is itself accessible.
