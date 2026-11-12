# PelvisPower for Men: exec'd from build_site.py (shares page, E, tc, paras, P, PAGES).
MSRC = '/home/claude/men/PelvisPower-for-Men_Draft_30-Days.txt'
_mt = open(MSRC).read()
_mb = re.split(r'\n={20,}\n', _mt)
_mparts = []
_i = 1
while _i < len(_mb):
    _mparts.append((_mb[_i].strip(), _mb[_i + 1] if _i + 1 < len(_mb) else ''))
    _i += 2
MSTART = []
for _blk in re.split(r'\n\n\n+', _mparts[0][1].strip()):
    _ls = _blk.strip().split('\n')
    MSTART.append((_ls[0].strip(), '\n'.join(_ls[1:]).strip()))
MLEVELS = []; MDAYS = {}; MLEAD = []
for _h, _body in _mparts[1:]:
    if _h.startswith('LEVEL'):
        _hh = _h.split('\n')
        MLEVELS.append({'n': int(re.search(r'LEVEL (\d)', _hh[0]).group(1)), 'name': _hh[0].split(':')[1].strip().title(), 'desc': _hh[1].strip(), 'days': []})
        for _db in re.split(r'\n\n\n+(?=DAY \d+\n)', _body.strip()):
            _db = _db.strip()
            if not _db.startswith('DAY'): continue
            _m = re.match(r"DAY (\d+)\n([^\n]+)\n([^\n]+)\n\n(.*?)\n\nTODAY'S SET\n(.*)$", _db, re.S)
            _n = int(_m.group(1)); _rest = _m.group(5); _ex = ''
            if _n == 30:
                _rest, _ex = _rest.split('\n\nTHE CERTIFICATE', 1); _ex = 'THE CERTIFICATE' + _ex
            MDAYS[_n] = {'n': _n, 'title': tc(_m.group(2).strip()), 'sub': _m.group(3).strip(), 'read': paras(_m.group(4)), 'set': _rest.strip().split('\n'), 'extra': _ex.strip(), 'level': MLEVELS[-1]['n']}
            MLEVELS[-1]['days'].append(_n)
    elif _h.startswith('BECOME'):
        MLEAD = paras(_body)
assert len(MDAYS) == 30, len(MDAYS)
MREC = {n for n, d in MDAYS.items() if d['title'].lower() == 'recess'} | {30}
json.dump({str(n): d['title'] for n, d in MDAYS.items()}, open('/home/claude/pelvispower/men_titles.json', 'w'))
json.dump([L['name'] for L in MLEVELS], open('/home/claude/pelvispower/men_levels.json', 'w'))

def mcard(n):
    d = MDAYS[n]
    im = '<span class="seal">★</span>' if n == 30 else ('<span class="rec">Recess</span>' if n in MREC else '')
    return f'<a class="dcard{" rc" if n in MREC else ""}" href="/men/day-{n:02d}/"><b>Day {n}</b>{im}<span>{E(d["sub"] if n in MREC and n != 30 else d["title"])}</span></a>'

_lv = ''.join(f'<section class="lvl"><h2>Level {L["n"]}: {E(L["name"])}</h2><p class="sub">{E(L["desc"])}</p><div class="dgrid">{"".join(mcard(n) for n in L["days"])}</div></section>' for L in MLEVELS)
_land = '''<p class="kick">PelvisPower for Men</p><h1>The 30-Day Course</h1><p class="sub">The same month, for the muscles men have too</p><article>
<p>Men have a pelvic floor, and it does a great deal. It supports sexual function, helps with control and stamina, and takes part in orgasm. It can be trained, and the training is friendly and discreet.</p>
<p>Three to ten minutes a day, in thin comfortable clothes. Light, funny and never clinical, with a Pleasure Dial from 1 to 5 and a reward that you set yourself. Every Day is open to read. Take them in order or wander.</p>
<p class="c"><a class="btn" href="/men/start-here/">Start here</a> <a class="btn alt" href="/men/dozen/">The Daily Dozen</a></p></article></main><main class="wide">''' + _lv + '''<article><h2>Train with her</h2><p>Many couples train in parallel, one in each book, and compare numbers over breakfast. See <a href="/two/">Together</a> and <a href="/women/">PelvisPower for Women</a>.</p>
<h2>The longer game</h2><p>A companion book is on the way: <i>Well-Suited to Pleasure: The Long Game for Male Sexual Performance</i>. Well-suited means the trunk stays suited for most of the day. The Long Game is stamina and control.</p></article>'''
page('/men/', 'PelvisPower for Men | 30-Day Course', 'All 30 Days of PelvisPower for Men: five Levels, twelve moves, a graduation diploma.', _land, active='/men/')

_sh = '<p class="kick">PelvisPower for Men</p><h1>Start Here</h1><p class="sub">What this book does for you, and how the month works</p><article>'
MDOZ = []
for _h, _b in MSTART:
    if _h == 'THE DAILY DOZEN':
        for _l in _b.split('\n'):
            _m = re.match(r'(\d+)\. (The [^.]+)\. (.*)$', _l.strip())
            if _m: MDOZ.append((_m.group(2), _m.group(3)))
        _sh += f'<h2>{tc(_h)}</h2><p>Twelve moves, learned once and polished all month. <a href="/men/dozen/">See the full list.</a></p>'; continue
    _sh += f'<h2 id="{re.sub(r"[^a-z]+", "-", _h.lower()).strip("-")}">{tc(_h)}</h2>' + P(paras(_b))
_sh += '</article><p class="c"><a class="btn" href="/men/day-01/">Begin with Day 1</a></p>'
page('/men/start-here/', 'Start Here | PelvisPower for Men', 'What the course does for you, how the month works, and how to train alone, in pairs or in a class.', _sh, active='/men/')

_dz = '<p class="kick">The moves</p><h1>The Daily Dozen</h1><p class="sub">Twelve moves. Every Day uses some of them.</p><div class="dozen">'
for _k, (_n, _d) in enumerate(MDOZ, 1):
    _used = [n for n, d in MDAYS.items() if any(_n.lower() in x.lower() for x in d['set'] if x.startswith('Move') or x.startswith('Warm-up') or x.startswith('Cool-down'))]
    _u = f'<p class="used">Featured on {", ".join(f"<a href=/men/day-{x:02d}/>Day {x}</a>" for x in _used[:8])}</p>' if _used else ''
    _dz += f'<div class="dz" id="m{_k}"><h3>{_k}. {E(_n)}</h3><p>{E(_d)}</p>{_u}</div>'
_dz += '</div>'
page('/men/dozen/', 'The Daily Dozen | PelvisPower for Men', 'Twelve simple pelvic floor moves for men.', _dz, active='/men/', main_class='wide')

for n, d in MDAYS.items():
    art = '<div class="sealbig">★</div>' if n == 30 else ''
    b = f'{art}<p class="kick">Day {n} · Level {d["level"]}{" · Recess" if n in MREC and n != 30 else ""}</p><h1>{E(d["title"])}</h1><p class="sub">{E(d["sub"])}</p><article>'
    for p in d['read']:
        if p.startswith('Form check:'):
            _t = p[11:].strip(); b += f'<p class="form"><b>Form check</b>{E(_t[0].upper() + _t[1:])}</p>'
        else: b += f'<p>{E(p)}</p>'
    b += '</article><div class="set"><h2>Today\'s Set</h2><dl>'
    for l in d['set']:
        m = re.match(r'^(Time|Position|Garment|Warm-up|Cool-down|Pleasure Dial|Variation|Move \d+, [^:]+|Test \d+, [^:]+|The Recess|The routine|The three numbers, each with a Soft Drop between|THE LOG):\s*(.*)$', l)
        if m: b += f'<dt>{E(m.group(1).replace("THE LOG", "The Log"))}</dt><dd>{E(m.group(2)[:1].upper() + m.group(2)[1:])}</dd>'
        elif l.startswith('  '): b += f'<dd class="sub2">{E(l.strip())}</dd>'
        else: b += f'<dt class="wide">&nbsp;</dt><dd>{E(l)}</dd>'
    b += '</dl></div>'
    if d['extra']:
        _ls = d['extra'].split('\n')
        b += '<div class="cert"><h2>The Certificate of Pelvic Excellence</h2>' + ''.join(f'<p>{E(x)}</p>' for x in _ls[1:]) + '<p class="c"><a class="btn alt" href="/women/leaders/">Become a leader</a></p></div>'
    prv = f'<a href="/men/day-{n-1:02d}/">← Day {n-1}</a>' if n > 1 else '<a href="/men/start-here/">← Start Here</a>'
    nxt = f'<a href="/men/day-{n+1:02d}/">Day {n+1} →</a>' if n < 30 else '<a href="/women/leaders/">Leaders →</a>'
    b += f'<div class="pn">{prv}<a href="/men/">All Days</a>{nxt}</div>'
    page(f'/men/day-{n:02d}/', f'Day {n}: {d["title"]} | PelvisPower for Men', d['sub'], b, active='/men/')
