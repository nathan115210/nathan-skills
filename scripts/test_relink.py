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

    def test_prunes_links_for_a_renamed_skill(self):
        self.assertEqual(self.run_relink().returncode, 0)
        (self.skill).rename(self.repo / 'skills/development/renamed')
        result = self.run_relink()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('prune', result.stdout)
        for folder in ROOTS:
            root = self.home / folder
            self.assertEqual(sorted(p.name for p in root.iterdir()), ['renamed'])
            self.assertTrue((root / 'renamed').resolve().exists())

    def test_prunes_links_for_a_removed_skill(self):
        second = self.add_skill('development/second')
        self.assertEqual(self.run_relink().returncode, 0)
        shutil.rmtree(second)
        result = self.run_relink()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for folder in ROOTS:
            root = self.home / folder
            self.assertEqual(sorted(p.name for p in root.iterdir()), ['example'])

    def test_prune_spares_real_directories_and_foreign_links(self):
        self.assertEqual(self.run_relink().returncode, 0)
        outsider = self.base / 'someone-elses-pack'
        (outsider / 'cloudflare').mkdir(parents=True)
        for folder in ROOTS:
            root = self.home / folder
            (root / 'real-pack').mkdir()
            (root / 'foreign').symlink_to(outsider / 'cloudflare')
        self.skill.rename(self.repo / 'skills/development/renamed')
        result = self.run_relink()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for folder in ROOTS:
            root = self.home / folder
            self.assertEqual(sorted(p.name for p in root.iterdir()),
                             ['foreign', 'real-pack', 'renamed'])
            self.assertTrue((root / 'real-pack').is_dir())
            self.assertEqual((root / 'foreign').resolve(), outsider / 'cloudflare')

    def test_prune_leaves_a_dangling_link_pointing_outside_the_clone(self):
        self.assertEqual(self.run_relink().returncode, 0)
        for folder in ROOTS:
            (self.home / folder / 'elsewhere').symlink_to(self.base / 'gone')
        result = self.run_relink()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for folder in ROOTS:
            root = self.home / folder
            self.assertTrue((root / 'elsewhere').is_symlink())

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



@unittest.skipUnless(shutil.which('git'), 'git is required to build a worktree')
class WorktreeGuardTests(unittest.TestCase):
    """relink derives its root from its own location, so a linked worktree
    would silently repoint every tool at that branch's skills."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name).resolve()
        self.home = self.base / 'home'
        self.main = self.base / 'main'
        skill = self.main / 'skills/development/example'
        skill.mkdir(parents=True)
        (skill / 'SKILL.md').write_text('---\nname: example\n---\n')
        (self.main / 'scripts').mkdir()
        shutil.copy2(Path(__file__).with_name('relink.sh'), self.main / 'scripts/relink.sh')
        self.git('init', '-b', 'main')
        self.git('add', '-A')
        self.git('-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-m', 'init')
        self.worktree = self.base / 'wt'
        self.git('worktree', 'add', '-b', 'side', str(self.worktree))

    def git(self, *args):
        return subprocess.run(['git', '-C', str(self.main), *args],
                              capture_output=True, text=True, check=True)

    def run_relink(self, root, *args):
        return subprocess.run(['bash', str(root / 'scripts/relink.sh'), *args],
                              env={**os.environ, 'HOME': str(self.home)},
                              capture_output=True, text=True)

    def test_main_worktree_links_normally(self):
        result = self.run_relink(self.main)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual((self.home / '.claude/skills/example').resolve(),
                         self.main / 'skills/development/example')

    def test_linked_worktree_is_refused_and_touches_nothing(self):
        result = self.run_relink(self.worktree)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('linked git worktree', result.stderr)
        self.assertIn(str(self.main), result.stderr)
        self.assertIn('--force', result.stderr)
        self.assertFalse(self.home.exists(), 'no tool directory may be created')

    def test_linked_worktree_does_not_replace_existing_main_links(self):
        self.assertEqual(self.run_relink(self.main).returncode, 0)
        self.assertNotEqual(self.run_relink(self.worktree).returncode, 0)
        self.assertEqual((self.home / '.claude/skills/example').resolve(),
                         self.main / 'skills/development/example')

    def test_force_links_from_a_linked_worktree_and_says_so(self):
        result = self.run_relink(self.worktree, '--force')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('WARN', result.stdout)
        self.assertIn('linked git worktree', result.stdout)
        self.assertEqual((self.home / '.claude/skills/example').resolve(),
                         self.worktree / 'skills/development/example')

    def test_list_stays_available_inside_a_linked_worktree(self):
        result = self.run_relink(self.worktree, '--list')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout.split('\0')[:-1],
                         [str(self.worktree / 'skills/development/example')])
        self.assertFalse(self.home.exists())


if __name__ == '__main__':
    unittest.main()
