# Supplied command-guard prototype: not installed

This is retained for review, not used as a security boundary. Its own 44 tests
pass, but verdict() returns allow for git symbolic-ref with a write operand,
git diff --output, sed w and sort -o. Unknown payloads also fail open. No hook
is installed by this skill. A real read-only environment must enforce writes
outside the model; this prototype cannot supply that guarantee.

The supplied hooks README describes possible adapters, not verified integrations.
The supplied reviewer had a machine-specific Claude hook path; that path and
provider-specific tool lists are deliberately absent from the portable reviewer.
Do not install this prototype or claim it protects any provider without a
separate implementation and adversarial runtime validation.

Original Python source follows, retained as inert Markdown:

```python
#!/usr/bin/env python3
# hooks/readonly-guard.py
"""Shell command guard: allow read-only commands, deny the rest.

Two layers, deliberately separate:

  POLICY   `verdict(command)` — a pure function, no I/O, no provider knowledge.
           Returns None to allow, or a human-readable reason to deny. This is the
           part worth keeping; everything else is plumbing.

  ADAPTERS `main()` — reads a command out of whatever the caller hands over and
           reports the verdict in whatever form the caller expects. Adding support
           for a new AI tool means adding an input shape or an output format here,
           never touching the policy.

Usage:
  readonly-guard.py                      read JSON (or a raw command) on stdin
  readonly-guard.py --command "git log"  check one command directly
  readonly-guard.py --self-test          run the built-in case suite

  --deny-exit N   exit code used for a denial (default 2, which is what Claude
                  Code's PreToolUse hooks expect; other tools use 1)
  --format FMT    `exit` (default) writes the reason to stderr and signals via
                  exit code. `claude-json` emits a PreToolUse permission decision
                  on stdout and exits 0.

Allowlist, not denylist: the set of commands a read-only agent needs is small and
knowable, while enumerating what's forbidden in a shell is a game you lose. Anything
unrecognised is denied with a reason the caller can read and route around.
"""

import argparse
import json
import re
import shlex
import sys

# ---------------------------------------------------------------- policy

# Read-only inspection commands a reviewer legitimately needs.
ALLOWED = {
    "ls", "cat", "head", "tail", "wc", "nl", "file", "stat", "pwd", "echo", "printf",
    "grep", "egrep", "fgrep", "rg", "ag", "ack", "find", "fd", "tree",
    "sort", "uniq", "cut", "tr", "comm", "diff", "column", "jq", "yq",
    "basename", "dirname", "realpath", "which", "type", "date", "od", "xxd",
    "git", "sed", "awk",  # gated further below
}

# git subcommands that cannot change refs, the index, or the working tree.
# branch/tag/remote/config/stash are deliberately absent: each has an operand form
# that writes, and a reviewer has read-only substitutes (rev-parse, for-each-ref).
GIT_READONLY = {
    "diff", "diff-tree", "diff-files", "diff-index", "log", "show", "status",
    "blame", "annotate", "describe", "shortlog", "whatchanged", "grep",
    "rev-parse", "rev-list", "merge-base", "name-rev", "symbolic-ref", "show-ref",
    "for-each-ref", "ls-files", "ls-tree", "cat-file", "count-objects", "version",
}

OPERATORS = ("&&", "||", ";", "|", "&", "\n")


class Denied(Exception):
    """Raised inside the policy; converted to a return value by verdict()."""


def _deny(reason):
    raise Denied(reason)


def _strip_quoted(s):
    """Blank out quoted spans so operator scanning doesn't trip on quoted punctuation."""
    return re.sub(r"'[^']*'|\"[^\"]*\"", "''", s)


def _substitutions(s):
    """Inner commands of $(...) and `...`, so substitution can't smuggle a command."""
    return re.findall(r"\$\(([^()]*)\)", s) + re.findall(r"`([^`]*)`", s)


def _check_segment(tokens, original):
    # Drop leading VAR=value assignments.
    while tokens and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", tokens[0]):
        tokens = tokens[1:]
    if not tokens:
        return

    # Match on the basename so /usr/bin/git resolves like git — and /bin/sh like sh,
    # which is not on the allowlist.
    name = tokens[0].rsplit("/", 1)[-1]
    args = tokens[1:]

    if name not in ALLOWED:
        _deny(f"'{name}' is not on the read-only allowlist. Command: {original}")

    if name == "git":
        sub = next((a for a in args if not a.startswith("-")), None)
        if sub is None:
            _deny(f"bare 'git' with no subcommand. Command: {original}")
        if sub not in GIT_READONLY:
            _deny(
                f"'git {sub}' is not a read-only git subcommand. "
                f"Allowed: {', '.join(sorted(GIT_READONLY))}. Command: {original}"
            )

    if name == "sed" and any(a.startswith("-i") or a == "--in-place" for a in args):
        _deny(f"'sed -i' edits files in place. Command: {original}")

    if name == "find":
        for bad in ("-delete", "-exec", "-execdir", "-ok", "-okdir", "-fprint", "-fls"):
            if bad in args:
                _deny(f"'find {bad}' can write or run commands. Command: {original}")

    if name == "awk" and any("system(" in a or "print >" in a or "printf >" in a for a in args):
        _deny(f"awk program writes or shells out. Command: {original}")


def _check(command, depth=0):
    if depth > 3:
        _deny("command substitution nested too deeply to verify.")

    for inner in _substitutions(command):
        _check(inner, depth + 1)

    # Redirections write files. Allow only the stderr/stdout merge forms.
    scan = re.sub(r"\d?>&\d?", "", _strip_quoted(command))
    if ">" in scan:
        _deny(f"output redirection writes to a file. Command: {command}")

    # Strip substitutions before tokenising; they were checked above.
    flat = re.sub(r"\$\([^()]*\)|`[^`]*`", "X", command)

    try:
        lexer = shlex.shlex(flat, posix=True, punctuation_chars=True)
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError as exc:
        _deny(f"could not parse command ({exc}). Command: {command}")

    segment = []
    for tok in tokens:
        if tok in OPERATORS:
            _check_segment(segment, command)
            segment = []
        else:
            segment.append(tok)
    _check_segment(segment, command)


def verdict(command):
    """None if the command is read-only; otherwise a reason string. Pure."""
    command = (command or "").strip()
    if not command:
        return None
    try:
        _check(command)
    except Denied as exc:
        return str(exc)
    return None


# ---------------------------------------------------------------- adapters

# Where different tools put the shell command in their hook payload. Extend this
# list to support a new provider — the policy above stays untouched.
COMMAND_PATHS = (
    ("tool_input", "command"),   # Claude Code PreToolUse
    ("toolInput", "command"),    # camelCase variants
    ("input", "command"),
    ("command",),                # bare payloads
)


def extract_command(payload):
    for path in COMMAND_PATHS:
        node = payload
        for key in path:
            if not isinstance(node, dict) or key not in node:
                node = None
                break
            node = node[key]
        if isinstance(node, str):
            return node
    return None


def read_stdin_command():
    """Pull a command out of stdin: JSON in a known shape, or a raw command line."""
    raw = sys.stdin.read()
    if not raw.strip():
        return None, False
    try:
        payload = json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        return raw, True  # Not JSON — treat the whole of stdin as the command.

    if not isinstance(payload, dict):
        return None, False

    # Claude Code fires one hook for every tool; only Bash carries a shell command.
    tool = payload.get("tool_name") or payload.get("toolName")
    if tool is not None and tool not in ("Bash", "bash", "shell", "run_command"):
        return None, False

    return extract_command(payload), True


def main():
    ap = argparse.ArgumentParser(add_help=True, description=__doc__.split("\n")[0])
    ap.add_argument("--command", help="check this command instead of reading stdin")
    ap.add_argument("--deny-exit", type=int, default=2,
                    help="exit code for a denial (default 2; Claude Code expects 2)")
    ap.add_argument("--format", choices=("exit", "claude-json"), default="exit")
    ap.add_argument("--self-test", action="store_true", help="run the built-in case suite")
    args = ap.parse_args()

    if args.self_test:
        sys.exit(self_test())

    if args.command is not None:
        command, recognised = args.command, True
    else:
        command, recognised = read_stdin_command()

    # Nothing we can judge — a non-shell tool call, an unknown payload shape, or an
    # empty command. Stay out of the way rather than blocking on our own ignorance.
    if not recognised or command is None:
        sys.exit(0)

    reason = verdict(command)
    if reason is None:
        sys.exit(0)

    reason = f"[read-only guard] {reason}"
    if args.format == "claude-json":
        json.dump({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }}, sys.stdout)
        sys.exit(0)

    print(reason, file=sys.stderr)
    sys.exit(args.deny_exit)


# ---------------------------------------------------------------- self-test

CASES = [
    # (should_allow, command)
    (True,  "git diff origin/main...HEAD"),
    (True,  "git log origin/main..HEAD --oneline"),
    (True,  "git show HEAD:src/foo.ts"),
    (True,  "git ls-files 'src/**/*.tsx'"),
    (True,  'grep -rn "a|b" src/'),                 # quoted pipe must not split
    (True,  "grep -rn 'foo' src | head -50"),
    (True,  "git diff $(git merge-base origin/main HEAD)..HEAD"),
    (True,  "git diff --stat && git log --oneline -5"),
    (True,  "cat package.json | jq -r '.name'"),
    (True,  "find . -name '*.scss' -not -path '*/node_modules/*'"),
    (True,  "git status 2>&1"),
    (True,  "/usr/bin/git diff"),
    (True,  "NODE_ENV=test git diff"),
    (True,  "sed -n '1,50p' src/foo.ts"),
    (False, "git commit -m 'fix'"),
    (False, "git push origin HEAD"),
    (False, "git checkout -- src/foo.ts"),
    (False, "git reset --hard origin/main"),
    (False, "git stash"),
    (False, "git clean -fd"),
    (False, "git apply patch.diff"),
    (False, "git branch -D feature"),
    (False, "git config user.name hacker"),
    (False, "rm -rf build"),
    (False, "mv a.ts b.ts"),
    (False, "npm install"),
    (False, "echo x > src/foo.ts"),
    (False, "git diff >> out.txt"),
    (False, "sed -i '' 's/a/b/' src/foo.ts"),
    (False, "sed -i.bak s/a/b/ f.ts"),
    (False, "find . -name '*.ts' -delete"),
    (False, r"find . -exec rm {} \;"),
    (False, "git diff && git commit -m x"),         # chained
    (False, "git diff; rm -rf /tmp/x"),             # chained
    (False, "git log | xargs rm"),                  # piped into denied
    (False, "sh -c 'git commit -m x'"),             # shell wrapper
    (False, "bash -c 'rm -rf .'"),
    (False, "/bin/sh -c 'git push'"),
    (False, "echo $(rm -rf build)"),                # substitution smuggling
    (False, "git diff `git commit -m x`"),          # backtick smuggling
    (False, "env FOO=1 rm x"),
    (False, "awk 'BEGIN{system(\"rm -rf .\")}'"),
    (False, "tee out.txt"),
    (False, "python3 -c 'import os;os.remove(\"x\")'"),
]


def self_test():
    failures = []
    for should_allow, command in CASES:
        reason = verdict(command)
        if should_allow != (reason is None):
            failures.append((should_allow, command, reason))
    print(f"{len(CASES) - len(failures)}/{len(CASES)} passed")
    for should_allow, command, reason in failures:
        want = "allow" if should_allow else "deny"
        print(f"  expected {want}: {command}\n      {reason}")
    return 1 if failures else 0


if __name__ == "__main__":
    main()

```
