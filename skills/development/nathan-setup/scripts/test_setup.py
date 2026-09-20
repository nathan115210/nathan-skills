"""Isolated regression tests for preserving project instructions."""
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('setup_helper', Path(__file__).with_name('setup.py'))
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class SetupTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def write(self, content):
        path = self.root / 'AGENTS.md'
        return helper.write_block(self.root, 'AGENTS.md',
                                  helper.file_info(path)['sha256'], content)

    def test_preserves_rules_and_idempotent_refresh(self):
        path = self.root / 'AGENTS.md'
        path.write_bytes(b'# Human rules\r\nUse existing CI.\r\n')
        self.write('Project commands')
        first = path.read_bytes()
        self.assertTrue(first.startswith(b'# Human rules\r\nUse existing CI.\r\n'))
        self.assertEqual(self.write('Project commands')['status'], 'unchanged')
        self.assertEqual(first, path.read_bytes())
        self.write('Updated commands')
        self.assertEqual(path.read_text().count(helper.BEGIN), 1)
        self.assertIn('Use existing CI.', path.read_text())

    def test_stale_plan_preserves_human_edit(self):
        self.write('Old')
        path = self.root / 'AGENTS.md'
        old = helper.file_info(path)['sha256']
        path.write_text('New human rules')
        with self.assertRaises(ValueError):
            helper.write_block(self.root, 'AGENTS.md', old, 'Replace')
        self.assertEqual(path.read_text(), 'New human rules')

    def test_symlink_target_never_written(self):
        target = self.root / 'external.md'
        target.write_text('Preserve me')
        (self.root / 'AGENTS.md').symlink_to(target)
        with self.assertRaises(ValueError):
            helper.write_block(self.root, 'AGENTS.md', 'missing', 'Replace')
        self.assertEqual(target.read_text(), 'Preserve me')

    def test_malformed_blocks_preserved(self):
        path = self.root / 'AGENTS.md'
        original = helper.END + '\n' + helper.BEGIN
        path.write_text(original)
        with self.assertRaises(ValueError):
            self.write('Replace')
        self.assertEqual(path.read_text(), original)

    def test_each_tool_independent_and_existing_claude_preserved(self):
        self.write('Rules')
        claude = self.root / 'CLAUDE.md'
        claude.write_text('Human Claude rules')
        inventory = {n: {'executable': '/fake/' + n, 'status': 'detected'} for n in helper.TOOLS}
        with patch.object(helper, 'discover', return_value=inventory):
            result = helper.connect(self.root)
            self.assertEqual(result['claude']['status'], 'blocked')
            self.assertEqual(result['codex']['status'], 'structurally_connected')
            self.assertEqual(result['agy']['status'], 'structurally_connected')
            self.assertEqual(claude.read_text(), 'Human Claude rules')
            helper.write_block(self.root, 'CLAUDE.md', helper.file_info(claude)['sha256'], '@AGENTS.md')
            self.assertEqual(helper.connect(self.root)['claude']['status'], 'structurally_connected')
            self.assertFalse(result['codex']['runtime_verified'])

    def test_missing_tool_does_not_create_claude_entry(self):
        self.write('Rules')
        inventory = {n: {'executable': None, 'status': 'not_detected'} for n in helper.TOOLS}
        with patch.object(helper, 'discover', return_value=inventory):
            self.assertEqual(helper.connect(self.root)['claude']['status'], 'not_detected')
        self.assertFalse((self.root / 'CLAUDE.md').exists())

    def test_new_claude_relative_link_and_dangling_link_preserved(self):
        self.write('Rules')
        inventory = {n: {'executable': '/fake/' + n, 'status': 'detected'} for n in helper.TOOLS}
        with patch.object(helper, 'discover', return_value=inventory):
            helper.connect(self.root)
            path = self.root / 'CLAUDE.md'
            self.assertEqual(os.readlink(path), 'AGENTS.md')
            path.unlink()
            path.symlink_to('missing-external.md')
            self.assertEqual(helper.connect(self.root)['claude']['status'], 'blocked')
            self.assertEqual(os.readlink(path), 'missing-external.md')

    def test_config_residue_is_not_absence(self):
        (self.root / '.gemini/config').mkdir(parents=True)
        with patch.object(helper.shutil, 'which', return_value=None):
            self.assertEqual(helper.discover(self.root)['agy']['status'], 'not_detected')

    def test_inspect_parent_nested_hashes_and_pruning(self):
        (self.root / '.git').mkdir()
        (self.root / 'AGENTS.md').write_text('Parent rule')
        project = self.root / 'app'
        (project / '.claude').mkdir(parents=True)
        (project / '.claude/CLAUDE.md').write_text('Local rule')
        (project / 'CLAUDE.local.md').write_text('Private rule')
        (project / 'pkg').mkdir()
        (project / 'pkg/AGENTS.md').write_text('Package rule')
        (project / 'node_modules/lib').mkdir(parents=True)
        (project / 'node_modules/lib/AGENTS.md').write_text('Ignore')
        scan = helper.instruction_scan(project)
        self.assertEqual(scan['boundary'], str(self.root))
        files = scan['files']
        self.assertEqual(files[str(self.root / 'AGENTS.md')]['scope'], 'ancestor')
        self.assertIn('sha256', files[str(project / '.claude/CLAUDE.md')])
        self.assertIn('sha256', files[str(project / 'CLAUDE.local.md')])
        self.assertIn(str(project / 'pkg/AGENTS.md'), files)
        self.assertFalse(any('node_modules' in name for name in files))
        self.assertTrue(helper.instruction_scan(project, limit=1)['truncated'])

    def test_shadowing_is_scope_review_not_connected(self):
        self.write('Rules')
        (self.root / 'AGENTS.override.md').write_text('Override')
        inventory = {n: {'executable': '/fake/' + n, 'status': 'detected'} for n in helper.TOOLS}
        with patch.object(helper, 'discover', return_value=inventory):
            results = helper.connect(self.root)
        self.assertEqual(results['codex']['status'], 'needs_scope_review')
        self.assertEqual(results['agy']['status'], 'needs_scope_review')

    def test_import_tokens_and_false_positives(self):
        for text in ('@AGENTS.md  ', '- @AGENTS.md', '@./AGENTS.md', 'Read @AGENTS.md now'):
            self.assertTrue(helper.has_import(text), text)
        for text in ('@AGENTS.md-backup', '@AGENTS.md/other', '`@AGENTS.md`',
                     '<!-- @AGENTS.md -->', '```text\n@AGENTS.md\n```'):
            self.assertFalse(helper.has_import(text), text)

    def test_discover_scans_once_for_three_providers(self):
        with patch.object(helper, 'skill_roots', return_value=[]) as scan:
            helper.discover(self.root)
            scan.assert_called_once()

    def test_dry_run_never_creates_state_or_instructions(self):
        result = helper.write_block(self.root, 'AGENTS.md', 'missing', 'Rules', dry_run=True)
        self.assertIn('+Rules', result['diff'])
        self.assertFalse((self.root / 'AGENTS.md').exists())
        self.assertFalse((self.root / '.nathan-setup').exists())
        inventory = {n: {'executable': '/fake/' + n, 'status': 'detected'} for n in helper.TOOLS}
        (self.root / 'AGENTS.md').write_text('Rules')
        with patch.object(helper, 'discover', return_value=inventory):
            helper.connect(self.root, dry_run=True)
        self.assertFalse((self.root / 'CLAUDE.md').exists())
        self.assertFalse((self.root / '.nathan-setup').exists())

    def test_human_block_edit_requires_review_even_with_fresh_hash(self):
        self.write('Original')
        path = self.root / 'AGENTS.md'
        path.write_text(path.read_text().replace('Original', 'Human rule'))
        expected = helper.file_info(path)['sha256']
        preview = helper.write_block(self.root, 'AGENTS.md', expected, 'Merged human rule', dry_run=True)
        self.assertTrue(preview['blocked'])
        with self.assertRaises(ValueError):
            helper.write_block(self.root, 'AGENTS.md', expected, 'Overwrite')
        helper.write_block(self.root, 'AGENTS.md', expected, 'Merged human rule', accept_edited=True)
        self.assertIn('Merged human rule', path.read_text())

    def test_remove_owned_block_preserves_surrounding_edits(self):
        path = self.root / 'AGENTS.md'
        path.write_text('Human prefix')
        self.write('Managed rule')
        path.write_text(path.read_text() + '\nHuman suffix')
        helper.write_block(self.root, 'AGENTS.md', helper.file_info(path)['sha256'], '', remove=True)
        self.assertIn('Human prefix', path.read_text())
        self.assertIn('Human suffix', path.read_text())
        self.assertNotIn('Managed rule', path.read_text())

    def test_remove_modified_block_refused(self):
        self.write('Managed')
        path = self.root / 'AGENTS.md'
        path.write_text(path.read_text().replace('Managed', 'Human'))
        with self.assertRaises(ValueError):
            helper.write_block(self.root, 'AGENTS.md', helper.file_info(path)['sha256'], '', remove=True)

    def test_setup_refresh_never_creates_or_changes_legacy_report(self):
        report = self.root / 'nathan-setup-report.md'
        for existing in (False, True):
            with self.subTest(existing=existing):
                if existing:
                    report.write_bytes(b'Historical report\r\n')
                with patch.object(helper, 'discover', return_value={
                        n: {'executable': None, 'status': 'not_detected'} for n in helper.TOOLS}):
                    inventory = helper.inspect(self.root)
                    self.assertNotIn(report.name, inventory['instructions'])
                    self.write('Project commands')
                    helper.connect(self.root, confirmed=['claude'])
                    self.write('Refreshed commands')
                    helper.status(self.root)
                self.assertTrue(helper.state_path(self.root).is_file())
                if existing:
                    self.assertEqual(report.read_bytes(), b'Historical report\r\n')
                else:
                    self.assertFalse(report.exists())

    def test_removed_report_command_fails_without_writing(self):
        import subprocess
        import sys
        result = subprocess.run(
            [sys.executable, helper.__file__, 'report', '--project', str(self.root)],
            capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('invalid choice', result.stderr)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_permissions_and_concurrent_editor_preserved(self):
        path = self.root / 'CLAUDE.md'
        path.write_text('Rules')
        path.chmod(0o640)
        helper.write_block(self.root, 'CLAUDE.md', helper.file_info(path)['sha256'], '@AGENTS.md')
        self.assertEqual(path.stat().st_mode & 0o777, 0o640)
        original = helper.tempfile.mkstemp
        def editor_race(*args, **kwargs):
            result = original(*args, **kwargs)
            path.write_text('Concurrent human edit')
            return result
        with patch.object(helper.tempfile, 'mkstemp', side_effect=editor_race):
            with self.assertRaises(ValueError):
                helper.atomic(path, b'Overwrite', helper.file_info(path)['sha256'])
        self.assertEqual(path.read_text(), 'Concurrent human edit')

    def test_only_owned_link_can_be_removed(self):
        self.write('Rules')
        (self.root / 'CLAUDE.md').symlink_to('AGENTS.md')
        with self.assertRaises(ValueError):
            helper.remove_link(self.root)
        (self.root / 'CLAUDE.md').unlink()
        inventory = {n: {'executable': '/fake/' + n, 'status': 'detected'} for n in helper.TOOLS}
        with patch.object(helper, 'discover', return_value=inventory):
            helper.connect(self.root)
        helper.remove_link(self.root, dry_run=True)
        self.assertTrue((self.root / 'CLAUDE.md').is_symlink())
        helper.remove_link(self.root)
        self.assertFalse((self.root / 'CLAUDE.md').is_symlink())

    def test_pending_pass_stale_and_retry(self):
        import json
        import sys
        self.write('Setup verification phrase: secret-rule')
        inventory = {n: {'executable': sys.executable, 'status': 'detected'} for n in helper.TOOLS}
        inventory['claude']['skills'] = {'nathan-setup': {'matches_source': True}}
        proof = {'instruction_phrase': 'secret-rule', 'instruction_sources': ['AGENTS.md'],
                 'skill_available': True, 'skill_path': str(Path(helper.__file__).resolve().parents[1]),
                 'skill_description': helper.skill_description(), 'steps': ['inspect', 'draft', 'connect', 'verify'],
                 'conflicts': []}
        answer = json.dumps({'result': json.dumps(proof)})
        command = [sys.executable, '-c', 'print(' + repr(answer) + ')']
        with patch.object(helper, 'discover', return_value=inventory), patch.object(helper, 'runtime_command', return_value=command):
            self.assertEqual(helper.status(self.root)['tools']['claude']['status'], 'pending')
            run = helper.verify(self.root, 'claude', 'secret-rule', timeout=10)
            self.assertEqual(run['status'], 'passed', run)
            self.assertEqual(helper.status(self.root)['overall'], 'partially_ready')
            self.assertEqual(helper.verify(self.root, 'claude', 'secret-rule', retry=True)['status'], 'already_passed')
            self.write('Changed project rule')
            self.assertEqual(helper.status(self.root)['tools']['claude']['status'], 'stale')

    def test_probe_failure_and_missing_executable_are_distinct(self):
        import sys
        inventory = {n: {'executable': sys.executable, 'status': 'detected'} for n in helper.TOOLS}
        with patch.object(helper, 'discover', return_value=inventory):
            with patch.object(helper, 'runtime_command', return_value=[sys.executable, '-c', 'print("{}")']):
                self.assertEqual(helper.verify(self.root, 'claude', 'secret')['status'], 'failed')
            with patch.object(helper, 'runtime_command', return_value=['/missing/nathan-cli']):
                self.assertEqual(helper.verify(self.root, 'claude', 'secret')['status'], 'pending')

    def test_unstructured_keyword_claim_cannot_pass(self):
        import sys
        import json
        inventory = {n: {'executable': sys.executable, 'status': 'detected',
                        'skills': {'nathan-setup': {'matches_source': True}}} for n in helper.TOOLS}
        text = json.dumps({'result': 'secret nathan-setup ' + helper.skill_description() + ' BUT skill not installed'})
        command = [sys.executable, '-c', 'print(' + repr(text) + ')']
        with patch.object(helper, 'discover', return_value=inventory), patch.object(helper, 'runtime_command', return_value=command):
            self.assertEqual(helper.verify(self.root, 'claude', 'secret')['status'], 'failed')

    def test_state_is_gitignored(self):
        import subprocess
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        self.write('Rules')
        result = subprocess.run(['git', '-C', str(self.root), 'status', '--porcelain', '--untracked-files=all'],
                                capture_output=True, text=True, check=True)
        self.assertNotIn('.nathan-setup', result.stdout)

    def test_probe_timeout_remains_pending(self):
        import sys
        inventory = {n: {'executable': sys.executable, 'status': 'detected'} for n in helper.TOOLS}
        with patch.object(helper, 'discover', return_value=inventory), patch.object(helper, 'runtime_command',
                return_value=[sys.executable, '-c', 'import time; time.sleep(5)']):
            self.assertEqual(helper.verify(self.root, 'codex', 'secret', timeout=0.05)['status'], 'pending')

    def test_agy_transport_failure_with_zero_exit_is_pending(self):
        import sys
        import json
        inventory = {n: {'executable': sys.executable, 'status': 'detected'} for n in helper.TOOLS}
        response = json.dumps({'status': 'ERROR', 'response': ''})
        command = [sys.executable, '-c', 'print(' + repr(response) + ')']
        with patch.object(helper, 'discover', return_value=inventory), patch.object(helper, 'runtime_command', return_value=command):
            result = helper.verify(self.root, 'agy', 'secret')
            self.assertEqual(result['status'], 'pending')
            self.assertIn('ERROR', result['reason'])

    def test_write_remove_cycles_do_not_accumulate_blank_lines(self):
        import hashlib
        original = '# Project\n\n- Keep this rule.\n'
        path = self.root / 'AGENTS.md'
        path.write_text(original)
        def current():
            return hashlib.sha256(path.read_bytes()).hexdigest()
        for _ in range(4):
            helper.write_block(self.root, 'AGENTS.md', current(), '## Managed\n- generated')
            helper.write_block(self.root, 'AGENTS.md', current(), '', remove=True)
            self.assertEqual(path.read_text(), original)

    def test_remove_keeps_text_on_both_sides_of_the_block(self):
        import hashlib
        path = self.root / 'AGENTS.md'
        path.write_text('# Top\n')
        def current():
            return hashlib.sha256(path.read_bytes()).hexdigest()
        helper.write_block(self.root, 'AGENTS.md', current(), '## Managed\n- generated')
        path.write_text(path.read_text().rstrip('\n') + '\n\n## Human tail\n- kept\n')
        helper.write_block(self.root, 'AGENTS.md', current(), '', remove=True)
        self.assertEqual(path.read_text(), '# Top\n\n## Human tail\n- kept\n')

    def test_evidence_after_fence_or_prose_still_parses(self):
        proof = {'instruction_phrase': 'secret'}
        import json
        fenced = '```json\n' + json.dumps(proof) + '\n```\n\nNotes: read AGENTS.md {not json}.'
        self.assertEqual(helper.extract_proof(fenced), proof)
        self.assertEqual(helper.extract_proof('Here it is:\n' + json.dumps(proof) + '\nDone.'), proof)
        self.assertEqual(helper.extract_proof('no json at all'), {})
        self.assertEqual(helper.extract_proof(None), {})

    def test_trailing_prose_does_not_fail_a_real_pass(self):
        import sys
        import json
        inventory = {n: {'executable': sys.executable, 'status': 'detected',
                        'skills': {'nathan-setup': {'matches_source': True}}} for n in helper.TOOLS}
        proof = {'instruction_phrase': 'secret', 'instruction_sources': ['AGENTS.md'],
                 'skill_available': True, 'skill_path': str(Path(helper.__file__).resolve().parents[1]),
                 'skill_description': helper.skill_description(), 'steps': ['a', 'b', 'c', 'd'],
                 'conflicts': []}
        answer = '```json\n' + json.dumps(proof) + '\n```\n\nNotes on how this was established: ...'
        command = [sys.executable, '-c', 'print(' + repr(json.dumps({'result': answer})) + ')']
        with patch.object(helper, 'discover', return_value=inventory), patch.object(helper, 'runtime_command', return_value=command):
            self.assertEqual(helper.verify(self.root, 'claude', 'secret')['status'], 'passed')

    def test_agy_auto_denied_tool_permission_is_pending_not_failed(self):
        import sys
        import json
        inventory = {n: {'executable': sys.executable, 'status': 'detected'} for n in helper.TOOLS}
        response = json.dumps({'status': 'SUCCESS', 'response': '',
                               'denied_actions': [{'action': 'command', 'display_name': 'RunCommand'}]})
        command = [sys.executable, '-c', 'print(' + repr(response) + ')']
        with patch.object(helper, 'discover', return_value=inventory), patch.object(helper, 'runtime_command', return_value=command):
            result = helper.verify(self.root, 'agy', 'secret')
            self.assertEqual(result['status'], 'pending')
            self.assertIn('RunCommand', result['reason'])

    def test_agy_denied_actions_alongside_real_answer_still_judged(self):
        import sys
        import json
        inventory = {n: {'executable': sys.executable, 'status': 'detected',
                        'skills': {'nathan-setup': {'matches_source': True}}} for n in helper.TOOLS}
        proof = {'instruction_phrase': 'secret', 'instruction_sources': ['AGENTS.md'],
                 'skill_available': True, 'skill_path': str(Path(helper.__file__).resolve().parents[1]),
                 'skill_description': helper.skill_description(), 'steps': ['inspect', 'draft', 'connect', 'verify'],
                 'conflicts': []}
        response = json.dumps({'status': 'SUCCESS', 'response': json.dumps(proof),
                               'denied_actions': [{'action': 'command', 'display_name': 'RunCommand'}]})
        command = [sys.executable, '-c', 'print(' + repr(response) + ')']
        with patch.object(helper, 'discover', return_value=inventory), patch.object(helper, 'runtime_command', return_value=command):
            self.assertEqual(helper.verify(self.root, 'agy', 'secret')['status'], 'passed')

    def test_agy_success_envelope_is_parsed(self):
        import sys
        import json
        inventory = {n: {'executable': sys.executable, 'status': 'detected',
                        'skills': {'nathan-setup': {'matches_source': True}}} for n in helper.TOOLS}
        proof = {'instruction_phrase': 'secret', 'instruction_sources': ['AGENTS.md'],
                 'skill_available': True, 'skill_path': str(Path(helper.__file__).resolve().parents[1]),
                 'skill_description': helper.skill_description(), 'steps': ['inspect', 'draft', 'connect', 'verify'],
                 'conflicts': []}
        response = json.dumps({'status': 'SUCCESS', 'response': json.dumps(proof)})
        command = [sys.executable, '-c', 'print(' + repr(response) + ')']
        with patch.object(helper, 'discover', return_value=inventory), patch.object(helper, 'runtime_command', return_value=command):
            self.assertEqual(helper.verify(self.root, 'agy', 'secret')['status'], 'passed')


if __name__ == '__main__':
    unittest.main()
