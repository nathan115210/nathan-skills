"""Check what skill source text states about the .nathan-skills save protocol."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills" / "development"
GRILL_ME = SKILLS / "nathan-grill-me"
CODEBASE_SCAN = SKILLS / "codebase-scan"
ACCESSIBILITY_REVIEW = SKILLS / "accessibility-review"
SHARED = GRILL_ME / "references" / "save-folder-protocol.md"

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
# Steps a skill must not restate once the protocol lives in the shared file.
RESTATED_STEPS = [r"\.gitignore", r"symlink"]


def read(path):
    return path.read_text(encoding="utf-8")


def normalise(text):
    return re.sub(r"\s+", " ", text).lower()


def states_protocol(path):
    text = normalise(read(path))
    return all(re.search(pattern.lower(), text) for pattern in SHARED_ITEMS.values())


class SaveProtocolTest(unittest.TestCase):
    def test_working_document_protocol_is_stated_in_exactly_one_file(self):
        stating = sorted(
            path.relative_to(GRILL_ME).as_posix()
            for path in GRILL_ME.rglob("*.md")
            if states_protocol(path)
        )
        self.assertEqual(["references/save-folder-protocol.md"], stating)

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

    def test_accessibility_review_reference_uses_no_cross_skill_relative_path(self):
        text = read(ACCESSIBILITY_REVIEW / "SKILL.md")
        self.assertNotRegex(text, r"\.\./[\w-]+/references")


if __name__ == "__main__":
    unittest.main()
