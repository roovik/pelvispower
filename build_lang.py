import re,os,html,json,sys,importlib
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import i18n
CODE=sys.argv[1]
cfg=importlib.import_module('langcfg.'+CODE)
T,DOZEN=cfg.T,cfg.DOZEN
PRE='/'+CODE
OUT='/home/claude/pelvispower/public'
E=html.escape
def r(s,**kw):
    for k,v in kw.items(): s=s.replace('{'+k+'}',str(v))
    return s
txt=open(f'/home/claude/lang/PelvisPower-for-Women_{CODE.upper()}.txt').read()
blocks=re.split(r'\n={20,}\n',txt)
parts=[(blocks[i].strip(),blocks[i+1] if i+1<len(blocks) else '') for i in range(1,len(blocks),2)]
def paras(s): return [re.sub(r'\s*\n\s*',' ',p.strip()) for p in re.split(r'\n\s*\n',s.strip()) if p.strip()]
START=[]
for blk in re.split(r'\n\n\n+',parts[0][1].strip()):
    L=blk.strip().split('\n'); START.append((L[0].strip(),'\n'.join(L[1:]).strip()))
LEVELS=[];DAYS={}
for hdr,body in parts[1:]:
    if hdr.startswith('LEVEL'):
        h=hdr.split('\n'); LEVELS.append({'n':int(re.search(r'LEVEL (\d)',h[0]).group(1)),'name':h[0].split(':',1)[1].strip(),'desc':h[1].strip(),'days':[]})
        for db in re.split(r'\n\n\n+(?=DAY \d+\n)',body.strip()):
            db=db.strip()
            if not db.startswith('DAY'): continue
            m=re.match(r"DAY (\d+)\n([^\n]+)\n([^\n]+)\n\n(.*?)\n\nTODAY'S SET\n(.*)$",db,re.S)
            n=int(m.group(1)); rest=m.group(5); extra=''
            if n==30:
                rest,extra=rest.split('\n\n'+T['cert_start'],1); extra=T['cert_start']+extra
            DAYS[n]={'n':n,'title':m.group(2).strip(),'sub':m.group(3).strip(),'read':paras(m.group(4)),'set':rest.strip().split('\n'),'extra':extra.strip(),'level':LEVELS[-1]['n']}
            LEVELS[-1]['days'].append(n)
assert len(DAYS)==30,len(DAYS)
RECESS={6,12,18,24,30}
S={'soft':'the-soft-drop','slow':'the-slow-squeeze','lift':'the-full-lift','flick':'quick-flicks','hold':'long-holds','elev':'the-elevator','rock':'the-rock','bridge':'the-bridge','wink':'the-rosebud-wink','squat':'the-squat-squeeze','pulse':'the-pulse','edge':'the-edge'}
DAYMOVE={1:'slow',2:'soft',3:'lift',4:'flick',5:'hold',7:'elev',8:'rock',9:'bridge',10:'lift',11:'wink',13:'flick',14:'squat',15:'pulse',16:'lift',17:'lift',19:'elev',20:'edge',21:'edge',22:'pulse',23:'soft',25:'hold',26:'flick',27:'elev',28:'lift',29:'hold'}
DZK=['soft','slow','lift','flick','hold','elev','rock','bridge','wink','squat','pulse','edge']
def nav(active=''):
    items=[(PRE+'/women/',T['nav_women']),(PRE+'/men/',T['nav_men']),(PRE+'/two/',T['nav_two']),(PRE+'/women/leaders/',T['nav_leaders'])]
    return ''.join(f'<a href="{u}"{" class=on" if active==u else ""}>{t}</a>' for u,t in items)
PAGES=[]
def page(path,title,desc,body,active='',main_class=''):
    full=PRE+path
    h=f'''<!doctype html><html lang="{CODE}" dir="{T['dir']}" translate="no"><head><meta charset="utf-8"><meta name="google" content="notranslate"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta name="rating" content="adult"><meta name="robots" content="index,follow">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:image" content="https://pelvispower.org/assets/cover.jpg"><meta name="theme-color" content="#4a1a35">
<link rel="icon" href="/assets/pics/the-full-lift.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/style.css">{'' if path=='/404.html' else i18n.alternates(full)}</head><body>
<header class="top"><a class="brand" href="{PRE}/">PelvisPower</a><nav>{nav(active)}</nav>{'' if path=='/404.html' else i18n.switcher(full,CODE)}</header>
<div id="agegate" hidden><div><h2>{T['gate_h']}</h2><p>{T['gate_p']}</p><button id="yes">{T['gate_yes']}</button> <a href="https://www.google.com">{T['gate_leave']}</a></div></div>
<main class="{main_class}">{body}</main>
<footer><p>{T['foot1']}</p><p>{T['foot2']}</p></footer>
<script src="/assets/site.js"></script></body></html>'''
    p=os.path.join(OUT,full.strip('/'),'index.html') if path!='/404.html' else os.path.join(OUT,CODE,'404.html')
    os.makedirs(os.path.dirname(p),exist_ok=True); open(p,'w').write(h)
    PAGES.append(full)
def icon(k,cls='ic'): return f'<img class="{cls}" src="/assets/pics/{S[k]}.svg" alt="" loading="lazy">'
def P(ps): return ''.join(f'<p>{E(p)}</p>' for p in ps)
DM=''.join(f'<a href="{PRE}/women/dozen/#{S[k]}">{icon(k)}<span>{E(n)}</span></a>' for (n,_),k in zip(DOZEN,DZK))
page('/',T['t_home'],T['d_home'],r(cfg.HOME,DOZENMINI=DM),main_class='wide')
def daycard(n):
    d=DAYS[n]; ic=DAYMOVE.get(n)
    im=icon(ic) if ic else ('<span class="seal">★</span>' if n==30 else f'<span class="rec">{T["recess"]}</span>')
    return f'<a class="dcard{" rc" if n in RECESS else ""}" href="{PRE}/women/day-{n:02d}/"><b>{r(T["day"],n=n)}</b>{im}<span>{E(d["sub"] if n in RECESS and n!=30 else d["title"])}</span></a>'
lv=''.join(f'<section class="lvl"><h2>{r(T["level"],n=L["n"],name=E(L["name"]))}</h2><p class="sub">{E(L["desc"])}</p><div class="dgrid">{"".join(daycard(n) for n in L["days"])}</div></section>' for L in LEVELS)
page('/women/',T['t_women'],T['d_women'],T['women_head']+'</main><main class="wide">'+lv,active=PRE+'/women/')
sh=T['start_head']; period_id=''
for k,(h,b) in enumerate(START):
    if h==T['dozen_heading']:
        sh+=f'<h2>{E(h)}</h2>'+T['start_dozen_p']; continue
    if T['period_kw'] in h.lower(): period_id=f'sec-{k}'
    sh+=f'<h2 id="sec-{k}">{E(h)}</h2>'+P(paras(b))
sh+='</article>'+T['start_btn']
page('/women/start-here/',T['t_start'],T['d_start'],sh,active=PRE+'/women/')
dz=T['dozen_head']
for k,((n,dsc),key) in enumerate(zip(DOZEN,DZK),1):
    used=[d for d,m in DAYMOVE.items() if m==key]
    dz+=f'<div class="dz" id="{S[key]}">{icon(key,"ic big")}<h3>{k}. {E(n)}</h3><p>{E(dsc)}</p><p class="used">{T["featured"]} {", ".join(f"<a href={PRE}/women/day-{d:02d}/>{r(T["dayshort"],n=d)}</a>" for d in used)}</p></div>'
dz+='</div>'
page('/women/dozen/',T['t_dozen'],T['d_dozen'],dz,active=PRE+'/women/',main_class='wide')
FC=T['formcheck']
for n,d in DAYS.items():
    ic=DAYMOVE.get(n)
    art=icon(ic,'ic hero2') if ic else ('<div class="sealbig">★</div>' if n==30 else '')
    b=f'{art}<p class="kick">{r(T["day"],n=n)} · {r(T["levelshort"],n=d["level"])}{" · "+T["recess"] if n in RECESS else ""}</p><h1>{E(d["title"])}</h1><p class="sub">{E(d["sub"])}</p><article>'
    for p in d['read']:
        if p.startswith(FC): b+=f'<p class="form"><b>{E(T["formcheck_label"])}</b>{E(p[len(FC):].strip()[:1].upper()+p[len(FC):].strip()[1:])}</p>'
        else: b+=f'<p>{E(p)}</p>'
    b+=r(T['period_box'],href=f'{PRE}/women/start-here/#{period_id}')+f'<div class="set"><h2>{T["set_h"]}</h2><dl>'
    for l in d['set']:
        m=re.match(r'^([^:]{1,60}):\s*(.*)$',l)
        if l.startswith('  '): b+=f'<dd class="sub2">{E(l.strip())}</dd>'
        elif m: b+=f'<dt>{E(m.group(1).strip())}</dt><dd>{E(m.group(2)[:1].upper()+m.group(2)[1:])}</dd>'
        else: b+=f'<dt class="wide">&nbsp;</dt><dd>{E(l)}</dd>'
    b+='</dl></div>'
    if d['extra']:
        lines=d['extra'].split('\n')
        b+=f'<div class="cert"><h2>{E(lines[0])}</h2>'+''.join(f'<p>{E(x)}</p>' for x in lines[1:])+f'<p class="c"><a class="btn alt" href="{PRE}/women/leaders/">{T["become_leader"]}</a></p></div>'
    prv=f'<a href="{PRE}/women/day-{n-1:02d}/">← {r(T["day"],n=n-1)}</a>' if n>1 else f'<a href="{PRE}/women/start-here/">← {T["start_back"]}</a>'
    nxt=f'<a href="{PRE}/women/day-{n+1:02d}/">{r(T["day"],n=n+1)} →</a>' if n<30 else f'<a href="{PRE}/women/leaders/">{T["nav_leaders"]} →</a>'
    b+=f'<div class="pn">{prv}<a href="{PRE}/women/">{T["all_days"]}</a>{nxt}</div>'
    page(f'/women/day-{n:02d}/',r(T['t_day'],n=n,title=d['title']),d['sub'],b,active=PRE+'/women/')
rows=''
for L in LEVELS:
    rows+=f'<h3>{r(T["level"],n=L["n"],name=E(L["name"]))}</h3><div class="cgrid">'
    for n in L['days']:
        ic=DAYMOVE.get(n); im=icon(ic) if ic else ('<span class="seal">★</span>' if n==30 else f'<span class="rec">{T["recess"]}</span>')
        rows+=f'<a class="ccell" href="{PRE}/women/day-{n:02d}/"><span class="box"></span><b>{r(T["day"],n=n)}</b>{im}<span class="t">{E(DAYS[n]["sub"] if n in RECESS and n!=30 else DAYS[n]["title"])}</span></a>'
    rows+='</div>'
page('/women/chart/',T['t_chart'],T['d_chart'],T['chart_head']+rows+T['chart_nums'],active=PRE+'/women/',main_class='wide chart')
page('/women/leaders/',T['t_leaders'],T['d_leaders'],cfg.LEADERS,active=PRE+'/women/leaders/')
page('/men/',T['t_men'],T['d_men'],cfg.MEN,active=PRE+'/men/')
page('/two/',T['t_two'],T['d_two'],cfg.TWO,active=PRE+'/two/')
page('/404.html',T['t_404'],T['t_404'],T['body_404'])
# merge page list for sitemap
f='/home/claude/pelvispower/th_pages.json'
cur=json.load(open(f)) if os.path.exists(f) else []
cur=[p for p in cur if not p.startswith(PRE+'/')]+[p for p in PAGES if not p.endswith('404.html')]
json.dump(cur,open(f,'w'))
print(CODE,len(PAGES),'pages')
