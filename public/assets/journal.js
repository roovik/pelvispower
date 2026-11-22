(function(){
var root=document.getElementById('pp-journal'); if(!root) return;
var book=root.dataset.book, KEY='pp_journal_'+book, N=+root.dataset.days||30;
var titles=JSON.parse(root.dataset.titles), recess=JSON.parse(root.dataset.recess||'[]');
var D={done:{},dial:{},note:{},nums:{}}, memOnly=false;
try{var raw=localStorage.getItem(KEY); if(raw){var o=JSON.parse(raw); if(o&&typeof o==='object')D=Object.assign(D,o)}}catch(e){memOnly=true}
function save(){try{localStorage.setItem(KEY,JSON.stringify(D))}catch(e){memOnly=true;var w=document.getElementById('pj-warn'); if(w)w.hidden=false}}
function $(s,c){return (c||root).querySelector(s)} function el(t,a,h){var e=document.createElement(t);for(var k in a||{})e.setAttribute(k,a[k]);if(h!=null)e.innerHTML=h;return e}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
if(memOnly){var w=$('#pj-warn'); if(w)w.hidden=false}
var cur=1; try{var q=new URLSearchParams(location.search).get('day'); if(q&&+q>=1&&+q<=N)cur=+q}catch(e){}
function renderGrid(){var g=$('#pj-grid'); g.innerHTML=''; var done=0;
 for(var n=1;n<=N;n++){var on=!!D.done[n]; if(on)done++;
  var b=el('button',{type:'button','class':'pj-cell'+(on?' on':'')+(n===cur?' cur':''),'aria-pressed':on?'true':'false','aria-label':'Day '+n+', '+titles[n-1]+(on?', done':'')},'<b>'+n+'</b><span>'+(recess.indexOf(n)>-1?'Recess':(on?'✓':''))+'</span>');
  (function(n){b.addEventListener('click',function(){cur=n;fillForm();renderGrid()})})(n); g.appendChild(b)}
 $('#pj-count').textContent=done+' of '+N+' Days done'; $('#pj-bar').style.width=(done/N*100)+'%'}
function fillForm(){$('#pj-dayname').textContent='Day '+cur+': '+titles[cur-1]; $('#pj-done').checked=!!D.done[cur]; $('#pj-dial').value=D.dial[cur]||''; $('#pj-note').value=D.note[cur]||''; $('#pj-open').href='/'+book+'/day-'+('0'+cur).slice(-2)+'/'; $('#pj-saved').textContent=''}
$('#pj-form').addEventListener('submit',function(e){e.preventDefault(); D.done[cur]=$('#pj-done').checked; var d=$('#pj-dial').value; if(d)D.dial[cur]=+d; else delete D.dial[cur]; var t=$('#pj-note').value.trim(); if(t)D.note[cur]=t; else delete D.note[cur]; save(); renderGrid(); renderEntries(); $('#pj-saved').textContent='Saved on this device.'});
function renderEntries(){var l=$('#pj-entries'); l.innerHTML=''; var any=false;
 for(var n=1;n<=N;n++){if(D.note[n]||D.dial[n]||D.done[n]){any=true; var li=el('li',{},'<b>Day '+n+'</b> '+esc(titles[n-1])+(D.dial[n]?' <span class="pj-dial">Dial '+D.dial[n]+'</span>':'')+(D.note[n]?'<br>'+esc(D.note[n]):'')); l.appendChild(li)}}
 if(!any)l.appendChild(el('li',{},'<i>Nothing logged yet.</i>'))}
var nk=['b1','b2','b3','a1','a2','a3'];
nk.forEach(function(k){var i=$('#pj-'+k); i.value=D.nums[k]!=null?D.nums[k]:''; i.addEventListener('input',function(){if(i.value==='')delete D.nums[k]; else D.nums[k]=+i.value; save(); diffs()})});
function diffs(){for(var i=1;i<=3;i++){var b=D.nums['b'+i],a=D.nums['a'+i],c=$('#pj-d'+i); if(b!=null&&a!=null){var d=a-b; c.textContent=(d>0?'+':'')+d; c.className='pj-diff '+(d>0?'up':(d<0?'down':''))}else{c.textContent='';c.className='pj-diff'}}}
$('#pj-export').addEventListener('click',function(){var t='PelvisPower for '+(book==='men'?'Men':'Women')+' journal\n\n';
 for(var n=1;n<=N;n++){if(D.note[n]||D.dial[n]||D.done[n])t+='Day '+n+': '+titles[n-1]+(D.done[n]?' [done]':'')+(D.dial[n]?' Dial '+D.dial[n]:'')+'\n'+(D.note[n]?D.note[n]+'\n':'')+'\n'}
 t+='Three numbers\n'; for(var i=1;i<=3;i++)t+=root.dataset['n'+i]+': before '+(D.nums['b'+i]!=null?D.nums['b'+i]:'-')+', after '+(D.nums['a'+i]!=null?D.nums['a'+i]:'-')+'\n';
 var a=el('a',{href:URL.createObjectURL(new Blob([t],{type:'text/plain'})),download:'pelvispower-'+book+'-journal.txt'}); document.body.appendChild(a); a.click(); a.remove()});
$('#pj-clear').addEventListener('click',function(){if(window.confirm('Erase this journal from this device? This cannot be undone.')){D={done:{},dial:{},note:{},nums:{}};try{localStorage.removeItem(KEY)}catch(e){} nk.forEach(function(k){$('#pj-'+k).value=''}); fillForm(); renderGrid(); renderEntries(); diffs()}});
fillForm(); renderGrid(); renderEntries(); diffs();
/* ---------- guided timer ---------- */
var T={run:false,pause:false,phase:0,left:0,rep:0,tm:null,ctx:null,wl:null};
var modes={hold:{names:['Lift','Release'],speak:['Lift','Release'],a:['pj-t-a','pj-t-b'],label:'reps'},breath:{names:['Breathe in','Breathe out'],speak:['Breathe in','Breathe out and let go'],label:'breaths'}};
function mode(){return $('#pj-mode').value} function nums(){return {a:Math.max(1,+$('#pj-t-a').value||3),b:Math.max(1,+$('#pj-t-b').value||3),r:Math.max(1,+$('#pj-t-r').value||5)}}
function beep(f){if(!$('#pj-sound').checked)return; try{T.ctx=T.ctx||new (window.AudioContext||window.webkitAudioContext)(); var o=T.ctx.createOscillator(),g=T.ctx.createGain(); o.type='sine'; o.frequency.value=f; g.gain.value=.12; o.connect(g); g.connect(T.ctx.destination); o.start(); o.stop(T.ctx.currentTime+.18)}catch(e){}}
function say(t){if(!$('#pj-speak').checked||!window.speechSynthesis)return; try{window.speechSynthesis.cancel(); var u=new SpeechSynthesisUtterance(t); u.rate=.9; u.volume=.8; window.speechSynthesis.speak(u)}catch(e){}}
function setView(){var m=modes[mode()],n=nums(); $('#pj-phase').textContent=T.run?m.names[T.phase]:'Ready'; $('#pj-left').textContent=T.run?T.left:'—'; $('#pj-rep').textContent=T.run?(T.rep+1)+' of '+n.r+' '+m.label:n.r+' '+m.label; $('#pj-timer').className='pj-timer'+(T.run?(T.phase===0?' in':' out'):'')}
function begin(ph){var n=nums(); T.phase=ph; T.left=ph===0?n.a:n.b; var m=modes[mode()]; beep(ph===0?660:440); say(m.speak[ph]); setView()}
function tick(){if(T.pause)return; T.left--; if(T.left<=0){ if(T.phase===0)begin(1); else{T.rep++; if(T.rep>=nums().r){finish();return} begin(0)} } else setView()}
function finish(){clearInterval(T.tm); T.run=false; beep(880); say('Done. Soft drop.'); setView(); $('#pj-start').textContent='Start'; $('#pj-pause').disabled=true; unlock()}
function lock(){try{if(navigator.wakeLock)navigator.wakeLock.request('screen').then(function(l){T.wl=l}).catch(function(){})}catch(e){}} function unlock(){try{if(T.wl){T.wl.release();T.wl=null}}catch(e){}}
$('#pj-start').addEventListener('click',function(){ if(T.run){finish();return} T.run=true;T.pause=false;T.rep=0; $('#pj-start').textContent='Stop'; $('#pj-pause').disabled=false; $('#pj-pause').textContent='Pause'; lock(); begin(0); T.tm=setInterval(tick,1000)});
$('#pj-pause').addEventListener('click',function(){T.pause=!T.pause; this.textContent=T.pause?'Resume':'Pause'});
function presets(){var m=mode(); var A=$('#pj-t-a'),B=$('#pj-t-b'),R=$('#pj-t-r'); if(m==='breath'){$('#pj-la').textContent='Breathe in (seconds)';$('#pj-lb').textContent='Breathe out (seconds)';$('#pj-lr').textContent='Breaths';A.value=4;B.value=6;R.value=5}else{$('#pj-la').textContent='Lift and hold (seconds)';$('#pj-lb').textContent='Release (seconds)';$('#pj-lr').textContent='Reps';A.value=3;B.value=3;R.value=5} setView()}
$('#pj-mode').addEventListener('change',function(){if(!T.run)presets()}); ['pj-t-a','pj-t-b','pj-t-r'].forEach(function(i){$('#'+i).addEventListener('input',function(){if(!T.run)setView()})});
presets();
})();
