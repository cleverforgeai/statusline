---
name: statusline
author: CleverForge
metadata:
  made_by: CleverForge
  source: github.com/cleverforgeai/statusline
description: Guided setup for the Claude Code status line. Use when the user types /statusline, or asks to set up, change or fix their status line, what it shows, favorite animation, country flags, mood, organization or compact alerts. Asks a few quick questions, applies the answers, shows a preview, and asks the user to confirm.
---

# Status line setup

Made by CleverForge (github.com/cleverforgeai/statusline).

The user should never have to read docs or edit files. You ask, they answer, you apply it and show the result.

CLI: `python3 ~/.claude/statusline.py <command>` (use `python` on Windows). Run the commands yourself.

## 1. Check the install

Make sure `~/.claude/statusline.py`, `~/.claude/statusline-command.sh` and a `statusLine` entry in `~/.claude/settings.json` exist. If not, tell the user to run the installer from a clone of the repo:

- macOS, Linux, Git Bash: `gh repo clone cleverforgeai/statusline && cd statusline && STATUSLINE_LOCAL="$PWD" bash install.sh`
- Windows PowerShell: `gh repo clone cleverforgeai/statusline; cd statusline; $env:STATUSLINE_LOCAL=$PWD; .\install.ps1`

Never overwrite other keys in `settings.json`. If a different `statusLine` already exists, show it and ask before replacing.

## 2. Pick the path

Read `~/.claude/statusline.config.json`.

- `setup_done` is not `true`: run the **guided setup** below.
- `setup_done` is `true`: ask with AskUserQuestion what to change (What it shows, Animation, Flags, Mood, Organization, Alerts, Start over). Do only that part, then step 4.

## 3. Guided setup

The line is short by default. The user decides what to add. Keep everything friendly and quick.

**Call 1.** One AskUserQuestion call with four questions:

1. **How much do you want on your status line?** Options: Minimal (just the model and memory bar), Standard (recommended: project, branch, model, memory bar, tasks, plus the fun row), Full (everything: GitHub and PR, tokens, cost, time, organization), Pick my own.
2. **Favorite animation?** Options: 🚗 car, 🦋 butterfly, 🐈 cat chasing a mouse, 🚀 rocket. "Other" lets them type any name or emoji.
3. **How are you feeling today?** Options: 😄 great, 😴 tired, 🔥 on fire, 🎯 focused. "Other" for anything else.
4. **Fun "time to /compact" warnings when memory runs low?** Options: yes (recommended), no.

**If they chose "Pick my own"**, ask one more AskUserQuestion call, all multi-select, nothing preselected beyond what they tick:

- **Project info:** branch changes (+/-), GitHub repo and PR, task list, organization name.
- **Usage info:** token count, cost, session time.
- **Fun row:** country flags, mood, animation, heart line.

Start from `preset minimal`, then `parts on <ticked names>`. Part names: `diff`, `github`, `tasks`, `org`, `tokens`, `cost`, `time`, `flags`, `mood`, `animation`, `heart` (also `app`, `branch`, `model`, `context`, `alerts`). Run `parts` to see them all.

**Then, only if needed**, ask in plain chat (one short message each, wait for the answer):

- If the organization piece is on: "What organization name should I show? Or say 'use my GitHub name'."
- If flags are on (Standard and Full include them): "Which countries' flags do you want? Name up to 10, or say skip."

Apply the answers:

| Answer | Command |
|---|---|
| Minimal / Standard / Full | `preset minimal`, `preset standard`, `preset full` |
| Pick my own | `preset minimal`, then `parts on ...` |
| Animation from the list | `sprite <name>`. Run `sprite` with no name to see all 24. An emoji that matches one (🐌) uses that name |
| Any other emoji or word | `sprite custom <emoji>` (one emoji) |
| "Surprise me" | `sprite random` |
| Mood | `mood <emoji> <label>` |
| GitHub name | `org ""` (and `parts on org` if it is off) |
| A typed name | `org "<name>"` (and `parts on org` if it is off) |
| Flags | `flags US PR IT`. Convert country names to 2-letter codes yourself. Max 10; if they name more, use the first 10 and say which were skipped. "Skip" means `flags clear` |
| Alerts | `parts on alerts` or `parts off alerts` |

Run `preset` first, because it resets any piece overrides.

## 4. Show and confirm

Run `python3 ~/.claude/statusline.py show` and put its output in a code block. Say the preview uses made-up project data (MyApp), and that the real line shows their real project. Then ask with AskUserQuestion: **"Does this look right?"** Options: "Looks great", "Change something".

- "Looks great": run `confirm`. Say it is saved, and that if the status line does not appear at the bottom they should open a new Claude Code session.
- "Change something": ask which part, redo only that part, show again.

Useful previews: `show minimal`, `show standard`, `show full` (compare layouts without saving) and `show low` (the low-memory warning). Offer `show full` once if they are unsure how much to add.

## Notes to keep honest

- The animation moves while Claude is working (about once a second) and rests with 💤 when idle.
- Flags use emoji. Some Windows terminals draw them as letters like `US`. If so, say so and offer `flags clear`.
- The heart line and warnings follow remaining context. `/compact` or `/clear` frees it and the heart recovers.
- Claude Code sends no organization or account name, which is why the organization comes from GitHub or what the user types.
- Never edit `statusline.config.json` by hand when a command exists. Use `set <key> <json>` for any other option.
- Full list of options: the README in the repo.
