"""Chapter-specific close-ups for document retrieval and graph execution."""


def page_filter(draw, scene, pos):
    from render import text, tile, stretch, INK, SUB, TEAL, PALE, AMBER, LINE

    filtered = pos >= .49
    text(draw, (35, 95), '휴관 요일은 언제인가요?     k = 1', 24)
    text(draw, (766, 95), 'page = 1' if filtered else '쪽 제한 없음', 21, TEAL, 'rm')
    cards = [(146, '대출', 2), (400, '휴관', 0), (654, '반납', 2)]
    for index, (x, topic, distance) in enumerate(cards):
        excluded = filtered and index != 0
        chosen = index == (0 if filtered else 1)
        # Lower excluded documents out of the candidate shelf before choosing its winner.
        down = 41 * stretch((pos - .49) / .13) if excluded else 0
        y = 147 + down
        tile(draw, (x-107, y, x+107, y+87), '#e8eae5' if excluded else PALE if chosen else '#ffffff', LINE if excluded else TEAL)
        text(draw, (x, y+23), f'library-{index+1} · {topic}', 22, SUB if excluded else INK, 'mm', 200)
        text(draw, (x, y+59), f'{index+1}쪽  /  거리² = {distance}', 17, SUB, 'mm')
        if excluded:
            draw.line((x-84, y+73, x+84, y+73), fill='#9b4c33', width=3)
    selected_x = cards[0 if filtered else 1][0]
    t = stretch((pos-(.62 if filtered else .10))/.14)
    if t:
        y = 242+int(26*t)
        draw.polygon([(selected_x,y),(selected_x-9,y-15),(selected_x+9,y-15)],fill=TEAL)
        tile(draw,(selected_x-88,273,selected_x+88,306),AMBER)
        text(draw,(selected_x,289),'반환할 첫 문서',18,INK,'mm')


def document_contract(draw, scene, pos):
    from render import text, tile, stretch, INK, SUB, TEAL, PALE, AMBER, LINE

    cases = [
        ('[]', '문서 수 0건', 'None · 생성 입력 없음'),
        ('library-2   /   page = 0', '쪽 번호 검사 실패', 'DataContractError'),
        ('library-2   /   page = 2', '필수 필드 검사 통과', '[library-2] … / p.2'),
    ]
    index = min(2, int(pos*3))
    case, why, result = cases[index]
    text(draw, (35, 95), 'prepare_inputs()에 같은 휴관 질문과 다른 문서 목록을 전달', 23, INK, width=723)
    tile(draw,(42,130,355,298),'#ffffff',LINE)
    text(draw,(62,158),'documents',20,SUB)
    text(draw,(200,219),case,22,INK,'mm',286)
    points=[(358,217),(402,217),(448,157+index*58)]
    draw.line(points,fill=TEAL,width=4)
    progress=stretch((pos*3-index-.12)/.47)
    if progress < .5:
        x,y=358+88*progress,217
    else:
        p=(progress-.5)*2
        x,y=402+46*p,217+(157+index*58-217)*p
    draw.ellipse((x-8,y-8,x+8,y+8),fill=AMBER,outline=INK,width=2)
    for i,(_,_,label) in enumerate(cases):
        y=157+i*58
        tile(draw,(453,y-21,760,y+21),PALE if i==index and progress>.85 else '#ffffff',TEAL if i==index else LINE)
        text(draw,(606,y),label,19,INK,'mm',295)
    text(draw,(400,321),why,18,SUB,'mm')


def equal_answers(draw, scene, pos):
    from render import text, tile, stretch, INK, SUB, TEAL, PALE, AMBER, LINE

    # At equal scores the retrieval function sorts by ID, so library-2 is the second hit.
    widened = pos >= .43
    y1, y2 = 168, 247
    text(draw,(35,99),'검색한 문서 목록',22,SUB)
    text(draw,(770,99),'양쪽 모두 첫 문서로 답변',20,TEAL,'rm')
    for label, y in [('LCEL · k=1', y1), ('Graph · k='+('2' if widened else '1'), y2)]:
        text(draw,(37,y),label,21,INK,width=152)
        tile(draw,(209,y-21,368,y+21),PALE,TEAL)
        text(draw,(289,y),'library-1',21,INK,'mm')
        draw.line((368,y,399,y-28,590,y-28,604,y),fill=TEAL,width=2)
        tile(draw,(604,y-23,759,y+23),'#ffffff',TEAL)
        text(draw,(682,y),'14일',24,INK,'mm')
    if widened:
        x=412+int(49*(1-stretch((pos-.43)/.19)))
        tile(draw,(x,y2-19,x+152,y2+20),AMBER,LINE)
        text(draw,(x+76,y2),'library-2',21,INK,'mm')
    text(draw,(397,314),'답변 일치  /  전체 상태 '+('불일치' if widened else '일치'),23,INK,'mm')


def loop_guard(draw, scene, pos):
    from render import text, tile, stretch, INK, SUB, TEAL, PALE, AMBER, LINE

    # A tool report travels back along a different edge; it is the incremented state
    # that decides whether to call the tool again.
    waypoints=[(218,177),(218,139),(529,139),(529,177),(529,246),(218,246),(218,206),(218,297),(500,297)]
    events=[(0,.24,0,3),(.27,.6,3,6),(.66,.93,6,8)]
    text(draw,(39,92),'질문   대출 기간은 며칠인가요?',22,INK)
    draw.line(waypoints[:4],fill=LINE,width=4)
    draw.line(waypoints[3:7],fill=LINE,width=4)
    draw.line(waypoints[6:],fill=LINE,width=4)
    for (x,y), name in [((218,189),'model · decide'),((529,189),'tool · 검색'),((620,297),'END')]:
        tile(draw,(x-101,y-19,x+101,y+19), '#ffffff',TEAL)
        text(draw,(x,y),name,20,INK,'mm')
    text(draw,(375,122),'search',17,SUB,'mm')
    text(draw,(395,265),'documents + rounds',17,SUB,'mm')
    text(draw,(759,92),'rounds = '+('1' if pos>=.27 else '0'),22,TEAL,'rm')
    for start,end,first,last in events:
        if pos<start: break
        u=stretch((pos-start)/(end-start))
        segments=waypoints[first:last+1]
        # Interpolate by distance so the token moves through corners without jumping.
        lengths=[abs(b[0]-a[0])+abs(b[1]-a[1]) for a,b in zip(segments,segments[1:])]
        travel=u*sum(lengths)
        for a,b,length in zip(segments,segments[1:],lengths):
            if travel<=length:
                frac=travel/length
                x=a[0]+(b[0]-a[0])*frac; y=a[1]+(b[1]-a[1])*frac
                break
            travel-=length
        else:
            x,y=segments[-1]
        if pos<end or first==6:
            draw.ellipse((x-8,y-8,x+8,y+8),fill=AMBER,outline=INK,width=2)
            break


EXTRAS = {
    23: dict(section='nb-search', title='쪽 필터를 걸면 가까운 문서도 빠질까요?',
             caption='휴관 질문은 필터가 없을 때 제곱 거리가 0인 library-2를 찾습니다. page=1로 후보를 제한하면 2쪽은 순위 계산에서 빠져 대출 안내인 library-1이 반환됩니다.',
             drawing='custom', paint=page_filter),
    25: dict(section='nb-repair', title='빈 문서 목록과 잘못된 쪽 번호는 어디로 갈까요?',
             caption='같은 질문에 문서 목록만 바꿔 prepare_inputs() 풀이의 세 경로를 비교합니다. 빈 목록은 None을 돌려주고, 쪽 번호 0은 검사 중 예외를 일으킵니다. 2쪽인 정상 문서만 출처가 붙은 문맥으로 조립됩니다.',
             drawing='custom', paint=document_contract),
    32: dict(section='nb-two-runners', title='답변이 같은 두 실행에서 무엇이 달라졌을까요?',
             caption='LCEL의 k는 1로 유지하고 그래프의 graph_k만 2로 바꾼 비교입니다. 두 답변은 첫 문서의 14일을 유지하지만 그래프의 documents에는 library-2가 더 있어 전체 상태를 비교하면 False입니다.',
             drawing='custom', paint=equal_answers),
    34: dict(section='nb-choose', title='검색을 한 번 마친 그래프는 어떻게 멈출까요?',
             caption='대출 질문에서 rounds가 0이면 model이 tool로 보냅니다. 검색이 끝나 rounds=1이 돌아오면 같은 model 노드의 조건을 다시 평가해 END로 이동합니다.',
             drawing='custom', paint=loop_guard),
}

AUDIT = {
    21: '겹침 길이를 바꿀 때 두 청크가 공유하는 글자와 시작 인덱스를 함께 읽는다. 크기 16, 겹침 4에서 둘째 시작점은 12다.',
    22: '제곱 L2 거리 실험과 FAISS 위치→문서 그림을 분리한다. 거리 0인 결과의 위치로 documents 배열을 찾아 library-1을 읽는다.',
    23: '중첩 목록 영상에서 [0][0]으로 세 필드를 복원하고, 검색 절에서는 page=1이 휴관 문서를 후보에서 먼저 제외하는 과정을 본다.',
    24: '검색된 library-2와 답변에 적은 ID를 대조하는 영상으로 invalid_citation을 설명한다. 빈 목록이면 생성을 생략하는 연습은 해당 절의 실행 경로와 함께 읽는다.',
    25: 'prepare_inputs()에서 같은 휴관 질문에 빈 목록, page=0, page=2를 넣어 None·예외·완성 문맥으로 갈리는 지점을 확인한다.',
    26: 'TypedDict 상태 영상에서 lookup의 documents 갱신과 답변 노드의 answer 갱신 뒤에도 question이 보존되는지 추적한다.',
    27: '분기 영상 뒤에 attempts와 검색 결과를 바꾸는 실험이 있다. 빈 결과의 첫 시도는 retry, 두 번째 시도는 stop이 된다.',
    28: '기존 메시지 ID와 새 ID를 선택해 덮어쓰기, add_messages의 교체와 누적에 따라 목록 길이와 메시지 내용이 달라지는 것을 확인한다.',
    29: 'thread_id A의 두 질문을 한 칸에 쌓고 B를 별도 칸에 표시해 세 번째 호출도 B의 사용자 발화 수는 1임을 확인한다.',
    30: '휴관 질문에서 검색한 library-2의 본문과 p.2가 검색 노드에서 답변 노드로 함께 이동하는 경로를 본다.',
    31: '검색이 끝난 빈 목록과 대기가 끝나 TimeoutError가 발생하는 경우를 나란히 본다. 후자의 적중 건수는 결정할 수 없다.',
    32: 'graph_k만 2로 바꿔 두 답변이 모두 14일이어도 documents 목록에서 상태가 어긋나는 것을 보고, 추적 절에서 검색 ID를 대조한다.',
    33: 'AIMessage가 요청한 검색과 결과 ToolMessage 사이에 같은 요청 ID가 붙는 위치를 추적한 뒤 search-1 예제를 확인한다.',
    34: 'tool→model로 rounds=1이 되돌아가 END가 선택되는 장면과, 검색 0회·1회 빈 목록·1회 적중이라는 실행 결과를 나누어 관찰한다.',
    35: 'dev-01의 기대 문서 library-1과 주차 질문 dev-03의 False·빈 목록은 질문별 대응표에서 동시에 대조할 수 있어 기존 표와 출력을 유지한다.',
    36: '상위 k를 바꿔 첫 적중 2위의 역수 0.5를 읽고, 별도 영상에서 library-1 인용이 유효해도 999일은 14일 원문과 어긋남을 대조한다.',
    37: '크기 조절 실험에서 17글자를 8·8·1글자로 분할하는 모습을 본다. top-k 절은 같은 정렬 목록을 1개와 2개로 자른 출력을 직접 비교한다.',
    38: '재정렬은 마침표와 대출 문장 청크의 순위를 서로 바꾸며, 다중 질의는 두 결과가 같은 library-1:0에 합쳐져 후보 한 건만 남는다.',
    39: 'dev-01 두 행의 답변·출처는 같고 rerank_calls만 0과 1이다. 기존 비교표에서 항목을 동시에 확인하고 baseline 채택 기록과 연결한다.',
    40: '폼 편집 중 화면에 남는 이전 결과와 제출 직후 갱신된 결과를 영상에서 비교한다. AppTest는 Streamlit 설치 후 실행하는 선택 경로다.',
}
