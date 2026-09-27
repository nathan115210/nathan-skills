"""Keep every workflow action pinned to an immutable, release-commented commit."""

from pathlib import Path
import re
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
DEPENDABOT = ROOT / ".github" / "dependabot.yml"

USES = re.compile(r"^\s*(?:-\s+)?uses:\s*(?P<ref>\S+)(?P<rest>.*)$")
PINNED = re.compile(r"^[^@\s]+/[^@\s]+@[0-9a-f]{40}$")
RELEASE_COMMENT = re.compile(r"^\s+#\s*v\d+\.\d+\.\d+\s*$")

NOT_PINNED = "not pinned to a full commit SHA"
NO_RELEASE = "pinned SHA has no exact release comment"


def workflow_violations(workflows=WORKFLOWS, root=ROOT):
    """Return (file, line, reason) for each action reference that can move."""
    violations = []
    for path in sorted(workflows.glob("*.yml")):
        relative = path.relative_to(root)
        for number, line in enumerate(path.read_text().splitlines(), start=1):
            if line.lstrip().startswith("#"):
                continue
            match = USES.match(line)
            if not match:
                continue
            ref = match["ref"].strip("'\"")
            if ref.startswith("./"):
                continue
            if not PINNED.match(ref):
                violations.append((relative, number, NOT_PINNED))
            elif not RELEASE_COMMENT.match(match["rest"]):
                violations.append((relative, number, NO_RELEASE))
    return violations


def violations_with(reason, violations):
    return [violation for violation in violations if violation[2] == reason]


class WorkflowPinningTest(unittest.TestCase):
    def check_fixture(self, uses_line):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            (workflows / "ci.yml").write_text(
                "jobs:\n"
                "  build:\n"
                "    steps:\n"
                f"      {uses_line}\n"
            )
            return workflow_violations(workflows, root)

    def test_every_workflow_action_is_pinned_to_a_commit_sha(self):
        violations = violations_with(NOT_PINNED, workflow_violations())
        self.assertEqual([], violations, "Pin these actions to a full commit SHA")

    def test_every_pinned_action_names_its_exact_release(self):
        violations = violations_with(NO_RELEASE, workflow_violations())
        self.assertEqual([], violations, "Add a '# vX.Y.Z' comment to these pins")

    def test_flags_a_pinned_action_without_a_release_comment(self):
        violations = self.check_fixture(
            "- uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1"
        )
        self.assertEqual(
            [(Path(".github/workflows/ci.yml"), 4, NO_RELEASE)], violations
        )

    def test_flags_an_action_referenced_by_a_tag(self):
        violations = self.check_fixture("- uses: actions/checkout@v7")
        self.assertEqual(
            [(Path(".github/workflows/ci.yml"), 4, NOT_PINNED)], violations
        )

    def test_flags_an_abbreviated_commit_sha(self):
        violations = self.check_fixture("- uses: actions/checkout@3d3c42e # v7.0.1")
        self.assertEqual(
            [(Path(".github/workflows/ci.yml"), 4, NOT_PINNED)], violations
        )

    def test_allows_a_local_action_path(self):
        self.assertEqual([], self.check_fixture("- uses: ./.github/actions/x"))

    def test_ignores_a_commented_out_uses_line(self):
        self.assertEqual([], self.check_fixture("# uses: foo@v1"))


class DependabotTest(unittest.TestCase):
    def test_dependabot_updates_github_actions_monthly(self):
        self.assertTrue(DEPENDABOT.is_file(), "Add .github/dependabot.yml")
        config = DEPENDABOT.read_text()
        for setting in (
            'package-ecosystem: "github-actions"',
            'directory: "/"',
            'interval: "monthly"',
        ):
            self.assertIn(setting, config)


if __name__ == "__main__":
    unittest.main()
