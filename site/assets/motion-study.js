/* Read one lossless frame atlas only as its illustration approaches the reader. */
function mountStudy(figure) {
  const canvas = figure.querySelector('canvas');
  const context = canvas.getContext('2d');
  if (!context) return;
  const viewport = figure.querySelector('.motion-viewport');
  const choices = figure.querySelector('.motion-choices');
  const controls = figure.querySelector('.motion-tools');
  const button = controls.querySelector('button');
  const slider = controls.querySelector('input');
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const frames = Number(figure.dataset.frames);
  const cols = Number(figure.dataset.cols);
  const duration = Number(figure.dataset.duration);
  const sheet = new Image();
  let ready = false, visible = false, started = false;
  let frame = 0, request = 0, origin = 0;

  function draw(index) {
    frame = index;
    const w = canvas.width, h = canvas.height;
    context.drawImage(sheet,(index % cols)*w,Math.floor(index/cols)*h,w,h,0,0,w,h);
    slider.value = String(index);
    slider.setAttribute('aria-valuetext', Math.round(index/(frames-1)*100)+'%');
    canvas.hidden = false;
    choices?.querySelectorAll('[data-frame]').forEach(choice => {
      choice.setAttribute('aria-pressed', String(Number(choice.dataset.frame) === index));
    });
  }
  function stop() {
    cancelAnimationFrame(request);
    request = 0;
    button.textContent = frame === frames-1 ? '다시 보기' : '재생';
  }
  function tick(now) {
    const index = Math.min(frames-1,Math.floor((now-origin)/duration*(frames-1)));
    if (frame !== index) draw(index);
    if (frame === frames-1) stop();
    else request = requestAnimationFrame(tick);
  }
  function play() {
    if (!ready || request) return;
    started = true;
    if (frame === frames-1) draw(0);
    origin = performance.now()-duration*frame/(frames-1);
    button.textContent = '일시 정지';
    request = requestAnimationFrame(tick);
  }
  function maybePlay() {
    if (ready && visible && !started && !motion.matches) play();
  }
  sheet.onload = () => {
    ready = true;
    draw(motion.matches ? frames-1 : 0);
    controls.hidden = false;
    if (choices) choices.hidden = false;
    stop();
    maybePlay();
  };
  choices?.addEventListener('click', event => {
    const choice = event.target.closest('[data-frame]');
    if (!choice) return;
    started = true;
    draw(Number(choice.dataset.frame));
    stop();
  });
  const zoom = figure.querySelector('.motion-zoom');
  zoom.addEventListener('click', () => {
    const expanded = viewport.classList.toggle('enlarged');
    zoom.setAttribute('aria-pressed', String(expanded));
    zoom.textContent = expanded ? '원래 크기' : '크게 보기';
    if (expanded) {
      viewport.tabIndex = 0;
      viewport.setAttribute('aria-label','확대한 그림. 좌우로 움직여 확인하세요.');
    } else {
      viewport.removeAttribute('tabindex');
      viewport.removeAttribute('aria-label');
    }
  });
  button.addEventListener('click', () => request ? stop() : play());
  slider.addEventListener('input', () => { started = true; draw(Number(slider.value)); stop(); });
  motion.addEventListener('change', () => {
    if (ready && motion.matches) { stop(); draw(frames-1); stop(); }
  });
  const observer = new IntersectionObserver(([entry]) => {
    visible = entry.isIntersecting;
    if (visible && !sheet.src) sheet.src = figure.dataset.sheet;
    if (visible) maybePlay();
    else if (request) stop();
  },{threshold:0.15});
  observer.observe(viewport);
}
document.querySelectorAll('.motion-study').forEach(mountStudy);
