#!/usr/bin/env bash
# Made by CleverForge (github.com/CleverForgeAI). Private repository.
# Installer for the Claude Code status line (macOS, Linux, Git Bash on Windows).
#
# Private repo, recommended: clone it, then install from the local folder.
#   gh repo clone cleverforgeai/statusline && cd statusline && STATUSLINE_LOCAL="$PWD" bash install.sh
# Private repo, one-liner with a GitHub token (needs read access to the repo):
#   curl -fsSL -H "Authorization: token $GH_TOKEN" https://raw.githubusercontent.com/cleverforgeai/statusline/main/install.sh | STATUSLINE_TOKEN="$GH_TOKEN" bash
# Env: STATUSLINE_REPO owner/repo, STATUSLINE_BASE raw URL base, STATUSLINE_TOKEN GitHub token,
#      STATUSLINE_LOCAL local folder, STATUSLINE_REFRESH seconds (0 = no timer).
set -euo pipefail

OWNER_REPO="${STATUSLINE_REPO:-cleverforgeai/statusline}"
BASE="${STATUSLINE_BASE:-https://raw.githubusercontent.com/${OWNER_REPO}/main}"
DEST="$HOME/.claude"
SETTINGS="$DEST/settings.json"

PY=python3
command -v python3 >/dev/null 2>&1 || PY=python
command -v "$PY" >/dev/null 2>&1 || { echo "Python 3 is required." >&2; exit 1; }
command -v git >/dev/null 2>&1 || echo "Warning: git not found. Git and GitHub segments will be empty." >&2

mkdir -p "$DEST/skills/statusline"

fetch() { # fetch <remote-path> <dest>
  if [ -n "${STATUSLINE_LOCAL:-}" ]; then cp "$STATUSLINE_LOCAL/$1" "$2"
  elif [ -n "${STATUSLINE_TOKEN:-}" ]; then curl -fsSL -H "Authorization: token $STATUSLINE_TOKEN" "$BASE/$1" -o "$2"
  else curl -fsSL "$BASE/$1" -o "$2"; fi
}

for f in statusline.py statusline-command.sh; do
  [ -f "$DEST/$f" ] && cp "$DEST/$f" "$DEST/$f.bak"
  fetch "$f" "$DEST/$f"
done
chmod +x "$DEST/statusline-command.sh"
fetch "skill/SKILL.md" "$DEST/skills/statusline/SKILL.md"

[ -f "$DEST/statusline.config.json" ] || cat > "$DEST/statusline.config.json" <<'EOF'
{
  "apps": {},
  "show_github": true,
  "show_tasks": true,
  "show_memory": false,
  "two_lines": true,
  "fun_line": true,
  "animate": true,
  "sprite": "car",
  "sprite_chosen": false,
  "setup_done": false,
  "flags": [],
  "compact_alert": true,
  "fav_reminder": true,
  "org": "",
  "life_source": "context"
}
EOF

# Merge only the statusLine key. Back up settings first.
[ -f "$SETTINGS" ] && cp "$SETTINGS" "$SETTINGS.bak"
CMD="bash $DEST/statusline-command.sh"
REFRESH="${STATUSLINE_REFRESH:-1}"   # seconds; 0 turns the timer off (no animation while idle)
"$PY" - "$SETTINGS" "$CMD" "$REFRESH" <<'PYEOF'
import json, sys, os
path, cmd, refresh = sys.argv[1], sys.argv[2], int(sys.argv[3])
data = {}
if os.path.exists(path):
    try:
        data = json.load(open(path, encoding='utf-8'))
    except Exception:
        print("settings.json is not valid JSON. Left untouched.", file=sys.stderr); sys.exit(1)
old = data.get("statusLine")
if old and old.get("command") != cmd:
    print(f"Replacing existing statusLine (backup at {path}.bak): {old.get('command')}")
new = {"type": "command", "command": cmd}
if refresh > 0:
    new["refreshInterval"] = refresh
data["statusLine"] = new
json.dump(data, open(path, "w", encoding="utf-8"), indent=2)
PYEOF

echo "Statusline Kit installed. Made by CleverForge."
echo "Restart Claude Code (or open a new session) to see the status line."
echo "Last step: open Claude Code and type /statusline. Claude asks a few quick questions and sets it all up."
echo "Edit $DEST/statusline.config.json to name your apps. Run /statusline in Claude Code to adjust."
