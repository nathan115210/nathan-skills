"""Run relink against isolated repositories and tool homes."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOTS = ('.claude/skills', '.codex/skills', '.gemini/config/skills')


class RelinkTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name).resolve()
        self.repo = self.base / 'repository with spaces'
        self.home = self.base / 'home'
        (self.repo / 'scripts').mkdir(parents=True)
        shutil.copy2(Path(__file__).with_name('relink.sh'), self.repo / 'scripts/relink.sh')
        self.skill = self.add_skill('development/example')

    def add_skill(self, relative):
        path = self.repo / 'skills' / relative
        path.mkdir(parents=True)
        (path / 'SKILL.md').write_text('---\nname: ' + path.name + '\n---\n')
        return path

    def run_relink(self):
        return subprocess.run(['bash', str(self.repo / 'scripts/relink.sh')],
                              env={**os.environ, 'HOME': str(self.home)},
                              capture_output=True, text=True)

    def test_flat_same_source_all_providers_and_idempotence(self):
        (self.skill / 'references/nested').mkdir(parents=True)
        (self.skill / 'references/nested/SKILL.md').write_text('not a separate skill')
        for _ in range(2):
            result = self.run_relink()
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for folder in ROOTS:
                root = self.home / folder
                self.assertEqual([p.name for p in root.iterdir()], ['example'])
                self.assertEqual((root / 'example').resolve(), self.skill)

    def test_migrates_owned_old_root_links(self):
        for folder in ROOTS:
            root = self.home / folder
            root.mkdir(parents=True)
            (root / 'example').symlink_to(self.repo / 'example')
        result = self.run_relink()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for folder in ROOTS:
            self.assertEqual((self.home / folder / 'example').resolve(), self.skill)

    def test_preserves_foreign_targets(self):
        foreign = self.base / 'foreign'
        foreign.mkdir()
        for folder in ROOTS:
            (self.home / folder).mkdir(parents=True)
        targets = [self.home / folder / 'example' for folder in ROOTS]
        targets[0].mkdir()
        targets[1].symlink_to(foreign)
        targets[2].symlink_to(self.base / 'foreign-missing')
        self.assertNotEqual(self.run_relink().returncode, 0)
        self.assertFalse(targets[0].is_symlink())
        self.assertEqual(targets[1].resolve(), foreign)
        self.assertEqual(os.readlink(targets[2]), str(self.base / 'foreign-missing'))

    def test_duplicate_names_fail_before_any_links(self):
        self.add_skill('other/example')
        result = self.run_relink()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('duplicate skill name', result.stderr)
        self.assertFalse(self.home.exists())

    def test_new_category_discovered_without_category_link(self):
        another = self.add_skill('learning/deep/teach')
        self.assertEqual(self.run_relink().returncode, 0)
        for folder in ROOTS:
            self.assertEqual((self.home / folder / 'teach').resolve(), another)
            self.assertFalse((self.home / folder / 'learning').exists())

    def test_list_is_same_catalog_without_mutating_home(self):
        nested = self.skill / 'examples/embedded'
        nested.mkdir(parents=True)
        (nested / 'SKILL.md').write_text('example only')
        result = subprocess.run(['bash', str(self.repo / 'scripts/relink.sh'), '--list'],
                                env={**os.environ, 'HOME': str(self.home)}, capture_output=True, check=True)
        self.assertEqual(result.stdout.split(b'\0')[:-1], [os.fsencode(self.skill)])
        self.assertFalse(self.home.exists())


if __name__ == '__main__':
    unittest.main()
