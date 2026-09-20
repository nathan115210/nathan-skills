"""Exercise shared instruction link ownership using isolated homes."""
from pathlib import Path
import tempfile
import unittest

from scripts.instructions import apply, targets


class InstructionLinksTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.home = self.root / "home"
        self.source = self.root / "clone/instructions/communication.md"
        self.source.parent.mkdir(parents=True)
        self.source.write_text("Shared rules\n")

    def test_preview_install_repeat_edit_and_remove(self):
        self.assertEqual(0, apply(self.home, self.source, dry_run=True))
        self.assertFalse(self.home.exists())
        for _ in range(2):
            self.assertEqual(0, apply(self.home, self.source))
        self.source.write_text("Updated rules\n")
        for target in targets(self.home):
            self.assertEqual("Updated rules\n", target.read_text())
        apply(self.home, self.source, remove=True, dry_run=True)
        self.assertTrue(all(p.is_symlink() for p in targets(self.home)))
        for _ in range(2):
            self.assertEqual(0, apply(self.home, self.source, remove=True))
        self.assertTrue(self.source.exists())
        self.assertFalse(any(p.is_symlink() for p in targets(self.home)))

    def test_preserves_real_file_foreign_and_dangling_links(self):
        paths = targets(self.home)
        for p in paths:
            p.parent.mkdir(parents=True)
        paths[0].write_text("Personal instructions")
        foreign = self.root / "foreign.md"
        foreign.write_text("Foreign instructions")
        paths[1].symlink_to(foreign)
        paths[2].symlink_to(self.root / "missing.md")
        self.assertEqual(1, apply(self.home, self.source))
        self.assertEqual(0, apply(self.home, self.source, remove=True))
        self.assertEqual("Personal instructions", paths[0].read_text())
        self.assertEqual(foreign, paths[1].readlink())
        self.assertTrue(paths[2].is_symlink())

    def test_override_blocks_codex_install(self):
        override = targets(self.home)[0].with_name("AGENTS.override.md")
        override.parent.mkdir(parents=True)
        override.write_text("Override")
        self.assertEqual(1, apply(self.home, self.source))
        self.assertFalse(targets(self.home)[0].exists())
        self.assertEqual("Override", override.read_text())

    def test_remove_exact_dangling_link_but_preserve_other_clone(self):
        apply(self.home, self.source)
        self.source.unlink()
        self.assertEqual(0, apply(self.home, self.source, remove=True))
        target = targets(self.home)[0]
        other = self.root / "other-clone/instructions/communication.md"
        target.symlink_to(other)
        apply(self.home, self.source, remove=True)
        self.assertEqual(other, target.readlink())


if __name__ == "__main__":
    unittest.main()
