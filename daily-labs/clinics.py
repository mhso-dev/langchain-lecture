"""Publish application exercises in the chapter, standalone notebook and offline set."""
import json
import re
import sys
from html import escape
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
from codex_studio import CASES
from todo_agent_workshop import STAGES, lesson, publish_bundle

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


def worked_example(day, companion):
    stem = f"chapter{companion:02}"
    original = source.parent / "site" / stem / (stem + ".ipynb")
    sequence = json.loads(original.read_text())["cells"]
    choices = []
    for index, cell in enumerate(sequence[:-1]):
        if cell["cell_type"] != "code" or sequence[index+1]["cell_type"] != "markdown":
            continue
        code = "".join(cell["source"]).strip()
        result = "".join("".join(o.get("text", [])) for o in cell["outputs"]).strip()
        note = "".join(sequence[index+1]["source"]).strip().split("\n\n")[0]
        if not result or len(code) > 1400 or len(result) > 700 or not note or note.startswith(("#","<","```")):
            continue
        if len(note) > 550 or any(word in (note+result) for word in ("설치된 수업 커널","대본 모델","테스트 모델","classroom-mock","MockTransport","FakeList","FakeMessages","API 키가 없")):
            continue
        choices.append((code, result, note))
    if not choices:
        return "", ""
    code, result, note = choices[day % min(3, len(choices))]
    url = f"../{stem}/{stem}.ipynb"
    title = f"관련 예제를 실행해 보기 · 자료 {companion}"
    web = (f"<h3>{title}</h3><pre><code>{escape(code)}</code></pre><p>예제 출력</p><pre>{escape(result)}</pre>"
           f'<p>{escape(note)}</p><p><a href="{url}">입력 준비부터 전체 노트북 실행하기</a></p>')
    excerpt = f"### {title}\n\n```python\n{code}\n```\n\n예제 출력\n\n```text\n{result}\n```\n\n{note}\n\n[입력 준비부터 전체 노트북 실행하기](https://langchain-lecture.vercel.app/{stem}/{stem}.ipynb)"
    return web, excerpt


def encode(book):
    return json.dumps(book, ensure_ascii=False, indent=1) + "\n"


publish_bundle(daily / "todo-agent.zip")
new_downloads = {"todo-agent.zip": daily / "todo-agent.zip"}
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
        example, excerpt = worked_example(day, other)
        if example:
            sample_html += example
            cells.append(markdown("connected-reading", excerpt))
        related_page = (out / f"chapter{other:02}/index.html").read_text()
        matches = re.findall(r'<section\b[^>]*?\bid="([^"]+)"[^>]*>(?:(?!</section>).)*?<h2[^>]*>(.*?)</h2>', related_page, re.S)
        links = [(key,re.sub('<[^>]+>', '', title)) for key,title in matches if key not in {"start","plan","sources","recap","daily-lab","applied-clinic"}][:2]
        items = ''.join(f'<li><a href="../chapter{other:02}/index.html#{key}">{title}</a></li>' for key,title in links)
        if items:
            sample_html += '<h3>함께 실행할 예제</h3><ul>'+items+'</ul>'
            cells.append(markdown("connected-examples","### 함께 실행할 예제\n\n"+"\n".join(f"- [{title}](https://langchain-lecture.vercel.app/chapter{other:02}/index.html#{key})" for key,title in links)))
    agent_section = ""
    if day in STAGES:
        agent_section, agent_cells = lesson(day)
        cells.extend(agent_cells)
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
           f'<a href="../daily/resources.zip" download>입력 자료 받기</a> · '
           f'<a href="../topics/{unit["slug"]}/index.html">{escape(unit["title"])} 통합 예제</a></p></section>')
    box += agent_section
    h = html.read_text()
    if 'href="../daily/resources.zip"' in h:
        box = box.replace('<a href="../daily/resources.zip" download>입력 자료 받기</a> · ', "")
    if day == 1:
        h = re.sub(r'<section class="lesson-section" id="daily-lab">.*?</section>', '<section id="daily-lab"><a href="#applied-clinic">첫 개인 실습</a></section>', h, count=1, flags=re.S)
    if day == 1:
        starter = escape("".join(lab["cells"][1]["source"]))
        box = box.replace("</section>", f"<h3>입력 자료 만들기</h3><pre><code>{starter}</code></pre></section>")
    # Keep both parts of a day's practice together, before the end-of-chapter controls.
    marker = h.find('id="daily-lab"')
    end = h.find("</section>", marker) if marker >= 0 else -1
    if end >= 0:
        end += len("</section>")
        html.write_text(h[:end]+box+h[end:])
    else:
        html.write_text(h.replace("</main>",box+"</main>",1))

with ZipFile(daily / "all-labs.zip") as old, ZipFile(daily / "labs.tmp", "w", ZIP_DEFLATED) as archive:
    for entry in old.infolist():
        if entry.filename not in new_downloads:
            archive.writestr(entry, old.read(entry))
    for name, path in new_downloads.items():
        archive.write(path, name)
(daily / "labs.tmp").replace(daily / "all-labs.zip")
