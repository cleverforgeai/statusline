#!/usr/bin/env bash
# Made by CleverForge (github.com/cleverforgeai/statusline).
# Claude Code status line wrapper. Passes the status JSON to statusline.py.
input=$(cat)
PY=python3
command -v python3 >/dev/null 2>&1 || PY=python
printf '%s' "$input" | PYTHONUTF8=1 "$PY" "$(dirname "$0")/statusline.py"
