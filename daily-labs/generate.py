"""Build the private-study assignment section, notebooks and offline download."""
import csv
from html import escape
from studios import NOTES, starter, variation
from lessons import READINGS, CHARTS, LINKS
from project_reference import project_reference
from execution import publish_results
import json
from pathlib import Path
import re
import shutil
import sys
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

HERE = Path(__file__).resolve().parent
OUT = Path(sys.argv[1])
DAILY = OUT / "daily"
DAILY.mkdir(exist_ok=True)
HOST = "https://langchain-lecture.vercel.app"
DATA = """from pathlib import Path
import csv
import json

data_dir = Path("daily_resources")
if data_dir.is_dir():
    def read_table(name):
        with (data_dir / name).open(encoding="utf-8", newline="") as file:
            return list(csv.DictReader(file))
    tickets = read_table("tickets.csv")
    questions = read_table("questions.csv")
    manifest = read_table("manifest.csv")
    chunks = json.loads((data_dir / "chunks.json").read_text(encoding="utf-8"))
    print("접수", len(tickets), "질문", len(questions), "문서", len(manifest), "조항", len(chunks))
else:
    print("자료를 쓰는 과제는 전체 묶음을 풀고 노트북을 daily_resources 옆에서 여세요.")"""
REQUEST = 'request = dict(branch="서울", audience="개인", as_of="2026-07-01", topic="receipt")'
START = {
 15:REQUEST+'\n# 잘못된 날짜와 누락 필드를 추가해 요청 검증 함수를 작성하세요.',
 20:'pdf_path = data_dir / "documents" / "R02.pdf"\ntext_path = data_dir / "documents" / "R04.txt"\n# pypdf.PdfReader로 두 쪽을 각각 읽고 TXT는 절로 분리하세요.',
 21:'document_ids = ["R02", "R03"]\n# 직접 나눈 각 조각에 문서 ID, 쪽 번호, 문자 범위를 보존하세요.',
 22:'from pathlib import Path\nindex_path = Path("my-practice-chroma")\nchange_dates = ["2026-06-30", "2026-07-01"]\n# reference/chroma_lab.py를 참고해 자기 index_path에 직접 적재하세요.\n# 날짜를 숫자로 저장하고 시작일 이하·종료일 이상 조건을 모두 적용하세요.',
 23:'case_ids = ["Q06", "Q07", "Q10"]\n# questions에서 세 사례의 입력만 검색기에 전달하세요. gold_chunk와 key는 채점할 때만 읽습니다.',
 24:'case_ids = ["Q01", "Q09"]\n# 입력→검색→생성(또는 보류) 결과를 요청별로 보관하세요.',
 25:'new_doc = {"doc_id":"N01", "branch":"대전", "topic":"export"}\n# 새 문서 원문을 직접 쓰고 대상, 유효 기간, 출처 경로를 정하세요.',
 33:REQUEST+'\n# lookup_policy 도구 호출에 고유 ID를 붙이고 상태 messages에 연결하세요.',
 55:'prompts = ["안녕하세요", "서울 개인 영수증 열람 기한은?", "T03의 처리 상태는?", "지난번 건 언제 나와요?"]\n# 각 질문에 예상 도구를 적은 뒤 실제 선택과 비교하세요.',
 56:'limits = [1, 2]\n# 요청 단위로 초기화하는 호출·실행·차단 기록을 만드세요.',
 57:'skill_names = ["receipt", "export"]\n# 예시 두 파일을 읽고 자기 작업 폴더에 수정한 SKILL.md를 저장하세요.',
 58:'topics = ["receipt", "export", "unknown"]\n# 선택과 상세 읽기를 다른 함수로 나누고 실제 연 경로만 로그에 기록하세요.',
 61:REQUEST+'\n# starter/my_policy.py와 my_server.py를 복사해 구현한 뒤\n# names, reply = await sample(request, 내_서버_경로)로 실제 프로세스를 호출하세요.',
 62:REQUEST+'\n# 62장 본문의 Streamable HTTP 클라이언트에 같은 조회 도구를 연결하세요.',
 64:'request_ids = ["export-1", "export-1", "export-2"]\n# 첫 요청을 두 번 승인하고 마지막 요청은 거절하세요.',
 66:REQUEST+'\nold_evidence = ["R01-1"]\n# 부모→조회 역할→검토 역할로 데이터를 넘기고 정상/오래된 인계를 비교하세요.',
 80:'items = [{"id":1,"title":"정리"},{"id":2,"title":"정리"}]\n# 브라우저 구현에서 id=2만 삭제한 뒤 실제 남은 ID를 확인하세요.',
 90:'test_set_version = "v1"\n# 개발 질문과 확인 질문을 다른 파일로 보관하세요.',
 118:'comparisons = [("서울","개인","2026-06-30"), ("서울","개인","2026-07-01"), ("서울","가맹점","2026-07-01")]\n# 세 근거 ID와 기간을 각각 찾아 evidence_ids에 저장하세요.'
}
START.update({20:"my_pages = []  # 편람의 36쪽과 메타데이터를 결합하세요.",21:"my_chunks = []  # 조각별 쪽 번호와 원문 위치를 저장하세요.",22:"index_path = Path('handbook-chroma')\n# 아래 본문의 영속 검색 예를 자신의 청크로 바꾸세요.",23:"cases = ['B03','B10']  # 후보와 근거 없음 응답을 구분하세요.",24:"cases = ['B02','B04','B10']",25:"source_files = ['N01-manual.pdf','N02-notice.txt']  # 두 문서를 직접 청킹하고 판본을 구분하세요."})
for codex_day in range(80,86):
    START[codex_day] = "# 위 예제로 내 저장소를 준비한 뒤 오늘 수정한 파일과 실제 실행 기록을 남기세요."
ANSWERS = {
 66:('두 역할 호출 예시','import sys\nsys.path.insert(0, str((data_dir / "reference").resolve()))\nfrom roles import run_roles\nprint(run_roles(request)["status"], run_roles(request, ["R01-1"])["status"])','accepted hold'),
 118:('판본 결과 대조','print([r["chunk_id"] for branch,who,day in comparisons for r in chunks if r["branch"]==branch and r["audience"]==who and r["valid_from"]<=day<=r["valid_to"] and r["topic"]=="receipt" and r["section"]==1])',"['R01-1', 'R02-1', 'R04-1']")
}
def cell(kind, key, text):
    out = dict(cell_type=kind, id="solo-"+key, metadata={}, source=text.splitlines(keepends=True))
    if kind=="code":
        out.update(execution_count=None,outputs=[])
    return out

def material(n):
    if n in (20,21,22,23,24,25,35): return 'handbook/operations.pdf(36쪽), pages.csv, evaluation.csv와 extension의 개정 공지. 날짜·지점·종류를 보존한다.'
    if n == 80: return '79일차 화면, 수업 노트북, 로컬 Git 저장소와 Codex.'
    if 81 <= n <= 85: return '오늘의 수업 노트북, 수업용 LangSmith 프로젝트와 가상 문의. 로컬 예제부터 실행하세요.'
    if n<=7: return 'cases/shift.csv의 교대 원장 26행. 전체 실습 묶음의 cases/shift_reference.py로 이전 단계의 처리 결과를 복원할 수 있습니다.'
    if n in (53,54): return 'tickets.csv 원본 6행, 수업 SQL 예제와 쓰기가 가능한 실습 데이터베이스'
    if n<=10: return 'tickets.csv, R02.pdf, R03.pdf, R04.txt와 해당 장 수업 예제'
    if n<=19: return '해당 장 SDK·LCEL 수업 예제, questions.csv의 Q01·Q09·Q10과 직접 바꾼 질문'
    if n<=54: return 'documents/ 원문, manifest.csv, questions.csv, chunks.json 및 전날 만든 색인·서비스. 처음 시작하면 공통 자료와 해당 장 수업 예제로 기준선을 만든다.'
    if n<=67 or n in (95,99,100,101): return 'starter/, skills/, reference/stdio_steps.md, policy.py와 해당 장 수업 예제. 실습 후 reference/ 구현으로 결과를 대조한다.'
    if n<=79: return '해당 장 FastAPI·DB·웹 예제, tickets.csv와 가상 정책 질문. 원격 실습은 배정된 수업용 환경을 사용한다.'
    return '자기 프로젝트 최신판·실행 기록. 독립 연습이 필요하면 공통 정책 문서와 reference/policy.py를 작은 서비스의 시작점으로 쓴다.'

def build_cells(n, title, first, second, check):
    duration = 60 if n in (8,9,10,43,86,87,88,115,116,117,118,119,120) else 120 if n in (55,56,64,66,67,80,81,82,83,84,85,22,25,34,45,55,61,62,66,71,73,74,77,85,106,112,113) else 90
    mins={60:(10,25,15,10),90:(10,40,25,15),120:(15,50,35,20)}[duration]
    cells=[cell("markdown","intro",f"## 개인 실습 {n:03} · {title}\n\n예상 {duration}분. 자료를 준비하고 입력을 예측하는 데 {mins[0]}분, 첫 구현에 {mins[1]}분, 다른 입력과 실패 사례에 {mins[2]}분, 결과를 다시 확인하는 데 {mins[3]}분을 씁니다.\n\n**준비물** {material(n)}\n\n[전체 실습 묶음]({HOST}/daily/all-labs.zip)을 풀고 이 노트북을 daily_resources 옆에 두세요. "+(f"[오늘의 수업 예제]({HOST}/chapter{n:02}/index.html)" if n<=116 else "특강·현장 일정에 맞춰 개별 수행합니다."))]
    goal, method, probe = NOTES[n]
    cells.append(cell("code","input",DATA))
    cells.append(cell("markdown","brief",f"### 납품할 결과\n\n{goal}\n\n**구현 단서** {method}"))
    cells.extend([cell("markdown","part-a","### 1. 구현하기\n\n"+first),cell("code","implementation",starter(n,START)),
                  cell("markdown","part-b","### 2. 조건을 바꿔 다시 실행하기\n\n"+second),
                  cell("code","variation",variation(n)),
                  cell("markdown","criteria","### 3. 스스로 확인하기\n\n"+check+"\n\n**실패 원인 좁히기** "+probe+"\n\n**내 기록**\n\n- 처음 사용한 입력과 기대값\n- 실제 실행 결과와 달랐던 지점\n- 수정한 줄 또는 설정, 다시 실행한 결과")])
    if n in (33,118):
        cells.extend([cell("markdown","bench-title","### 기준 구현과 대조하기\n\n자기 구현을 먼저 실행한 뒤 아래 비교 셀을 사용하세요. 검색 도구는 필터에 맞는 조항을 반환합니다. 검색 순위와 자연어 답변은 별도 검사합니다."),
                      cell("code","bench","import sys\nif data_dir.is_dir():\n    sys.path.insert(0, str((data_dir / 'reference').resolve()))\n    from policy import lookup_policy\n    from check_filter import check_filter\n    print(check_filter(lookup_policy))\n    # 자기 함수를 완성한 뒤 check_filter(내_조회함수)로 교체하세요.")])
    if n in ANSWERS:
        label,code,result=ANSWERS[n]
        cells.append(cell("markdown","answer","<details><summary>"+label+"</summary><pre><code>"+escape(code)+"</code></pre><p>"+escape(result)+"</p></details>"))
    return duration,cells

def encode(obj):
    return (json.dumps(obj,ensure_ascii=False,indent=1)+"\n").encode()

def put(z,name,data):
    info=ZipInfo(name,(2026,11,24,0,0,0))
    info.compress_type=ZIP_DEFLATED
    z.writestr(info,data)

spec=[line.split("|") for line in (HERE/"assignments.txt").read_text().splitlines() if line]
if [int(row[0]) for row in spec]!=[n for n in range(2,121) if not (43<=n<=52 or 86<=n<=116)] or any(len(row)!=5 for row in spec):
    raise ValueError("교육일·실습 필드를 확인하세요")
if set(NOTES) != {int(row[0]) for row in spec}:
    raise ValueError("개인 과제와 작업 의뢰서의 교육일이 다릅니다")
resources=DAILY/"resources.zip"
with ZipFile(HERE/"resources.zip") as original, ZipFile(resources,"w") as packed:
    for name in original.namelist():
        override = HERE / "live-resources" / name.removeprefix("daily_resources/")
        put(packed,name,override.read_bytes() if override.is_file() else original.read(name))
    for path in sorted((HERE/"cases").glob("*")):
        if path.is_file():
            put(packed,"daily_resources/cases/"+path.name,path.read_bytes())
with ZipFile(resources) as data, ZipFile(DAILY/"all-labs.zip","w") as archive:
    for entry in data.namelist():
        raw=data.read(entry)
        put(archive,entry,raw)
        target=DAILY/entry
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(raw)
    for number,title,first,second,check in spec:
        n=int(number)
        duration,cells=build_cells(n,title,first,second,check)
        goal,method,probe=NOTES[n]
        extras=[]
        article=''
        if n in READINGS and not 80 <= n <= 85:
            heading,reading,program,observation=READINGS[n]
            source_link=LINKS.get(n)
            extras=[cell("markdown","walkthrough",f"### {heading}\n\n{reading}"),
                    cell("code","walkthrough-code",program),
                    cell("markdown","walkthrough-result",observation)]
            article=f'<h3>{escape(heading)}</h3><p>{escape(reading)}</p><pre style="overflow:auto"><code>{escape(program)}</code></pre><p><mark>실행 뒤 확인</mark> {escape(observation)}</p>'
            if source_link:
                article+=f'<p><a href="{source_link}">공식 문서</a></p>'
                extras.append(cell("markdown","source",f"[공식 문서]({source_link})"))
            if n in CHARTS:
                chart=CHARTS[n]
                extras.append(cell("markdown","chart","### 실행 경로\n\n```mermaid\n"+chart+"\n```"))
                article+='<figure class="workflow-reading" data-workflow><h3>실행 경로</h3><div class="workflow-view" hidden></div><script type="text/plain">'+chart+'</script></figure>'
            cells[2:2]=extras
        if n == 19:
            cells = json.loads((OUT/"chapter19/sdk-inquiry.ipynb").read_text())["cells"] + [cells[-1]]
        if n == 80:
            cells = [cells[0], cells[2], cell("markdown", "app", first+"\n\n"+second), cells[-1]]
            cells += [cell("code","acceptance","expected_ids = [1]  # ID 2를 삭제한 뒤 실제 화면과 대조하세요.")]
        if 81 <= n <= 85:
            stem = f"chapter{n:02}"
            core = json.loads((OUT/stem/(stem+".ipynb")).read_text())["cells"]
            cells = [cells[0], *core]
        name=f"day{n:03}.ipynb"
        notebook=dict(nbformat=4,nbformat_minor=5,metadata={"kernelspec":{"name":"python3","language":"python","display_name":"Python 3"}},cells=cells)
        raw=encode(notebook)
        (DAILY/name).write_bytes(raw)
        put(archive,name,raw)
        section=f'<section class="lesson-section" id="daily-lab"><h2>개인 실습 · {escape(title)}</h2><p>예상 {duration}분 · {escape(material(n))}</p><h3>작업 의뢰</h3><p>{escape(goal)}</p>{article}<ol><li>{escape(first)}</li><li>{escape(second)}</li></ol><p><mark>구현 단서</mark> {escape(method)}</p><p><strong>결과가 다르면</strong> {escape(probe)}</p><p><mark>완료 기준</mark> {escape(check)}</p><p><a href="../daily/{name}" download>오늘의 개인 과제</a> · <a href="../daily/resources.zip" download>공통 실습 자료</a></p></section>'
        if 81 <= n <= 85:
            section = section.replace("</section>", '<p><a href="#workshop">로컬 예제와 풀이</a> · <a href="#service">서비스에 적용하기</a></p></section>')
        if n == 80:
            section=section.replace("</section>",'<p><a href="../daily/codex-harness.ipynb" download>선택 실습 · 이전 판 Codex 하네스 노트북</a></p></section>')
        if n in (20,21,22,23,24,25,35):
            section=section.replace("</section>",'<p><a href="../daily/daily_resources/handbook/operations.pdf">36쪽 운영 편람 원문</a> · <a href="../daily/daily_resources/handbook/pages.csv">쪽별 대장</a></p></section>')
        if n<=116:
            chapter=OUT/f"chapter{n:02}"
            page=chapter/"index.html"
            source=page.read_text()
            marker='<footer class="lesson-footer">'
            if marker not in source:raise ValueError(page)
            source=source.replace(marker,section+marker,1)
            source=re.sub(r'(<a class="download"[^>]*>.*?</a>)',r'\1<p class="reuse-note"><a href="#daily-lab">오늘의 개인 실습 · '+str(duration)+'분</a></p>',source,count=1,flags=re.S)
            if n in CHARTS and "../assets/workflows.js" not in source:
                source=source.replace("</head>",'<script defer src="../assets/mermaid/mermaid.tiny.js"></script><script defer src="../assets/workflows.js"></script></head>')
            page.write_text(source)
            file=chapter/(chapter.name+".ipynb")
            original=json.loads(file.read_bytes())
            if not 81 <= n <= 85:
                original["cells"].append(cell("markdown","daily-assignment",f"## 개인 실습 · {title} ({duration}분)\n\n{goal}\n\n1. {first}\n2. {second}\n\n**구현 단서** {method}\n\n**스스로 확인하기** {check}\n\n{probe}\n\n[오늘의 개인 실습 노트북]({HOST}/daily/{name}) · [실습 자료 묶음]({HOST}/daily/resources.zip)"))
            original["cells"].extend(extras)
            file.write_bytes(encode(original))
        # Show the supplied starter and worked answer beside the assignment.
        snippets = []
        labels = {"solo-input":"입력 자료 준비", "solo-implementation":"구현할 코드", "solo-variation":"다른 입력으로 확인하기",
                  "solo-bench":"기준 구현과 대조하기", "setup":"실습 준비", "example":"실행 예제", "task":"직접 작성하기"}
        for item in cells:
            key = item["id"]
            raw = "".join(item["source"])
            if key in labels and item["cell_type"] == "code":
                snippets.append(f'<h3>{labels[key]}</h3><pre><code>{escape(raw)}</code></pre>')
            elif key in {"solo-answer", "answer"} and raw.startswith("<details"):
                snippets.append(raw.replace("<details>", '<details class="notebook-answer">', 1))
        if n <= 116:
            if snippets:
                text = page.read_text()
                page.write_text(text.replace(section, section[:-10]+"".join(snippets)+"</section>", 1))
        else:
            folder = OUT / f"chapter{n:02}"
            folder.mkdir(exist_ok=True)
            (folder / "index.html").write_text(section[:-10]+"".join(snippets)+"</section>")

    put(archive,"codex-harness.ipynb",(DAILY/"codex-harness.ipynb").read_bytes())
first = OUT/"chapter01"/"index.html"
first.write_text(first.read_text().replace('<footer class="lesson-footer">','<section class="lesson-section" id="daily-lab"><h2>첫 개인 과제 준비</h2><p>오늘은 수업 예제로 커널과 파일 열기를 익힙니다. 다음 수업부터 26행의 상담 원장으로 교대 인수인계 프로그램을 만듭니다.</p><p><a href="../chapter02/index.html#daily-lab">2일차 교대 원장 열기</a></p></section><footer class="lesson-footer">',1))
for project_day in list(range(43,53))+list(range(86,117)):
    project_reference(OUT/f"chapter{project_day:02}",encode)
# Keep the downloadable PDF lab notebook identical to the separately served chapter 20 notebook.
pdf_kit = OUT / "chapter20" / "chapter20-lab.zip"
if pdf_kit.exists():
    with ZipFile(pdf_kit) as previous:
        contents = {name:previous.read(name) for name in previous.namelist()}
    contents["chapter20.ipynb"] = (pdf_kit.parent/"chapter20.ipynb").read_bytes()
    contents["day020.ipynb"]=(DAILY/"day020.ipynb").read_bytes()
    with ZipFile(resources) as data:
        for name in data.namelist():
            contents[name]=data.read(name)
    with ZipFile(pdf_kit,"w") as updated:
        for name,raw in contents.items():
            put(updated,name,raw)
index=OUT/"updates/index.html"
changed=[*range(20,26),35,*range(43,53),55,56,64,66,67,*range(80,117)]
entries=[]
for day in changed:
    ch=OUT/f"chapter{day:02}"; nb=json.loads((ch/(ch.name+".ipynb")).read_bytes())
    title="".join(nb["cells"][0]["source"]).splitlines()[0].strip("# ")
    target="daily-lab" if day in READINGS and not 81 <= day <= 85 else "recap"
    entries.append(f'<li><a href="../{ch.name}/index.html#{target}">{escape(title)}</a></li>')
news='<section class="edition-group"><h2>11월 24일 · 프로젝트 일정과 후반 실습 개편</h2><p>프로젝트 41일은 팀 작업과 참고 사례에 쓰고, 일반 수업에서 긴 PDF 검색, 승인 재개, Codex 하네스를 직접 구현합니다.</p><ul>'+"".join(entries)+'</ul></section>'
history=index.read_text()
for day in (*range(43,53),*range(86,117)):
    route=f'../chapter{day:02}/index.html'
    page=(OUT/f'chapter{day:02}/index.html').read_text()
    def current_section(match):
        anchor=match.group(1)
        return route+'#'+(anchor if f'id="{anchor}"' in page else 'workshop')
    history=re.sub(re.escape(route)+r'#([\w-]+)',current_section,history)
all_changed=[]
for day in [1]+[int(item[0]) for item in spec]:
    if day<=116:
        folder=OUT/f'chapter{day:02}'
        title=''.join(json.loads((folder/(folder.name+'.ipynb')).read_bytes())['cells'][0]['source']).splitlines()[0].strip('# ')
        all_changed.append(f'<li><a href="../{folder.name}/index.html#daily-lab">{escape(title)}</a></li>')
    else:
        title=next(row[1] for row in spec if int(row[0])==day)
        all_changed.append(f'<li><a href="../chapter{day:02}/index.html#daily-lab">{day}일 · {escape(title)}</a></li>')
edition='<section class="edition-group"><h2>11월 24일 · 교대 인수인계와 실무 과제 개정</h2><p>첫날 별도 과제를 없애고 2~7일에 교대 원장 하나를 인수인계합니다. 이후 개인 과제마다 납품할 결과와 구체적인 시험 조건을 제공합니다.</p><p><a href="../schedule.html">실습이 포함된 일차별 교재</a> · <a href="../chapter64/index.html#daily-lab">재발급 승인 창구</a> · <a href="../chapter85/index.html#daily-lab">Codex 기능 변경 납품</a> · <a href="../execution/index.html">대기 장 실행 결과</a></p><details><summary>개정 장 전체 목록</summary><ul>'+"".join(all_changed)+'</ul></details></section>'
index.write_text(history.replace("<main>","<main>"+edition+news,1))

publish_results(OUT)
