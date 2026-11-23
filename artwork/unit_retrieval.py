"""Retrieval, graph state and evaluation (20–42)."""
from studio import (
    scene, ease, travel, INK, BLUE, TEAL, RED, GOLD, LIGHT, PAPER, MINT, PINK, YELLOW, SKY, MUTED, math
)

@scene(20, 1, 'source-bookmark', '휴관일의 근거는 어느 쪽에 꽂혀 있을까요?', 'library-2는 원문의 2쪽을 가리킵니다. 책갈피를 따라가면 월요일 휴관이라는 문장을 다시 읽을 수 있습니다.')
def bookmark(b, t):
    b.page(69, 38, 235, 144, '1쪽 · 대출', 4)
    b.page(306, 38, 235, 144, '2쪽 · 휴관', 0)
    b.text(424, 123, '월요일 휴관', 24, INK, True)
    y = travel(t, 8, 67)
    b.poly((477, y, 505, y, 505, y + 59, 491, y + 48, 477, y + 59), GOLD)
    b.text(162, 149, '14일', 19, BLUE)

@scene(21, 2, 'source-offset', '잘린 조각으로 원문의 자리를 되찾을 수 있을까요?', '조각에 원문 ID와 위치를 붙이면 짧은 “일입니다.”도 원래 문장의 어느 부분인지 찾을 수 있습니다.')
def offset(b, t):
    b.text(318, 44, 'library-1   도서 대출 기간은 14일입니다.', 23, INK, True)
    full = 'library-1   도서 대출 기간은 14일입니다.'
    from studio import font, SCALE
    end = 318 + font(23, True).getlength(full) / SCALE / 2
    span = font(23, True).getlength('일입니다.') / SCALE
    x = travel(t, 94, end - span)
    b.line((x, 68, x + span, 68), GOLD, 6)
    b.line((x + 31, 73, 341, 126), BLUE)
    b.chip(339, 150, 'library-1:1    일입니다.', MINT, 254)

@scene(22, 3, 'faiss-index', '검색 위치 0은 문서 번호 0일까요?', 'FAISS가 돌려준 위치를 저장 순서에 맞춘 목록에서 읽습니다. 이 예제의 위치 0에 대응하는 문서 ID는 library-1입니다.')
def faiss(b, t):
    b.text(128, 39, '벡터 배열 위치', 18)
    b.text(431, 36, '같은 순서의 문서 목록', 18)
    for i in range(3):
        y = 72 + i * 46
        b.chip(120, y, str(i), YELLOW if i == 0 else LIGHT, 67, 33)
        b.slot(354, y - 18, 163, 'library-' + str(i + 1), MINT if i == 0 else PAPER)
    b.arrow(161, 72, travel(t, 176, 349), 72)

@scene(23, 2, 'query-compass', '질문이 바뀌면 첫 번째 문서는 어떻게 바뀔까요?', '대출 기간이라는 질문은 library-1, 휴관일 질문은 library-2를 첫 근거로 찾습니다. 바뀐 단어를 따라 나침반이 다른 원문을 가리킵니다.')
def compass(b, t):
    b.circ(306, 110, 72, PAPER, INK)
    b.text(98, 107, 'library-1', 22, BLUE, True)
    b.text(534, 107, 'library-2', 22, TEAL, True)
    a = math.pi * (1 + ease(t))
    x = 306 + 61 * math.cos(a)
    y = 110 + 61 * math.sin(a)
    b.arrow(306, 110, x, y)
    b.circ(306, 110, 6, INK)
    b.text(320, 192, '대출 기간은?' if t < 0.5 else '휴관일은?', 22)

@scene(24, 2, 'citation-ring', '검색 울타리 안에 인용 ID가 있을까요?', '휴관일 질문으로 찾은 집합에는 library-2가 있습니다. library-1도 존재하는 문서지만 이번 집합 밖의 인용이라 검사를 통과하지 못합니다.')
def ring(b, t):
    b.circ(219, 111, 89, MINT, TEAL)
    b.text(219, 65, '이번 검색 집합', 18)
    b.chip(217, 115, 'library-2', PAPER, 126)
    b.chip(485, 115, 'library-1', PINK, 126)
    b.lens(travel(t, 222, 481), 114, 47)
    b.text(485, 178, '이번 결과 밖', 18, RED)

@scene(25, 3, 'regression-tracing', '틀린 검색 결과는 어느 원문과 대조할까요?', '휴관 요일 질문에서 잘못 찾은 library-1과 직접 확인한 library-2의 2쪽을 대조합니다. 원문을 찾은 뒤에는 검색기도 같은 문서를 찾는지 따로 확인해야 합니다.')
def tracing(b, t):
    b.text(320, 32, '휴관 요일은 언제인가요?', 22, INK, True)
    b.page(39, 57, 246, 116, '잘못 찾은 기록', 0)
    b.text(162, 127, 'library-1 · 대출', 20)
    b.page(352, 57, 245, 116, '원문에서 직접 대조', 0)
    b.text(474, 127, 'library-2 · 2쪽', 20)
    b.lens(travel(t, 167, 466), 126, 37)
    b.text(320, 194, '휴관일은 library-2의 문장에 있습니다.', 16)

@scene(26, 1, 'state-patch', '한 필드만 돌려주면 나머지 필드는 지워질까요?', '질문의 공백을 정리하는 노드는 question만 갱신합니다. documents의 빈 목록과 answer의 빈 문자열은 원래 칸에 남습니다.')
def patch(b, t):
    for (i, (k, v)) in enumerate([('question', '대출 기간은?'), ('documents', '[]'), ('answer', '""')]):
        y = 25 + i * 57
        b.text(114, y + 20, k, 20, INK, True)
        b.slot(225, y, 300, v, YELLOW if not i else PAPER)
    pad = 28 * (1 - ease(t))
    b.rect(301 - pad, 37, pad, 18, SKY)
    b.rect(445, 37, pad, 18, SKY)
    b.text(325, 193, '파란 공백만 지우고 나머지 필드는 유지합니다.', 17)

@scene(27, 2, 'retry-tokens', '검색을 더 할 수 있는 횟수가 얼마나 남았나요?', '시도할 때마다 표 한 장을 씁니다. 최대 두 번이면 두 장을 모두 쓴 뒤에는 같은 실패가 돌아와도 세 번째 검색을 시작하지 않습니다.')
def tokens(b, t):
    for i in range(2):
        y = travel(t, 92, 148, 0.13 + i * 0.38, 0.36 + i * 0.38)
        x = 178 + i * 240
        b.rect(x - 70, y - 24, 140, 48, YELLOW, INK, 3)
        for j in range(4):
            b.circ(x - 70, y - 15 + j * 10, 3, PAPER)
        b.text(x, y, f'검색 {i + 1}회', 21, INK, True)
    b.line((40, 120, 594, 120), MUTED)
    b.text(315, 28, '사용 가능한 검색표  ' + str(2 - int(t > 0.36) - int(t > 0.74)) + '장', 21)

@scene(28, 2, 'message-id-edit', '같은 ID로 오타를 고치면 말풍선이 늘어날까요?', '질문 한 건이 든 initial에 같은 h1으로 수정한 질문을 넣습니다. 기존 말풍선의 문장이 바뀌고 개수는 한 개로 유지됩니다.')
def identity(b, t):
    b.chip(87, 71, 'h1', SKY, 62)
    b.rect(135, 44, 376, 53, PAPER, INK, 16)
    b.text(323, 71, '질문 원문' if t < 0.52 else '고친 질문', 24)
    b.line((travel(t, 164, 471), 55, travel(t, 164, 471), 85), BLUE, 3)
    b.text(317, 151, '메시지 수   1개', 25, TEAL, True)

@scene(29, 1, 'thread-spools', '같은 그래프에서 이전 질문은 어디에 남을까요?', 'A의 두 발화는 같은 thread_id의 이력에 감깁니다. B를 열어도 A의 발화가 B의 새 이력으로 옮겨가지 않습니다.')
def spools(b, t):
    for (i, k) in enumerate('AB'):
        x = 187 + i * 268
        b.circ(x, 109, 65, PAPER, INK)
        if not i:
            for j in range(2):
                b.arc(x, 109, 47 - j * 12, -90, -89 + 350 * ease(t, 0.08 + j * 0.37, 0.44 + j * 0.37), TEAL, 6)
        b.circ(x, 109, 16, SKY, INK)
        b.text(x, 109, k, 17, INK, True)
        b.text(x, 190, 'thread ' + k, 19)
    b.text(320, 28, '사용자 발화 기록', 19)

@scene(30, 1, 'evidence-luggage', '문장을 건넬 때 출처 꼬리표는 따라갈까요?', '검색 결과에는 문장과 문서 ID·쪽 번호가 함께 들어 있습니다. 답변 노드가 근거 위치를 읽으려면 꼬리표까지 전달해야 합니다.')
def luggage(b, t):
    x = travel(t, 95, 248)
    b.rect(x + 85, 47, 53, 26, None, INK)
    b.rect(x, 65, 236, 85, SKY, INK)
    b.text(x + 118, 107, '도서 대출 기간은 14일', 21, INK, True)
    b.line((x + 226, 81, x + 262, 130), INK)
    b.chip(x + 268, 148, 'library-1 · p.1', YELLOW, 138, 36)

@scene(31, 1, 'empty-or-timeout', '빈 목록과 시간 초과는 어떻게 구별할까요?', '[]는 검색을 마치고 받은 빈 결과입니다. 시간 초과에서는 결과를 받지 못했습니다. 두 경우 모두 근거 문장은 없지만 관찰한 사건이 다릅니다.')
def timeout(b, t):
    b.rect(39, 51, 213, 104, PAPER, INK)
    b.text(145, 102, '[  ]', 42, TEAL, True)
    b.text(146, 184, '완료된 빈 검색', 19)
    b.circ(470, 102, 56, None, INK)
    a = -math.pi / 2 + ease(t) * math.pi * 1.65
    b.line((470, 102, 470 + 40 * math.cos(a), 102 + 40 * math.sin(a)), RED, 5)
    b.text(470, 185, 'TimeoutError', 19, RED, True)

@scene(32, 2, 'aligned-traces', '두 구현은 어느 값에서 처음 달라질까요?', '같은 대출 질문에서 LCEL과 그래프 모두 library-1과 14일을 반환합니다. 입력을 맞추고 위아래의 같은 항목을 짝지어 대조합니다.')
def traces(b, t):
    for (i, s) in enumerate(['LCEL', 'Graph']):
        y = 73 + 67 * i
        b.text(69, y, s, 18, INK, True)
        for (j, v) in enumerate(['대출 기간은?', 'library-1', '14일']):
            b.text(193 + j * 155, y, v, 18)
    x = travel(t, 116, 423)
    b.rect(x, 45, 150, 124, None, BLUE, 8)
    b.text(318, 187, '고정 질문의 저장 출력', 17, MUTED)

@scene(33, 2, 'reply-envelope', 'search-1과 library-1은 각각 무엇을 가리킬까요?', '답장 봉투의 search-1은 도구 호출 ID입니다. 봉투 안에서 꺼낸 library-1은 검색한 문서 ID입니다.')
def envelope(b, t):
    y = travel(t, 105, 36)
    b.page(185, y, 258, 75, '문서  library-1', 1)
    b.rect(151, 107, 323, 86, SKY, INK, 2)
    b.line((151, 107, 314, 155, 474, 107), BLUE)
    b.text(310, 173, '호출  search-1', 20, INK, True)

@scene(34, 1, 'unused-tool', '도구 요청이 없으면 검색기는 움직일까요?', '도구 호출 목록이 비어 있으면 검색 노드를 실행하지 않고 끝냅니다. 도구를 사용할 수 있다는 사실만으로 호출 횟수가 늘지는 않습니다.')
def unused(b, t):
    b.text(152, 44, '도구 호출 목록', 18)
    b.chip(149, 104, '[  ]', SKY, 126, 64)
    b.line((212, 106, 297, 106))
    end = travel(t, 0, -49)
    b.line((298, 106, 363, 106 + end), BLUE, 5)
    b.circ(370, 106, 5, None, INK)
    b.line((377, 106, 450, 106))
    b.circ(502, 106, 49, PAPER, INK)
    b.text(502, 106, '0회', 29, INK, True)
    b.text(499, 181, '검색 실행', 18)

@scene(35, 2, 'sealed-holdout', '설정을 고르는 동안 어느 질문을 덮어 둘까요?', '개발 문항을 보며 설정을 조정하고 확인용 문항은 따로 보관합니다. 확인 문항을 미리 열어 설정을 고르면 마지막 비교의 의미가 달라집니다.')
def holdout(b, t):
    b.page(50, 42, 226, 128, '개발 문항', 4)
    b.page(359, 42, 226, 128, '확인용 문항', 4)
    y = travel(t, -75, 49)
    b.rect(357, y, 230, 123, SKY, INK)
    b.line((358, y + 4, 472, y + 69, 586, y + 4), BLUE)
    b.text(472, y + 90, '평가 때 개봉', 20, BLUE, True)

@scene(36, 1, 'rank-reciprocal', '정답이 두 번째여도 찾은 비율은 1일까요?', '기대 문서가 하나이고 앞 두 건 안에서 찾았습니다. Recall@2는 1이고 첫 정답 순위의 역수는 1/2입니다.')
def reciprocal(b, t):
    b.ribbon(34, 65, 358, ['1위 · 다른 문서', '2위 · 기대 문서'], 1)
    for (i, (l, v)) in enumerate([('Recall@2', 1), ('RR', 0.5)]):
        y = 117 + 44 * i
        b.text(90, y, l, 17)
        b.meter(160, y - 7, 310, ease(t) * v, 1, TEAL if i == 0 else BLUE)
        b.text(532, y, '1' if i == 0 else '1/2', 21, INK, True)

@scene(37, 3, 'topk-aperture', 'k만 늘리면 청크 경계도 바뀔까요?', '같은 순위에서 k를 1에서 2로 늘리면 둘째 조각도 보입니다. 이미 잘라 둔 조각의 내용과 경계는 그대로입니다.')
def aperture(b, t):
    for (i, s) in enumerate(['library-1:0', 'library-1:1']):
        b.page(72 + i * 253, 55, 220, 102, s, 3)
    w = travel(t, 233, 485)
    b.rect(64, 45, w, 126, None, TEAL, 6)
    b.text(309, 191, '검색 범위 k = ' + ('1' if t < 0.5 else '2'), 20, TEAL, True)

@scene(38, 2, 'union-of-hits', '두 표현으로 찾은 첫 후보가 같으면 두 건일까요?', '두 검색이 모두 library-1:0을 찾았습니다. 같은 청크 ID를 합치면 최종 후보는 한 건만 남습니다.')
def union(b, t):
    b.text(320, 33, '표현이 다른 두 검색', 18)
    f = ease(t)
    for (x, fill) in [(140 + 180 * f, SKY), (500 - 180 * f, YELLOW)]:
        b.chip(x, 105, 'library-1:0', fill, 164, 55)
    b.text(320, 175, '고유 후보 1건', 23, TEAL, True)

@scene(39, 2, 'clipped-answer', '24라는 숫자가 남으면 문장 전체도 남았을까요?', '반납함 사례는 24시간이라는 숫자를 찾았지만 문장이 잘렸습니다. 숫자 일치와 근거 문장을 온전히 읽을 수 있는지를 따로 봅니다.')
def clipped(b, t):
    b.page(35, 40, 563, 127, '반납함 · 원문과 검색 조각', 0)
    from studio import font, SCALE
    full = '무인 반납함은 24시간 이용할 수 있습니다.'
    prefix = '무인 반납함은 24시간 이용할'
    start = 318 - font(23, False).getlength(full) / SCALE / 2
    b.text(318, 109, full, 23)
    end = start + font(23, False).getlength(prefix) / SCALE
    x = travel(t, 576, end + 0.5)
    b.rect(x, 87, 579 - x, 46, LIGHT, None, 0)
    b.line((x, 76, x, 143), RED, 2)
    b.text(315, 187, '남은 조각   “무인 반납함은 24시간 이용할”', 18)

@scene(40, 1, 'form-carbon', '입력하다 멈춘 글도 제출한 질문일까요?', '폼의 입력 초안은 제출할 때 복사됩니다. 그전까지 앱이 보관한 마지막 질문은 바뀌지 않습니다.')
def carbon(b, t):
    b.text(160, 35, '입력 중', 20)
    b.rect(31, 64, 257, 76, PAPER, INK)
    b.text(160, 101, '주차 요금은?'[:int(8 * ease(t, 0.08, 0.45))], 24)
    b.text(478, 35, '제출된 질문', 20)
    b.rect(354, 64, 249, 76, MINT, TEAL)
    b.text(477, 100, '주차 요금은?' if t > 0.68 else '—', 24)
    b.line((70, 173, travel(t, 70, 565, 0.48, 0.68), 173), BLUE, 4)
    b.text(321, 194, '제출', 17)

@scene(41, 2, 'new-chat-window', '새 대화를 열면 이전 기록도 지워질까요?', '새 ID의 화면은 비어 있습니다. 기존 ID로 저장된 질문들은 그 대화에 남습니다.')
def newchat(b, t):
    b.page(40, 30, 316, 153, '대화 A', 0)
    b.chip(179, 96, '대출 기간은?', SKY, 174, 31)
    b.chip(213, 140, '주차 요금은?', YELLOW, 174, 31)
    x = travel(t, 519, 334)
    b.page(x, 51, 188, 130, '새 대화 B', 0)
    b.text(x + 94, 125, '[  ]', 31, TEAL, True)

@scene(42, 2, 'stale-page-tab', '검색은 맞았는데 화면 쪽수가 틀리다면?', '휴관일을 찾은 결과는 library-2의 2쪽입니다. 화면의 출처 탭을 현재 결과에 맞추면 이전 질문의 1쪽이 남는 문제를 찾을 수 있습니다.')
def pagetab(b, t):
    b.page(50, 48, 240, 127, '현재 검색 결과', 0)
    b.text(168, 116, 'library-2 · 2쪽', 21)
    b.page(342, 48, 230, 127, '화면 출처', 0)
    b.text(455, 117, '1쪽' if t < 0.5 else '2쪽', 29, INK, True)
    b.rect(515, travel(t, 62, 113), 69, 22, YELLOW, GOLD)
    b.text(315, 194, '휴관일 질문', 17)
