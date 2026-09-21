"""Exercise uninstall in temporary clones and homes; never touch real installs."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOTS = ('.claude/skills', '.codex/skills', '.gemini/config/skills')


class UnlinkTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name).resolve()
        self.repo = self.base / 'clone with spaces'
        self.home = self.base / 'home'
        (self.repo / 'scripts/lib').mkdir(parents=True)
        for script in ('relink.sh', 'unlink.sh'):
            shutil.copy2(Path(__file__).with_name(script), self.repo / 'scripts' / script)
        shutil.copy2(Path(__file__).parent / 'lib/links.sh', self.repo / 'scripts/lib/links.sh')
        self.skill = self.repo / 'skills/development/example'
        self.skill.mkdir(parents=True)
        (self.skill / 'SKILL.md').write_text('---\nname: example\n---\n')

    def test_missing_lib_fails_with_error(self):
        (self.repo / 'scripts/lib/links.sh').unlink()
        result = self.run_script('unlink.sh')
        self.assertEqual(result.returncode, 1)
        self.assertIn('scripts/lib/links.sh', result.stderr)

    def run_script(self, script='unlink.sh', *args):
        return subprocess.run(['bash', str(self.repo / 'scripts' / script), *args],
                              env={**os.environ, 'HOME': str(self.home)},
                              capture_output=True, text=True)

    def install(self):
        result = self.run_script('relink.sh')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_preview_uninstall_repeat_and_reinstall(self):
        self.install()
        preview = self.run_script('unlink.sh', '--dry-run')
        self.assertEqual(preview.returncode, 0)
        self.assertIn('would remove: 3', preview.stdout)
        for root in ROOTS:
            self.assertTrue((self.home / root / 'example').is_symlink())
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('removed: 3', result.stdout)
        for root in ROOTS:
            self.assertFalse((self.home / root / 'example').is_symlink())
        self.assertTrue((self.skill / 'SKILL.md').is_file())
        self.assertIn('removed: 0', self.run_script().stdout)
        self.install()

    def test_owned_stale_relative_and_foreign_links(self):
        self.install()
        foreign = self.base / 'foreign'
        foreign.mkdir()
        (self.repo / 'escape').symlink_to(foreign)
        for root in ROOTS:
            folder = self.home / root
            (folder / 'stale').symlink_to(self.repo / 'removed-skill')
            (folder / 'relative').symlink_to(os.path.relpath(self.skill, folder))
            (folder / 'cloudflare').mkdir()
            (folder / '.system').mkdir()
            (folder / 'file').write_text('keep')
            for name, dest in {
                'foreign': foreign,
                'foreign-missing': self.base / 'missing',
                'prefix-collision': Path(str(self.repo) + '-other') / 'missing',
                'traversal': str(self.repo) + '/../missing',
                'escape-missing': self.repo / 'escape/missing',
                'escape-existing': self.repo / 'escape',
            }.items():
                (folder / name).symlink_to(dest)
        for legacy in ('.gemini/skills', '.copilot/skills'):
            folder = self.home / legacy
            folder.mkdir(parents=True)
            (folder / 'example').symlink_to(self.skill)
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        for root in ROOTS:
            folder = self.home / root
            self.assertEqual(set(p.name for p in folder.iterdir()), {
                'cloudflare', '.system', 'file', 'foreign', 'foreign-missing',
                'prefix-collision', 'traversal', 'escape-missing', 'escape-existing'})
        for legacy in ('.gemini/skills', '.copilot/skills'):
            self.assertTrue((self.home / legacy / 'example').is_symlink())

    def test_missing_home_and_invalid_arguments_do_not_mutate(self):
        self.assertEqual(self.run_script().returncode, 0)
        self.assertFalse(self.home.exists())
        self.install()
        for args in (('--invalid',), ('--dry-run', 'extra')):
            self.assertNotEqual(self.run_script('unlink.sh', *args).returncode, 0)
        for root in ROOTS:
            self.assertTrue((self.home / root / 'example').is_symlink())

    def test_moved_clone_preserves_old_links(self):
        self.install()
        moved = self.base / 'moved clone'
        self.repo.rename(moved)
        self.repo = moved
        result = self.run_script()
        self.assertEqual(result.returncode, 0)
        self.assertIn('kept: 3', result.stdout)
        for root in ROOTS:
            self.assertTrue((self.home / root / 'example').is_symlink())


if __name__ == '__main__':
    unittest.main()
