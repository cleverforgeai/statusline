# ✨ Statusline

**Made by CleverForge** · [github.com/cleverforgeai/statusline](https://github.com/cleverforgeai/statusline)

> A live dashboard for the bottom of Claude Code: your project, how much memory Claude has left, a little animation that moves while Claude works (a butterfly, a car, a cat chasing a mouse...), your country flags, your mood, and a fun nudge when it is time to `/compact`. 🦋🇺🇸🚗

**You decide how much to show.** The line is short by default, and during setup Claude asks what you want. This is the *Full* layout, with everything switched on:

```
MyApp:feature | feat/login (+42 -7) | gh:acme/myapp ↑2 PR #31 approved | Sonnet 5.5 | ████░░░░░░ 41% | 82.0K tok/200K | $0.4100 | 18min
tasks ■■■□□□□□ 3/8 | ▶ Build login form [1/3 sub] › Wire up validation
🏢 Acme | 🇺🇸🇵🇷🇮🇹 | 🔥 shipping day | ········🦋······ | ♥ ▁█▃▁▃▁▁▁▂▁▁█ 59%
```

---

## Contents

1. [What is this?](#what-is-this)
2. [Pick how much you want to see](#pick-how-much-you-want-to-see)
3. [Before you start](#before-you-start)
4. [Install](#install)
5. [Setup: Claude asks, you answer](#setup-claude-asks-you-answer)
6. [How to read your status line](#how-to-read-your-status-line)
7. [Choose your pieces](#choose-your-pieces)
8. [Animations](#animations)
9. [Flags](#flags)
10. [Compact alerts](#compact-alerts)
11. [The heart line](#the-heart-line)
12. [Mood and organization](#mood-and-organization)
13. [Tasks and sub-tasks](#tasks-and-sub-tasks)
14. [Command cheat sheet](#command-cheat-sheet)
15. [Settings](#settings)
16. [Troubleshooting](#troubleshooting)
17. [Privacy and safety](#privacy-and-safety)
18. [Update and uninstall](#update-and-uninstall)
19. [Roadmap](#roadmap)

---

## What is this?

**Claude Code** is Anthropic's coding assistant that runs in your terminal. At the bottom of its window is a **status line**: text that Claude Code lets *you* control. By default it is plain. This kit fills it with useful, glanceable information and a bit of fun.

You do not need to be a programmer. If you can open a terminal and paste a command, you can install it, and after that **Claude walks you through the setup by asking questions**.

### Two words you will see a lot

- **Token**: a small chunk of text, roughly three quarters of a word. Everything you and Claude say is counted in tokens.
- **Context window**: how much of the conversation Claude can hold in mind at once. Think of it as a whiteboard. When it fills up, older things get squeezed out and Claude can lose track. The status line shows how full the whiteboard is, so you know when to tidy up with `/compact` (summarize and free space) or `/clear` (start fresh).

---

## Pick how much you want to see

Nobody needs everything on screen. There are three layouts, and you can add or remove single pieces on top of any of them.

### 🟢 Minimal: just the essentials

```
Sonnet 5.5 | ████░░░░░░ 41%
```

### 🔵 Standard: the default

Project, branch, model, memory bar, your tasks, and a fun row with your flags, mood, animation and heart line.

```
MyApp:feature | feat/login | Sonnet 5.5 | ████░░░░░░ 41%
tasks ■■■□□□□□ 3/8 | ▶ Build login form [1/3 sub] › Wire up validation
🇺🇸🇵🇷🇮🇹 | 🔥 shipping day | ········🦋······ | ♥ ▂▁▁█▃▁▃▁▁▁▂▁ 59%
```

### 🟣 Full: everything

GitHub repo, sync state and pull request, lines changed, tokens, cost, session time, and your organization.

```
MyApp:feature | feat/login (+42 -7) | gh:acme/myapp ↑2 PR #31 approved | Sonnet 5.5 | ████░░░░░░ 41% | 82.0K tok/200K | $0.4100 | 18min
tasks ■■■□□□□□ 3/8 | ▶ Build login form [1/3 sub] › Wire up validation
🏢 Acme | 🇺🇸🇵🇷🇮🇹 | 🔥 shipping day | ········🦋······ | ♥ ▁█▃▁▃▁▁▁▂▁▁█ 59%
```

> These previews use made-up project data (`MyApp`). Your real status line shows your real project, branch and tasks.

Want something in between? Choose **Pick my own** during setup, or add and remove single pieces later. See [Choose your pieces](#choose-your-pieces).

---

## Before you start

You need three things. Open a terminal and check:

```bash
claude --version     # Claude Code
python3 --version    # Python 3 (on Windows try: python --version)
git --version        # Git
```

If each prints a version number, you are ready. If one says "command not found":

| Missing | Get it |
|---|---|
| Claude Code | Follow the [official setup guide](https://code.claude.com/docs/en/overview) |
| Python 3 | [python.org/downloads](https://www.python.org/downloads/). On Windows, tick **Add Python to PATH** |
| Git | [git-scm.com](https://git-scm.com/downloads). **Windows users:** Git for Windows also provides the `bash` this kit uses |
| GitHub CLI (`gh`), optional | [cli.github.com](https://cli.github.com/). Only used to look up your pull request when Claude Code does not supply it. Run `gh auth login` once after installing |

> **Which terminal?** Any works: Terminal on macOS, Windows Terminal, iTerm2, the terminal inside VS Code. Modern terminals draw emoji and flags best.

---

## Install

Installing takes one command and a restart. Pick the route that fits you.

### Route A: one line (easiest)

macOS, Linux, or Git Bash on Windows:

```bash
curl -fsSL https://raw.githubusercontent.com/cleverforgeai/statusline/main/install.sh | bash
```

Windows PowerShell:

```powershell
irm https://raw.githubusercontent.com/cleverforgeai/statusline/main/install.ps1 | iex
```

You should see `Statusline Kit installed. Made by CleverForge.` Then **restart Claude Code** and continue with [Setup](#setup-claude-asks-you-answer).

> **Like to read a script before running it?** Good habit. Use Route B, or open [install.sh](install.sh) first. It is short.

### Route B: download it, then install

With git:

```bash
git clone https://github.com/cleverforgeai/statusline
cd statusline
```

No git? On the repo page click **Code → Download ZIP**, unzip it, and open a terminal inside the unzipped folder.

Then run the installer from that folder.

macOS, Linux, or Git Bash on Windows:

```bash
STATUSLINE_LOCAL="$PWD" bash install.sh
```

Windows PowerShell:

```powershell
$env:STATUSLINE_LOCAL = $PWD; .\install.ps1
```

Restart Claude Code, then continue with [Setup](#setup-claude-asks-you-answer).

### Using a fork?

Point the installer at your own copy: `STATUSLINE_REPO=yourname/statusline` before the one-liner. If your fork is private, also set `STATUSLINE_TOKEN` to a GitHub token that can read it.

### What the installer touches

It is deliberately gentle:

- Copies `statusline.py`, `statusline-command.sh` and the `/statusline` skill into your `~/.claude/` folder.
- Creates `~/.claude/statusline.config.json` **only if it does not exist yet**.
- Adds one entry (`statusLine`) to `~/.claude/settings.json`. **Your other settings are left alone.**
- Saves a `.bak` backup of anything it replaces. If you already had a different status line, the installer tells you what it replaced.

---

## Setup: Claude asks, you answer

After installing, open Claude Code and type:

```
/statusline
```

Claude asks a few quick questions (tap an answer, or choose *Other* to type your own). No files to edit.

| Claude asks | What you can answer |
|---|---|
| **How much do you want on your status line?** | Minimal, Standard (recommended), Full, or Pick my own |
| **What's your favorite animation?** | Any of the [24 animations](#animations) like 🦋 or 🚗 or 🐈, or type any emoji you like |
| **How are you feeling today?** | 😄 great, 😴 tired, 🔥 on fire, 🎯 focused, or your own |
| **Want fun "time to /compact" warnings?** | Yes or no |
| *If you chose Pick my own:* which pieces? | Tick what you want: branch changes, GitHub and PR, tasks, organization, tokens, cost, time, flags, mood, animation, heart |
| *If organization is on:* what name? | Type a name, or "use my GitHub name" |
| *If flags are on:* which countries? | Name up to 10, like "USA, Puerto Rico, Italy". Claude turns them into flags 🇺🇸🇵🇷🇮🇹 |

Then Claude applies your answers, **shows you your status line, and asks "Does this look right?"** If not, tell it what to change and it redoes only that part. When you say yes, setup is saved.

Until setup is confirmed, a small `🎬?` hint sits next to the animation as a reminder to run `/statusline`.

**Change your mind later?** Type `/statusline` again and pick what to change: what it shows, the animation, flags, mood, organization, or the alerts.

If you do not see the new status line, open a fresh Claude Code session.

---

## How to read your status line

Here is the Full layout, piece by piece. Your line will have fewer pieces depending on your layout.

```
MyApp:feature | feat/login (+42 -7) | gh:acme/myapp ↑2 PR #31 approved | Sonnet 5.5 | ████░░░░░░ 41% | 82.0K tok/200K | $0.4100 | 18min
tasks ■■■□□□□□ 3/8 | ▶ Build login form [1/3 sub] › Wire up validation
🏢 Acme | 🇺🇸🇵🇷🇮🇹 | 🔥 shipping day | ········🦋······ | ♥ ▁█▃▁▃▁▁▁▂▁▁█ 59%
```

### Row 1: where you are and how things look

| Piece | Meaning |
|---|---|
| `MyApp:feature` | Your project folder name, and a **phase** guessed from the git branch name (table below) |
| `feat/login (+42 -7)` | The git branch, with lines added (green) and removed (red) since your last commit. The `(+42 -7)` part is the `diff` piece |
| `gh:acme/myapp` | The GitHub repository this folder belongs to |
| `↑2` / `↓1` | Your branch is 2 commits ahead of / 1 behind GitHub. `synced` means equal. `no upstream` means this branch has not been pushed yet |
| `PR #31 approved` | Your open pull request and its review state (`approved`, `changes requested`, `draft`) |
| `Sonnet 5.5` | The Claude model in use |
| `████░░░░░░ 41%` | How full the context window is. 🟢 under 50%, 🟡 50 to 75%, 🔴 above 75% |
| `82.0K tok/200K` | Tokens used out of the model's maximum |
| `$0.4100` | Estimated cost of this session |
| `18min` | How long the session has run |

**Phases** come from the first letters of your branch name:

| Branch starts with | Phase | | Branch starts with | Phase |
|---|---|---|---|---|
| `main`, `master` | `prod` | | `refactor` | `refactor` |
| `feat` | `feature` | | `chore` | `chore` |
| `fix`, `bug` | `bugfix` | | `deploy` | `deploy` |
| `hotfix` | `hotfix` | | `test` | `testing` |
| `release` | `release` | | anything else | `dev` |

No git in the folder? You will see `init`, and the git pieces quietly disappear.

### Row 2: what Claude is working on

```
tasks ■■■□□□□□ 3/8 | ▶ Build login form [1/3 sub] › Wire up validation
```

Overall progress (3 of 8 done), the task in progress (▶), how many of its sub-steps are done, and the sub-step it is on now. No task list yet? The row does not appear.

### Row 3: the fun row

```
🏢 Acme | 🇺🇸🇵🇷🇮🇹 | 🔥 shipping day | ········🦋······ | ♥ ▁█▃▁▃▁▁▁▂▁▁█ 59%
```

Organization, [flags](#flags), [mood](#mood-and-organization), your [animation](#animations), and the [heart line](#the-heart-line).

### Row 4: only when memory runs low

```
🧳 Start packing: you'll need to /compact soon
```

See [Compact alerts](#compact-alerts).

---

## Choose your pieces

Every piece of the line can be switched on or off. The layouts are just starting points:

| Piece | What it shows | Minimal | Standard | Full |
|---|---|:-:|:-:|:-:|
| `app` | Project name and phase (MyApp:feature) | · | ✓ | ✓ |
| `branch` | Git branch | · | ✓ | ✓ |
| `diff` | Lines added and removed (+42 -7) | · | · | ✓ |
| `github` | GitHub repo, sync state and PR | · | · | ✓ |
| `model` | Claude model | ✓ | ✓ | ✓ |
| `context` | Memory bar (how full the context is) | ✓ | ✓ | ✓ |
| `tokens` | Token count | · | · | ✓ |
| `cost` | Session cost | · | · | ✓ |
| `time` | Session time | · | · | ✓ |
| `tasks` | Task list and progress | · | ✓ | ✓ |
| `org` | Organization name | · | · | ✓ |
| `flags` | Country flags | · | ✓ | ✓ |
| `mood` | Mood of the day | · | ✓ | ✓ |
| `animation` | Your animation | · | ✓ | ✓ |
| `heart` | Heart line (memory left) | · | ✓ | ✓ |
| `alerts` | Low-memory /compact warnings | ✓ | ✓ | ✓ |

**See what is on right now:**

```bash
python3 ~/.claude/statusline.py parts
```

**Switch a layout** (this resets any single-piece changes):

```bash
python3 ~/.claude/statusline.py preset minimal      # or: standard, full
```

**Add or remove single pieces:**

```bash
python3 ~/.claude/statusline.py parts on tokens cost
python3 ~/.claude/statusline.py parts off mood heart
```

**Preview a layout without saving it:**

```bash
python3 ~/.claude/statusline.py show full
```

(On Windows use `python` if `python3` is not found. Or just type `/statusline` and ask Claude to do it.)

---

## Animations

Your animation lives on the fun row. It **moves while something is happening** (tokens, cost or the session transcript changing) and **rests with 💤** after about 8 seconds of quiet. The butterfly flutters, the car cruises, the cat chases the mouse, the ball bounces.

Pick yours during setup, or any time with:

```bash
python3 ~/.claude/statusline.py sprite butterfly
```

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

**Use any emoji you like:**

```bash
python3 ~/.claude/statusline.py sprite custom 🐙
```

**See them all in your terminal:** `python3 ~/.claude/statusline.py preview` draws every animation, moving and resting.

**Good to know**

- Animations move about **once per second** at best. That is a Claude Code limit on how often it refreshes the status line, not a bug.
- A very long single answer can look idle until it finishes, because activity is detected from changes in tokens, cost and the transcript.
- When the heart flatlines, the animation turns into a 🪫 low battery.
- Some animations carry a chaser (the cat, the shark, the ghost behind Pac-Man). Pac-Man also eats the dots behind him.

---

## Flags

Show up to **10 country flags** on the fun row, for example `🇺🇸🇵🇷🇮🇹🇨🇴🇲🇽🇪🇸`. Handy if you work across countries or just want to rep yours.

During setup, Claude asks which countries and converts the names for you. Or set them yourself with 2-letter country codes:

```bash
python3 ~/.claude/statusline.py flags US PR IT CO MX ES
python3 ~/.claude/statusline.py flags clear
```

`EU` and `UN` work too. Give more than 10 and only the first 10 are used. On narrow terminals (under 90 columns) the line shows the first 5 plus `+n`.

> Some Windows terminals draw flag emoji as letters (a `US` instead of 🇺🇸). That is the terminal and its font, not the kit. Windows Terminal and the VS Code terminal handle them depending on version and font. If yours does not, run `flags clear`.

---

## Compact alerts

When Claude's memory (context) runs low, an extra row appears with a fun nudge that changes every few seconds. It disappears once you `/compact` or `/clear`.

| Memory left | Tone | Examples |
|---|---|---|
| 30% or less | 🟡 Friendly heads-up | `🧳 Start packing: you'll need to /compact soon` · `⏳ Memory is filling up... /compact soon` · `🧹 Tidy-up time is coming: /compact soon` |
| 15% or less | 🟠 Getting serious | `🚨 Almost full! Run /compact before the next big task` · `🫠 Brain getting heavy... /compact please` |
| 8% or less | 🔴 Blinking | `🆘 COMPACT NOW or Claude starts forgetting things!` · `🔔 FINAL CALL: /compact` |
| 3% or less | 💔 Flatline | `💔 Flatlined. /compact to revive, or /clear to start fresh` |

Preview any level without waiting: `python3 ~/.claude/statusline.py show low` (also `critical` and `dead`).

Turn it off: `python3 ~/.claude/statusline.py parts off alerts`

---

## The heart line

```
♥ ▁█▃▁▃▁▁▁▂▁▁█ 59%
```

An ECG heartbeat that **tracks how much context (memory) Claude has left**.

| Remaining | What you see | What it means |
|---|---|---|
| 50% or more | 🟢 Strong, regular beats | All good |
| 25 to 50% | 🟡 Beats get smaller (they start **skipping** under 30%) | Getting fuller |
| 8 to 25% | 🟠 Small beats, and under 12% only one in three | Time to `/compact` |
| 4 to 8% | 🔴 Faint, rare beats | Do it now |
| 3% or less | 🔴 **Flatline**, 💔, animation becomes 🪫 | Context is nearly gone |

**The heart comes back to life** after `/compact` or `/clear`, because context is freed up. Nothing is permanently lost.

If your plan reports a 5-hour usage limit, you can track that instead:

```bash
python3 ~/.claude/statusline.py set life_source '"five_hour"'
```

Use `'"lowest"'` to follow whichever is lower, and `'"context"'` to go back.

---

## Mood and organization

**Mood of the day.** Claude asks during setup. To change it any time, type `/statusline` or run:

```bash
python3 ~/.claude/statusline.py mood 😴 tired
```

It lasts one day. Tomorrow it shows `🙂?` until you pick again. To silence that reminder: `set mood_reminder false`.

**Organization.** Claude Code does not tell the status line your organization name, so the kit uses your GitHub owner by default, or the name you type. The `org` piece is on in the Full layout (turn it on in any layout with `parts on org`).

```bash
python3 ~/.claude/statusline.py org "My Team"
```

An empty name (`org ""`) goes back to the GitHub owner.

---

## Tasks and sub-tasks

When Claude keeps a to-do list, the `tasks` piece follows it by reading your session transcript. Claude Code tasks have no built-in parent/child link, so a task shows as a **sub-step** when its metadata has `parent` set to the parent task's id, or when it is named `Parent task > Sub task`. The `/statusline` skill tells Claude to use these forms.

---

## Command cheat sheet

Claude runs these for you when you use `/statusline`. You can also run them yourself in any terminal as `python3 ~/.claude/statusline.py <command>` (use `python` on Windows if needed).

| Command | What it does |
|---|---|
| `preset [minimal\|standard\|full]` | Choose a layout (no name lists them) |
| `parts` | Show every piece and whether it is on |
| `parts on <names>` / `parts off <names>` | Add or remove single pieces |
| `sprite` | List every animation |
| `sprite <name>` | Choose your animation |
| `sprite custom 🐙` | Use any emoji as your animation |
| `sprite random` | A different animation per session |
| `flags US PR IT` | Set up to 10 flags (`flags clear` removes them) |
| `mood 😄 great` | Set today's mood |
| `org "Name"` | Set the organization name |
| `show` | Show your line as it looks now (add `minimal`, `standard`, `full`, `low`, `critical` or `dead` to preview) |
| `confirm` | Mark setup as done (hides the `🎬?` hint) |
| `set <key> <json>` | Change any setting |
| `preview` | Draw every animation and heart level |
| `about` | Version and credits |

---

## Settings

Your settings live in `~/.claude/statusline.config.json`. Most are easier to change with the commands above. For the rest, use `set`:

```bash
python3 ~/.claude/statusline.py set active_seconds 15
```

| Setting | Default | What it does |
|---|---|---|
| `preset` | `standard` | Layout: `minimal`, `standard`, `full` |
| `parts` | `{}` | Single-piece overrides on top of the layout, e.g. `{"tokens": true}` |
| `sprite` | `car` | Animation name, `random`, or `custom` |
| `custom_emoji` | none | Emoji used when `sprite` is `custom` |
| `sprite_chosen`, `setup_done` | `false` | Set when you finish setup |
| `fav_reminder` | `true` | Show the `🎬?` hint until setup is done |
| `flags` | `[]` | Up to 10 country codes, e.g. `["US","PR"]` |
| `org` | blank | Organization name. Blank means your GitHub owner |
| `life_source` | `context` | What the heart tracks: `context`, `five_hour`, `lowest` |
| `active_seconds` | `8` | How long the animation keeps moving after the last change |
| `mood_reminder` | `true` | Show `🙂?` when no mood is set today |
| `two_lines` | `true` | Tasks on their own row (`false` squeezes them into row 1) |
| `use_gh` | `true` | Ask the `gh` tool for your PR when Claude Code does not provide it |
| `apps` | `{}` | Friendly names, e.g. `{"datahub": "DataHub"}` maps any folder containing "datahub" to "DataHub" |
| `show_memory`, `memory_file` | off | Show a section count from a notes file you point at |

**Refresh timer.** The installer sets `"refreshInterval": 1` so the animation moves even while Claude is quiet. Git results are cached for 3 seconds and the task list per transcript version, so this stays light. To install without the timer: `STATUSLINE_REFRESH=0 bash install.sh`. The animation then only moves when Claude Code sends an update.

---

## Troubleshooting

**I never got asked any questions.**
Open a new Claude Code session and type `/statusline`. That starts the question-and-answer setup.

**Nothing shows at the bottom.**
Fully restart Claude Code or open a new session. Then check `~/.claude/settings.json` has a `statusLine` entry pointing at `statusline-command.sh`.

**I see `statusline: bad JSON` or the line is blank.**
Run a manual test:

```bash
echo '{"model":{"display_name":"Claude Sonnet"},"context_window":{"remaining_percentage":59},"cwd":"."}' | bash ~/.claude/statusline-command.sh
```

If that prints rows, the kit is fine and Claude Code just needs a restart. If it prints an error, read the message. It is almost always Python missing from your PATH.

**`python3: command not found`.**
On Windows use `python`. On macOS or Linux install Python 3 (see [Before you start](#before-you-start)).

**Windows: nothing shows up.**
The wrapper needs `bash`. Install **Git for Windows**, check that `bash --version` works in PowerShell, then reinstall.

**The line is too long or too busy.**
Switch to a smaller layout: `preset minimal`, or turn off single pieces with `parts off tokens cost time`.

**The animation is not moving.**
It only moves while Claude is active, and about once a second. Send Claude a request and watch. Also confirm `"refreshInterval": 1` is in your `statusLine` settings (reinstall without `STATUSLINE_REFRESH=0` if not), and that `animation` is on (`parts`).

**Spacing looks off or emoji are squished.**
Emoji width varies by terminal. Try a modern terminal (Windows Terminal, iTerm2, VS Code's terminal). If one animation looks wrong, choose another, or use `sprite custom` with a different emoji, and open an issue with the terminal name.

**Flags show as letters like `US`.**
Your terminal cannot draw flag emoji. Run `flags clear`, or switch terminals.

**`gh: no remote` shows up.**
This folder has git but no GitHub remote yet: `git remote add origin <url>`.

**The PR never appears.**
The `github` piece must be on (Full layout, or `parts on github`). Install the GitHub CLI and run `gh auth login`. Claude Code supplies PR info itself in many cases; the CLI is the fallback.

**`settings.json is not valid JSON. Left untouched.`**
The installer refuses to edit a settings file it cannot parse. Fix the JSON (a stray comma is the usual cause) and run it again.

**I want my old status line back.**
Restore `~/.claude/settings.json.bak`.

---

## Privacy and safety

- Everything runs **locally on your machine**. There is no telemetry and no account.
- It reads only what Claude Code hands it (model, context, cost, folder), the git state of your current folder, and your session transcript file to find the task list.
- The one place it can touch the network is the optional `gh pr view`, which asks GitHub about your own PR, and only when the `github` piece is on and Claude Code did not supply the PR. Turn that off with `set use_gh false`.
- It writes only inside `~/.claude/`: your config, a small `.statusline-cache/` folder (cleaned automatically after two days), and `.bak` backups.
- Text that comes from outside, such as task titles, has terminal control characters stripped so it cannot mess with your terminal.

---

## Update and uninstall

**Update:** run the installer again. Your settings and config are kept, and your old scripts are saved as `.bak`.

```bash
curl -fsSL https://raw.githubusercontent.com/cleverforgeai/statusline/main/install.sh | bash
```

(Installed from a clone? `git pull`, then `STATUSLINE_LOCAL="$PWD" bash install.sh`.)

**Uninstall:**

1. Remove the `statusLine` key from `~/.claude/settings.json` (or restore `settings.json.bak`).
2. Delete these from `~/.claude/`: `statusline.py`, `statusline-command.sh`, `statusline.config.json`, `skills/statusline/` and `.statusline-cache/`.

---

## Roadmap

Today this kit works in **Claude Code**, because that is where the status line hook exists. Planned next: a shared core with small adapters so the same animations and heartbeat can run in other tools such as VS Code, Codex and Ollama. These are plans, not features yet.

---

Built on the [official Claude Code status line feature](https://code.claude.com/docs/en/statusline).

**Made by CleverForge.** Copyright © 2026 CleverForge. All rights reserved.
