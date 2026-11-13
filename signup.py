#!/usr/bin/env python3
"""PelvisPower free registration: sign-up pages (8 languages), Terms, closed notice, home notice, removal of the old age pop-up.
Run after the builders and before sidebar.py (build_all.sh does this).

GIVEAWAY SWITCH
  giveaway.cfg (two lines):  mode=on  and  until=1 January 2027
  mode=on  puts the "Free until <date>" notice on the home pages. mode=off removes it.
  The access rule itself (worker.js) is driven only by FREE_UNTIL in wrangler.toml.
TO RUN AGAIN IN A FUTURE YEAR
  1. giveaway.cfg: mode=on and the new date text, update DATES below for every language.
  2. wrangler.toml: FREE_UNTIL (ISO, UTC) and FREE_UNTIL_TEXT (used in the welcome email).
  3. sh build_all.sh, commit and push.
"""
import os, re, glob, html, json
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE + '/public'
LANGS = ['fr', 'es', 'de', 'pt', 'ru', 'he', 'th']

T = {
 'en': dict(h1='Start free', sub='One quick step before you read. It takes a minute.', email='Your email', age='I am 18 or older.',
   terms='I accept the <a href="/terms/">Terms and Privacy Notice</a>.',
   aware='I understand that this site contains frank material about sexual matters. It is educational and sensual, with no pornographic images or video.',
   btn='Open the free week', fine='We keep your email and the time you agreed so we know you have registered. We never sell or share it.',
   err='Enter a valid email and tick all three boxes.', member='Already a member?', signin='Sign in'),
 'fr': dict(h1='Commencer gratuitement', sub='Une petite étape avant de lire. Elle prend une minute.', email='Votre e-mail', age="J'ai 18 ans ou plus.",
   terms='J\'accepte les <a href="/terms/">Conditions et l\'Avis de confidentialité</a> (en anglais).',
   aware="Je comprends que ce site contient des textes francs sur la sexualité. Le contenu est éducatif et sensuel, sans images ni vidéos pornographiques.",
   btn='Ouvrir la semaine gratuite', fine="Nous conservons votre e-mail et l'heure de votre accord pour savoir que vous êtes inscrit(e). Nous ne le vendons ni ne le partageons jamais.",
   err='Saisissez un e-mail valide et cochez les trois cases.', member='Déjà membre ?', signin='Se connecter'),
 'es': dict(h1='Empieza gratis', sub='Un paso rápido antes de leer. Lleva un minuto.', email='Tu correo electrónico', age='Tengo 18 años o más.',
   terms='Acepto los <a href="/terms/">Términos y el Aviso de privacidad</a> (en inglés).',
   aware='Entiendo que este sitio contiene material franco sobre temas sexuales. Es educativo y sensual, sin imágenes ni vídeos pornográficos.',
   btn='Abrir la semana gratis', fine='Guardamos tu correo y la hora de tu aceptación para saber que te has registrado. Nunca lo vendemos ni lo compartimos.',
   err='Escribe un correo válido y marca las tres casillas.', member='¿Ya eres miembro?', signin='Iniciar sesión'),
 'de': dict(h1='Kostenlos starten', sub='Ein kurzer Schritt vor dem Lesen. Er dauert eine Minute.', email='Deine E-Mail', age='Ich bin 18 oder älter.',
   terms='Ich akzeptiere die <a href="/terms/">Bedingungen und die Datenschutzhinweise</a> (auf Englisch).',
   aware='Ich verstehe, dass diese Seite offene Texte über Sexualität enthält. Sie sind aufklärend und sinnlich, ohne pornografische Bilder oder Videos.',
   btn='Die Gratiswoche öffnen', fine='Wir speichern deine E-Mail und den Zeitpunkt deiner Zustimmung, damit wir wissen, dass du registriert bist. Wir verkaufen oder teilen sie nie.',
   err='Gib eine gültige E-Mail ein und setze alle drei Häkchen.', member='Schon Mitglied?', signin='Anmelden'),
 'pt': dict(h1='Comece de graça', sub='Um passo rápido antes de ler. Leva um minuto.', email='Seu e-mail', age='Tenho 18 anos ou mais.',
   terms='Aceito os <a href="/terms/">Termos e o Aviso de Privacidade</a> (em inglês).',
   aware='Entendo que este site contém material franco sobre assuntos sexuais. É educativo e sensual, sem imagens ou vídeos pornográficos.',
   btn='Abrir a semana grátis', fine='Guardamos seu e-mail e o momento do seu aceite para saber que você se cadastrou. Nunca o vendemos nem o compartilhamos.',
   err='Digite um e-mail válido e marque as três caixas.', member='Já é membro?', signin='Entrar'),
 'ru': dict(h1='Начните бесплатно', sub='Один короткий шаг перед чтением. Он займёт минуту.', email='Ваш e-mail', age='Мне 18 лет или больше.',
   terms='Я принимаю <a href="/terms/">Условия и Уведомление о конфиденциальности</a> (на английском).',
   aware='Я понимаю, что на этом сайте есть откровенные материалы на сексуальные темы. Они познавательные и чувственные, без порнографических изображений и видео.',
   btn='Открыть бесплатную неделю', fine='Мы храним ваш e-mail и время вашего согласия, чтобы знать, что вы зарегистрированы. Мы никогда не продаём его и не передаём другим.',
   err='Введите настоящий e-mail и отметьте все три пункта.', member='Уже участница?', signin='Войти'),
 'he': dict(h1='מתחילות בחינם', sub='צעד קצר אחד לפני הקריאה. הוא לוקח דקה.', email='האימייל שלך', age='אני בת 18 ומעלה.',
   terms='אני מאשרת את <a href="/terms/">התנאים והודעת הפרטיות</a> (באנגלית).',
   aware='אני מבינה שהאתר כולל חומר גלוי על עניינים מיניים. החומר חינוכי ותחושתי, בלי תמונות או סרטונים פורנוגרפיים.',
   btn='לפתוח את השבוע החינמי', fine='אנחנו שומרים את האימייל שלך ואת מועד ההסכמה כדי לדעת שנרשמת. אנחנו לא מוכרים ולא משתפים אותו לעולם.',
   err='הזיני אימייל תקין וסמני את שלוש התיבות.', member='כבר חברה?', signin='כניסה'),
 'th': dict(h1='เริ่มอ่านฟรี', sub='ขั้นตอนสั้น ๆ ก่อนอ่าน ใช้เวลาไม่ถึงหนึ่งนาที', email='อีเมลของคุณ', age='ฉันอายุ 18 ปีขึ้นไป',
   terms='ฉันยอมรับ<a href="/terms/">ข้อกำหนดและประกาศความเป็นส่วนตัว</a> (ภาษาอังกฤษ)',
   aware='ฉันเข้าใจว่าเว็บไซต์นี้มีเนื้อหาตรงไปตรงมาเกี่ยวกับเรื่องเพศ เนื้อหาให้ความรู้และเร้าความรู้สึก ไม่มีภาพหรือวิดีโอลามก',
   btn='เปิดสัปดาห์ฟรี', fine='เราเก็บอีเมลและเวลาที่คุณยอมรับ เพื่อให้รู้ว่าคุณลงทะเบียนแล้ว เราไม่ขายและไม่แบ่งปันให้ใคร',
   err='กรอกอีเมลที่ถูกต้องและติ๊กทั้งสามช่อง', member='เป็นสมาชิกแล้ว?', signin='เข้าสู่ระบบ'),
}

BTN = {'en': 'Register and start', 'fr': "S'inscrire et commencer", 'es': 'Registrarme y empezar', 'de': 'Registrieren und starten',
       'pt': 'Cadastrar e começar', 'ru': 'Зарегистрироваться и начать', 'he': 'להירשם ולהתחיל', 'th': 'ลงทะเบียนและเริ่ม'}
for _l, _b in BTN.items():
    T[_l]['btn'] = _b

DATES = {'en': '1 January 2027', 'fr': '1er janvier 2027', 'es': '1 de enero de 2027', 'de': '1. Januar 2027',
         'pt': '1º de janeiro de 2027', 'ru': '1 января 2027', 'he': '1 בינואר 2027', 'th': '1 มกราคม 2570'}
NOTE = {
 'en': ('Free until {d}. Register with your email to read the courses.', 'Register free'),
 'fr': ("Gratuit jusqu'au {d}. Inscrivez-vous avec votre e-mail pour lire les cours.", "S'inscrire gratuitement"),
 'es': ('Gratis hasta el {d}. Regístrate con tu correo para leer los cursos.', 'Registrarme gratis'),
 'de': ('Kostenlos bis zum {d}. Registriere dich mit deiner E-Mail, um die Kurse zu lesen.', 'Kostenlos registrieren'),
 'pt': ('Grátis até {d}. Cadastre-se com o seu e-mail para ler os cursos.', 'Cadastrar grátis'),
 'ru': ('Бесплатно до {d}. Зарегистрируйтесь по e-mail, чтобы читать курсы.', 'Зарегистрироваться бесплатно'),
 'he': ('בחינם עד {d}. נרשמים עם כתובת מייל כדי לקרוא את הקורסים.', 'הרשמה בחינם'),
 'th': ('ฟรีถึง {d} ลงทะเบียนด้วยอีเมลเพื่ออ่านคอร์ส', 'ลงทะเบียนฟรี'),
}
CLOSED = {'h1': 'The free access has closed', 'p': 'The courses were free to read until 1 January 2027, and that period has ended. The landing pages stay open. Write to hello@pelvispower.org to hear about what comes next.'}


def form(lang, t):
    return (f'<form class="reg" method="post" action="/api/register"><input type="hidden" name="lang" value="{lang}"><input type="hidden" name="next" value="">'
            f'<p class="regerr" hidden>{t["err"]}</p>'
            f'<label class="em">{t["email"]}<input type="email" name="email" required autocomplete="email"></label>'
            f'<label class="ck"><input type="checkbox" name="age" value="1" required><span>{t["age"]}</span></label>'
            f'<label class="ck"><input type="checkbox" name="terms" value="1" required><span>{t["terms"]}</span></label>'
            f'<label class="ck"><input type="checkbox" name="aware" value="1" required><span>{t["aware"]}</span></label>'
            f'<input class="hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">'
            f'<button class="btn">{t["btn"]}</button></form>')


def body(lang):
    t = T[lang]
    return f'<h1>{t["h1"]}</h1><p class="sub">{t["sub"]}</p>{form(lang, t)}<p class="fine">{t["fine"]}</p>'


TERMS = '''<h1>Terms and Privacy Notice</h1><p class="sub">Plain words about who this is for and how we treat your information</p><article>
<h2>Who this site is for</h2><p>PelvisPower is for adults. You must be 18 or older, or the age of majority where you live if that is higher, to register and read.</p>
<h2>What you will find here</h2><p>Frank, friendly exercise courses for the muscles behind sexual pleasure and sensation, with plain talk about bodies. It is educational. It contains no pornographic images or video, and nothing involving minors. You can stop at any time and skip anything you do not want to do.</p>
<h2>Not medical or therapeutic advice</h2><p>PelvisPower and Dress for Caress are education and personal exploration. They are not medical care, physiotherapy, therapy or a substitute for any of them. If you have pain, bleeding, a medical condition, a recent surgery, a pregnancy or a recent birth, ask a qualified clinician before you try an exercise. Stop if anything hurts.</p>
<h2>Your access</h2><p>Access is free after you register, until the date shown on the site. Content is for your own personal use. Do not copy, resell or publish it, or share it as your own.</p>
<h2>Your information</h2><p>When you register we keep your email address, the time you agreed to these terms, your confirmation that you are 18 or older and that you understand the nature of the material, and the language you used. We use your email to remember that you registered and to send you a welcome message and news about the courses. We do not sell or share your information.</p>
<p>We use only the cookie needed to remember your registration. Our service providers include Cloudflare (hosting and storage) and Resend (email delivery).</p>
<p>To see or delete your information, write to <a href="mailto:hello@pelvispower.org">hello@pelvispower.org</a>.</p>
<h2>Changes</h2><p>We may update these terms and will change the date below. Version 2026-11.</p></article>'''


def page_from(lang, title, main):
    pre = '' if lang == 'en' else '/' + lang
    s = open(ROOT + pre + '/two/index.html', encoding='utf-8').read()
    s = re.sub(r'<!--sb-->.*?<!--/sb-->', '', s, flags=re.S)
    s = re.sub(r'<!--sb2-->.*?</aside></div><!--/sb2-->', '', s, flags=re.S)
    s = re.sub(r'<!--sb2-->.*?<!--/sb2-->', '', s, flags=re.S)
    s = re.sub(r'<aside class="side".*?</aside></div>', '', s, flags=re.S)
    s = re.sub(r'<main.*</main>', lambda m: '<main>' + main + '</main>', s, count=1, flags=re.S)
    s = re.sub(r'<title>.*?</title>', '<title>%s | PelvisPower</title>' % html.escape(title), s, count=1)
    s = re.sub(r'<link rel="(?:alternate|canonical)"[^>]*>', '', s)
    s = re.sub(r' class=on(?=>)| aria-current="page"| aria-current=page', '', s)
    s = re.sub(r'<meta name="description"[^>]*>', '<meta name="description" content="%s">' % html.escape(title), s, count=1)
    s = s.replace('<meta name="robots" content="index,follow">', '<meta name="robots" content="noindex">')
    return s


def write(path, s):
    d = ROOT + path
    os.makedirs(d, exist_ok=True)
    open(d + 'index.html', 'w', encoding='utf-8').write(s)


def cfg():
    c = {}
    try:
        for ln in open(HERE + '/giveaway.cfg', encoding='utf-8'):
            if '=' in ln: k, v = ln.strip().split('=', 1); c[k.strip()] = v.strip()
    except FileNotFoundError:
        pass
    return c


def notice(lang, on):
    if not on: return ''
    t, b = NOTE[lang]
    pre = '' if lang == 'en' else '/' + lang
    return '<!--gv--><p class="gvnote">%s <a class="btn" href="%s/start/">%s</a></p><!--/gv-->' % (t.format(d=DATES[lang]), pre, b)


def run():
    on = cfg().get('mode') == 'on'
    write('/start/', page_from('en', 'Register free', body('en')))
    write('/terms/', page_from('en', 'Terms and Privacy Notice', TERMS).replace('<meta name="robots" content="noindex">', '<meta name="robots" content="index,follow">'))
    write('/closed/', page_from('en', CLOSED['h1'], '<h1>%s</h1><p class="sub">%s</p>' % (CLOSED['h1'], CLOSED['p'])))
    for c in LANGS:
        write('/%s/start/' % c, page_from(c, T[c]['h1'], body(c)))
    # home notice on every language home page
    for c in ['en'] + LANGS:
        p = ROOT + ('' if c == 'en' else '/' + c) + '/index.html'
        s = open(p, encoding='utf-8').read()
        s = re.sub(r'<!--gv-->.*?<!--/gv-->', '', s, flags=re.S)
        if on: s = re.sub(r'(<main[^>]*>)', lambda m: m.group(1) + notice(c, on), s, count=1)
        open(p, 'w', encoding='utf-8').write(s)
    # remove the old under-18 pop-up everywhere
    n = 0
    pat = re.compile(r'<div id="agegate" hidden>.*?</div></div>\s*', re.S)
    for p in glob.glob(ROOT + '/**/*.html', recursive=True):
        s = open(p, encoding='utf-8').read()
        t2 = pat.sub('', s)
        if t2 != s:
            open(p, 'w', encoding='utf-8').write(t2); n += 1
    js = ('document.addEventListener("click",function(e){var d=document.querySelector("details.lang");if(d&&d.open&&!d.contains(e.target))d.open=false});'
          'document.addEventListener("keydown",function(e){var d=document.querySelector("details.lang");if(e.key==="Escape"&&d)d.open=false});\n'
          '(function(){var f=document.querySelector("form.reg");if(!f)return;try{var q=new URLSearchParams(location.search);var n=q.get("next");'
          'if(n&&/^\\/[^\\/\\\\]/.test(n))f.next.value=n;if(q.get("e")){var e=f.querySelector(".regerr");if(e)e.hidden=false}}catch(x){}})();\n')
    open(ROOT + '/assets/site.js', 'w').write(js)
    print('pp signup: pages written, notice %s, agegate removed from %d pages' % ('on' if on else 'off', n))


if __name__ == '__main__':
    run()
