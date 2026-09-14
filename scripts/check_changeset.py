#!/usr/bin/env python3
"""Guard the two changeset rules this repository cares about.

  major   No changeset may request a major bump before 1.0. Changesets does not
          soften major on a 0.x version, so one would take 0.1.0 to 1.0.0.
  present A pull request that changes something a tool runs must add a
          changeset describing it.

Run with no arguments to check the working tree against the default base
branch; both checks can be waived, see --help.
"""
import argparse
from pathlib import Path
import re
import subprocess
import sys

REPO = Path(__file__).resolve().parent.parent
CHANGESET_DIR = REPO / '.changeset'
NOT_A_CHANGESET = {'README.md'}

# Changes under these paths are run by a tool, so they need a changeset.
RUNTIME_PREFIXES = ('skills/', 'scripts/')

FRONTMATTER = re.compile(r'\A---\s*\n(.*?)\n---\s*\n', re.DOTALL)
BUMP = re.compile(r'^\s*(?:"[^"]*"|\'[^\']*\'|[\w@/.-]+)\s*:\s*'
                  r'(major|minor|patch)\s*$', re.MULTILINE)


def changeset_files(directory=None):
    """Every pending changeset, ignoring the folder's own documentation."""
    directory = CHANGESET_DIR if directory is None else directory
    if not directory.is_dir():
        return []
    return sorted(p for p in directory.glob('*.md') if p.name not in NOT_A_CHANGESET)


def bumps(path):
    """The bump levels a changeset requests, or [] if it has no frontmatter."""
    match = FRONTMATTER.match(path.read_text(encoding='utf-8'))
    if not match:
        return []
    return BUMP.findall(match.group(1))


def check_major(files):
    """Report every changeset asking for a major bump."""
    return [(path, level) for path in files for level in bumps(path)
            if level == 'major']


def changed_files(base, repo=None):
    """Paths that differ from the base ref, or None if the ref is unknown."""
    repo = REPO if repo is None else repo
    merge_base = subprocess.run(['git', 'merge-base', 'HEAD', base],
                                cwd=repo, capture_output=True, text=True)
    if merge_base.returncode != 0:
        return None
    diff = subprocess.run(['git', 'diff', '--name-only',
                           merge_base.stdout.strip(), 'HEAD'],
                          cwd=repo, capture_output=True, text=True)
    if diff.returncode != 0:
        return None
    return [line for line in diff.stdout.splitlines() if line]


def needs_changeset(paths):
    """The changed paths that a tool actually runs."""
    return [p for p in paths if p.startswith(RUNTIME_PREFIXES)
            and not p.startswith('.changeset/')]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--base', default='origin/master',
                        help='branch this change will merge into (default: origin/master)')
    parser.add_argument('--allow-major', action='store_true',
                        help='permit a major bump — for the deliberate 1.0.0 release')
    parser.add_argument('--skip-present', action='store_true',
                        help='do not require a changeset — for a change no tool runs')
    args = parser.parse_args(argv)

    pending = changeset_files()
    failures = []

    offenders = check_major(pending)
    if offenders and not args.allow_major:
        for path, _ in offenders:
            failures.append(
                f'{path.relative_to(REPO)} asks for a major bump. Before 1.0 that '
                f'jumps the version straight to 1.0.0 — record breaking changes '
                f'as minor. Releasing 1.0.0 is deliberate: rerun with '
                f'--allow-major (CI: the allow-major label).')
    elif offenders:
        print(f'major bump allowed for {len(offenders)} changeset(s)')

    if args.skip_present:
        print('changeset requirement waived')
    else:
        changed = changed_files(args.base)
        if changed is None:
            print(f'cannot compare against {args.base}; skipping the '
                  f'changeset requirement', file=sys.stderr)
        else:
            runtime = needs_changeset(changed)
            added = [p for p in changed if p.startswith('.changeset/')
                     and not p.endswith('/README.md')]
            if runtime and not added:
                listed = '\n  '.join(runtime[:10])
                more = '' if len(runtime) <= 10 else f'\n  ... and {len(runtime) - 10} more'
                failures.append(
                    f'These change what a tool runs but no changeset was added:\n'
                    f'  {listed}{more}\n'
                    f'Run `npm run changeset`. For a change no tool runs, rerun '
                    f'with --skip-present (CI: the skip-changeset label).')

    for failure in failures:
        print(f'error: {failure}', file=sys.stderr)
    if failures:
        return 1
    print(f'changesets ok ({len(pending)} pending)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
