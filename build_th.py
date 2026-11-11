import re,os,html,json,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import i18n
SRC='/home/claude/PelvisPower-for-Women_TH.txt'
OUT='/home/claude/pelvispower/public'
E=html.escape
txt=open(SRC).read()
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
                rest,extra=rest.split('\n\nประกาศนียบัตร',1); extra='ประกาศนียบัตร'+extra
            DAYS[n]={'n':n,'title':m.group(2).strip(),'sub':m.group(3).strip(),'read':paras(m.group(4)),'set':rest.strip().split('\n'),'extra':extra.strip(),'level':LEVELS[-1]['n']}
            LEVELS[-1]['days'].append(n)
assert len(DAYS)==30,len(DAYS)
RECESS={6,12,18,24,30}
S={'soft':'the-soft-drop','slow':'the-slow-squeeze','lift':'the-full-lift','flick':'quick-flicks','hold':'long-holds','elev':'the-elevator','rock':'the-rock','bridge':'the-bridge','wink':'the-rosebud-wink','squat':'the-squat-squeeze','pulse':'the-pulse','edge':'the-edge'}
DAYMOVE={1:'slow',2:'soft',3:'lift',4:'flick',5:'hold',7:'elev',8:'rock',9:'bridge',10:'lift',11:'wink',13:'flick',14:'squat',15:'pulse',16:'lift',17:'lift',19:'elev',20:'edge',21:'edge',22:'pulse',23:'soft',25:'hold',26:'flick',27:'elev',28:'lift',29:'hold'}
DOZEN=[('ปล่อยนุ่ม','ผ่อนคลายเต็มที่ไปกับลมหายใจ ทุกครั้งที่ฝึกจะเริ่มและจบด้วยท่านี้','soft'),
('บีบช้า','บีบเบาๆ ที่ด้านหน้า แล้วปล่อย','slow'),
('ยกเต็มที่','ด้านหน้าและด้านหลังยกไปพร้อมกัน ดึงขึ้นและเข้าด้านใน','lift'),
('ดีดเร็ว','บีบเร็ว ปล่อยเร็ว','flick'),
('ค้างนาน','ยกค้างไว้ หายใจต่อไป แล้วปล่อย','hold'),
('ลิฟต์','ยกทีละชั้น แล้วลงทีละชั้น','elev'),
('โยกสะโพก','เอียงเชิงกรานและหมุนสะโพก','rock'),
('สะพาน','ยกก้นแบบกลูทบริดจ์ พร้อมยกกล้ามเนื้อที่ด้านบน','bridge'),
('กุหลาบขยิบตา','บีบแล้วปล่อยประตูหลังเบาๆ และเร็ว','wink'),
('สควอตบีบ','นั่งยองหรือก้าวขาพร้อมยกกล้ามเนื้อ','squat'),
('จังหวะพัลส์','จังหวะการหดตัวของจุดสุดยอด ฝึกอย่างตั้งใจ','pulse'),
('ขอบความสุข','สัมผัสเบาๆ ผ่านเสื้อผ้าบาง อารมณ์ค่อยๆ ขึ้น หยุดค้าง แล้วปล่อย','edge')]
PRE='/th'
def nav(active=''):
    items=[('/th/women/','ผู้หญิง'),('/th/men/','ผู้ชาย'),('/th/two/','ฝึกด้วยกัน'),('/th/women/leaders/','ผู้นำ')]
    return ''.join(f'<a href="{u}"{" class=on" if active==u else ""}>{t}</a>' for u,t in items)
PAGES=[]
def page(path,title,desc,body,active='',main_class=''):
    full=PRE+path
    h=f'''<!doctype html><html lang="th" translate="no"><head><meta charset="utf-8"><meta name="google" content="notranslate"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta name="rating" content="adult"><meta name="robots" content="index,follow">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:image" content="https://pelvispower.org/assets/cover.jpg"><meta name="theme-color" content="#4a1a35">
<link rel="icon" href="/assets/pics/the-full-lift.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/style.css">{'' if path=='/404.html' else i18n.alternates(full)}</head><body>
<header class="top"><a class="brand" href="/th/">PelvisPower</a><nav>{nav(active)}</nav>{'' if path=='/404.html' else i18n.switcher(full,'th')}</header>
<div id="agegate" hidden><div><h2>สำหรับผู้ใหญ่เท่านั้น</h2><p>เว็บไซต์นี้สำหรับผู้อ่านอายุ 18 ปีขึ้นไป และพูดถึงความสุขทางเพศและสุขภาพทางเพศ</p><button id="yes">ฉันอายุ 18 ปีขึ้นไป</button> <a href="https://www.google.com">ออกจากเว็บไซต์</a></div></div>
<main class="{main_class}">{body}</main>
<footer><p>PelvisPower โดย R. J. Koret ส่วนหนึ่งของ <a href="https://carnal.nowlej.com/">Carnal NOWlej</a> เล่มคู่กับ <a href="https://dressforcaress.com/">Dress for Caress</a></p>
<p>นี่คือคู่มือออกกำลังกายและความสุขที่เป็นมิตร ไม่ใช่สิ่งทดแทนการดูแลทางการแพทย์ หากมีอาการปวด เลือดออกโดยไม่ทราบสาเหตุ หรือรู้สึกถึงแรงกดในอุ้งเชิงกราน ควรพบนักกายภาพบำบัดอุ้งเชิงกรานหรือแพทย์</p></footer>
<script src="/assets/site.js"></script></body></html>'''
    p=os.path.join(OUT,full.strip('/'),'index.html') if path!='/404.html' else os.path.join(OUT,'th','404.html')
    os.makedirs(os.path.dirname(p),exist_ok=True); open(p,'w').write(h)
    PAGES.append(full)
def icon(slug,cls='ic'): return f'<img class="{cls}" src="/assets/pics/{S[slug]}.svg" alt="" loading="lazy">'
def P(ps): return ''.join(f'<p>{E(p)}</p>' for p in ps)
def W(u): return f'/th{u}'
# Home
home=f'''<section class="herow"><img class="cover" src="/assets/cover.jpg" alt="PelvisPower for Women: ซูเปอร์ฮีโร่ในชุดโยคะ พร้อมเหรียญ PP สีทอง"><div>
<p class="kick">หลักสูตรเซ็กเซอร์ไซส์ 30 วัน</p><h1>PelvisPower</h1><p class="sub">ฝึกกล้ามเนื้อที่ควบคุมความสุขของคุณ</p>
<p>สามสิบวัน สิบสองท่า พื้นเชิงกรานที่มีความสุขหนึ่งเดียว เทรนเนอร์ส่วนตัวแสนเป็นมิตรสำหรับกล้ามเนื้อที่อยู่เบื้องหลังอารมณ์ ความรู้สึก และจุดสุดยอด พร้อมความมั่นใจเรื่องกระเพาะปัสสาวะและหลังส่วนล่างที่สบายขึ้นเป็นของแถม</p>
<p>ใส่เสื้อผ้าอยู่ ไม่มีอะไรเข้าไปในร่างกาย และวันละสามถึงสิบนาทีก็เพียงพอ</p>
<p><a class="btn" href="/th/women/start-here/">เริ่มเดือนนี้</a> <a class="btn alt" href="/th/women/">ดูครบทั้ง 30 วัน</a></p></div></section>
<section class="three"><a class="card" href="/th/women/"><h2>สำหรับผู้หญิง</h2><p>หลักสูตร 30 วันเต็ม เปิดอ่านได้ทุกวัน พร้อมภาพสัญลักษณ์ ตารางพิมพ์ และตัวเลขสามตัวของคุณ</p></a>
<a class="card" href="/th/men/"><h2>สำหรับผู้ชาย</h2><p>หนึ่งเดือนแบบเดียวกันสำหรับกล้ามเนื้อที่ผู้ชายก็มี อยู่ระหว่างเตรียมการ พร้อมตัวอย่างว่าทำงานอย่างไร</p></a>
<a class="card" href="/th/two/"><h2>ฝึกด้วยกัน</h2><p>ฝึกกับเพื่อน คู่รัก หรือในคลาสเล็กๆ วันเดียวกัน เสื่อเคียงกัน รอยยิ้มกว้างๆ</p></a></section>
<section class="band"><h2>สิบสองท่าประจำวัน</h2><p>เรียนครั้งเดียว แล้วฝึกให้เก่งตลอดเดือน</p><div class="dozen mini">{''.join(f'<a href="/th/women/dozen/#{S[s]}">{icon(s)}<span>{E(n)}</span></a>' for n,_,s in DOZEN)}</div></section>
<section class="two"><div><h2>ทำไมต้องฝึก</h2><p>พื้นเชิงกรานคือเปลญวนของกล้ามเนื้อจากกระดูกหัวหน่าวถึงก้นกบ มันพยุงร่างกาย ช่วยให้แห้งสบาย และร่วมอยู่ในทุกจุดสุดยอด มีงานศึกษาบางชิ้นที่เชื่อมโยงการฝึกกับอารมณ์ที่ดีขึ้นและจุดสุดยอดที่แรงขึ้น และงานวิจัยยังใหม่ ลองมองว่านี่คือการทดลองที่น่ารัก</p></div>
<div><h2>มีรางวัลให้ด้วย</h2><p>ความสุขคือรางวัลของการมาฝึก และคุณกำหนดขนาดของมัน จุดสุดยอดยินดีต้อนรับและไม่เคยบังคับ ผู้อ่านหลายคนจับคู่หนึ่งเดือนนี้กับ <a href="https://dressforcaress.com/">Dress for Caress</a> หนึ่งเดือนแห่งความสุขใต้กางเกงใน</p></div></section>
<section class="band alt"><h2>แบ่งปันการเดินทาง</h2><p>ผู้จบหลักสูตรนำเพื่อน กลุ่ม และคลาสเล็กๆ ได้ หลักสูตรผู้นำกำลังจะมา และหน้าสำหรับผู้นำเปิดแล้ว</p><p><a class="btn alt" href="/th/women/leaders/">ผู้นำและคลาส</a></p></section>'''
page('/','PelvisPower | หลักสูตรเซ็กเซอร์ไซส์ 30 วัน','ฝึกกล้ามเนื้อที่ควบคุมความสุขของคุณ หลักสูตร 30 วันแสนเป็นมิตรสำหรับพื้นเชิงกราน พร้อมสิบสองท่าง่ายๆ',home,main_class='wide')
# Women landing
def daycard(n):
    d=DAYS[n]; ic=DAYMOVE.get(n)
    im=icon(ic) if ic else ('<span class="seal">★</span>' if n==30 else '<span class="rec">พักเบรก</span>')
    return f'<a class="dcard{" rc" if n in RECESS else ""}" href="/th/women/day-{n:02d}/"><b>วันที่ {n}</b>{im}<span>{E(d["sub"] if n in RECESS and n!=30 else d["title"])}</span></a>'
lv=''.join(f'<section class="lvl"><h2>ระดับ {L["n"]}: {E(L["name"])}</h2><p class="sub">{E(L["desc"])}</p><div class="dgrid">{"".join(daycard(n) for n in L["days"])}</div></section>' for L in LEVELS)
w=f'''<img class="coversm" src="/assets/cover.jpg" alt="ปก PelvisPower for Women"><p class="kick">PelvisPower สำหรับผู้หญิง</p><h1>หลักสูตร 30 วัน</h1><p class="sub">เปิดอ่านได้ทุกวัน อ่านตามลำดับหรือเดินดูก่อนก็ได้</p>
<p class="c"><a class="btn" href="/th/women/start-here/">เริ่มที่นี่</a> <a class="btn alt" href="/th/women/dozen/">สิบสองท่าประจำวัน</a> <a class="btn alt" href="/th/women/chart/">ตารางพิมพ์</a></p></main><main class="wide">{lv}'''
page('/women/','PelvisPower สำหรับผู้หญิง | หลักสูตร 30 วัน','ครบทั้ง 30 วันของ PelvisPower สำหรับผู้หญิง ห้าระดับ สิบสองท่า และประกาศนียบัตร',w,active='/th/women/')
# Start here
sh='<p class="kick">PelvisPower สำหรับผู้หญิง</p><h1>เริ่มที่นี่</h1><p class="sub">หนังสือเล่มนี้ให้อะไรกับคุณ และเดือนนี้ทำงานอย่างไร</p><article>'
period_id=None
for k,(h,b) in enumerate(START):
    if h=='สิบสองท่าประจำวัน':
        sh+=f'<h2>{E(h)}</h2><p>สิบสองท่า เรียนครั้งเดียว แล้วฝึกให้เก่งตลอดเดือน <a href="/th/women/dozen/">ดูพร้อมภาพสัญลักษณ์</a></p>'; continue
    if 'ประจำเดือน' in h: period_id=f'sec-{k}'
    sh+=f'<h2 id="sec-{k}">{E(h)}</h2>'+P(paras(b))
sh+='</article><p class="c"><a class="btn" href="/th/women/day-01/">เริ่มวันที่ 1</a></p>'
page('/women/start-here/','เริ่มที่นี่ | PelvisPower สำหรับผู้หญิง','หลักสูตรให้อะไรกับคุณ เดือนนี้ทำงานอย่างไร และฝึกคนเดียว เป็นคู่ หรือเป็นคลาสอย่างไร',sh,active='/th/women/')
# Dozen
dz='<p class="kick">ท่าทั้งหมด</p><h1>สิบสองท่าประจำวัน</h1><p class="sub">สิบสองท่า ทุกวันใช้บางท่าในนี้</p><div class="dozen">'
for k,(n,dsc,s) in enumerate(DOZEN,1):
    used=[d for d,m in DAYMOVE.items() if m==s]
    dz+=f'<div class="dz" id="{S[s]}">{icon(s,"ic big")}<h3>{k}. {E(n)}</h3><p>{E(dsc)}</p><p class="used">ฝึกในวันที่ {", ".join(f"<a href=/th/women/day-{d:02d}/>{d}</a>" for d in used)}</p></div>'
dz+='</div>'
page('/women/dozen/','สิบสองท่าประจำวัน | PelvisPower สำหรับผู้หญิง','สิบสองท่าบริหารพื้นเชิงกรานแสนง่าย พร้อมภาพสัญลักษณ์ทุกท่า',dz,active='/th/women/',main_class='wide')
# Days
for n,d in DAYS.items():
    ic=DAYMOVE.get(n)
    art=icon(ic,'ic hero2') if ic else ('<div class="sealbig">★</div>' if n==30 else '')
    b=f'{art}<p class="kick">วันที่ {n} · ระดับ {d["level"]}{" · พักเบรก" if n in RECESS else ""}</p><h1>{E(d["title"])}</h1><p class="sub">{E(d["sub"])}</p><article>'
    for p in d['read']:
        if p.startswith('เช็กท่า:'): b+=f'<p class="form"><b>เช็กท่า</b>{E(p[len("เช็กท่า:"):].strip())}</p>'
        else: b+=f'<p>{E(p)}</p>'
    b+=f'</article><p class="period"><b>อยู่ในช่วงมีประจำเดือน?</b> ฝึกต่อได้เลย ฝึกเบาๆ สลับเป็นวันพักเบรก หรือหยุดพักก็ได้ คุณเป็นคนตัดสินใจ <a href="/th/women/start-here/#{period_id}">ดูตัวเลือก</a></p><div class="set"><h2>ชุดฝึกวันนี้</h2><dl>'
    for l in d['set']:
        m=re.match(r'^([^:]{1,60}):\s*(.*)$',l)
        if l.startswith('  '): b+=f'<dd class="sub2">{E(l.strip())}</dd>'
        elif m: b+=f'<dt>{E(m.group(1))}</dt><dd>{E(m.group(2))}</dd>'
        else: b+=f'<dt class="wide">&nbsp;</dt><dd>{E(l)}</dd>'
    b+='</dl></div>'
    if d['extra']:
        lines=d['extra'].split('\n')
        b+=f'<div class="cert"><h2>{E(lines[0])}</h2>'+''.join(f'<p>{E(x)}</p>' for x in lines[1:])+'<p class="c"><a class="btn alt" href="/th/women/leaders/">เป็นผู้นำ</a></p></div>'
    prv=f'<a href="/th/women/day-{n-1:02d}/">← วันที่ {n-1}</a>' if n>1 else '<a href="/th/women/start-here/">← เริ่มที่นี่</a>'
    nxt=f'<a href="/th/women/day-{n+1:02d}/">วันที่ {n+1} →</a>' if n<30 else '<a href="/th/women/leaders/">ผู้นำ →</a>'
    b+=f'<div class="pn">{prv}<a href="/th/women/">ทุกวัน</a>{nxt}</div>'
    page(f'/women/day-{n:02d}/',f'วันที่ {n}: {d["title"]} | PelvisPower',d['sub'],b,active='/th/women/')
# Chart
rows=''
for L in LEVELS:
    rows+=f'<h3>ระดับ {L["n"]}: {E(L["name"])}</h3><div class="cgrid">'
    for n in L['days']:
        ic=DAYMOVE.get(n); im=icon(ic) if ic else ('<span class="seal">★</span>' if n==30 else '<span class="rec">พักเบรก</span>')
        rows+=f'<a class="ccell" href="/th/women/day-{n:02d}/"><span class="box"></span><b>วันที่ {n}</b>{im}<span class="t">{E(DAYS[n]["sub"] if n in RECESS and n!=30 else DAYS[n]["title"])}</span></a>'
    rows+='</div>'
ch=f'''<p class="kick">พิมพ์ได้</p><h1>หนึ่งเดือนในแผ่นเดียว</h1><p class="sub">ติ๊กแต่ละวันเมื่อทำเสร็จ และเขียนตัวเลขสามตัวด้านล่าง</p>
<p class="c noprint"><button class="btn" onclick="window.print()">พิมพ์หน้านี้</button></p>{rows}
<h3>ตัวเลขสามตัว</h3><table class="nums"><tr><th></th><th>วันที่ 1 (ก่อน)</th><th>วันที่ 29 (หลัง)</th></tr><tr><th>ค้างนานที่สุด เป็นวินาที (หยุดที่ 30)</th><td></td><td></td></tr><tr><th>จำนวนดีดใน 30 วินาที</th><td></td><td></td></tr><tr><th>ขั้นที่ยกขึ้น (หยุดที่ 10)</th><td></td><td></td></tr></table>'''
page('/women/chart/','หนึ่งเดือนในแผ่นเดียว | PelvisPower','ตารางเช็กลิสต์ 30 วันแบบพิมพ์ได้ และตัวติดตามตัวเลขสามตัว',ch,active='/th/women/',main_class='wide chart')
# Leaders
LL={1:'รากฐาน เหมาะกับคลาสแรก สอนการหากล้ามเนื้อ ปล่อยนุ่ม และยกเต็มที่ และรักษาบรรยากาศให้สนุก วันพักเบรกเป็นการบ้าน',
2:'ความอึด เพิ่มค้างนานและลิฟต์ นับออกเสียงด้วยกัน และชมจังหวะที่นิ่งมากกว่าการค้างที่ยาว',
3:'พลัง ดีดเร็ว สควอตบีบ และจังหวะพัลส์ งานท่ายืนเหมาะกับห้อง ใช้กำแพงและเก้าอี้',
4:'ความเชี่ยวชาญ ทำคอมโบและการหายใจในคลาส วันขอบความสุขเป็นเรื่องส่วนตัวและเหมาะกับที่บ้าน ให้เป็นบันทึกกลับไปทำแบบไม่บังคับ',
5:'พิธีจบหลักสูตร รอบความเร็ว ชั้นบนสุด ชุดเต็ม และสอบปลายภาคใช้ในกลุ่มได้ทั้งหมด จบด้วยประกาศนียบัตรและการชนแก้ว'}
ld=f'''<p class="kick">สำหรับผู้นำ</p><h1>นำการเดินทาง</h1><p class="sub">คู่ กลุ่มเพื่อน และคลาสเล็กๆ</p><article>
<p>PelvisPower ใช้ได้ทั้งคนเดียว เป็นคู่ และในคลาสเล็กๆ หน้านี้คือมุมของผู้นำ และเปิดให้ผู้อ่านทุกคน</p>
<h2>กฎพื้นฐานของทุกกลุ่ม</h2>
<p>ใส่เสื้อผ้าอยู่ พูดเบาๆ และใครจะข้ามท่าไหนก็ได้ ไม่มีใครแตะต้องใคร ตัวเลขของแต่ละคนเป็นส่วนตัว เว้นแต่เธอเลือกที่จะแบ่งปัน</p>
<p>รักษาน้ำเสียงแบบเทรนเนอร์ส่วนตัวที่เป็นมิตร ข้อเท็จจริงชัดเจน มุกตลกยินดีต้อนรับ และไม่มีอะไรเป็นทางคลินิก</p>
<h2>หนึ่งคลาสมีสี่ช่วง</h2>
<ul><li><b>มาถึง (5 นาที)</b> นั่งบนเสื่อ หายใจช้าห้าครั้งด้วยกัน และจบด้วยปล่อยนุ่ม</li>
<li><b>โค้ช (5 นาที)</b> อ่านบทโค้ชของวันนั้นออกเสียง รวมถึงเช็กท่า</li>
<li><b>ฝึก (15 ถึง 25 นาที)</b> เรียกชุดฝึกวันนี้ นับออกเสียง รักษาจังหวะ และดูท่า</li>
<li><b>ปิดคลาส (5 นาที)</b> ปล่อยนุ่มยาวๆ คนละหนึ่งบรรทัดว่ารู้สึกอย่างไร และเสียงเชียร์</li></ul>
<h2>ทีละระดับ</h2><ul>{''.join(f'<li><b>ระดับ {k}</b> {E(v)}</li>' for k,v in LL.items())}</ul>
<h2>เป็นคู่</h2><p>เพื่อนสองคนทำวันเดียวกันเคียงข้างกันหรือผ่านวิดีโอคอล คนหนึ่งนับขณะอีกคนฝึก แล้วสลับกัน เพื่อนฝึกของคุณใช้ PelvisPower สำหรับผู้หญิงหรือสำหรับผู้ชายก็ได้</p>
<h2>ขนาดกลุ่มและพื้นที่</h2><p>สี่ถึงสิบสองคนกำลังดี ต้องมีเสื่อคนละผืน หมอนสองสามใบ และกำแพงหนึ่งด้าน เก้าอี้ช่วยในแบบปรับท่ายืนและท่านั่ง</p>
<h2>เมื่อไหร่ควรชี้ทางไปต่อ</h2><p>ปวดเวลามีเพศสัมพันธ์ เลือดออกโดยอธิบายไม่ได้ หรือรู้สึกกดทับหรือหนักในอุ้งเชิงกราน เป็นสัญญาณให้พบนักกายภาพบำบัดอุ้งเชิงกรานหรือแพทย์ คนตั้งครรภ์ หลังคลอด หรือพักฟื้นจากการผ่าตัด แนะนำให้ตรวจก่อน ผู้นำให้กำลังใจและไม่วินิจฉัย</p>
<div class="set"><h2>หลักสูตรผู้นำ PelvisPower</h2><p>หลักสูตรรับรองกำลังจะมา สอนให้คุณนำกลุ่มและคู่ผ่านหนึ่งเดือน ดูแลทุกเซสชันให้ปลอดภัยและสบาย และรู้ว่าเมื่อไหร่ควรส่งต่อ เหมาะกับคนอบอุ่นและช่างสงสัย และไม่ต้องมีพื้นฐานทางการแพทย์</p>
<p>ผู้นำจะได้รับแผนเซสชันสำหรับทุกระดับ บทพูดเปิดคลาส เคล็ดลับสำหรับกลุ่มที่ความสามารถต่างกัน และประกาศนียบัตร</p>
<form class="wait" onsubmit="return false"><label>เข้าร่วมรายชื่อรอคิว<input type="email" placeholder="you@example.com" disabled></label><button class="btn" disabled>เปิดเร็วๆ นี้</button></form></div></article>'''
page('/women/leaders/','ผู้นำและคลาส | PelvisPower','วิธีนำ PelvisPower เป็นคู่ กลุ่มเพื่อน และคลาสเล็กๆ รวมถึงหลักสูตรรับรองผู้นำที่กำลังจะมา',ld,active='/th/women/leaders/')
# Men
mn='''<img class="coversm" src="/assets/pics/the-full-lift.svg" alt="" style="max-width:120px;background:#fff;border-radius:12px;padding:8px"><p class="kick">อยู่ระหว่างเตรียมการ</p><h1>PelvisPower สำหรับผู้ชาย</h1><p class="sub">หนึ่งเดือนแบบเดียวกัน สำหรับกล้ามเนื้อที่ผู้ชายก็มี</p><article>
<p>ผู้ชายก็มีพื้นเชิงกราน และมันทำงานมากมาย มันรองรับการทำงานทางเพศ ช่วยเรื่องการควบคุมและความอึด และร่วมอยู่ในจุดสุดยอด ฝึกได้ และการฝึกก็เป็นมิตรและเป็นส่วนตัว</p>
<p>หนึ่งเดือนนี้เดินตามแผนเดียวกับหลักสูตรของผู้หญิง สามสิบวัน ห้าระดับ สิบสองท่า และพิธีจบหลักสูตร ท่าต่างกันเล็กน้อยและจิตวิญญาณเหมือนกัน</p>
<h2>สิ่งที่จะได้พบ</h2><p>วันละสามถึงสิบนาที ในชุดบางๆ ที่ใส่สบาย เบาสบาย ขำขัน ไม่เป็นทางคลินิก มีหน้าปัดความสุขตั้งแต่ 1 ถึง 5 และรางวัลที่คุณกำหนดเอง</p>
<h2>ฝึกกับเธอ</h2><p>หลายคู่ฝึกขนานกัน คนละเล่ม และเปรียบเทียบตัวเลขกันตอนอาหารเช้า ดู <a href="/th/two/">ฝึกด้วยกัน</a></p>
<p class="c"><a class="btn alt" href="/th/women/">ระหว่างนี้ ดูหลักสูตรของผู้หญิง</a></p></article>'''
page('/men/','PelvisPower สำหรับผู้ชาย | อยู่ระหว่างเตรียมการ','หลักสูตรพื้นเชิงกราน 30 วันสำหรับผู้ชาย อยู่ระหว่างเตรียมการ',mn,active='/th/men/')
# Together
tg='''<p class="kick">ดีกว่าเมื่อไปด้วยกัน</p><h1>ฝึกด้วยกัน</h1><p class="sub">วันเดียวกัน เสื่อเคียงกัน รอยยิ้มกว้างๆ</p><article>
<h2>เคียงข้างกัน</h2><p>คุณกับคู่ของคุณฝึกวันเดียวกัน คนหนึ่งใช้ PelvisPower สำหรับผู้หญิง อีกคนใช้สำหรับผู้ชาย นับจำนวนครั้งให้กัน เชียร์กัน และเปรียบเทียบตัวเลขเหนือกาแฟ</p>
<h2>กับเพื่อน</h2><p>เพื่อน พี่สาวน้องสาว หรือเพื่อนฝึก ทำวันเดียวกันได้ในห้องเดียวกันหรือผ่านวิดีโอคอล ทุกคนใส่เสื้อผ้าอยู่และอยู่ในพื้นที่ของตัวเอง</p>
<h2>ในคลาสเล็กๆ</h2><p>สี่ถึงสิบสองคนบนเสื่อ พร้อมผู้นำที่อ่านบทโค้ชและเรียกชุดฝึก ดู<a href="/th/women/leaders/">มุมของผู้นำ</a>สำหรับแผน</p>
<h2>กับ Dress for Caress</h2><p>PelvisPower คือการออกกำลัง และ <a href="https://dressforcaress.com/">Dress for Caress</a> คือรางวัล ฝึกก่อน แล้วเพลิดเพลินกับวันนั้นของ Dress for Caress หรือจบเดือน PelvisPower แล้วค่อยเริ่ม หรือผสมกันก็ได้ จังหวะไหนที่ทำให้คุณยิ้มได้คือจังหวะที่ถูกต้อง</p></article>'''
page('/two/','ฝึกด้วยกัน | PelvisPower','ฝึกกับคู่ เพื่อน หรือคลาสเล็กๆ และจับคู่ PelvisPower กับ Dress for Caress',tg,active='/th/two/')
page('/404.html','ไม่พบหน้านี้ | PelvisPower','ไม่พบหน้านี้','<h1>ไม่พบหน้านี้</h1><p class="sub">หน้านั้นปล่อยนุ่มไปแล้ว</p><p class="c"><a class="btn" href="/th/">หน้าแรก</a></p>')
json.dump(PAGES,open('/home/claude/pelvispower/th_pages.json','w'))
print(len(PAGES),'th pages')
