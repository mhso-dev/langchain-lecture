"""Publish the daily index, legacy day downloads and offline pack from the same workbooks."""
from html import escape
from pathlib import Path
import re
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

OUT = Path(__file__).resolve().parents[1] / "dist"
DAILY = OUT / "daily"
BOOK = OUT / "pre-mid"
TASKS = [
    "진단을 풀고 A 또는 B를 고르세요. A는 녹음 길이를 초로 바꾸고, B는 단어 네 개를 두 기준으로 정렬합니다.",
    "A는 색상 목록에서 원본과 복사본을 바꿔 보고, B는 먼저 보여 줄 단어를 바꿔 정렬 결과를 확인하세요.",
    "A는 양의 짝수만 모으고, B는 새 출력 형식을 하나 추가해 기존 세 형식의 결과를 비교하세요.",
    "A는 두 번 호출한 기록이 섞이는 함수를 고치고, B는 출력 내용이 그대로인 채 호출 기록이 한 건씩 남는지 확인하세요.",
    "A는 두 카운터의 값이 독립인지 확인하고, B는 새로운 요구를 적용한 두 구현을 같은 입력으로 비교하세요.",
    "내 예제를 수정하던 중 오타 제보가 들어왔습니다. 별도 워크트리에서 오타만 커밋한 뒤, 원래 폴더에 어떤 변경이 남았는지 확인하세요.",
    "짝에게 예제 리뷰를 요청하고 같은 PR에 수정 커밋을 올리세요. 병합 뒤에는 짝이 처음 보는 입력으로 예제를 다시 실행합니다.",
    "첫 공지를 한 문장으로 요약해 달라고 요청하세요. 장소만 바꾼 공지를 같은 지시로 보내고 두 답에서 날짜와 장소를 확인하세요.",
    "같은 공지를 신입 회원용과 진행자용으로 안내하세요. 독자만 바꿨을 때 각자 해야 할 행동이 답에 드러나는지 원문과 비교하세요.",
    "일시와 장소를 뽑는 예시를 직접 쓰세요. 장소가 빠진 공지에서도 모델이 추측하지 않도록 프롬프트를 고쳐 보세요.",
    "모임 날짜를 토요일로 정정한 뒤 최종 안내를 요청하세요. 새 대화에 같은 마지막 질문만 보냈을 때와 비교하세요.",
    "채팅창에 두 번 질문하고 입력과 답이 몇 쌍 남는지 확인하세요. 화면이 다시 그려질 때 이전 입력이 한 번 더 전송되는지 살펴보세요.",
    "짝이 새 공지로 요약 길이를 바꾸도록 요청하게 하세요. 이어지는 대화와 초기화한 대화에서 이전 공지가 어떻게 처리되는지 확인하세요.",
]
pattern_sections = ["b02", "b11", "b19", "b28", "b42"]


def link(href, title):
    return f'<a href="{escape(href, quote=True)}">{escape(title)}</a>'


rows = []
downloads = {}
for day, task in enumerate(TASKS, 1):
    chapter = OUT / f"chapter{day:02}"
    alias = (chapter / "index.html").read_text()
    route = re.search(r'<a href="([^"]+)">([^<]+)</a>', alias)
    if not route or not route[1].startswith("../pre-mid/"):
        raise ValueError(f"{chapter.name}의 개편 교재 경로를 확인하세요.")
    href, title = route.groups()
    unit = href.split("/")[2]
    name = f"day{day:03}.ipynb"
    raw = (BOOK / unit / "lesson.ipynb").read_bytes()
    (DAILY / name).write_bytes(raw)
    downloads[name] = raw
    choices = [link(href, "수업 교재")]
    if day == 1:
        choices.append(link("../pre-mid/python-basics/index.html", "A 문법 수업"))
    if day <= 5:
        choices.extend([
            link("../pre-mid/python-basics/practice.html", "A 활동지"),
            link(f"../pre-mid/python-patterns/index.html#section-{pattern_sections[day-1]}-1", "B 패턴 수업"),
            link("../pre-mid/python-patterns/practice.html", "B 활동지"),
        ])
    else:
        choices.append(link(f"../pre-mid/{unit}/practice.html", "실습 활동지"))
    choices.append(link(name, "진단 노트북" if day == 1 else "A 수업 노트북" if day <= 5 else "수업 노트북"))
    if day == 1:
        choices.append(link("../pre-mid/python-basics/lesson.ipynb", "A 수업 노트북"))
    if day <= 5:
        choices.append(link("../pre-mid/python-patterns/lesson.ipynb", "B 수업 노트북"))
    rows.append(f'<li id="day{day:03}"><h2>{day}장 · {escape(title)}</h2><p>{task}</p><p>{" · ".join(choices)}</p></li>')

page = DAILY / "index.html"
html = page.read_text()
start = html.index('<li id="day002">')
end = html.index('<li id="day014">', start)
html = html[:start] + "".join(rows) + html[end:]
html = html.replace("2일부터 일반 수업 74일", "첫날부터 일반 수업 75일")
html = html.replace("개인 실습 78개와 자료 전체 받기", "수업 노트북과 실습 자료 전체 받기")
html = html.replace('<a href="#day002">2일</a>', '<a href="#day001">1일</a> · <a href="#day008">8일</a>')
# Jump links use the same task title as the destination.
headings = dict(re.findall(r'<li id="(day\d+)"><h2>([^<]+)</h2>', html))
html = re.sub(r'<a href="#(day\d+)">\d+일</a>', lambda m: f'<a href="#{m[1]}">{headings[m[1]]}</a>', html)
page.write_text(html)

# Keep the workbook and its relative Markdown links together when the ZIP is extracted.
materials = {path.relative_to(OUT).as_posix(): path.read_bytes() for path in sorted(BOOK.rglob("*"))
             if path.is_file() and path.suffix in {".ipynb", ".md", ".pdf", ".csv", ".txt"}}
materials["1-13일_실습_안내.txt"] = (
    "1~13장은 pre-mid 폴더에서 선택한 과정의 lesson.ipynb와 practice.md를 함께 여세요.\n"
    "1~5장은 diagnostic으로 시작해 python-basics 또는 python-patterns 중 하나를 고릅니다.\n"
    "6~7장은 team-git, 8~10장은 prompt-workshop, 11~13장은 chat-workshop에서 진행합니다.\n"
    "공지와 대여 규정, 녹음기 설명서는 pre-mid/documents에 있습니다.\n"
).encode()
for archive_name, additions in [
    ("all-labs.zip", {**downloads, **materials}),
    ("resources.zip", {k: v for k, v in materials.items() if not k.endswith(".ipynb")}),
]:
    target = DAILY / archive_name
    temp = target.with_suffix(".tmp")
    with ZipFile(target) as old, ZipFile(temp, "w") as new:
        for info in old.infolist():
            if info.filename not in additions:
                new.writestr(info, old.read(info))
        for name, raw in additions.items():
            info = ZipInfo(name, (2026, 11, 26, 0, 0, 0))
            new.writestr(info, raw, compress_type=ZIP_DEFLATED)
    temp.replace(target)
