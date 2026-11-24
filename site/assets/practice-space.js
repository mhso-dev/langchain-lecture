/* Each scene computes its own teaching example. Its text output also works without WebGL. */
(() => {
  const panel = document.querySelector('[data-practice]');
  if (!panel) return;
  const stage = panel.querySelector('.practice-stage');
  const result = panel.querySelector('output');
  const control = panel.querySelector('input, select');
  const key = panel.dataset.practice;
  const teal = 0x22c9bb, amber = 0xffb25b, muted = 0x405573, white = 0xc6dafa;
  let renderer, scene, camera, diagram;
  const T = window.THREE;
  try {
    renderer = new T.WebGLRenderer({antialias:true, alpha:true});
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.domElement.setAttribute('aria-hidden', 'true');
    stage.append(renderer.domElement);
    scene = new T.Scene();
    camera = new T.OrthographicCamera(-6,6,2.9,-2.9,.1,80);
    camera.position.set(0,0,18);
    scene.add(new T.HemisphereLight(0xffffff,0x7587a2,1.8));
    const lamp = new T.DirectionalLight(0xffffff,1.8);
    lamp.position.set(-3,5,8); scene.add(lamp);
  } catch (err) { renderer = null; stage.hidden = true; }

  function solid(geometry,x,y,color,z=0) {
    const obj = new T.Mesh(geometry,new T.MeshStandardMaterial({color,roughness:.55}));
    obj.position.set(x,y,z); diagram.add(obj); return obj;
  }
  function box(x,y,w,h,color,depth=.24) {
    if (!renderer) return;
    return solid(new T.BoxGeometry(w,h,depth),x,y,color);
  }
  function ball(x,y,r,color,z=0) {
    if (!renderer) return;
    return solid(new T.SphereGeometry(r,24,16),x,y,color,z);
  }
  function line(x1,y1,x2,y2,color) {
    const dx=x2-x1,dy=y2-y1,stick=box((x1+x2)/2,(y1+y2)/2,Math.hypot(dx,dy),.06,color,.06);
    if (stick) stick.rotation.z=Math.atan2(dy,dx);
  }
  function label(s,x,y,size=.36,color='#f2f6ff') {
    if (!renderer) return;
    const surface=document.createElement('canvas'),ctx=surface.getContext('2d');
    ctx.font='600 56px system-ui'; surface.width=Math.ceil(ctx.measureText(s).width)+20; surface.height=84;
    ctx.font='600 56px system-ui';ctx.fillStyle=color;ctx.textAlign='center';ctx.textBaseline='middle';
    ctx.fillText(s,surface.width/2,42);
    const texture=new T.CanvasTexture(surface);
    const sprite=new T.Sprite(new T.SpriteMaterial({map:texture,depthTest:false}));
    sprite.scale.set(size*surface.width/60,size*84/60,1);sprite.position.set(x,y,.7);diagram.add(sprite);
  }

  function records(value) {
    const rows=[['Python 기초',30,true],['Git 연습',20,false],['리스트 복습',40,true]];
    let total=0;
    rows.forEach(([name,min,done],i)=>{
      const x=(i-1)*3.4, pass=done && min>=value;
      box(x,-.95+min/40,1.35,min/20,pass?teal:muted);
      label(name,x,-1.55);label(min+'분',x,1.4);label(done?'완료':'미완료',x,-2.08,.28);
      if(pass) total+=min;
    });
    return 'done이 True이고 minutes ≥ '+value+'인 기록의 합계는 '+total+'분입니다.';
  }
  function chunks(value) {
    const text='도서 대출 기간은 14일입니다.', length=key==='size'?value:16, overlap=key==='size'?0:value;
    const step=length-overlap, parts=[];
    for(let start=0;start<text.length;start+=step) {
      parts.push([start,text.slice(start,start+length)]);
      if(start+length>=text.length) break;
    }
    const w=.60;
    [...text].forEach((c,j)=>label(c===' '?'·':c,(j-8)*w,1.58,.36));
    parts.forEach(([start,part],r)=>{
      for(let j=0;j<part.length;j++) {
        const x=(start+j-8)*w,y=.61-r*.55;
        box(x,y,w-.03,.45,r>0&&j<overlap?amber:r%2?white:teal);
      }
    });
    return parts.map(([start,p])=>'['+start+':'+(start+p.length)+'] '+p).join('　/　');
  }
  function vectors(v) {
    const pg=key==='pgdist', points=pg?[[1,1,0],[1,0,1]]:[[1,0,0],[0,1,0],[0,0,1]];
    const names=pg?['p1','p2']:['대출','휴관','반납'];
    const q=v.split(',').map(Number);
    if(renderer) {
      const scale=2.25, origin=new T.Vector3(-scale/2,-scale/2,-scale/2);
      const position=p=>new T.Vector3(...p).multiplyScalar(scale).add(origin);
      function edge(a,b,color) {
        const geometry=new T.BufferGeometry().setFromPoints([a,b]);
        diagram.add(new T.Line(geometry,new T.LineBasicMaterial({color})));
      }
      function caption(s,point,dx,dy) {
        label(s,point.x+dx,point.y+dy,.29);
        diagram.children.at(-1).position.z=point.z;
      }
      const axes=pg?['과제','제출','검토']:['대출','휴관','반납'];
      [[1,0,0],[0,1,0],[0,0,1]].forEach((a,j)=>{
        const tip=position(a.map(x=>x*1.35));
        edge(origin,tip,muted);
        caption(axes[j]+' 축',tip,.10,.20);
      });
      const qp=position(q);
      points.forEach((p,i)=>{
        const pp=position(p);
        edge(qp,pp,amber);
        ball(pp.x,pp.y,.14,teal,pp.z);
        caption(names[i],pp,-.23,-.30);
      });
      ball(qp.x,qp.y,.095,amber,qp.z+.11);
      caption('질의',qp,.36,.24);
      diagram.rotation.set(.18,rotation,0);
    }
    const distances=points.map(p=>{
      const sq=p.reduce((sum,x,j)=>sum+(x-q[j])**2,0);
      return pg?Math.sqrt(sq):sq;
    });
    return '질의 ['+q+'] · '+(pg?'L2 거리':'제곱 L2 거리')+'　'+distances.map((d,i)=>names[i]+' '+Number(d.toFixed(3))).join('　/　');
  }
  function ranking(k) {
    const docs=['무관 문서','기대 근거','다른 문서'];
    docs.forEach((d,i)=>{const x=(i-1)*3.45;box(x,0,2.9,1.2,i<k?(i===1?amber:teal):muted);label('#'+(i+1),x,.99);label(d,x,0,.31,'#0b192d');});
    return '기대 문서는 2위입니다. k = '+k+'일 때 Recall@k = '+(k>=2?'1':'0')+', 상위 k 안에서 계산한 첫 적중 순위의 역수 = '+(k>=2?'0.5':'0')+'입니다.';
  }
  function rerank(v) {
    const a='.',b='도서 대출 기간은 14일입니다', before=[a,b],after=v==='on'?[b,a]:before;
    label('검색 후보',-2.9,1.78);label('최종 순위',2.9,1.78);
    before.forEach((d,i)=>{const y=1-i*2.1,n=after.indexOf(d),y2=1-n*2.1,c=i?teal:amber;
      line(-1.6,y,1.6,y2,c);box(-3,y,2.9,.86,c);box(3,y2,2.9,.86,c);
      label(i?'14일 문장':'.',-3,y,.31,'#102236');label(i?'14일 문장':'.',3,y2,.31,'#102236');
    });
    return '1위 「'+after[0]+'」 · 2위 「'+after[1]+'」. 후보 수는 두 건입니다.';
  }
  function memory(n) {
    const turns=['장소 · 회의실 B','언어 · 한국어','기한 · 금요일 18시','분량 · 5장'];
    turns.forEach((t,i)=>{const x=(i-1.5)*2.6,active=i>=turns.length-n;box(x,active?.23:-.43,2.4,1.35,active?teal:muted);label('턴 '+(i+1),x,1.3);label(t,x,active?.23:-.43,.23,active?'#0b192d':'#ffffff');});
    return 'turns[-'+n+':]에 남는 발화　'+turns.slice(-n).join(' / ');
  }
  function switches(n) {
    [n%2===1,n>0].forEach((on,i)=>{const x=i?2.5:-2.5;box(x,-.5,3,1.1,muted);ball(x+(on?.65:-.65),-.5,.44,on?teal:amber,.42);label(i?'completed = True':'not completed',x,1.25);label(String(on),x,-1.68);});
    return '같은 완료 요청 '+n+'회　/　토글 방식 '+(n%2?'True':'False')+'　/　목표값 대입 '+(n?'True':'False');
  }
  function latency(wait) {
    const segments=[['대기',wait,amber],['처리',3.5,teal]];
    let pos=-5;for(const [name,t,c] of segments){const w=t*.55;if(w){box(pos+w/2,0,w,.7,c);label(name,pos+w/2,.88,.31);}pos+=w;}
    return '합성 예시 · 대기 '+wait+' ms + 처리 3.5 ms = 전체 '+(wait+3.5)+' ms';
  }
  function retry(state) {
    const [docs,attempts]=state.split(',').map(Number),dest=docs?'답변':attempts<2?'재검색':'종료';
    label('검색 결과',-3.7,0);['답변','재검색','종료'].forEach((d,i)=>{const y=1.65-i*1.65;line(-2.65,0,1.35,y,d===dest?amber:muted);ball(1.45,y,.17,d===dest?amber:muted);label(d,2.55,y);});
    return 'documents 길이 '+docs+' · attempts '+attempts+' → '+dest;
  }
  function session(owner) {
    ['alice','bob'].forEach((u,i)=>{const x=i?2.5:-2.5;box(x,-.1,3.55,1.85,owner===u?teal:muted);label(u+' / main',x,1.45);label(i?'RULE-B':'RULE-A',x,-.10,.45);});
    return 'sessions[("'+owner+'", "main")] → ["RULE-'+(owner==='alice'?'A':'B')+'"]';
  }
  function bars(names, amounts, suffix) {
    const max=Math.max(1,...amounts);
    names.forEach((name,i)=>{
      const x=(i-(names.length-1)/2)*3.2, height=2.7*amounts[i]/max;
      if(height) box(x,-1.35+height/2,1.55,height,i===names.length-1?amber:teal);
      label(String(amounts[i])+suffix,x,-1.02+height,.37);
      label(name,x,-1.88,.32);
    });
  }
  function branch(input, choices, selected) {
    label(input,-3.8,0,.32);
    choices.forEach((choice,i)=>{
      const y=(choices.length-1)*.78-i*1.56, active=i===selected;
      line(-2.35,0,.67,y,active?amber:muted);
      box(2.65,y,3.7,.79,active?teal:muted);
      label(choice,2.65,y,.32,active?'#102236':'#ffffff');
    });
  }
  function accumulator(mode) {
    let sum=0;
    const totals=[30,20,40].map(n=>{ if(mode==='inside')sum=0; sum+=n; return sum; });
    bars(['30분 처리','20분 처리','40분 처리'],totals,'분');
    return '각 반복이 끝난 직후의 total = '+totals.join(' → ')+'분입니다.';
  }
  function classify(question) {
    const billing=question.includes('영수증'), technical=question.includes('오류');
    const route=billing===technical?'clarify':billing?'billing':'technical';
    const choices=['billing','technical','clarify'];
    branch('문의 단서',choices,choices.indexOf(route));
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
    result.forEach(([id,content],i)=>{
      const x=(i-(result.length-1)/2)*3.3;
      box(x,0,2.95,1.32,id===incoming[0]?amber:teal);
      label(id,x,1.12);label(content,x,0,.32,'#102236');
    });
    return '기존 [h1, a1]에 '+incoming[0]+' 수신 → ['+result.map(row=>row[0]).join(', ')+']. 수정 답변을 포함한 메시지는 총 '+result.length+'개입니다.';
  }
  function approvals(choice) {
    const status=choice==='wait'?'승인 대기':choice==='approve'?'completed':'declined';
    const choices=['승인 대기','completed','declined'];
    branch('문의 A1',choices,choices.indexOf(status));
    if(choice==='wait') return '__interrupt__에 대기 중인 요청이 있습니다. status는 아직 설정되지 않았고 등록은 0건입니다.';
    return '결정 전달 뒤 status = '+status+'. 등록된 문의는 '+Number(choice==='approve')+'건입니다.';
  }
  function publish(choice) {
    const [event,ref,check]=choice.split('|');
    const allowed=event==='push'&&ref==='main'&&check==='pass';
    branch('check', ['publish 실행','publish 생략'], allowed?0:1);
    return event+' · '+ref+' · 검사 '+(check==='pass'?'성공':'실패')+' → publish '+(allowed?'실행':'생략')+'.';
  }
  function wrapping(width) {
    const left=-4.95, scale=.0214, gap=10, input=180, button=100;
    const wrap=input+gap+button>width, right=left+width*scale;
    line(left,1.25,right,1.25,white);line(right,1.25,right,-1.65,white);
    function element(text,x,y,w,c) {box(x+w*scale/2,y,w*scale,.78,c);label(text,x+w*scale/2,y,.30,'#102236');}
    element('입력 180',left,.46,input,teal);
    element('버튼 100',wrap?left:left+(input+gap)*scale,wrap?-.72:.46,button,amber);
    return '고정 폭 비교 예시 · 180 + 10 + 100 = 290px. 컨테이너 '+width+'px에서 버튼은 '+(wrap?'둘째':'첫째')+' 줄입니다.';
  }
  function substring(needle) {
    const titles=['복습 50%','복습 마무리'];
    const positions=titles.map(title=>title.indexOf(needle)+1);
    titles.forEach((title,i)=>{
      const y=.85-i*1.7;
      label(title,-2.8,y,.42);
      box(1.9,y,3.2,.85,positions[i]?teal:muted);
      label('instr = '+positions[i],1.9,y,.32,positions[i]?'#102236':'#ffffff');
    });
    return '검색어 「'+needle+'」 · instr()가 0보다 큰 행은 '+positions.filter(Boolean).length+'건입니다. 위치는 1부터 셉니다.';
  }
  function equipment(question) {
    const found=['A','B'].filter(id=>question.includes('장비 '+id));
    const selected=found.length===1?found[0]==='A'?0:1:2;
    branch('장비명 검사',['RULE-A','RULE-B','추가 질문'],selected);
    return selected===2?'장비가 하나로 정해지지 않아 추가 질문을 합니다.':
      '장비 '+found[0]+'만 일치해 점검 안내를 돌려줍니다.'+(question.includes('교체')?' 이 규칙은 교체 일정이라는 의도를 검사하지 않아 오답입니다.':'');
  }
  function regexBoundary(input) {
    const output=input.replace(/장비([AB])(?=$|[^A-Za-z0-9])/g,'장비 $1');
    const chars=[...output];
    chars.forEach((c,i)=>{
      const x=(i-(chars.length-1)/2)*1.05, inserted=output!==input&&c===' ';
      box(x,0,.91,1.13,inserted?amber:teal);
      label(c===' '?'␣':c,x,0,.5,'#102236');
    });
    return '입력 「'+input+'」 → 출력 「'+output+'」. '+(input===output?'경계 조건을 통과하지 않아 원문을 유지합니다.':'A 또는 B 앞에 공백 한 칸을 넣었습니다.');
  }
  function taskDenominator(fourth) {
    const outcomes=['success','failed','aborted',fourth];
    const attempts=outcomes.filter(s=>s!=='not_started'), wins=attempts.filter(s=>s==='success');
    outcomes.forEach((s,i)=>{
      const x=(i-1.5)*2.6;
      box(x,0,2.35,.96,s==='not_started'?muted:s==='success'?teal:amber);
      label('SYN-0'+(i+1),x,1.15,.35);label(s,x,0,.25,s==='not_started'?'#ffffff':'#102236');
    });
    return '성공 '+wins.length+'건 / 실제 시작 '+attempts.length+'건 = '+(100*wins.length/attempts.length).toFixed(1)+'%. 중단한 과업도 시작 횟수에 포함합니다.';
  }
  const draw={accumulator,classify,messageIds,approvals,publish,wrapping,substring,equipment,regexBoundary,taskDenominator,records,overlap:chunks,size:chunks,vector:vectors,pgdist:vectors,ranking,rerank,memory,switches,latency,retry,session};
  let rotation=-.54;
  function update() {
    if (renderer) {
      if(diagram){diagram.traverse(obj=>{obj.geometry?.dispose();obj.material?.map?.dispose();obj.material?.dispose();});scene.remove(diagram);}
      diagram=new T.Group();scene.add(diagram);
    }
    const value=control.type==='range'?Number(control.value):control.value;
    result.textContent=draw[key](value);
    const badge=panel.querySelector('.practice-value');
    if(badge) badge.textContent=value;
    if(renderer) {
      const w=Math.max(1,stage.clientWidth),h=Math.max(1,stage.clientHeight);
      camera.left=-5.9;camera.right=5.9;camera.top=Math.max(2.7,5.9*h/w);camera.bottom=-camera.top;
      camera.updateProjectionMatrix();renderer.setSize(w,h,false);renderer.render(scene,camera);
    }
  }
  if(renderer && ['vector','pgdist'].includes(key)) {
    const rotate=panel.querySelector('.practice-rotate');
    if(rotate) {
      rotate.hidden=false;
      rotate.addEventListener('click',()=>{rotation-=Math.PI/6;update();});
    }
  }
  control.addEventListener('input',update);window.addEventListener('resize',update);
  update();
})();
