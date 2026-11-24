"""Project chapters: request delivery, evaluation, deployment and restored history."""


def delivery(draw, scene, pos):
    from render import text, tile, stretch, INK, SUB, TEAL, PALE, AMBER, LINE

    broken = pos < .5
    t = stretch((pos * 2) % 1 / .71)
    text(draw, (37, 91), '연결이 끊긴 경우' if broken else '저장 오류가 전달된 경우', 22, INK)
    tile(draw, (42, 143, 233, 224), '#ffffff', LINE)
    tile(draw, (567, 143, 758, 224), '#ffffff', LINE)
    text(draw, (138, 171), '서비스', 24, INK, 'mm')
    text(draw, (662, 171), '화면', 24, INK, 'mm')
    text(draw, (138, 200), '응답 전송' if broken else '저장 오류 응답', 16, SUB, 'mm')
    reached = t > .94
    verdict = ('수신 확인 불가' if broken else 'failed 수신') if reached else '응답 대기'
    text(draw, (662, 200), verdict, 16, SUB, 'mm')
    y = 185
    if broken:
        draw.line((234, y, 381, y), fill=TEAL, width=4)
        draw.line((417, y, 566, y), fill=LINE, width=4)
        draw.line((385, y-10, 397, y+10), fill=INK, width=3)
        draw.line((401, y-10, 413, y+10), fill=INK, width=3)
    else:
        draw.line((234, y, 558, y), fill=TEAL, width=4)
        draw.polygon([(557, y-6), (568, y), (557, y+6)], fill=TEAL)
    x = 241 + (134 if broken else 307) * t
    tile(draw, (x-16, y-10, x+16, y+10), AMBER, INK, 2)
    draw.line([(x-15, y-8), (x, y+2), (x+15, y-8)], fill=INK, width=1)
    text(draw, (400, 260), '응답이 도착하지 않았습니다.' if broken else 'storage_status = failed', 21, SUB, 'mm')
    if reached:
        label = '기록을 조회할 때까지 저장 여부 미확인' if broken else '저장 실패로 안내하고 완료 이력에서 제외'
        tile(draw, (70, 285, 730, 326), PALE)
        text(draw, (400, 305), label, 21, INK, 'mm')


def trimming(draw, scene, pos):
    from render import text, tile, stretch, INK, SUB, TEAL, PALE, AMBER, LINE

    text(draw, (38, 94), '비교 기준', 18, SUB)
    text(draw, (173, 94), '장비 A의 점검 전 확인 사항은?', 23, INK)
    draw.line((38, 119, 761, 119), fill=LINE, width=2)
    reworded = pos >= .62
    if not reworded:
        t = stretch((pos-.06)/.32)
        text(draw, (39, 152), 'PUBLIC-DUP-01', 18, SUB)
        # Actual leading and trailing spaces travel away from the retained question.
        for side in (-1, 1):
            start = 231 if side==-1 else 569
            for j in range(2):
                x=start + side*(j*24+90*t)
                if t < .98:
                    tile(draw,(x-9,186,x+9,213),AMBER,LINE,2)
                    draw.line((x-5,197,x-5,204,x+5,204,x+5,197),fill=SUB,width=2)
        tile(draw,(249,180,551,221),PALE,TEAL)
        text(draw,(400,200),'장비 A의 점검 전 확인 사항은?',19,INK,'mm',286)
        label='strip() 전 · 양끝 공백 두 칸씩' if t < .5 else 'strip() 뒤 · 기준 문자열과 일치'
    else:
        text(draw, (39, 152), 'PUBLIC-PARAPHRASE-01', 18, SUB)
        tile(draw,(100,180,700,221),'#ffffff',LINE)
        text(draw,(400,200),'장비 A를 살펴보기 전에 볼 것은 무엇인가요?',22,INK,'mm',580)
        label='문자열 비교는 False · 의미 중복은 따로 검토'
    text(draw,(400,277),label,22,INK,'mm',714)


def regression(draw, scene, pos):
    from render import text, tile, stretch, INK, SUB, TEAL, PALE, AMBER, LINE

    u=stretch((pos-.30)/.45)
    text(draw,(40,96),'같은 공개 문항을 기준판과 후보판에서 재실행합니다.',21,SUB)
    for y,name,count,initial in [(158,'기본 문항',7,7),(238,'확장 문항',3,1)]:
        text(draw,(42,y),name,22,INK)
        for i in range(count):
            x=172+61*i
            tile(draw,(x,y-19,x+46,y+20),'#ffffff',LINE,7)
            fixed = y==238 and i>0
            # Expansion cases were 1/3. Fill only the two newly passing cases.
            portion = 1 if not fixed else stretch((u-(i-1)*.45)/.5)
            if portion>0:
                draw.rounded_rectangle((x+2,y-17,x+2+42*portion,y+18),radius=4,fill=TEAL if not fixed else AMBER)
            text(draw,(x+23,y),str(i+1),16,'#ffffff' if not fixed else INK,'mm')
        passed=initial if y==158 else 1+int(u>=.50)+int(u>=.95)
        text(draw,(665,y),f'{passed} / {count}',27,INK,'mm')
    text(draw,(400,306),'기본 7개 유지' if u<.07 else '기본 7개 유지  ·  공개 확장 2개 추가 통과',22,INK,'mm')


def deployment(draw, scene, pos):
    from render import text, tile, stretch, INK, SUB, TEAL, PALE, AMBER, LINE

    # Compose namespace boundaries stay fixed while independent packets travel through them.
    network=pos<.50
    t=stretch(((pos*2)%1-.08)/.63)
    tile(draw,(30,92,769,291),'#ffffff',LINE,14)
    text(draw,(46,111),'호스트',16,SUB)
    tile(draw,(401,108,746,277),PALE,TEAL,9)
    text(draw,(419,128),'서비스 컨테이너',18,INK)
    draw.line((197,173,592,173),fill=TEAL if network else LINE,width=4)
    draw.line((197,238,592,238),fill=LINE if network else TEAL,width=4)
    tile(draw,(47,152,230,194),'#ffffff',LINE)
    text(draw,(137,173),'127.0.0.1:8104',19,INK,'mm')
    tile(draw,(47,217,230,259),'#ffffff',LINE)
    text(draw,(137,238),'p1-json',20,INK,'mm')
    tile(draw,(526,152,721,194),'#ffffff',LINE)
    text(draw,(623,173),'포트 8104',19,INK,'mm')
    tile(draw,(526,217,721,259),'#ffffff',LINE)
    text(draw,(623,238),'runtime-data/',19,INK,'mm')
    x=240+(514-240)*t
    if network:
        draw.ellipse((x-8,165,x+8,181),fill=AMBER,outline=INK,width=2)
    else:
        draw.polygon([(x-8,228),(x+5,228),(x+10,234),(x+10,248),(x-8,248)],fill=AMBER,outline=INK)
    text(draw,(400,313),'호스트의 루프백 주소에서 컨테이너 포트로' if network else '이름 있는 볼륨을 컨테이너 디렉터리에 마운트',21,INK,'mm')


def replay_window(draw, scene, pos):
    from render import text, tile, stretch, INK, SUB, TEAL, PALE, AMBER, LINE

    r6=pos<.52
    u=stretch((((pos/.52) if r6 else (pos-.52)/.48)-.07)/.60)
    text(draw,(35,95),'복원한 alice 세션 · 보존된 요청 ID',21,SUB)
    for j,name in enumerate(['r2','r3','r4','r5','r6']):
        x=133+j*120
        selected=r6 and j==4 and u>.88
        tile(draw,(x-45,154,x+45,204),AMBER if selected else PALE,TEAL)
        text(draw,(x,179),name,24,INK,'mm')
    target=613 if r6 else 78
    x=398+(target-398)*u
    y=275-(56 if r6 else 35)*u
    tile(draw,(x-46,y-16,x+46,y+16),INK)
    text(draw,(x,y),'재요청 '+('r6' if r6 else 'r0'),16,'#ffffff','mm')
    if u>.87:
        label='r6 일치 · 중복 요청 거부' if r6 else 'r0 없음 · 이 기록만으로 중복 여부 확인 불가'
        text(draw,(400,313),label,21,INK,'mm')
    else:
        text(draw,(400,313),'재요청의 ID를 보존 목록과 대조합니다.',20,SUB,'mm')


EXTRAS = {
    105: dict(section='nb-uncertain', title='응답이 끊기면 저장 실패라고 할 수 있을까요?',
              caption='첫 장면의 화면은 결과를 받지 못해 저장 상태를 모릅니다. 다음 장면에서는 failed가 화면에 도착하므로 저장 실패를 알릴 수 있습니다. 전송이 끊기면 같은 요청 기록부터 확인합니다.', drawing='custom',paint=delivery),
    108: dict(section='nb-overlap', title='공백을 지운 자리에 어떤 차이가 남을까요?',
              caption='PUBLIC-DUP-01은 양끝 공백을 떼면 Q01과 같은 문장이 됩니다. 표현을 바꾼 두 번째 문항은 문자열이 달라도 기존 질문과 같은 내용을 물을 수 있어 사람이 의미를 대조합니다.', drawing='custom',paint=trimming),
    111: dict(section='nb-freeze', title='기본 일곱 문항과 확장 세 문항을 따로 세기',
              caption='한 칸은 공개 평가 문항 하나입니다. 기본 문항은 두 판 모두 7/7이고 확장 문항만 1/3에서 3/3으로 바뀝니다. 이 결과로 실제 사용자 질문에서의 성능까지 판정할 수는 없습니다.', drawing='custom',paint=regression),
    112: dict(section='nb-configuration', title='호스트 포트와 볼륨은 어디로 연결될까요?',
              caption='위쪽은 127.0.0.1:8104에서 서비스 포트 8104로 들어가는 경로입니다. 아래쪽은 p1-json 볼륨을 /app/input106/project-ui/backend/runtime-data에 연결한 모습입니다. 배포 시안의 두 설정을 따라간 예시입니다.', drawing='custom',paint=deployment),
    113: dict(section='nb-replay', title='복구 파일에서 r6과 r0을 다시 찾기',
              caption='최근 요청 r2~r6을 보존한 가상 복구 기록입니다. r6 재요청은 목록에서 찾아 거부하지만, 보존 구간 밖의 r0까지 과거에 처리했는지는 이 목록으로 판정할 수 없습니다.', drawing='custom',paint=replay_window),
}


AUDIT = {
    101: '기존 도구로 Q01이 RULE-A를 찾는 출력과 외부 일정 조회를 보류하는 선택 메모를 대조하는 수업이다. 두 조건을 학생이 읽고 결정할 수 있어 작성 예시를 유지했다.',
    102: '답변 생성과 저장 성공 여부를 구분하는 절에서 두 요청의 answered를 고정한 채 저장 경계의 committed와 storage_error가 갈리는 지점을 관찰한다.',
    103: '힌트 뒤 2.1절을 선택한 행동과 출처 카드 간격에 관한 가설을 실제 문장으로 구별할 수 있다. 검증하지 않은 개선 효과는 행동 시연으로 덧붙이지 않았다.',
    104: '대기 중 이전 답변과 출처 초기화 절에서 새 요청 직후 현재 본문과 RULE-A가 함께 비는 변화를 보여 준다. 과거 대화에 남는 답과 현재 카드를 구분한다.',
    105: '응답 단절과 저장 실패의 구분 절에서 전송선이 끊긴 상황과 failed가 화면까지 도착한 상황을 나란히 추적한다. 미확인 상태에서 보이는 다음 행동이 다르다.',
    106: '부분 성공과 저장 실패 인계 절에서 eval-v1:Q01의 committed와 save_failure 요청의 session_commit/OSError를 각각 같은 요청 기록에 연결한다.',
    107: '도움 없이 완료한 과업의 판정 절에서 SYN-04의 상태를 바꾸며 성공률 분모를 재계산한다. not_started는 제외되고 aborted는 시작 횟수에 남는다.',
    108: '질문 문자열 정규화와 중복 판별 절에서 공백 두 칸씩만 사라지는 Q01 변형과, 같은 의도를 다른 글자로 쓴 문항을 대조한다.',
    109: '다른 사용자의 대화 조회 거부 절에서 session_read의 거부가 None과 not_attempted로 이어지는 기록을 연결해 읽는다. 다음 절의 RULE-B는 정상 소유자의 별도 검사다.',
    110: '처리 시간과 대기 시간 절의 기존 조작에서 3.5ms 처리 구간을 고정하고 대기 폭과 총 시간을 비교한다. 운영 비용을 측정한 값으로 오해하지 않게 합성 시각을 유지한다.',
    111: '회귀 통과 범위 절에서 기본 문항 7칸과 확장 문항 3칸을 분리해 기준판과 후보판의 통과 차이를 본다. 실제 사용자 평가를 포함하지 않는 범위도 병기한다.',
    112: '접속 경로와 볼륨 절에서 한 호스트의 포트와 컨테이너 포트를 잇는 경로, 이름 있는 볼륨이 runtime-data 디렉터리에 붙는 위치를 서로 다른 높이에 표시한다.',
    113: '별도 경로로 복원하는 기존 영상에 이어 복원 레코드 검사 절에서는 보존 구간 r2~r6의 안과 밖을 대조한다. 바이트 일치와 중복 요청 검증을 구분한다.',
    114: '실행 입력·기대 출력·근거 절에서 실제 첫 질문, RULE-A, 1쪽 2.1절과 개정일을 README 예시와 대조할 수 있어 정적 인수 문서를 유지했다.',
    115: '시연 순서와 데모 실패 전환 조건은 Q01의 실제 출력과 Q02·Q03 대체 셀을 지목하는 대본으로 확인한다. 학생이 라이브로 가리킬 근거를 읽는 과제다.',
    116: '정규화 수정 범위는 Q98-N01·N02 출력, 장비AB 반례, 미생성 holdout으로 명시된다. 개인 기여와 미검증 범위는 작성된 회고 행을 근거로 확인한다.',
}
