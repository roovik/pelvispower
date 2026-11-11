import re,os,html,shutil,json,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import i18n
SRC='/home/claude/PelvisPower-for-Women_Draft_30-Days.txt'
OUT='/home/claude/pelvispower/public'
E=html.escape
txt=open(SRC).read()
# ---------- parse
blocks=re.split(r'\n={20,}\n',txt)
# blocks: [title, 'START HERE\nsub', body..., 'LEVEL 1...\ndesc', body ...]
start={};levels={};days={};leader=None
i=1
cur=None
parts=[]
while i<len(blocks):
    hdr=blocks[i].strip(); body=blocks[i+1] if i+1<len(blocks) else ''
    parts.append((hdr,body)); i+=2
def paras(s): return [re.sub(r'\s*\n\s*',' ',p.strip()) for p in re.split(r'\n\s*\n',s.strip()) if p.strip()]
# Start Here
hdr,body=parts[0]; assert hdr.startswith('START HERE')
secs=[];name=None;buf=[]
for blk in re.split(r'\n\n\n+',body.strip()):
    lines=blk.strip().split('\n')
    secs.append((lines[0].strip(),'\n'.join(lines[1:]).strip()))
START=secs
LEVELS=[];DAYS={}
for hdr,body in parts[1:]:
    if hdr.startswith('LEVEL'):
        h=hdr.split('\n'); LEVELS.append({'n':int(re.search(r'LEVEL (\d)',h[0]).group(1)),'name':h[0].split(':')[1].strip().title(),'desc':h[1].strip(),'days':[]})
        dayblocks=re.split(r'\n\n\n+(?=DAY \d+\n)',body.strip())
        for db in dayblocks:
            db=db.strip()
            if not db.startswith('DAY'): continue
            m=re.match(r'DAY (\d+)\n([^\n]+)\n([^\n]+)\n\n(.*?)\n\nTODAY\'S SET\n(.*)$',db,re.S)
            n=int(m.group(1)); rest=m.group(5)
            extra=''
            if n==30:
                rest,extra=rest.split('\n\nTHE CERTIFICATE',1); extra='THE CERTIFICATE'+extra
            DAYS[n]={'n':n,'title':m.group(2).strip(),'sub':m.group(3).strip(),'read':paras(m.group(4)),'set':[l for l in rest.strip().split('\n')],'extra':extra.strip(),'level':LEVELS[-1]['n']}
            LEVELS[-1]['days'].append(n)
    elif hdr.startswith('BECOME'):
        LEVELS_LEAD=paras(body)
assert len(DAYS)==30,len(DAYS)
def tc(s):
    small={'a','an','the','and','of','to','in','at','for','with','on'}
    w=s.title().split(); return ' '.join(x if (i==0 or x.lower() not in small) else x.lower() for i,x in enumerate(w))
for d in DAYS.values(): d['title']=tc(d['title'])
RECESS={6,12,18,24,30}
ICON={'Soft Drop':'the-soft-drop','Slow Squeeze':'the-slow-squeeze','Full Lift':'the-full-lift','Quick Flicks':'quick-flicks','Long Holds':'long-holds','Elevator':'the-elevator','Rock':'the-rock','Bridge':'the-bridge','Rosebud Wink':'the-rosebud-wink','Squat Squeeze':'the-squat-squeeze','Pulse':'the-pulse','Edge':'the-edge'}
DAYMOVE={1:'Slow Squeeze',2:'Soft Drop',3:'Full Lift',4:'Quick Flicks',5:'Long Holds',7:'Elevator',8:'Rock',9:'Bridge',10:'Full Lift',11:'Rosebud Wink',13:'Quick Flicks',14:'Squat Squeeze',15:'Pulse',16:'Full Lift',17:'Full Lift',19:'Elevator',20:'Edge',21:'Edge',22:'Pulse',23:'Soft Drop',25:'Long Holds',26:'Quick Flicks',27:'Elevator',28:'Full Lift',29:'Long Holds'}
DOZEN=[('The Soft Drop','Full release with the breath. Every session starts and ends with it.','the-soft-drop'),
('The Slow Squeeze','A gentle squeeze at the front, then a release.','the-slow-squeeze'),
('The Full Lift','Front and back together, drawn up and in.','the-full-lift'),
('Quick Flicks','Fast squeeze, fast let go.','quick-flicks'),
('Long Holds','Hold the lift, keep breathing, release.','long-holds'),
('The Elevator','Lift in steps, one floor at a time, then come down one floor at a time.','the-elevator'),
('The Rock','Pelvic tilts and hip circles.','the-rock'),
('The Bridge','A glute bridge with a lift at the top.','the-bridge'),
('The Rosebud Wink','A small, quick squeeze and release of the back door.','the-rosebud-wink'),
('The Squat Squeeze','A squat or a step with a lift.','the-squat-squeeze'),
('The Pulse','The rhythm of orgasm contractions, practiced on purpose.','the-pulse'),
('The Edge','Light pressure through thin clothes, arousal rising, a hold, a release.','the-edge')]
# ---------- templates
def nav(active=''):
    items=[('/women/','Women'),('/men/','Men'),('/two/','Together'),('/women/leaders/','Leaders')]
    return ''.join(f'<a href="{u}"{" class=on" if active==u else ""}>{t}</a>' for u,t in items)
def page(path,title,desc,body,active='',extra_head='',main_class=''):
    h=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta name="rating" content="adult"><meta name="robots" content="index,follow">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:image" content="https://pelvispower.org/assets/cover.jpg"><meta name="theme-color" content="#4a1a35">
<link rel="icon" href="/assets/pics/the-full-lift.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/style.css">{'' if path=='/404.html' else i18n.alternates(path)}{extra_head}</head><body>
<header class="top"><a class="brand" href="/">PelvisPower</a><nav>{nav(active)}</nav>{'' if path=='/404.html' else i18n.switcher(path,'en')}</header>
<div id="agegate" hidden><div><h2>Adults only</h2><p>This site is for readers 18 and over and talks about sexual pleasure and sexual health.</p><button id="yes">I am 18 or older</button> <a href="https://www.google.com">Leave</a></div></div>
<main class="{main_class}">{body}</main>
<footer><p>PelvisPower, by R. J. Koret. Part of <a href="https://carnal.nowlej.com/">Carnal NOWlej</a>. Companion to <a href="https://dressforcaress.com/">Dress for Caress</a>.</p>
<p>This is a friendly fitness and pleasure guide and is no substitute for medical care. Pain, unexplained bleeding or pelvic pressure deserve a visit with a pelvic floor physical therapist or a doctor.</p></footer>
<script src="/assets/site.js"></script></body></html>'''
    p=os.path.join(OUT,path.strip('/'),'index.html') if path!='/404.html' else os.path.join(OUT,'404.html')
    os.makedirs(os.path.dirname(p),exist_ok=True); open(p,'w').write(h)
    PAGES.append(path)
PAGES=[]
def icon(slug,cls='ic'): return f'<img class="{cls}" src="/assets/pics/{slug}.svg" alt="" loading="lazy">'
def P(ps): return ''.join(f'<p>{E(p)}</p>' for p in ps)
# ---------- Home
home=f'''<section class="herow"><img class="cover" src="/assets/cover.jpg" alt="PelvisPower for Women: a superhero in a yoga outfit with a gold PP medal"><div>
<p class="kick">A 30-day sexercise course</p><h1>PelvisPower</h1><p class="sub">Train the muscles that run your pleasure.</p>
<p>Thirty days. Twelve moves. One happy pelvic floor. A friendly personal trainer for the muscles behind arousal, sensation and orgasm, with bladder confidence and a happier lower back thrown in for good measure.</p>
<p>Clothes stay on, nothing goes inside, and three to ten minutes a day is plenty.</p>
<p><a class="btn" href="/women/start-here/">Start the month</a> <a class="btn alt" href="/women/">See all 30 days</a></p></div></section>
<section class="three"><a class="card" href="/women/"><h2>For Women</h2><p>The full 30-day course, every Day open to read, with the pictograms, a printable chart and your three numbers.</p></a>
<a class="card" href="/men/"><h2>For Men</h2><p>The same month for the muscles men have too. In preparation, with a preview of how it works.</p></a>
<a class="card" href="/two/"><h2>Together</h2><p>Train with a friend, a partner or in a small class. Same Day, same mats, big smiles.</p></a></section>
<section class="band"><h2>The Daily Dozen</h2><p>Twelve moves, learned once and polished all month.</p><div class="dozen mini">{''.join(f'<a href="/women/dozen/#{s}">{icon(s)}<span>{E(n)}</span></a>' for n,_,s in DOZEN)}</div></section>
<section class="two"><div><h2>Why train it?</h2><p>The pelvic floor is a hammock of muscles from your pubic bone to your tailbone. It holds you up, keeps you dry and joins in every orgasm. A few studies link training it with better arousal and stronger orgasms, and the research is young, so think of this as a well-loved experiment.</p></div>
<div><h2>Reward included</h2><p>Pleasure is the reward for showing up, and you set its size. An orgasm is welcome and never required. Many readers pair the month with <a href="https://dressforcaress.com/">Dress for Caress</a>, a month of panties-on joy.</p></div></section>
<section class="band alt"><h2>Share the journey</h2><p>Graduates can lead friends, circles and small classes. The leader course is on the way, and the practitioner pages are already open.</p><p><a class="btn alt" href="/women/leaders/">Leaders and classes</a></p></section>'''
page('/','PelvisPower | A 30-Day Sexercise Course','Train the muscles that run your pleasure. A friendly 30-day course for the pelvic floor, with twelve simple moves.',home,main_class='wide')
# ---------- Women landing
def daycard(n):
    d=DAYS[n]; ic=DAYMOVE.get(n)
    im=icon(ICON[ic]) if ic else ('<span class="seal">★</span>' if n==30 else '<span class="rec">Recess</span>')
    return f'<a class="dcard{" rc" if n in RECESS else ""}" href="/women/day-{n:02d}/"><b>Day {n}</b>{im}<span>{E(d["sub"] if n in RECESS and n!=30 else d["title"])}</span></a>'
lv=''.join(f'<section class="lvl"><h2>Level {L["n"]}: {E(L["name"])}</h2><p class="sub">{E(L["desc"])}</p><div class="dgrid">{"".join(daycard(n) for n in L["days"])}</div></section>' for L in LEVELS)
w=f'''<img class="coversm" src="/assets/cover.jpg" alt="PelvisPower for Women cover"><p class="kick">PelvisPower for Women</p><h1>The 30-Day Course</h1><p class="sub">Every Day is open to read. Take them in order or wander.</p>
<p class="c"><a class="btn" href="/women/start-here/">Start here</a> <a class="btn alt" href="/women/dozen/">The Daily Dozen</a> <a class="btn alt" href="/women/chart/">Printable chart</a></p></main><main class="wide">{lv}'''
page('/women/','PelvisPower for Women | 30-Day Course','All 30 Days of PelvisPower for Women: five Levels, twelve moves, a graduation certificate.',w,active='/women/')
# ---------- Start here
sh='<p class="kick">PelvisPower for Women</p><h1>Start Here</h1><p class="sub">What this book does for you, and how the month works</p><article>'
for h,b in START:
    if h=='THE DAILY DOZEN':
        sh+=f'<h2>{tc(h)}</h2><p>Twelve moves, learned once and polished all month. <a href="/women/dozen/">See them with pictograms.</a></p>'; continue
    sh+=f'<h2 id="{re.sub(r"[^a-z]+","-",h.lower()).strip("-")}">{tc(h)}</h2>'+P(paras(b))
sh+='</article><p class="c"><a class="btn" href="/women/day-01/">Begin with Day 1</a></p>'
page('/women/start-here/','Start Here | PelvisPower for Women','What the course does for you, how the month works, and how to train alone, in pairs or in a class.',sh,active='/women/')
# ---------- Dozen
dz='<p class="kick">The moves</p><h1>The Daily Dozen</h1><p class="sub">Twelve moves. Every Day uses some of them.</p><div class="dozen">'
for k,(n,dsc,s) in enumerate(DOZEN,1):
    used=[d for d,m in DAYMOVE.items() if ICON[m]==s]
    dz+=f'<div class="dz" id="{s}">{icon(s,"ic big")}<h3>{k}. {E(n)}</h3><p>{E(dsc)}</p><p class="used">Featured on {", ".join(f"<a href=/women/day-{d:02d}/>Day {d}</a>" for d in used)}</p></div>'
dz+='</div>'
page('/women/dozen/','The Daily Dozen | PelvisPower for Women','Twelve simple pelvic floor moves, each with a pictogram.',dz,active='/women/',main_class='wide')
# ---------- Days
for n,d in DAYS.items():
    ic=DAYMOVE.get(n)
    art=icon(ICON[ic],'ic hero2') if ic else ('<div class="sealbig">★</div>' if n==30 else '')
    b=f'{art}<p class="kick">Day {n} · Level {d["level"]}{" · Recess" if n in RECESS else ""}</p><h1>{E(d["title"])}</h1><p class="sub">{E(d["sub"])}</p><article>'
    for p in d['read']:
        if p.startswith('Form check:'): b+=f'<p class="form"><b>Form check</b>{E(p[11:].strip().capitalize() if False else (p[11:].strip()[0].upper()+p[11:].strip()[1:]))}</p>'
        else: b+=f'<p>{E(p)}</p>'
    b+='</article><p class="period"><b>On your period?</b> Power through, go gentle, swap in a Recess or pause. It is your call. <a href="/women/start-here/#during-your-period">See the options.</a></p><div class="set"><h2>Today\'s Set</h2><dl>'
    extra=''
    for l in d['set']:
        m=re.match(r'^(Time|Position|Garment|Warm-up|Cool-down|Pleasure Dial|Variation|Move \d+, [^:]+|Test \d+, [^:]+|The Recess|The routine|The three numbers, each with a Soft Drop between|THE LOG):\s*(.*)$',l)
        if m: b+=f'<dt>{E(m.group(1).replace("THE LOG","The Log"))}</dt><dd>{E(m.group(2)[:1].upper()+m.group(2)[1:])}</dd>'
        elif l.startswith('  '): b+=f'<dd class="sub2">{E(l.strip())}</dd>'
        else: b+=f'<dt class="wide">&nbsp;</dt><dd>{E(l)}</dd>'
    b+='</dl></div>'
    if d['extra']:
        lines=d['extra'].split('\n')
        b+='<div class="cert"><h2>The Certificate of Pelvic Excellence</h2>'+''.join(f'<p>{E(x)}</p>' for x in lines[1:])+'<p class="c"><a class="btn alt" href="/women/leaders/">Become a leader</a></p></div>'
    prv=f'<a href="/women/day-{n-1:02d}/">← Day {n-1}</a>' if n>1 else '<a href="/women/start-here/">← Start Here</a>'
    nxt=f'<a href="/women/day-{n+1:02d}/">Day {n+1} →</a>' if n<30 else '<a href="/women/leaders/">Leaders →</a>'
    b+=f'<div class="pn">{prv}<a href="/women/">All Days</a>{nxt}</div>'
    page(f'/women/day-{n:02d}/',f'Day {n}: {d["title"]} | PelvisPower for Women',d['sub'],b,active='/women/')
# ---------- Chart (printable)
rows=''
for L in LEVELS:
    rows+=f'<h3>Level {L["n"]}: {E(L["name"])}</h3><div class="cgrid">'
    for n in L['days']:
        ic=DAYMOVE.get(n); im=icon(ICON[ic]) if ic else ('<span class="seal">★</span>' if n==30 else '<span class="rec">Recess</span>')
        rows+=f'<a class="ccell" href="/women/day-{n:02d}/"><span class="box"></span><b>Day {n}</b>{im}<span class="t">{E(DAYS[n]["sub"] if n in RECESS and n!=30 else DAYS[n]["title"])}</span></a>'
    rows+='</div>'
ch=f'''<p class="kick">Print me</p><h1>Your Month at a Glance</h1><p class="sub">Tick each Day as you finish. Write your three numbers below.</p>
<p class="c noprint"><button class="btn" onclick="window.print()">Print this page</button></p>{rows}
<h3>The Three Numbers</h3><table class="nums"><tr><th></th><th>Day 1 (before)</th><th>Day 29 (after)</th></tr><tr><th>Longest hold, in seconds (stop at 30)</th><td></td><td></td></tr><tr><th>Flicks in 30 seconds</th><td></td><td></td></tr><tr><th>Steps up (stop at 10)</th><td></td><td></td></tr></table>'''
page('/women/chart/','Month at a Glance | PelvisPower for Women','A printable 30-day checklist and the three-numbers tracker.',ch,active='/women/',main_class='wide chart')
# ---------- Leaders
LEAD_LEVELS={1:'Foundations. Great for a first class. Teach finding the muscles, the Soft Drop and the Full Lift, and keep the mood playful. Recess day is homework.',
2:'Endurance. Add Long Holds and the Elevator. Count aloud together and praise steady beats over long ones.',
3:'Power. Quick Flicks, the Squat Squeeze and the Pulse. Standing work suits the room, so use the wall and a chair.',
4:'Mastery. Run the Combo and the breath work in class. The Edge days are personal and belong at home, so give those out as optional take-home notes.',
5:'Graduation. The Speed Round, Top Floor, the Full Routine and the Final Exam all work in a group. Finish with the diploma and a toast.'}
ld=f'''<p class="kick">For practitioners</p><h1>Lead the Journey</h1><p class="sub">Pairs, circles and small classes</p><article>
<p>PelvisPower works alone, in pairs and in a small class. This page is the leader's corner, and it is open to every reader.</p>
<h2>Ground rules for every group</h2>
<p>Clothes stay on, voices stay low and anyone can skip any move. Nobody touches anybody. Each person's numbers are private unless she chooses to share them.</p>
<p>Keep the tone of a friendly personal trainer. Facts are clear, jokes are welcome and nothing is clinical.</p>
<h2>A class in four parts</h2>
<ul><li><b>Arrive (5 minutes).</b> Settle on mats, take five slow breaths together and finish with a Soft Drop.</li>
<li><b>Coach (5 minutes).</b> Read the Day's coaching note aloud, with the Form check.</li>
<li><b>Train (15 to 25 minutes).</b> Call Today's Set. Count aloud, keep the pace and watch the form.</li>
<li><b>Close (5 minutes).</b> A long Soft Drop, one line each on how it felt, and a cheer.</li></ul>
<h2>Level by level</h2><ul>{''.join(f'<li><b>Level {k}.</b> {E(v)}</li>' for k,v in LEAD_LEVELS.items())}</ul>
<h2>Pairs</h2><p>Two friends can follow the same Day side by side or on a video call. One counts while the other trains, then they swap. Your buddy can use PelvisPower for Women or PelvisPower for Men.</p>
<h2>Group size and space</h2><p>Four to twelve people works well. You need a mat each, a few cushions and a wall. Chairs help for standing and sitting variations.</p>
<h2>When to point someone onward</h2><p>Pain with sex, bleeding that cannot be explained, or a feeling of pressure or heaviness in the pelvis are signs to see a pelvic floor physical therapist or a doctor. Pregnant, postpartum or recovering from surgery? Suggest a check-in first. A leader encourages and never diagnoses.</p>
<div class="set"><h2>The PelvisPower Leader Course</h2><p>A certification course is on the way. It teaches you to guide groups and pairs through the month, keep every session safe and comfortable, and know when to refer. It suits warm, curious people, and no medical background is needed.</p>
<p>Leaders receive session plans for every Level, an opening script, tips for mixed abilities and a certificate.</p>
<form class="wait" onsubmit="return false"><label>Join the waiting list<input type="email" placeholder="you@example.com" disabled></label><button class="btn" disabled>Opening soon</button></form></div></article>'''
page('/women/leaders/','Leaders and Classes | PelvisPower','How to lead PelvisPower in pairs, circles and small classes, plus the coming leader certification.',ld,active='/women/leaders/')
# ---------- Men
mn='''<img class="coversm" src="/assets/pics/the-full-lift.svg" alt="" style="max-width:120px;background:#fff;border-radius:12px;padding:8px"><p class="kick">In preparation</p><h1>PelvisPower for Men</h1><p class="sub">The same month, for the muscles men have too</p><article>
<p>Men have a pelvic floor, and it does a great deal. It supports sexual function, helps with control and stamina, and takes part in orgasm. It can be trained, and the training is friendly and discreet.</p>
<p>The month follows the same plan as the women's course. Thirty days, five Levels, twelve moves and a graduation. The moves differ in small ways and the spirit is the same.</p>
<h2>What to expect</h2><p>Three to ten minutes a day, in thin comfortable clothes. Light, funny and never clinical, with a Pleasure Dial from 1 to 5 and a reward that you set yourself.</p>
<h2>Train with her</h2><p>Many couples train in parallel, one in each book, and compare numbers over breakfast. See <a href="/two/">Together</a>.</p>
<h2>The longer game</h2><p>A companion book, <i>Well-Suited for Pleasure: The Long Game for Hands-Free Male Orgasm</i>, is also on the way, with a tree for every Day.</p>
<p class="c"><a class="btn alt" href="/women/">Meanwhile, see the women's course</a></p></article>'''
page('/men/','PelvisPower for Men | In Preparation','The 30-day pelvic floor course for men, in preparation.',mn,active='/men/')
# ---------- Together
tg='''<p class="kick">Better together</p><h1>Train Together</h1><p class="sub">Same Day, same mats, big smiles</p><article>
<h2>Side by side</h2><p>You and a partner train the same Day, one in PelvisPower for Women and one in PelvisPower for Men. Count each other's reps, cheer, and compare numbers over coffee.</p>
<h2>With a friend</h2><p>A friend, a sister or a training buddy can follow the same Day in the same room or on a video call. Everyone stays clothed and in their own space.</p>
<h2>In a small class</h2><p>Four to twelve people on mats, with a leader who reads the coaching note and calls the set. See the <a href="/women/leaders/">leader's corner</a> for the plan.</p>
<h2>With Dress for Caress</h2><p>PelvisPower is the workout and <a href="https://dressforcaress.com/">Dress for Caress</a> is the reward. Train first, then enjoy that Day of Dress for Caress, or finish the PelvisPower month and then begin it, or mix the two. Any rhythm that makes you smile is the right one.</p></article>'''
page('/two/','Train Together | PelvisPower','Train with a partner, a friend or a small class, and pair PelvisPower with Dress for Caress.',tg,active='/two/')
page('/404.html','Not found | PelvisPower','Page not found','<h1>Not found</h1><p class="sub">That page took a Soft Drop.</p><p class="c"><a class="btn" href="/">Home</a></p>')
# sitemap
TH=json.load(open('/home/claude/pelvispower/th_pages.json')) if os.path.exists('/home/claude/pelvispower/th_pages.json') else []
sm='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>https://pelvispower.org{p}</loc></url>' for p in PAGES+TH if not p.endswith('404.html'))+'</urlset>'
open(OUT+'/sitemap.xml','w').write(sm)
open(OUT+'/robots.txt','w').write('User-agent: *\nAllow: /\nSitemap: https://pelvispower.org/sitemap.xml\n')
print(len(PAGES),'pages')
