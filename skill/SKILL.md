---
name: statusline
author: CleverForge
metadata:
  made_by: CleverForge
  source: github.com/cleverforgeai/statusline
description: Guided setup for the Claude Code status line. Use when the user types /statusline, or asks to set up, change or fix their status line, favorite animation, country flags, mood, organization or compact alerts. Asks a few quick questions, applies the answers, shows a preview, and asks the user to confirm.
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
- `setup_done` is `true`: ask with AskUserQuestion what to change (Animation, Flags, Mood, Organization, Alerts, Start over). Do only that part, then step 4.

## 3. Guided setup

Keep it short and friendly. One AskUserQuestion call with these four questions:

1. **Favorite animation?** Options: 🚗 car, 🦋 butterfly, 🐈 cat chasing a mouse, 🚀 rocket. "Other" lets them type any name or emoji.
2. **How are you feeling today?** Options: 😄 great, 😴 tired, 🔥 on fire, 🎯 focused. "Other" for anything else.
3. **Organization name?** Options: use my GitHub name, hide it. "Other" to type a name.
4. **Fun "time to /compact" warnings when memory runs low?** Options: yes (recommended), no.

Then ask in plain chat, as a separate message: **"Which countries' flags do you want on your line? Name up to 10, or say skip."** Wait for the answer.

Apply the answers:

| Answer | Command |
|---|---|
| Animation from the list | `sprite <name>`. Run `sprite` with no name to see all 24. An emoji that matches one (🐌) uses that name |
| Any other emoji or word | `sprite custom <emoji>` (one emoji) |
| "Surprise me" | `sprite random` |
| Mood | `mood <emoji> <label>` |
| GitHub name | `org ""` and `set show_org true` |
| A typed name | `org "<name>"` and `set show_org true` |
| Hide organization | `set show_org false` |
| Flags | `flags US PR IT`. Convert country names to 2-letter codes yourself. Max 10; if they name more, use the first 10 and say which were skipped. "Skip" means `flags clear` |
| Alerts | `set compact_alert true` or `set compact_alert false` |

## 4. Show and confirm

Run `python3 ~/.claude/statusline.py show` and put its output in a code block so the user sees their line. Then ask with AskUserQuestion: **"Does this look right?"** Options: "Looks great", "Change something".

- "Looks great": run `confirm`. Say it is saved, and that if the status line does not appear at the bottom they should open a new Claude Code session.
- "Change something": ask which part, redo only that part, show again.

Offer once, in one line, to preview the low-memory warning with `show low`.

## Notes to keep honest

- The animation moves while Claude is working (about once a second) and rests with 💤 when idle.
- Flags use emoji. Some Windows terminals draw them as letter pairs like `US`. If so, say so and offer `flags clear`.
- The heart line and warnings follow remaining context. `/compact` or `/clear` frees it and the heart recovers.
- Claude Code sends no organization or account name, which is why the organization comes from GitHub or what the user types.
- Never edit `statusline.config.json` by hand when a command exists. Use `set <key> <json>` for any other option.
- Full list of options: docs/REFERENCE.md in the repo.
