"""Python objects, evidence in language, and model–tool protocols (1–19)."""
from studio import (
    scene, ease, travel, INK, BLUE, TEAL, RED, GOLD, LIGHT, PAPER, MINT, PINK, YELLOW, SKY, MUTED, math
)

@scene(1, 2, 'kernel-imprint', '고친 이름은 언제 커널에 찍힐까요?', '셀에서 이름을 고쳐도 커널의 값은 그대로입니다. 이름 셀을 실행한 뒤에야 다음 인사가 새 이름을 사용합니다.')
def kernel(b, t):
    b.page(40, 30, 210, 132, '이름 셀', 0)
    b.text(145, 103, 'learner = "지민"' if t > 0.22 else 'learner = "학습자"', 19)
    b.cylinder(385, 48, 182, 90, '지민' if t > 0.67 else '학습자')
    x = travel(t, 245, 384, 0.38, 0.66)
    b.arrow(254, 96, x, 96)
    b.text(320, 170, '이름 셀 실행' if t > 0.38 else '편집 중', 20, BLUE)
    b.text(476, 25, '커널 메모리', 17)

@scene(2, 2, 'minute-sieve', '어떤 기록이 70분에 들어갈까요?', '완료했고 30분 이상인 두 기록만 합계에 들어갑니다. Git 연습은 미완료이고 20분이어서 합계에서 빠집니다.')
def sieve(b, t):
    b.text(150, 25, '활동 기록', 18)
    b.text(485, 25, '선택한 시간의 합', 18)
    for (i, (name, n, ok)) in enumerate([('Python 기초', 30, True), ('Git 연습', 20, False), ('리스트 복습', 40, True)]):
        y = 62 + 55 * i
        b.text(85, y, name, 18)
        x = travel(t, 205, 405, 0.14 + i * 0.1, 0.46 + i * 0.13) if ok else 205
        b.chip(x, y, str(n) + '분', MINT if ok else LIGHT, 74)
    b.text(533, 113, str((30 if t > 0.46 else 0) + (40 if t > 0.72 else 0)) + '분', 40, TEAL, True)

@scene(3, 2, 'minute-boundary', '480분과 481분을 가르는 한 칸', '480까지는 정수를 돌려줍니다. 바로 다음 눈금인 481에서는 범위 검사에서 ValueError가 발생합니다.')
def boundary(b, t):
    b.rect(55, 83, 345, 25, MINT)
    b.rect(400, 83, 185, 25, PINK)
    for (i, n) in enumerate(range(477, 484)):
        x = 80 + i * 80
        b.line((x, 77, x, 118))
        b.text(x, 138, n, 19)
    x = travel(t, 320, 400, 0.22, 0.68)
    b.poly((x, 79, x - 10, 59, x + 10, 59), BLUE)
    b.text(x, 38, '480' if t < 0.22 else '481' if t > 0.68 else '입력 변경 중', 24, BLUE, True)
    b.stamp(326, 183, '정수 480' if t < 0.22 else 'ValueError' if t > 0.68 else '검사 전', t < 0.22, 170)

@scene(4, 1, 'independent-switches', '같은 설계도로 만든 두 기록의 스위치', '두 객체는 같은 클래스에서 만들어져도 각자의 done 값을 기억합니다. 한쪽 스위치를 눌러도 옆 기록은 그대로입니다.')
def switches(b, t):
    b.page(20, 52, 135, 103, '클래스', 3)
    for (i, name) in enumerate(['첫 번째 객체', '두 번째 객체']):
        x = 267 + i * 220
        b.text(x, 48, name, 20, INK, True)
        b.rect(x - 62, 81, 124, 44, MINT if i == 0 and t > 0.52 else LIGHT, INK, 22)
        b.circ(x - 39 + (78 * ease(t, 0.28, 0.65) if i == 0 else 0), 103, 17, PAPER, INK)
        b.text(x, 155, 'done = ' + ('True' if i == 0 and t > 0.54 else 'False'), 18)

@scene(5, 2, 'id-overlay', '두 번째 4번 행은 합계에 또 들어갈까요?', '유효한 행의 ID는 1, 2, 4, 4입니다. 같은 ID를 포개면 세 건이 남아 총 90분이 됩니다.')
def dedup(b, t):
    for (i, (n, minutes)) in enumerate([(1, 30), (2, 20), (4, 40), (4, 40)]):
        x = 55 + i * 144
        if i == 3:
            x = travel(t, x, 343)
        b.page(x, 47, 108, 90, 'ID ' + str(n), 0)
        b.text(x + 54, 103, f'{minutes}분', 22, TEAL, True)
    b.bracket(56, travel(t, 595, 453), 160, '세 건 · 합계 90분' if t > 0.84 else '유효한 행 네 개' if t < 0.1 else '같은 ID 대조')

@scene(6, 3, 'string-false', '따옴표 속 false가 왜 참으로 읽힐까요?', '문자열 "false"에는 글자가 다섯 개 있습니다. bool은 비어 있는지를 검사하므로 True이고, JSON의 논리값 false를 읽으면 False입니다.')
def stringfalse(b, t):
    b.ribbon(24, 81, 318, list('false'), min(4, int(t * 6)))
    b.text(180, 32, '문자열 · 글자 다섯 개', 18)
    b.chip(472, 81, 'bool → True', MINT, 165)
    b.line((34, 125, 605, 125), LIGHT)
    b.text(179, 167, 'JSON 논리값  false', 21)
    b.chip(472, 167, 'False', SKY, 165)

@scene(7, 1, 'reset-tank', '초기화를 한 줄 옮기면 왜 합계가 40일까요?', '30, 20, 40을 더할 때마다 누적값을 비우면 마지막 40만 남습니다. 반복문 밖에서 한 번만 비운 쪽에는 90이 남습니다.')
def tank(b, t):
    points = [(0, 0), (0.23, 30), (0.32, 30), (0.36, 0), (0.53, 20), (0.62, 20), (0.66, 0), (0.85, 40), (1, 40)]

    def level(seq):
        for ((a, x), (c, y)) in zip(seq, seq[1:]):
            if t <= c:
                return travel(t, x, y, a, c)
        return seq[-1][1]
    for (i, (s, v)) in enumerate([('반복할 때마다 초기화', level(points)), ('시작할 때 한 번 초기화', level([(0, 0), (0.23, 30), (0.36, 30), (0.53, 50), (0.66, 50), (0.85, 90), (1, 90)]))]):
        x = 80 + i * 300
        b.rect(x, 48, 160, 112, PAPER, INK)
        b.rect(x + 3, 156 - v * 1.12, 154, v * 1.12, SKY if i == 0 else MINT)
        events = [(0, 0), (0.23, 30), (0.36, 0), (0.53, 20), (0.66, 0), (0.85, 40)] if i == 0 else [(0, 0), (0.23, 30), (0.53, 50), (0.85, 90)]
        shown = next((n for (when, n) in reversed(events) if t >= when))
        b.text(x + 80, 112, f'{shown}분', 32, INK, True)
        b.text(x + 80, 186, s, 18)

@scene(8, 1, 'meeting-ink', '회의에서 무엇을 정했고 무엇을 남겨 두었을까요?', '“아직 합의하지 않았다”는 비용이 확정됐다는 근거가 될 수 없습니다. 결정한 항목과 검토 중인 항목의 서술어를 따로 읽습니다.')
def minutes(b, t):
    b.page(36, 20, 565, 178, '가상 독서 모임 · 회의록', 0)
    b.text(315, 84, '다음 모임은 11월 21일 토요일 14시, 온라인으로 진행한다.', 19)
    b.line((92, 101, travel(t, 92, 544, 0.05, 0.46), 101), TEAL, 4)
    b.text(315, 146, '예산과 참가비는 아직 합의하지 않았다.', 21)
    b.line((293, 162, travel(t, 293, 486, 0.47, 0.87), 162), GOLD, 4)

@scene(9, 2, 'price-label', '무료라는 가격표는 어디까지 붙일 수 있을까요?', '원문의 무료는 설명회 참가비에 붙습니다. 교육과정 수강료 칸에는 발표 전까지 금액을 쓸 근거가 없습니다.')
def price(b, t):
    for (x, s) in [(155, '설명회 참가비'), (470, '교육과정 수강료')]:
        b.line((x, 35, x, 65), MUTED)
        b.poly((x - 90, 74, x - 65, 53, x + 90, 53, x + 90, 153, x - 90, 153), YELLOW if x < 200 else LIGHT)
        b.text(x, 87, s, 20)
    b.text(travel(t, 302, 155), 125, '무료', 30, TEAL, True)
    b.text(470, 125, '미발표', 23, MUTED, True)

@scene(10, 1, 'seats-and-people', '성인 20명과 30석을 같은 숫자로 읽어도 될까요?', '의자는 시설 자료의 좌석 수이고 점은 행사 안내에서 정한 모집 인원입니다. 같은 방을 가리켜도 두 숫자의 단위와 출처가 다릅니다.')
def seats(b, t):
    for i in range(30):
        x = 42 + i % 10 * 39
        y = 52 + i // 10 * 54
        b.rect(x, y, 27, 28, PAPER, INK)
        b.line((x + 3, y + 25, x + 3, y + 33), INK)
        if i < round(20 * ease(t)):
            b.circ(x + 13, y + 12, 8, TEAL)
    b.text(514, 77, '시설 30석', 23, INK, True)
    b.text(514, 130, '모집 대상 20명', 23, TEAL, True)

@scene(11, 2, 'offline-response', '응답 문자열만 보면 실제 모델 호출을 알 수 있을까요?', '수업용 고정 응답도 SDK가 읽을 수 있는 모양으로 돌아옵니다. 같은 문장이 보여도 이 예제에서 응답을 제공한 곳은 모의 전송기입니다.')
def mock(b, t):
    b.rect(35, 40, 348, 124, INK)
    b.text(210, 68, 'SDK · 모의 전송기', 20, SKY, True)
    b.text(210, 115, '가상 안내를 확인했습니다.'[:int(18 * ease(t))], 22, PAPER)
    b.circ(511, 95, 49, None, MUTED)
    b.line((472, 125, 550, 64), RED, 4)
    b.text(511, 172, '외부 요청 0회', 20)

@scene(12, 3, 'schema-stencil', '형식 검사를 통과한 제목도 틀릴 수 있을까요?', '“요리 모임”도 문자열이라 형식 검사를 통과합니다. 공지에 적힌 “독서 모임”과 나란히 읽어야 내용 오류가 드러납니다.')
def stencil(b, t):
    b.page(36, 35, 215, 133, '원문 공지', 0)
    b.text(144, 106, '독서 모임', 29, INK, True)
    b.text(451, 41, 'title · 문자열', 18)
    b.rect(325, 72, 244, 70, SKY, BLUE)
    b.text(445, 106, '요리 모임', 29, INK, True)
    b.lens(travel(t, 495, 398), 106, 32)
    b.text(325, 187, '형식 통과   ·   제목 불일치', 20, RED, True)

@scene(13, 1, 'summary-strip', '다음 호출에 들어가는 문장은 어디서 왔을까요?', '첫 호출이 만든 영수증 문의 요약을 다음 호출의 입력에 끼웁니다. 요약이 비어 있으면 분류할 문장도 없습니다.')
def strip(b, t):
    b.rect(35, 42, 553, 119, PAPER, INK)
    b.text(115, 65, '분류 입력', 18, BLUE, True)
    b.rect(77, 87, 463, 42, LIGHT)
    x = travel(t, 198, 309)
    b.chip(x, 108, '사용자가 결제 영수증 확인 방법을 문의했다.', YELLOW, 381)
    b.text(445, 185, '분류값   billing', 18, TEAL, True)

@scene(14, 2, 'route-rail', '분류가 불분명하면 어떤 호출이 남을까요?', 'technical은 기술 문의 단계로 갑니다. 분류 오류 사례에서는 후속 호출 수가 0이므로 임의의 담당자에게 보내지 않습니다.')
def rail(b, t):
    b.line((44, 105, 245, 105, 344, 53, 572, 53), BLUE, 5)
    b.line((244, 106, 344, 157, 572, 157), LIGHT, 5)
    b.text(492, 24, '기술 문의 · 1회', 17)
    b.text(495, 190, '분류 오류 · 후속 호출 0회', 17)
    q = ease(t)
    x = 60 + 420 * q
    y = 105 - 52 * ease(q, 0.44, 0.7)
    b.circ(x, y, 13, TEAL, INK)
    b.line((302, 123, 302, 157), RED, 5)
    b.circ(travel(t, 62, 290, 0.1, 0.53), travel(t, 115, 139, 0.35, 0.53), 8, RED)
    b.text(151, 181, '오류 입력', 16, RED)

@scene(15, 1, 'enum-wheel', '도구가 받을 수 있는 요일은 어느 쪽일까요?', 'day의 허용값은 weekday와 weekend입니다. 주말 조회에는 weekend가 들어가며, 명세에 없는 Friday는 허용값 밖입니다.')
def wheel(b, t):
    b.circ(178, 111, 70, PAPER, INK)
    ang = math.pi * travel(t, 1.2, 1.8)
    u = 178 + 52 * math.cos(ang)
    v = 111 + 52 * math.sin(ang)
    b.line((178, 111, u, v), BLUE, 5)
    b.circ(178, 111, 8, BLUE)
    b.text(80, 34, 'weekday', 18)
    b.text(273, 34, 'weekend', 18)
    b.chip(476, 91, 'day = ' + ('weekday' if t < 0.5 else 'weekend'), MINT, 206)
    b.text(474, 146, 'Friday · 허용값 밖', 18, RED)

@scene(16, 2, 'matching-stubs', '도구 결과는 어느 요청의 영수증일까요?', '요청과 결과에 같은 call_id가 남습니다. 주말 시간 10:00~16:00을 읽을 때도 이 표식으로 원래 요청을 찾습니다.')
def stubs(b, t):
    b.rect(35, 50, 252, 112, SKY, INK)
    x = travel(t, 358, 288)
    b.rect(x, 50, 248, 112, MINT, INK)
    b.text(158, 79, '요청  weekend', 21)
    b.text(158, 132, 'call_1', 25, BLUE, True)
    b.text(x + 122, 79, '10:00~16:00', 23)
    b.text(x + 122, 132, 'call_1', 25, BLUE, True)
    for y in range(64, 157, 18):
        b.circ(287, y, 3, PAPER)

@scene(17, 2, 'call-abacus', '도구 두 번을 썼는데 모델은 왜 세 번 불렀을까요?', '첫 두 판단은 조회를 요청하고 마지막 판단은 두 결과로 답합니다. 각 기록의 역할을 따로 세면 모델 3회와 도구 2회가 됩니다.')
def abacus(b, t):
    for (row, (s, n, positions)) in enumerate([('모델', 3, [0.08, 0.44, 0.78]), ('도구', 2, [0.23, 0.61])]):
        y = 67 + row * 81
        b.text(70, y, s, 22)
        b.line((123, y, 574, y), MUTED, 4)
        for (i, start) in enumerate(positions):
            x = travel(t, 535 - 37 * i, 151 + 39 * i, start, start + 0.13)
            b.circ(x, y, 17, SKY if row == 0 else MINT, INK)
        b.text(603, y, sum((t > p + 0.1 for p in positions)), 24, INK, True)

@scene(18, 1, 'empty-argument-socket', '빈 객체와 빈 호출 ID는 같은 빈칸일까요?', '인자가 없는 get_loan_rule은 {}를 받습니다. call_id까지 비면 반환 결과를 요청과 연결할 수 없습니다.')
def socket(b, t):
    b.text(173, 43, 'arguments · JSON 문자열', 19)
    b.chip(97, 107, '"{}"', SKY, 83)
    b.arrow(147, 107, travel(t, 150, 219), 107)
    b.chip(274, 107, '{}', MINT, 76)
    b.text(206, 160, '파싱한 빈 객체', 17)
    b.text(483, 43, 'call_id', 21)
    b.rect(387, 77, 190, 66, PAPER, RED)
    b.text(483, 110, '""', 31, RED, True)
    b.text(483, 170, '빈 ID 거부', 18, RED)

@scene(19, 3, 'stream-typesetter', '조각으로 받은 답은 어디에서 한 문장이 될까요?', '먼저 도착한 글자는 자리에 남고 다음 조각이 뒤에 붙습니다. 마지막에 이어 읽은 문자열과 조각 한 개를 구별해 보세요.')
def typeset(b, t):
    sentence = '가상 도서관의 대출 기간은 14일입니다.'
    n = min(len(sentence), max(0, int((t - .08) * len(sentence) / .80)))
    b.rect(35, 54, 570, 99, PAPER, INK)
    b.text(114, 76, '누적 문자열', 16, BLUE)
    b.text(320, 114, sentence[:n], 26, INK, True)
    for i in range(len(sentence)):
        b.rect(40 + i * 25, 172, 18, 7, TEAL if i < n else LIGHT)
