"""Check what skill source text states about the .nathan-skills save protocol."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills" / "development"
GRILL_ME = SKILLS / "nathan-grill-me"
CODEBASE_SCAN = SKILLS / "codebase-scan"
ACCESSIBILITY_REVIEW = SKILLS / "accessibility-review"
TO_SPEC = SKILLS / "to-spec"
SHARED = GRILL_ME / "references" / "save-folder-protocol.md"

# The protocol's section for a skill opening a file it did not write.
READER_HEADING = "Reading a file another skill saved"

# Each saving skill's own rules: skill folder, subfolder, filename key and the
# pattern for its replace-or-resume rule.
SAVING_SKILLS = [
    (GRILL_ME, "prd", "topic", r"resume by topic"),
    (
        CODEBASE_SCAN,
        "code-scan",
        "scope",
        r"rescan on the same day with the same scope replaces that day's file",
    ),
    (
        ACCESSIBILITY_REVIEW,
        "accessibility-audit",
        "topic",
        r"re-review on the same day of the same topic replaces that day's file",
    ),
]

# One pattern per shared item in the protocol. A file states the protocol only
# when it matches every one.
SHARED_ITEMS = {
    "project root": r"git top-level",
    "filename shape": r"<key>-<YYYY-MM-DD>\.md",
    "gitignore written only if absent": r"does not exist, create it containing `\*`",
    "gitignore never overwritten": r"never overwrite an existing `\.gitignore`",
    "symlink stop": r"stop if `\.nathan-skills` is a symlink",
    "no filename question": r"do not ask the user for the filename",
    "path said once": r"full path once",
    "write failure said plainly": r"say so plainly",
    "working-document disclaimer": r"not backed up",
}
# Items only the protocol should word this way; used to catch restatement elsewhere.
DISTINCTIVE_ITEMS = [
    "no filename question",
    "path said once",
    "working-document disclaimer",
    "symlink stop",
]
# Steps a skill must not restate once the protocol lives in the shared file.
RESTATED_STEPS = [r"\.gitignore", r"symlink"]


def read(path):
    return path.read_text(encoding="utf-8")


def normalise(text):
    return re.sub(r"\s+", " ", text).lower()


def states_protocol(path):
    text = normalise(read(path))
    return all(re.search(pattern.lower(), text) for pattern in SHARED_ITEMS.values())


def section(text, heading):
    """Return the body of the `## heading` section, or "" when it is absent."""
    match = re.search(
        rf"^##\s+{re.escape(heading)}\s*$(.*?)(?=^##\s|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    return match.group(1) if match else ""


def paragraph_mentioning(text, needle):
    """Return the blank-line-separated paragraph containing `needle`, or ""."""
    for block in re.split(r"\n\s*\n", text):
        if needle in block:
            return normalise(block)
    return ""


class SaveProtocolTest(unittest.TestCase):
    def test_working_document_protocol_is_stated_in_exactly_one_file(self):
        stating = sorted(
            path.relative_to(SKILLS).as_posix()
            for path in SKILLS.rglob("*.md")
            if states_protocol(path)
        )
        self.assertEqual(["nathan-grill-me/references/save-folder-protocol.md"], stating)

    def test_no_other_skill_file_restates_a_distinctive_protocol_step(self):
        for path in SKILLS.rglob("*.md"):
            if path == SHARED:
                continue
            text = normalise(read(path))
            for name in DISTINCTIVE_ITEMS:
                with self.subTest(file=path.relative_to(SKILLS).as_posix(), item=name):
                    self.assertNotRegex(text, SHARED_ITEMS[name].lower())

    def test_shared_protocol_constrains_the_filename_key(self):
        text = normalise(read(SHARED))
        self.assertRegex(text, r"lowercase letters, digits and hyphens")

    def test_dependent_skills_say_what_to_do_when_the_protocol_is_missing(self):
        for skill, _subfolder, _key, _rule in SAVING_SKILLS:
            with self.subTest(skill=skill.name):
                text = normalise(read(skill / "SKILL.md"))
                self.assertRegex(text, r"cannot be found, say so and present")
                self.assertIn("do not save from memory", text)

    def test_shared_protocol_covers_every_shared_item(self):
        text = normalise(read(SHARED))
        missing = [
            name
            for name, pattern in SHARED_ITEMS.items()
            if not re.search(pattern.lower(), text)
        ]
        self.assertEqual([], missing)

    def test_nathan_grill_me_does_not_restate_the_gitignore_and_symlink_steps(self):
        text = read(GRILL_ME / "SKILL.md")
        # The pointer may name the topics; restating a step means describing
        # how to perform it.
        for step in RESTATED_STEPS:
            hits = [
                line
                for line in text.splitlines()
                if re.search(step, line, re.IGNORECASE)
                and not line.lstrip().startswith("- Read the save-folder protocol")
            ]
            self.assertEqual([], hits, f"restates {step}")

    def test_shared_protocol_defines_project_root_outside_a_repository(self):
        text = normalise(read(SHARED))
        self.assertRegex(text, r"outside a git repository .{0,40}working directory")

    def test_nathan_grill_me_keeps_resume_by_topic_and_fixed_creation_date(self):
        text = normalise(read(GRILL_ME / "SKILL.md"))
        self.assertIn("resume by topic", text)
        self.assertRegex(text, r"creation date and never changes")
        self.assertIn("subfolder is `prd`", text)

    def test_codebase_scan_does_not_restate_the_gitignore_and_symlink_steps(self):
        text = read(CODEBASE_SCAN / "SKILL.md")
        for step in RESTATED_STEPS:
            hits = [
                line
                for line in text.splitlines()
                if re.search(step, line, re.IGNORECASE)
            ]
            self.assertEqual([], hits, f"restates {step}")

    def test_codebase_scan_replaces_a_same_day_file_for_the_same_scope(self):
        text = normalise(read(CODEBASE_SCAN / "SKILL.md"))
        self.assertIn("subfolder is `code-scan`", text)
        self.assertIn("`<key>` is `<scope>`", text)
        self.assertRegex(
            text, r"rescan on the same day with the same scope replaces that day's file"
        )
        self.assertRegex(text, r"the user may decline the file")

    def test_accessibility_review_does_not_restate_the_gitignore_and_symlink_steps(self):
        text = read(ACCESSIBILITY_REVIEW / "SKILL.md")
        for step in RESTATED_STEPS:
            hits = [
                line
                for line in text.splitlines()
                if re.search(step, line, re.IGNORECASE)
            ]
            self.assertEqual([], hits, f"restates {step}")

    def test_accessibility_review_keeps_identity_header_and_scope_line(self):
        text = normalise(read(ACCESSIBILITY_REVIEW / "SKILL.md"))
        self.assertIn("subfolder is `accessibility-audit`", text)
        self.assertIn("`<key>` is `<topic>`", text)
        self.assertRegex(
            text, r"re-review on the same day of the same topic replaces that day's file"
        )
        self.assertRegex(text, r"the user may decline the file")
        self.assertIn("one-line identity header", text)
        self.assertIn("the scope line", text)
        self.assertIn("read the save-folder protocol", text)

    def test_each_saving_skill_names_its_subfolder_filename_key_and_replace_or_resume_rule(self):
        for skill, subfolder, key, rule in SAVING_SKILLS:
            with self.subTest(skill=skill.name):
                text = normalise(read(skill / "SKILL.md"))
                self.assertIn(f"subfolder is `{subfolder}`", text)
                self.assertIn(f"`<key>` is `<{key}>`", text)
                self.assertRegex(text, rule)

    def test_saving_skills_reference_the_protocol_without_a_cross_skill_relative_path(self):
        for skill, _subfolder, _key, _rule in SAVING_SKILLS:
            with self.subTest(skill=skill.name):
                text = read(skill / "SKILL.md")
                self.assertIn("save-folder-protocol.md", text)
                self.assertIn("skill catalogue", normalise(text))
                # Other cross-skill links (codebase-scan's reviewer discipline)
                # are outside the protocol; only paths reaching it are barred.
                self.assertNotRegex(
                    text, r"\.\.?/[^\s)`]*(nathan-grill-me|save-folder-protocol)"
                )

    def test_shared_protocol_tells_a_reader_where_a_saved_file_is_and_how_it_is_named(self):
        reader = normalise(section(read(SHARED), READER_HEADING))
        self.assertNotEqual("", reader, f"no `## {READER_HEADING}` section")
        # Addressed to a skill opening a file some other skill wrote.
        self.assertRegex(reader, r"did not write")
        self.assertRegex(reader, SHARED_ITEMS["project root"].lower())
        self.assertRegex(reader, SHARED_ITEMS["filename shape"].lower())
        self.assertRegex(reader, r"git-ignored")
        self.assertRegex(reader, r"belongs? to (one|a single) checkout")

    def test_shared_protocol_opening_covers_a_reader_as_well_as_a_saving_skill(self):
        opening = paragraph_mentioning(read(SHARED), "owns this file")
        self.assertRegex(opening, r"read")

    def test_to_spec_does_not_restate_the_filename_shape_or_the_project_root(self):
        text = normalise(read(TO_SPEC / "SKILL.md"))
        # Key-agnostic: to-spec used to write `<topic>-`, not `<key>-`, so a
        # pattern tied to `<key>-` would pass without asserting anything.
        self.assertNotRegex(text, r"<[^>]+>-<yyyy-mm-dd>\.md")
        self.assertNotRegex(text, SHARED_ITEMS["project root"].lower())

    def test_to_spec_references_the_protocol_without_a_cross_skill_relative_path(self):
        text = read(TO_SPEC / "SKILL.md")
        self.assertIn("save-folder-protocol.md", text)
        self.assertIn("skill catalogue", normalise(text))
        self.assertNotRegex(
            text, r"\.\.?/[^\s)`]*(nathan-grill-me|save-folder-protocol)"
        )

    def test_to_spec_keeps_its_subfolder_latest_date_rule_and_ambiguity_rule(self):
        text = normalise(read(TO_SPEC / "SKILL.md"))
        self.assertIn("subfolder is `prd`", text)
        self.assertRegex(text, r"latest trailing date")
        self.assertRegex(text, r"several topics could be meant, ask")
        self.assertRegex(text, r"say which file you took")
        self.assertRegex(text, r"missing or empty, ask for the file's path")

    def test_to_spec_reads_the_protocol_only_when_it_locates_the_prd_itself(self):
        pointer = paragraph_mentioning(read(TO_SPEC / "SKILL.md"), "save-folder-protocol.md")
        self.assertNotEqual("", pointer, "no paragraph points at the protocol")
        # The read hangs off the locate-it-yourself branch, not the skill's start.
        self.assertRegex(pointer, r"only .{0,80}locate the prd yourself")

    def test_to_spec_proceeds_and_says_so_when_the_protocol_is_missing(self):
        text = normalise(read(TO_SPEC / "SKILL.md"))
        self.assertRegex(text, r"cannot be found, do not stop")
        self.assertRegex(text, r"say that the protocol was unavailable")
        self.assertRegex(text, r"name the file you took")
        # Reading has no irreversible write to guard.
        self.assertNotIn("do not save from memory", text)


if __name__ == "__main__":
    unittest.main()
