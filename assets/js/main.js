/* Agvysta demo: elgsena (vanilla JS, be priklausomybių).
   Meniu, atsiradimai, skaičiai, video tik matomoje srityje, paslaugų rodyklė, projektų karuselė,
   nuotraukų peržiūra, projektų filtras, demonstracinė forma. Jokių scroll klausytojų: tik IntersectionObserver. */
(() => {
  'use strict';
  window.__agv = 1;
  const d = document, html = d.documentElement;
  const calm = html.classList.contains('calm');
  const $ = (s, c = d) => c.querySelector(s);
  const $$ = (s, c = d) => Array.from(c.querySelectorAll(s));

  /* įėjimo seka: palaukiama šriftų (ne ilgiau 700 ms) */
  const loaded = () => requestAnimationFrame(() => html.classList.add('is-loaded'));
  if (d.fonts && d.fonts.ready) Promise.race([d.fonts.ready, new Promise(r => setTimeout(r, 700))]).then(loaded);
  else loaded();

  /* pranešimas */
  const toastEl = $('.toast');
  let toastT;
  const toast = msg => {
    if (!toastEl) return;
    toastEl.textContent = msg;
    toastEl.classList.add('is-on');
    clearTimeout(toastT);
    toastT = setTimeout(() => toastEl.classList.remove('is-on'), 3200);
  };

  /* antraštė: permatoma virš hero, vientisa toliau */
  const hdr = $('[data-hdr]');
  const hero = $('.hero');
  if (hdr && hero && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver(([e]) => hdr.classList.toggle('is-solid', !e.isIntersecting), { rootMargin: '-72px 0px 0px 0px' });
    io.observe(hero);
  } else if (hdr) hdr.classList.add('is-solid');

  /* išskleidžiamas paslaugų meniu */
  $$('.nav__item--drop').forEach(item => {
    const btn = $('.nav__btn', item);
    let t;
    const set = v => { btn.setAttribute('aria-expanded', String(v)); item.classList.toggle('is-open', v); };
    btn.addEventListener('click', () => set(btn.getAttribute('aria-expanded') !== 'true'));
    item.addEventListener('mouseenter', () => { clearTimeout(t); if (matchMedia('(hover: hover)').matches) set(true); });
    item.addEventListener('mouseleave', () => { t = setTimeout(() => set(false), 140); });
    item.addEventListener('keydown', e => { if (e.key === 'Escape') { set(false); btn.focus(); } });
    item.addEventListener('focusout', e => { if (!item.contains(e.relatedTarget)) set(false); });
    d.addEventListener('click', e => { if (!item.contains(e.target)) set(false); });
  });

  /* mobilus meniu */
  const burger = $('.burger'), mnav = $('#mnav');
  const setMenu = open => {
    if (!burger) return;
    burger.setAttribute('aria-expanded', String(open));
    burger.setAttribute('aria-label', open ? 'Uždaryti meniu' : 'Atidaryti meniu');
    mnav.hidden = !open;
    html.classList.toggle('menu-open', open);
  };
  burger && burger.addEventListener('click', () => setMenu(burger.getAttribute('aria-expanded') !== 'true'));
  d.addEventListener('keydown', e => { if (e.key === 'Escape' && html.classList.contains('menu-open')) { setMenu(false); burger.focus(); } });
  mnav && mnav.addEventListener('click', e => { if (e.target.closest('a')) setMenu(false); });

  /* kalbos (demo) */
  $$('[data-lang]').forEach(b => b.addEventListener('click', () => toast(`${b.dataset.lang} versija bus perkelta kitame etape. Demo rodoma lietuviškai.`)));

  /* atsiradimai */
  if (!calm && 'IntersectionObserver' in window) {
    const ro = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('in'); ro.unobserve(e.target); }
    }), { rootMargin: '0px 0px -8% 0px', threshold: .06 });
    $$('.reveal').forEach(el => ro.observe(el));
  } else $$('.reveal').forEach(el => el.classList.add('in'));

  /* skaičiai */
  const fmt = n => Math.round(n).toLocaleString('lt-LT').replace(/\s/g, ' ');
  if (!calm && 'IntersectionObserver' in window) {
    const co = new IntersectionObserver(es => es.forEach(e => {
      if (!e.isIntersecting) return;
      co.unobserve(e.target);
      const el = e.target, to = +el.dataset.count, t0 = performance.now(), dur = 1500;
      const step = now => {
        const k = Math.min(1, (now - t0) / dur), ease = 1 - Math.pow(1 - k, 4);
        el.textContent = fmt(to * ease);
        if (k < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    }), { threshold: .6 });
    $$('[data-count]').forEach(el => { el.textContent = '0'; co.observe(el); });
  }

  /* video: įkeliama ir rodoma tik matomoje srityje */
  const loadVid = v => {
    if (v.dataset.loaded) return;
    $$('source', v).forEach(s => { if (s.dataset.src) s.src = s.dataset.src; });
    v.load();
    v.dataset.loaded = '1';
  };
  const canPlay = v => !calm && !v.dataset.userPaused && !v.closest('[data-svc-frame]:not(.is-on), [data-cond-frame]:not(.is-on)');
  const play = v => { loadVid(v); const p = v.play(); if (p && p.catch) p.catch(() => {}); };
  const vids = $$('video[data-auto]');
  vids.forEach(v => v.addEventListener('playing', () => v.classList.add('is-playing')));
  if ('IntersectionObserver' in window) {
    const vo = new IntersectionObserver(es => es.forEach(e => {
      const v = e.target;
      v._vis = e.isIntersecting;
      if (e.isIntersecting && canPlay(v)) play(v);
      else if (!e.isIntersecting && !v.paused) v.pause();
    }), { rootMargin: '160px 0px', threshold: .01 });
    vids.forEach(v => vo.observe(v));
  }
  d.addEventListener('visibilitychange', () => {
    vids.forEach(v => { if (d.hidden) v.pause(); else if (v._vis && canPlay(v)) play(v); });
  });

  /* hero video valdymas (WCAG 2.2.2) */
  const ctl = $('[data-vidctl]'), hv = $('video[data-hero]');
  if (ctl && hv) {
    const icon = $('i', ctl);
    const sync = paused => {
      icon.className = 'ph ' + (paused ? 'ph-play' : 'ph-pause');
      ctl.setAttribute('aria-label', paused ? 'Paleisti foninį vaizdo įrašą' : 'Sustabdyti foninį vaizdo įrašą');
      ctl.setAttribute('aria-pressed', String(paused));
    };
    if (calm) sync(true);
    ctl.addEventListener('click', () => {
      if (hv.paused) { delete hv.dataset.userPaused; play(hv); sync(false); }
      else { hv.pause(); hv.dataset.userPaused = '1'; sync(true); }
    });
  }

  /* paslaugų rodyklė: užvedus keičiasi video */
  const frames = $$('[data-svc-frame]');
  const svcLinks = $$('[data-svc]');
  const activate = a => {
    const i = a.dataset.svc;
    svcLinks.forEach(x => x.classList.toggle('is-active', x === a));
    frames.forEach(f => {
      const on = f.dataset.svcFrame === i, v = $('video', f);
      f.classList.toggle('is-on', on);
      if (!v) return;
      if (on && !calm) play(v); else v.pause();
    });
  };
  if (svcLinks.length) {
    svcLinks[0].classList.add('is-active');
    svcLinks.forEach(a => { a.addEventListener('mouseenter', () => activate(a)); a.addEventListener('focus', () => activate(a)); });
  }

  /* sąlygos: pasirinkus sąlygą keičiasi nuotrauka / video */
  const cond = $('[data-cond]');
  if (cond) {
    const btns = $$('[data-cond-i]', cond), cframes = $$('[data-cond-frame]', cond);
    const pick = b => {
      const i = b.dataset.condI;
      btns.forEach(x => { const on = x === b; x.setAttribute('aria-pressed', String(on)); x.parentElement.classList.toggle('is-on', on); });
      cframes.forEach(f => {
        const on = f.dataset.condFrame === i, v = $('video', f);
        f.classList.toggle('is-on', on);
        if (v) { if (on && !calm) play(v); else v.pause(); }
      });
    };
    btns.forEach(b => {
      b.addEventListener('click', () => pick(b));
      b.addEventListener('mouseenter', () => { if (matchMedia('(hover: hover)').matches) pick(b); });
    });
  }

  /* karuselė */
  const track = $('[data-track]');
  if (track) {
    const prev = $('[data-track-prev]'), next = $('[data-track-next]');
    const step = () => { const c = $('.pcard', track); return c ? c.getBoundingClientRect().width + parseFloat(getComputedStyle(track).columnGap || 20) : 320; };
    const go = dir => track.scrollBy({ left: dir * step(), behavior: calm ? 'auto' : 'smooth' });
    prev.addEventListener('click', () => go(-1));
    next.addEventListener('click', () => go(1));
    const bar = $('[data-track-bar]');
    const ends = () => {
      const max = track.scrollWidth - track.clientWidth;
      prev.disabled = track.scrollLeft < 8;
      next.disabled = track.scrollLeft > max - 8;
      if (bar) {
        const size = Math.max(.12, track.clientWidth / track.scrollWidth);
        bar.style.setProperty('--size', (size * 100) + '%');
        bar.style.setProperty('--pos', (max > 0 ? track.scrollLeft / max * (1 / size - 1) * 100 : 0) + '%');
      }
    };
    window.addEventListener('resize', ends);
    /* tempimas pele (tik pelė; liečiant veikia natūralus slinkimas) */
    let dx0 = 0, sl0 = 0, moved = false, down = false;
    track.addEventListener('pointerdown', e => {
      if (e.pointerType !== 'mouse' || e.button !== 0) return;
      down = true; moved = false; dx0 = e.clientX; sl0 = track.scrollLeft;
    });
    window.addEventListener('pointermove', e => {
      if (!down) return;
      const dx = e.clientX - dx0;
      if (!moved && Math.abs(dx) > 6) { moved = true; track.classList.add('is-drag'); }
      if (moved) track.scrollLeft = sl0 - dx;
    });
    window.addEventListener('pointerup', () => {
      if (!down) return;
      down = false;
      if (moved) {
        track.classList.remove('is-drag');
        const w = step(), target = Math.round(track.scrollLeft / w) * w;
        track.scrollTo({ left: target, behavior: calm ? 'auto' : 'smooth' });
        track.addEventListener('click', ev => { ev.stopPropagation(); ev.preventDefault(); }, { capture: true, once: true });
      }
    });
    track.addEventListener('scroll', () => { cancelAnimationFrame(track._r); track._r = requestAnimationFrame(ends); }, { passive: true });
    ends();
  }

  /* nuotraukų peržiūra */
  const lb = $('#lb');
  if (lb) {
    const img = $('.lb__img', lb), cap = $('.lb__cap', lb), cnt = $('.lb__count', lb), thumbs = $('.lb__thumbs', lb);
    const bPrev = $('[data-lb="prev"]', lb), bNext = $('[data-lb="next"]', lb), bClose = $('[data-lb="close"]', lb);
    let list = [], caps = [], idx = 0, last = null;
    const show = i => {
      idx = (i + list.length) % list.length;
      img.src = list[idx];
      img.alt = caps[idx] || '';
      cap.textContent = caps[idx] || '';
      cnt.textContent = list.length > 1 ? `${idx + 1} / ${list.length}` : '';
      if (list.length > 1) { const pre = new Image(); pre.src = list[(idx + 1) % list.length]; }
      $$('.lb__t', thumbs).forEach((t, k) => {
        t.setAttribute('aria-current', String(k === idx));
        if (k === idx) t.scrollIntoView({ block: 'nearest', inline: 'center', behavior: calm ? 'auto' : 'smooth' });
      });
    };
    const small = src => src.replace(/(-800)?\.webp$/, '-800.webp');
    const thumbHtml = (s, k) => '<button class="lb__t" type="button" data-k="' + k + '" aria-label="Nuotrauka ' + (k + 1) + '"><img src="' + small(s) + '" alt="" loading="lazy"></button>';
    const open = (srcs, captions, start) => {
      list = srcs; caps = captions; last = d.activeElement;
      bPrev.hidden = bNext.hidden = list.length < 2;
      thumbs.hidden = list.length < 2;
      thumbs.innerHTML = list.length < 2 ? '' : list.map(thumbHtml).join('');
      lb.hidden = false;
      html.classList.add('lb-open');
      show(start);
      requestAnimationFrame(() => lb.classList.add('is-open'));
      bClose.focus();
    };
    const close = () => {
      lb.classList.remove('is-open');
      lb.hidden = true;
      html.classList.remove('lb-open');
      img.removeAttribute('src');
      last && last.focus();
    };
    d.addEventListener('click', e => {
      const t = e.target.closest('[data-gallery]');
      if (!t) return;
      e.preventDefault();
      const srcs = t.dataset.gallery.split('|').filter(Boolean);
      if (!srcs.length) return;
      const captions = t.dataset.captions ? t.dataset.captions.split('|') : srcs.map(() => t.dataset.caption || '');
      open(srcs, captions, +(t.dataset.start || 0));
    });
    thumbs.addEventListener('click', e => { const t = e.target.closest('.lb__t'); if (t) show(+t.dataset.k); });
    bPrev.addEventListener('click', () => show(idx - 1));
    bNext.addEventListener('click', () => show(idx + 1));
    bClose.addEventListener('click', close);
    lb.addEventListener('click', e => { if (e.target === lb || e.target.classList.contains('lb__stage')) close(); });
    d.addEventListener('keydown', e => {
      if (lb.hidden) return;
      if (e.key === 'Escape') close();
      else if (e.key === 'ArrowLeft' && list.length > 1) show(idx - 1);
      else if (e.key === 'ArrowRight' && list.length > 1) show(idx + 1);
      else if (e.key === 'Tab') {
        const f = [...$$('.lb__t', thumbs), bPrev, bNext, bClose].filter(b => !b.hidden);
        const i = f.indexOf(d.activeElement);
        e.preventDefault();
        f[(i + (e.shiftKey ? -1 : 1) + f.length) % f.length].focus();
      }
    });
    let x0 = null;
    lb.addEventListener('touchstart', e => { x0 = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', e => {
      if (x0 === null || list.length < 2) return;
      const dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 50) show(idx + (dx < 0 ? 1 : -1));
      x0 = null;
    });
  }

  /* galerija: rodyti visas */
  $$('[data-gal-more]').forEach(b => b.addEventListener('click', () => {
    const g = b.previousElementSibling;
    g.classList.add('gal--all');
    $$('.is-more', g).forEach(el => el.classList.add('in'));
    b.hidden = true;
  }));

  /* projektų filtras */
  const pl = $('[data-plist]');
  if (pl) {
    const rows = $$('.prow', pl), yrs = $$('[data-yr]', pl);
    const out = $('[data-count-out]', pl), empty = $('[data-empty]', pl), q = $('[data-q]', pl), ph = $('[data-ph]', pl);
    const segs = $$('[data-status]', pl), chips = $$('[data-cat]', pl), clear = $('[data-clear]', pl);
    const norm = s => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
    rows.forEach(r => { r._t = norm(r.dataset.text); r._c = r.dataset.cats.split(' '); });
    const params = new URLSearchParams(location.search);
    let st = ['vykdomi', 'atlikti'].includes(params.get('b')) ? params.get('b') : 'all';
    let cat = chips.some(c => c.dataset.cat === params.get('k')) ? params.get('k') : 'all';
    const apply = () => {
      const qq = norm(q.value.trim());
      let n = 0;
      rows.forEach(r => {
        const ok = (st === 'all' || r.dataset.st === st) && (cat === 'all' || r._c.includes(cat)) && (!qq || r._t.includes(qq)) && (!ph.checked || r.dataset.ph === '1');
        r.hidden = !ok;
        if (ok) n++;
      });
      yrs.forEach(y => { y.hidden = !$$('.prow', y).some(r => !r.hidden); });
      out.textContent = `Rodoma ${n} iš ${rows.length}`;
      empty.hidden = n > 0;
      segs.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.status === st)));
      chips.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.cat === cat)));
      clear.hidden = st === 'all' && cat === 'all' && !qq && !ph.checked;
    };
    segs.forEach(b => b.addEventListener('click', () => { st = b.dataset.status; apply(); }));
    chips.forEach(b => b.addEventListener('click', () => { cat = b.dataset.cat; apply(); }));
    let qt;
    q.addEventListener('input', () => { clearTimeout(qt); qt = setTimeout(apply, 120); });
    ph.addEventListener('change', apply);
    const reset = () => { st = 'all'; cat = 'all'; q.value = ''; ph.checked = false; apply(); };
    $('[data-reset]', pl).addEventListener('click', reset);
    clear.addEventListener('click', reset);
    apply();
  }

  /* el. pašto kopijavimas */
  $$('[data-copy]').forEach(b => b.addEventListener('click', () => {
    const v = b.dataset.copy;
    (navigator.clipboard ? navigator.clipboard.writeText(v) : Promise.reject()).then(() => toast('El. pašto adresas nukopijuotas'), () => toast(v));
  }));

  /* demonstracinė forma */
  const form = $('[data-form]');
  if (form) {
    const fName = $('#f-name', form), fTel = $('#f-tel', form), fMail = $('#f-mail', form), fMsg = $('#f-msg', form);
    const mark = (input, bad, errId) => {
      const f = input.closest('.field');
      f.classList.toggle('is-err', bad);
      input.setAttribute('aria-invalid', String(bad));
      if (bad) input.setAttribute('aria-describedby', errId); else input.removeAttribute('aria-describedby');
      return bad;
    };
    form.addEventListener('submit', e => {
      e.preventDefault();
      const mailOk = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(fMail.value.trim());
      const telOk = fTel.value.replace(/\D/g, '').length >= 8;
      const errs = [
        mark(fName, !fName.value.trim(), 'f-name-err') && fName,
        mark(fMail, !(mailOk || (telOk && !fMail.value.trim())), 'f-mail-err') && fMail,
        mark(fMsg, fMsg.value.trim().length < 5, 'f-msg-err') && fMsg,
      ].filter(Boolean);
      if (errs.length) { errs[0].focus(); return; }
      const ok = $('.form__ok', form);
      ok.hidden = false;
      form.reset();
      ok.focus && ok.setAttribute('tabindex', '-1');
      ok.focus();
    });
  }
})();
