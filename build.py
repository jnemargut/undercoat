#!/usr/bin/env python3
"""
Undercoat: render AGENTS.md from patterns.json.

patterns.json is the original; AGENTS.md is generated and committed (design decision 2),
so nobody installing Undercoat ever runs a build step. This script is for you.

  python3 build.py           write AGENTS.md
  python3 build.py --check   exit 1 if AGENTS.md is stale (for CI / pre-commit)
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PATTERNS = HERE / "patterns.json"
OUTPUT = HERE / "AGENTS.md"

HEADER = """<!-- Generated from patterns.json by build.py. Do not edit by hand. -->

# Undercoat

The invisible layer that keeps AI-built interfaces from looking AI-built.

This file is the floor. It will not make an interface beautiful. It exists to stop one
looking machine-made. Every rule below is a documented tell of machine-made
interfaces. A rule refuses a write only when its match means one thing and almost
nobody wants that thing on purpose; everything else advises.

On tools that support hooks, the `block` rules are enforced at the write and the file
never lands. Everywhere else, this file is all there is, so read it and honour it.
"""

FOOTER = """
## When a rule is wrong

Some projects genuinely need a banned pattern. A brand really is purple, a client
really did specify that face. Mute the rule for the project rather than working around
it:

```json
// .undercoat.local.json  (local, not committed)
{ "off": ["ai-purple"] }
```

Muting is per-rule and per-project on purpose. There is no per-line escape hatch,
because an agent could write one and grant itself permission.
"""


def section(rules, severity, title, preamble):
    picked = [r for r in rules if r["severity"] == severity]
    if not picked:
        return ""
    out = [f"\n## {title}\n", preamble, ""]
    for rule in picked:
        out.append(f"### {rule['id']}\n")
        out.append(f"{rule['because']}\n")
        out.append(f"**Instead:** {rule['instead']}\n")
        scope = ", ".join(f"`{g}`" for g in rule["in"])
        out.append(f"*Applies to: {scope}*")
        if rule.get("risk_note"):
            out.append(f"\n*Advises rather than blocks: {rule['risk_note']}*")
        out.append("")
    return "\n".join(out)


def render() -> str:
    data = json.loads(PATTERNS.read_text())
    rules = data["rules"]
    body = HEADER
    body += section(
        rules, "block", "Do not write these",
        "Patterns that mean one thing and that almost nobody wants on purpose. On Claude "
        "Code these are refused at the write, and the file will not be created until they "
        "are gone.",
    )
    body += section(
        rules, "warn", "Think twice about these",
        "Real tells that fail one of the two blocking tests. Either the match is a proxy "
        "that also catches legitimate code, or the pattern is sometimes wanted "
        "deliberately. These do not block anything.",
    )
    body += FOOTER
    return body


def main() -> int:
    rendered = render()
    if "--check" in sys.argv:
        current = OUTPUT.read_text() if OUTPUT.exists() else ""
        if current != rendered:
            print("AGENTS.md is stale. Run: python3 build.py", file=sys.stderr)
            return 1
        print("AGENTS.md is up to date.")
        return 0
    OUTPUT.write_text(rendered)
    counts = {}
    for rule in json.loads(PATTERNS.read_text())["rules"]:
        counts[rule["severity"]] = counts.get(rule["severity"], 0) + 1
    print(f"Wrote {OUTPUT.name}: {counts.get('block', 0)} block, {counts.get('warn', 0)} warn.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
