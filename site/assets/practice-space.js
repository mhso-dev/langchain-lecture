(() => {
  const panel = document.querySelector('[data-practice]');
  if (!panel) return;
  const result = panel.querySelector('output');
  const control = panel.querySelector('input, select');
  const key = panel.dataset.practice;
  function records(value) {
    const rows = [{minutes:30, done:true}, {minutes:20, done:false}, {minutes:40, done:true}];
    const total = rows.filter(row => row.done && row.minutes >= value).reduce((sum, row) => sum + row.minutes, 0);
    return 'done이 True이고 minutes ≥ '+value+'인 기록의 합계는 '+total+'분입니다.';
  }
  function ranking(k) {
    return '기대 문서는 2위입니다. k = '+k+'일 때 Recall@k = '+(k>=2?'1':'0')+', 상위 k 안에서 계산한 첫 적중 순위의 역수 = '+(k>=2?'0.5':'0')+'입니다.';
  }
  function rerank(mode) {
    const candidates = [
      { id: 'library-1:1', text: '.', containsLoan: false },
      { id: 'library-1:0', text: '도서 대출 기간은 14일입니다', containsLoan: true }
    ];
    const ranked = candidates.slice();
    if (mode === 'on') ranked.sort((a, b) => Number(b.containsLoan) - Number(a.containsLoan));
    const items = ranked.map((doc) => {
      const item = document.createElement('li');
      const id = document.createElement('code');
      id.textContent = doc.id;
      item.append(id, '　', doc.text);
      return item;
    });
    panel.querySelector('.ranked-documents').replaceChildren(...items);
    return '1위 ' + ranked[0].id + ' · 후보 2건 · 정렬 키는 본문에 ‘대출’이 있는지 여부입니다.';
  }
  function memory(n) {
    const turns=['장소 · 회의실 B','언어 · 한국어','기한 · 금요일 18시','분량 · 5장'];
    return 'turns[-'+n+':]에 남는 발화　'+turns.slice(-n).join(' / ');
  }
  function switches(n) {
    return '같은 완료 요청 '+n+'회　/　토글 방식 '+(n%2?'True':'False')+'　/　목표값 대입 '+(n?'True':'False');
  }
  function latency(wait) {
    return '합성 예시 · 대기 '+wait+' ms + 처리 3.5 ms = 전체 '+(wait+3.5)+' ms';
  }
  function retry(state) {
    const [docs,attempts]=state.split(',').map(Number),dest=docs?'답변':attempts<2?'재검색':'종료';
    return 'documents 길이 '+docs+' · attempts '+attempts+' → '+dest;
  }
  function session(owner) {
    return 'sessions[("'+owner+'", "main")] → ["RULE-'+(owner==='alice'?'A':'B')+'"]';
  }
  function accumulator(mode) {
    let sum=0;
    const totals=[30,20,40].map(n=>{ if(mode==='inside')sum=0; sum+=n; return sum; });
    return '각 반복이 끝난 직후의 total = '+totals.join(' → ')+'분입니다.';
  }
  function classify(question) {
    const billing=question.includes('영수증'), technical=question.includes('오류');
    const route=billing===technical?'clarify':billing?'billing':'technical';
    return '영수증 단서 '+Number(billing)+'개, 오류 단서 '+Number(technical)+'개 → '+route+
      '. 안내 작성 함수 호출은 '+(route==='clarify'?0:1)+'회입니다.';
  }
  function messageIds(mode) {
    const messages=[['h1','대출 기간은?'],['a1','답변 초안']];
    const incoming=[mode==='new'?'a2':'a1','수정 답변'];
    const result=mode==='plain'?[incoming]:messages.map(row=>row.slice());
    if(mode!=='plain'){
      const index=result.findIndex(row=>row[0]===incoming[0]);
      if(index<0)result.push(incoming);else result[index]=incoming;
    }
    return '기존 [h1, a1]에 '+incoming[0]+' 수신 → ['+result.map(row=>row[0]).join(', ')+']. 수정 답변을 포함한 메시지는 총 '+result.length+'개입니다.';
  }
  function approvals(choice) {
    const status=choice==='wait'?'승인 대기':choice==='approve'?'completed':'declined';
    if(choice==='wait') return '__interrupt__에 대기 중인 요청이 있습니다. status는 아직 설정되지 않았고 등록은 0건입니다.';
    return '결정 전달 뒤 status = '+status+'. 등록된 문의는 '+Number(choice==='approve')+'건입니다.';
  }
  function publish(choice) {
    const [event,ref,check]=choice.split('|');
    const allowed=event==='push'&&ref==='main'&&check==='pass';
    return event+' · '+ref+' · 검사 '+(check==='pass'?'성공':'실패')+' → publish '+(allowed?'실행':'생략')+'.';
  }
  function wrapping(width) {
    panel.querySelector('.wrapping-example').style.width = width + 'px';
    const wraps = 180 + 10 + 100 > width;
    return '입력 180px + 간격 10px + 버튼 100px = 290px. 설정한 폭 ' + width +
      'px에서 버튼은 ' + (wraps ? '둘째' : '첫째') + ' 줄에 배치됩니다.';
  }
  function substring(needle) {
    const titles = ['복습 50%', '복습 마무리'];
    return titles.map(title => '「' + title + '」 → ' + (title.indexOf(needle) + 1)).join('　/　') +
      ' · instr()의 결과는 첫 글자가 1, 일치하는 문자열이 없으면 0입니다.';
  }
  function equipment(question) {
    const found=['A','B'].filter(id=>question.includes('장비 '+id));
    const selected=found.length===1?found[0]==='A'?0:1:2;
    return selected===2?'장비가 하나로 정해지지 않아 추가 질문을 합니다.':
      '장비 '+found[0]+'만 일치해 점검 안내를 돌려줍니다.'+(question.includes('교체')?' 이 규칙은 교체 일정이라는 의도를 검사하지 않아 오답입니다.':'');
  }
  function regexBoundary(input) {
    const output = input.replace(/장비([AB])(?=$|[^A-Za-z0-9])/g, '장비 $1');
    return '입력 「' + input + '」 → 출력 「' + output + '」 · ' +
      (output === input ? '경계 조건을 만족하지 않아 원문을 유지합니다.' : '장비명과 영문자 사이에 공백을 삽입했습니다.');
  }
  function taskDenominator(fourth) {
    const outcomes=['success','failed','aborted',fourth];
    const attempts=outcomes.filter(s=>s!=='not_started'), wins=attempts.filter(s=>s==='success');
    return '성공 '+wins.length+'건 / 실제 시작 '+attempts.length+'건 = '+(100*wins.length/attempts.length).toFixed(1)+'%. 중단한 과업도 시작 횟수에 포함합니다.';
  }
  const draw={accumulator,classify,messageIds,approvals,publish,wrapping,substring,equipment,regexBoundary,taskDenominator,records,ranking,rerank,memory,switches,latency,retry,session};
  function update() {
    const value=control.type==='range'?Number(control.value):control.value;
    result.textContent=draw[key](value);
    const badge=panel.querySelector('.practice-value');
    if(badge) badge.textContent=value;
  }
  control.addEventListener('input',update);
  update();
})();
