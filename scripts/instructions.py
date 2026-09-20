#!/usr/bin/env python3
"""Install/remove this clone's shared communication links, preserving other files."""
import argparse
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "instructions/communication.md"


def targets(home):
    return [home / ".codex/AGENTS.md", home / ".claude/CLAUDE.md",
            home / ".gemini/config/rules/AGENTS.md"]


def apply(home, source, remove=False, dry_run=False):
    failed = False
    for target in targets(home):
        # Exact absolute link identity, including a dangling link after deletion.
        # Never follow or adopt another source's symlink.
        ours = target.is_symlink() and os.readlink(target) == str(source)
        exists = target.exists() or target.is_symlink()
        if remove:
            if ours:
                if not dry_run:
                    target.unlink()
                print(f"{'WOULD REMOVE' if dry_run else 'REMOVE'} {target}")
            elif exists:
                print(f"KEEP {target}: not this clone's link")
            continue
        override = target.with_name("AGENTS.override.md")
        if target == targets(home)[0] and (override.exists() or override.is_symlink()):
            print(f"SKIP {target}: inspect {override} first", file=sys.stderr)
            failed = True
            continue
        if ours:
            print(f"OK {target}")
        elif exists:
            print(f"SKIP {target}: existing file or foreign link", file=sys.stderr)
            failed = True
        else:
            if not dry_run:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.symlink_to(source)
            print(f"{'WOULD LINK' if dry_run else 'LINK'} {target}")
    return int(failed)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["install", "remove"])
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.action == "install":
        gitdir = subprocess.check_output(
            ["git", "rev-parse", "--absolute-git-dir"], cwd=ROOT, text=True).strip()
        common = subprocess.check_output(
            ["git", "rev-parse", "--git-common-dir"], cwd=ROOT, text=True).strip()
        if Path(gitdir).resolve() != (ROOT / common).resolve():
            parser.error("install from the main checkout, never a linked worktree")
        if not SOURCE.is_file():
            parser.error(f"missing {SOURCE}")
        configured = os.environ.get("CODEX_HOME")
        if configured and Path(configured).expanduser().resolve() != Path.home() / ".codex":
            parser.error("custom CODEX_HOME: configure its instruction entry manually")
    return apply(Path.home(), SOURCE, args.action == "remove", args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
