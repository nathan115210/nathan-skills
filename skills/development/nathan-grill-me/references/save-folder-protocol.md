# Save-folder protocol

How a skill saves a working document under `.nathan-skills/`. `nathan-grill-me`
owns this file; other saving skills locate it through the runtime's skill
catalogue and add only their own subfolder, filename key and replace-or-resume
rule. If this file is unavailable, say so and present the draft instead of
saving from memory.

## Location

- Write to `<project root>/.nathan-skills/<subfolder>/<key>-<YYYY-MM-DD>.md`. The
  calling skill supplies `<subfolder>` and `<key>`; the date is in local time.
- The project root is the git top-level of the working directory. Outside a git
  repository it is the working directory itself.

## First write

- Create `.nathan-skills/<subfolder>/` as needed. If `.nathan-skills/.gitignore`
  does not exist, create it containing `*` and nothing else, so the folder ignores
  itself and no tracked file changes.
- Never overwrite an existing `.gitignore`, whatever it contains.
- Stop if `.nathan-skills` is a symlink. Write nothing through it and say why.

## Naming and reporting

- Do not ask the user for the filename. Say the full path once, when you first
  write the file.
- If permissions or the active mode prevent writing, say so plainly and present
  the draft. Do not claim the file was saved.

## Working-document disclaimer

Say this when handing the file over: it is git-ignored, it belongs to this
checkout only (another worktree or a fresh clone does not have it), it is not
backed up, and it does not travel to another machine.
