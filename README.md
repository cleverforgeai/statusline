# ✨ Statusline

**Made by CleverForge** · [github.com/cleverforgeai/statusline](https://github.com/cleverforgeai/statusline)

> Turn the quiet strip at the bottom of Claude Code into a live dashboard: what you're working on, how much of Claude's memory is left, what it's costing, and a little animation that moves while Claude works. 🚗💨

```
MyApp:feature | feat/login (+42 -7) | gh:acme/myapp ↑2 PR #31 approved | Sonnet 5.5 | ████░░░░░░ 41% | 82.0K tok/200K | $0.4120 | 18min
tasks ■■■□□□□□ 3/8 | ▶ Build login form [1/3 sub] › Wire up validation
🏢 Acme | 🔥 shipping day | ··🦋············ | ♥ ▁▁█▃▁▃▁▁▁▂▁▁ 59%
```

---

## Contents

1. [What is this?](#what-is-this)
2. [Before you start](#before-you-start)
3. [Install in 3 steps](#install-in-3-steps)
4. [Your first minute](#your-first-minute)
5. [How to read your status line](#how-to-read-your-status-line)
6. [Animations](#animations)
7. [The heart line](#the-heart-line)
8. [Mood and organization](#mood-and-organization)
9. [Command cheat sheet](#command-cheat-sheet)
10. [Settings](#settings)
11. [Troubleshooting](#troubleshooting)
12. [Privacy and safety](#privacy-and-safety)
13. [Uninstall](#uninstall)
14. [Roadmap](#roadmap)

---

## What is this?

**Claude Code** is Anthropic's coding assistant that lives in your terminal. At the bottom of its window there is a **status line**: one or more lines of text that Claude Code lets *you* control. Out of the box it is plain. This kit fills it with useful, glanceable information.

You do not need to be a programmer to use it. If you can open a terminal and paste a command, you can install it.

**What you get**

| | |
|---|---|
| 📍 **Where am I?** | Project name, git branch, GitHub repo, and the state of your pull request |
| 🧠 **How much memory is left?** | A bar showing how full Claude's "context window" is (explained below) |
| 💸 **What is this costing?** | Tokens used, estimated cost, and how long the session has run |
| ✅ **What is Claude doing?** | Your task list with progress, the current task, and its current step |
| 🎬 **Something fun** | An animation that moves while Claude works, a heartbeat that fades as memory runs low, your mood of the day |

### Two words you will see a lot

- **Token**: a small chunk of text, roughly three quarters of a word. Everything you and Claude say is counted in tokens.
- **Context window**: how much of the conversation Claude can hold in mind at once. Think of it as a whiteboard. When it fills up, older things get squeezed out and Claude can lose track. The status line shows how full the whiteboard is, so you know when to tidy up with `/compact` (summarize and free space) or `/clear` (start fresh).

---

## Before you start

You need three things. Here is how to check each one. Open a terminal and run:

```bash
claude --version     # Claude Code itself
python3 --version    # Python 3 (on Windows try: python --version)
git --version        # Git
```

If each prints a version number, you are ready. If one says "command not found":

| Missing | Get it |
|---|---|
| Claude Code | Follow the [official setup guide](https://code.claude.com/docs/en/overview) |
| Python 3 | [python.org/downloads](https://www.python.org/downloads/) (on Windows, tick "Add Python to PATH") |
| Git | [git-scm.com](https://git-scm.com/downloads). **Windows users:** Git for Windows also provides the `bash` this kit needs |
| GitHub CLI (`gh`), recommended | [cli.github.com](https://cli.github.com/). After installing, run `gh auth login` once |

The GitHub CLI is optional for *using* the status line, but it makes installing from a private repo painless.

> **Which terminal?** Any works: Terminal on macOS, Windows Terminal, the terminal inside VS Code, and so on. Modern terminals draw the emoji best.

---

## Install in 3 steps

> This repository is currently **private**, so you need access to it, and the usual one-line `curl | bash` trick returns "404" without a token. Cloning is the simplest route.

### Step 1: Download the kit

```bash
gh repo clone cleverforgeai/statusline
cd statusline
```

No `gh`? On the repo page click **Code → Download ZIP**, unzip it, and open a terminal inside the unzipped folder.

### Step 2: Run the installer

**macOS, Linux, or Git Bash on Windows**

```bash
STATUSLINE_LOCAL="$PWD" bash install.sh
```

**Windows PowerShell**

```powershell
$env:STATUSLINE_LOCAL = $PWD; .\install.ps1
```

You should see `Statusline Kit installed. Made by CleverForge.`

### Step 3: Restart Claude Code

Close Claude Code and open it again (or just start a new session). The new status line appears at the bottom. 🎉

<details>
<summary>Prefer a one-liner with a token?</summary>

Create a GitHub token that can read this repo, then:

```bash
export GH_TOKEN=your_token_here
curl -fsSL -H "Authorization: token $GH_TOKEN" https://raw.githubusercontent.com/cleverforgeai/statusline/main/install.sh | STATUSLINE_TOKEN="$GH_TOKEN" bash
```
</details>

### What the installer touches

It is deliberately gentle:

- Copies `statusline.py`, `statusline-command.sh` and the `/statusline` skill into your `~/.claude/` folder.
- Creates `~/.claude/statusline.config.json` **only if it does not exist yet**.
- Adds one entry (`statusLine`) to `~/.claude/settings.json`. **Your other settings are left alone.**
- Saves a `.bak` backup of anything it replaces.
- If you already had a different status line, the installer tells you what it replaced.

---

## Your first minute

1. Open Claude Code.
2. Type **`/statusline`** and press Enter.
3. Claude asks: **"What's your favorite animation?"** Pick one, or choose *Other* and type any emoji (🐙, 🦖, anything).
4. Claude offers to set your **mood of the day**. Say how you feel.

That is it. Ask Claude to do something and watch the little animation on the third line start moving. When Claude finishes and things go quiet, it stops and shows 💤.

Until you pick a favorite, a small `🎬?` hint sits next to the animation as a reminder.

---

## How to read your status line

The status line has up to three rows.

### Row 1: Where you are and how things look

```
MyApp:feature | feat/login (+42 -7) | gh:acme/myapp ↑2 PR #31 approved | Sonnet 5.5 | ████░░░░░░ 41% | 82.0K tok/200K | $0.4120 | 18min
```

| Piece | Meaning |
|---|---|
| `MyApp:feature` | Your project folder name, and a **phase** guessed from the git branch name (table below) |
| `feat/login (+42 -7)` | The git branch, with lines you have added (green) and removed (red) since the last commit |
| `gh:acme/myapp` | The GitHub repository this folder belongs to |
| `↑2` / `↓1` | Your branch is 2 commits ahead of / 1 behind GitHub. `synced` means equal. `no upstream` means this branch has not been pushed yet |
| `PR #31 approved` | Your open pull request and its review state (`approved`, `changes requested`, `draft`) |
| `Sonnet 5.5` | The Claude model in use |
| `████░░░░░░ 41%` | How full the context window is. 🟢 under 50%, 🟡 50 to 75%, 🔴 above 75% |
| `82.0K tok/200K` | Tokens used out of the model's maximum |
| `$0.4120` | Estimated cost of this session |
| `18min` | How long the session has run |

**Phases** come from the first letters of your branch name:

| Branch starts with | Phase | | Branch starts with | Phase |
|---|---|---|---|---|
| `main`, `master` | `prod` | | `refactor` | `refactor` |
| `feat` | `feature` | | `chore` | `chore` |
| `fix`, `bug` | `bugfix` | | `deploy` | `deploy` |
| `hotfix` | `hotfix` | | `test` | `testing` |
| `release` | `release` | | anything else | `dev` |

No git in the folder? You will see `init` and the git parts quietly disappear.

### Row 2: What Claude is working on

```
tasks ■■■□□□□□ 3/8 | ▶ Build login form [1/3 sub] › Wire up validation
```

When Claude keeps a to-do list, this row shows overall progress (3 of 8 done), the task in progress (▶), how many of its sub-steps are done, and the sub-step it is on now. No task list yet? The row simply does not appear.

### Row 3: The fun line

```
🏢 Acme | 🔥 shipping day | ··🦋············ | ♥ ▁▁█▃▁▃▁▁▁▂▁▁ 59%
```

Organization, your mood, your animation, and the heart line. All of it is optional and can be switched off.

---

## Animations

The animation moves while something is happening (tokens, cost or the session transcript changing) and rests with 💤 after about 8 seconds of quiet. Pick yours with `/statusline`, or run:

```bash
python3 ~/.claude/statusline.py sprite cat
```

(On Windows use `python` instead of `python3`.)

| Name | Looks like | What it does |
|---|---|---|
| `ball` | ⚽ | Bounces back and forth |
| `bee` | 🐝 | Buzzes around |
| `bike` | 🚲 | Pedals down the path |
| `butterfly` | 🦋 | Flutters up and down |
| `can` | 🥫 | Rolls over bumpy ground |
| `car` | 🚗 | Cruises down the road |
| `cat` | 🐈 ➜ 🐁 | A cat chases a mouse |
| `dancer` | 💃 🕺 | Dances along, swapping moves |
| `dog` | 🐕 | Runs and runs |
| `fish` | 🐠 | Swims through the water |
| `ghost` | 👻 | Floats and drifts |
| `horse` | 🏇 | Gallops along |
| `pacman` | 👻 ➜ 🟡 | Munches dots with a ghost behind |
| `plane` | 🛫 | Takes off and keeps flying |
| `rocket` | 🚀 | Blasts across the sky |
| `sailboat` | ⛵ | Sails over rolling waves |
| `shark` | 🦈 ➜ 🐟 | A shark chases a fish through the waves |
| `snail` | 🐌 | Slow and steady |
| `snake` | 🐍 | Slithers side to side |
| `train` | 🚂 | Chugs along the tracks |
| `turtle` | 🐢 | Takes its time |
| `ufo` | 🛸 | Hovers and zips about |
| `walker` | 🚶 🏃 | Walks, then jogs |
| `random` | 🎲 | A different animation for every Claude Code session |
| `custom` | ✨ | Your own emoji, for example `sprite custom 🐙` |

Want to see them all? `python3 ~/.claude/statusline.py preview` draws every animation, moving and resting.

**Good to know**

- Animations move about **once per second** at best. That is a Claude Code limit on how often it refreshes the status line, not a bug.
- A very long single answer can look idle until it finishes, because activity is detected from changes in tokens, cost and the transcript.
- When the heart flatlines, the animation turns into a 🪫 low battery.

---

## The heart line

```
♥ ▁▁█▃▁▃▁▁▁▂▁▁ 59%
```

It is an ECG heartbeat that **tracks how much context (memory) Claude has left**.

| Remaining | What you see | What it means |
|---|---|---|
| 50% or more | 🟢 Strong, regular beats | All good |
| 25 to 50% | 🟡 Beats get smaller (they start **skipping** under 30%) | Getting fuller |
| 8 to 25% | 🟠 Small beats, and under 12% only one in three | Time to `/compact` |
| 4 to 8% | 🔴 Faint, rare beats | Do it now |
| 3% or less | 🔴 **Flatline**, 💔, animation becomes 🪫 | Context is nearly gone |

**The heart comes back to life** after `/compact` or `/clear`, because context is freed up. Nothing is permanently lost.

On a Pro or Max plan you can track your **5-hour usage limit** instead:

```bash
python3 ~/.claude/statusline.py set life_source '"five_hour"'
```

Use `'"lowest"'` to follow whichever is lower, and `'"context"'` to go back.

---

## Mood and organization

**Mood of the day.** Type `/statusline mood` in Claude Code, or run:

```bash
python3 ~/.claude/statusline.py mood 😴 tired
```

It lasts one day. Tomorrow it shows `🙂?` until you pick again. To silence the reminder: `set mood_reminder false`.

**Organization.** Claude Code does not tell the status line your organization name, so the kit uses your GitHub owner by default. To set your own:

```bash
python3 ~/.claude/statusline.py org "My Team"
```

An empty name (`org ""`) goes back to the GitHub owner.

---

## Command cheat sheet

Run these in any terminal (use `python` on Windows if `python3` is not found). All of them are also available through `/statusline` in Claude Code.

| Command | What it does |
|---|---|
| `statusline.py sprite` | List every animation |
| `statusline.py sprite <name>` | Choose your animation |
| `statusline.py sprite custom 🐙` | Use any emoji as your animation |
| `statusline.py sprite random` | A different animation per session |
| `statusline.py mood 😄 great` | Set today's mood |
| `statusline.py org "Name"` | Set the organization name |
| `statusline.py set <key> <json>` | Change any setting (see below) |
| `statusline.py preview` | Show all animations and heart levels |
| `statusline.py about` | Version and credits |

Run them as `python3 ~/.claude/statusline.py <command>`.

---

## Settings

Your settings live in `~/.claude/statusline.config.json`. Change one with `set`, for example:

```bash
python3 ~/.claude/statusline.py set fun_line false      # hide row 3
python3 ~/.claude/statusline.py set show_tasks false    # hide row 2
```

| Setting | Default | What it does |
|---|---|---|
| `fun_line` | `true` | Show the third row |
| `animate` | `true` | Animation and heart line |
| `sprite` | `car` | Animation name, `random`, or `custom` |
| `custom_emoji` | none | Emoji used when `sprite` is `custom` |
| `sprite_chosen` | `false` | Becomes `true` when you pick a favorite |
| `fav_reminder` | `true` | Show the `🎬?` hint until you pick |
| `life_source` | `context` | What the heart tracks: `context`, `five_hour`, `lowest` |
| `active_seconds` | `8` | How long the animation keeps moving after the last change |
| `org` | blank | Organization name. Blank means your GitHub owner |
| `show_org`, `show_mood` | `true` | Parts of the fun line |
| `mood_reminder` | `true` | Show `🙂?` when no mood is set today |
| `show_github` | `true` | The GitHub part of row 1 |
| `use_gh` | `true` | Ask the `gh` tool for your PR when Claude Code does not provide it |
| `show_tasks` | `true` | Row 2 |
| `two_lines` | `true` | Tasks on their own row (`false` squeezes them into row 1) |
| `show_memory`, `memory_file` | off | Show a section count from a notes file you point at |
| `apps` | `{}` | Friendly names, e.g. `{"datahub": "DataHub"}` maps any folder containing "datahub" to "DataHub" |

**Sub-tasks.** Claude Code tasks have no built-in parent/child link. A task shows as a sub-step when its metadata has `parent` set to the parent task's id, or when it is named `Parent task > Sub task`. The `/statusline` skill tells Claude to use these forms.

**Refresh timer.** The installer sets `"refreshInterval": 1` so the animation moves even while Claude is quiet. Git results are cached for 3 seconds and the task list is cached per transcript version, so this stays light. To install without the timer: `STATUSLINE_REFRESH=0 bash install.sh`. The animation then only moves when Claude Code sends an update.

---

## Troubleshooting

**Nothing changed after install.**
Fully restart Claude Code or open a new session. Then check `~/.claude/settings.json` contains a `statusLine` entry pointing at `statusline-command.sh`.

**I see `statusline: bad JSON` or the line is blank.**
Run a manual test:
```bash
echo '{"model":{"display_name":"Claude Sonnet"},"context_window":{"remaining_percentage":59},"cwd":"."}' | bash ~/.claude/statusline-command.sh
```
If that prints rows, the kit is fine and Claude Code just needs a restart. If it prints an error, read the message; it is almost always Python missing from your PATH.

**`python3: command not found`.**
On Windows use `python`. On macOS or Linux install Python 3 (see [Before you start](#before-you-start)).

**Windows: nothing shows up.**
The wrapper needs `bash`. Install **Git for Windows**, make sure `bash --version` works in PowerShell, then reinstall.

**The animation is not moving.**
It only moves while Claude is active, and only about once a second. Send Claude a request and watch. Also confirm `"refreshInterval": 1` is in your `statusLine` settings (reinstall without `STATUSLINE_REFRESH=0` if not), and that `animate` is `true`.

**The spacing looks off or the emoji are squished.**
Emoji width varies by terminal. Try a modern terminal (Windows Terminal, iTerm2, VS Code's terminal). If one animation looks wrong in your terminal, choose another, or use `sprite custom` with a different emoji, and please open an issue with the terminal name.

**`gh: no remote` shows up.**
This folder has git but no GitHub remote yet. Add one with `git remote add origin <url>`.

**The PR never appears.**
Install the GitHub CLI and run `gh auth login`. Claude Code supplies PR info itself in many cases; the CLI is the fallback.

**`settings.json is not valid JSON. Left untouched.`**
The installer refuses to edit a settings file it cannot parse. Fix the JSON (a stray comma is the usual cause) and run it again.

**I want my old status line back.**
Restore `~/.claude/settings.json.bak`.

---

## Privacy and safety

- Everything runs **locally on your machine**. There is no telemetry and no account.
- It reads only what Claude Code hands it (model, context, cost, folder), the git state of your current folder, and your session transcript file to find the task list.
- The one place it can touch the network is the optional `gh pr view`, which asks GitHub about your own PR, and only when Claude Code did not supply it. Turn that off with `set use_gh false`.
- It writes only inside `~/.claude/`: your config, a small `.statusline-cache/` folder (cleaned automatically after two days), and `.bak` backups.
- Text that comes from outside, such as task titles, has terminal control characters stripped so it cannot mess with your terminal.

---

## Uninstall

1. Remove the `statusLine` key from `~/.claude/settings.json` (or restore `settings.json.bak`).
2. Delete these from `~/.claude/`: `statusline.py`, `statusline-command.sh`, `statusline.config.json`, `skills/statusline/` and `.statusline-cache/`.

---

## Roadmap

Today this kit works in **Claude Code**, because that is where the status line hook exists. Planned next: a shared core with small adapters so the same animations and heartbeat can run in other tools such as VS Code, Codex and Ollama. These are plans, not features yet.

---

Built on the [official Claude Code status line feature](https://code.claude.com/docs/en/statusline).

**Made by CleverForge.** Copyright © 2026 CleverForge. All rights reserved.
