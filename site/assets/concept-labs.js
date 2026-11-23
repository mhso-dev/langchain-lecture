/* Each miniature uses the values and the rule in its adjacent notebook cell. */
function mountConceptLab(lab) {
  const field = name => lab.querySelector('[data-input="' + name + '"]');
  function show(name, value) {
    const output = lab.querySelector('[data-out="' + name + '"]');
    if (output.textContent === value) return;
    output.textContent = value;
    if (!matchMedia('(prefers-reduced-motion: reduce)').matches) {
      output.animate?.([{ backgroundColor: '#ffe5a6' }, { backgroundColor: 'transparent' }], { duration: 650 });
    }
  }
  let memory = '학습자';
  let working = '초안';
  let committed = working;
  let revision = 0;
  const actions = {
    kernel(action) {
      if (action === 'assign') {
        memory = field('name').value;
        show('memory', memory);
      } else {
        show('greeting', '안녕하세요, ' + memory + '님!');
      }
    },
    return(action) {
      const returns = action === 'return';
      lab.classList.toggle('returns-value', returns);
      show('screen', returns ? '출력 없음' : '30');
      show('saved', returns ? '30' : 'None');
      show('sum', returns ? '40' : 'TypeError');
    },
    citation(action) {
      const match = action === 'right';
      show('citation', match ? 'library-1 · 1쪽' : 'library-2 · 2쪽');
      show('verdict', match ? '일치 · library-1은 대출 기간의 근거입니다.' : '불일치 · library-2는 이번 검색 결과에 없습니다.');
    },
    transaction(action) {
      if (action === 'edit') working = '수정한 초안';
      if (action === 'commit') committed = working;
      if (action === 'rollback') working = committed;
      if (action === 'reset') working = committed = '초안';
      show('working', working);
      show('committed', committed);
    },
    owner(action) {
      show('key', '(' + action + ', language)');
      show('value', action === 'alice' ? '한국어' : 'None');
    },
    stream(action) {
      show('event', action);
      show('count', action === 'done' ? '완료 확인' : '완료 미확인 · 저장 여부는 다시 조회');
    },
    percent(action) {
      const wildcard = action === 'like';
      show('last', wildcard ? '일치' : '제외');
      show('count', wildcard ? '2건' : '1건');
    },
    restore(action) {
      const same = action === 'same';
      show('body', same ? '과제함에 제출합니다.' : '제출 기한 미확인');
      show('equal', same ? '본문 일치 · True' : '본문 불일치 · False');
    },
    async digest(action) {
      const current = ++revision;
      const raw = '점검 전' + (action === 'newline' ? '\n' : ' ') + '전원 표시등을 확인합니다.';
      show('raw', raw);
      show('clean', raw.trim().split(/\s+/u).join(' '));
      if (!globalThis.crypto?.subtle) {
        show('digest', '이 브라우저에서 지문을 계산할 수 없습니다. 노트북 셀에서 확인하세요.');
        return;
      }
      const bytes = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(raw));
      if (current === revision) show('digest', Array.from(new Uint8Array(bytes), b => b.toString(16).padStart(2, '0')).join(''));
    }
  };
  lab.addEventListener('click', event => {
    const button = event.target.closest('button[data-action]');
    if (button) actions[lab.dataset.lab](button.dataset.action);
  });
  const wait = field('wait');
  if (wait) wait.addEventListener('input', () => {
    lab.style.setProperty('--wait-width', (Number(wait.value) / 15.5 * 100) + '%');
    show('wait', wait.value + 'ms');
    show('total', (Number(wait.value) + 3.5) + 'ms');
  });
  const gap = field('gap');
  if (gap) gap.addEventListener('input', () => {
    lab.querySelector('.wrap-row').style.gap = gap.value + 'px';
    show('gap', gap.value + 'px');
  });
}
document.querySelectorAll('[data-lab]').forEach(mountConceptLab);
