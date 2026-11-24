"""Additional visual explanations for the workflow, SQL and agent lessons."""


def accounting(draw, scene, pos):
    """The local call advances its counter without crossing the model boundary."""
    from render import text, tile, stretch, INK, SUB, TEAL, PALE, AMBER, LINE

    tile(draw,(24,103,472,270),'#ffffff',LINE)
    tile(draw,(485,103,776,270),'#ffffff',LINE)
    text(draw,(44,128),'로컬 생성 규칙',22,INK)
    text(draw,(506,128),'외부 모델 API',22,INK)
    draw.line((46,194,345,194),fill=LINE,width=5)
    for y in range(155,234,13):
        draw.line((474,y,474,y+6),fill=SUB,width=2)
    progress=stretch((pos-.15)/.44)
    x=54+progress*263
    tile(draw,(x,174,x+60,214),AMBER,INK)
    text(draw,(x+30,193),'p3',21,INK,'mm')
    local_count=int(progress>.94)
    text(draw,(389,191),str(local_count),42,TEAL,'mm')
    text(draw,(402,232),'생성 규칙 실행 횟수',16,SUB,'mm',126)
    text(draw,(632,191),'0',42,INK,'mm')
    text(draw,(632,232),'외부 요청 횟수',17,SUB,'mm')
    if not local_count:
        text(draw,(42,310),'Q03 · 오류 안내 문단 p3을 찾았습니다.',20,INK)
    else:
        text(draw,(42,310),'잘못된 p2 인용으로 응답 차단  ·  모델 비용과 지연은 미측정(None)',20,INK,width=717)


def citation_fix(draw, scene, pos):
    """Follow the retrieved identifier onto the generated citation."""
    from render import text, tile, stretch, INK, SUB, TEAL, PALE, AMBER, LINE

    tile(draw,(28,118,288,266),'#ffffff',LINE)
    text(draw,(44,145),'Q03 · 검색한 원문',21,INK)
    text(draw,(44,185),'오류 화면과 발생 시간 기록',17,SUB,width=220)
    tile(draw,(43,213,260,250),PALE,TEAL)
    text(draw,(151,231),'course-guide-v1:p3',19,INK,'mm')
    tile(draw,(435,118,771,266),'#ffffff',LINE)
    text(draw,(453,145),'Q03 · 생성한 안내',21,INK)
    text(draw,(453,179),'오류 내용을 담당 강사에게 문의',17,SUB,width=295)
    phase=stretch((pos-.24)/.37)
    if phase<1:
        x=464+round(55*phase)
        tile(draw,(x,210,x+103,251),'#f7e0d6',LINE)
        text(draw,(x+51,230),'고정값 p2',17,INK,'mm')
        if phase>.35:
            draw.line((x+7,246,x+95,213),fill='#ad5542',width=3)
    if phase>0:
        x=44+int(423*phase)
        y=212-int(54*4*phase*(1-phase))
        tile(draw,(x,y,x+207,y+38),AMBER,INK)
        text(draw,(x+103,y+18),'course-guide-v1:p3',19,INK,'mm')
    if phase==0:
        tip='p3을 읽었는데 답변에 고정값 p2가 붙어 인용 검사를 통과하지 못합니다.'
    elif phase<1:
        tip='검색한 원문에서 evidence["id"]를 읽어 답변 끝으로 옮깁니다.'
    else:
        tip='Q03은 p3으로 인용합니다. 기존 성공 문항 Q01도 다시 대조합니다.'
    text(draw,(33,310),tip,20,INK,width=738)


def count_roles(draw, scene, pos):
    """Count actual role messages as they cross a cursor in their recorded order."""
    from render import text, tile, stretch, INK, SUB, TEAL, PALE, AMBER, LINE

    roles=['human','ai','tool','ai','tool','ai']
    labels=['질문','시간 요청','주말 시간','기간 요청','14일','최종 안내']
    t=stretch((pos-.05)/.83)
    cursor=35+729*t
    draw.line((35,192,764,192),fill=LINE,width=4)
    seen=[]
    for i,(role,desc) in enumerate(zip(roles,labels)):
        x=89+i*124
        active=cursor>=x
        if active:seen.append(role)
        c=(TEAL if role=='ai' else '#bc8436' if role=='tool' else SUB) if active else LINE
        draw.ellipse((x-8,184,x+8,200),fill=c)
        text(draw,(x,131),role,22,c,'mm')
        text(draw,(x,158),desc,17,INK if active else SUB,'mm')
    draw.polygon([(cursor,181),(cursor-6,171),(cursor+6,171)],fill=INK)
    for x,name,count,color in [(40,'모델 메시지',seen.count('ai'),PALE),(410,'도구 메시지',seen.count('tool'),'#ffe8b7')]:
        tile(draw,(x,219,x+347,266),color)
        text(draw,(x+16,243),name,20)
        text(draw,(x+317,244),str(count),25,INK,'mm')
    text(draw,(40,306),'마지막 ai 메시지는 최종 안내를 내고, 새 도구를 요청하지 않습니다.',20,INK,width=719)


def memory_summary(draw, scene, pos):
    """Trace one deadline from the original turn to the two memory forms."""
    from render import text, tile, stretch, INK, SUB, TEAL, PALE, AMBER, LINE

    facts=['장소 · 회의실 B','언어 · 한국어','기한 · 금요일 18시','분량 · 5장']
    text(draw,(28,96),'발화 원문',20,INK)
    for i,name in enumerate(facts):
        y=130+43*i
        tile(draw,(29,y-17,225,y+17),AMBER if i==2 else '#ffffff',LINE)
        text(draw,(40,y),name,17,INK,width=174)
    tile(draw,(315,100,768,181),'#ffffff',LINE)
    text(draw,(330,121),'처음 3개 발화의 수업용 요약',19,INK)
    text(draw,(330,156),'회의실 B  ·  한국어',20,TEAL)
    tile(draw,(315,196,768,285),'#ffffff',LINE)
    text(draw,(330,217),'최근 2개 발화  turns[-2:]',19,INK)
    text(draw,(605,255),'분량 · 5장',18,SUB)
    t=stretch((pos-.28)/.42)
    x=42+round(297*t)
    y=216+round(39*t)
    if t>0:
        tile(draw,(x,y-16,x+170,y+16),AMBER,INK)
        text(draw,(x+85,y),'기한 · 금요일 18시',17,INK,'mm',160)
    if pos>.72:
        text(draw,(748,157),'기한 누락',17,'#99432e','rm')
        text(draw,(30,316),'요약에 “금요일 18시”가 있는지 검사하면 False입니다. 최근 발화에는 남습니다.',19,INK,width=735)
    else:
        text(draw,(30,316),'3번째 발화의 제출 기한은 어느 쪽에 남을까요?',20,INK)


EXTRAS={
    49:dict(section='nb-model-cost',title='로컬 생성 1회일 때 외부 호출은 몇 회일까요?',
            caption='Q03 후보에서 로컬 생성 규칙은 한 번 실행되고 p2 인용 오류로 응답이 막힙니다. 외부 모델 요청은 0회입니다. 실험에서 측정하지 않은 모델 비용과 지연은 None으로 남깁니다.',
            drawing='custom',paint=accounting),
    50:dict(section='nb-fix-id',title='답변 끝에 고정한 p2를 어떤 값으로 바꿀까요?',
            caption='Q03의 오류 안내는 p3에서 검색됐습니다. 생성 규칙이 그 문단의 본문과 ID를 함께 읽으면 표시되는 인용도 p3이 됩니다. 이어지는 회귀 검사에서는 Q01이 기존 결과와 같은지도 확인합니다.',
            drawing='custom',paint=citation_fix),
    55:dict(section='nb-trace',title='모델 메시지 세 개와 도구 메시지 두 개 세기',
            caption='대본의 역할 순서를 왼쪽부터 읽습니다. 도구 요청 두 번과 최종 안내 한 번이 ai 메시지 세 개를 만들고, 실행 결과 두 개가 tool 메시지가 됩니다.',
            drawing='custom',paint=count_roles),
    59:dict(section='nb-summary',title='같은 제출 기한이 요약과 최근 발화에 남는 방식',
            caption='수업용 요약은 첫 세 발화 중 장소와 언어만 보존합니다. 세 번째 발화의 금요일 18시는 요약에서 빠지지만 최근 두 발화에는 남습니다. 같은 사실을 두 메모리 표현에서 찾아보세요.',
            drawing='custom',paint=memory_summary)
}

AUDIT={
    41:'화면 상태와 스레드 이력을 비교했다. A의 두 번째 질문 뒤 history에는 두 발화가 남고 현재 sources만 []로 바뀌는 모습을 nb-new-session에서 보여준다.',
    42:'대출 질문을 고정하고 검색·답변의 library-1과 화면에 남은 library-2(p.2)를 맞대어, 교체할 값이 표시 출처임을 확인한다.',
    43:'범위 결정서는 A2의 점수 문의와 점수를 만들지 않는 기대 행동을 한 행에 제시한다. 팀이 기준을 작성할 때 두 문장을 함께 읽도록 정적 예시를 유지한다.',
    44:'Q04의 주말 일정 질문을 평일 오전 9시 원문과 대조한다. 기대 답과 해당 문단의 텍스트를 동시에 읽어야 하므로 정적 대조가 적절하다.',
    45:'과제 제출 질문 전체가 일치할 때의 p2와 업로드 실패 질문의 빈 목록을 비교해, 관련 문서가 있어도 검색되지 않는 이유를 확인한다.',
    46:'실패 키워드를 추가해 p3을 찾은 뒤에도 invalid_citation이 남는 과정을 보여준다. 검색 단계와 인용 단계를 따로 추적한다.',
    47:'생략한 검색 0회, 성공한 필수 검색 1회, 반복 상한의 검색 2회를 종료 상태와 짝지어 비교한다.',
    48:'업로드 실패 질문으로 바뀌었을 때 현재 카드에서 이전 출처 p2가 사라지고 sources가 []로 바뀌는지 본다.',
    49:'Q03 후보에서 로컬 생성 1회와 외부 모델 요청 0회를 별도로 세어, 비용·지연의 None과 구분한다.',
    50:'Q03의 잘못된 고정 인용 p2가 검색 문단의 실제 ID p3으로 바뀌는 과정을 추적한 뒤, Q01의 기존 성공 결과를 재확인한다.',
    51:'동일 입력 바이트 확인은 True이며 새 OS·설치·동료 재현은 not_run이다. 함께 제시한 실행 기록으로 확인 범위를 읽는다.',
    52:'완성된 시연 대본에는 no_evidence, invalid_citation, answered가 순서대로 적혀 있다. 팀별 시연 근거와 나란히 읽을 수 있게 대본으로 유지한다.',
    53:'alice 두 행과 bob 한 행을 사용자 키에 연결해 COUNT(*) 결과가 학습자 A 2건, B 1건으로 모이는 과정을 본다.',
    54:'같은 연결에서 갱신한 제목과 마지막으로 커밋된 제목을 함께 보고 rollback() 뒤 초안으로 복원되는 과정을 확인한다.',
    55:'c1·c2 결과를 원래 요청에 연결한 뒤 nb-trace에서 human/ai/tool을 순서대로 세어 도구 2회와 모델 메시지 3개를 구분한다.',
    56:'추가 검색 요청이 와도 run_limit=1인 실행에서 실제 함수의 executed 목록에는 대출 한 건만 남는 것을 보여준다.',
    57:'두 SKILL.md의 설명과 자료 부재 시 처리 규칙, 비교 입력의 k=2와 k=1을 정적으로 대조한다. 문구를 직접 수정하는 과제를 유지한다.',
    58:'목록 메타데이터에서 선택한 SKILL.md를 먼저 열고, 지시에 따라 references/source-check.md가 필요해지는 시점을 확인한다.',
    59:'슬라이싱 실험에서 최근 두 발화를 확인한 뒤 요약과 원문 대조 절에서 금요일 18시가 요약에만 빠지는 모습을 추적한다.',
    60:'language 키가 같아도 alice의 설정만 저장된 초기 예시에서 bob 조회가 None이 되는 과정을 복합 키와 연결한다.',
}
