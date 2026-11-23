"""Runtime, data and user-interface concepts (66–90)."""
from studio import (
    scene, ease, travel, INK, BLUE, TEAL, RED, GOLD, LIGHT, PAPER, MINT, PINK, YELLOW, SKY, MUTED, math
)

@scene(66, 1, 'handoff-bundle', '다음 역할에 ID만 주면 무엇이 빠질까요?', '질문, 근거 원문, 출처 ID를 함께 넘겨야 다음 역할이 원문을 다시 찾지 않고 답을 쓸 수 있습니다.')
def bundle(b, t):
    for (i, (s, c)) in enumerate([('질문', SKY), ('과제함에 제출', MINT), ('문단 p2', YELLOW)]):
        x = travel(t, 115 + 205 * i, 175 + 143 * i)
        b.chip(x, 98, s, c, 129)
    w = travel(t, 590, 461)
    b.rect((640 - w) / 2, 58, w, 84, None, BLUE)
    b.text(320, 171, '다음 역할에 넘기는 한 묶음', 21, BLUE)

@scene(67, 1, 'fact-check-xray', '맞는 인용 ID 아래 틀린 답이 숨을 수 있을까요?', '답은 개인 메신저를 가리키지만 인용한 p2 원문은 학습 관리 페이지의 과제함을 가리킵니다. ID 검사를 통과한 뒤에도 행동 지시가 일치하는지 읽습니다.')
def xray(b, t):
    b.chip(118, 43, 'p2  인용 ID', MINT, 160, 34)
    b.check(228, 43)
    for (i, (s, c)) in enumerate([('답변    개인 메신저로만 제출', PINK), ('원문    학습 관리 페이지 과제함에 제출', MINT)]):
        y = 75 + i * 57
        b.rect(50, y, 540, 45, c)
        b.text(318, y + 23, s, 20, INK, True)
    x = travel(t, 135, 462)
    b.line((x, 66, x, 182), BLUE, 3)

@scene(68, 2, 'two-verdicts', '422와 빈 근거는 어디에서 갈라질까요?', '공백 질문은 입력 검사에서 422가 됩니다. 형식이 맞는 질문으로 검색을 마쳤지만 문서가 없었다면 입력 오류로 고칠 이유가 없습니다.')
def verdicts(b, t):
    b.text(141, 36, '공백 질문', 19)
    b.text(480, 36, '유효한 질문', 19)
    b.rect(38, 57, 214, 105, PAPER, INK)
    b.rect(370, 57, 214, 105, PAPER, INK)
    b.stamp(145, travel(t, 73, 111), '422', False, 126)
    b.text(475, 111, '검색 결과  [ ]', 21, TEAL, True)
    b.text(320, 189, '요청 형식과 검색 결과는 다른 판정', 17)

@scene(69, 1, 'newline-framer', '받은 조각의 끝이 이벤트의 끝일까요?', 'NDJSON은 줄바꿈을 만났을 때 한 줄을 읽습니다. 네트워크가 JSON 중간에서 나눠 보내면 뒷조각이 올 때까지 그 줄을 버퍼에 둡니다.')
def framer(b, t):
    b.text(121, 37, '수신 버퍼', 20)
    b.rect(43, 62, 554, 70, INK)
    wire = '{"type":"delta","text":"과제함에 제출하세요."}'
    n = int(len(wire) * ease(t, 0.08, 0.65))
    b.text(300, 96, wire[:n] + ('  \\n' if t > 0.72 else ''), 19, PAPER, True)
    b.lamp(118, 174, t > 0.72)
    b.text(343, 173, '줄 완성 · 이벤트 하나' if t > 0.72 else '줄바꿈을 기다리는 중', 21)

@scene(70, 1, 'ready-index', '접수한 문서가 곧바로 검색될까요?', 'received 상태의 문서를 접수한 뒤 본문을 준비해 ready로 바꿉니다. 준비 전후를 나누어야 아직 비어 있는 문서를 검색 근거로 쓰지 않습니다.')
def ready(b, t):
    b.page(37, 38, 277, 144, 'DB의 문서 한 행', 0)
    saved = t > 0.67
    b.text(176, 99, '과제는 학습 관리 페이지의' if saved else 'body = NULL', 18)
    if saved:
        b.text(176, 125, '과제함에 제출합니다.', 17)
    b.text(176, 154, 'ready' if saved else 'received', 20, TEAL, True)
    b.text(462, 66, 'UPDATE 한 문장', 21, INK, True)
    b.meter(366, 100, 190, ease(t, 0.1, 0.67), 1)
    b.text(462, 147, '본문과 상태를 함께 확정', 16)

@scene(71, 1, 'image-imprint', '이미지에 적힌 CMD는 언제 실행될까요?', '이미지는 시작 명령을 보관합니다. 컨테이너를 시작하면 그 명령으로 프로세스가 생깁니다. 이 그림은 원리 설명이며 실제 Docker 실행 여부는 셀 출력에서 확인합니다.')
def imprint(b, t):
    for (i, c) in enumerate([LIGHT, SKY, MINT]):
        b.rect(47, 99 - i * 16, 237, 48, c, INK, 4)
    b.text(167, 92, 'CMD · uvicorn', 20, INK, True)
    b.rect(355, 50, 224, 116, None, INK)
    b.text(469, 72, '실행 중인 컨테이너', 16)
    b.circ(410, 120, 13 * ease(t), TEAL)
    b.text(492, 120, '프로세스' if t > 0.42 else '', 21)
    b.text(169, 175, '이미지 레이어', 18)

@scene(72, 2, 'persistent-volume', '컨테이너를 바꿀 때 데이터는 어디에 남을까요?', '기존 볼륨에 있던 데이터를 새 DB 컨테이너가 같은 위치에 다시 연결해 읽습니다. 같은 이름의 새 컨테이너만 만들어서는 이 연결이 보장되지 않습니다.')
def volume(b, t):
    x = travel(t, 75, -210, 0.09, 0.43)
    b.rect(x, 37, 212, 64, SKY, INK)
    b.text(x + 106, 68, '이전 DB 컨테이너', 18)
    x = travel(t, 661, 310, 0.37, 0.77)
    b.rect(x, 37, 235, 64, MINT, INK)
    b.text(x + 118, 68, '새 DB 컨테이너', 19)
    b.cylinder(218, 144, 206, 47, '같은 자료 볼륨')
    if t < 0.39:
        b.line((181, 103, 283, 144), BLUE, 3)
    if t > 0.74:
        b.line((426, 103, 364, 144), TEAL, 3)

@scene(73, 1, 'distance-triangle', '좌표 두 칸이 다르면 거리는 왜 1.414일까요?', 'p1은 질문과 같은 점이라 거리가 0입니다. p2는 두 축에서 각각 1만큼 달라 직각삼각형의 빗변 길이 √2만큼 떨어져 있습니다.')
def triangle(b, t):
    (x, y) = (140, 154)
    a = 91
    b.line((x, y, x + a, y, x + a, y - a), MUTED, 3)
    f = ease(t)
    b.line((x, y, x + a * f, y - a * f), TEAL, 5)
    b.circ(x, y, 7, BLUE)
    b.circ(x + a, y - a, 7, TEAL)
    b.text(94, 165, '질문·p1', 18)
    b.text(256, 41, 'p2', 18)
    b.text(x + a / 2, 178, '1', 18)
    b.text(x + a + 20, 114, '1', 18)
    b.text(459, 89, 'p1   0.000', 24)
    b.text(459, 135, 'p2   √2 ≈ 1.414', 25, TEAL, True)

@scene(74, 1, 'published-port', '외부에서 보이는 포트와 안쪽 포트는 같을까요?', '프록시의 443만 호스트에 공개합니다. 안쪽의 api:8000은 공통 네트워크에서 프록시가 찾는 목적지입니다.')
def ports(b, t):
    b.rect(182, 37, 414, 138, None, INK)
    b.text(504, 59, '내부 네트워크', 16)
    b.line((41, 113, 570, 113), LIGHT, 5)
    b.rect(174, 83, 16, 60, SKY, BLUE)
    b.chip(284, 113, '프록시 :443', PAPER, 145)
    b.chip(486, 113, 'api:8000', MINT, 139)
    b.line((52, 139, 410, 139, 410, 113, 417, 113), BLUE, 2)
    b.circ(travel(t, 52, 410, .1, .69), travel(t, 139, 113, .69, .84), 7, GOLD)
    b.text(87, 78, '외부 HTTPS', 18)

@scene(75, 2, 'row-diff', '같은 행 수 아래 무엇이 달라졌을까요?', '원본과 복구본에 모두 한 행이 있어도 같은 키의 본문이 다르면 복구 검사는 실패합니다. 확대경은 개수가 아닌 실제 행 내용을 대조합니다.')
def rowdiff(b, t):
    for (i, (label, v)) in enumerate([('원본 · 1행', '과제함에 제출합니다.'), ('복구본 · 1행', '제출 기한 미확인')]):
        x = 37 + i * 292
        b.page(x, 44, 261, 120, label, 0)
        b.text(x + 129, 118, v, 18)
    b.lens(travel(t, 161, 458), 117, 36)
    b.text(317, 191, '같은 키   (alice, doc-1)', 17)

@scene(76, 2, 'ci-barrier', '검사 프로그램이 1을 돌려주면 게시 작업은?', '종료 코드 1은 검사 실패입니다. check에 의존하는 publish는 건너뜁니다. 게시를 실행했다가 실패한 경우와 구별하세요.')
def barrier(b, t):
    b.line((54, 144, 585, 144), MUTED, 4)
    b.chip(144, 104, 'check · 1', PINK, 145)
    a = travel(t, -1.15, 0)
    (x, y) = (310, 137)
    b.line((x, y, x + 119 * math.cos(a), y + 119 * math.sin(a)), RED, 9)
    b.circ(x, y, 11, GOLD, INK)
    b.text(506, 81, 'publish', 25)
    b.text(506, 113, 'skipped', 19, MUTED)
    b.text(160, 180, '검사 실패', 19, RED)

@scene(77, 1, 'floating-tag', '태그를 옮겨도 이미지 내용의 지문이 바뀔까요?', '같은 태그가 다른 이미지 바이트를 가리킬 수 있습니다. 검토한 후보를 다시 지정할 때는 그 내용의 digest를 대조합니다.')
def tag(b, t):
    for (i, (s, c)) in enumerate([('이미지 A', SKY), ('이미지 B', MINT)]):
        x = 67 + i * 304
        b.rect(x, 79, 200, 82, c, INK)
        b.text(x + 100, 105, s, 21)
        for j in range(18):
            b.rect(x + 16 + j * 9, 131, 2 + j * (i + 2) % 6, 16, INK, None, 0)
    x = travel(t, 165, 470)
    b.chip(x, 45, '같은 태그', YELLOW, 120, 32)
    b.line((x, 61, x, 79), GOLD, 3)

@scene(78, 1, 'label-focus', '레이블을 눌렀을 때 커서는 어디에 생길까요?', 'for와 id가 같으면 레이블을 눌러도 연결된 입력칸에 초점이 갑니다. 두 값이 다르면 그 관계가 끊깁니다.')
def focus(b, t):
    b.chip(145, 84, '할 일 제목', YELLOW, 159)
    b.text(145, 142, 'for="todo-title"', 16)
    b.rect(334, 58, 240, 59, PAPER, BLUE if t > 0.48 else INK)
    b.text(457, 142, 'id="todo-title"', 16)
    if t > 0.48:
        b.line((352, 68, 352, 106), BLUE, 3)
    x = travel(t, 73, 145, 0.08, 0.4)
    y = travel(t, 160, 96, 0.08, 0.4)
    b.poly((x, y, x + 7, y + 25, x + 13, y + 16, x + 25, y + 16), INK)

@scene(79, 2, 'response-unfold', '응답이 도착하면 답 문장도 곧바로 읽을 수 있을까요?', '응답 상태를 받은 것과 본문을 파싱해 answer를 꺼낸 것은 다른 관찰입니다. 본문을 펼쳐야 답 문장과 출처가 보입니다.')
def unfold(b, t):
    b.rect(64, 34, 507, 49, SKY, INK)
    b.text(318, 59, 'HTTP 응답 도착', 23, INK, True)
    h = travel(t, 5, 91)
    b.rect(77, 85, 479, h, PAPER, INK, 2)
    if h > 44:
        b.text(317, 114, '과제함에 제출하세요.', 22)
    if h > 69:
        b.text(317, 150, 'course-guide-v1:p2', 17, TEAL)
    b.text(320, 195, '응답 본문', 16)

@scene(80, 2, 'blank-title', '빈 제목을 거절하면 목록에는 몇 건이 남을까요?', '공백뿐인 제목을 정리하면 쓸 글자가 없습니다. INVALID_TITLE을 돌려주고 저장 목록에는 새 행을 만들지 않습니다.')
def blank(b, t):
    n = round(3 * (1 - ease(t)))
    b.text(135, 44, '제목의 공백', 18)
    for i in range(n):
        x = 69 + i * 62
        b.rect(x - 25, 92, 50, 40, PAPER, INK)
        b.line((x - 9, 106, x - 9, 117, x + 9, 117, x + 9, 106), BLUE, 2)
    b.text(470, 44, '저장 목록', 18)
    b.rect(358, 75, 221, 74, PAPER, INK)
    b.text(468, 112, '0건', 30)
    if not n:
        b.stamp(139, 109, 'INVALID_TITLE', False, 178)

@scene(81, 2, 'status-card', '없는 항목의 수정을 요청하면 기존 목록도 바뀔까요?', '1번 항목을 완료로 바꾸면 200입니다. 없는 999번을 수정하면 404가 돌아오지만 화면에 있던 1번 행은 그대로 남습니다.')
def card(b, t):
    b.rect(48, 33, 544, 150, PAPER, INK)
    first = t < 0.54
    b.text(234, 65, 'PATCH /todos/1' if first else 'PATCH /todos/999', 21)
    b.chip(490, 65, '200' if first else '404', MINT if first else PINK, 100, 34)
    b.line((66, 93, 573, 93), LIGHT, 2)
    b.chip(234, 131, '복습 · 완료', MINT, 186, 36)
    b.text(460, 129, '목록의 1번 행 유지', 17, INK)
    if not first:
        b.text(321, 164, '999번 항목은 찾지 못했습니다.', 16, RED)

@scene(82, 1, 'reopen-database', '연결을 닫으면 저장한 할 일도 사라질까요?', '파일 DB에 커밋한 복습 50% 행은 연결 객체를 새로 만들어도 같은 파일에서 읽을 수 있습니다.')
def reopen(b, t):
    b.cylinder(215, 94, 213, 77, 'todos.db')
    b.text(322, 193, '1번 행 · 복습 50%', 18)
    for (i, s) in enumerate(['첫 연결', '새 연결']):
        x = 93 + i * 448
        b.chip(x, 52, s, SKY if i == 0 else MINT, 101, 36)
        f = 1 - ease(t, 0.15, 0.43) if i == 0 else ease(t, 0.52, 0.82)
        b.line((x, 75, x + (320 - x) * f, 75 + 25 * f), BLUE, 3)

@scene(83, 1, 'toggle-rocker', '같은 완료 요청을 두 번 보내면 스위치는 어디에 있을까요?', '현재 값을 뒤집으면 첫 요청 뒤 True, 재전송 뒤 False입니다. 요청에 적힌 최종값 True를 대입하면 재전송 뒤에도 True가 남습니다.')
def rocker(b, t):
    pulse = ease(t, 0.15, 0.35)
    again = ease(t, 0.55, 0.77)
    for (i, (s, v)) in enumerate([('현재 값 뒤집기', pulse - again), ('원하는 값 대입', pulse)]):
        x = 165 + i * 311
        b.text(x, 47, s, 19)
        b.rect(x - 81, 83, 162, 55, MINT if v > 0.5 else LIGHT, INK, 28)
        b.circ(x - 53 + 106 * v, 110, 20, PAPER, INK)
        b.text(x, 172, 'True' if v > 0.5 else 'False', 21, INK, True)

@scene(84, 1, 'schema-extension', '기존 행에 새 열을 붙이면 어떤 값이 생길까요?', '기존 제목 복습은 남습니다. 마감일은 None, 우선순위는 기본값 normal로 시작해 새 스키마에서도 행을 읽을 수 있습니다.')
def extension(b, t):
    b.slot(39, 89, 170, '제목 · 복습', SKY)
    for (i, (s, c)) in enumerate([('마감일 · None', PAPER), ('우선순위 · normal', MINT)]):
        x = travel(t, 658 + 188 * i, 216 + 194 * i, 0.13, 0.77)
        b.slot(x, 89, 187, s, c)
    b.text(319, 42, '기존 행의 열 확장', 21)
    b.bracket(220, 595, 153, '새 열의 초기값')

@scene(85, 2, 'shared-record', '앱을 새로 띄워도 같은 행을 읽을 수 있을까요?', '새 앱 인스턴스가 같은 DB를 읽으면 저장했던 복습, 2027-04-02, high가 함께 돌아옵니다. 앱의 수명과 행의 수명을 따로 볼 수 있습니다.')
def instance(b, t):
    b.cylinder(54, 59, 208, 100, '같은 DB')
    for (i, s) in enumerate(['앱 A', '새 앱 B']):
        b.chip(473, 65 + i * 80, s, SKY if not i else MINT, 139)
    b.line((267, 106, 394, travel(t, 65, 145)), TEAL, 4)
    b.text(316, 191, '복습    /    2027-04-02    /    high', 19)

@scene(86, 1, 'handover-lamp', '교대 담당자가 가리켜야 할 물체는 무엇일까요?', '장비 A의 규정 2.1은 점검 전에 전원 표시등을 확인하라고 합니다. 막연한 “점검”을 실제로 확인할 물체와 원문 위치까지 좁힌 예입니다.')
def panel(b, t):
    b.rect(48, 43, 273, 120, INK)
    b.lamp(105, 102, t > 0.4, 19)
    b.text(213, 102, '전원 표시등', 20, PAPER)
    b.page(382, 40, 196, 137, '규정 A', 1)
    b.text(479, 123, '§ 2.1', 27, TEAL, True)
    b.lens(travel(t, 203, 105), 102, 34)

@scene(87, 1, 'missing-equipment', '장비 이름이 빠졌을 때 왜 다음 행동이 질문일까요?', '“점검 전 확인 사항은?”에는 장비가 지정되지 않았습니다. A와 B의 서로 다른 규정 중 하나를 임의로 고르지 않고 장비명을 다시 묻습니다.')
def missing(b, t):
    b.chip(317, 40, '어느 장비인가요?', YELLOW, 238)
    for (i, s) in enumerate(['A · 전원 표시등', 'B · 고정 장치']):
        x = 169 + i * 301
        b.rect(x - 119, 103, 238, 62, SKY if i == 0 else MINT, INK)
        b.text(x, 134, s, 20)
        f = ease(t)
        b.line((321, 65, 321 + (x - 321) * f, 65 + 31 * f), MUTED, 2)
    b.text(320, 190, 'need_clarification', 17)

@scene(88, 1, 'source-ruler', '“출처가 있다”를 무엇으로 확인할까요?', '수용 기준에는 문서 이름과 쪽·절·개정일·판본이 있습니다. 규정 이름만 보이는 상태와 원문 위치까지 다시 찾을 수 있는 상태를 구분합니다.')
def ruler(b, t):
    b.text(320, 28, 'RULE-A · 인용에 필요한 다섯 필드', 20, INK, True)
    labels = ['문서', '쪽', '절', '개정일', '판본']
    values = ['규정 A', '1', '2.1', '2026-11-01', 'rules-v1']
    for (i, (label, value)) in enumerate(zip(labels, values)):
        x = 67 + i * 126
        b.text(x, 73, label, 18)
        y = travel(t, 167, 118, 0.12, 0.7)
        b.rect(x - 56, 96, 112, 42, PAPER, INK)
        b.text(x, y, value, 17, TEAL, True, 105)
    b.text(319, 192, 'ID만 있으면 나머지 원문 위치를 다시 찾아야 합니다.', 16)

@scene(89, 2, 'offline-copy', '연결이 끊기면 어떤 규정을 읽을 수 있을까요?', '수업에서 미리 확보한 허용 규정 RULE-A와 RULE-B는 사본으로 확인할 수 있습니다. 사본 밖 자료를 읽었다고 기록할 수는 없습니다.')
def offline(b, t):
    b.text(135, 49, '외부 자료', 19)
    b.rect(53, 72, 170, 67, PAPER, INK)
    b.text(138, 105, '연결', 19)
    b.line((226, 106, 284, 106), BLUE, 3)
    b.line((284, 106, 335, 106 - 47 * ease(t, 0.15, 0.54)), BLUE, 4)
    b.line((335, 106, 388, 106), MUTED, 3)
    b.page(404, 37, 160, 123, '수업용 사본', 0)
    b.text(485, 98, 'RULE-A', 19)
    b.text(485, 130, 'RULE-B', 19)
    b.stamp(317, 181, '사본 사용' if t > 0.54 else '연결 가능', True, 131)

@scene(90, 1, 'expected-pair', '기대하는 답과 출처를 왜 한 쌍으로 둘까요?', 'Q01의 답을 평가할 때 RULE-A도 함께 대조합니다. 답할 근거가 없는 문항에는 출처를 비워 둬야 만들어 낸 인용을 발견할 수 있습니다.')
def pair(b, t):
    stage = t > 0.52
    b.text(316, 32, 'Q03 · 근거 없는 일정 문의' if stage else 'Q01 · 장비 A 점검', 21, INK, True)
    for (x, head, val) in [(172, '기대 상태 / 핵심 사실', 'no_evidence' if stage else '전원 표시등'), (468, '기대 출처', '[  ]' if stage else 'RULE-A')]:
        b.text(x, 74, head, 17)
        b.chip(x, 125, val, MINT if stage else SKY, 201, 48)
        b.check(x, 173)
