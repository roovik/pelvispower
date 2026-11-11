# Language registry. Add a language by setting live=True once its folder is built.
LANGS=[('en','EN','English','',True),('th','TH','ไทย','/th',True),
('fr','FR','Français','/fr',True),('es','ES','Español','/es',True),
('de','DE','Deutsch','/de',True),('pt','PT','Português','/pt',True),('ru','RU','Русский','/ru',True),('he','HE','עברית','/he',True)]
SITE='https://pelvispower.org'
def live(): return [l for l in LANGS if l[4]]
def strip(path):
    for c,_,_,pre,_ in LANGS:
        if pre and (path==pre+'/' or path.startswith(pre+'/')): return path[len(pre):] or '/'
    return path
def switcher(path,cur):
    base=strip(path)
    out='<div class="lang" role="group" aria-label="Language">'
    for c,code,name,pre,_ in live():
        on=' class="on" aria-current="true"' if c==cur else ''
        out+=f'<a{on} href="{pre}{base}" hreflang="{c}" lang="{c}" title="{name}"><img src="/assets/flags/{c}.svg" alt="" width="20" height="14"><span>{code}</span></a>'
    return out+'</div>'
def alternates(path):
    base=strip(path); out=''
    for c,_,_,pre,_ in live():
        out+=f'<link rel="alternate" hreflang="{c}" href="{SITE}{pre}{base}">'
    return out+f'<link rel="alternate" hreflang="x-default" href="{SITE}{base}">'
