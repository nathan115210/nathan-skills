"""Check that skills reach each other through the skill catalogue, not by path."""

import os
from pathlib import Path
import re
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
CODEBASE_SCAN = SKILLS_ROOT / "development" / "codebase-scan"
INSTRUCTIONS = ROOT / "CLAUDE.md"

# A token that climbs at least one directory, as a Markdown link target or in prose.
CLIMBING_PATH = re.compile(r"[^\s()\[\]<>`'\"]*\.\./[^\s()\[\]<>`'\"]*")


def read(path):
    return path.read_text(encoding="utf-8")


def normalise(text):
    return re.sub(r"\s+", " ", text).lower()


def paragraph_mentioning(text, needle):
    """Return the first blank-line-separated paragraph containing needle."""
    for paragraph in re.split(r"\n\s*\n", text):
        if needle in paragraph:
            return normalise(paragraph)
    return ""


def section(text, heading):
    """Return the body of the `## heading` section, or "" when it is absent."""
    match = re.search(
        rf"^##\s+{re.escape(heading)}\s*$(.*?)(?=^##\s|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    return match.group(1) if match else ""


def skill_folder(path, skills_root):
    """Return the nearest folder at or above path that holds a SKILL.md."""
    for folder in [path, *path.parents]:
        if folder == skills_root:
            break
        if (folder / "SKILL.md").is_file():
            return folder
    return None


def cross_skill_paths(path, text, skills_root=SKILLS_ROOT):
    """Return the relative paths in text that leave path's skill for another.

    A path into another skill's folder is a violation. So is a missing path
    outside every skill: categories hold only skill folders, so it names a
    skill that was renamed or removed. An existing category or the skills root
    itself is not a skill, and a path that leaves skills_root is no reference.
    """
    own = skill_folder(path.parent, skills_root)
    if own is None:
        return []
    violations = []
    for token in CLIMBING_PATH.findall(text):
        target = Path(os.path.normpath(path.parent / token.split("#")[0]))
        if not target.is_relative_to(skills_root) or target.is_relative_to(own):
            continue
        if skill_folder(target, skills_root) is not None or not target.exists():
            violations.append(token)
    return violations


class CrossSkillReferenceTest(unittest.TestCase):
    def test_codebase_scan_locates_reviewer_discipline_through_the_skill_catalogue(self):
        text = read(CODEBASE_SCAN / "SKILL.md")
        pointer = paragraph_mentioning(text, "reviewer.md")
        self.assertNotEqual("", pointer, "no paragraph mentions reviewer.md")
        self.assertIn("code-review", pointer)
        self.assertIn("skill catalogue", pointer)
        self.assertFalse(
            "../code-review/" in text, "codebase-scan names a ../code-review/ path"
        )

    def test_no_skill_file_links_into_another_skill_by_relative_path(self):
        for path in sorted(SKILLS_ROOT.rglob("*.md")):
            relative = path.relative_to(ROOT).as_posix()
            with self.subTest(file=relative):
                violations = cross_skill_paths(path, read(path))
                self.assertEqual(
                    [],
                    violations,
                    f"{relative} reaches into another skill by relative path: "
                    + ", ".join(violations)
                    + "; locate it through the skill catalogue instead",
                )

    def test_relative_path_detector_flags_a_sibling_skill_path(self):
        with tempfile.TemporaryDirectory() as temporary:
            skills = Path(temporary) / "skills"
            scan = skills / "development" / "codebase-scan"
            review = skills / "development" / "code-review"
            for skill in (scan, review):
                (skill / "references").mkdir(parents=True)
                (skill / "SKILL.md").write_text("", encoding="utf-8")

            text = "[reviewer discipline](../code-review/references/reviewer.md)"
            self.assertEqual(
                ["../code-review/references/reviewer.md"],
                cross_skill_paths(scan / "SKILL.md", text, skills),
            )
            # The same climb from a references file, and into a removed skill.
            deeper = "../../../development/code-review/references/reviewer.md"
            self.assertEqual(
                [deeper],
                cross_skill_paths(scan / "references" / "x.md", deeper, skills),
            )
            gone = "see ../retired-skill/SKILL.md"
            self.assertEqual(
                ["../retired-skill/SKILL.md"],
                cross_skill_paths(scan / "SKILL.md", gone, skills),
            )

    def test_relative_path_detector_allows_a_skill_own_references_path(self):
        with tempfile.TemporaryDirectory() as temporary:
            skills = Path(temporary) / "skills"
            scan = skills / "development" / "codebase-scan"
            (scan / "references").mkdir(parents=True)
            (scan / "SKILL.md").write_text("", encoding="utf-8")

            own = "[coverage](references/coverage.md) and ./references/coverage.md"
            self.assertEqual([], cross_skill_paths(scan / "SKILL.md", own, skills))
            back = "[the skill](../SKILL.md) and ../references/coverage.md#rules"
            self.assertEqual(
                [], cross_skill_paths(scan / "references" / "x.md", back, skills)
            )

    def test_relative_path_detector_allows_parent_category_navigation(self):
        with tempfile.TemporaryDirectory() as temporary:
            skills = Path(temporary) / "skills"
            scan = skills / "development" / "codebase-scan"
            (scan / "references").mkdir(parents=True)
            (scan / "SKILL.md").write_text("", encoding="utf-8")
            (skills / "development" / "README.md").write_text("", encoding="utf-8")

            up = "[category](../), [all skills](../../) and ../README.md"
            self.assertEqual([], cross_skill_paths(scan / "SKILL.md", up, skills))
            deeper = "../../../development/"
            self.assertEqual(
                [], cross_skill_paths(scan / "references" / "x.md", deeper, skills)
            )

    def test_rename_procedure_tells_you_to_search_other_skills_for_the_old_name(self):
        rename = section(read(INSTRUCTIONS), "Renaming a skill")
        self.assertNotEqual("", rename, "no `## Renaming a skill` section")
        steps = [normalise(step) for step in re.split(r"\n(?=\d+\.\s)", rename)]
        searching = [step for step in steps if re.search(r"grep -rn .*skills/", step)]
        self.assertEqual(1, len(searching), "expected one step that greps skills/")
        step = searching[0]
        self.assertRegex(step, r"other skill|another skill")
        self.assertIn("skill.md", step)
        self.assertIn("references/", step)
        self.assertRegex(step, r"update")

    def test_removal_procedure_points_to_the_cross_skill_reference_step(self):
        removal = normalise(section(read(INSTRUCTIONS), "Removing a skill"))
        self.assertNotEqual("", removal, "no `## Removing a skill` section")
        self.assertRegex(removal, r"other skill|another skill")
        self.assertRegex(removal, r"update or remove")
        self.assertIn("renaming a skill", removal)
        self.assertIn("grep -rn", removal)


if __name__ == "__main__":
    unittest.main()
