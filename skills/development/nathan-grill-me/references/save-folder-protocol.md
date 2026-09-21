# Save-folder protocol

How a skill saves a working document under `.nathan-skills/`, and how a skill
that reads one it did not write finds it. `nathan-grill-me` owns this file;
every other skill locates it through the runtime's skill catalogue. A saving
skill adds only its own subfolder, filename key and replace-or-resume rule; if
this file is unavailable to it, say so and present the draft instead of saving
from memory. A reading skill adds its own folder and disambiguation rules, and
says for itself what it does when this file is unavailable.

## Location

- Write to `<project root>/.nathan-skills/<subfolder>/<key>-<YYYY-MM-DD>.md`. The
  calling skill supplies `<subfolder>` and `<key>`; the date is in local time.
- `<key>` uses only lowercase letters, digits and hyphens, and does not start with a
  hyphen. If the name the skill would use contains anything else (a slash, `..`, a
  space), normalise it to that form before writing.
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

## Reading a file another skill saved

For a skill opening a file it did not write:

- Look under `<project root>/.nathan-skills/<subfolder>/`, where the project root
  is the git top-level of the working directory. The reading skill supplies the
  `<subfolder>` it expects.
- Files there are named `<key>-<YYYY-MM-DD>.md`, with the date in local time. The
  `<key>` is whatever the writing skill chose, lowercase letters, digits and
  hyphens; match on the shape, not on a key you assume.
- The files are git-ignored and belong to one checkout, so a different worktree
  or a fresh clone does not have them. A missing or empty folder is an ordinary
  outcome, not a fault to investigate.
