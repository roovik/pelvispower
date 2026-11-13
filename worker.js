// PelvisPower: public landing pages, course pages need a one-time free registration (18+, terms, content notice).
// Free access runs until FREE_UNTIL (wrangler.toml). After that the course pages show the /closed/ notice.
const enc = new TextEncoder();
const b64 = (buf) => btoa(String.fromCharCode(...new Uint8Array(buf))).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');
async function sign(secret, data) {
  const k = await crypto.subtle.importKey('raw', enc.encode(secret), {name:'HMAC',hash:'SHA-256'}, false, ['sign']);
  return b64(await crypto.subtle.sign('HMAC', k, enc.encode(data)));
}
async function makeToken(env, email, ttl) {
  const p = b64(enc.encode(JSON.stringify({e: email, x: Date.now() + ttl})));
  return p + '.' + await sign(env.SESSION_SECRET, p);
}
async function readToken(env, tok) {
  if (!tok || !tok.includes('.') || !env.SESSION_SECRET) return null;
  const [p, s] = tok.split('.');
  if (s !== await sign(env.SESSION_SECRET, p)) return null;
  try { const o = JSON.parse(atob(p.replace(/-/g,'+').replace(/_/g,'/'))); return o.x > Date.now() ? o : null; } catch { return null; }
}
const cookie = (req, n) => (req.headers.get('cookie') || '').split(/;\s*/).map(c => c.split('=')).find(c => c[0] === n)?.[1];
const REG = 'ppr', TERMS = '2026-11';
const LANGRE = '(?:(fr|es|de|pt|ru|he|th)\\/)?';
const freeNow = (env) => !!env.FREE_UNTIL && Date.now() < Date.parse(env.FREE_UNTIL);
const isRegistered = async (env, req) => { try { return !!(await readToken(env, cookie(req, REG))); } catch { return false; } };
// only same-site paths are accepted as a redirect target
const safeNext = (n, dflt) => (typeof n === 'string' && /^\/[^\/\\]/.test(n) && !/[\r\n]/.test(n)) ? n : dflt;

async function welcome(env, origin, email) {
  if (!env.RESEND_API_KEY) return false;
  const until = env.FREE_UNTIL_TEXT || '1 January';
  const text = 'Welcome to PelvisPower.\n\nYou are registered, and all of the courses are open to you for free until ' + until + ': PelvisPower for Women, PelvisPower for Men and the Daily Dozen, on any device.\n\nWomen: ' + origin + '/women/start-here/\nMen: ' + origin + '/men/start-here/\n\nOn another device, open ' + origin + '/start/ and enter this email address (' + email + ').\n\nA companion for the reading side of the month is Dress for Caress: https://dressforcaress.com\n\nThese courses are education and exercise, not medical care. If you have pain, a medical condition or a recent surgery, check with a clinician first.\n\nIf you have a question, reply to this email.\n\nPelvisPower\nhello@pelvispower.org';
  try {
    const r = await fetch('https://api.resend.com/emails', {method:'POST', headers:{authorization:'Bearer ' + env.RESEND_API_KEY,'content-type':'application/json'},
      body: JSON.stringify({from:'PelvisPower <hello@pelvispower.org>', reply_to:'hello@pelvispower.org', to:[email], subject:'Welcome to PelvisPower', text})});
    if (!r.ok) console.error('welcome: resend failed', r.status);
    return r.ok;
  } catch (e) { console.error('welcome error', e && e.message); return false; }
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url), path = url.pathname, origin = url.origin;

    if (path === '/api/register' && req.method === 'POST') {
      try {
        const ct = req.headers.get('content-type') || '';
        const f = /form/.test(ct) ? await req.formData() : new FormData();
        const email = String(f.get('email') || '').trim().toLowerCase();
        const lg = String(f.get('lang') || ''); const pre = /^(fr|es|de|pt|ru|he|th)$/.test(lg) ? '/' + lg : '';
        const next = safeNext(String(f.get('next') || ''), '/women/start-here/');
        if (f.get('website')) return Response.redirect(origin + '/', 303);   // honeypot
        if (!freeNow(env)) return Response.redirect(origin + '/closed/', 303);
        const valid = /^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(email) && email.length < 200;
        if (!valid || !f.get('age') || !f.get('terms') || !f.get('aware'))
          return Response.redirect(origin + pre + '/start/?e=1&next=' + encodeURIComponent(next), 303);
        if (!env.SESSION_SECRET) { console.error('register: SESSION_SECRET is not set'); return new Response('Registration is not switched on yet. Write to hello@pelvispower.org.', {status: 503}); }
        const seen = await env.MEMBERS.get('r:' + email).catch(() => null);
        await env.MEMBERS.put('r:' + email, JSON.stringify({at: Date.now(), terms: TERMS, over18: true, aware: true, lang: lg || 'en'}));
        if (!seen) await welcome(env, origin, email);
        const tok = await makeToken(env, email, 365*24*3600*1000);
        return new Response(null, {status: 303, headers: {location: origin + next, 'set-cookie': `${REG}=${tok}; Path=/; Max-Age=31536000; HttpOnly; Secure; SameSite=Lax`}});
      } catch (err) {
        console.error('register error', err && err.message);
        return new Response('Something went wrong on our side. Try again in a minute, or write to hello@pelvispower.org.', {status: 500});
      }
    }

    const sm = new RegExp('^\\/' + LANGRE + 'start\\/?$').exec(path);
    if (sm) {
      if (!freeNow(env)) return Response.redirect(origin + '/closed/', 302);
      if (await isRegistered(env, req)) return Response.redirect(origin + safeNext(url.searchParams.get('next'), '/women/start-here/'), 302);
      const r = await env.ASSETS.fetch(req); const h = new Headers(r.headers); h.set('cache-control', 'private, no-store'); return new Response(r.body, {status: r.status, headers: h});
    }

    // course pages: everything under /women/ and /men/ except the landing page itself
    const gm = new RegExp('^\\/' + LANGRE + '(women|men)\\/[^\\/].*$').exec(path);
    if (gm) {
      if (!freeNow(env)) return Response.redirect(origin + '/closed/', 302);
      if (!(await isRegistered(env, req)))
        return Response.redirect(origin + (gm[1] ? '/' + gm[1] : '') + '/start/?next=' + encodeURIComponent(path), 302);
      const r = await env.ASSETS.fetch(req); const h = new Headers(r.headers);
      h.set('cache-control', 'private, no-store'); h.set('x-robots-tag', 'noindex');
      return new Response(r.body, {status: r.status, headers: h});
    }
    return env.ASSETS.fetch(req);
  }
};
