# Coverage obligations, per axis

Coverage is defined **per axis**, not once for the whole run. Each axis below
says what it must inspect, how it finds its own targets, and what it must
declare it did not cover. Read only the section for the axis you are running.

Two rules apply to all three:

- **Count what you read, not what you matched.** A grep hit is a lead. A file
  you opened is coverage. The not-covered list is built from the difference.
- **A declared gap is a result.** "Not covered: the payment service, no source
  in this repository" is a finding the reader can act on. Silence about it is
  not.

---

## Security — exhaustive by risk surface

Not hotspot-first, and not sampled. The surface is fixed in advance and every
part of it is inspected **regardless of when that code last changed**. Old,
rarely-touched authentication and boundary code is where risk settles; a scan
that prioritised by churn would systematically miss it. If a surface is absent
from this codebase, say it is absent — that is different from not looking.

### The four surfaces

| Surface | Inspect |
| --- | --- |
| **Authentication and authorization** | Where identity is established, where a session or token is issued, validated, refreshed and revoked. Every authorization check, and every route, handler, job or command that has none. Role and tenant boundaries. Who can act on whose data. |
| **Input boundaries** | Every place untrusted data enters: HTTP handlers and their parameters, request bodies, headers, cookies, file uploads, queue and webhook consumers, CLI arguments, environment, deserialization, and anything reaching a query, a shell, a filesystem path, a template or an outbound request. Check validation at the boundary, not only downstream. |
| **Secrets** | Committed credentials, keys and tokens in source, tests, fixtures, configuration, CI definitions and container files. How secrets reach runtime, whether any is logged or returned in an error, and whether `.gitignore` and example files actually keep them out. Also check history if the tooling allows it read-only, and say whether you did. |
| **Dependencies** | The manifests and lockfiles actually present. Direct dependencies with known-risk profiles, unpinned or floating versions, abandoned packages, install-time scripts, and anything fetched at build from an unverified source. |

### Method

Enumerate each surface from the code before judging any of it — routes from the
router, entry points from the manifest and the framework's conventions, secrets
by pattern across the whole tree, dependencies from the manifests. Enumeration
first, inspection second: a surface you never enumerated cannot appear in either
the findings or the not-covered list, and that is how a gap becomes invisible.

Do not run scanners, install tooling or call external vulnerability services.
Checking a version against remembered advisories is a **judgement call** and must
be labelled one; say that no advisory database was queried in this run.

### Declare as not covered

Any surface not enumerated, and why. Any enumerated entry point not read. Any
code whose behaviour could not be resolved statically — dynamic dispatch,
generated handlers, configuration-driven routing, infrastructure defined
elsewhere. Anything needing a runtime, a deployed environment or a live
credential to judge. Whether git history was searched for secrets.

---

## Architecture — hotspot-first, over a named window

Prioritised by commit history, because the code that changes most is where
structural cost is actually paid. **The report names the window.** An unnamed
window makes the prioritisation unreviewable.

### Find the hotspots

```
git log --since='<window>' --name-only --pretty=format: \
  | grep -v '^$' | sort | uniq -c | sort -rn | head -40
```

Pick a window that spans a real amount of activity — twelve months is a sane
default; a young repository uses its whole history and says so. Exclude the
vendored and generated paths already declared. Then read the top files
**together with what they depend on and what depends on them**: a hotspot is a
symptom, and the cause is usually a boundary near it.

Also read, regardless of churn: the entry points, the module or package layout,
the dependency direction between layers, and any ADRs, architecture notes or
project rules the repository carries. Those are the stated intent this axis
judges the code against, when they exist.

### What to look for

Coupling that crosses a stated boundary; a module every change has to touch;
duplicated concepts that drift; layering that inverts; state shared where it
should be passed; abstraction that does not pay for itself; a missing seam that
forces every test to be an integration test; dead scaffolding still carried.
Name the **consequence** — what this costs at the next change — not the label.

Judge against the project's own stated intent first, then neighbouring
convention. Your taste is not a rule; anything not backed by a stated rule or a
demonstrated cost is a judgement call and is labelled one.

### Declare as not covered

The window used, and therefore what fell outside it: files below the churn
threshold, and anything not touched inside the window at all. The depth reached
— which hotspots were read with their neighbourhood and which were only
counted. Any subsystem not read. Whether ADRs or architecture notes existed; if
none did, say the axis judged against convention alone.

---

## Accessibility — every file that renders or styles UI

Enumerated, not sampled. The output includes the list of files found.

Read `accessibility-review`'s `references/code-audit.md` for UI discovery and
`references/accessibility-checklist.md` for the criteria, located through the
runtime's skill catalogue, the sibling skill in this source tree, or the
project's configured skill locations. Keep no duplicated standards here. This
reads shared reference material; it does **not** invoke `accessibility-review`,
and it never runs that skill's persona branch.

One difference of scope from `code-review`, and it is deliberate: that skill
passes only the requested diff. **This passes the whole repository**, which is
what `code-audit.md` is written for. Existing barriers are in scope regardless
of when they arrived.

If those references are unavailable, report the axis as **not assessed** and say
which file was missing. Do not invent a WCAG checklist.

If the repository renders no UI at all, that is a legitimate outcome: say the
axis found no UI-rendering files, list what you searched for, and report it as
not applicable rather than as passed.

### Declare as not covered

Files matched by extension but not read, and why. Styles resolved elsewhere — a
design system, a theme package, a CDN stylesheet. Anything requiring a runtime:
real contrast values, focus order, announcement order, whether a journey is
completable. Those are structural limits of static analysis, not oversights, and
naming them is what keeps a static scan from reading as an audit of the
experience.
