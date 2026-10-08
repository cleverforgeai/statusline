#!/usr/bin/env python3
"""Claude Code status line.

Made by CleverForge (github.com/CleverForgeAI). Copyright (c) 2026 CleverForge.
github.com/cleverforgeai/statusline

Line 1: App:phase | branch | GitHub repo, sync, PR | model | context bar | tokens | cost | time
Line 2: task and subtask progress (from the session transcript)
Line 3: organization | mood of the day | animated sprite | heart-line life meter

The sprite moves while the session is active (tokens, cost or transcript changing)
and rests when idle. The heart line is an ECG that weakens as context runs out and
flatlines at the end. Set "refreshInterval": 1 on the statusLine setting to animate.

Config: ~/.claude/statusline.config.json   (see README)
CLI:    python statusline.py mood|sprite|org|set|preview ...
"""
import sys, json, subprocess, os, re, datetime, time, hashlib, math

__author__ = 'CleverForge'
__org__ = 'CleverForgeAI'
__version__ = '1.3.0'
__repo__ = 'github.com/cleverforgeai/statusline'
__made_by__ = 'Made by CleverForge'

R = '\033[0m'; BOLD = '\033[1m'; DIM = '\033[2m'
CYAN = '\033[96m'; YELLOW = '\033[93m'; GREEN = '\033[92m'; MAGENTA = '\033[95m'
BLUE = '\033[94m'; RED = '\033[91m'; WHITE = '\033[97m'; ORANGE = '\033[33m'

CLAUDE_DIR = os.path.expanduser('~/.claude')
CFG_PATH = os.path.join(CLAUDE_DIR, 'statusline.config.json')
CACHE_DIR = os.path.join(CLAUDE_DIR, '.statusline-cache')

MOODS = [('😄', 'great'), ('🙂', 'good'), ('😐', 'meh'), ('😴', 'tired'), ('🤯', 'overloaded'),
         ('😤', 'frustrated'), ('🔥', 'on fire'), ('🎯', 'focused'), ('🥳', 'celebrating')]

# Each sprite: frames (cycled while active), fill (ground characters), step (cells per tick,
# fractions are slow), path (line | flutter | bounce), optional extras:
#   roll   ground shifts with position so it looks like it rolls or flows
#   follow a second glyph chasing the main one
#   eat    ground behind the sprite is wiped (Pac-Man)
WAVE = ['~', '~', '-']
SPRITES = {
    'car':       {'frames': ['🚗'],       'fill': ['─'],      'step': 2,   'path': 'line',    'desc': 'Cruises down the road'},
    'butterfly': {'frames': ['🦋'],       'fill': ['·'],      'step': 1,   'path': 'flutter', 'desc': 'Flutters up and down'},
    'can':       {'frames': ['🥫'],       'fill': ['_', '‾'], 'step': 1,   'path': 'line',    'desc': 'Rolls over bumpy ground', 'roll': True},
    'walker':    {'frames': ['🚶', '🏃'], 'fill': ['·'],      'step': 1,   'path': 'line',    'desc': 'Walks, then jogs'},
    'rocket':    {'frames': ['🚀'],       'fill': ['·'],      'step': 2,   'path': 'line',    'desc': 'Blasts across the sky'},
    'cat':       {'frames': ['🐁'],       'fill': ['·'],      'step': 1,   'path': 'line',    'desc': 'A cat chases a mouse', 'follow': '🐈'},
    'shark':     {'frames': ['🐟'],       'fill': WAVE,       'step': 1,   'path': 'line',    'desc': 'A shark chases a fish through the waves', 'follow': '🦈', 'roll': True},
    'pacman':    {'frames': ['🟡'],       'fill': ['·'],      'step': 1,   'path': 'line',    'desc': 'Munches dots with a ghost behind', 'follow': '👻', 'eat': True},
    'dog':       {'frames': ['🐕'],       'fill': ['·'],      'step': 2,   'path': 'line',    'desc': 'Runs and runs'},
    'horse':     {'frames': ['🏇'],       'fill': ['·'],      'step': 2,   'path': 'line',    'desc': 'Gallops along'},
    'bike':      {'frames': ['🚲'],       'fill': ['─'],      'step': 2,   'path': 'line',    'desc': 'Pedals down the path'},
    'train':     {'frames': ['🚂'],       'fill': ['=', '=', '-'], 'step': 2, 'path': 'line',  'desc': 'Chugs along the tracks'},
    'plane':     {'frames': ['🛫'],       'fill': ['·'],      'step': 2,   'path': 'line',    'desc': 'Takes off and keeps flying'},
    'sailboat':  {'frames': ['⛵'],       'fill': WAVE,       'step': 1,   'path': 'line',    'desc': 'Sails over rolling waves', 'roll': True},
    'snail':     {'frames': ['🐌'],       'fill': ['·'],      'step': 0.5, 'path': 'line',    'desc': 'Slow and steady'},
    'turtle':    {'frames': ['🐢'],       'fill': ['·'],      'step': 0.5, 'path': 'line',    'desc': 'Takes its time'},
    'fish':      {'frames': ['🐠'],       'fill': WAVE,       'step': 1,   'path': 'flutter', 'desc': 'Swims through the water', 'roll': True},
    'bee':       {'frames': ['🐝'],       'fill': ['·'],      'step': 1,   'path': 'flutter', 'desc': 'Buzzes around'},
    'ghost':     {'frames': ['👻'],       'fill': ['·'],      'step': 1,   'path': 'flutter', 'desc': 'Floats and drifts'},
    'ufo':       {'frames': ['🛸'],       'fill': ['·'],      'step': 1,   'path': 'flutter', 'desc': 'Hovers and zips about'},
    'snake':     {'frames': ['🐍'],       'fill': ['·'],      'step': 1,   'path': 'flutter', 'desc': 'Slithers side to side'},
    'ball':      {'frames': ['⚽'],       'fill': ['─'],      'step': 1,   'path': 'bounce',  'desc': 'Bounces back and forth'},
    'dancer':    {'frames': ['💃', '🕺'], 'fill': ['·', '*'], 'step': 1,   'path': 'line',    'desc': 'Dances along, swapping moves', 'roll': True},
}
# Anything else: `sprite custom <emoji>` uses your own emoji as the sprite.
CUSTOM_FILL = ['·']


# ---------------------------------------------------------------- flags
ISO = set(('AD AE AF AG AI AL AM AO AQ AR AS AT AU AW AX AZ BA BB BD BE BF BG BH BI BJ BL BM BN BO BQ BR BS BT BV BW BY BZ '
           'CA CC CD CF CG CH CI CK CL CM CN CO CR CU CV CW CX CY CZ DE DJ DK DM DO DZ EC EE EG EH ER ES ET FI FJ FK FM FO FR '
           'GA GB GD GE GF GG GH GI GL GM GN GP GQ GR GS GT GU GW GY HK HM HN HR HT HU ID IE IL IM IN IO IQ IR IS IT JE JM JO JP '
           'KE KG KH KI KM KN KP KR KW KY KZ LA LB LC LI LK LR LS LT LU LV LY MA MC MD ME MF MG MH MK ML MM MN MO MP MQ MR MS MT '
           'MU MV MW MX MY MZ NA NC NE NF NG NI NL NO NP NR NU NZ OM PA PE PF PG PH PK PL PM PN PR PS PT PW PY QA RE RO RS RU RW '
           'SA SB SC SD SE SG SH SI SJ SK SL SM SN SO SR SS ST SV SX SY SZ TC TD TF TG TH TJ TK TL TM TN TO TR TT TV TW TZ UA UG '
           'UM US UY UZ VA VC VE VG VI VN VU WF WS XK YE YT ZA ZM ZW EU UN').split())
MAX_FLAGS = 10


def flag(code):
    return ''.join(chr(0x1F1E6 + ord(ch) - 65) for ch in code)


def flags_segment(cfg, narrow):
    codes = [str(x).upper() for x in (cfg.get('flags') or []) if str(x).upper() in ISO][:MAX_FLAGS]
    if not codes:
        return ''
    cap = 5 if narrow else MAX_FLAGS
    shown = ''.join(flag(x) for x in codes[:cap])
    more = len(codes) - cap
    return shown + (c(DIM + WHITE, f' +{more}') if more > 0 else '')


# ---------------------------------------------------------------- compact alerts
ALERTS = {
    'warn': ["🧳 Start packing: you'll need to /compact soon",
             '⏳ Memory is filling up... /compact soon',
             '🧹 Tidy-up time is coming: /compact soon',
             '🍿 Fun fact: a /compact is on the horizon'],
    'urgent': ['🚨 Almost full! Run /compact before the next big task',
               '🫠 Brain getting heavy... /compact please',
               '🎒 The bag is nearly full: time to /compact'],
    'critical': ['🆘 COMPACT NOW or Claude starts forgetting things!',
                 '💥 Memory almost gone: /compact or /clear, right now',
                 '🔔 FINAL CALL: /compact'],
    'dead': ['💔 Flatlined. /compact to revive, or /clear to start fresh'],
}


def alert_line(rem, now, sid):
    """Fun nudge when context is running low. Rotates its message every few seconds."""
    if rem is None or rem > 30:
        return ''
    level = 'dead' if rem <= 3 else 'critical' if rem <= 8 else 'urgent' if rem <= 15 else 'warn'
    msgs = ALERTS[level]
    seed = int(md5(sid).hexdigest(), 16) % 97
    msg = msgs[(int(now // 8) + seed) % len(msgs)]
    if level == 'warn':
        col = YELLOW
    elif level == 'urgent':
        col = ORANGE + BOLD
    elif level == 'critical':
        col = (RED + BOLD) if int(now) % 2 == 0 else (DIM + RED)   # blinks
    else:
        col = DIM + RED
    return c(col, msg)


def get_sprite(name, cfg):
    if name == 'custom':
        emo = (cfg.get('custom_emoji') or '⭐').strip()
        return {'frames': [emo], 'fill': CUSTOM_FILL, 'step': 1, 'path': 'line', 'desc': 'Your own emoji'}
    return SPRITES.get(name) or SPRITES['car']


def c(color, text):
    return f'{color}{text}{R}'


_CTRL = re.compile(r'[\x00-\x08\x0b-\x1f\x7f-\x9f]')


def clean(s):
    """Strip control and escape characters from text we did not write (task names, config).
    Stops a hostile task title or repo name from injecting terminal escape sequences."""
    return _CTRL.sub('', str(s))


def md5(text):
    try:
        return hashlib.md5(text.encode(), usedforsecurity=False)
    except TypeError:
        return hashlib.md5(text.encode())


def load_config():
    try:
        with open(CFG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def save_config(cfg):
    os.makedirs(CLAUDE_DIR, exist_ok=True)
    with open(CFG_PATH, 'w', encoding='utf-8') as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)


def cached(key, ttl, fn):
    """Tiny file cache so slow calls do not run on every redraw."""
    try:
        os.makedirs(CACHE_DIR, exist_ok=True)
    except Exception:
        return fn() or ''
    path = os.path.join(CACHE_DIR, md5(key).hexdigest())
    try:
        if time.time() - os.path.getmtime(path) < ttl:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
    except Exception:
        pass
    val = fn() or ''
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(val)
    except Exception:
        pass
    return val


def cleanup_cache():
    try:
        cutoff = time.time() - 2 * 86400
        for n in os.listdir(CACHE_DIR):
            p = os.path.join(CACHE_DIR, n)
            if os.path.getmtime(p) < cutoff:
                os.remove(p)
    except Exception:
        pass


# ---------------------------------------------------------------- what to show
PARTS = ['app', 'branch', 'diff', 'github', 'model', 'context', 'tokens', 'cost', 'time',
         'tasks', 'org', 'flags', 'mood', 'animation', 'heart', 'alerts']
PART_DESC = {
    'app': 'Project name and phase (MyApp:feature)', 'branch': 'Git branch',
    'diff': 'Lines added and removed (+42 -7)', 'github': 'GitHub repo, sync state and PR',
    'model': 'Claude model', 'context': 'Memory bar (how full the context is)',
    'tokens': 'Token count', 'cost': 'Session cost', 'time': 'Session time',
    'tasks': 'Task list and progress', 'org': 'Organization name', 'flags': 'Country flags',
    'mood': 'Mood of the day', 'animation': 'Your animation', 'heart': 'Heart line (memory left)',
    'alerts': 'Low-memory /compact warnings',
}
PRESETS = {
    'minimal':  {'model', 'context', 'alerts'},
    'standard': {'app', 'branch', 'model', 'context', 'tasks', 'flags', 'mood', 'animation', 'heart', 'alerts'},
    'full':     set(PARTS),
}
PRESET_DESC = {
    'minimal': 'Just the model and the memory bar',
    'standard': 'Project, branch, model, memory bar, tasks, and the fun row (default)',
    'full': 'Everything: GitHub and PR, tokens, cost, time, organization and more',
}
LEGACY = {'github': 'show_github', 'tasks': 'show_tasks', 'org': 'show_org', 'mood': 'show_mood',
          'flags': 'show_flags', 'alerts': 'compact_alert'}


def part_on(cfg, name):
    """Is this piece of the status line switched on? Preset first, then per-piece overrides."""
    over = cfg.get('parts') or {}
    base = PRESETS.get(cfg.get('preset', 'standard'), PRESETS['standard'])
    on = bool(over[name]) if name in over else (name in base)
    if on and LEGACY.get(name) and cfg.get(LEGACY[name]) is False:
        on = False
    if on and name in ('org', 'flags', 'mood', 'animation', 'heart') and cfg.get('fun_line') is False:
        on = False
    if on and name in ('animation', 'heart') and cfg.get('animate') is False:
        on = False
    return on


# ---------------------------------------------------------------- fun line pieces
BEAT = [0, 0, 1, 0, 0, 7, 2, 0, 2, 0]   # P wave, QRS spike, T wave
LEVELS = '▁▂▃▄▅▆▇█'


def life_color(health):
    return GREEN if health >= 50 else (YELLOW if health >= 25 else (ORANGE if health >= 8 else RED))


def ecg_line(health, width, t):
    """Heartbeat trace. Spikes shrink as health drops, beats start to skip, then it flatlines."""
    if health <= 3:
        return c(DIM + RED, '▁' * width)
    amp = min(1.0, health / 60.0)
    p = len(BEAT)
    out = []
    for i in range(width):
        k = t + i
        beat, ph = divmod(k, p)
        h = BEAT[ph]
        if health < 30 and beat % 3 == 2:
            h = 0
        if health < 12 and beat % 3 != 0:
            h = 0
        out.append(LEVELS[min(7, int(round(h * amp)))])
    return c(life_color(health), ''.join(out))


def heart_segment(health, width, t):
    if health <= 3:
        return '💔 ' + ecg_line(health, width, t) + ' ' + c(DIM + RED, 'flatline')
    col = life_color(health)
    return c(col, '♥') + ' ' + ecg_line(health, width, t) + ' ' + c(col + BOLD, f'{round(health)}%')


def sprite_x(sp, pos, span):
    ip = int(pos)
    if sp['path'] == 'flutter':
        return int((pos * 0.8 + 2 * math.sin(pos * 0.9)) % span)
    if sp['path'] == 'bounce':
        period = max(1, 2 * (span - 1))
        k = ip % period
        return k if k < span else period - k
    return ip % span


def track_segment(name, pos, width, active, dead, cfg=None):
    sp = get_sprite(name, cfg or {})
    span = width - 2          # emoji is two columns wide
    x = sprite_x(sp, pos, span)
    ip = int(pos)
    fill, frames = sp['fill'], sp['frames']

    def ground(i):
        return fill[(i + (ip if sp.get('roll') else 0)) % len(fill)]

    glyph = '🪫' if dead else (frames[ip % len(frames)] if active else frames[0])
    cells = [(ground(i), False) for i in range(width)]
    if sp.get('eat'):
        for i in range(x):
            cells[i] = (' ', False)
    fol = sp.get('follow')
    if fol and not dead and x - 3 >= 0 and sp['path'] != 'bounce':
        cells[x - 3] = (fol, True)
        cells[x - 2] = ('', True)
    cells[x] = (glyph, True)
    cells[x + 1] = ('', True)

    out, buf = '', ''
    for text, is_glyph in cells:
        if is_glyph:
            if buf:
                out += c(DIM + WHITE, buf); buf = ''
            out += text
        else:
            buf += text
    if buf:
        out += c(DIM + WHITE, buf)
    tail = '' if active or dead else ' ' + c(DIM, '💤')
    return out + tail


def mood_segment(cfg):
    m = cfg.get('mood') or {}
    today = datetime.date.today().isoformat()
    if m.get('emoji') and m.get('date') == today:
        return clean(m['emoji']) + (' ' + c(DIM + WHITE, clean(m['label'])) if m.get('label') else '')
    return c(DIM + WHITE, '🙂?') if cfg.get('mood_reminder', True) else ''


def pick_sprite(cfg, sid):
    name = cfg.get('sprite', 'car')
    if name == 'random':
        names = sorted(SPRITES)
        return names[int(md5(sid).hexdigest(), 16) % len(names)]
    if name == 'custom' and (cfg.get('custom_emoji') or '').strip():
        return 'custom'
    return name if name in SPRITES else 'car'


# ---------------------------------------------------------------- CLI
def cli(argv):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    cfg = load_config()
    cmd = argv[1]
    today = datetime.date.today().isoformat()
    if cmd == 'mood':
        if len(argv) < 3:
            print('Moods: ' + '  '.join(f'{e} {l}' for e, l in MOODS))
            print('Usage: statusline.py mood <emoji> [label]')
            return 0
        cfg['mood'] = {'emoji': argv[2], 'label': ' '.join(argv[3:]), 'date': today}
        print(f"Mood set for {today}: {argv[2]} {' '.join(argv[3:])}")
    elif cmd == 'sprite':
        opts = sorted(SPRITES) + ['random', 'custom']
        if len(argv) < 3:
            print('Pick your favorite animation: statusline.py sprite <name>\n')
            for n in sorted(SPRITES):
                print(f"  {n.ljust(10)} {SPRITES[n]['frames'][0]}  {SPRITES[n]['desc']}")
            print(f"  {'random'.ljust(10)} 🎲  A different one for each session")
            print(f"  {'custom'.ljust(10)} ✨  Your own emoji: statusline.py sprite custom 🐙")
            print(f"\nCurrent: {cfg.get('sprite', 'car')}" + (f" {cfg.get('custom_emoji', '')}" if cfg.get('sprite') == 'custom' else ''))
            return 0
        if argv[2] == 'custom':
            emo = clean(' '.join(argv[3:])).strip()
            if not emo or len(emo) > 8:
                print('Usage: statusline.py sprite custom <one emoji>')
                return 1
            cfg['sprite'], cfg['custom_emoji'] = 'custom', emo
            cfg['sprite_chosen'] = True
            print(f'Sprite set to your own emoji: {emo}')
        elif argv[2] in opts:
            cfg['sprite'] = argv[2]
            cfg['sprite_chosen'] = True
            print(f'Sprite set to {argv[2]}')
        else:
            print('Unknown sprite. Run: statusline.py sprite   (shows the full list)')
            return 1
    elif cmd == 'preset':
        if len(argv) < 3 or argv[2] not in PRESETS:
            print('Presets (pick how much you want on the line):')
            for n in ('minimal', 'standard', 'full'):
                print(f'  {n.ljust(9)} {PRESET_DESC[n]}')
            print(f"\nCurrent: {cfg.get('preset', 'standard')}")
            return 0 if len(argv) < 3 else 1
        cfg['preset'], cfg['parts'] = argv[2], {}
        print(f"Preset set to {argv[2]}: " + ', '.join(n for n in PARTS if n in PRESETS[argv[2]]))
    elif cmd == 'parts':
        if len(argv) < 3:
            print(f"Preset: {cfg.get('preset', 'standard')}   (change a piece: statusline.py parts on|off <name> ...)\n")
            for n in PARTS:
                print(f"  {'✓' if part_on(cfg, n) else '·'} {n.ljust(10)} {PART_DESC[n]}")
            return 0
        if argv[2] not in ('on', 'off') or len(argv) < 4:
            print('Usage: statusline.py parts on|off <name> [name ...]   (run `parts` to see names)')
            return 1
        names = [x.lower() for a in argv[3:] for x in re.split(r'[,\s]+', a) if x]
        bad = [n for n in names if n not in PARTS]
        if bad:
            print('Unknown piece: ' + ', '.join(bad) + '\nValid: ' + ', '.join(PARTS))
            return 1
        over = cfg.get('parts') or {}
        for n in names:
            over[n] = (argv[2] == 'on')
            if argv[2] == 'on' and LEGACY.get(n):
                cfg.pop(LEGACY[n], None)          # clear an old off-switch so the new one wins
        cfg['parts'] = over
        print(f"{argv[2].upper()}: " + ', '.join(names))
    elif cmd == 'flags':
        if len(argv) < 3:
            cur = [x for x in (cfg.get('flags') or []) if x in ISO]
            print('Flags: ' + (''.join(flag(x) for x in cur) + '  ' + ' '.join(cur) if cur else '(none)'))
            print(f'Usage: statusline.py flags US PR IT     (2-letter country codes, up to {MAX_FLAGS})')
            print('       statusline.py flags clear')
            return 0
        if argv[2].lower() in ('clear', 'none', 'off'):
            cfg['flags'] = []
            print('Flags cleared')
        else:
            codes = [x.upper() for a in argv[2:] for x in re.split(r'[,\s]+', a) if x]
            bad = [x for x in codes if x not in ISO]
            if bad:
                print('Not a valid 2-letter country code: ' + ', '.join(bad))
                return 1
            seen = []
            for x in codes:
                if x not in seen:
                    seen.append(x)
            cfg['flags'] = seen[:MAX_FLAGS]
            cfg['show_flags'] = True
            print('Flags set: ' + ''.join(flag(x) for x in cfg['flags']) + '  ' + ' '.join(cfg['flags']))
            if len(seen) > MAX_FLAGS:
                print(f'Only the first {MAX_FLAGS} are used. Skipped: ' + ' '.join(seen[MAX_FLAGS:]))
    elif cmd == 'show':
        level = next((a for a in argv[2:] if a in ('low', 'warn', 'critical', 'dead')), '')
        rem_v = {'low': 12, 'warn': 25, 'critical': 6, 'dead': 2}.get(level, 59)
        pre = next((a for a in argv[2:] if a in PRESETS), '')
        sample = {'session_id': 'preview', 'model': {'display_name': 'Claude Sonnet 5.5'},
                  'context_window': {'used_percentage': 100 - rem_v, 'remaining_percentage': rem_v,
                                     'total_input_tokens': (100 - rem_v) * 2000 - 2000, 'total_output_tokens': 2000,
                                     'context_window_size': 200000},
                  'cost': {'total_cost_usd': 0.41, 'total_duration_ms': 1080000}, 'cwd': '/MyApp',
                  'pr': {'number': 31, 'review_state': 'approved'}}
        env = dict(os.environ, COLUMNS='120', PYTHONUTF8='1', STATUSLINE_SAMPLE='1')
        if pre:
            env['STATUSLINE_PRESET'] = pre
        r = subprocess.run([sys.executable, os.path.abspath(__file__)], input=json.dumps(sample),
                           capture_output=True, text=True, encoding='utf-8', env=env)
        out = r.stdout if '--color' in argv else re.sub(r'\x1b\[[0-9;]*m', '', r.stdout)
        print(out if out.strip() else (r.stderr or 'No output'))
        return 0
    elif cmd == 'confirm':
        cfg['setup_done'] = True
        cfg['sprite_chosen'] = True
        print('Setup confirmed. Your status line is ready.')
    elif cmd == 'org':
        cfg['org'] = ' '.join(argv[2:])
        print(f"Organization set to {cfg['org'] or '(auto from GitHub owner)'}")
    elif cmd == 'set' and len(argv) >= 4:
        try:
            val = json.loads(argv[3])
        except Exception:
            val = argv[3]
        cfg[argv[2]] = val
        print(f'{argv[2]} = {val!r}')
    elif cmd in ('about', 'version', '--version'):
        print(f'Statusline Kit v{__version__}')
        print(f'{__made_by__} - {__repo__}')
        return 0
    elif cmd == 'preview':
        w_t, w_e = 16, 12
        for name in sorted(SPRITES):
            print(name.ljust(10) + track_segment(name, 7, w_t, True, False) + '   ' +
                  track_segment(name, 7, w_t, False, False))
        print()
        for h in (100, 70, 45, 25, 10, 2):
            print(f'life {h:>3}%  ' + heart_segment(h, w_e, 3))
        print('\nMoods: ' + '  '.join(f'{e} {l}' for e, l in MOODS))
        print(f'\n{__made_by__} v{__version__}')
        return 0
    else:
        print('Commands: preset [name] | parts [on|off names] | sprite [name] | flags [codes] | mood [emoji label] | org [name] | show [preset|low] | confirm | set <key> <json> | preview | about')
        return 1
    save_config(cfg)
    return 0


if len(sys.argv) > 1:
    try:
        sys.exit(cli(sys.argv))
    except BrokenPipeError:
        sys.exit(0)

# ---------------------------------------------------------------- main
CFG = load_config()
if os.environ.get('STATUSLINE_PRESET') in PRESETS:     # used by `show <preset>` to preview without saving
    CFG['preset'], CFG['parts'] = os.environ['STATUSLINE_PRESET'], {}
SAMPLE = os.environ.get('STATUSLINE_SAMPLE') == '1'     # `show` uses a made-up project so every piece can appear

try:
    d = json.load(sys.stdin)
except Exception:
    print('statusline: bad JSON', end='')
    sys.exit(0)

if int(time.time()) % 50 == 0:
    cleanup_cache()

ws = d.get('workspace') or {}
cwd = (ws.get('current_dir') or d.get('cwd') or '').replace('\\', '/')
sid = re.sub(r'[^A-Za-z0-9_-]', '', str(d.get('session_id') or 'nosession'))[:64] or 'nosession'
try:
    cols = int(os.environ.get('COLUMNS', '120'))
except ValueError:
    cols = 120

model_d = d.get('model') or {}
model = clean(re.sub(r'^Claude\s+', '', model_d.get('display_name') or model_d.get('id') or 'unknown'))

ctx_d = d.get('context_window') or {}
pct = ctx_d.get('used_percentage')
rem = ctx_d.get('remaining_percentage')
if rem is None and pct is not None:
    rem = 100 - pct
t_in, t_out = ctx_d.get('total_input_tokens'), ctx_d.get('total_output_tokens')
used_tok = (t_in or 0) + (t_out or 0) if (t_in is not None or t_out is not None) else None
max_tok = ctx_d.get('context_window_size')

cost_raw = d.get('cost') if isinstance(d.get('cost'), dict) else {}
cost_val = cost_raw.get('total_cost_usd')
sess_mins = round(cost_raw['total_duration_ms'] / 60000) if cost_raw.get('total_duration_ms') else None


def git(*args, timeout=2):
    try:
        r = subprocess.run(['git', '-C', cwd, '-c', 'core.fsmonitor=false', *args],
                           capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip() if r.returncode == 0 else None
    except Exception:
        return None


def parse_remote(url):
    if not url:
        return None
    m = re.match(r'^(?:git@|ssh://git@|https?://(?:[^@/]+@)?)([^:/]+)[:/]([^/]+)/(.+?)(?:\.git)?/?$', url)
    return m.groups() if m else None


def git_info():
    info = {'has_git': False}
    if not cwd or git('rev-parse', '--git-dir') is None:
        return json.dumps(info)
    info['has_git'] = True
    branch = git('rev-parse', '--abbrev-ref', 'HEAD') or git('rev-parse', '--short', 'HEAD') or ''
    info['branch'] = branch
    info['top'] = git('rev-parse', '--show-toplevel') or ''
    added = removed = 0
    for line in (git('diff', '--numstat', 'HEAD', timeout=3) or '').splitlines():
        p = line.split('\t')
        if len(p) >= 2:
            added += int(p[0]) if p[0].isdigit() else 0
            removed += int(p[1]) if p[1].isdigit() else 0
    info['added'], info['removed'] = added, removed
    rem_ = parse_remote(git('remote', 'get-url', 'origin'))
    if rem_:
        info['host'], info['owner'], info['name'] = rem_
    up = git('rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{u}')
    info['upstream'] = up
    if up:
        counts = git('rev-list', '--left-right', '--count', f'HEAD...{up}')
        if counts:
            a, b = (counts.split() + ['0', '0'])[:2]
            info['ahead'], info['behind'] = int(a), int(b)
    return json.dumps(info)


gi = {'has_git': False}
if cwd:
    try:
        gi = json.loads(cached('git:' + cwd, 3, git_info) or '{}') or gi
    except Exception:
        pass

if SAMPLE:
    gi = {'has_git': True, 'branch': 'feat/login', 'top': '/MyApp', 'added': 42, 'removed': 7,
          'upstream': 'origin/feat/login', 'ahead': 2, 'behind': 0,
          'host': 'github.com', 'owner': 'acme', 'name': 'myapp'}
SAMPLE_TASKS = (
    [{'id': str(i), 'subject': f'Task {i}', 'status': 'completed', 'parent': None} for i in (1, 2, 3)] +
    [{'id': '4', 'subject': 'Build login form', 'status': 'in_progress', 'parent': None},
     {'id': '41', 'subject': 'Layout', 'status': 'completed', 'parent': '4'},
     {'id': '42', 'subject': 'Wire up validation', 'status': 'in_progress', 'parent': '4'},
     {'id': '43', 'subject': 'Add tests', 'status': 'pending', 'parent': '4'}] +
    [{'id': str(i), 'subject': f'Task {i}', 'status': 'pending', 'parent': None} for i in (5, 6, 7, 8)])

# ---------- App name and phase
cwd_lower = cwd.lower()
folder = os.path.basename(cwd.rstrip('/')) if cwd else ''
app = None
for key, name in (CFG.get('apps') or {}).items():
    if key.lower() in cwd_lower:
        app = name
        break
if not app:
    app = os.path.basename(gi.get('top') or '') or folder or 'Root'
app = clean(app)

branch = clean(gi.get('branch') or '')
added, removed = gi.get('added', 0), gi.get('removed', 0)
if branch:
    bl = branch.lower()
    if bl in ('main', 'master'): phase, pcol = 'prod', GREEN
    elif bl.startswith('feat'): phase, pcol = 'feature', CYAN
    elif bl.startswith(('fix', 'bug')): phase, pcol = 'bugfix', ORANGE
    elif bl.startswith('hotfix'): phase, pcol = 'hotfix', RED
    elif bl.startswith('release'): phase, pcol = 'release', MAGENTA
    elif bl.startswith('refactor'): phase, pcol = 'refactor', BLUE
    elif bl.startswith('chore'): phase, pcol = 'chore', DIM + WHITE
    elif bl.startswith('deploy'): phase, pcol = 'deploy', GREEN
    elif bl.startswith('test'): phase, pcol = 'testing', YELLOW
    else: phase, pcol = 'dev', CYAN
else:
    phase, pcol = 'init', DIM + WHITE
phase_str = c(pcol + BOLD, f'{app}:{phase}')

branch_str = ''
if branch:
    branch_str = c(YELLOW + BOLD, branch)
    if (added or removed) and part_on(CFG, 'diff'):
        parts = []
        if added: parts.append(c(GREEN, f'+{added}'))
        if removed: parts.append(c(RED, f'-{removed}'))
        branch_str += ' ' + c(DIM + WHITE, '(') + ' '.join(parts) + c(DIM + WHITE, ')')

# ---------- GitHub connection (native fields first, git as fallback)
repo = ws.get('repo') or {}
g_host = repo.get('host') or gi.get('host')
g_owner = repo.get('owner') or gi.get('owner')
g_name = repo.get('name') or gi.get('name')


def pr_lookup():
    try:
        r = subprocess.run(['gh', 'pr', 'view', '--json', 'number,state'], cwd=cwd,
                           capture_output=True, text=True, timeout=4)
        if r.returncode == 0:
            j = json.loads(r.stdout)
            return f"#{j['number']} {j['state'].lower()}"
    except Exception:
        pass
    return ''


github_str = ''
if part_on(CFG, 'github') and gi.get('has_git'):
    if g_owner and g_name:
        label = f'{g_owner}/{g_name}' if 'github' in (g_host or 'github') else f'{g_host}:{g_owner}/{g_name}'
        github_str = c(WHITE, 'gh:') + c(CYAN, label)
        if gi.get('upstream'):
            a, b = gi.get('ahead', 0), gi.get('behind', 0)
            bits = []
            if a: bits.append(c(GREEN, f'↑{a}'))
            if b: bits.append(c(RED, f'↓{b}'))
            github_str += ' ' + (' '.join(bits) if bits else c(DIM + WHITE, 'synced'))
        else:
            github_str += ' ' + c(ORANGE, 'no upstream')
        pr = d.get('pr') or {}
        if pr.get('number'):
            rs = pr.get('review_state')
            rcol = {'approved': GREEN, 'changes_requested': RED, 'draft': DIM + WHITE}.get(rs, MAGENTA)
            github_str += ' ' + c(rcol, f"PR #{pr['number']}" + (f' {rs.replace("_", " ")}' if rs else ''))
        elif 'pr' not in d and CFG.get('use_gh', True) and branch not in ('main', 'master', ''):
            ghpr = cached(f'pr:{g_owner}/{g_name}:{branch}', 120, pr_lookup)
            if ghpr:
                github_str += ' ' + c(MAGENTA, f'PR {ghpr}')
    else:
        github_str = c(ORANGE, 'gh: no remote')

# ---------- Tasks and subtasks
STATUS_DONE = ('completed', 'done')


def read_tasks(transcript_path):
    """Rebuild the latest task list from the session transcript (TodoWrite, TaskCreate, TaskUpdate)."""
    todos = None
    tasks, order, seq = {}, [], 0
    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            for line in f:
                if '"tool_use"' not in line:
                    continue
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                content = (obj.get('message') or {}).get('content')
                if not isinstance(content, list):
                    continue
                for blk in content:
                    if not isinstance(blk, dict) or blk.get('type') != 'tool_use':
                        continue
                    name, inp = blk.get('name') or '', blk.get('input') or {}
                    if name == 'TodoWrite':
                        todos = [{'id': str(i), 'subject': t.get('content') or t.get('subject') or '',
                                  'status': t.get('status', 'pending'), 'parent': t.get('parent') or t.get('parentId')}
                                 for i, t in enumerate(inp.get('todos') or [])]
                        tasks, order = {}, []
                    elif name == 'TaskCreate':
                        seq += 1
                        tid = str(seq)
                        meta = inp.get('metadata') or {}
                        tasks[tid] = {'id': tid, 'subject': inp.get('subject', ''), 'status': 'pending',
                                      'parent': meta.get('parent') or meta.get('parentId') or inp.get('parent')}
                        order.append(tid)
                        todos = None
                    elif name == 'TaskUpdate':
                        tid = str(inp.get('taskId', ''))
                        if tid in tasks:
                            if inp.get('status') == 'deleted':
                                tasks.pop(tid, None)
                                order = [x for x in order if x != tid]
                            else:
                                if inp.get('status'):
                                    tasks[tid]['status'] = inp['status']
                                if inp.get('subject'):
                                    tasks[tid]['subject'] = inp['subject']
    except Exception:
        return []
    return todos if todos is not None else [tasks[t] for t in order if t in tasks]


def tasks_cached(tp):
    try:
        st = os.stat(tp)
    except Exception:
        return []
    key = f'tasks:{tp}:{st.st_size}:{st.st_mtime_ns}'
    try:
        return json.loads(cached(key, 86400, lambda: json.dumps(read_tasks(tp))) or '[]')
    except Exception:
        return []


def split_tree(items):
    ids = {str(t['id']) for t in items}
    parents, subs, last_parent = [], {}, None
    for t in items:
        subj, par = t.get('subject') or '', t.get('parent')
        if par is not None and str(par) in ids:
            subs.setdefault(str(par), []).append(t)
            continue
        if ' > ' in subj:
            head, tail = subj.split(' > ', 1)
            t['subject'] = tail
            for p in parents:
                if p['subject'] == head:
                    subs.setdefault(str(p['id']), []).append(t)
                    break
            else:
                parents.append(t)
            continue
        if subj.startswith(('- ', '  ')) and last_parent is not None:
            t['subject'] = subj.strip(' -')
            subs.setdefault(str(last_parent['id']), []).append(t)
            continue
        parents.append(t)
        last_parent = t
    return parents, subs


def bar(done, total, width=8):
    filled = round(width * done / total) if total else 0
    col = GREEN if done == total else (YELLOW if done else DIM + WHITE)
    return c(col, '■' * filled) + c(DIM + WHITE, '□' * (width - filled))


def trunc(s, n):
    s = ' '.join(clean(s).split())
    return s if len(s) <= n else s[:n - 1] + '…'


tasks_str = tasks_line2 = ''
tp = d.get('transcript_path')
if part_on(CFG, 'tasks') and (tp or SAMPLE):
    items = [dict(t) for t in SAMPLE_TASKS] if SAMPLE else tasks_cached(tp)
    if items:
        parents, subs = split_tree(items)
        done = sum(1 for p in parents if p['status'] in STATUS_DONE)
        total = len(parents)
        tasks_str = c(WHITE, 'tasks ') + bar(done, total) + ' ' + c(WHITE + BOLD, f'{done}/{total}')
        active_t = next((p for p in parents if p['status'] == 'in_progress'), None) \
            or next((p for p in parents if p['status'] not in STATUS_DONE), None)
        if active_t is not None:
            kids = subs.get(str(active_t['id']), [])
            line = c(CYAN + BOLD, '▶ ') + c(WHITE, trunc(active_t['subject'], 48))
            if kids:
                kd = sum(1 for k in kids if k['status'] in STATUS_DONE)
                line += ' ' + c(DIM + WHITE, f'[{kd}/{len(kids)} sub]')
                cur = next((k for k in kids if k['status'] == 'in_progress'), None) \
                    or next((k for k in kids if k['status'] not in STATUS_DONE), None)
                if cur:
                    line += c(DIM + WHITE, ' › ') + c(YELLOW, trunc(cur['subject'], 40))
            tasks_line2 = line

# ---------- Context, tokens, cost, time
if pct is not None:
    filled = min(10, round(pct / 10))
    bc = GREEN if pct < 50 else (YELLOW if pct < 75 else RED)
    ctx_bar = c(bc, chr(9608) * filled) + c(DIM + WHITE, chr(9617) * (10 - filled)) + ' ' + c(bc + BOLD, f'{round(pct)}%')
else:
    ctx_bar = c(DIM, chr(9617) * 10 + ' --%')

tok_str = ''
if used_tok is not None:
    tok_str = c(WHITE, f'{used_tok / 1000:.1f}K tok') if used_tok >= 1000 else c(WHITE, f'{used_tok} tok')
    if max_tok:
        tok_str += c(DIM + WHITE, f'/{max_tok // 1000}K')
cost_str = c(GREEN, f'${cost_val:.4f}') if cost_val is not None else ''
time_str = ''
if sess_mins is not None:
    time_str = c(BLUE, f'{sess_mins}min') if sess_mins < 60 else c(BLUE, f'{sess_mins // 60}h{sess_mins % 60:02d}m')

memory_str = ''
if CFG.get('show_memory') and CFG.get('memory_file'):
    try:
        with open(os.path.expanduser(CFG['memory_file']), 'r', encoding='utf-8') as f:
            memory_str = c(DIM + WHITE, f"mem[{len(re.findall(r'^## (.+)', f.read(), re.MULTILINE))}sec]")
    except Exception:
        memory_str = c(DIM, 'mem:--')

# ---------- Fun line: organization, mood, sprite, heart line
fun_line = ''
if CFG.get('fun_line', True):
    # life: how much runway is left. context (default), five_hour (plan limit) or lowest of both.
    five = ((d.get('rate_limits') or {}).get('five_hour') or {}).get('used_percentage')
    src = CFG.get('life_source', 'context')
    options = []
    if src in ('context', 'lowest') and rem is not None: options.append(rem)
    if src in ('five_hour', 'lowest') and five is not None: options.append(100 - five)
    health = max(0.0, min(100.0, min(options))) if options else 100.0
    dead = health <= 3

    # activity: did tokens, cost or the transcript change recently?
    now = time.time()
    state_path = os.path.join(CACHE_DIR, f'state-{sid}.json')
    state = {}
    try:
        with open(state_path, 'r', encoding='utf-8') as f:
            state = json.load(f)
    except Exception:
        pass
    sig = json.dumps([cost_val, t_in, t_out, cost_raw.get('total_lines_added'), cost_raw.get('total_api_duration_ms')])
    last_change = state.get('last_change', 0)
    if sig != state.get('sig'):
        last_change = now
    try:
        last_change = max(last_change, os.path.getmtime(tp)) if tp else last_change
    except Exception:
        pass
    linger = float(CFG.get('active_seconds', 8))
    active = (now - last_change) < linger and not dead
    pos = float(state.get('pos', 0))
    if active and now - state.get('ts', 0) >= 0.25:
        pos = (pos + get_sprite(pick_sprite(CFG, sid), CFG)['step']) % 1000000
        state['ts'] = now
    state.update({'sig': sig, 'last_change': last_change, 'pos': pos})
    try:
        os.makedirs(CACHE_DIR, exist_ok=True)
        with open(state_path, 'w', encoding='utf-8') as f:
            json.dump(state, f)
    except Exception:
        pass

    narrow = cols < 90
    w_track, w_ecg = (10, 8) if narrow else (16, 12)
    org = clean(CFG.get('org') or g_owner or '')
    pieces = []
    if org and part_on(CFG, 'org'):
        pieces.append('🏢 ' + c(CYAN + BOLD, org))
    if part_on(CFG, 'flags'):
        fl = flags_segment(CFG, narrow)
        if fl: pieces.append(fl)
    if part_on(CFG, 'mood'):
        m = mood_segment(CFG)
        if m: pieces.append(m)
    if part_on(CFG, 'animation'):
        track = track_segment(pick_sprite(CFG, sid), pos, w_track, active, dead, CFG)
        if not (CFG.get('sprite_chosen') or CFG.get('setup_done')) and CFG.get('fav_reminder', True):
            track += ' ' + c(DIM + WHITE, '🎬?')   # nudge: run /statusline to pick a favorite animation
        pieces.append(track)
    if part_on(CFG, 'heart'):
        pieces.append(heart_segment(health, w_ecg, int(now * 2)))
    fun_line = c(DIM + WHITE, ' | ').join(pieces)

# ---------- Assemble
SEP = c(DIM + WHITE, ' | ')
line1 = []
if part_on(CFG, 'app'): line1.append(phase_str)
if branch_str and part_on(CFG, 'branch'): line1.append(branch_str)
if github_str: line1.append(github_str)
if tasks_str and not CFG.get('two_lines', True): line1.append(tasks_str)
if part_on(CFG, 'model'): line1.append(c(MAGENTA + BOLD, model))
if part_on(CFG, 'context'): line1.append(ctx_bar)
for name, val in (('tokens', tok_str), ('cost', cost_str), ('time', time_str)):
    if val and part_on(CFG, name): line1.append(val)
if memory_str: line1.append(memory_str)

lines = []
if line1:
    lines.append(SEP.join(line1))
if CFG.get('two_lines', True):
    row2 = [x for x in (tasks_str, tasks_line2) if x]
    if row2:
        lines.append(SEP.join(row2))
if fun_line:
    lines.append(fun_line)
if part_on(CFG, 'alerts'):
    al = alert_line(rem, time.time(), sid)
    if al:
        lines.append(al)

sys.stdout.buffer.write('\n'.join(lines).encode('utf-8'))
