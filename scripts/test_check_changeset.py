"""Run the changeset guard against isolated repositories."""
import importlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
check_changeset = importlib.import_module('check_changeset')


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


class BumpTests(unittest.TestCase):
    """Reading bump levels out of a changeset's frontmatter."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name)

    def changeset(self, name, body):
        write(self.dir / name, body)
        return self.dir / name

    def test_reads_each_quoting_style(self):
        for frontmatter in ('"nathan-skills": major', "'nathan-skills': major",
                            'nathan-skills: major'):
            with self.subTest(frontmatter=frontmatter):
                path = self.changeset('c.md', f'---\n{frontmatter}\n---\n\nwhy\n')
                self.assertEqual(check_changeset.bumps(path), ['major'])

    def test_ignores_the_folder_readme_and_bodies(self):
        write(self.dir / 'README.md', '---\n"nathan-skills": major\n---\n')
        self.changeset('real.md', '---\n"nathan-skills": patch\n---\n\n'
                                  'mentions major in prose\n')
        files = check_changeset.changeset_files(self.dir)
        self.assertEqual([p.name for p in files], ['real.md'])
        self.assertEqual(check_changeset.check_major(files), [])

    def test_file_without_frontmatter_requests_nothing(self):
        path = self.changeset('c.md', 'just notes\n')
        self.assertEqual(check_changeset.bumps(path), [])


class GuardTests(unittest.TestCase):
    """The two rules, run end to end against a throwaway git repository."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name) / 'repo'
        (self.repo / '.changeset').mkdir(parents=True)
        self.git('init', '-b', 'master')
        self.git('config', 'user.email', 'test@example.com')
        self.git('config', 'user.name', 'test')
        write(self.repo / 'README.md', 'base\n')
        self.commit('base')
        # Guarded changes arrive on a branch; master stays at the base commit
        # so the diff against it is the pull request's own diff.
        self.git('checkout', '-b', 'feature')
        self.patch_repo()

    def patch_repo(self):
        for name, value in (('REPO', self.repo),
                            ('CHANGESET_DIR', self.repo / '.changeset')):
            original = getattr(check_changeset, name)
            setattr(check_changeset, name, value)
            self.addCleanup(setattr, check_changeset, name, original)

    def git(self, *args):
        return subprocess.run(('git',) + args, cwd=self.repo,
                              capture_output=True, text=True, check=True)

    def commit(self, message):
        self.git('add', '-A')
        self.git('commit', '-m', message)

    def run_guard(self, *args):
        return check_changeset.main(['--base', 'master', *args])

    def add_changeset(self, level):
        write(self.repo / '.changeset' / f'{level}-change.md',
              f'---\n"nathan-skills": {level}\n---\n\nwhy\n')

    def change_a_skill(self):
        write(self.repo / 'skills/development/example/SKILL.md',
              '---\nname: example\n---\n')

    def test_major_fails_and_the_waiver_releases_it(self):
        self.add_changeset('major')
        self.change_a_skill()
        self.commit('breaking')
        self.assertEqual(self.run_guard(), 1)
        self.assertEqual(self.run_guard('--allow-major'), 0)

    def test_minor_and_patch_pass(self):
        for level in ('minor', 'patch'):
            with self.subTest(level=level):
                self.add_changeset(level)
        self.change_a_skill()
        self.commit('two changes')
        self.assertEqual(self.run_guard(), 0)

    def test_changed_skill_without_a_changeset_fails(self):
        self.change_a_skill()
        self.commit('undocumented')
        self.assertEqual(self.run_guard(), 1)
        self.assertEqual(self.run_guard('--skip-present'), 0)

    def test_documentation_only_change_needs_nothing(self):
        write(self.repo / 'docs/development/README.md', 'prose\n')
        self.commit('docs')
        self.assertEqual(self.run_guard(), 0)

    def test_unknown_base_does_not_fail_the_build(self):
        self.change_a_skill()
        self.commit('undocumented')
        self.assertEqual(check_changeset.main(['--base', 'origin/nope']), 0)


if __name__ == '__main__':
    unittest.main()
