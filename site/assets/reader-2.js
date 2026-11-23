/* Precise GIF scenes are opt-in; step stills and transcripts are always available. */
document.addEventListener('DOMContentLoaded', () => {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  document.querySelectorAll('[data-motion]').forEach(lab => {
    const img=lab.querySelector('.motion-screen img'), steps=[...lab.querySelectorAll('[data-motion-step]')];
    const play=lab.querySelector('[data-motion-action="play"]'), status=lab.querySelector('.motion-status'), note=lab.querySelector('.motion-note');
    let current=0, timer=null, started=0;
    const seconds=Number(lab.dataset.seconds);
    function update(){
      steps.forEach((b,i)=>b.setAttribute('aria-pressed',String(i===current)));
      status.textContent=`${current+1} / ${steps.length} · ${steps[current].dataset.title}`;
      note.textContent=steps[current].dataset.note;
    }
    function stop(){clearInterval(timer);timer=null;play.setAttribute('aria-pressed','false');play.textContent='움직임 재생';img.src=steps[current].dataset.frame;img.alt=steps[current].dataset.title+'。'+steps[current].dataset.note;update();}
    steps.forEach((b,i)=>b.addEventListener('click',()=>{current=i;stop();}));
    play.addEventListener('click',()=>{
      if(timer){stop();return;}
      if(reduced.matches){status.textContent='동작 줄이기 설정이 켜져 있습니다. 단계 버튼이나 정지 그림으로 읽어 주세요.';return;}
      current=0;update();started=performance.now();img.src=img.dataset.animation;img.alt=lab.querySelector('h3').textContent+' 설명 애니메이션';
      play.setAttribute('aria-pressed','true');play.textContent='움직임 정지';
      timer=setInterval(()=>{const next=Math.min(steps.length-1,Math.floor((performance.now()-started)/1000/seconds));if(next!==current){current=next;update();}if(performance.now()-started>=steps.length*seconds*1000){stop();}},150);
    });
    lab.querySelector('[data-motion-action="stop"]').addEventListener('click',stop);
    lab.querySelector('[data-motion-action="reset"]').addEventListener('click',()=>{current=0;stop();});
    reduced.addEventListener('change',()=>{if(reduced.matches)stop();});
    document.addEventListener('visibilitychange',()=>{if(document.hidden&&timer)stop();});
  });
  document.querySelectorAll('video').forEach(v=>{v.autoplay=false;reduced.addEventListener('change',()=>{if(reduced.matches)v.pause();});});
});
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

/* Teaching films: native playback, exact scene seeking, no autoplay. */
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('[data-teaching-video]').forEach(lab => {
    const video=lab.querySelector('video');
    const buttons=[...lab.querySelectorAll('[data-seek]')];
    const update=()=>{
      let active=0;
      buttons.forEach((b,i)=>{if(video.currentTime>=Number(b.dataset.seek))active=i;});
      buttons.forEach((b,i)=>b.setAttribute('aria-pressed', String(i===active)));
    };
    // Some local preview servers omit byte-range support. A local blob preserves seeking.
    let seekReady=null;
    const prepareSeeking=()=>{
      if(video.seekable.length && video.seekable.end(video.seekable.length-1)>0) return Promise.resolve();
      if(!seekReady) seekReady=(async()=>{
        const response=await fetch(video.currentSrc || video.querySelector('source').src);
        if(!response.ok) throw new Error('영상 파일을 읽지 못했습니다.');
        const blob=await response.blob();
        await new Promise((resolve,reject)=>{
          video.addEventListener('loadedmetadata',resolve,{once:true});
          video.addEventListener('error',reject,{once:true});
          video.src=URL.createObjectURL(blob); video.load();
        });
      })().catch(error=>{seekReady=null;throw error;});
      return seekReady;
    };
    buttons.forEach(button=>button.addEventListener('click',async()=>{
      video.pause();
      try {
        await prepareSeeking();
        video.currentTime=Number(button.dataset.seek)+0.05;update();
      } catch {
        lab.querySelector('.motion-transcript').open=true;
        lab.querySelector('.teaching-controls p').textContent='장면 이동을 사용할 수 없습니다. 아래 정지 화면과 설명을 펼쳤습니다.';
      }
    }));
    lab.querySelector('select').addEventListener('change',event=>{video.playbackRate=Number(event.target.value);});
    video.addEventListener('timeupdate',update);update();
    document.addEventListener('visibilitychange',()=>{if(document.hidden)video.pause();});
  });
});
/* SVG learning pictures: offline, paused on entry, explicit movement only. */
document.addEventListener('DOMContentLoaded', () => {
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');
  document.querySelectorAll('[data-svg-learning]').forEach(lab=>{
    const svg=lab.querySelector('svg'), viewport=lab.querySelector('.svg-viewport');
    const steps=[...lab.querySelectorAll('[data-svg-step]')];
    const slider=lab.querySelector('input[type=range]'), status=lab.querySelector('.svg-status'), caption=lab.querySelector('.svg-caption');
    const play=lab.querySelector('[data-svg-action=play]'), replay=lab.querySelector('[data-svg-action=step]');
    const total=Number(lab.dataset.duration), stepSeconds=total/steps.length;
    let selected=0, playing=false, frame=null, stopAt=total-.01;
    const gif=lab.querySelector('.gif-alternative'), img=gif.querySelector('img');
    const gifState=()=>{img.src=gif.open&&!reduced.matches?img.dataset.gif:img.dataset.still;};
    gif.addEventListener('toggle',gifState);reduced.addEventListener('change',gifState);
    if(typeof svg.pauseAnimations!=='function'){
      lab.querySelectorAll('.svg-controls button,.svg-controls select,.svg-step-buttons button,.svg-scrub input').forEach(control=>{control.disabled=true;});
      status.textContent='현재 브라우저에서는 SVG 움직임을 제어할 수 없습니다. 아래 정지 그림과 설명을 읽거나 GIF를 펼쳐 보세요.';
      lab.querySelector('.motion-transcript').open=true;
      return;
    }
    svg.pauseAnimations();svg.setCurrentTime(0);viewport.classList.add('svg-ready');
    function update(){
      const t=Math.min(svg.getCurrentTime(),total-.01);
      const next=Math.min(steps.length-1,Math.floor(t/stepSeconds));
      selected=next;slider.value=String(t);
      steps.forEach((b,i)=>b.setAttribute('aria-pressed',String(i===selected)));
      const message=`${selected+1} / ${steps.length} · ${steps[selected].dataset.title}`;
      if(status.textContent!==message)status.textContent=message;
      caption.textContent=steps[selected].dataset.caption;
      lab.querySelector('[data-svg-action=previous]').disabled=selected===0;
      lab.querySelector('[data-svg-action=next]').disabled=selected===steps.length-1;
    }
    function pause(){svg.pauseAnimations();playing=false;cancelAnimationFrame(frame);play.textContent='전체 재생';update();}
    function seek(t){pause();svg.setCurrentTime(Math.max(0,Math.min(total-.01,t)));update();}
    function tick(){
      if(!playing)return;
      if(svg.getCurrentTime()>=stopAt){seek(stopAt);return;}
      update();frame=requestAnimationFrame(tick);
    }
    function start(until){if(reduced.matches)return;stopAt=until;playing=true;play.textContent='재생 중';svg.unpauseAnimations();frame=requestAnimationFrame(tick);}
    lab.querySelectorAll('[data-svg-action]').forEach(button=>button.addEventListener('click',()=>{
      const action=button.dataset.svgAction;
      if(action==='pause')return pause();
      if(action==='reset')return seek(0);
      if(action==='previous')return seek(Math.max(0,selected)*stepSeconds-.01);
      if(action==='next')return seek((selected+2)*stepSeconds-.01);
      if(action==='step'){const i=selected;seek(i*stepSeconds);start((i+1)*stepSeconds-.01);return;}
      if(action==='play'){
        if(playing)return pause();
        seek(0);
        start(total-.01);
      }
    }));
    steps.forEach((b,i)=>b.addEventListener('click',()=>seek((i+1)*stepSeconds-.01)));
    slider.addEventListener('input',()=>seek(Number(slider.value)));
    lab.querySelector('select').addEventListener('change',event=>{svg.style.width=Number(event.target.value)*100+'%';});
    function motionPreference(){pause();play.disabled=reduced.matches;replay.disabled=reduced.matches;}
    reduced.addEventListener('change',motionPreference);motionPreference();
    document.addEventListener('visibilitychange',()=>{if(document.hidden)pause();});
    update();
  });
});
