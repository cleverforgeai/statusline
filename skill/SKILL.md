---
name: statusline
author: CleverForge
metadata:
  made_by: CleverForge
  source: github.com/cleverforgeai/statusline
description: Install, check, or adjust the Claude Code status line (phase, branch, GitHub repo and PR, task and subtask progress, organization, mood of the day, animated sprite, heart-line life meter, model, context, cost). Use when the user types /statusline, asks to set or change their favorite animation, mood, sprite or organization, or wants to set up or fix the status line. On a first run, ask the user for their favorite animation.
---

# Status line

Made by CleverForge (github.com/CleverForgeAI). Run `python3 ~/.claude/statusline.py about` to see the installed version.

Files in `~/.claude/`:
- `statusline.py`: all the logic and a small CLI.
- `statusline-command.sh`: wrapper that Claude Code calls.
- `statusline.config.json`: options.
- `settings.json`: has the `statusLine` entry, including `"refreshInterval": 1`. The animation needs that timer.

Run the CLI with `python3 ~/.claude/statusline.py <command>` (use `python` on Windows).

## When invoked

1. Check the install: the files above exist and `settings.json` points `statusLine.command` at `statusline-command.sh`.
2. If anything is missing, give the installer:
   - macOS, Linux, Git Bash: `gh repo clone cleverforgeai/statusline && cd statusline && STATUSLINE_LOCAL="$PWD" bash install.sh`
   - Windows PowerShell: `gh repo clone cleverforgeai/statusline; cd statusline; $env:STATUSLINE_LOCAL=$PWD; .\install.ps1`
3. Test: `echo '{"model":{"display_name":"Claude Sonnet"},"context_window":{"remaining_percentage":59},"cwd":"<repo path>"}' | bash ~/.claude/statusline-command.sh`. Confirm three lines of output at most and no Python errors.
4. Tell the user to open a new session after changes to `settings.json`.
5. Read `~/.claude/statusline.config.json`. If `sprite_chosen` is not `true`, run the favorite animation flow below before anything else. The status line also shows a small `🎬?` next to the sprite until a favorite is picked.

## Favorite animation

Ask the user what their favorite animation is, then put it in the line.

1. Ask "What's your favorite animation?" with AskUserQuestion. Offer four options: 🚗 car, 🦋 butterfly, 🐈 cat chasing a mouse, 🚀 rocket. The user can pick "Other" to type any name or any emoji. If they want to browse first, run `python3 ~/.claude/statusline.py sprite` and show them the list (24 animations plus `random` and `custom`).
2. Set it:
   - A name from the list: `python3 ~/.claude/statusline.py sprite <name>` (cat, shark, pacman, snail, ball, dancer and so on).
   - An emoji that belongs to a listed animation (for example 🐌): use that animation's name.
   - Any other emoji or word they like (for example 🐙): `python3 ~/.claude/statusline.py sprite custom 🐙`. One emoji only.
   - "Surprise me": `python3 ~/.claude/statusline.py sprite random`.
3. Confirm in one line what was set. Say it moves while Claude is working and rests with 💤 when idle, and that the change shows up within a second or on the next update.
4. Then offer to set today's mood (see below).


## Mood of the day

When the user asks for `/statusline mood` or says how they feel:
1. Ask "How are you feeling today?" with AskUserQuestion. Offer 😄 great, 😴 tired, 🔥 on fire, 🎯 focused. The user can type any other emoji or word.
2. Run `python3 ~/.claude/statusline.py mood <emoji> <label>`. Full list: `python3 ~/.claude/statusline.py mood`.
3. The mood is stamped with today's date. Tomorrow the line shows `🙂?` until a new one is set. Turn the reminder off with `set mood_reminder false`.

## Other commands

- `sprite`: list every animation. `sprite <name>`: choose one. `sprite random`: a different one per session. `sprite custom <emoji>`: use your own emoji.
- `org "<name>"`: set the organization name. Empty string goes back to the GitHub owner.
- `set <key> <json>`: change any option, e.g. `set life_source "lowest"` or `set fun_line false`.
- `preview`: print every sprite and the heart line at different life levels.

## Config keys

| Key | Default | Meaning |
|---|---|---|
| `apps` | `{}` | Folder keyword to display name. |
| `org` | `""` | Organization name. Blank uses the GitHub owner. Claude Code does not send an account or organization name. |
| `show_org`, `show_mood`, `show_github`, `show_tasks`, `show_memory` | on, on, on, on, off | Turn segments on or off. |
| `memory_file` | none | MEMORY.md path for `show_memory`. |
| `fun_line` | `true` | The third line (organization, mood, sprite, heart). |
| `animate` | `true` | Sprite and heart line. |
| `sprite` | `car` | Animation name, `random` (stable per session) or `custom`. |
| `custom_emoji` | none | The emoji used when `sprite` is `custom`. |
| `sprite_chosen` | `false` | Set to `true` once the user has picked a favorite. While `false`, a `🎬?` hint shows. |
| `fav_reminder` | `true` | Show the `🎬?` hint until a favorite is chosen. |
| `life_source` | `context` | What the heart tracks: `context` (remaining context), `five_hour` (plan limit, subscribers only), or `lowest`. |
| `active_seconds` | `8` | How long the sprite keeps moving after the last change. |
| `two_lines` | `true` | Tasks on their own line. |
| `use_gh` | `true` | Fall back to the `gh` CLI for the PR when Claude Code does not send one. |

## How it behaves

- The sprite moves while tokens, cost or the transcript change. When nothing changes for `active_seconds` it stops and shows 💤.
- The heart line is an ECG. It scrolls with the timer, spikes shrink as life drops, beats start to skip under 30%, and it flatlines at 3% or less. The sprite becomes 🪫 and the heart becomes 💔.
- Life is context remaining by default, so it refills after `/compact` or `/clear`.
- Animation is about one frame per second, because Claude Code re-runs the script at most on its timer and debounces updates at 300ms.

## Tasks and subtasks

Claude Code tasks have no parent field. A task shows as a subtask when its metadata has `parent` set to the parent task id, or its subject reads `Parent subject > Child subject`. Use one of those forms when creating tasks.

## Rules

- Never overwrite other keys in `settings.json`. Merge only `statusLine`.
- If a different `statusLine` exists, show it to the user and ask before replacing.
