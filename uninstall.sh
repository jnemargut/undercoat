#!/usr/bin/env bash
# Reverses install.sh. Prints every action.

set -euo pipefail

TARGET="${1:-$PWD}"
CLAUDE_DIR="${HOME}/.claude"
SETTINGS="${CLAUDE_DIR}/settings.json"

echo "Removing Undercoat from ${TARGET}"

for f in UNDERCOAT.md .undercoat.patterns.json; do
  if [ -f "${TARGET}/${f}" ]; then
    rm "${TARGET}/${f}"
    echo "  → removed ${TARGET}/${f}"
  fi
done

if [ -f "${TARGET}/AGENTS.md" ] && grep -q "^@UNDERCOAT.md$" "${TARGET}/AGENTS.md"; then
  python3 - "${TARGET}/AGENTS.md" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1])
lines = [l for l in p.read_text().splitlines() if l.strip() != "@UNDERCOAT.md"]
p.write_text("\n".join(lines).rstrip() + "\n")
PY
  echo "  → removed the @UNDERCOAT.md include from AGENTS.md"
elif [ -f "${TARGET}/AGENTS.md" ] && head -1 "${TARGET}/AGENTS.md" | grep -q "Generated from patterns.json"; then
  rm "${TARGET}/AGENTS.md"
  echo "  → removed ${TARGET}/AGENTS.md (it was ours)"
fi

echo "  · left .undercoat.local.json and the .gitignore line alone — yours to delete"

if [ -f "$SETTINGS" ]; then
  python3 - "$SETTINGS" <<'PY'
import json, pathlib, sys
p = pathlib.Path(sys.argv[1])
try:
    settings = json.loads(p.read_text())
except Exception as exc:
    print(f"  ! could not parse {p} ({exc}); remove the hook by hand")
    sys.exit(0)

pre = settings.get("hooks", {}).get("PreToolUse", [])
before = len(pre)
kept = []
for entry in pre:
    hooks = [h for h in entry.get("hooks", []) if "undercoat" not in str(h.get("command", ""))]
    if hooks:
        entry["hooks"] = hooks
        kept.append(entry)
    elif not entry.get("hooks"):
        kept.append(entry)

if len(kept) != before or any("undercoat" in json.dumps(e) for e in pre):
    settings["hooks"]["PreToolUse"] = kept
    if not kept:
        settings["hooks"].pop("PreToolUse", None)
    if not settings.get("hooks"):
        settings.pop("hooks", None)
    p.write_text(json.dumps(settings, indent=2) + "\n")
    print(f"  → removed the Undercoat hook from {p}")
else:
    print(f"  · no Undercoat hook found in {p}")
PY
fi

if [ -f "${CLAUDE_DIR}/undercoat/global" ]; then
  echo "  → global mode was on; clearing it"
fi
rm -rf "${CLAUDE_DIR}/undercoat"
echo "  → removed ${CLAUDE_DIR}/undercoat"
rm -f /tmp/undercoat-*.json 2>/dev/null || true

echo
echo "✓ Undercoat removed."
