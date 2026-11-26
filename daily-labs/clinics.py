"""Publish application exercises in the chapter, standalone notebook and offline set."""
import json
import re
import sys
from html import escape
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
from codex_studio import CASES

source = Path(__file__).parent
out = Path(sys.argv[1])
daily = out / "daily"
units = json.loads((source.parent / "coursebook/units.json").read_text())
units_by_day = {day: unit for unit in units for day in unit["lessons"]}
topics = {}
for line in (source / "extensions.txt").read_text().splitlines():
    number, title, explanation, assignment = line.split("|")
    topics[int(number)] = title, explanation, assignment
assert set(topics) == {*range(1, 43), *range(53, 86)}
curriculum = (source.parent / "curriculum.md").read_text().split("## 일차별 수업과 결과물")[1]
schedule = re.findall(r"^\| (\d+) \| ([^|]+) \| ([^|]+) \|$", curriculum, re.M)


# Pairing follows the data each exercise consumes, including deliberate revisits.
companions = {
    1:2,2:3,3:2,4:3,5:2,6:5,7:4,8:9,9:8,10:9,11:10,12:11,13:12,14:13,15:14,16:15,17:16,18:17,
    19:13,20:21,21:20,22:21,23:22,24:23,25:24,26:27,27:26,28:27,29:28,30:23,31:24,32:30,
    33:16,34:33,35:31,36:35,37:36,38:37,39:38,40:29,41:40,42:39,
    53:5,54:53,55:17,56:55,57:55,58:57,59:29,60:59,61:33,62:61,63:62,64:63,65:56,66:64,67:66,
    68:54,69:41,70:68,71:68,72:71,73:22,74:72,75:74,76:7,77:76,78:40,79:68,80:79,
    81:17,82:36,83:55,84:39,85:84,
}
assert set(companions) == set(topics)

def markdown(key, text):
    return dict(cell_type="markdown", id=key, metadata={}, source=text.splitlines(True))


def encode(book):
    return json.dumps(book, ensure_ascii=False, indent=1) + "\n"


new_downloads = {}
for number, scheduled_title, goal in schedule:
    day = int(number)
    folder = out / f"chapter{day:02}"
    chapter = folder / (folder.name + ".ipynb")
    file = daily / f"day{day:03}.ipynb"
    team = 43 <= day <= 52 or 86 <= day <= 116
    if day >= 117:
        continue  # Fieldwork already has a standalone 60–120 minute assignment.
    if team:
        title = scheduled_title + " · 팀 작업 점검"
        explanation = "팀이 개발 중인 서비스에서 오늘 확인할 결과는 “" + goal + "”이다."
        task = "입력과 통과 기준을 먼저 합의하고 한 명이 구현한 결과를 다른 팀원이 재현한다. 기대와 다른 사례 한 건을 이슈에 남기고 수정 후 같은 조건에서 다시 확인한다."
        timing = "팀 프로젝트 시간 안에서 60~120분"
    else:
        title, explanation, task = topics[day]
        timing = "기존 개인 과제를 포함해 60~120분"
    unit = units_by_day[day]
    if 75 <= day <= 80:
        task += " 전체 실습 묶음을 풀고 daily_resources/codex-kit에서 시작한다. tasks.json에 같은 이름의 두 항목이 있다. python -m unittest -v로 기준 결과를 확보하고 매번 같은 저장소에서 수정한다."
    label = "팀 실습" if team else "개인 실습"
    text = f"## {title}\n\n{explanation}\n\n### {label} · {timing}\n\n{task}\n\n실행한 입력, 기대값, 관찰한 결과와 수정 근거를 아래에 남긴다."
    cells = [markdown("clinic-brief", text), markdown("clinic-record", "### 내 실행 기록\n\n입력과 기대값 · 실제 결과 · 다음 수정")]
    sample_html = ""
    if day in CASES:
        heading, seed, probe, solution, expected = CASES[day]
        answer = '<details class="notebook-answer"><summary>풀이와 확인 기준</summary><pre><code>'+escape(solution)+'</code></pre><p>'+escape(expected)+'</p></details>'
        def program(key, value):
            return dict(cell_type="code", id=key, metadata={}, outputs=[], execution_count=None, source=value.splitlines(True))
        cells[1:1] = [markdown("codex-case","### "+heading), program("codex-example",seed),
                      markdown("codex-brief",probe), program("codex-work","# 위 조건을 검증하는 코드를 작성하세요."), markdown("codex-answer",answer)]
        sample_html = "<h3>"+escape(heading)+"</h3><pre><code>"+escape(seed)+"</code></pre><p>"+escape(probe)+"</p>"+answer
    if day in companions:
        other = companions[day]
        related_page = (out / f"chapter{other:02}/index.html").read_text()
        matches = re.findall(r'<section\b[^>]*?\bid="([^"]+)"[^>]*>(?:(?!</section>).)*?<h2[^>]*>(.*?)</h2>', related_page, re.S)
        links = [(key,re.sub('<[^>]+>', '', title)) for key,title in matches if key not in {"start","plan","sources","recap","daily-lab","applied-clinic"}][:2]
        items = ''.join(f'<li><a href="../chapter{other:02}/index.html#{key}">{title}</a></li>' for key,title in links)
        if items:
            sample_html += '<h3>함께 실행할 예제</h3><ul>'+items+'</ul>'
            cells.append(markdown("connected-examples","### 함께 실행할 예제\n\n"+"\n".join(f"- [{title}](https://langchain-lecture.vercel.app/chapter{other:02}/index.html#{key})" for key,title in links)))
    core = json.loads(chapter.read_text())
    core["cells"].extend(cells)
    chapter.write_text(encode(core))
    if file.exists():
        lab = json.loads(file.read_text())
    else:
        lab = dict(nbformat=4, nbformat_minor=5, metadata=core["metadata"], cells=[])
    lab["cells"].extend(cells)
    if day == 1:
        lab["cells"].insert(1, dict(cell_type="code", id="csv-input", execution_count=None, outputs=[], metadata={}, source=[
            'from pathlib import Path\n', 'sample = Path("first-shift.csv")\n',
            'sample.write_text("ticket,branch\\nA,서울\\nB,부산\\nC,서울\\n", encoding="utf-8")\n',
            '# CSV를 다시 읽어 서울 2건, 부산 1건인지 확인하세요.']))
    file.write_text(encode(lab))
    new_downloads[file.name] = file
    html = folder / "index.html"
    link = f'../daily/{file.name}'
    box = (f'<section class="lesson-section" id="applied-clinic"><h2>{escape(title)}</h2><p>{escape(explanation)}</p>'
           f'{sample_html}<h3>{label} · {timing}</h3><p>{escape(task)}</p><p><a href="{link}" download>실습 노트북</a> · '
           f'<a href="../topics/{unit["slug"]}/index.html">{escape(unit["title"])} 통합 예제</a></p></section>')
    h = html.read_text()
    if day == 1:
        h = re.sub(r'<section class="lesson-section" id="daily-lab">.*?</section>', '<section id="daily-lab"><a href="#applied-clinic">첫 개인 실습</a></section>', h, count=1, flags=re.S)
    html.write_text(h.replace('</main>',box+'</main>',1))

with ZipFile(daily / "all-labs.zip") as old, ZipFile(daily / "labs.tmp", "w", ZIP_DEFLATED) as archive:
    for entry in old.infolist():
        if entry.filename not in new_downloads:
            archive.writestr(entry, old.read(entry))
    for name, path in new_downloads.items():
        archive.write(path, name)
(daily / "labs.tmp").replace(daily / "all-labs.zip")
idx = daily / "index.html"
h = idx.read_text().replace('2일부터 일반 수업 74일과 특강 4일에 하루 60~120분. 중간·최종 프로젝트 41일은 팀 작업에 사용합니다.', '일반 수업 75일과 특강 4일은 개인 실습, 프로젝트 41일은 팀 산출물 점검에 60~120분을 씁니다.').replace('개인 실습 78개와 자료 전체 받기','120일 실습과 자료 전체 받기')
extra_days = [1, *range(43, 53), *range(86, 117)]
links = ''.join(f'<li><a href="../chapter{n:02}/index.html#applied-clinic">{n}일 · {escape(schedule[n-1][1])}</a></li>' for n in extra_days)
idx.write_text(h.replace('</main>', '<section><h2>첫날 과제와 팀 프로젝트 실습</h2><ul>'+links+'</ul></section></main>', 1))
