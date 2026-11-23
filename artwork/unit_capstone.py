"""Source-grounded reading, interaction design and evaluation (91–116)."""
from studio import (
    scene, ease, travel, INK, BLUE, TEAL, RED, GOLD, LIGHT, PAPER, MINT, YELLOW, SKY, MUTED, math
)

@scene(91, 2, 'intent-key', '장비 A가 같으면 교체 일정도 알 수 있을까요?', '점검 전 확인 사항과 교체 일정은 서로 다른 질문입니다. 장비 이름만 맞추는 첫 구현은 두 질문에 같은 점검 문장을 반환해 일정 질문에서 틀립니다.')
def intent(b, t):
    b.chip(112, 82, '장비 A', MINT, 113)
    b.chip(321, 82, '교체 일정' if t > 0.46 else '점검 전 확인', YELLOW, 169)
    b.rect(46, 119, 134, 9, TEAL)
    b.text(110, 158, '항상 일치', 16, TEAL)
    b.chip(509, 146, '전원 표시등', PAPER, 152)
    b.arrow(163, 105, 400, 143)
    if t > 0.46:
        b.check(594, 146, False)
    b.text(321, 30, '질문에서 장비 이름만 읽는 규칙', 19)

@scene(92, 2, 'baseline-error', '7문항 중 두 개를 맞힌 기록에서 어디를 고칠까요?', 'Q03의 기대는 no_evidence와 빈 출처입니다. 첫 구현은 장비명만 보고 answered와 RULE-A를 반환했습니다. 전체 점수에서 이 한 행을 꺼내야 오류가 보입니다.')
def baseline(b, t):
    b.text(154, 29, '첫 기준선  2 / 7', 20, INK, True)
    for i in range(7):
        x = 37 + i * 39
        b.circ(x, 82, 10, TEAL if i in [1, 5] else LIGHT, INK)
        b.text(x, 57, f'Q0{i + 1}', 13)
    b.rect(321, 29, 291, 151, PAPER, INK)
    b.text(467, 55, 'Q03 · 일정 문의', 19)
    b.text(467, 98, '기대   no_evidence  /  [ ]', 18, TEAL)
    b.text(467, 140, '실제   answered  /  RULE-A', 18, RED)
    f = ease(t)
    b.line((115, 96, 115, 118, 115 + 205 * f, 118), BLUE, 3)

@scene(93, 2, 'paired-status', '출처 칸은 답변 상태와 어떻게 맞물릴까요?', '답을 근거로 확인한 Q01에는 RULE-A가 붙습니다. 근거가 없는 질문을 표시할 때는 상태를 바꾸면서 현재 출처 목록도 비워야 합니다.')
def paired(b, t):
    b.rect(77, 49, 477, 119, PAPER, INK)
    b.text(170, 77, '답변 상태', 16)
    b.text(456, 77, '현재 출처', 16)
    yes = t < 0.52
    b.chip(175, 123, 'answered' if yes else 'no_evidence', MINT if yes else YELLOW, 160)
    b.chip(452, 123, 'RULE-A' if yes else '[  ]', SKY if yes else PAPER, 142)
    b.line((272, 122, 352, 122), INK, 3)
    b.circ(travel(t, 276, 348), 122, 8, TEAL)

@scene(94, 2, 'byte-fingerprint', '같은 검색 문장에 왜 서로 다른 원문 지문이 붙을까요?', 'UTF-8에서 공백 한 바이트 0x20과 줄바꿈 한 바이트 0x0A는 다릅니다. 원문을 해시하면 지문이 달라지고, 공백을 정리한 검색 문장은 같습니다.')
def fingerprint(b, t):
    import hashlib
    raw = '점검 전' + (' ' if t < 0.48 else '\n') + '전원 표시등을 확인합니다.'
    digest = hashlib.sha256(raw.encode()).digest()
    b.chip(121, 79, '0x20 · 공백' if t < 0.48 else '0x0A · 개행', YELLOW, 148)
    for (i, v) in enumerate(digest):
        for j in range(8):
            if v & 1 << j:
                b.rect(267 + i * 9, 44 + j * 10, 7, 8, BLUE, None, 0)
    b.text(410, 150, digest.hex()[:16] + '…', 19, INK, True)
    b.text(319, 190, '검색용 본문  ·  점검 전 전원 표시등을 확인합니다.', 18)

@scene(95, 1, 'allowed-library', '검색 목록이 비면 모든 자료에 답이 없다는 뜻일까요?', '검색은 현재 그룹에 허용된 자료 안에서만 이뤄집니다. 빈 목록은 이번 검색 범위 안에서 근거를 찾지 못했다는 결과입니다.')
def allowed(b, t):
    b.rect(29, 40, 360, 126, MINT, TEAL)
    b.text(203, 59, 'public에서 열 수 있는 문서', 17)
    b.page(50, 83, 139, 66, 'RULE-A', 1)
    b.page(213, 83, 139, 66, 'RULE-B', 1)
    b.rect(412, 62, 194, 87, LIGHT, MUTED)
    b.text(509, 88, 'RULE-ADMIN', 19)
    b.text(509, 124, 'admin만 허용', 17, RED)
    b.lens(travel(t, 113, 276), 113, 21)
    b.text(319, 193, '“관리자 전용 절차” 검색   ·   허용 범위의 결과 [  ]', 18, INK, True)

@scene(96, 1, 'section-zoom', 'RULE-A만 보고 원문의 한 줄을 다시 찾을 수 있을까요?', '문서에서 1쪽 2.1절로 좁히면 전원 표시등을 확인하라는 근거가 나옵니다. 개정일과 rules-v1은 어느 판본에서 읽었는지 남깁니다.')
def zoom(b, t):
    b.page(44, 23, 296, 166, '규정 A · 1쪽', 0)
    for (i, s) in enumerate(['1. 개요', '2. 점검', '2.1  전원 표시등']):
        b.text(193, 74 + i * 35, s, 18)
    b.lens(travel(t, 174, 149), travel(t, 72, 145), 23)
    b.text(476, 82, '§ 2.1', 35, TEAL, True)
    b.text(476, 132, '2026-11-01', 19)
    b.text(476, 161, 'rules-v1', 17, MUTED)

@scene(97, 2, 'turn-filmstrip', '새 질문이 와도 예전 턴의 근거까지 지워질까요?', '화면은 현재 턴의 출처만 읽습니다. Q03에서 빈 목록이 보이더라도 이력의 Q01은 RULE-A를 유지하고, Q04에는 RULE-B가 붙습니다.')
def strip(b, t):
    for (i, (q, s)) in enumerate([('Q01', 'RULE-A'), ('Q03', '[  ]'), ('Q04', 'RULE-B')]):
        x = 38 + i * 197
        b.rect(x, 71, 166, 79, PAPER, INK, 2)
        b.text(x + 83, 92, q, 16)
        b.text(x + 83, 126, s, 22)
    x = travel(t, 35, 429)
    b.rect(x, 65, 172, 91, None, TEAL, 3)
    b.text(322, 187, '이력에서 현재 표시할 턴', 18)

@scene(98, 2, 'word-boundary', 'A 뒤에 B가 더 있으면 틈을 내도 될까요?', 'A·B 뒤가 문자열 끝이거나 다음 글자가 영문·숫자가 아닐 때만 공백을 넣습니다. “장비A의”는 바뀌지만 “장비AB”에는 A 뒤에 B가 이어져 원문이 유지됩니다.')
def word(b, t):
    from studio import font, SCALE
    face = font(29, True)
    for (i, tail) in enumerate(['A의', 'AB']):
        y = 66 + i * 80
        left = 78
        w = face.getlength('장비') / SCALE
        more = face.getlength(' ') / SCALE * ease(t) if not i else 0
        b.text(left + w / 2, y, '장비', 29, INK, True)
        b.text(left + w + more + face.getlength(tail) / SCALE / 2, y, tail, 29, BLUE, True)
        if more > 1:
            b.rect(left + w, y + 20, more, 4, GOLD, None, 0)
        b.text(439, y, '한글 의가 이어짐 · 적용' if not i else '영문 B가 이어짐 · 유지', 20)
    b.text(317, 191, '추가한 공백만 금색으로 표시합니다.', 16)

@scene(99, 2, 'retry-budget-clock', '똑같이 두 번 시도했는데 끝 상태가 왜 다를까요?', '첫 시간 초과 뒤에는 한 번 더 시도할 수 있습니다. 두 번째 결과가 성공이면 완료하고 다시 시간 초과면 예산을 소진해 중단합니다.')
def clocks(b, t):
    for (i, s) in enumerate(['회복한 두 번째 시도', '두 번째도 시간 초과']):
        x = 153 + i * 315
        b.circ(x, 105, 53, None, INK)
        b.line((x + 46, 105, x + 60, 105), RED, 4)
        stop = 0.71 if not i else 1
        a = -math.pi / 2 + math.pi / 2 * min(ease(t, 0.12, 0.79), stop)
        b.line((x, 105, x + 45 * math.cos(a), 105 + 45 * math.sin(a)), BLUE, 4)
        b.text(x, 27, s, 17)
        b.text(x, 177, ('성공 · 완료' if not i else '한도 도달 · 중단') if t > 0.77 else '응답 대기', 18)
    b.text(318, 201, '빨간 눈금은 설명용 시간 제한선입니다.', 14, MUTED)

@scene(100, 2, 'five-turn-window', '여섯 번째 턴을 쓰면 어느 기록이 밀릴까요?', '이 설계는 세션 안에서 최근 다섯 턴만 유지합니다. 새 턴이 들어오면 가장 오래된 턴이 빠집니다. 세션 전체의 300초 만료 조건은 별도로 적용됩니다.')
def window(b, t):
    for i in range(6):
        x = 115 + i * 83 - 83 * ease(t)
        b.chip(x, 106, '턴 ' + str(i + 1), SKY if i < 5 else MINT, 70)
    b.rect(0, 64, 72, 88, '#fbf0e9', None, 0)
    b.rect(495, 62, 145, 89, '#fbf0e9', None, 0)
    b.rect(72, 72, 423, 70, None, INK)
    b.text(283, 42, '최근 5턴', 22, INK, True)
    b.text(315, 180, '오래된 쪽  ←                           새 턴', 17)

@scene(101, 1, 'missing-roster', '규정 문서로 근무 교대표를 채울 수 있을까요?', '장비 규정과 개인 근무 일정은 다른 자료입니다. 일정 자료와 조회 권한을 확인하기 전에는 교대표를 채워 넣지 않고 연동을 보류합니다.')
def roster(b, t):
    b.page(48, 47, 199, 124, '장비 규정', 3)
    b.rect(313, 40, 272, 132, PAPER, INK)
    b.text(451, 65, '근무 일정', 18)
    for i in range(4):
        b.line((329 + i * 79, 87, 329 + i * 79, 154), LIGHT)
    for y in [87, 119, 154]:
        b.line((329, y, 566, y), LIGHT)
    b.stamp(452, travel(t, 186, 118), '연동 보류', False, 131)

@scene(102, 2, 'split-receipt', '답을 만들었다는 영수증이 저장까지 보장할까요?', '계산한 답과 저장 결과는 독립된 필드입니다. 저장 실패 사례에서는 답이 있어도 저장을 완료했다고 표시할 수 없습니다.')
def receipt(b, t):
    b.page(122, 27, 390, 165, '요청 처리 기록', 0)
    b.text(221, 82, '답 생성', 20)
    b.check(415, 82)
    for x in range(146, 490, 14):
        b.line((x, 109, x + 6, 109), MUTED)
    b.text(220, 144, '저장', 20)
    b.stamp(414, travel(t, 173, 144), '실패', False, 95)

@scene(103, 1, 'hint-divider', '힌트를 받은 뒤 찾은 근거를 자력 성공으로 셀까요?', '가상 관찰에서는 답을 읽고 멈췄다가 힌트 뒤에 2.1절을 선택했습니다. 힌트 시점 앞뒤를 나누어야 다음 화면에서 무엇을 고칠지 판단할 수 있습니다.')
def hint(b, t):
    b.line((54, 117, 586, 117), INK, 3)
    b.rect(335, 58, 4, 107, GOLD)
    b.text(338, 36, '힌트 제공', 17, GOLD, True)
    x = travel(t, 75, 550)
    b.circ(x, 117, 10, BLUE)
    b.text(176, 156, '답에서 멈춤', 19)
    b.text(487, 156, '§ 2.1 선택', 19)
    b.text(318, 193, '가상 관찰 기록', 16, MUTED)

@scene(104, 2, 'clear-on-send', '새 요청이 대기하는 동안 무엇을 지워야 할까요?', '직전 질문의 답과 출처를 함께 비웁니다. 새 요청의 결과가 도착한 뒤에야 그 요청의 답과 근거를 표시합니다.')
def erase(b, t):
    b.rect(70, 39, 491, 131, PAPER, INK)
    b.text(305, 83, '직전 질문의 답', 21)
    b.chip(308, 130, '직전 출처 · RULE-A', SKY, 220, 35)
    w = travel(t, 0, 482, 0.1, 0.67)
    b.rect(74, 45, w, 119, PAPER, None, 0)
    if t > 0.69:
        b.text(311, 104, '새 요청 대기 중', 23, BLUE, True)
    b.text(313, 191, '새 질문을 보낸 화면', 18)

@scene(105, 2, 'lost-ack', '응답이 끊기면 저장 실패로 단정할 수 있을까요?', '응답을 받지 못한 클라이언트는 저장 결과를 알 수 없습니다. 같은 요청을 다시 보내기 전에 해당 요청의 기록을 확인하는 안내가 필요합니다.')
def ack(b, t):
    b.chip(117, 94, '서버', SKY, 114)
    b.chip(521, 94, '화면', MINT, 114)
    for x in range(180, 460, 18):
        b.line((x, 94, x + 8, 94), LIGHT, 3)
    x = travel(t, 187, 320, 0.12, 0.5)
    if t < 0.55:
        b.circ(x, 94, 9, BLUE)
    else:
        b.line((312, 72, 330, 87, 307, 103, 323, 122), RED, 4)
    b.text(319, 174, '응답 미수신 · 저장 여부 미확인', 21, RED, True)

@scene(106, 2, 'two-indicators', '답은 있는데 저장에 실패한 요청은 어떻게 보일까요?', '계산 완료와 저장 완료를 두 표시등으로 봅니다. 저장 실패 사례에서는 답 계산 쪽만 켜지고 저장 완료 쪽은 켜지지 않습니다.')
def indicators(b, t):
    b.rect(70, 40, 499, 136, INK)
    for (i, s) in enumerate(['답 계산 완료', '저장 완료']):
        x = 192 + i * 255
        b.lamp(x, 92, t > 0.32 and (not i), 23)
        b.text(x, 145, s, 20, PAPER, True)
    b.text(316, 196, 'save_failure 사례', 16, MUTED)

@scene(107, 1, 'observed-attempts', '과업을 시작한 횟수와 성공한 횟수는 같을까요?', '가상 과업은 세 번 시작했고 한 번 성공했습니다. 시작한 세 건을 분모로 두어야 완료한 한 건의 뜻을 읽을 수 있습니다.')
def attempts(b, t):
    for (i, (key, result)) in enumerate([('01', '성공'), ('02', '실패'), ('03', '중단'), ('04', '시작 전')]):
        x = 77 + i * 157
        y = 85 + (48 * ease(t) if i == 3 else 0)
        b.chip(x, y, 'SYN-' + key, MINT if i == 0 else LIGHT, 108)
        b.text(x, y + 41, result, 18)
    b.bracket(25, 441, 158, '시작한 세 건 중 성공 한 건')
    b.text(547, 191, '분모 밖', 16, RED)

@scene(108, 1, 'trim-overlay', 'ID가 다른 질문이 같은 평가 문항일 수 있을까요?', 'PUBLIC-DUP-01은 Q01 문장의 양끝에 공백을 붙인 예입니다. 양끝을 정리한 두 문장을 겹치면 ID가 달라도 질문 내용은 같습니다.')
def trim(b, t):
    from studio import font, SCALE
    sentence = '장비 A의 점검 전 확인 사항은?'
    w = font(21, True).getlength(sentence) / SCALE
    start = 250
    for (i, key) in enumerate(['Q01', 'DUP-01']):
        y = 62 + i * 70
        b.text(83, y, key, 17)
        b.text(start + w / 2, y, sentence, 21, INK, True)
        if i:
            gap = 18 * (1 - ease(t))
            for j in range(2):
                b.rect(start - (j + 1) * gap, y + 13, gap * 0.82, 5, GOLD, None, 0)
                b.rect(start + w + j * gap, y + 13, gap * 0.82, 5, GOLD, None, 0)
    b.text(321, 186, '금색은 양끝 공백 두 칸씩입니다.', 17)

@scene(109, 2, 'owner-pocket', '다른 사람의 대화를 막아도 내 대화는 열릴까요?', '예시에서 bob은 자기 대화의 장비 B 근거 RULE-B를 읽습니다. 본인 기록을 읽을 수 있다는 정상 사례도 함께 점검합니다.')
def pocket(b, t):
    for (i, s) in enumerate(['alice', 'bob']):
        x = 61 + 299 * i
        b.rect(x, 55, 217, 112, SKY if i == 0 else MINT, INK)
        if i:
            b.chip(x + 109, travel(t, 114, 63), 'RULE-B', YELLOW, 126)
        b.rect(x + 4, 103, 209, 61, PAPER, INK)
        b.text(x + 110, 134, s, 22, INK, True)
    b.text(321, 189, '조회 주체  bob', 18)

@scene(110, 1, 'stopwatch-span', '12와 15.5라는 눈금 사이에서 잰 값은 무엇일까요?', '서비스 시작과 종료에 찍은 합성 시각의 차이는 3.5ms입니다. 브라우저에서 요청을 보내고 답을 그리는 시간은 이 두 눈금 밖에 있습니다.')
def span(b, t):
    b.line((35, 112, 602, 112), MUTED, 2)
    (x1, x2) = (145, 465)
    b.line((x1, 83, x1, 128), INK)
    b.line((x2, 83, x2, 128), INK)
    b.text(x1, 59, '12.0ms', 20)
    b.text(x2, 59, '15.5ms', 20)
    b.rect(x1, 101, travel(t, 0, x2 - x1), 15, TEAL, None, 0)
    b.bracket(x1, x2, 150, '서비스 처리 3.5ms')

@scene(111, 2, 'release-evidence', '확장 문항 세 개를 맞히면 바로 출시할 수 있을까요?', '공개 기본 7문항은 전후 모두 통과했습니다. 확장 세 문항 중 통과가 1개에서 3개로 늘었지만 운영 근거가 남아 후보의 출시 결정은 보류입니다.')
def release(b, t):
    b.text(117, 65, '기본 문항', 19)
    b.dots(218, 65, 7, 7, 38)
    b.text(117, 125, '확장 문항', 19)
    for (i, key) in enumerate(['N01', 'N02', 'G01']):
        x = 222 + i * 70
        b.circ(x, 119, 9, TEAL if i == 2 or t > 0.55 else LIGHT, INK)
        b.text(x, 143, key, 15)
    b.stamp(451, 165, '출시 보류', False, 129)
    b.text(164, 179, '공개 개발 기록', 17)

@scene(112, 1, 'mount-bridge', '컨테이너 경로와 자료 볼륨은 어떻게 이어질까요?', '시안은 p1-json을 앱의 runtime-data 위치에 연결합니다. 재배포 뒤 데이터 보존 여부는 같은 볼륨을 연결하고 실제 세션을 다시 읽어 확인합니다.')
def mount(b, t):
    b.rect(40, 39, 291, 135, PAPER, INK)
    b.text(185, 65, '앱 컨테이너', 18)
    b.slot(64, 102, 238, 'runtime-data', SKY)
    b.cylinder(415, 71, 162, 76, 'p1-json')
    x = travel(t, 300, 414)
    b.line((299, 123, x, 123), TEAL, 6)
    b.text(313, 195, '배포 설정 시안', 16, MUTED)

@scene(113, 2, 'replay-window', '복구한 목록만으로 오래된 중복까지 알 수 있을까요?', '가상 복구 기록에는 r2부터 r6까지 남습니다. r6은 기록에서 찾을 수 있지만 이미 밀려난 r0의 처리 여부는 이 다섯 칸만 보고 알 수 없습니다.')
def replay(b, t):
    b.ribbon(105, 89, 461, ['r2', 'r3', 'r4', 'r5', 'r6'])
    b.rect(99, 58, 473, 64, None, BLUE)
    x = travel(t, 521, 57)
    b.lens(x, 90, 26)
    b.text(64, 153, 'r0 · 기록 밖', 16, RED)
    b.text(489, 158, 'r6 · 보관 중', 17, TEAL)
    b.text(315, 192, '보존 범위가 중복 확인 범위도 제한합니다.', 16)

@scene(114, 2, 'handover-checkpoint', '“안 돼요” 대신 어느 지점까지 읽었는지 알려 주면?', '인수자가 직접 확인한 마지막 출력과 아직 실행하지 않은 연결을 구분합니다. Q01에서 RULE-A 2.1절을 읽었다는 기록은 다음 확인 위치를 좁혀 줍니다.')
def checkpoint(b, t):
    b.page(45, 30, 336, 157, '인수자의 노트북 기록', 0)
    b.text(213, 83, 'Q01   장비 A', 20)
    b.text(213, 134, 'RULE-A   § 2.1', 23, TEAL, True)
    b.line((83, 154, travel(t, 84, 338), 154), GOLD, 4)
    b.rect(421, 73, 168, 76, None, MUTED)
    b.text(505, 95, '외부 연결', 18)
    b.text(505, 127, '미확인', 20, MUTED)

@scene(115, 1, 'demo-spotlight', '발표에서 답을 읽은 뒤 어디를 가리킬까요?', '장비 A의 점검 답을 보여 준 뒤 규정 2.1절과 개정일을 짚습니다. 관객은 그 표식으로 답의 근거를 다시 찾을 수 있습니다.')
def spotlight(b, t):
    b.rect(33, 27, 574, 163, INK)
    b.text(320, 68, '점검 전 전원 표시등을 확인합니다.', 23, PAPER, True)
    b.text(316, 131, '규정 A    ·    2.1절    ·    2026-11-01', 21, SKY, True)
    x = travel(t, 198, 458)
    b.line((x - 34, 153, x + 34, 153), YELLOW, 5)

@scene(116, 2, 'claim-radius', '세 질문으로 확인한 기여의 범위는 어디까지일까요?', '두 장비의 붙여쓰기와 모호한 장비AB는 공개 개발 사례입니다. 이 세 입력에서 확인한 수정 효과와 실제 사용자 질문 전체의 품질을 구분해 인계합니다.')
def radius(b, t):
    for (x, y, s) in [(154, 75, 'A'), (244, 74, 'B'), (203, 142, 'AB')]:
        b.chip(x, y, s, YELLOW if s == 'AB' else MINT, 49, 33)
    b.chip(483, 99, '새 사용자 표현', LIGHT, 159)
    b.arc(202, 110, 91, -90, -89 + 358 * ease(t), TEAL, 5)
    b.text(206, 206, '공개 개발 입력 3개', 17, TEAL, True)
    b.text(487, 157, '효과 미평가', 17, MUTED)
