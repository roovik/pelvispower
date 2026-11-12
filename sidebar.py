#!/usr/bin/env python3
"""Right-hand widget column for Dress for Caress and PelvisPower (all 8 languages).
Idempotent. Same file lives in both repos.
  dressforcaress/tools/sidebar.py   -> processes DfC public/ and private-pages.js
  pelvispower/sidebar.py            -> processes PelvisPower public/
Run after the page builders. Usage: python3 sidebar.py"""
import os, re, json, glob, html

DFC = '/home/claude/dressforcaress'
PP = '/home/claude/pelvispower'
LANGS = ['en', 'fr', 'es', 'de', 'pt', 'ru', 'he', 'th']
PRE = {'en': ''}
PRE.update({l: '/' + l for l in LANGS if l != 'en'})

S = {
 'en': dict(side_h='The 30 days', comp_k='Companion course', pp_b='A 30-day pelvic floor plan that goes with this book. Same month, same pace.', pp_cta='Open PelvisPower', pair_k="Today's pairing", prog='Day {n} of 30', dfc_k='Companion book', dfc_b='Thirty days of stories and notes to read alongside your training. Week one is free.', dfc_cta='Read Dress for Caress', pairr_k="Today's reading", your='Your 30 days', soon='In preparation', men_h='The 30 days', men_b='The same month, for the muscles men have too.', her_k='For the woman in your life', her_b='She can start today with PelvisPower for Women and its companion book.', her_cta='PelvisPower for Women', both_h='Choose your path', w='Women', m='Men', t='Together', members='members'),
 'fr': dict(side_h='Les 30 jours', comp_k='Cours compagnon', pp_b="Un plan de 30 jours pour le plancher pelvien, qui accompagne ce livre. Même mois, même rythme.", pp_cta='Ouvrir PelvisPower', pair_k="L'association du jour", prog='Jour {n} sur 30', dfc_k='Livre compagnon', dfc_b="Trente jours d'histoires et de notes à lire en parallèle de votre entraînement. La première semaine est gratuite.", dfc_cta='Lire Dress for Caress', pairr_k='La lecture du jour', your='Vos 30 jours', soon='En préparation', men_h='Les 30 jours', men_b='Le même mois, pour les muscles que les hommes ont aussi.', her_k='Pour la femme de votre vie', her_b="Elle peut commencer aujourd'hui avec PelvisPower pour les femmes et son livre compagnon.", her_cta='PelvisPower pour les femmes', both_h='Choisissez votre voie', w='Femmes', m='Hommes', t='À deux', members='membres'),
 'es': dict(side_h='Los 30 días', comp_k='Curso compañero', pp_b='Un plan de 30 días para el suelo pélvico que acompaña a este libro. El mismo mes, el mismo ritmo.', pp_cta='Abrir PelvisPower', pair_k='La pareja de hoy', prog='Día {n} de 30', dfc_k='Libro compañero', dfc_b='Treinta días de relatos y notas para leer junto a tu entrenamiento. La primera semana es gratis.', dfc_cta='Leer Dress for Caress', pairr_k='La lectura de hoy', your='Tus 30 días', soon='En preparación', men_h='Los 30 días', men_b='El mismo mes, para los músculos que los hombres también tienen.', her_k='Para la mujer de tu vida', her_b='Ella puede empezar hoy con PelvisPower para mujeres y su libro compañero.', her_cta='PelvisPower para mujeres', both_h='Elige tu camino', w='Mujeres', m='Hombres', t='En pareja', members='miembros'),
 'de': dict(side_h='Die 30 Tage', comp_k='Begleitkurs', pp_b='Ein 30-Tage-Plan für den Beckenboden, der zu diesem Buch gehört. Derselbe Monat, dasselbe Tempo.', pp_cta='PelvisPower öffnen', pair_k='Das heutige Paar', prog='Tag {n} von 30', dfc_k='Begleitbuch', dfc_b='Dreißig Tage voller Geschichten und Notizen, die du neben deinem Training liest. Die erste Woche ist kostenlos.', dfc_cta='Dress for Caress lesen', pairr_k='Die heutige Lektüre', your='Deine 30 Tage', soon='In Vorbereitung', men_h='Die 30 Tage', men_b='Derselbe Monat, für die Muskeln, die auch Männer haben.', her_k='Für die Frau in deinem Leben', her_b='Sie kann heute mit PelvisPower für Frauen und dem Begleitbuch beginnen.', her_cta='PelvisPower für Frauen', both_h='Wähle deinen Weg', w='Frauen', m='Männer', t='Zu zweit', members='Mitglieder'),
 'pt': dict(side_h='Os 30 dias', comp_k='Curso companheiro', pp_b='Um plano de 30 dias para o assoalho pélvico que acompanha este livro. O mesmo mês, o mesmo ritmo.', pp_cta='Abrir PelvisPower', pair_k='O par de hoje', prog='Dia {n} de 30', dfc_k='Livro companheiro', dfc_b='Trinta dias de histórias e notas para ler junto com o seu treino. A primeira semana é grátis.', dfc_cta='Ler Dress for Caress', pairr_k='A leitura de hoje', your='Seus 30 dias', soon='Em preparação', men_h='Os 30 dias', men_b='O mesmo mês, para os músculos que os homens também têm.', her_k='Para a mulher da sua vida', her_b='Ela pode começar hoje com PelvisPower para mulheres e o livro companheiro.', her_cta='PelvisPower para mulheres', both_h='Escolha o seu caminho', w='Mulheres', m='Homens', t='A dois', members='membros'),
 'ru': dict(side_h='30 дней', comp_k='Курс-компаньон', pp_b='30-дневный план для тазового дна, который идёт вместе с этой книгой. Тот же месяц, тот же темп.', pp_cta='Открыть PelvisPower', pair_k='Пара на сегодня', prog='День {n} из 30', dfc_k='Книга-компаньон', dfc_b='Тридцать дней историй и заметок, которые читаются рядом с вашими тренировками. Первая неделя бесплатна.', dfc_cta='Читать Dress for Caress', pairr_k='Чтение на сегодня', your='Ваши 30 дней', soon='В подготовке', men_h='30 дней', men_b='Тот же месяц, для мышц, которые есть и у мужчин.', her_k='Для женщины в вашей жизни', her_b='Она может начать сегодня с PelvisPower для женщин и книгой-компаньоном.', her_cta='PelvisPower для женщин', both_h='Выберите свой путь', w='Женщины', m='Мужчины', t='Вдвоём', members='для участников'),
 'he': dict(side_h='30 הימים', comp_k='קורס מלווה', pp_b='תוכנית של 30 יום לרצפת האגן שהולכת יד ביד עם הספר הזה. אותו חודש, אותו קצב.', pp_cta='לפתוח את PelvisPower', pair_k='הזיווג של היום', prog='יום {n} מתוך 30', dfc_k='ספר מלווה', dfc_b='שלושים ימים של סיפורים והערות לקריאה לצד האימון שלך. השבוע הראשון חינם.', dfc_cta='לקרוא את Dress for Caress', pairr_k='הקריאה של היום', your='30 הימים שלך', soon='בהכנה', men_h='30 הימים', men_b='אותו חודש, לשרירים שיש גם לגברים.', her_k='לאישה שבחייך', her_b='היא יכולה להתחיל היום עם PelvisPower לנשים והספר המלווה שלו.', her_cta='PelvisPower לנשים', both_h='בחרו את הדרך שלכם', w='נשים', m='גברים', t='ביחד', members='לחברות'),
 'th': dict(side_h='30 วัน', comp_k='คอร์สคู่ใจ', pp_b='แผน 30 วันสำหรับกล้ามเนื้อเชิงกรานที่ไปด้วยกันกับหนังสือเล่มนี้ เดือนเดียวกัน จังหวะเดียวกัน', pp_cta='เปิด PelvisPower', pair_k='คู่ของวันนี้', prog='วันที่ {n} จาก 30', dfc_k='หนังสือคู่ใจ', dfc_b='เรื่องเล่าและบันทึกสามสิบวันให้อ่านควบคู่กับการฝึก สัปดาห์แรกอ่านฟรี', dfc_cta='อ่าน Dress for Caress', pairr_k='บทอ่านของวันนี้', your='30 วันของคุณ', soon='กำลังเตรียม', men_h='30 วัน', men_b='เดือนเดียวกัน สำหรับกล้ามเนื้อที่ผู้ชายก็มี', her_k='สำหรับผู้หญิงในชีวิตคุณ', her_b='เธอเริ่มได้วันนี้ด้วย PelvisPower สำหรับผู้หญิงและหนังสือคู่ใจ', her_cta='PelvisPower สำหรับผู้หญิง', both_h='เลือกเส้นทางของคุณ', w='ผู้หญิง', m='ผู้ชาย', t='ด้วยกัน', members='สมาชิก'),
}

OPEN = '<!--sb--><div class="shell"><div class="col"><!--/sb-->'
CLOSE_RE = re.compile(r'<!--sb2-->.*?<!--/sb2-->', re.S)
OPEN_RE = re.compile(r'<!--sb-->.*?<!--/sb-->', re.S)


def read(p):
    return open(p, encoding='utf-8').read()


# ---------------------------------------------------------------- scraping
def scrape_dfc():
    """{lang: {n: (title, locked, label)}} from DfC contents pages."""
    out = {}
    for l in LANGS:
        p = f'{DFC}/public{PRE[l]}/contents/index.html'
        if not os.path.exists(p):
            continue
        s = read(p)
        d = {}
        for m in re.finditer(r'<li class="(locked)?"?>?<a href="[^"]*/day-(\d\d)/"><span class="dk">[^<]*</span>\s*(.*?)</a>(.*?)</li>', s):
            d[int(m.group(2))] = (m.group(3), bool(m.group(1)))
        if not d:
            for m in re.finditer(r'<li class="([^"]*)"><a href="[^"]*/day-(\d\d)/"><span class="dk">[^<]*</span>\s*(.*?)</a>', s):
                d[int(m.group(2))] = (m.group(3), 'locked' in m.group(1))
        out[l] = d
    return out


def scrape_pp():
    out = {}
    for l in LANGS:
        p = f'{PP}/public{PRE[l]}/women/index.html'
        if not os.path.exists(p):
            continue
        s = read(p)
        d = {}
        for m in re.finditer(r'<a class="dcard[^"]*" href="([^"]*/women/day-(\d\d)/)">.*?<span>([^<]*)</span></a>', s):
            d[int(m.group(2))] = (m.group(3), m.group(1))
        out[l] = d
    return out


def men_titles():
    f = '/nonexistent'
    cache = f'{PP}/men_titles.json'
    d = {}
    if os.path.exists(f):
        L = read(f).split('\n')
        for i, x in enumerate(L):
            m = re.fullmatch(r'DAY (\d+)', x.strip())
            if m and i + 1 < len(L):
                d[int(m.group(1))] = L[i + 1].strip().title().replace("'S", "'s")
        json.dump(d, open(cache, 'w'))
    elif os.path.exists(cache):
        d = {int(k): v for k, v in json.load(open(cache)).items()}
    return d


def scrape_levels():
    out = {}
    for l in LANGS:
        p = f'{PP}/public{PRE[l]}/women/index.html'
        if os.path.exists(p):
            out[l] = re.findall(r'<section class="lvl"><h2>(.*?)</h2>', read(p))
    return out


LV = scrape_levels()
MENLV = json.load(open(f'{PP}/men_levels.json')) if os.path.exists(f'{PP}/men_levels.json') else []
CTRL = {'fr': 'Contrôle', 'es': 'Control', 'de': 'Kontrolle', 'pt': 'Controle', 'ru': 'Контроль', 'he': 'שליטה', 'th': 'การควบคุม'}


def men_level_heads(l):
    base = list(LV.get(l) or LV['en'])
    if l == 'en':
        return [f'Level {i + 1}: {n}' for i, n in enumerate(MENLV)] if MENLV else base
    if len(base) > 3 and l in CTRL and ':' in base[3]:
        base[3] = base[3].split(':')[0] + ': ' + CTRL[l]
    return base


DF = scrape_dfc()
PW = scrape_pp()
MEN = men_titles()


def pp_href(l, n):
    """PelvisPower women day link for language l, falling back to English."""
    for lang in (l, 'en'):
        h = f'{PRE[lang]}/women/day-{n:02d}/'
        if os.path.exists(f'{PP}/public{h}index.html'):
            return 'https://pelvispower.org' + h
    return 'https://pelvispower.org/women/'


def dfc_href(l, n):
    for lang in (l, 'en'):
        h = f'{PRE[lang]}/day-{n:02d}/'
        if os.path.exists(f'{DFC}/public{h}index.html'):
            return 'https://dressforcaress.com' + h
    return 'https://dressforcaress.com/contents/'


def e(x):
    return html.escape(x, quote=True)


# ---------------------------------------------------------------- blocks
def card(kind, k, title, body, cta, href, extra=''):
    cov = f'<a class="scov" href="{href}" rel="noopener"><img src="/assets/dfc-cover.jpg" width="210" height="315" alt="Dress for Caress, book cover" loading="lazy"></a>' if kind == 'dfc' else ''
    return (f'<div class="sw card {kind}">{cov}<p class="sk">{e(k)}</p><p class="st">{e(title)}</p>{extra}'
            f'<p class="sb">{e(body)}</p><a class="sbtn" href="{href}" rel="noopener">{e(cta)}</a></div>')


def prog_bar(t, n):
    return (f'<div class="prog" role="img" aria-label="{e(t["prog"].format(n=n))}"><i style="width:{round(n * 100 / 30)}%"></i></div>'
            f'<p class="pt">{e(t["prog"].format(n=n))}</p>')


def dfc_list(l, cur, t):
    items = DF.get(l) or DF['en']
    pre = PRE[l] if l in DF else ''
    li = ''
    for n in range(1, 31):
        title, locked = items.get(n, ('', False))
        cls = ' class="cur" aria-current="page"' if n == cur else (' class="lk"' if locked else '')
        mark = f'<span class="lm">{e(t["members"])}</span>' if locked else ''
        li += f'<li{cls}><a href="{pre}/day-{n:02d}/"><b>{n}</b><span>{title}</span></a>{mark}</li>'
    return f'<div class="sw days"><h2>{e(t["side_h"])}</h2><ol>{li}</ol></div>'


def pp_list(l, cur, t, heading):
    items = PW.get(l) or PW['en']
    lv = LV.get(l) or LV['en']
    li = ''
    for n in range(1, 31):
        title, h = items.get(n, ('', ''))
        if (n - 1) % 6 == 0 and len(lv) >= (n - 1) // 6 + 1:
            li += ('</ol>' if n > 1 else '') + f'<h3 class="lv">{lv[(n - 1) // 6]}</h3><ol>'
        href = '/women/day-%02d/' % n
        pre = PRE[l] if l in PW else ''
        href = f'{pre}{href}'
        if not os.path.exists(f'{PP}/public{href}index.html'):
            href = '/women/day-%02d/' % n
        cls = ' class="cur" aria-current="page"' if n == cur else ''
        li += f'<li{cls}><a href="{href}"><b>{n}</b><span>{title}</span></a></li>'
    return f'<div class="sw days"><h2>{e(heading)}</h2>{li}</ol></div>'


def men_list(l, t, cur=0):
    lv = men_level_heads(l)
    li = ''
    for n in range(1, 31):
        if (n - 1) % 6 == 0 and len(lv) >= (n - 1) // 6 + 1:
            li += ('</ol>' if n > 1 else '') + f'<h3 class="lv">{lv[(n - 1) // 6]}</h3><ol>'
        cls = ' class="cur" aria-current="page"' if n == cur else ''
        li += f'<li{cls}><a href="/men/day-{n:02d}/"><b>{n}</b><span lang="en">{e(MEN.get(n, ""))}</span></a></li>'
    return f'<div class="sw days"><h2>{e(t["men_h"])}</h2>{li}</ol></div>'


def side_dfc(l, cur):
    t = S[l]
    pre = PRE[l] if l in PW else ''
    if cur:
        pt = (PW.get(l) or PW['en']).get(cur, ('', ''))[0]
        extra = (f'<p class="pair"><span>{e(t["pair_k"])}</span><a href="{pp_href(l, cur)}" rel="noopener">PelvisPower, {e(t["prog"].format(n=cur))}: {e(pt)}</a></p>'
                 + prog_bar(t, cur))
        head = card('pp', t['comp_k'], 'PelvisPower', t['pp_b'], t['pp_cta'], pp_href(l, cur) if cur else 'https://pelvispower.org/', extra)
    else:
        head = card('pp', t['comp_k'], 'PelvisPower', t['pp_b'], t['pp_cta'], 'https://pelvispower.org' + (PRE[l] + '/women/' if l in PW else '/women/'))
    cover = f'<a class="scov" href="{PRE[l] if l in DF else ""}/"><img src="/assets/cover-sm.jpg" width="210" height="315" alt="Dress for Caress, book cover"></a>'
    ppc = (f'<a class="scov" href="{pp_href(l, cur) if cur else "https://pelvispower.org" + (PRE[l] + "/women/" if l in PW else "/women/")}" rel="noopener"><img src="/assets/pp-cover-sm.jpg" width="210" height="315" alt="PelvisPower for Women, book cover"></a>')
    head = head.replace('<p class="st">PelvisPower</p>', '<p class="st">' + e(t['her_cta']) + '</p>').replace('<div class="sw card pp">', '<div class="sw card pp">' + ppc, 1)
    return head + cover + '<p class="sh" lang="en">Dress for Caress: 30 Days to Peak Pleasure</p>' + dfc_list(l, cur, t)


def side_pp(l, kind, cur):
    """kind: women | men | gen"""
    t = S[l]
    dfc_pre = 'https://dressforcaress.com' + (PRE[l] if l in DF else '')
    if kind == 'women':
        if cur:
            dt = (DF.get(l) or DF['en']).get(cur, ('', False))[0]
            extra = (f'<p class="pair"><span>{e(t["pairr_k"])}</span><a href="{dfc_href(l, cur)}" rel="noopener">Dress for Caress, {e(t["prog"].format(n=cur))}: {dt}</a></p>')
            top = card('dfc', t['dfc_k'], 'Dress for Caress', t['dfc_b'], t['dfc_cta'], dfc_href(l, cur), extra)
        else:
            top = card('dfc', t['dfc_k'], 'Dress for Caress', t['dfc_b'], t['dfc_cta'], dfc_pre + '/')
        return top + pp_list(l, cur, t, t['your'])
    if kind == 'men':
        top = (f'<div class="sw card men"><p class="sk">PelvisPower</p><p class="st">{e(t["m"])}</p><p class="sb">{e(t["men_b"])}</p></div>')
        book = (f'<div class="sw card book"><p class="sk">{e(t["soon"])}</p><p class="st" lang="en">Well-Suited to Pleasure</p><p class="sb" lang="en">The Long Game for Male Sexual Performance</p></div>')
        her = card('her', t['her_k'], t['her_cta'], t['her_b'], t['her_cta'], f'https://pelvispower.org{PRE[l] if l in PW else ""}/women/')
        return top + men_list(l, t, cur) + book + her
    wl = f'{PRE[l]}/women/'
    ml = f'{PRE[l]}/men/'
    tl = f'{PRE[l]}/two/'
    paths = (f'<div class="sw card gen"><p class="sk">{e(t["both_h"])}</p><ul class="paths">'
             f'<li><a href="{wl}">{e(t["w"])}</a></li><li><a href="{ml}">{e(t["m"])}</a></li><li><a href="{tl}">{e(t["t"])}</a></li></ul></div>')
    return paths + card('dfc', t['dfc_k'], 'Dress for Caress', t['dfc_b'], t['dfc_cta'], dfc_pre + '/')


# ---------------------------------------------------------------- wrapping
def wrap(s, aside):
    s = OPEN_RE.sub('', s)
    s = CLOSE_RE.sub('', s)
    i = s.find('<main')
    j = s.rfind('</main>')
    if i < 0 or j < 0:
        return s
    j += len('</main>')
    close = f'<!--sb2--></div><aside class="side" aria-label="Sidebar">{aside}</aside></div><!--/sb2-->'
    return s[:i] + OPEN + s[i:j] + close + s[j:]


def lang_of(rel):
    first = rel.strip('/').split('/')[0]
    return first if first in LANGS and first != 'en' else 'en'


def dfc_page(rel, s):
    if '<main' not in s or rel.endswith('404.html'):
        return s
    l = lang_of(rel)
    m = re.search(r'(?:^|/)day-(\d\d)(?:/|$)', rel)
    cur = int(m.group(1)) if m else 0
    return wrap(s, side_dfc(l, cur))


def pp_page(rel, s):
    if '<main' not in s or rel.endswith('404.html') or 'class="wide chart' in s or 'main class="chart' in s:
        return s
    l = lang_of(rel)
    r = '/' + rel.strip('/')
    if l != 'en':
        r = r[len(PRE[l]):]
    m = re.match(r'/(?:women|men)/day-(\d\d)/', r + '/')
    cur = int(m.group(1)) if m else 0
    if r.startswith('/women'):
        kind = 'women'
    elif r.startswith('/men'):
        kind = 'men'
    else:
        kind = 'gen'
    return wrap(s, side_pp(l, kind, cur))


def run_dfc():
    n = 0
    root = DFC + '/public'
    for p in glob.glob(root + '/**/*.html', recursive=True):
        rel = os.path.relpath(p, root)
        s = read(p)
        t = dfc_page(rel, s)
        if t != s:
            open(p, 'w', encoding='utf-8').write(t)
            n += 1
    # private pages bundle
    pj = DFC + '/private-pages.js'
    txt = read(pj)
    m = re.match(r'(.*?)(\{.*\})(\s*;?\s*[^{}]*)$', txt, re.S)
    # find the JSON object boundaries robustly
    a = txt.index('{')
    b = txt.rindex('}') + 1
    pages = json.loads(txt[a:b])
    c = 0
    for k, v in pages.items():
        nv = dfc_page(k + '/index.html', v)
        if nv != v:
            pages[k] = nv
            c += 1
    open(pj, 'w', encoding='utf-8').write(txt[:a] + json.dumps(pages, ensure_ascii=False) + txt[b:])
    print('dfc static pages', n, 'private pages', c)


def run_pp():
    n = 0
    root = PP + '/public'
    for p in glob.glob(root + '/**/*.html', recursive=True):
        rel = os.path.relpath(p, root)
        s = read(p)
        t = pp_page(rel, s)
        if t != s:
            open(p, 'w', encoding='utf-8').write(t)
            n += 1
    print('pp pages', n)


CSS = r'''
/*sidebar*/
.shell{display:grid;grid-template-columns:minmax(0,__W__px) 300px;gap:32px;justify-content:center;max-width:1200px;margin:0 auto;padding:0 16px}
.shell .col{min-width:0}
.shell main,.shell main.wide{max-width:none;margin:0;padding-left:0;padding-right:0}
.shell .dgrid{grid-template-columns:repeat(3,1fr)}
.shell main.wide:has(>.lvl){display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;align-items:start}
.shell main.wide:has(>.lvl) .lvl{margin:24px 0 8px}
.shell main.wide:has(>.lvl) .lvl h2{font-size:1rem;line-height:1.25;text-align:center;min-height:2.5em;display:flex;align-items:flex-end;justify-content:center}
.shell main.wide:has(>.lvl) .lvl .sub{font-size:12px;line-height:1.3;text-align:center;margin:4px 0 0;min-height:6.6em}
.shell main:has(+main.wide){padding-bottom:0}
.shell main.wide:has(>.lvl) .dgrid{grid-template-columns:1fr;gap:8px}
.shell main.wide:has(>.lvl) .dcard{height:142px;justify-content:flex-start;box-sizing:border-box;overflow:hidden;padding:14px 4px 8px}
.shell main.wide:not(:has(.dcard img)) .dcard{height:116px;justify-content:center;padding:8px 4px;gap:4px}
.shell main.wide:not(:has(.dcard img)) .rec,.shell main.wide:not(:has(.dcard img)) .seal{line-height:26px;font-size:1.3rem}
.shell main.wide:has(>.lvl)>*:not(.lvl){grid-column:1/-1}
@media(max-width:700px){.shell main.wide:has(>.lvl){grid-template-columns:repeat(2,minmax(0,1fr))}.shell main.wide:has(>.lvl) .lvl .sub{min-height:0}}
:root{--side:#fbf3f5}@media(prefers-color-scheme:dark){:root{--side:#261a20}}
.side{align-self:start;margin-top:24px;padding:18px 16px 24px;background:var(--side);border-radius:16px;font:14px/1.4 system-ui,sans-serif}
.side .scov{display:block;margin:0 0 14px}.side .scov img{display:block;width:100%;max-width:210px;height:auto;margin:0 auto;border-radius:6px;box-shadow:0 6px 18px rgba(0,0,0,.28)}
.side .sh{margin:0 0 12px;font:600 17px/1.25 Georgia,serif;color:var(--plum)}
.sw{border:0;border-radius:0;background:transparent;padding:6px 0;margin-bottom:18px}
.sw .sk{margin:0 0 4px;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--gold);font-weight:600}
.sw .st{margin:0 0 6px;font:600 20px/1.2 Georgia,serif;color:var(--plum)}
.sw .sb{margin:0 0 12px;color:var(--ink)}
.sw .sbtn{display:inline-block;padding:8px 14px;border-radius:999px;background:var(--plum);color:var(--bg);text-decoration:none;font-weight:600}
.sw .sbtn:hover{opacity:.88}
.sw .pair{margin:0 0 10px;padding:0 0 0 10px;border-inline-start:3px solid var(--gold)}
.sw .pair span{display:block;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--mute)}
.sw .pair a{color:var(--plum);font-weight:600;text-decoration:none}
.sw .prog{height:6px;border-radius:3px;background:var(--rose);overflow:hidden;margin:0 0 4px}
.sw .prog i{display:block;height:100%;background:var(--gold)}
.sw .pt{margin:0 0 10px;font-size:12px;color:var(--mute)}
.sw.days h2{margin:0 0 8px;font:600 13px system-ui,sans-serif;letter-spacing:.1em;text-transform:uppercase;color:var(--gold)}
.sw.days ol{list-style:none;margin:0 0 6px;padding:0}
.sw.days h3.lv{margin:14px 0 4px;font:600 13px/1.3 Georgia,serif;color:var(--plum)}
.sw.days li{border-top:1px solid var(--rose);display:flex;align-items:baseline;gap:8px}
.sw.days li a,.sw.days li .nolink{flex:1;display:flex;gap:8px;padding:6px 4px;color:var(--ink);text-decoration:none;min-width:0}
.sw.days li b{flex:0 0 1.6em;font-weight:600;color:var(--gold);text-align:end}
.sw.days li a:hover{color:var(--plum)}
.sw.days li.cur{background:var(--rose);border-radius:8px;border-color:transparent}
.sw.days li.cur a{color:var(--plum);font-weight:700}
.sw.days li.lk a{color:var(--mute)}
.sw .lm{font-size:10px;color:var(--mute);white-space:nowrap}
.sw .nolink{color:var(--mute)!important}
.sw .paths{list-style:none;margin:0;padding:0;display:flex;gap:8px;flex-wrap:wrap}
.sw .paths a{display:inline-block;padding:7px 13px;border-radius:999px;border:1px solid var(--plum);color:var(--plum);text-decoration:none;font-weight:600}
@media(max-width:940px){.shell{display:block}.side{margin-top:0}}
html:not([lang=en]) .sw.days li a>span{text-transform:lowercase;display:block}html:not([lang=en]) .sw.days li a>span::first-letter{text-transform:uppercase}
/*fig cutout*/
.hero.art{box-shadow:none;border-radius:0;background:transparent;filter:drop-shadow(0 12px 18px rgba(60,10,30,.28))}
@media print{.side{display:none}.shell{display:block}}
'''


def write_css(path, width):
    s = read(path)
    s = re.sub(r'\n/\*sidebar\*/.*$', '', s, flags=re.S)
    open(path, 'w').write(s.rstrip('\n') + '\n' + CSS.replace('__W__', str(width)))


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    if os.path.exists(DFC + '/public/assets/style.css'):
        write_css(DFC + '/public/assets/style.css', 660)
        run_dfc()
    if os.path.exists(PP + '/public/assets/style.css'):
        write_css(PP + '/public/assets/style.css', 720)
        run_pp()
