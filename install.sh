#!/usr/bin/env bash
# Undercoat installer. Prints every action. Reverse it with ./uninstall.sh
#
# Installs two things:
#   1. AGENTS.md + patterns.json into the target project  (works with any agent tool)
#   2. a PreToolUse hook into ~/.claude/settings.json      (Claude Code enforcement)
#
# Step 2 is the upgrade, not the product. Skip it with --no-hook and the floor still
# applies as guidance everywhere else.

set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${1:-$PWD}"
CLAUDE_DIR="${HOME}/.claude"
SETTINGS="${CLAUDE_DIR}/settings.json"
HOOK_DEST="${CLAUDE_DIR}/undercoat/hook.py"
WANT_HOOK=1

for arg in "$@"; do
  [ "$arg" = "--no-hook" ] && WANT_HOOK=0
done
[ "${1:-}" = "--no-hook" ] && TARGET="$PWD"

if [ "$TARGET" = "$SRC" ]; then
  echo "Refusing to install into Undercoat's own directory."
  echo "Usage: $SRC/install.sh /path/to/your/project"
  exit 1
fi

echo "Undercoat → ${TARGET}"

# --- 1. the portable half -----------------------------------------------------
cp "${SRC}/AGENTS.md" "${TARGET}/UNDERCOAT.md"
echo "  → wrote ${TARGET}/UNDERCOAT.md"

if [ -f "${TARGET}/AGENTS.md" ]; then
  if grep -q "Undercoat" "${TARGET}/AGENTS.md"; then
    echo "  · AGENTS.md already references Undercoat, left alone"
  else
    printf '\n@UNDERCOAT.md\n' >> "${TARGET}/AGENTS.md"
    echo "  → appended @UNDERCOAT.md to your existing AGENTS.md"
  fi
else
  cp "${SRC}/AGENTS.md" "${TARGET}/AGENTS.md"
  echo "  → wrote ${TARGET}/AGENTS.md"
fi

cp "${SRC}/patterns.json" "${TARGET}/.undercoat.patterns.json"
echo "  → wrote ${TARGET}/.undercoat.patterns.json"

# mutes are local and must not travel with the repo (design decision 5)
if [ -f "${TARGET}/.gitignore" ] && grep -qx ".undercoat.local.json" "${TARGET}/.gitignore"; then
  echo "  · .gitignore already covers .undercoat.local.json"
else
  printf '\n# Undercoat: locally muted rules, not shared\n.undercoat.local.json\n' >> "${TARGET}/.gitignore"
  echo "  → added .undercoat.local.json to ${TARGET}/.gitignore"
fi

if [ "$WANT_HOOK" -eq 0 ]; then
  echo
  echo "✓ Undercoat installed as guidance. Skipped the hook (--no-hook)."
  exit 0
fi

# --- 2. the enforcement half --------------------------------------------------
mkdir -p "$(dirname "$HOOK_DEST")"
cp "${SRC}/hook.py" "$HOOK_DEST"
cp "${SRC}/patterns.json" "$(dirname "$HOOK_DEST")/patterns.json"
chmod +x "$HOOK_DEST"
echo "  → installed hook to ${HOOK_DEST}"

python3 - "$SETTINGS" "$HOOK_DEST" <<'PY'
import json, sys, pathlib

settings_path, hook_path = pathlib.Path(sys.argv[1]), sys.argv[2]
command = f"python3 {hook_path}"

settings = {}
if settings_path.exists():
    raw = settings_path.read_text().strip()
    if raw:
        try:
            settings = json.loads(raw)
        except json.JSONDecodeError as exc:
            # Refuse rather than guess — this file governs the whole agent setup.
            print(f"  ! {settings_path} is not valid JSON ({exc}).")
            print("  ! Refusing to touch it. Add this hook by hand:")
            print(f'  !   PreToolUse matcher "Write|Edit|MultiEdit|NotebookEdit|Bash" -> {command}')
            sys.exit(3)

hooks = settings.setdefault("hooks", {})
pre = hooks.setdefault("PreToolUse", [])

for entry in pre:
    for h in entry.get("hooks", []):
        if "undercoat" in str(h.get("command", "")):
            print("  · settings.json already has an Undercoat hook, left alone")
            sys.exit(0)

conflicting = [
    e for e in pre
    if e.get("matcher") == "Write|Edit|MultiEdit|NotebookEdit|Bash"
]
if conflicting:
    print("  ! An existing PreToolUse entry already uses this exact matcher.")
    print("  ! Refusing to merge automatically. Add this to its hooks list by hand:")
    print(f'  !   {{"type": "command", "command": "{command}"}}')
    sys.exit(3)

pre.append({
    "matcher": "Write|Edit|MultiEdit|NotebookEdit|Bash",
    "hooks": [{"type": "command", "command": command}],
})

settings_path.parent.mkdir(parents=True, exist_ok=True)
if settings_path.exists():
    backup = settings_path.with_suffix(".json.undercoat-backup")
    backup.write_text(settings_path.read_text())
    print(f"  → backed up settings to {backup.name}")
settings_path.write_text(json.dumps(settings, indent=2) + "\n")
print(f"  → added PreToolUse hook to {settings_path}")
PY

echo
echo "✓ Undercoat active. 25 rules block, 31 advise."
echo "  Mute a rule for this project:  echo '{\"off\":[\"ai-purple\"]}' > .undercoat.local.json"
echo "  Remove it entirely:            ${SRC}/uninstall.sh ${TARGET}"
