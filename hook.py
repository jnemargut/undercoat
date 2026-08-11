#!/usr/bin/env python3
"""
Undercoat: the write-time floor.

A Claude Code PreToolUse hook. Reads the tool call about to run, matches the content
against patterns.json, and refuses the write before the file lands.

  exit 0  allow (possibly with a warning attached)
  exit 2  refuse; stderr is fed back to the agent

Implemented in Python rather than shell because the job is JSON + regex + globs, and
python3 is present on more machines than jq is. The plan called this hook.sh; the
behavior is unchanged.

What this implements:
  rules carry scope globs, a reason, and a direction
  Write / Edit / MultiEdit / NotebookEdit, plus Bash write *routes*
  block where refusing is safe, warn otherwise, per-project mutes
  agent-directive refusal message, and a retry cap so a stuck agent stops
"""

import json
import os
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PATTERNS_FILE = HERE / "patterns.json"
LOCAL_MUTES = ".undercoat.local.json"

# The hook is registered globally in settings.json. Which projects it acts on depends
# on the mode:
#
#   default        opt-in.  A project is covered only if install.sh dropped a marker.
#   --global mode  opt-out. Every project is covered except those carrying .undercoat.off.
#
# Opt-out always wins over opt-in, so a single file disarms any project in either mode.
OPT_IN_MARKERS = (".undercoat.patterns.json", "UNDERCOAT.md")
OPT_OUT_MARKER = ".undercoat.off"
GLOBAL_FLAG = HERE / "global"

# Three attempts on the same rule and file, then stop and hand it to the human
# rather than letting the agent loop on a refusal.
RETRY_CAP = 3


# --------------------------------------------------------------------------- globs

def glob_to_regex(pattern: str) -> re.Pattern:
    """Translate a glob to a regex. Handles ** (any depth) and * (one segment)."""
    out, i = [], 0
    while i < len(pattern):
        if pattern.startswith("**/", i):
            out.append("(?:.*/)?")
            i += 3
        elif pattern.startswith("**", i):
            out.append(".*")
            i += 2
        elif pattern[i] == "*":
            out.append("[^/]*")
            i += 1
        elif pattern[i] == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(pattern[i]))
            i += 1
    return re.compile("^" + "".join(out) + "$")


def path_matches(path: str, patterns) -> bool:
    if not patterns:
        return False
    norm = str(path).replace("\\", "/").lstrip("./")
    return any(glob_to_regex(p).search(norm) for p in patterns)


def rule_applies_to(rule: dict, path: str) -> bool:
    if not path:
        return False
    if not path_matches(path, rule.get("in")):
        return False
    if path_matches(path, rule.get("not_in")):
        return False
    return True


# --------------------------------------------------------------------------- config

def project_root():
    """
    The directory to enforce in, or None to do nothing.

    Walks up from the cwd to the repo boundary looking for a marker. An opt-out
    marker stops enforcement anywhere it is found, in either mode. Otherwise an
    opt-in marker enables it; in global mode the repo root enables it by default.
    """
    global_mode = GLOBAL_FLAG.exists()

    for base in (Path.cwd(), *Path.cwd().parents):
        if (base / OPT_OUT_MARKER).exists():
            return None
        if any((base / marker).exists() for marker in OPT_IN_MARKERS):
            return base
        if (base / ".git").exists():
            return base if global_mode else None

    return Path.cwd() if global_mode else None


def load_rules(root: Path):
    """Project-local rules if the project shipped its own, else the installed set."""
    local = root / ".undercoat.patterns.json"
    source = local if local.is_file() else PATTERNS_FILE
    try:
        data = json.loads(source.read_text())
    except Exception as exc:  # a broken rules file must never block a build
        print(f"undercoat: could not read {source}: {exc}", file=sys.stderr)
        return []
    return data.get("rules", [])


def load_mutes() -> set:
    """Per-project muted rule ids. Local, uncommitted."""
    for base in (Path.cwd(), *Path.cwd().parents):
        candidate = base / LOCAL_MUTES
        if candidate.is_file():
            try:
                return set(json.loads(candidate.read_text()).get("off", []))
            except Exception:
                return set()
        if (base / ".git").exists():
            break
    return set()


# --------------------------------------------------------------------- what to check

def targets_from(tool_name: str, tool_input: dict):
    """Return [(path, content)] pairs this tool call would write."""
    if tool_name == "Write":
        return [(tool_input.get("file_path", ""), tool_input.get("content", "") or "")]

    if tool_name == "Edit":
        return [(tool_input.get("file_path", ""), tool_input.get("new_string", "") or "")]

    if tool_name == "MultiEdit":
        path = tool_input.get("file_path", "")
        joined = "\n".join(
            e.get("new_string", "") or "" for e in tool_input.get("edits", []) or []
        )
        return [(path, joined)]

    if tool_name == "NotebookEdit":
        path = tool_input.get("notebook_path", "") or tool_input.get("file_path", "")
        return [(path, tool_input.get("new_source", "") or "")]

    return []


# Shell constructs that put bytes into a file. We refuse the *route*, not the
# content traveling down it, a far smaller job than parsing shell.
BASH_WRITE_ROUTES = [
    (re.compile(r"(?<![0-9&])>>?\s*([^\s;|&'\"<>]+)"), "redirect"),
    (re.compile(r"\btee\b(?:\s+-\w+)*\s+([^\s;|&'\"<>]+)"), "tee"),
    (re.compile(r"\bsed\b[^;|&]*?\s-i\b[^;|&]*?\s([^\s;|&'\"<>]+)"), "sed -i"),
    (re.compile(r"\bdd\b[^;|&]*?\bof=([^\s;|&'\"<>]+)"), "dd of="),
    (re.compile(r"\bperl\b[^;|&]*?\s-i\b[^;|&]*?\s([^\s;|&'\"<>]+)"), "perl -i"),
]


def bash_write_targets(command: str):
    """Paths this shell command would write to, with the construct that does it."""
    found = []
    for pattern, label in BASH_WRITE_ROUTES:
        for match in pattern.finditer(command or ""):
            target = match.group(1).strip()
            if target and not target.startswith("/dev/"):
                found.append((target, label))
    return found


# ------------------------------------------------------------------------ retry cap

def attempt_count(session_id: str, rule_id: str, path: str) -> int:
    """Count refusals of this rule on this file, and record one more."""
    state_file = Path(tempfile.gettempdir()) / f"undercoat-{session_id or 'nosession'}.json"
    try:
        state = json.loads(state_file.read_text())
    except Exception:
        state = {}
    key = f"{rule_id}::{path}"
    state[key] = state.get(key, 0) + 1
    try:
        state_file.write_text(json.dumps(state))
    except Exception:
        pass  # a read-only tmp must not turn into a broken build
    return state[key]


# -------------------------------------------------------------------------- messages

def refusal(rule: dict, path: str, matched: str) -> str:
    """A directive, not a complaint. The agent is the reader, not the human."""
    return "\n".join([
        f"REFUSED  undercoat/{rule['id']}",
        f"FILE  {path}",
        f"MATCH  {matched!r}",
        f"WHY  {rule['because']}",
        f"CONSTRAINT  {rule['instead']}",
        "DO NOT  ask the user to approve this. Choose a direction and rewrite the file.",
    ])


def stop_message(rule: dict, path: str, count: int) -> str:
    return "\n".join([
        f"STOP  undercoat/{rule['id']}",
        f"FILE  {path}",
        f"This write has been refused {count} times for the same rule.",
        "DO NOT  retry again. Stop and tell the user what you were trying to do and why the",
        f"rule is in the way, so they can decide. They can mute it with: "
        f'{{"off": ["{rule["id"]}"]}} in {LOCAL_MUTES}',
    ])


def note(rule: dict, path: str, matched: str) -> str:
    """Warn tier: same shape, no prohibition."""
    return "\n".join([
        f"NOTE  undercoat/{rule['id']}",
        f"FILE  {path}",
        f"MATCH  {matched!r}",
        f"WHY  {rule['because']}",
        f"CONSIDER  {rule['instead']}",
    ])


def allow_with_note(text: str):
    """
    Attach a note to an allowed write.

    NOTE: whether the agent actually reads permissionDecisionReason on an allow is
    unverified. If warnings are visibly ignored across a few builds, promote those
    rules to block or delete the tier.
    We also write to stderr so the note is at least visible to the human.
    """
    print(text, file=sys.stderr)
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": text,
        }
    }))


# ------------------------------------------------------------------------------ main

def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0  # never break a build over a payload we cannot read

    tool_name = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {}) or {}
    session_id = payload.get("session_id", "")

    # Opted out, or not a project at all, so do nothing.
    root = project_root()
    if root is None:
        return 0

    rules = load_rules(root)
    if not rules:
        return 0
    muted = load_mutes()
    active = [r for r in rules if r["id"] not in muted]

    # --- Bash: refuse the route, so blocking Write cannot push the agent into a heredoc
    if tool_name == "Bash":
        command = tool_input.get("command", "") or ""
        covered = {g for r in active for g in r.get("in", [])}
        exempt = {g for r in active for g in r.get("not_in", [])}
        for target, construct in bash_write_targets(command):
            if path_matches(target, covered) and not path_matches(target, exempt):
                print("\n".join([
                    "REFUSED  undercoat/shell-write-route",
                    f"FILE  {target}",
                    f"MATCH  {construct}",
                    "WHY  Undercoat checks files at the write. A shell redirect bypasses that "
                    "check, so the floor would not apply to this file.",
                    "CONSTRAINT  Use the Write or Edit tool for files Undercoat covers.",
                    "DO NOT  ask the user to approve this. Reissue the change as a Write.",
                ]), file=sys.stderr)
                return 2
        return 0

    warnings = []
    for path, content in targets_from(tool_name, tool_input):
        if not content:
            continue
        for rule in active:
            if not rule_applies_to(rule, path):
                continue
            found = re.search(rule["match"], content)
            if not found:
                continue

            matched = found.group(0)
            if len(matched) > 60:
                matched = matched[:57] + "..."

            if rule["severity"] == "block":
                count = attempt_count(session_id, rule["id"], path)
                if count >= RETRY_CAP:
                    print(stop_message(rule, path, count), file=sys.stderr)
                else:
                    print(refusal(rule, path, matched), file=sys.stderr)
                return 2

            warnings.append(note(rule, path, matched))

    if warnings:
        allow_with_note("\n\n".join(warnings))

    return 0


if __name__ == "__main__":
    sys.exit(main())
