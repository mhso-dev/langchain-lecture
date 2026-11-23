"""Additional close-ups where the chapter teaches a second, independent concept."""
from studio import (
    scene, ease, travel, INK, BLUE, TEAL, RED, LIGHT, PAPER, MINT, PINK, YELLOW, SKY, MUTED, math
)

@scene(6, 2, 'http-envelope', '200 응답 안에 JSON이 없을 수도 있을까요?', '상태 코드는 봉투 겉면의 정보입니다. HTTP 응답을 받은 뒤에도 본문을 JSON으로 읽을 수 없으면 별도의 파싱 오류가 납니다.')
def http(b, t):
    b.rect(95, 57, 288, 126, SKY, INK)
    b.line((95, 58, 237, 125, 383, 58), BLUE)
    y = travel(t, 98, 29)
    b.page(144, y, 189, 68, '<html>점검 중</html>', 1)
    b.chip(238, 151, 'HTTP 200', MINT, 127, 34)
    b.text(494, 105, 'JSONDecodeError' if t > 0.64 else '본문 확인 전', 17, RED)

@scene(21, 1, 'overlap-scissors', '가위가 네 글자 되돌아가면 어느 부분이 두 번 남을까요?', '첫 청크는 처음 16글자입니다. 다음 시작점을 16에서 12로 되돌리면 “일입니다” 네 글자가 두 청크에 모두 남습니다.')
def scissors(b, t):
    chars = '도서 대출 기간은 14일입니다.'
    dx = 31
    x0 = 65
    overlap = round(4 * ease(t))
    for (i, c) in enumerate(chars):
        x = x0 + i * dx
        b.rect(x - 13, 69, 26, 31, YELLOW if 16 - overlap <= i < 16 else PAPER, INK, 3)
        b.text(x, 85, c, 18)
        if i >= 12:
            b.text(x, 55, i, 13, MUTED)
    x = x0 + (16 - overlap - 0.5) * dx
    b.line((x, 62, x, 109), RED, 3)
    b.circ(x - 6, 119, 5, None, RED)
    b.circ(x + 6, 119, 5, None, RED)
    b.line((x - 5, 116, x + 5, 105), RED)
    b.text(320, 151, '다음 시작 위치  ' + str(16 - round(4 * ease(t))), 18, BLUE, True)
    b.text(320, 185, '겹치는 글자   ' + (' · '.join(chars[16 - overlap:16]) or '없음'), 19)

@scene(22, 1, 'squared-tiles', '대출과 휴관 사이의 제곱거리 2는 어디서 나올까요?', '세 축은 대출·휴관·반납입니다. [1,0,0]과 [0,1,0]은 두 축에서 1씩 달라서 차이의 제곱을 더하면 2가 됩니다.')
def squares(b, t):
    for (i, (word, a, v)) in enumerate([('대출', 1, 0), ('휴관', 0, 1), ('반납', 0, 0)]):
        x = 122 + i * 197
        b.text(x, 27, word, 17)
        b.chip(x, 69, f'{a} - {v}', SKY, 103, 39)
        side = 40 * ease(t) if a != v else 0
        b.rect(x - side / 2, 139 - side, side, side, MINT, TEAL, 0)
        b.text(x, 157, ['1²', '(-1)²', '0²'][i], 16)
    b.text(320, 193, '1 + 1 + 0 = 2', 22, INK, True)

@scene(36, 2, 'number-under-citation', '근거 ID가 맞으면 999일이라는 답도 통과할까요?', '[library-1]이 들어 있는지는 참입니다. 하지만 원문은 14일이라고 하므로 답의 999일은 틀렸습니다.')
def wrongnumber(b, t):
    b.page(42, 31, 556, 151, 'library-1   ·   대출 규정', 0)
    b.text(192, 104, '원문  14일', 25, TEAL, True)
    b.text(458, 104, '답  999일', 25, RED, True)
    b.lens(travel(t, 209, 474), 105, 33)
    b.text(312, 157, '같은 ID 아래 서로 다른 숫자', 17)

@scene(38, 1, 'candidate-race', '마침표와 대출 문장 중 어느 조각이 1위일까요?', '첫 후보는 마침표 한 글자입니다. 같은 두 후보의 순위를 다시 매기면 대출 기간을 담은 문장이 위로 오릅니다. 새 문서를 추가한 것은 아닙니다.')
def race(b, t):
    f = ease(t)
    for i in range(2):
        b.text(55, 72 + i * 74, str(i + 1) + '위', 18, MUTED)
    # Opposite arcs keep both candidate identities readable while their ranks cross.
    x = 288 - 120 * math.sin(math.pi * f)
    y = 72 + 74 * f
    b.chip(x, y, '“.”   ·   :1', YELLOW, 131)
    x = 330 + 110 * math.sin(math.pi * f)
    y = 146 - 74 * f
    b.chip(x, y, '도서 대출 기간은 14일입니다   ·   :0', MINT, 306)
    b.text(321, 193, '후보 목록 안에서 순위만 이동', 17)

@scene(59, 1, 'memory-aperture', '최근 두 턴만 남기면 회의실 B를 찾을 수 있을까요?', '네 턴을 전부 볼 때는 장소가 있습니다. 최근 두 턴에는 기한과 슬라이드 수만 남으므로 그 두 턴에서 회의실 B를 다시 찾을 수 없습니다.')
def aperture(b, t):
    labels = ['회의실 B', '한국어', '금요일 18시', '슬라이드 5장']
    for (i, s) in enumerate(labels):
        b.chip(85 + i * 156, 96, s, [SKY, YELLOW, MINT, PAPER][i], 140)
    w = travel(t, 0, 313)
    b.rect(0, 67, w, 60, LIGHT, None, 0)
    b.line((w, 63, w, 131), BLUE, 3)
    b.text(320, 162, '회색 부분은 현재 창에서 볼 수 없는 과거 턴', 17)
    b.text(320, 190, '최근 두 턴 · 금요일 18시, 슬라이드 5장' if t > 0.83 else '대화 이력 네 턴', 16, TEAL)

@scene(72, 1, 'localhost-mirrors', '두 컨테이너에서 localhost는 같은 곳일까요?', '각 컨테이너의 localhost는 자기 자신을 가리킵니다. 같은 Compose 네트워크에서 API가 DB를 찾을 때 쓰는 주소는 db:5432입니다.')
def mirrors(b, t):
    for (i, key) in enumerate(['API', 'DB']):
        x = 58 + i * 309
        b.rect(x, 46, 220, 117, SKY if not i else MINT, INK)
        b.text(x + 108, 71, key, 20, INK, True)
        b.arc(x + 110, 122, 25, 15, 310, BLUE, 3)
        b.text(x + 110, 122, '나', 16)
    b.arrow(250, 103, travel(t, 252, 401), 103, TEAL)
    b.text(323, 186, '컨테이너 사이의 목적지   db:5432', 18)

@scene(77, 2, 'rollback-switch', '정상 응답 200 뒤에도 버전을 되돌릴 수 있을까요?', '후보 B는 200을 돌려줘도 필수 출처가 없습니다. 이 수업용 상태에서는 출처를 되찾기 위해 이전 A로 바꿉니다.')
def switchback(b, t):
    for (i, (s, c)) in enumerate([('A · p2 있음', MINT), ('B · 출처 없음', PINK)]):
        b.chip(173 + i * 294, 78, s, c, 211, 52)
    x = travel(t, 467, 173)
    b.poly((x, 116, x - 14, 143, x + 14, 143), BLUE)
    b.text(x, 168, '활성 버전', 18, BLUE, True)
