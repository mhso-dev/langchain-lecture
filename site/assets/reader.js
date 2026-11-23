/* Progressive enhancement: core content is already rendered in the HTML. */
(() => {
  'use strict';
  document.documentElement.classList.add('js');
  let toastTimer;
  const toast = message => {
    const el = document.querySelector('.toast');
    el.textContent = message;
    el.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => el.classList.remove('show'), 2400);
  };
  document.querySelectorAll('[data-copy]').forEach(button => {
    button.addEventListener('click', async () => {
      const source = document.getElementById(button.dataset.copy).textContent;
      try {
        if (!navigator.clipboard) throw new Error('Clipboard unavailable');
        await navigator.clipboard.writeText(source);
      } catch {
        const field = document.createElement('textarea');
        field.value = source;
        field.style.cssText = 'position:fixed;left:-9999px;top:0';
        document.body.append(field);
        field.select();
        const copied = document.execCommand('copy');
        field.remove();
        button.focus();
        if (!copied) { toast('코드를 선택한 뒤 직접 복사해 주세요.'); return; }
      }
      button.textContent = '복사됨';
      toast('코드를 복사했어요.');
      setTimeout(() => { button.textContent = '복사'; }, 2000);
    });
  });
  const menu = document.querySelector('.menu-button');
  const sidebar = document.querySelector('.sidebar');
  const closeMenu = () => { sidebar.classList.remove('open'); menu.setAttribute('aria-expanded', 'false'); };
  menu.addEventListener('click', () => {
    const open = sidebar.classList.toggle('open');
    menu.setAttribute('aria-expanded', String(open));
  });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeMenu(); });
  document.addEventListener('click', e => { if (!sidebar.contains(e.target) && !menu.contains(e.target)) closeMenu(); });
  document.querySelectorAll('.sidebar nav a').forEach(link => link.addEventListener('click', closeMenu));
  const sections = [...document.querySelectorAll('.lesson-section')];
  const links = [...document.querySelectorAll('.sidebar nav a')];
  const updateReading = () => {
    const total = document.documentElement.scrollHeight - innerHeight;
    const progress = total > 0 ? Math.max(0, Math.min(100, Math.round(scrollY / total * 100))) : 100;
    document.querySelector('.reading-track span').style.width = `${progress}%`;
    document.querySelector('.reading-label').textContent = `읽기 진행 ${progress}%`;
    let active = sections[0]?.id;
    for (const s of sections) if (s.getBoundingClientRect().top <= 180) active = s.id;
    links.forEach(link => {
      const chosen = link.hash === '#' + active;
      link.classList.toggle('active', chosen);
      if (chosen) link.setAttribute('aria-current', 'location'); else link.removeAttribute('aria-current');
    });
  };
  let scheduled = false;
  addEventListener('scroll', () => { if (!scheduled) { scheduled = true; requestAnimationFrame(() => { updateReading(); scheduled = false; }); } }, {passive:true});
  addEventListener('resize', updateReading);
  updateReading();
  const stopPlayers = [];
  document.querySelectorAll('[data-flow]').forEach(flow => {
    const panels = [...flow.querySelectorAll('.flow-panel')];
    const nodes = [...flow.querySelectorAll('.flow-track li')];
    const status = flow.querySelector('.flow-status');
    const previous = flow.querySelector('[data-flow-action="previous"]');
    const next = flow.querySelector('[data-flow-action="next"]');
    const play = flow.querySelector('[data-flow-action="play"]');
    let current = 0, timer = null;
    const stop = () => { clearInterval(timer); timer = null; play.textContent = '자동 재생'; play.setAttribute('aria-pressed', 'false'); };
    const render = () => {
      panels.forEach((p, i) => { p.hidden = i !== current; });
      nodes.forEach((n, i) => { n.classList.toggle('active', i === current); n.classList.toggle('done', i < current); });
      status.textContent = `${current + 1} / ${panels.length}`;
      previous.disabled = current === 0;
      next.disabled = current === panels.length - 1;
    };
    flow.querySelectorAll('[data-flow-action]').forEach(button => button.addEventListener('click', () => {
      const action = button.dataset.flowAction;
      if (action === 'play') {
        if (timer) { stop(); return; }
        if (matchMedia('(prefers-reduced-motion: reduce)').matches) {
          toast('동작 줄이기 설정에 따라 다음 단계 버튼으로 진행해 주세요.'); return;
        }
        if (current === panels.length - 1) current = 0;
        play.textContent = '일시 정지'; play.setAttribute('aria-pressed', 'true'); render();
        timer = setInterval(() => { if (current >= panels.length - 1) { stop(); return; } current++; render(); if (current === panels.length - 1) stop(); }, 2800);
        return;
      }
      stop();
      if (action === 'reset') current = 0;
      if (action === 'previous') current = Math.max(0, current - 1);
      if (action === 'next') current = Math.min(panels.length - 1, current + 1);
      render();
    }));
    stopPlayers.push(stop);
    render();
  });
  document.addEventListener('visibilitychange', () => { if (document.hidden) stopPlayers.forEach(stop => stop()); });
  let printDetails = [];
  addEventListener('beforeprint', () => {
    stopPlayers.forEach(stop => stop());
    printDetails = [...document.querySelectorAll('details')].map(el => ({el, open: el.open}));
    printDetails.forEach(x => { x.el.open = true; });
  });
  addEventListener('afterprint', () => printDetails.forEach(x => { x.el.open = x.open; }));
  document.querySelector('[data-print]').addEventListener('click', () => window.print());
})();
