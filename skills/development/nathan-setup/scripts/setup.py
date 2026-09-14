#!/usr/bin/env python3
"""Inspect, connect, verify and safely refresh Nathan project setup (Python 3)."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import difflib
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import uuid

TOOLS = {'claude': ('.claude', '.claude/skills'),
         'codex': ('.codex', '.codex/skills'),
         'agy': (None, '.gemini/config/skills')}
BEGIN, END = '<!-- nathan-setup:begin -->', '<!-- nathan-setup:end -->'
FILES = ('AGENTS.md', 'CLAUDE.md')
REPORT = 'nathan-setup-report.md'
SKIP = {'.git', 'node_modules', '.venv', 'venv', '__pycache__', 'dist', 'build',
        '.next', '.nathan-setup', 'vendor'}
INSTRUCTIONS = ('AGENTS.md', 'AGENTS.override.md', 'CLAUDE.md', 'CLAUDE.local.md',
                '.claude/CLAUDE.md')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def file_info(path):
    if path.is_symlink():
        result = {'kind': 'symlink', 'target': os.readlink(path), 'exists': path.exists()}
        if path.is_file():
            result['target_sha256'] = digest(path.read_bytes())
        return result
    if not path.exists():
        return {'kind': 'missing', 'sha256': 'missing'}
    if not path.is_file():
        return {'kind': 'unsupported'}
    return {'kind': 'file', 'sha256': digest(path.read_bytes())}


def repository_root():
    for parent in Path(__file__).resolve().parents:
        if (parent / 'scripts/relink.sh').is_file() and (parent / 'skills').is_dir():
            return parent
    raise ValueError('Cannot locate skills source repository')


def skill_roots():
    proc = subprocess.run(['bash', str(repository_root() / 'scripts/relink.sh'), '--list'],
                          capture_output=True, check=True)
    return [Path(os.fsdecode(p)) for p in proc.stdout.split(b'\0') if p]


def discover(home=None):
    home = home or Path.home()
    sources = skill_roots()  # One canonical scan for all providers.
    result = {}
    for name, (config, skills) in TOOLS.items():
        executable = shutil.which(name)
        # Gemini configuration is not evidence of an agy installation.
        residue = bool(config and (home / config).exists())
        links = {}
        for source in sources:
            target = home / skills / source.name
            links[source.name] = {**file_info(target),
                                  'matches_source': target.is_symlink() and target.resolve() == source.resolve(),
                                  'source_sha256': digest((source / 'SKILL.md').read_bytes())}
        result[name] = {'status': 'detected' if executable else ('unconfirmed' if residue else 'not_detected'),
                        'executable': executable, 'skills': links, 'runtime_verified': False}
    return result


def instruction_scan(project, home=None, limit=2000):
    home = (home or Path.home()).resolve()
    ancestors, found, errors = [], {}, []
    current = project
    for _ in range(64):
        ancestors.append(current)
        if (current / '.git').exists() or current == home or current.parent == current:
            break
        current = current.parent
    def capture(directory, scope):
        for name in INSTRUCTIONS:
            path = directory / name
            if path.exists() or path.is_symlink():
                try:
                    found[str(path)] = {'scope': scope, **file_info(path)}
                except OSError as error:
                    errors.append(str(error))
    for directory in reversed(ancestors):
        capture(directory, 'root' if directory == project else 'ancestor')
    visited, truncated = 0, False
    for directory, children, _ in os.walk(project, followlinks=False,
                                           onerror=lambda e: errors.append(str(e))):
        children[:] = sorted(c for c in children if c not in SKIP and
                             not (Path(directory) / c).is_symlink())
        visited += 1
        if visited > limit:
            truncated = True
            break
        if Path(directory) != project:
            capture(Path(directory), 'nested')
    return {'files': found, 'boundary': str(ancestors[-1]), 'truncated': truncated,
            'errors': errors, 'directories_scanned': min(visited, limit)}


def inspect(project):
    candidates = ['README.md', 'package.json', 'pyproject.toml', 'Makefile', 'Cargo.toml', 'go.mod']
    return {'project': str(project), 'tools': discover(),
            'instructions': {n: file_info(project / n) for n in (*FILES, REPORT)},
            'instruction_scan': instruction_scan(project),
            'candidates': [p for p in candidates if (project / p).exists()],
            'ci': sorted(str(p.relative_to(project)) for p in
                         (project / '.github/workflows').glob('*') if p.is_file()),
            'verification': 'structural_only'}


def state_path(project):
    folder = project / '.nathan-setup'
    if folder.is_symlink() or (folder.exists() and not folder.is_dir()):
        raise ValueError('Unsafe setup state directory')
    path = folder / 'state.json'
    if path.is_symlink():
        raise ValueError('Refusing symlinked state file')
    return path


def load_state(project):
    path = state_path(project)
    if path.exists():
        data = json.loads(path.read_text())
        if data.get('version') != 1:
            raise ValueError('Unsupported setup state version')
        return data
    return {'version': 1, 'managed': {}, 'runs': []}


@contextmanager
def locked(project):
    path = state_path(project)
    path.parent.mkdir(mode=0o700, exist_ok=True)
    ignore = path.parent / '.gitignore'
    if not ignore.exists() and not ignore.is_symlink():
        ignore.write_text('*\n')
    fd = os.open(path.parent / 'lock', os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'w') as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        yield


def atomic(path, data, expected=None):
    before = file_info(path)
    if before['kind'] not in ('missing', 'file'):
        raise ValueError('Refusing non-regular target: ' + str(path))
    if expected is not None and before.get('sha256') != expected:
        raise ValueError('File changed; read it again before writing')
    fd, temporary = tempfile.mkstemp(prefix='.nathan-setup-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, path.stat().st_mode & 0o777 if path.exists() else 0o600)
        if file_info(path) != before:
            raise ValueError('File changed during write; retry after reading')
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def save_state(project, state):
    atomic(state_path(project), json.dumps(state, ensure_ascii=False, indent=2).encode())


def block_span(text):
    if BEGIN not in text and END not in text:
        return None
    if text.count(BEGIN) != 1 or text.count(END) != 1 or text.index(END) < text.index(BEGIN):
        raise ValueError('Ambiguous management markers; preserve and resolve manually')
    return text.index(BEGIN), text.index(END) + len(END)


def plan_block(project, name, expected, content, accept_edited=False, remove=False):
    if name not in FILES:
        raise ValueError('Unsupported instruction file')
    path = project / name
    info = file_info(path)
    if info['kind'] not in ('missing', 'file'):
        raise ValueError('Refusing to edit symlink or non-regular instruction file')
    if info['sha256'] != expected:
        raise ValueError('Instruction file changed; read it again before writing')
    old = path.read_bytes() if path.exists() else b''
    text, state = old.decode('utf-8'), load_state(project)
    span = block_span(text)
    previous = state['managed'].get(name)
    managed = text[span[0]:span[1]] if span else ''
    edited = bool(span and (not previous or previous.get('block_hash') != digest(managed.encode())))
    if remove and (not previous or not span):
        raise ValueError('No owned managed block to remove')
    if remove and edited:
        raise ValueError('Managed block was edited; automatic removal refused')
    if not remove and (not content.strip() or BEGIN in content or END in content):
        raise ValueError('Content must be nonempty and contain no management markers')
    block = '' if remove else BEGIN + '\n' + content.rstrip() + '\n' + END
    if span and remove:
        # Drop the blank separator the writer inserted, so repeated
        # write/remove cycles do not accumulate blank lines.
        head, tail = text[:span[0]].rstrip('\n'), text[span[1]:].lstrip('\n')
        updated = head + '\n\n' + tail if head and tail else (head + '\n' if head else tail)
    elif span:
        updated = text[:span[0]] + block + text[span[1]:]
    else:
        updated = text + ('\n\n' if text else '') + block + '\n'
    return {'old': old, 'data': updated.encode(), 'state': state, 'block': block,
            'human_edits': edited, 'blocked': edited and not accept_edited,
            'diff': ''.join(difflib.unified_diff(text.splitlines(True), updated.splitlines(True),
                                               fromfile=name, tofile=name))}


def write_block(project, name, expected, content, dry_run=False, accept_edited=False, remove=False):
    if dry_run:
        plan = plan_block(project, name, expected, content, accept_edited, remove)
        return {k: plan[k] for k in ('diff', 'human_edits', 'blocked')}
    with locked(project):
        plan = plan_block(project, name, expected, content, accept_edited, remove)
        if plan['blocked']:
            raise ValueError('Human edits or unowned block detected; review dry-run diff, merge, then use --accept-edited-block')
        if plan['data'] == plan['old']:
            return {'file': name, 'status': 'unchanged', 'sha256': digest(plan['data'])}
        atomic(project / name, plan['data'], expected)
        state = plan['state']
        if remove:
            state['managed'].pop(name, None)
        else:
            state['managed'][name] = {'block_hash': digest(plan['block'].encode())}
        save_state(project, state)
        return {'file': name, 'status': 'removed' if remove else 'written',
                'sha256': digest(plan['data']), 'diff': plan['diff']}


def append_report(project, expected, content, dry_run=False):
    if not content.strip():
        raise ValueError('Empty report')
    path = project / REPORT
    def append():
        info = file_info(path)
        if info.get('sha256') != expected or info['kind'] not in ('missing', 'file'):
            raise ValueError('Report changed or is not a regular file')
        old = path.read_bytes() if path.exists() else b''
        entry = ('\n\n## Setup verification — ' + now() + '\n\n' + content.rstrip() + '\n').encode()
        if dry_run:
            return {'status': 'preview', 'append': entry.decode()}
        atomic(path, old + entry, expected)
        return {'status': 'appended', 'sha256': digest(old + entry)}
    if dry_run:
        return append()
    with locked(project):
        return append()


def has_import(text):
    # Accept a complete relative import token, not @AGENTS.md-other.
    in_fence = False
    for line in re.sub(r'<!--.*?-->', '', text, flags=re.S).splitlines():
        if line.lstrip().startswith(('```', '~~~')):
            in_fence = not in_fence
        if not in_fence and re.search(r'(?:^|\s)@(?:\./)?AGENTS\.md(?=\s|$)', line):
            return True
    return False


def connect(project, confirmed=(), dry_run=False):
    tools, scan = discover(), instruction_scan(project)
    result, shared = {}, project / 'AGENTS.md'
    for name, tool in tools.items():
        if not tool['executable'] and name not in confirmed:
            result[name] = {'status': 'needs_detection' if tool['status'] == 'unconfirmed' else 'not_detected',
                            'runtime_verified': False}
            continue
        warnings = [path for path, info in scan['files'].items()
                    if info['scope'] == 'nested' or Path(path).name == 'AGENTS.override.md']
        try:
            if not shared.is_file() or not shared.read_text().strip():
                raise ValueError('Missing or empty shared AGENTS.md')
            if name == 'claude':
                target = project / 'CLAUDE.md'
                if not target.exists() and not target.is_symlink():
                    if not dry_run:
                        with locked(project):
                            state = load_state(project)
                            target.symlink_to('AGENTS.md')
                            state['managed']['CLAUDE.md:link'] = 'AGENTS.md'
                            save_state(project, state)
                elif target.is_symlink():
                    if target.resolve() != shared.resolve():
                        raise ValueError('Existing CLAUDE.md symlink points elsewhere; preserved')
                elif not has_import(target.read_text()):
                    raise ValueError('Existing CLAUDE.md preserved; add a reviewed @AGENTS.md import')
                warnings += [p for p in scan['files'] if p.endswith(('.claude/CLAUDE.md', 'CLAUDE.local.md'))]
            result[name] = {'status': 'needs_scope_review' if warnings or scan['truncated'] or scan['errors']
                            else ('would_connect' if dry_run else 'structurally_connected'),
                            'scope_warnings': sorted(set(warnings)), 'runtime_verified': False}
        except (OSError, ValueError) as error:
            result[name] = {'status': 'blocked', 'reason': str(error), 'runtime_verified': False}
    return result


def remove_link(project, dry_run=False):
    def remove():
        state = load_state(project)
        target = project / 'CLAUDE.md'
        if state['managed'].get('CLAUDE.md:link') != 'AGENTS.md' or not target.is_symlink() or os.readlink(target) != 'AGENTS.md':
            raise ValueError('No unchanged setup-owned CLAUDE.md link to remove')
        if not dry_run:
            target.unlink()
            state['managed'].pop('CLAUDE.md:link')
            save_state(project, state)
        return {'status': 'would_remove' if dry_run else 'removed', 'file': 'CLAUDE.md'}
    if dry_run:
        return remove()
    with locked(project):
        return remove()


def fingerprint(project, tool):
    inventory = discover()[tool]
    executable = inventory.get('executable')
    if executable:
        stat = Path(executable).stat()
        inventory['executable_identity'] = [stat.st_size, stat.st_mtime_ns]
    home = Path.home()
    profile_roots = {'claude': home / '.claude', 'codex': Path(os.environ.get('CODEX_HOME', str(home / '.codex'))), 'agy': home / '.gemini/config'}
    profile = profile_roots[tool]
    inventory['profile'] = {name: file_info(profile / name) for name in
                            ('AGENTS.md', 'AGENTS.override.md', 'CLAUDE.md', 'settings.json', 'config.toml')}
    scan = instruction_scan(project)
    return digest(json.dumps({'files': scan['files'], 'tool': inventory}, sort_keys=True).encode())


def status(project):
    inventory, state = discover(), load_state(project)
    results = {}
    for tool, info in inventory.items():
        if info['status'] != 'detected':
            results[tool] = {'status': info['status']}
            continue
        runs = [r for r in state['runs'] if r['tool'] == tool]
        latest = runs[-1] if runs else None
        if not latest:
            results[tool] = {'status': 'pending'}
        elif latest['fingerprint'] != fingerprint(project, tool):
            results[tool] = {'status': 'stale', 'previous_run': latest['id']}
        else:
            results[tool] = {k: latest[k] for k in ('status', 'id', 'reason')}
    passed = sum(r['status'] == 'passed' for r in results.values())
    required = [r for r in results.values() if r['status'] != 'not_detected']
    return {'tools': results, 'overall': 'ready' if required and passed == len(required)
            else ('partially_ready' if passed else 'not_ready'), 'scope': 'instruction_and_skill_discovery_only'}


def runtime_command(tool, prompt, timeout=90, project=None):
    if tool == 'claude':
        return ['claude', '-p', '--permission-mode', 'plan', '--tools', 'Read,Glob,Grep',
                '--strict-mcp-config', '--mcp-config', '{"mcpServers":{}}',
                '--no-session-persistence', '--output-format', 'json', prompt]
    if tool == 'codex':
        return ['codex', 'exec', '--sandbox', 'read-only', '--skip-git-repo-check',
                '--ephemeral', '--color', 'never', prompt]
    # agy does not take its workspace from the working directory: without
    # --add-dir it reports an empty root and may answer from prior context
    # instead of the project being probed. Let it also return its envelope
    # before the outer kill, so a slow run reports a parseable status.
    return ['agy', '--mode', 'plan', '--sandbox', '--add-dir', str(project or Path.cwd()),
            '--print-timeout', '%ds' % max(10, int(timeout) - 10),
            '--output-format', 'json', '--print', prompt]


def skill_description():
    text = (Path(__file__).resolve().parents[1] / 'SKILL.md').read_text()
    return next(line.split(':', 1)[1].strip() for line in text.splitlines() if line.startswith('description:'))


def extract_proof(answer):
    """Pull the evidence object out of a provider answer.

    Providers are asked for JSON only, but some append a prose note after the
    closing fence or wrap the object in commentary. Refusing to parse those
    would report real, complete evidence as failed, so locate the object and
    let the field checks decide.
    """
    if not isinstance(answer, str):
        return {}
    text = answer.strip()
    fenced = re.findall(r'```(?:json)?\s*(.*?)```', text, re.DOTALL)
    decoder = json.JSONDecoder()
    for candidate in [block.strip() for block in fenced] + [text]:
        if not candidate:
            continue
        start = candidate.find('{')
        if start < 0:
            continue
        try:
            value, _ = decoder.raw_decode(candidate[start:])
        except ValueError:
            continue
        if isinstance(value, dict):
            return value
    return {}


def verify(project, tool, expected, timeout=90, retry=False, dry_run=False,
           question='Quote the exact value of Setup verification phrase from project instructions.'):
    if not expected.strip():
        raise ValueError('Provide a nonempty expected phrase from the project instructions')
    current = status(project)['tools'][tool]['status']
    previous = [r for r in load_state(project)['runs'] if r['tool'] == tool]
    if retry and current == 'passed' and previous[-1].get('expect_hash') == digest((question + '\n' + expected).encode()):
        return {'tool': tool, 'status': 'already_passed'}
    prompt = ('Use $nathan-setup as a read-only reference for this verification only; do not execute setup. '
              'Inspect the applicable project instruction sources and the provider personal skill entry '
              'for nathan-setup, including symlinks (Glob may omit symlinks). Use your built-in read-only '
              'file tools rather than shell commands, which a headless run may auto-deny; no writes, '
              'external actions or setup initialization. '
              'Return ONLY a JSON object with these fields: instruction_phrase (answer to this project-rule question: '
              + question + '), instruction_sources (list of paths), '
              'skill_available (boolean: can this provider read its installed skill entry), '
              'skill_path (installed entry path), skill_description (exact YAML description), '
              'steps (four concise workflow steps), conflicts (list of actual conflicts, empty if none). '
              'Do not infer missing skills solely from glob output. If an entry cannot be read, '
              'set skill_available false and describe that in conflicts.')
    command = runtime_command(tool, prompt, timeout, project)
    if dry_run:
        return {'command': command, 'cwd': str(project), 'status': 'preview'}
    before = fingerprint(project, tool)
    run = {'id': uuid.uuid4().hex, 'tool': tool, 'at': now(), 'fingerprint': before,
           'status': 'pending', 'reason': '', 'command': command[:-1], 'expect_hash': digest((question + '\n' + expected).encode())}
    try:
        with tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
            process = subprocess.Popen(command, cwd=project, stdin=subprocess.DEVNULL,
                                       stdout=stdout, stderr=stderr, start_new_session=True)
            try:
                process.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
                raise TimeoutError('CLI timed out; authentication or runtime may be unavailable')
            stdout.seek(0); output = stdout.read(2_000_000).decode(errors='replace')
            stderr.seek(0); error = stderr.read(200_000).decode(errors='replace')
        # Do not count echoed prompts/tool events as the final answer.
        answer, transport_issue = output, None
        if tool in ('claude', 'agy'):
            try:
                value = json.loads(output)
                if tool == 'agy' and value.get('status') != 'SUCCESS':
                    transport_issue = 'agy response status: ' + str(value.get('status', 'missing'))
                # Headless runs cannot prompt, so a required tool may be auto-denied.
                # That is an environment gap, not evidence that discovery failed.
                denied = value.get('denied_actions') or []
                if denied and not str(value.get('response', '')).strip():
                    transport_issue = ('provider auto-denied required tool permissions in headless mode: '
                                       + ', '.join(sorted({str(d.get('display_name') or d.get('action'))
                                                           for d in denied if isinstance(d, dict)}))
                                       + '; allow them for this provider or re-run interactively')
                if tool == 'claude' and value.get('is_error'):
                    transport_issue = 'Claude returned is_error'
                answer = value.get('result', value.get('response', ''))
                if not isinstance(answer, str):
                    answer = json.dumps(answer)
            except (ValueError, AttributeError):
                answer = ''
        run['evidence_sha256'] = digest(output.encode())
        run['exit_code'] = process.returncode
        proof = extract_proof(answer)
        installed = discover()[tool].get('skills', {}).get('nathan-setup', {})
        valid = (isinstance(proof, dict) and proof.get('instruction_phrase') == expected
                 and proof.get('skill_available') is True
                 and proof.get('skill_description') == skill_description()
                 and isinstance(proof.get('instruction_sources'), list) and proof['instruction_sources']
                 and isinstance(proof.get('steps'), list) and len(proof['steps']) == 4
                 and proof.get('conflicts') == [] and installed.get('matches_source') is True)
        if valid:
            try:
                valid = Path(proof['skill_path']).expanduser().resolve() in (
                    Path(__file__).resolve().parents[1], Path(__file__).resolve().parents[1] / 'SKILL.md')
            except (KeyError, TypeError, OSError):
                valid = False
        if transport_issue:
            run.update(status='pending', reason=transport_issue)
        elif process.returncode != 0:
            run.update(status='pending', reason='CLI unavailable or failed (exit %s); inspect authentication/runtime' % process.returncode)
        elif valid:
            run.update(status='passed', reason='Structured discovery evidence matches project phrase, installed skill and four steps; no reported conflicts')
        else:
            run.update(status='failed', reason='Final structured evidence missing, inconsistent, conflicting or not matched to installed skill')
        # Print bounded evidence for review, but never persist raw provider logs automatically.
        evidence = {'answer': answer[-12000:], 'diagnostic': error[-2000:] if process.returncode else '',
                    'response_envelope': {k: value.get(k) for k in ('status', 'subtype', 'is_error')}
                    if tool in ('claude', 'agy') and 'value' in locals() and isinstance(value, dict) else {}}
    except (OSError, TimeoutError) as error:
        run['reason'] = str(error)
        evidence = {}
    if fingerprint(project, tool) != before:
        run.update(status='stale', reason='Instructions or tool discovery changed during probe')
    with locked(project):
        state = load_state(project)
        state['runs'].append(run)
        save_state(project, state)
    return {**run, **evidence}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('inspect', 'write', 'connect', 'report', 'remove', 'status', 'verify'):
        child = sub.add_parser(name)
        child.add_argument('--project', required=True, type=Path)
        child.add_argument('--dry-run', action='store_true')
        if name in ('write', 'remove'):
            child.add_argument('--file', required=True, choices=FILES)
            child.add_argument('--expected', default='missing')
            child.add_argument('--link', action='store_true')
        if name in ('write', 'report'):
            child.add_argument('--content', required=True, type=Path)
        if name == 'write':
            child.add_argument('--accept-edited-block', action='store_true')
        if name == 'report':
            child.add_argument('--expected', required=True)
        if name == 'connect':
            child.add_argument('--tool', action='append', choices=TOOLS, default=[])
        if name == 'verify':
            child.add_argument('--tool', required=True, choices=TOOLS)
            child.add_argument('--expect', required=True)
            child.add_argument('--timeout', type=int, default=90)
            child.add_argument('--retry', action='store_true')
            child.add_argument('--question', default='Quote the exact value of Setup verification phrase from project instructions.')
    args = parser.parse_args()
    try:
        project = args.project.resolve(strict=True)
        if not project.is_dir():
            raise ValueError('Project must be a directory')
        if args.command == 'inspect': result = inspect(project)
        elif args.command == 'status': result = status(project)
        elif args.command == 'connect': result = connect(project, args.tool, args.dry_run)
        elif args.command == 'report': result = append_report(project, args.expected, args.content.read_text(), args.dry_run)
        elif args.command == 'verify': result = verify(project, args.tool, args.expect, args.timeout, args.retry, args.dry_run, args.question)
        elif args.command == 'remove':
            if args.link and args.file != 'CLAUDE.md': raise ValueError('Only CLAUDE.md link is managed')
            result = remove_link(project, args.dry_run) if args.link else write_block(project, args.file, args.expected, '', args.dry_run, remove=True)
        else: result = write_block(project, args.file, args.expected, args.content.read_text(), args.dry_run, args.accept_edited_block)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print(json.dumps({'error': str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
