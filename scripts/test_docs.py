"""Keep generated runtime evidence out of the human-facing docs tree."""

from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
FORBIDDEN_DIRECTORIES = {
    "verification",
    "evidence",
    "fixtures",
    "logs",
    "test-results",
}
FORBIDDEN_SUFFIXES = {".jsonl", ".log"}
FORBIDDEN_ARTIFACT_ENDINGS = {
    ".command.json",
    ".stdout.txt",
    ".stderr.txt",
}


def raw_evidence_paths(docs=DOCS, root=ROOT):
    """Return repository-relative docs paths that look like run artifacts."""
    violations = []
    if not docs.exists():
        return violations

    for path in docs.rglob("*"):
        relative = path.relative_to(root)
        parts = {part.lower() for part in relative.parts[:-1]}
        if parts & FORBIDDEN_DIRECTORIES:
            violations.append(relative)
            continue
        if path.is_file() and (
            path.suffix.lower() in FORBIDDEN_SUFFIXES
            or any(path.name.lower().endswith(ending) for ending in FORBIDDEN_ARTIFACT_ENDINGS)
        ):
            violations.append(relative)
    return sorted(set(violations))


class DocsPolicyTest(unittest.TestCase):
    def test_docs_contain_no_raw_runtime_evidence(self):
        violations = raw_evidence_paths()
        self.assertEqual(
            [],
            violations,
            "Move runtime evidence outside the repository: "
            + ", ".join(map(str, violations)),
        )

    def test_detector_rejects_evidence_directories_and_raw_logs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            evidence = docs / "development" / "verification"
            evidence.mkdir(parents=True)
            (evidence / "run.json").write_text("{}")
            (docs / "trace.jsonl").write_text("{}\n")

            self.assertEqual(
                [
                    Path("docs/development/verification/run.json"),
                    Path("docs/trace.jsonl"),
                ],
                raw_evidence_paths(docs, root),
            )


if __name__ == "__main__":
    unittest.main()
