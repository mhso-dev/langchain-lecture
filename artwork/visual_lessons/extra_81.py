"""Equipment-project and SQLite motion studies, verified against the student notebooks."""


def database_connection(draw, scene, pos):
    from render import text, tile, stretch, INK, SUB, TEAL, PALE, AMBER, LINE
    # SQLite commits on a successful exit from "with db". The close is separate.
    writing = pos < .44
    closed = .44 <= pos < .62
    reading = pos >= .62
    track = 212
    method = 'with db → commit' if writing else 'db.close()' if closed else 'connect(db_path) → SELECT'
    text(draw, (40, 94), method, 24, INK)
    tile(draw, (38, 132, 303, 278), '#ffffff', LINE)
    text(draw, (57, 158), 'Python 연결', 19, SUB)
    text(draw, (57, 196), '첫 연결' if writing else '연결 닫힘' if closed else '새 연결', 25, INK)
    if reading and pos > .84:
        text(draw, (57, 247), '(1, 복습 50%, 0)', 22, TEAL)
    draw.line((303, track, 501, track), fill=LINE, width=3)
    if closed:
        for x in (380, 398):
            draw.line((x, track+12, x+11, track-12), fill=INK, width=4)
    # Use a disk cylinder so the saved row does not disappear with the Python object.
    draw.rectangle((506, 161, 752, 265), fill=PALE, outline=TEAL, width=2)
    draw.ellipse((506, 240, 752, 287), fill=PALE, outline=TEAL, width=2)
    draw.rectangle((508, 222, 750, 262), fill=PALE)
    draw.ellipse((506, 138, 752, 184), fill='#e9f5ef', outline=TEAL, width=2)
    text(draw, (629, 161), 'todos.db', 21, INK, 'mm')
    if pos >= .32:
        tile(draw, (526, 202, 731, 245), '#ffffff', TEAL)
        text(draw, (628, 224), '1  |  복습 50%  |  0', 20, INK, 'mm')
    if writing and pos < .32:
        t = stretch((pos-.06)/.26)
        x = 305 + t*195
        tile(draw, (x-24, track-14, x+24, track+14), AMBER, INK, 6)
        text(draw, (x, track), '행 1', 14, INK, 'mm')
    if reading:
        t = stretch((pos-.66)/.20)
        x = 502 - t*194
        draw.ellipse((x-7, track-7, x+7, track+7), fill=TEAL)
    message = ('정상 종료한 트랜잭션이 1번 행을 기록합니다.' if writing else
               '연결이 닫혀도 같은 작업 폴더의 DB 파일은 남습니다.' if closed else
               '같은 파일을 다시 열어 1번 행을 읽습니다.')
    text(draw, (400, 321), message, 21, SUB, 'mm', 735)


def public_inventory(draw, scene, pos):
    from render import text, tile, stretch, INK, SUB, TEAL, PALE, AMBER, LINE
    text(draw, (36, 96), '판본 rules-v1  ·  자료 3건', 20, SUB)
    text(draw, (533, 96), 'public 검색 후보', 22, INK)
    tile(draw, (484, 118, 765, 284), '#ffffff', LINE)
    gate_x = 415
    draw.line((gate_x, 129, gate_x, 277), fill=TEAL, width=4)
    for index, (identifier, groups) in enumerate([
        ('RULE-A', 'public · admin'), ('RULE-B', 'public · admin'), ('RULE-ADMIN', 'admin')
    ]):
        y = 132+index*53
        start = index*.18
        passed = index < 2
        t = stretch((pos - start - .04) / .31)
        x = 180 + (337 if passed else 15)*t
        # The source label stays visible as the candidate slip travels to the list.
        text(draw, (39, y+17), identifier, 19, SUB)
        if t > 0 and passed:
            draw.line((170, y+18, min(x, 484), y+18), fill=LINE, width=2)
        tile(draw, (x, y, x+213, y+38), PALE if passed else AMBER, TEAL if passed else INK)
        text(draw, (x+107, y+18), identifier if t>.3 else groups, 19, INK, 'mm')
    if pos>.68:
        text(draw, (625, 262), '2건', 18, TEAL, 'mm')
    text(draw, (400, 321), 'admin만 허용한 RULE-ADMIN은 공개 그룹의 후보 밖에 남습니다.', 20, INK, 'mm', 735)


def baseline_audit(draw, scene, pos):
    from render import text, tile, stretch, INK, SUB, TEAL, PALE, AMBER, LINE
    passed = {2, 6}
    text(draw, (36, 93), 'rules-v1  ×  eval-v1', 21, SUB)
    for i in range(1, 8):
        x = 38+(i-1)*105
        scan = pos >= i*.053
        fill = (PALE if i in passed else '#f0ebe2') if scan else '#ffffff'
        tile(draw, (x, 117, x+94, 179), fill, TEAL if (scan and i in passed) else LINE, 7)
        text(draw, (x+47, 134), f'Q{i:02d}', 20, INK, 'mm')
        text(draw, (x+47, 160), ('통과' if i in passed else '실패') if scan else '대기', 16, SUB, 'mm')
    seen = sum(1 for i in passed if pos >= i*.053)
    text(draw, (736, 94), f'통과 {seen} / 7', 20, TEAL, 'rm')
    if pos < .42:
        t=stretch(pos/.38)
        draw.line((38,191,44+int(709*t),191), fill=TEAL, width=4)
        text(draw, (401,251), '같은 판본의 일곱 문항을 한 건씩 확인합니다.', 21, SUB, 'mm')
    else:
        t = stretch((pos-.42)/.16)
        draw.line((84,182,84,182+34*t), fill=TEAL, width=3)
        tile(draw,(36,215,762,306),'#ffffff',TEAL,9)
        text(draw,(55,237),'Q01  ·  실패한 조건 펼치기',19,INK)
        text(draw,(55,278),'필수 사실 일치',19,TEAL)
        text(draw,(307,278),'출처 ID 일치',19,TEAL)
        tile(draw,(478,256,744,299),AMBER)
        text(draw,(611,278),'출처 세부 정보 누락',19,INK,'mm')
    text(draw, (400,328), '공개 개발 문항의 통과 건수입니다.', 17, SUB, 'mm')


def owner_delete(draw, scene, pos):
    from render import text, tile, stretch, INK, SUB, TEAL, PALE, AMBER, LINE
    text(draw, (39, 97), 'remaining = dict(sessions)', 23, INK)
    text(draw, (40, 141), '복합 키', 18, SUB)
    text(draw, (527, 141), '메모리 사본의 값', 18, SUB)
    for i,(owner,proof) in enumerate([('alice','RULE-A'),('bob','RULE-B')]):
        y = 168 + 66*i
        tile(draw,(36,y,360,y+47),AMBER if i==0 and pos>.2 else '#ffffff',LINE)
        text(draw,(54,y+24),f'("{owner}", "main")',22,INK)
        if i==0 and pos>.36:
            t = stretch((pos-.36)/.32)
            # Collapse just the selected binding; the other owner remains visible and fixed.
            draw.line((361,y+23,466-102*t,y+23),fill=LINE,width=3)
            if t<.98:
                x=510+int(29*t)
                tile(draw,(x,y,x+201,y+46),PALE,TEAL)
                text(draw,(x+99,y+23),proof,21,INK,'mm')
                draw.line((x,y+45,x+201*t,y+45-45*t),fill=INK,width=3)
            else:
                text(draw,(600,y+24),'None',23,SUB,'mm')
        else:
            draw.line((360,y+24,501,y+24), fill=TEAL, width=3)
            tile(draw,(510,y,711,y+46),PALE,TEAL)
            text(draw,(611,y+23),proof,21,INK,'mm')
    text(draw, (400,321), 'alice/main만 pop()하면 bob/main에는 [RULE-B]가 남습니다.', 20, INK, 'mm', 730)


EXTRAS = {
    82: dict(section='nb-persist', title='연결을 닫은 뒤에도 1번 행을 읽는 이유',
             caption='with 블록이 정상 종료되며 todos.db에 저장된 1번 행을 새 연결이 다시 읽습니다. 예시는 임시 작업 폴더가 유지되는 동안의 결과입니다.',
             drawing='custom', paint=database_connection),
    89: dict(section='nb-inventory', title='공개 그룹의 검색 후보에 들어가는 문서',
             caption='문서마다 groups에 public이 있는지 먼저 확인합니다. RULE-A와 RULE-B만 후보로 들어가고 관리자 전용 문서는 검색 전에 제외됩니다.',
             drawing='custom', paint=public_inventory),
    92: dict(section='nb-difference', title='일곱 문항에서 실패한 조건 하나까지 따라가기',
             caption='Q02와 Q06이 통과해 기준선은 2/7입니다. Q01의 상세 검사에서는 답변 내용과 출처 ID가 맞아도 절과 개정일 등 출처 세부 정보가 빠져 실패합니다.',
             drawing='custom', paint=baseline_audit),
    100: dict(section='nb-expiry', title='같은 main에서 alice의 이력만 지우기',
              caption='세션 사본에서 (alice, main)을 지운 뒤 다시 조회하면 None이 나옵니다. 같은 대화 이름을 쓰는 (bob, main)에서는 여전히 RULE-B를 읽습니다.',
              drawing='custom', paint=owner_delete),
}

AUDIT = {
    81:'PATCH 성공 뒤 1번 행의 완료값과 없는 999번 ID의 404를 같은 화면 행에 대응시켜 실패 응답으로 기존 상태가 바뀌지 않는지 본다.',
    82:'nb-persist에서 커밋·연결 종료·파일 재연결을 따라 같은 1번 행을 읽고, nb-filter 실험에서는 %를 찾을 때 instr의 1기준 위치를 관찰한다.',
    83:'토글과 목표값 대입 실험에서 같은 완료 요청을 두 번 보내 토글은 False로 돌아가고 True 대입은 유지되는 것을 확인한다.',
    84:'부분 수정 절에서 날짜·우선순위를 갱신한 뒤 제목만 바꿔도 2027-04-02와 high가 같은 행에 남는 것을 본다.',
    85:'재시작 실험에서 첫 앱과 새 앱이 같은 파일을 열고 기존 ID의 날짜와 high를 다시 읽는지 확인한다.',
    86:'최소 시연 예시의 질문과 RULE-A 2.1절 문장을 한 화면에서 대조하는 과제로, 채워진 장비 A·B 근거 예시를 유지한다.',
    87:'시나리오 카드에서 장비를 특정하지 않은 Q02의 추가 질문·빈 출처와 public/admin 질문의 기대 상태를 직접 읽어 대조한다.',
    88:'수용 조건의 required 여섯 항목에 ID만 있는 인용을 대조하면 누락된 다섯 필드가 바로 출력되므로 기존 체크 예시가 적절하다.',
    89:'공개 범위별 문서 목록에서 3개 문서 중 public 허용이 있는 RULE-A·B만 움직여 검색 후보가 되는 순서를 관찰한다.',
    90:'Q01의 기대 ID·필수 표현 두 조건과 Q03의 빈 근거 목록을 채운 사례로 읽고, 공개된 개발 문항과 미확보 독립 확인 문항을 구분한다.',
    91:'thin_lookup() 조작에서 “장비 A”가 일치해도 교체 일정 질문에 점검 안내를 돌려주는 오답을 관찰한다.',
    92:'판본별 기준선 2/7에서 Q01을 펼치며 필수 사실·ID는 통과했지만 source_metadata가 실패한 차이를 읽는다.',
    93:'next_step()의 공백·교체 일정·점검 질의가 각각 invalid_input·no_evidence·check_equipment 분기로 들어가는 과정을 본다.',
    94:'기존 영상과 hashlib 과제에서 정규화한 텍스트와 별도로 원문에 줄바꿈을 넣을 때 SHA-256 지문이 달라지는지 대조한다.',
    95:'공백 입력 오류, 유효하지만 허용 문서가 없는 빈 결과, RULE-A 적중을 세 가지 서로 다른 반환 경로로 확인한다.',
    96:'코드 출력에 실제 답과 p.1·2.1절·개정일이 붙어 있고 빈 sources의 출력도 한 줄로 제공되어 두 완성 카드를 정적으로 대조할 수 있다.',
    97:'기존 영상에서 현재 질문이 no_evidence로 바뀔 때 현재 출처는 비고 첫 질문의 RULE-A는 이력에 남는 두 위치를 구별한다.',
    98:'정규식 경계 실험에서 장비A 뒤가 한글일 때와 영문 B일 때를 바꾸어 공백 삽입과 장비AB 유지의 차이를 본다.',
    99:'같은 첫 TimeoutError 뒤 둘째 시도의 completed와 attempt_limit을 나란히 보고 각 로그에서 실제 시작된 시도를 센다.',
    100:'조회 실험의 소유자 복합 키를 선택 삭제 예제에 이어, 사본에서 alice/main을 지운 뒤 bob/main의 RULE-B가 그대로인지 확인한다.',
}
