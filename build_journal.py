# exec'd from build_site.py after build_men.py: journal and guided timer pages for Women and Men.
import json as _j
_BL=_j.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'booklinks.json')))
def _bookbox(key):
    l=_BL.get(key,{}); bt=''
    if l.get('kindle'): bt+=f'<a class="btn" href="{E(l["kindle"])}" rel="noopener">Get the Kindle edition</a>'
    if l.get('paperback'): bt+=f'<a class="btn" href="{E(l["paperback"])}" rel="noopener">Get the paperback</a>'
    if l.get('pdf'): bt+=f'<a class="btn alt" href="{E(l["pdf"])}" rel="noopener">Get the PDF edition</a>'
    if not bt: return ''
    return f'<div class="bookbox noprint"><p><b>Prefer paper or a file?</b> The full book is also available to keep, read offline and write in.</p><p>{bt}</p></div>'
def _journal(key,label,days,rec,n_labels):
    titles=_j.dumps([days[n]['title'] for n in range(1,31)])
    na=''.join(f'data-n{i}="{E(t)}" ' for i,t in enumerate(n_labels,1))
    rows=''.join(f'<tr><th>{E(t)}</th><td><input type="number" min="0" inputmode="numeric" id="pj-b{i}" aria-label="{E(t)} before"></td><td><input type="number" min="0" inputmode="numeric" id="pj-a{i}" aria-label="{E(t)} after"></td><td id="pj-d{i}" class="pj-diff"></td></tr>' for i,t in enumerate(n_labels,1))
    b=f'''<p class="kick">Your private record</p><h1>Your Journal and Timer</h1><p class="sub">Tick off Days, log how it went, track your three numbers and train with a guided timer.</p>
<div class="pj" id="pp-journal" data-book="{key}" data-days="30" data-titles='{E(titles)}' data-recess='{_j.dumps(sorted(rec))}' {na}>
<div class="pj-private"><b>Private by design.</b> Everything you type here is saved only in this browser on this device. Nothing is sent to us or to anyone else. Use Export to keep a copy, since clearing your browser data will erase it.</div>
<p class="pj-warn" id="pj-warn" hidden>This browser is not allowing saved data right now (private browsing can do that). Your entries will be lost when you close the page, so use Export before you leave.</p>
<h2>Your month</h2><div class="pj-bar"><i id="pj-bar"></i></div><p id="pj-count" aria-live="polite"></p>
<div class="pj-grid" id="pj-grid"></div>
<h2 id="log">Log a Day</h2>
<form id="pj-form"><p><b id="pj-dayname"></b> <a id="pj-open" href="#">Open this Day</a></p>
<label class="chk"><input type="checkbox" id="pj-done"> I finished this Day</label>
<div class="row"><div><label for="pj-dial">Pleasure Dial (1 to 5)</label><select id="pj-dial"><option value="">Not set</option><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option></select></div></div>
<label for="pj-note">One line about today</label><textarea id="pj-note" maxlength="600" placeholder="What felt different? What was funny?"></textarea>
<p class="noprint" style="color:var(--mute);font-size:14px">To speak instead of type, use the microphone key on your phone or computer keyboard. Your device handles the dictation, and this page never hears your voice.</p>
<p><button class="btn" type="submit">Save</button> <span id="pj-saved" aria-live="polite"></span></p></form>
<h2>Your log</h2><ul class="pj-entries" id="pj-entries"></ul>
<h2>The three numbers</h2><table><tr><th></th><th>Day 1 (before)</th><th>Day 29 (after)</th><th>Change</th></tr>{rows}</table>
<p class="pj-btns"><button class="btn alt" type="button" id="pj-export">Export as a text file</button> <button class="btn alt" type="button" id="pj-clear">Erase this journal</button></p>
<h2 id="timer">Guided timer</h2><p>Soft tones mark each phase, so you can close your eyes. Turn on spoken cues if you like.</p>
<label for="pj-mode">Exercise</label><select id="pj-mode"><option value="hold">Lift, hold and release</option><option value="breath">Soft Drop breathing</option></select>
<div class="row"><div><label id="pj-la" for="pj-t-a">Lift and hold (seconds)</label><input type="number" min="1" max="60" id="pj-t-a" value="3"></div><div><label id="pj-lb" for="pj-t-b">Release (seconds)</label><input type="number" min="1" max="60" id="pj-t-b" value="3"></div><div><label id="pj-lr" for="pj-t-r">Reps</label><input type="number" min="1" max="60" id="pj-t-r" value="5"></div></div>
<div class="opts"><label><input type="checkbox" id="pj-sound" checked> Tones</label><label><input type="checkbox" id="pj-speak"> Spoken cues</label></div>
<div class="pj-timer" id="pj-timer" aria-live="polite"><div class="pj-phase" id="pj-phase">Ready</div><div class="pj-left" id="pj-left">&#8212;</div><div class="pj-rep" id="pj-rep"></div></div>
<p class="c"><button class="btn" type="button" id="pj-start">Start</button> <button class="btn alt" type="button" id="pj-pause" disabled>Pause</button></p>
<p style="color:var(--mute);font-size:14px">Set the numbers to match today's set. Always finish with a full release.</p>
</div>{_bookbox(key)}<p class="c noprint"><a class="btn alt" href="/{key}/">All Days</a> <a class="btn alt" href="/{key}/chart/" style="display:{'inline-block' if key=='women' else 'none'}">Printable chart</a></p>
<script src="/assets/journal.js" defer></script>'''
    page(f'/{key}/journal/',f'Your Journal and Timer | PelvisPower for {label}','A private journal, three-numbers tracker and guided timer. Saved only on your device.',b,active=f'/{key}/',extra_head='<link rel="stylesheet" href="/assets/journal.css">')
_journal('women','Women',DAYS,RECESS,['Longest hold, in seconds (stop at 30)','Flicks in 30 seconds','Steps up (stop at 10)'])
_journal('men','Men',MDAYS,MREC,['Longest hold, in seconds (stop at 30)','Salutes in thirty seconds','Steps up (stop at 10)'])
