"""Independent review of the Python, prompt and workflow chapters."""


def git_snapshot(draw, scene, pos):
    from render import text, tile, stretch, INK, SUB, TEAL, PALE, AMBER, LINE

    # A file remains in the working tree when the index and commit take copies.
    labels = ['작업 폴더', '스테이징 영역', '커밋 기록']
    for x, name in zip([28, 290, 552], labels):
        tile(draw, (x, 123, x + 216, 280), '#e8efe8', LINE)
        text(draw, (x + 108, 104), name, 21, INK, 'mm')
    for k, x in enumerate([28, 290, 552]):
        start = [0, .18, .55][k]
        if pos < start:
            continue
        shift = 0 if k == 0 else -262 * (1-stretch((pos-start)/.20))
        left = x + 19 + shift
        tile(draw, (left, 151, left+178, 250), PALE if k < 2 else '#fff0c7', TEAL if k < 2 else INK)
        text(draw, (left+89, 179), 'README.md', 21, INK, 'mm')
        draw.line((left+17, 200, left+160, 200), fill=LINE, width=2)
        text(draw, (left+89, 224), '첫 인사 셀을 실행하세요.', 16, SUB, 'mm', 162)
    if pos < .18:
        status = 'README.md 작성'
    elif pos < .55:
        status = 'git add README.md'
    else:
        status = 'git commit  ·  첫 인사 실행 안내'
    tile(draw, (193, 293, 608, 331), INK)
    text(draw, (400,311), status, 19, '#ffffff', 'mm')


def nested_record(draw, scene, pos):
    from render import text, tile, stretch, INK, SUB, TEAL, PALE, AMBER, LINE

    step = min(int(pos*3.25),2)
    text(draw, (37,100), 'data', 21, TEAL)
    text(draw, (117,100), '["records"]', 23, TEAL if step >= 0 else SUB)
    text(draw, (282,100), '[0]', 23, TEAL if step >= 1 else SUB)
    text(draw, (366,100), '["minutes"]', 23, TEAL if step >= 2 else SUB)
    tile(draw, (32,136,768,314), '#edf2eb', TEAL)
    for i, name in enumerate(['Python 기초','Git 연습','리스트 복습']):
        x=53+i*241
        tile(draw,(x,161,x+216,293),PALE if step>=1 and i==0 else '#ffffff',TEAL if step>=1 and i==0 else LINE)
        text(draw,(x+12,184),f'[{i}]  {name}',21,INK,width=191)
        text(draw,(x+12,230),'minutes',19,SUB)
        color=AMBER if step==2 and i==0 else '#e6ece7'
        tile(draw,(x+110,211,x+194,250),color)
        text(draw,(x+152,230),str([30,20,40][i]),21,INK,'mm')
    if step==2:
        u=stretch((pos-.62)/.25)
        draw.line((456,113,456,127,206,127,206,126+73*u),fill=TEAL,width=3)


def minutes_limit(draw, scene, pos):
    from render import text, tile, stretch, INK, SUB, TEAL, PALE, AMBER, LINE

    # Magnify only the right boundary; numeric ticks use equal spacing.
    text(draw,(33,97),'parse_minutes()의 범위 검사',22,SUB)
    x0,spacing,y=200,125,183
    draw.line((80,y,725,y),fill=LINE,width=4)
    draw.line((80,y,x0+2*spacing,y),fill=TEAL,width=8)
    for i,n in enumerate([478,479,480,481,482]):
        x=x0+i*spacing
        draw.line((x,y-9,x,y+10),fill=INK,width=2)
        text(draw,(x,y+34),str(n),20,INK,'mm')
    branch=pos>=.49
    x=x0+(2+stretch((pos-.49)/.22))*spacing
    draw.ellipse((x-11,y-12,x+11,y+10),fill=AMBER,outline=INK,width=2)
    text(draw,(x,y-34),'"481"' if branch else '"480"',22,INK,'mm')
    for idx,(left,label) in enumerate([(40,'return minutes'),(419,'raise ValueError')]):
        active=idx==int(branch) and (not branch or pos>.64)
        tile(draw,(left,263,left+341,321),PALE if active else '#ffffff',TEAL if active else LINE)
        text(draw,(left+170,291),label,23,INK if active else SUB,'mm')


def seat_capacity(draw, scene, pos):
    from render import text, tile, stretch, INK, SUB, TEAL, PALE, AMBER, LINE

    text(draw,(34,102),'시설 안내  ·  세미나실 좌석',21,SUB)
    text(draw,(507,103),'두 원문에서 센 대상',22,SUB)
    fill=int(stretch((pos-.17)/.48)*20)
    for i in range(30):
        col,row=i%6,i//6
        x,y=55+63*col,130+39*row
        # Seat with a back and two feet. A disc represents one permitted attendee.
        draw.rounded_rectangle((x,y,x+38,y+19), radius=4,outline=SUB,width=2,fill='#ffffff')
        draw.line((x+4,y+20,x+4,y+25),fill=SUB,width=2)
        draw.line((x+34,y+20,x+34,y+25),fill=SUB,width=2)
        if i < fill:
            draw.ellipse((x+12,y+2,x+26,y+16),fill=TEAL)
    for y,word,val,col in [(154,'세미나실 좌석','30석','#ffffff'),(232,'행사 참가 정원','20명',PALE if fill==20 else '#ffffff')]:
        tile(draw,(488,y-15,758,y+51),col,LINE)
        text(draw,(503,y+19),word,19,SUB)
        text(draw,(740,y+19),val,26,INK,'rm')
    text(draw,(35,327),'점 1개 = 정원 1명',16,SUB)


def empty_summary(draw, scene, pos):
    from render import text, tile, stretch, INK, SUB, TEAL, PALE, AMBER, LINE

    text(draw,(35,100),'요약 단계가 공백 세 칸을 반환한 경우',22,SUB)
    for i,(x,tag) in enumerate([(48,'원래 요약'),(319,'strip() 결과'),(580,'classify 호출')]):
        tile(draw,(x,142,x+164,248),'#ffffff',LINE)
        text(draw,(x+82,167),tag,19,SUB,'mm')
    for j in range(3):
        x=73+39*j
        draw.line((x,207,x,218,x+25,218,x+25,207),fill=TEAL,width=3)
    u=stretch((pos-.14)/.27)
    draw.line((212,204,212+101*u,204),fill=TEAL,width=4)
    if u>.9:
        text(draw,(401,213),'""',29,INK,'mm')
    draw.line((489,204,569,204),fill=LINE,width=2)
    blocker=stretch((pos-.40)/.14)
    if blocker:
        draw.line((526,201-23*blocker,526,207+23*blocker),fill='#a34435',width=6)
    text(draw,(662,215),'0회' if pos>.52 else '대기',23,INK,'mm')
    if pos>.52:
        tile(draw,(70,267,730,321),'#ffe4d4','#a34435')
        text(draw,(400,294),'ValueError   ·   빈 단계 출력: summarize',23,INK,'mm')


def collect_pieces(draw, scene, pos):
    from render import text, tile, stretch, INK, SUB, TEAL, PALE, AMBER, LINE

    text(draw,(31,98),'체인이 없을 때 쓰는 제공 조각',21,SUB)
    text(draw,(28,245),'결합 결과',18,SUB)
    draw.line((156,282,736,282),fill=LINE,width=2)
    pieces=[('가상','가상',51,166),('안내','안내',280,287)]
    for i,(_,label,orig,target) in enumerate(pieces):
        u=stretch((pos-.12-i*.32)/.27)
        x=orig+(target-orig)*u
        y=139+105*u
        tile(draw,(x,y,x+121,y+55),PALE if i==0 else '#fff0c7',TEAL if i==0 else INK)
        text(draw,(x+36,y+28),label,23,INK,'mm')
        if i==0:
            # Draw the trailing space explicitly. The bracket is a teaching mark.
            draw.line((x+77,y+28,x+77,y+36,x+103,y+36,x+103,y+28),fill=TEAL,width=2)
    if pos>.78:
        text(draw,(472,268),'→  가상 안내',25,TEAL)
    text(draw,(37,322),'첫 조각의 끝 공백도 문자열의 일부입니다.',18,SUB)


EXTRAS = {
    1: dict(section='nb-git-snapshot', title='git add 뒤에 커밋되는 파일은 어디에 있을까요?',
            caption='README.md를 추가하면 현재 내용이 스테이징 영역에 담깁니다. git commit은 그 내용을 커밋에 기록하고 git log에는 메시지 ‘첫 인사 실행 안내’가 표시됩니다.', drawing='custom', paint=git_snapshot),
    2: dict(section='nb-one-record', title='data["records"][0]["minutes"]를 한 칸씩 따라가기',
            caption='records 키로 세 기록의 목록에 들어갑니다. 인덱스 0으로 첫 기록을 고른 뒤 minutes 키로 30을 읽습니다.', drawing='custom', paint=nested_record),
    3: dict(section='nb-exception', title='480은 반환하고 481은 예외가 되는 경계',
            caption='0~480분을 허용하는 parse_minutes()에 두 값을 차례로 넣는 비교입니다. 480은 return에 도달하고, 481은 raise에서 호출한 쪽의 except로 넘어갑니다.', drawing='custom', paint=minutes_limit),
    10: dict(section='nb-record', title='좌석 30석을 행사 정원 30명으로 써도 될까요?',
             caption='시설 안내에 있는 좌석을 모두 그리면 30석입니다. 행사 안내가 허용한 성인 참가자 20명을 점으로 표시하면 10석이 남습니다. 점은 실제 예약 현황이 아니라 행사 정원을 나타냅니다.', drawing='custom', paint=seat_capacity),
    13: dict(section='nb-trace', title='요약이 공백이면 다음 호출은 몇 번 실행될까요?',
             caption='summarize가 공백만 돌려주는 경우를 run_workflow의 검사 순서로 따라갑니다. strip() 결과가 빈 문자열이면 해당 단계 이름으로 예외가 발생해 분류와 안내 작성은 시작하지 않습니다.', drawing='custom', paint=empty_summary),
    19: dict(section='nb-stream', title='두 출력 조각이 한 문자열이 되는 과정',
             caption='제공된 두 조각 "가상 "과 "안내"는 도착 순서로 이어집니다. 빈 문자열로 join해도 첫 조각 끝의 공백이 남아서 "가상 안내"가 됩니다.', drawing='custom', paint=collect_pieces),
}

AUDIT = {
    1: '커널 변수의 셀 편집·실행 차이를 기존 영상에서 보고, git add와 commit이 README.md 내용을 어떤 위치에 복사하는지 별도 장면에서 대조한다.',
    2: 'records → [0] → minutes의 경로에서 값 30을 읽은 뒤, 기존 실험에서 최소 시간을 바꾸며 done 조건과 누적 합계를 확인한다.',
    3: 'print만 한 함수가 돌려주는 None은 기존 영상, 허용 경계의 480과 예외를 내는 481은 nb-exception의 수직선에서 구별한다.',
    4: '첫 인스턴스에서 mark_done()을 실행해도 second.done은 False인 상태 분리를 nb-object-state의 기존 영상과 셀 02 출력으로 대조한다.',
    5: '빈 시간이 든 ID 2를 먼저 제외해야 같은 ID의 20분 행이 남고, 유효한 ID 4 두 행은 한 건으로 합쳐지는 순서를 nb-clean-order에 표시한다.',
    6: 'HTTP 상태 오류는 상태 검사에서, 형식 오류는 json.loads()에서 드러남을 nb-failures의 두 예외 출력과 연결한다.',
    7: '30·20·40분을 처리할 때 total 초기화 위치를 바꿔 마지막 40과 누적 90을 비교한다. Git 충돌은 원문 표시 세 줄을 읽는 정적 예시로 유지한다.',
    8: '무료라는 후보 답변 바로 아래 원문에 ‘예산과 참가비는 아직 합의하지 않았다’가 출력되고, 하늘의 마감일도 원문 대조 과제에서 찾도록 되어 있어 정적 비교로 충분하다.',
    9: '고정 원문을 놓고 참가비 무료와 수강료 미발표를 대조한 뒤, 원문에서 수강료만 5만 원으로 바꾸는 nb-versions 셀의 두 문장을 직접 비교한다.',
    10: 'nb-record에서 시설 좌석 30개에 행사 정원 20명만 표시해 원문의 수치가 지칭하는 대상 차이를 확인한다.',
    11: '가상 user 요청 → MockTransport의 응답 → response.output_text로 이어지는 값의 이동을 보며 실제 SDK 메서드와 모의 서버 경계를 읽는다.',
    12: '비교 기준으로 확인했다. 키가 존재하며 값이 null인 경우와 키 자체가 없는 경우를 같은 서식에서 구별한다.',
    13: 'nb-summary에 요약문과 분류 billing의 전달을, nb-trace에는 공백 요약을 받은 뒤 다음 호출이 0회인 실패 경로를 배치한다.',
    14: '영수증과 오류 단서를 바꾸면 billing·technical·clarify 중 어디로 가는지, 안내 작성 호출이 1회와 0회 중 어떻게 바뀌는지 조작한다.',
    15: '도구 스키마의 enum과 required는 코드에서 바로 읽고, nb-request-item에서는 arguments를 읽은 호출 요청과 실제 도구 실행의 차이를 기존 영상으로 확인한다.',
    16: '두 반환값 순서가 바뀐 비교 예시로 call_id가 같은 요청과 출력만 연결해야 함을 nb-id-match에서 확인한다.',
    17: 'nb-loop에서 도구 반환 2건이 쌓인 뒤 세 번째 모델 응답이 최종 message가 되어야 completed인 실행 기록을 차례로 확인한다.',
    18: '인자 없는 도구의 유효한 {}와 결과를 연결할 수 없는 빈 ID 및 허용 목록 밖 이름을 세 갈래 검사의 대응으로 확인한다.',
    19: 'LCEL 파이프 전달은 기존 영상, 문자열 조각의 순서와 끝 공백 보존은 nb-stream의 제공 조각 두 장으로 따로 설명한다.',
    20: 'nb-sources의 기존 영상에서 문서·쪽·본문의 연결을 따라가고, nb-loaders의 TXT page=None과 PDF page=1은 실제 출력 두 줄로 대조한다.',
}
