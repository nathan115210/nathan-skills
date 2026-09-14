---
name: nathan-setup
description: Set up or refresh Nathan skills in a new or existing project. Discover project rules and validation commands, preserve existing instructions, and connect installed Claude Code, Codex, and agy tools.
disable-model-invocation: true
---

# Nathan Setup

On the user's explicit request, prepare the selected project for Nathan skills. Use the same project rules and workflow across Claude Code, Codex and agy. Configure all installed tools; one unavailable tool does not block verified tools.

The helper is `scripts/setup.py` inside this skill; resolve its physical absolute path. It requires Python 3 on macOS/Linux. Examples below abbreviate that path as `HELPER`; substitute it and the actual project path. Read [references.md](references.md) when running provider probes or interpreting scope differences.

## 1. Inspect the project and existing setup

Run `python3 HELPER inspect --project PROJECT` and `status --project PROJECT`. Confirm the intended project root from the user's context and Git; support non-Git projects. `inspect` inventories parent instructions up to the nearest Git root, home, or filesystem root, and nested instructions with a bounded scan. Read the reported files, relevant README, manifests and CI. Scan limits and unreadable paths are unresolved scope, not proof of absence. Check global/profile instructions separately when relevant.

Use the project's existing architecture, commands and working agreements as evidence. Keep project scope: no package installation, global setting changes, application-code edits, commits or external publication implicit in setup. Missing personal skill links belong to `scripts/relink.sh` in the source repository; preserve third-party installations. agy is Antigravity CLI, not Gemini CLI. An app or binary outside PATH needs independent installation evidence, not guesses based on a generic Gemini directory.

## 2. Draft missing guidance and preview changes

Keep root AGENTS.md concise; reference existing documents instead of copying them. Preserve rules and meaningful human edits, discussing only unresolved material conflicts. Do not reconfirm agreed decisions.

A block might contain the following **only when confirmed by this project**:

```markdown
## Project workflow
- Purpose: an internal order-management service.
- Architecture and boundaries: see README.md and docs/architecture.md.
- Business logic lives in src/orders; HTTP routes call that layer.
- Use the lockfile's package manager.
- Validation: run pnpm lint and pnpm test from the repository root.
- Integration tests require the local test database described in README.md.
- Treat existing test failures as baseline evidence; record their causes.
- Use grill-me to clarify behavior and write a root topic PRD.
- Development gates are not yet installed; dependent workflows remain unavailable.
```

Draft only missing, verified content in a temporary UTF-8 file. Use the current hash from inspect (`missing` for a new file):

```text
python3 HELPER write --project PROJECT --file AGENTS.md --expected HASH --content DRAFT --dry-run
python3 HELPER write --project PROJECT --file AGENTS.md --expected HASH --content DRAFT
```

Dry-run produces a diff without creating files or state. The helper preserves text outside the managed block and checks both the full-file hash and the previous managed-block baseline. Human edits or an unowned legacy block require reading and merging the diff first. After that review, `--accept-edited-block` allows the reviewed replacement; never use it merely to silence a refusal. The helper detects changes, not semantic correctness. Existing symlinked instruction files are preserved and reported for ownership-aware handling.

## 3. Connect every installed provider

Run `connect --project PROJECT --dry-run`, then `connect --project PROJECT`. It creates a relative CLAUDE.md link only when absent; existing files are preserved. For an independent CLAUDE.md, read it and add a reviewed `@AGENTS.md` import with the same write/dry-run mechanism. Codex and agy share AGENTS.md. Overrides, nested instructions, scan errors and extra Claude sources produce `needs_scope_review`; inspect their applicability before claiming a connection is effective. Nested files are specialization, not automatically a conflict.

`connect --tool NAME` includes an installation independently confirmed outside PATH; it does not prove that a runnable CLI or authentication exists. Structural connection and runtime verification remain distinct. Never install a placeholder hook: required development/QA mechanisms that do not exist must be reported as unavailable.

## 4. Verify, report and enable safe retries

Run appropriate **reviewed** project validation commands in their correct directories with the host execution tool. Record command, prerequisites, coverage limits and outcome: passed, code failure, environment blocked, not applicable or not run. Do not run deployments hidden behind a script or fix baseline failures as an implicit setup step.

Use the concrete CLI probes in references.md via `verify --project PROJECT --tool NAME --question QUESTION --expect PHRASE`. Choose a precise question about an existing project rule (for example, “Quote the first bullet under Project workflow exactly”) and its expected answer from the file. The answer is checked locally and is not supplied to the provider. Do not add artificial rules to a real project merely to pass the test. Without `--question`, the default asks for a labelled `Setup verification phrase`, useful in isolated fixtures. Verify also requests the exact skill description, installed entry path, four steps and conflicts as structured evidence. Review the evidence, not just the status label.

`status` summarizes recorded discovery probes. `verify ... --retry` skips unchanged passed probes and retries pending, failed or stale ones. Missing CLI/authentication/timeouts are pending with reasons; a completed response that fails to establish discovery is failed. Pending is a normal unverified state, never a pass. This verifies instruction/skill discovery, not identical model reasoning, hook enforcement or every workflow. Version/profile changes require fresh evidence. Read-only modes have provider-specific limits documented in references.md.

Append a concise dated report with `report --project PROJECT --expected HASH --content NOTE [--dry-run]`. Use the report hash from inspect. This operation preserves all previous report bytes and adds a new entry in root `nathan-setup-report.md`; include existing setup docs by reference. Do not rewrite the report with a bare editor. Exclude credentials, raw provider logs and personal absolute paths. Local `.nathan-setup/` stores baselines and probe metadata, ignores itself in Git and is not portable project policy.

Report readiness **per tool and per workflow**. A failed or pending tool permits partial readiness if another passed. No verified installed tool means not ready. Structural-only checks never establish readiness. Project validation failures and missing required hooks must remain visible even if the discovery probe passed.

For undo, preview `remove --project PROJECT --file AGENTS.md --expected HASH --dry-run` and then apply it. This removes only an unchanged owned block, preserving surrounding human text. For a setup-created CLAUDE.md link use `remove --file CLAUDE.md --link`; unrelated links remain protected. Remove dependent imports/links before removing a shared block. Modified or unowned blocks require manual reconciliation, not forced deletion. Report history is retained. Finish with changed file links, checks run, readiness and actionable gaps; follow the project's staging policy and do not commit.
