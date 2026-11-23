"""Evidence, regression and agent memory (43–65)."""
from studio import (
    scene, ease, travel, INK, BLUE, TEAL, RED, GOLD, LIGHT, PAPER, MINT, PINK, YELLOW, SKY, MUTED, math
)

@scene(43, 1, 'answer-territory', '운영 안내로 내 점수까지 알 수 있을까요?', '과제 제출 위치는 안내 문서 안에 있습니다. 개인 점수는 이 자료에 없어 숫자를 만들어 답할 수 없습니다.')
def territory(b, t):
    b.circ(220, 112, 87, MINT, TEAL)
    b.text(215, 61, '운영 안내', 18)
    b.chip(213, 123, '과제함 위치', PAPER, 125)
    b.chip(travel(t, 357, 475), 110, '내 점수는?', PINK, 129)
    b.text(482, 166, '문서 범위 밖', 20, RED)

@scene(44, 2, 'calendar-reach', '평일 오전 9시를 토요일에도 옮겨 적을 수 있을까요?', '문단 p1은 평일 시작 시각만 정합니다. 토·일 칸에는 시각이 없어 Q04의 답은 문서에서 확인할 수 없습니다.')
def calendar(b, t):
    for (i, s) in enumerate('월화수목금토일'):
        x = 31 + i * 83
        b.rect(x, 46, 77, 110, MINT if i < 5 else PAPER, INK, 2)
        b.text(x + 38, 67, s, 20, INK, True)
        b.text(x + 38, 117, '9시' if i < 5 else '?', 23, TEAL if i < 5 else RED)
    b.line((35, 174, travel(t, 38, 439), 174), TEAL, 5)
    b.text(239, 194, 'p1이 알려 주는 범위', 16)

@scene(45, 2, 'missed-shelf', '빈 검색 목록 뒤에도 원문은 남아 있을까요?', 'Q03의 업로드 실패 안내는 p3에 있습니다. 검색 목록이 비었다는 사실만으로 문서에도 답이 없다고 결론 내릴 수 없습니다.')
def shelf(b, t):
    for (i, s) in enumerate(['p1', 'p2', 'p3']):
        x = 45 + i * 64
        b.rect(x, 45, 54, 105, [SKY, YELLOW, MINT][i], INK)
        b.text(x + 27, 105, s, 20)
    b.line((27, 153, 257, 153), INK, 5)
    b.lens(travel(t, 77, 201), 88, 27)
    b.text(458, 65, 'Q03의 검색 목록', 19)
    b.chip(460, 124, '[  ]', PAPER, 154, 55)
    b.text(151, 184, '사람이 대조한 p3 · 업로드 실패', 16)

@scene(46, 2, 'wrong-citation-pin', 'p3을 찾았는데 왜 답을 보류할까요?', '검색으로 가져온 문단은 p3입니다. 고정 생성기가 인용한 p2를 그 위에 맞춰 봐도 문단 번호가 일치하지 않습니다.')
def pin(b, t):
    b.page(63, 41, 288, 130, '검색으로 읽은 문단', 0)
    b.text(206, 112, 'p3 · 오류 안내', 24, INK, True)
    x = travel(t, 488, 365)
    b.line((x, 57, x - 24, 116), RED, 3)
    b.circ(x, 55, 12, RED)
    b.chip(x + 54, 132, '인용 p2', PINK, 112)
    b.text(311, 190, 'invalid_citation', 18, RED)

@scene(47, 2, 'search-fuse', '같은 검색을 반복하면 어디서 끊길까요?', '반복 정책에서 검색을 두 번 하고 남은 탐색 횟수가 0이 되면 step_limit으로 끝납니다. 같은 요청이 돌아와도 횟수는 다시 채워지지 않습니다.')
def fuse(b, t):
    b.circ(188, 107, 65, None, INK)
    b.arc(188, 107, 54, -90, -89 + min(1, t * 1.1) * 350, BLUE, 8)
    b.text(188, 107, str(2 - int(t > 0.35) - int(t > 0.75)), 36, INK, True)
    b.text(188, 191, '남은 횟수', 17)
    b.line((290, 104, 435, 104), GOLD, 5)
    b.line((435, 104, 476, 104 - 46 * ease(t, 0.69, 0.81)), RED, 5)
    b.text(471, 151, 'step_limit' if t > 0.75 else '검색 중', 20)

@scene(48, 1, 'page-and-paragraph', '문단 p2가 원문 1쪽에 있을 수 있을까요?', 'course-guide-v1:p2의 p2는 문단 식별자입니다. 수업용 페이지판을 펴면 그 문단이 적힌 실제 위치는 1쪽입니다.')
def ppage(b, t):
    b.page(109, 23, 403, 165, '가상 과정 운영 안내', 0)
    b.text(309, 76, 'p1    수업 일정', 17)
    b.rect(165, 96, 292, 35, YELLOW)
    b.text(306, 113, 'p2    과제는 과제함에 제출', 19, INK, True)
    b.text(308, 164, '—   1쪽   —', 18)
    b.lens(travel(t, 192, 308), travel(t, 116, 162), 22)

@scene(49, 2, 'instrument-blanks', '호출 수 0과 비용 미측정은 같은 눈금일까요?', '로컬 규칙에서 외부 모델 호출은 0회입니다. 모델 비용과 지연은 재지 않았으므로 계기판에 0을 채우지 않습니다.')
def instruments(b, t):
    for (i, (s, v)) in enumerate([('외부 호출', '0회'), ('모델 비용', '미측정'), ('모델 지연', '미측정')]):
        x = 109 + i * 211
        b.arc(x, 117, 67, 185, 355, TEAL if not i else MUTED, 5)
        if not i:
            a = math.radians(travel(t, 217, 185))
            b.line((x, 117, x + 51 * math.cos(a), 117 + 51 * math.sin(a)), BLUE, 3)
        b.text(x, 144, v, 22, INK, True)
        b.text(x, 178, s, 17)

@scene(50, 2, 'regression-stitches', '한 곳을 고친 뒤 어느 문항을 다시 당겨 볼까요?', 'Q03이 p3을 인용하도록 수정한 뒤 기존 Q01의 p2도 검사합니다. 새 사례의 성공만으로 기존 답이 보존됐는지는 알 수 없습니다.')
def stitch(b, t):
    for (i, (q, v)) in enumerate([('Q03', 'p3'), ('Q01', 'p2')]):
        y = 67 + i * 84
        b.chip(106, y, q, SKY, 93)
        b.chip(516, y, v, MINT, 90)
        end = travel(t, 159, 462, 0.06 + i * 0.41, 0.43 + i * 0.43)
        for x in range(158, round(end), 18):
            b.line((x, y, min(x + 11, end), y), TEAL, 4)
        if end > 450:
            b.check(586, y)
    b.text(314, 110, '같은 질문으로 재확인', 17)

@scene(51, 2, 'nested-environments', '새 폴더에서 성공하면 새 컴퓨터에서도 검증됐을까요?', '재현한 것은 같은 컴퓨터의 새 경로입니다. 새 설치, 다른 운영체제, 동료의 재현은 각각 별도 확인이 필요합니다.')
def environments(b, t):
    b.rect(34, 30, 349, 150, PAPER, INK)
    b.text(206, 52, '같은 컴퓨터', 20)
    for (i, s) in enumerate(['원래 폴더', '새 폴더']):
        b.slot(59 + i * 151, 89, 126, s, SKY if i == 0 else MINT)
    b.chip(travel(t, 117, 268), 147, '회귀표', YELLOW, 79, 29)
    b.rect(420, 47, 180, 111, None, MUTED)
    b.text(510, 80, '다른 운영체제', 18)
    b.text(510, 120, '미실행', 23, MUTED, True)

@scene(52, 1, 'failure-crosssection', '세 기록에서 오류 위치는 어떻게 달라졌을까요?', '동일한 Q03에서도 빈 검색, 잘못된 인용, 근거가 맞는 답의 기록이 남았습니다. 발표에서 어떤 수정을 말할지 실제 기록과 맞춰 보세요.')
def crosssection(b, t):
    stage = min(2, int(t * 3))
    retrieved = ['[  ]', 'p3', 'p3'][stage]
    cited = ['없음', 'p2', 'p3'][stage]
    b.text(320, 30, '같은 질문 Q03 · 저장된 세 버전', 19)
    b.chip(168, 97, '검색   ' + retrieved, SKY, 192, 55)
    b.chip(477, 97, '인용   ' + cited, MINT if stage == 2 else PINK, 192, 55)
    b.stamp(318, 168, ['no_evidence', 'invalid_citation', 'answered'][stage], stage == 2, 221)

@scene(53, 2, 'join-threads', '이름 옆의 질문 수는 어떻게 생길까요?', '질문 행의 owner를 같은 사용자의 행에 연결합니다. 연결된 줄을 이름별로 세면 학습자 A는 2건, 학습자 B는 1건입니다.')
def join(b, t):
    for (i, name) in enumerate(['학습자 A', '학습자 B']):
        b.chip(126, 70 + i * 82, name, SKY, 142)
    for (i, j) in enumerate([0, 0, 1]):
        y = 46 + i * 57
        b.chip(486, y, '질문 행 ' + str(i + 1), PAPER, 133, 33)
        f = ease(t, 0.05 + i * 0.15, 0.48 + i * 0.15)
        b.line((206, 70 + j * 82, 206 + 208 * f, 70 + j * 82 + (y - 70 - j * 82) * f), [TEAL, TEAL, BLUE][i], 3)

@scene(54, 2, 'carbon-rollback', '취소할 수 있는 수정은 어느 종이에 적혀 있을까요?', '확정된 제목은 초안입니다. 같은 연결에서 수정한 제목을 읽어도 commit 전이라면 rollback이 임시 수정을 걷어내 원래 제목이 다시 보입니다.')
def rollback(b, t):
    b.page(139, 40, 339, 137, '확정한 행', 0)
    b.text(307, 115, '초안', 29, INK, True)
    x = travel(t, 146, 650, 0.38, 0.8)
    b.rect(x, 76, 322, 76, YELLOW, GOLD, 2)
    b.text(x + 161, 115, '수정한 초안', 27, INK, True)
    b.text(316, 195, 'rollback · 임시 수정 취소', 17, BLUE)

@scene(55, 2, 'unpaired-return', '결과 하나가 도착했는데 어떤 호출이 남았을까요?', 'c1에 주말 운영 시간이 도착해도 c2의 대출 기간은 아직 비어 있습니다. 반환된 ID를 맞춘 뒤에야 어느 요청이 끝났는지 알 수 있습니다.')
def unpaired(b, t):
    for (i, s) in enumerate(['c1 · 운영 시간', 'c2 · 대출 기간']):
        x = 75 + i * 283
        b.rect(x, 55, 205, 115, PAPER, INK)
        b.text(x + 102, 81, s, 19)
        b.line((x + 12, 106, x + 190, 106), LIGHT)
    b.chip(176, travel(t, 29, 136), '10:00~16:00', MINT, 161, 32)
    b.text(461, 137, '아직 반환 전', 19, MUTED)

@scene(56, 1, 'positive-k', '검색 개수 k의 첫 허용 눈금은 어디일까요?', '이 도구는 양의 정수 k를 받습니다. 0에서는 입력 오류가 나고 1은 이 조건을 만족합니다. 출처와 호출 한도는 별도로 검사합니다.')
def positive(b, t):
    b.line((55, 115, 584, 115), INK, 3)
    for (i, k) in enumerate([-2, -1, 0, 1, 2, 3]):
        x = 80 + i * 94
        b.circ(x, 115, 6, RED if k <= 0 else TEAL)
        b.text(x, 144, k, 20)
    x = travel(t, 268, 362)
    b.poly((x - 10, 83, x + 10, 83, x, 105), BLUE)
    b.text(x, 53, 'k', 25, BLUE, True)
    b.bracket(362, 550, 174, '허용되는 정수')

@scene(57, 1, 'skill-bookcase', '이름이 비슷한 지침 중 어떤 본문을 펼칠까요?', '근거를 찾아 답하는 작업에서는 원문 대조 지침을 엽니다. 비교 보고서 지침은 두 실행 기록을 대조하는 다른 작업에 쓰입니다.')
def bookcase(b, t):
    for (i, (s, fill)) in enumerate([('근거 답변', MINT), ('비교 보고', SKY)]):
        x = 90 + i * 229
        y = travel(t, 54, 26) if i == 0 else 54
        b.rect(x, y, 176, 117, fill, INK)
        b.line((x + 19, y, x + 19, y + 117), INK)
        b.text(x + 97, y + 55, s, 22, INK, True)
    b.line((50, 177, 566, 177), INK, 5)
    b.text(316, 197, '질문   “근거를 찾아 답해 주세요.”', 16)

@scene(58, 1, 'foldout-reference', '참고자료는 언제 펼쳐 읽을까요?', '선택한 SKILL.md가 원문 대조를 요구할 때 references/source-check.md를 엽니다. 읽은 파일의 크기는 각각 2,511바이트와 1,049바이트입니다.')
def foldout(b, t):
    b.page(66, 50, 222, 118, 'SKILL.md', 2)
    w = travel(t, 10, 255)
    b.rect(291, 57, w, 105, MINT, TEAL, 3)
    if w > 153:
        b.text(290 + w / 2, 93, 'source-check.md', 20, INK, True, w - 10)
        b.text(290 + w / 2, 132, '1,049 B', 19)
    b.text(175, 145, '2,511 B', 17)

@scene(59, 2, 'summary-hole', '대화를 요약하면 기한도 자동으로 남을까요?', '원문에는 금요일 18시라는 제출 기한이 있습니다. 요약에서 그 사실을 빼면 요약만 읽는 다음 호출은 기한을 확인할 수 없습니다.')
def hole(b, t):
    b.ribbon(34, 64, 573, ['회의실 B', '한국어', '금요일 18시'], 1)
    b.chip(132, 150, '회의실 B', SKY, 130)
    b.chip(504, 150, '한국어', MINT, 140)
    y = travel(t, 145, 197)
    b.text(317, y, '금요일 18시', 18, MUTED)
    b.line((231, 147, 400, 147), RED, 3)
    b.text(77, 187, '요약', 16)

@scene(60, 1, 'double-key', '서랍 이름이 language로 같아도 값은 누구 것일까요?', '사용자 이름까지 맞아야 같은 기억입니다. alice의 language에는 한국어가 있고, 이 예제에서 bob의 같은 키는 None입니다.')
def doublekey(b, t):
    for (i, s) in enumerate(['alice', 'bob']):
        x = 58 + i * 302
        b.rect(x, 49, 221, 120, SKY if not i else LIGHT, INK)
        b.text(x + 110, 72, s, 20, INK, True)
        y = travel(t, 92, 112) if not i else 92
        b.slot(x + 18, y, 185, '한국어' if not i and t > 0.45 else 'language', PAPER)
    b.text(474, 188, '조회 결과  None', 18)

@scene(61, 1, 'registered-tool', '파이썬 함수는 언제 도구 목록에 나타날까요?', '시간표 함수를 서버에 등록하면 클라이언트가 get_library_hours라는 이름을 조회할 수 있습니다. 목록에 이름이 보이는 것과 주말 시간을 실제 조회하는 것은 다른 관찰입니다.')
def registry(b, t):
    b.page(34, 37, 255, 143, '서버의 시간표 함수', 0)
    b.text(161, 118, 'get_library_hours', 19)
    if t > 0.48:
        b.chip(159, 83, '@server.tool()', YELLOW, 173, 29)
    b.page(345, 37, 253, 143, '클라이언트가 본 목록', 0)
    b.text(469, 114, '[get_library_hours]' if t > 0.48 else '[  ]', 18, TEAL, True)
    b.text(319, 192, '함수 정의와 도구 등록', 17)

@scene(62, 2, 'weekday-dial', '형식이 맞는 시간표도 틀린 답일 수 있을까요?', '평일 요청에 주말 시각을 반환해도 필드 자체는 있을 수 있습니다. 요청한 요일과 맞춰 읽으면 평일에는 09:00~18:00이 대응합니다.')
def dial(b, t):
    for (i, (s, v)) in enumerate([('weekday', '09:00~18:00'), ('weekend', '10:00~16:00')]):
        y = 74 + i * 73
        b.text(128, y, s, 20)
        b.chip(457, y, v, MINT if not i else SKY, 173)
    b.line((202, 74, 352, travel(t, 147, 74)), BLUE, 4)
    b.circ(201, 74, 6, BLUE)
    b.text(312, 191, '평일 요청', 17)

@scene(63, 2, 'generation-stop', '검색 근거가 비면 생성 호출도 줄어들까요?', '근거가 한 건도 없는 경로는 답변 생성 전에 멈춥니다. 계산한 호출 수는 0이며, 근거 없이 만든 문장을 화면에 붙이지 않습니다.')
def stop(b, t):
    b.chip(99, 106, '근거 0건', LIGHT, 122)
    b.line((169, 106, 471, 106), MUTED)
    x = travel(t, 176, 344)
    b.circ(x, 106, 10, BLUE)
    b.rect(357, 66, 9, 82, RED)
    b.text(502, 70, '생성 호출', 19)
    b.text(506, 133, '0', 39, TEAL, True)

@scene(64, 2, 'approval-latch', '문의 내용이 보이는 순간 등록도 끝났을까요?', '승인 대기 중 등록 건수는 0입니다. 같은 실행을 승인해 재개한 뒤에만 등록 건수가 1로 바뀝니다.')
def latch(b, t):
    b.rect(70, 61, 283, 96, PAPER, INK)
    b.text(211, 107, '과제 등록 오류 문의', 22)
    y = travel(t, 87, 43, 0.31, 0.6)
    b.rect(332, y, 23, 66, GOLD, INK)
    b.text(486, 74, '등록 건수', 18)
    b.text(484, 127, '1' if t > 0.65 else '0', 42, TEAL, True)
    b.text(317, 187, '승인 후 재개' if t > 0.6 else '승인 대기', 19)

@scene(65, 2, 'tool-apertures', '기술 문의에 열리는 도구 칸은 어디일까요?', '기술 문의로 분류한 예제는 technical_faq를 사용합니다. 분류값이 정해졌다고 모든 도구가 허용되는 것은 아닙니다.')
def apertures(b, t):
    b.text(318, 32, '분류  technical', 23, INK, True)
    b.chip(163, 111, '결제 문의 도구', LIGHT, 217, 65)
    b.chip(475, 111, 'technical_faq', MINT, 217, 65)
    h = travel(t, 61, 0)
    b.rect(369, 80, 212, h, BLUE)
    b.line((66, 88, 252, 132), MUTED, 4)
    b.text(472, 174, '기술 문의 도구 허용', 18, TEAL)
