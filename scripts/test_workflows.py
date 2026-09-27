"""Keep workflow actions pinned and GitHub expressions out of shell scripts."""

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
RUN = re.compile(r"^(?P<lead>\s*(?:-\s+)?)run:(?P<value>.*)$")
BLOCK_HEADER = re.compile(r"^\s*[|>][-+0-9]*\s*(?:#.*)?$")

NOT_PINNED = "not pinned to a full commit SHA"
NO_RELEASE = "pinned SHA has no exact release comment"
EXPRESSION_IN_RUN = "expression inside a run block; pass it through env:"


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


def run_expression_violations(workflows=WORKFLOWS, root=ROOT):
    """Return (file, line, reason) for each ${{ }} Actions expands into a script.

    A block scalar's content is every following line indented more than its
    run: key, plus blank lines; a # line inside it is script text, not YAML.
    """
    violations = []
    paths = [*workflows.glob("*.yml"), *workflows.glob("*.yaml")]
    for path in sorted(paths):
        relative = path.relative_to(root)
        block_indent = None
        for number, line in enumerate(path.read_text().splitlines(), start=1):
            if block_indent is not None:
                indent = len(line) - len(line.lstrip())
                if not line.strip() or indent > block_indent:
                    if "${{" in line:
                        violations.append((relative, number, EXPRESSION_IN_RUN))
                    continue
                block_indent = None
            if line.lstrip().startswith("#"):
                continue
            match = RUN.match(line)
            if not match:
                continue
            if BLOCK_HEADER.match(match["value"]):
                block_indent = len(match["lead"])
            elif "${{" in match["value"]:
                violations.append((relative, number, EXPRESSION_IN_RUN))
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


class WorkflowRunExpressionTest(unittest.TestCase):
    def check_fixture(self, *step_lines, name="ci.yml"):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            steps = "".join(f"      {line}\n" for line in step_lines)
            (workflows / name).write_text(
                "jobs:\n"
                "  build:\n"
                "    steps:\n"
                f"{steps}"
            )
            return run_expression_violations(workflows, root)

    def violation_at(self, line):
        return [(Path(".github/workflows/ci.yml"), line, EXPRESSION_IN_RUN)]

    def test_no_workflow_run_block_contains_an_expression(self):
        self.assertEqual(
            [],
            run_expression_violations(),
            "Pass these values to the script through env: instead of ${{ }}",
        )

    def test_flags_an_expression_in_a_single_line_run(self):
        violations = self.check_fixture("- run: echo ${{ github.ref }}")
        self.assertEqual(self.violation_at(4), violations)

    def test_flags_an_expression_in_a_yaml_extension_workflow(self):
        violations = self.check_fixture(
            "- run: echo ${{ github.ref }}", name="ci.yaml"
        )
        self.assertEqual(
            [(Path(".github/workflows/ci.yaml"), 4, EXPRESSION_IN_RUN)], violations
        )

    def test_flags_an_expression_in_a_literal_block_run(self):
        violations = self.check_fixture(
            "- name: Check changesets",
            "  run: |",
            "    python3 scripts/check_changeset.py \\",
            '      --base "origin/${{ github.event.pull_request.base.ref }}"',
        )
        self.assertEqual(self.violation_at(7), violations)

    def test_flags_an_expression_in_a_folded_block_run(self):
        violations = self.check_fixture(
            "- run: >-",
            "    echo ${{ x }}",
        )
        self.assertEqual(self.violation_at(5), violations)

    def test_flags_an_expression_in_a_shell_comment_inside_a_run_block(self):
        violations = self.check_fixture(
            "- run: |",
            "    # ${{ secrets.X }}",
            "    echo done",
        )
        self.assertEqual(self.violation_at(5), violations)

    def test_allows_an_expression_in_step_env(self):
        violations = self.check_fixture(
            "- env:",
            "    FOO: ${{ github.ref }}",
            '  run: echo "$FOO"',
        )
        self.assertEqual([], violations)

    def test_run_block_ends_at_a_less_indented_key(self):
        violations = self.check_fixture(
            "- run: |",
            '    echo "$FOO"',
            "",
            "  env:",
            "    FOO: ${{ github.ref }}",
        )
        self.assertEqual([], violations)

    def test_ignores_an_expression_in_a_commented_out_run_line(self):
        self.assertEqual([], self.check_fixture("# - run: echo ${{ x }}"))


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
