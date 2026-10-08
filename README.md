# ✨ Statusline

**Made by CleverForge** · [github.com/cleverforgeai/statusline](https://github.com/cleverforgeai/statusline)

> Give Claude Code a live dashboard: your project, how much memory is left, a little animation that moves while Claude works, your country flags, and a fun nudge when it's time to `/compact`. 🚗💨

```
MyApp:feature | feat/login (+42 -7) | gh:acme/myapp ↑2 PR #31 approved | Sonnet 5.5 | ████░░░░░░ 41% | 82.0K tok/200K | $0.4120 | 18min
tasks ■■■□□□□□ 3/8 | ▶ Build login form [1/3 sub] › Wire up validation
🏢 Acme | 🇺🇸🇵🇷🇮🇹 | 🔥 shipping day | ··🦋············ | ♥ ▁▁█▃▁▃▁▁▁▂▁▁ 59%
```

And when memory runs low, a fourth row appears:

```
🧳 Start packing: you'll need to /compact soon
```

## Set it up in 2 minutes

**1. Install** (needs Claude Code, Python 3 and Git)

```bash
gh repo clone cleverforgeai/statusline
cd statusline
STATUSLINE_LOCAL="$PWD" bash install.sh
```

On Windows PowerShell, the last line is `$env:STATUSLINE_LOCAL = $PWD; .\install.ps1`.

**2. Open Claude Code and type `/statusline`**

**3. Answer Claude's questions.** That's the whole setup:

| Claude asks | You pick |
|---|---|
| What's your favorite animation? | One of 24 (🚗 🦋 🐈 🚀 ...) or any emoji you like |
| How are you feeling today? | 😄 😴 🔥 🎯 or your own |
| What's your organization name? | Your GitHub name, a name you type, or none |
| Want fun "time to /compact" warnings? | Yes or no |
| Which countries' flags? | Up to 10, like "USA, Puerto Rico, Italy" |

Claude applies your answers, **shows you your status line, and asks you to confirm.** Not right? Say what to change and it redoes just that part.

## Later

Type `/statusline` again any time to change something. The animation moves while Claude is working and rests with 💤 when it is idle. The heart line fades as memory runs low and comes back after `/compact` or `/clear`.

## Something wrong?

- **Nothing at the bottom?** Open a new Claude Code session.
- **Windows?** You need Git for Windows (it provides `bash`). Use `python` instead of `python3` if needed.
- **Flags show as letters like `US`?** Your terminal can't draw flag emoji. Ask Claude to clear the flags.
- More help: [docs/REFERENCE.md](docs/REFERENCE.md) has every setting, command and a longer troubleshooting list.

## Privacy

Runs entirely on your machine. No telemetry, no account. It writes only inside `~/.claude/`. Remove it by deleting the `statusLine` entry from `~/.claude/settings.json`.

---

Built on the [official Claude Code status line feature](https://code.claude.com/docs/en/statusline).
**Made by CleverForge.** Copyright © 2026 CleverForge. All rights reserved.
