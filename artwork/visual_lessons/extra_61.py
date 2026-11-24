"""Section-level teaching decisions and moving examples for chapters 61–80."""

AUDIT = {
    61: 'nb-call에서 목록이 반환한 get_library_hours와 실제 호출이 반환한 weekend 10:00~16:00을 서로 다른 시점에 본다.',
    62: 'nb-mismatch에서 요청한 weekend와 수신한 weekday를 대조한다. hours 문자열만 읽으면 평일 09:00~18:00이 잘못 전달된다.',
    63: 'nb-envelope에서 두 요청이 동일하게 completed로 끝나도 안쪽 result의 sources와 generation_calls가 갈라지는 과정을 본다.',
    64: 'nb-pause의 중단 시점 0건과 nb-resume의 승인 후 1건을 연결한다. 새 실행을 거절할 때에는 등록이 0건인 분기도 실험한다.',
    65: 'nb-tool의 단일 단서 technical과 혼합 단서 clarify를 비교한다. 이 장면은 네트워크를 쓰지 않는 규칙 분류에 해당한다.',
    66: 'nb-observations에서 Q01의 두 기록을 계수한다. 역할 분리 시 모델 호출이 2회에서 4회로 늘어도 필수 검색은 각각 1회이다.',
    67: 'nb-fact에서 같은 p2 ID를 가리킨 뒤 개인 메신저라는 답변과 과제함이라는 자료의 차이를 읽는다. nb-sample의 실행 분모는 별도 평가 기록표로 확인한다.',
    68: 'nb-errors에서 공백으로 422가 된 요청과 검사를 통과한 뒤 근거를 찾지 못한 200 응답을 구분해 본다.',
    69: 'nb-stream의 NDJSON 경계에 이어 nb-partial에서 실제 history 저장과 events[:2]에 남은 클라이언트 관측을 따로 추적한다.',
    70: 'nb-upload에서 doc-1의 received와 NULL이 본문을 읽은 뒤 ready와 본문으로 함께 바뀌고 조회에 포함되는 지점을 본다.',
    71: '이미지와 컨테이너 수명 영상이 도입을 제공한다. 선택 실습의 create·start·stop·start는 Docker 환경에서 같은 컨테이너 ID를 다시 조회해 직접 비교한다.',
    72: 'nb-compose에서 127.0.0.1:55432와 db:5432 두 접근 경로를 같은 DB에 겹쳐 추적하고, nb-volume의 별도 영상에서 교체 뒤 데이터 보존을 본다.',
    73: 'nb-embed의 Three.js 실험에서 질의를 바꾸고 p1·p2와의 L2 거리를 비교한다. 노트북의 첫 입력은 각각 0.0과 1.414이다.',
    74: 'nb-network에서 프록시 443에서 내부 api:8000으로 전달되는 요청을 추적한다. nb-deployment는 실제 URL이 준비된 경우에만 확인하는 선택 실습이다.',
    75: 'nb-incident에서 복원 후 행 한 건을 읽고 실제 본문이 원문과 일치하는지 확인한다. 행 수만 유지된 반례는 노트북에서 비교한다.',
    76: 'nb-workflow에서 이벤트·브랜치·검사 상태를 조합해 publish 실행 여부를 바꾼다. nb-exit-code의 실패한 포트 검사가 선행 조건에 대응한다.',
    77: 'nb-candidate의 태그·digest 영상에 이어 nb-rollback에서 B의 HTTP 200과 출처 없음이 함께 보이는 순간 A로 전환하는 과정을 추적한다.',
    78: 'nb-layout에서 컨테이너 폭을 바꾸며 입력칸과 버튼이 두 줄로 갈라지는 경계를 확인한다. nb-markup의 for/id는 원래 입력 예제로 대조한다.',
    79: 'nb-event에서 양끝 공백이 있는 폼 문자열이 trim을 거쳐 question과 k=2가 담긴 JSON 본문으로 바뀌는 값을 읽는다.',
    80: 'nb-review에서 동일 제목 두 행 중 2번을 눌렀을 때 find(title)와 find(id)가 서로 다른 행에 완료 상태를 쓰는 과정을 비교한다.',
}


def envelope(draw, scene, pos):
    from render import text, tile, stretch, INK, SUB, TEAL, PALE, AMBER, LINE
    mode = int(pos >= .5)
    turn = (2 * pos) % 1
    text(draw, (35, 96), '수업용 검색 조건   ·   질문에 “과제”가 있는가?', 20, SUB)
    tile(draw, (31, 125, 251, 214), '#ffffff', LINE)
    text(draw, (141, 149), 'alice · chat-a', 17, SUB, 'mm')
    text(draw, (141, 184), ['과제는 어디에 내나요?', '주차할 수 있나요?'][mode], 21, INK, 'mm', 212)
    draw.line((251, 170, 337, 170), fill=TEAL, width=3)
    x = 258 + stretch(turn / .37) * 72
    draw.ellipse((x-7, 163, x+7, 177), fill=AMBER, outline=INK)
    tile(draw, (340, 115, 768, 311), '#e7eee9', TEAL)
    text(draw, (357, 139), 'run_status', 17, SUB)
    text(draw, (745, 139), 'completed' if turn >= .35 else '…', 21, INK, 'rm')
    tile(draw, (356, 164, 753, 296), '#ffffff', LINE)
    text(draw, (370, 185), 'result', 18, TEAL)
    values = ('answered', '문서 1개', '1') if not mode else ('no_evidence', '[]', '0')
    for i,(key, value) in enumerate(zip(('status', 'sources', 'generation_calls'), values)):
        y = 214 + i * 30
        text(draw, (375, y), key, 18, SUB)
        text(draw, (730, y), value if turn >= .36 else '…', 20, INK, 'rm')


def call_counts(draw, scene, pos):
    from render import text, tile, stretch, INK, SUB, TEAL, PALE, AMBER, LINE
    text(draw, (38, 97), 'Q01 · 호출 종류별로 따로 세기', 22, INK)
    text(draw, (255, 131), '모델 호출', 20, TEAL)
    text(draw, (595, 131), '필수 검색', 20, SUB)
    progress = min(1, max(0, (pos-.08)/.73))
    for i,(name,n) in enumerate((('단일 경로',2),('역할 분리',4))):
        y = 186 + 82 * i
        text(draw, (41, y), name, 22, INK)
        for j in range(n):
            x=263+55*j
            tile(draw, (x, y-20, x+43, y+20), '#ffffff', LINE, 7)
            a=stretch(progress*4.5-j)
            if a:
                draw.rounded_rectangle((x+3,y+17-34*a,x+40,y+17),4,fill=TEAL)
        text(draw, (506,y), f'{min(n, int(progress*4.5))}회', 23, INK)
        draw.line((554,y-26,554,y+26), fill=LINE, width=2)
        draw.ellipse((602,y-15,632,y+15), fill=AMBER, outline=INK, width=2)
        text(draw, (653,y), '1회', 23, INK)
    text(draw, (40,319), '같은 질문·고정된 검색 결과로 얻은 두 실행 기록', 18, SUB)


def stream_observation(draw,scene,pos):
    from render import text, tile, stretch, INK, SUB, TEAL, PALE, AMBER, LINE
    text(draw,(28,94),'서버가 만든 이벤트',21,INK)
    text(draw,(509,94),'학생이 남긴 수신 기록',21,INK)
    progress=min(3,pos*3.8)
    signal=['start','delta','done']
    for i,name in enumerate(signal):
        y=142+59*i
        active=progress>=i
        tile(draw,(32,y-20,189,y+19),PALE if active else '#ffffff',LINE)
        text(draw,(110,y),name,21,INK if active else SUB,'mm')
        if i<2:
            draw.line((190,y,491,y),fill=LINE,width=2)
            t=stretch(progress-i)
            if active:
                x=194+280*t
                draw.ellipse((x-7,y-7,x+7,y+7),fill=AMBER,outline=INK)
        else:
            draw.line((195,y,368,y),fill=LINE,width=2)
            draw.line((370,y-12,370,y+12),fill=SUB,width=3)
        if i<2 and progress>=i+.58:
            tile(draw,(493,y-20,761,y+20),'#ffffff',TEAL)
            text(draw,(628,y),('start','delta · 과제함에 제출하세요.')[i],19,INK,'mm',253)
        elif i==2:
            text(draw,(506,y),'events[:2]에는 없음',19,SUB)
    text(draw,(35,321),'서버 history 길이   '+('1' if progress>=2 else '0'),20,TEAL)
    text(draw,(498,321),'done 관찰   '+('아니요' if progress>=2 else '대기'),19,SUB)


def db_routes(draw,scene,pos):
    from render import text, tile, stretch, INK, SUB, TEAL, PALE, AMBER, LINE
    host=pos<.5
    u=stretch(((pos%0.5)*2-.10)/.72)
    tile(draw,(31,157,276,243),'#ffffff',LINE)
    text(draw,(152,180),'호스트 컴퓨터',19,SUB,'mm')
    text(draw,(152,216),'127.0.0.1:55432',23,INK,'mm')
    tile(draw,(314,95,770,309),'#e7eee9',TEAL)
    text(draw,(333,115),'Compose 네트워크',20,TEAL)
    tile(draw,(354,143,525,193),'#ffffff',LINE)
    text(draw,(439,167),'api 컨테이너',21,INK,'mm')
    tile(draw,(573,202,746,264),PALE,TEAL)
    text(draw,(659,222),'DB 컨테이너',17,SUB,'mm')
    text(draw,(659,246),'db:5432',23,INK,'mm')
    paths = ([(275,216),(330,216),(330,244),(574,244)],
             [(525,166),(545,166),(545,219),(574,219)])
    for i,path in enumerate(paths):
        draw.line(path,fill=TEAL if i==int(not host) else LINE,width=4)
    path=paths[int(not host)]
    lengths=[abs(x2-x1)+abs(y2-y1) for (x1,y1),(x2,y2) in zip(path,path[1:])]
    remaining=u*sum(lengths)
    for a,b,length in zip(path,path[1:],lengths):
        if remaining <= length:
            t=remaining/length
            x=a[0]+(b[0]-a[0])*t; y=a[1]+(b[1]-a[1])*t
            draw.ellipse((x-8,y-8,x+8,y+8),fill=AMBER,outline=INK,width=2)
            break
        remaining-=length
    text(draw,(33,326),'호스트에서 접속   ·   55432 → 5432' if host else 'API에서 접속   ·   db:5432',20,INK)


def rollback(draw,scene,pos):
    from render import text, tile, stretch, INK, SUB, TEAL, PALE, AMBER, LINE
    legs = ['이전 버전 A 서비스 중','후보 B를 적용','B의 근거 누락 발견','기능 검사 실패 · A로 복구']
    k=min(3,int(pos*4)); u=stretch((pos*4-k)/.48)
    loc=[0,u,1,1-u][k]
    text(draw,(35,98),legs[k],22,INK)
    draw.line((187,159,612,159),fill=LINE,width=4)
    for x,version in ((187,'A'),(612,'B')):
        draw.ellipse((x-12,147,x+12,171),fill='#ffffff',outline=TEAL,width=3)
        text(draw,(x,195),'이미지 '+version,23,INK,'mm')
    x=187+(612-187)*loc
    draw.polygon([(x,151),(x-13,126),(x+13,126)],fill=AMBER,outline=INK)
    for j,(version,source) in enumerate((('A','course-guide-v1:p2'),('B','None'))):
        start=28+393*j
        active=j==0 or k>=2
        tile(draw,(start,221,start+351,306),PALE if active and j==0 else ('#ffe6b0' if active else '#ffffff'),LINE)
        text(draw,(start+14,245),'health',18,SUB)
        text(draw,(start+333,245),'200' if active else '검사 전',21,INK,'rm')
        text(draw,(start+14,281),'source',18,SUB)
        text(draw,(start+333,281),source if active else '검사 전',21,INK,'rm')


def todo_identity(draw,scene,pos):
    from render import text, tile, stretch, INK, SUB, TEAL, PALE, AMBER, LINE
    mode=int(pos>=.5); turn=pos*2-mode
    text(draw,(39,98),'사용자가 두 번째 ‘복습’ 항목을 선택했습니다.',22,INK)
    text(draw,(38,142),'배열 탐색',19,SUB)
    columns=[(198,1),(491,2)]
    for x,ident in columns:
        selected=turn>=.50 and ident==mode+1
        tile(draw,(x,158,x+254,241),PALE if selected else '#ffffff',TEAL if selected else LINE)
        text(draw,(x+17,180),f'id = {ident}',19,SUB)
        text(draw,(x+17,214),'복습',24,INK)
        draw.rounded_rectangle((x+193,187,x+231,222),5,outline=TEAL,width=2,fill=TEAL if selected else '#ffffff')
        if selected: draw.line((x+201,203,x+209,212,x+225,195),fill='#ffffff',width=3)
    end=232+293*mode
    cursor=103+(end-103)*stretch(turn/.49)
    draw.polygon([(cursor,249),(cursor-10,265),(cursor+10,265)],fill=AMBER,outline=INK)
    text(draw,(39,295),'find(row => row.'+('id === 2)' if mode else 'title === "복습")'),22,INK)
    text(draw,(39,324),'ID 일치 · 2번만 완료' if mode else '제목 일치 · 먼저 찾은 1번이 완료',19,TEAL)


EXTRAS = {
    63: dict(section='nb-envelope',title='실행은 완료됐는데 답변은 왜 없을까요?',caption='alice의 chat-a에서 같은 함수를 두 번 호출한 경우입니다. 두 요청 모두 run_status는 completed지만, 주차 질문은 근거가 없어 result.status가 no_evidence이고 생성은 0회입니다.',drawing='custom',paint=envelope),
    66: dict(section='nb-observations',title='역할을 나누면 어떤 호출이 늘어날까요?',caption='고정된 근거를 사용한 Q01의 두 기록을 종류별로 집계합니다. 필수 검색은 양쪽 모두 1회이고 모델 호출만 2회에서 4회로 늘어납니다. 막대는 실제 실행 순서나 지연 시간을 나타내지 않습니다.',drawing='custom',paint=call_counts),
    69: dict(section='nb-partial',title='본문은 보이는데 완료 여부는 왜 모를까요?',caption='서버는 delta를 보낸 뒤 history에 한 턴을 넣고 done을 보냅니다. 학생이 잘라 읽은 events[:2]에는 start와 delta만 있어, 본문을 읽었다는 사실만으로 저장을 확인할 수 없습니다.',drawing='custom',paint=stream_observation),
    72: dict(section='nb-compose',title='같은 DB에 호스트와 API는 어디로 접속할까요?',caption='호스트에서 127.0.0.1:55432로 접속하면 공개 포트가 DB의 5432로 연결됩니다. 같은 Compose 네트워크의 API는 서비스 이름을 써서 db:5432로 곧바로 접속합니다.',drawing='custom',paint=db_routes),
    77: dict(section='nb-rollback',title='HTTP 200을 받은 이미지 B가 왜 롤백될까요?',caption='B는 HTTP 200을 반환하지만 출처가 None입니다. 검사 실패를 확인하면 active를 previous에 보관한 A로 되돌리고 A의 course-guide-v1:p2를 다시 읽습니다.',drawing='custom',paint=rollback),
    80: dict(section='nb-review',title='제목이 같은 두 할 일에서 어느 행이 바뀔까요?',caption='각 장면은 두 항목 모두 미완료인 상태에서 시작합니다. 제목으로 찾으면 첫 번째 복습이, 선택한 ID 2로 찾으면 두 번째 복습만 완료됩니다.',drawing='custom',paint=todo_identity),
}
