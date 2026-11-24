"""Build the private-study assignment section, notebooks and offline download."""
import csv
from html import escape
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
 1:'request_id = "T01"\nbranch = "서울"\nstatus = "완료"\n# 세 변수로 한 줄 접수증을 작성하세요.',
 2:'rows = [("T01", "완료", 12), ("T02", "접수", 0), ("T03", "완료", 18), ("T03", "완료", 18), ("T04", "보류", 5), ("T05", "완료", 0)]\n# 중복 ID를 먼저 처리하고 평균을 average_minutes에 저장하세요.',
 3:'samples = [" 12 ", "0", "", "-3"]\n# parse_minutes(value)를 작성하고 각 입력의 결과 또는 오류를 기록하세요.',
 4:'requests = ["T01", "T02"]\n# 각 요청의 상태와 기록을 따로 보존하는 클래스를 작성하세요.',
 5:'normal, duplicates, incomplete = [], [], []\n# tickets의 레코드 6건을 분류하고 파일로 저장하세요.',
 6:'paths = ["/tickets/T01", "/tickets/T99", "/tickets/slow"]\n# 수업 노트북의 MockTransport 핸들러를 세 경우로 확장하세요.',
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
ANSWERS = {
 1:('접수증 예시','print(f"{branch} / {request_id} / {status}")','서울 / T01 / 완료'),
 2:('평균 검산','unique = {key:(state, minutes) for key,state,minutes in rows}\ncompleted = [m for state,m in unique.values() if state == "완료"]\nprint(sum(completed) / len(completed))','10.0'),
 3:('입력 검산','def parse_minutes(value):\n    number = int(value.strip())\n    if number < 0:\n        raise ValueError("음수 시간")\n    return number','12와 0 허용, 빈 문자열과 음수는 ValueError'),
 61:('실제 MCP 연결 예시','import sys\nsys.path.insert(0, str((data_dir / "reference").resolve()))\nfrom mcp_client import sample\nnames, reply = await sample(request)\nprint(names, reply["items"][0]["chunk_id"])',"['lookup_policy'] R02-1"),
 66:('두 역할 호출 예시','import sys\nsys.path.insert(0, str((data_dir / "reference").resolve()))\nfrom roles import run_roles\nprint(run_roles(request)["status"], run_roles(request, ["R01-1"])["status"])','accepted hold'),
 118:('판본 결과 대조','print([r["chunk_id"] for branch,who,day in comparisons for r in chunks if r["branch"]==branch and r["audience"]==who and r["valid_from"]<=day<=r["valid_to"] and r["topic"]=="receipt" and r["section"]==1])',"['R01-1', 'R02-1', 'R04-1']")
}
def cell(kind, key, text):
    out = dict(cell_type=kind, id="solo-"+key, metadata={}, source=text.splitlines(keepends=True))
    if kind=="code":
        out.update(execution_count=None,outputs=[])
    return out

def material(n):
    if n<=10: return 'tickets.csv, R02.pdf, R03.pdf, R04.txt와 해당 장 수업 예제'
    if n<=19: return '해당 장 SDK·LCEL 수업 예제, questions.csv의 Q01·Q09·Q10과 직접 바꾼 질문'
    if n<=54: return 'documents/ 원문, manifest.csv, questions.csv, chunks.json 및 전날 만든 색인·서비스. 처음 시작하면 공통 자료와 해당 장 수업 예제로 기준선을 만든다.'
    if n<=67 or n in (95,99,100,101): return 'starter/, skills/, reference/stdio_steps.md, policy.py와 해당 장 수업 예제. 실습 후 reference/ 구현으로 결과를 대조한다.'
    if n<=79: return '해당 장 FastAPI·DB·웹 예제, tickets.csv와 가상 정책 질문. 원격 실습은 배정된 수업용 환경을 사용한다.'
    if n<=85: return '자기 투두 저장소와 해당 장 수업 노트북. 중간에 시작하면 81장 참조 앱으로 초기 상태를 만든다.'
    return '자기 프로젝트 최신판·실행 기록. 독립 연습이 필요하면 공통 정책 문서와 reference/policy.py를 작은 서비스의 시작점으로 쓴다.'

def basecode(n):
    if n<=19: return '# 오늘의 수업 예제에서 입력 하나를 골라 아래에 변형한 입력을 작성하세요.'
    if n<=67 or n>=86: return 'case_ids = ["Q01", "Q09", "Q10"]\n# 자기 시나리오의 입력을 정하고, 기대 결과를 실행 전에 적으세요.'
    return '# 오늘의 앱이나 저장소에서 정상 사례와 실패 사례를 하나씩 준비하세요.'

def build_cells(n, title, first, second, check):
    duration = 60 if n in (1,2,8,9,10,43,86,87,88,115,116,117,118,119,120) else 120 if n in (22,25,34,45,55,61,62,66,71,73,74,77,85,106,112,113) else 90
    mins={60:(10,25,15,10),90:(10,40,25,15),120:(15,50,35,20)}[duration]
    cells=[cell("markdown","intro",f"## 개인 실습 {n:03} · {title}\n\n예상 {duration}분. 자료를 준비하고 입력을 예측하는 데 {mins[0]}분, 첫 구현에 {mins[1]}분, 다른 입력과 실패 사례에 {mins[2]}분, 결과를 다시 확인하는 데 {mins[3]}분을 씁니다.\n\n**준비물** {material(n)}\n\n[전체 실습 묶음]({HOST}/daily/all-labs.zip)을 풀고 이 노트북을 daily_resources 옆에 두세요. "+(f"[오늘의 수업 예제]({HOST}/chapter{n:02}/index.html)" if n<=116 else "특강·현장 일정에 맞춰 개별 수행합니다."))]
    if n>1: cells.append(cell("code","input",DATA))
    cells.extend([cell("markdown","part-a","### 1. 구현하기\n\n"+first),cell("code","implementation",START.get(n,basecode(n))),
                  cell("markdown","part-b","### 2. 조건을 바꿔 다시 실행하기\n\n"+second),
                  cell("code","variation","# 첫 실행과 달라진 입력을 적고, 앞에서 만든 함수 또는 서비스를 다시 호출하세요.\n# 코드 밖에서 한 작업은 사용한 파일·버전·관찰값을 이 셀 아래 기록하세요."),
                  cell("markdown","criteria","### 3. 스스로 확인하기\n\n"+check+"\n\n**내 기록**\n\n- 처음 사용한 입력과 기대값\n- 실제 실행 결과와 달랐던 지점\n- 수정한 줄 또는 설정, 다시 실행한 결과")])
    if n in (20,21,22,23,25,33,55,57,58,61,62,63,64,66,67,95,101,118):
        cells.extend([cell("markdown","bench-title","### 기준 구현과 대조하기\n\n자기 구현을 먼저 실행한 뒤 아래 비교 셀을 사용하세요. 검색 도구는 필터에 맞는 조항을 반환합니다. 검색 순위와 자연어 답변은 별도 검사합니다."),
                      cell("code","bench","import sys\nif data_dir.is_dir():\n    sys.path.insert(0, str((data_dir / 'reference').resolve()))\n    from policy import lookup_policy\n    from check_filter import check_filter\n    print(check_filter(lookup_policy))\n    # 자기 함수를 완성한 뒤 check_filter(내_조회함수)로 교체하세요.")])
    if n==22:
        cells.append(cell("markdown","chroma","<details><summary>영속 저장·재개방 예제 펼치기</summary><pre><code>from chroma_lab import open_index, ingest, retrieve, lexical_vectors\ncollection = open_index(index_path)\ningest(collection, chunks, lexical_vectors)\n# 다음 날에는 ingest 없이 같은 경로에서 다시 열어 아래 두 사례를 조회합니다.\ncollection = open_index(index_path)\nfor q in questions[2:4]:\n    print(q['qid'], retrieve(collection, q, lexical_vectors))</code></pre>lexical_vectors는 글자 기반 비교입니다. 실제 의미 임베딩에서는 수업용 모델의 encode 결과를 리스트로 반환하는 함수로 바꾸고 새 컬렉션에 저장하세요. 문서와 질의에는 같은 임베딩 함수를 사용하세요.</details>"))
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
if [int(row[0]) for row in spec]!=list(range(1,121)) or any(len(row)!=5 for row in spec):
    raise ValueError("교육일·실습 필드를 확인하세요")
resources=HERE/"resources.zip"
shutil.copyfile(resources,DAILY/"resources.zip")
links=[]
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
        name=f"day{n:03}.ipynb"
        notebook=dict(nbformat=4,nbformat_minor=5,metadata={"kernelspec":{"name":"python3","language":"python","display_name":"Python 3"}},cells=cells)
        raw=encode(notebook)
        (DAILY/name).write_bytes(raw)
        put(archive,name,raw)
        link=f'<a href="{name}" download>개인 과제 노트북</a>'
        section=f'<section class="lesson-section" id="daily-lab"><h2>개인 실습 · {escape(title)}</h2><p>예상 {duration}분 · {escape(material(n))}</p><ol><li>{escape(first)}</li><li>{escape(second)}</li></ol><p><mark>완료 기준</mark> {escape(check)}</p><p><a href="../daily/{name}" download>오늘의 개인 과제</a> · <a href="../daily/resources.zip" download>공통 실습 자료</a> · <a href="../daily/index.html">전체 과제</a></p></section>'
        if n<=116:
            chapter=OUT/f"chapter{n:02}"
            page=chapter/"index.html"
            source=page.read_text()
            marker='<footer class="lesson-footer">'
            if marker not in source:raise ValueError(page)
            source=source.replace(marker,section+marker,1)
            source=re.sub(r'(<a class="download"[^>]*>.*?</a>)',r'\1<p class="reuse-note"><a href="#daily-lab">오늘의 개인 실습 · '+str(duration)+'분</a></p>',source,count=1,flags=re.S)
            page.write_text(source)
            file=chapter/(chapter.name+".ipynb")
            original=json.loads(file.read_bytes())
            original["cells"].append(cell("markdown","daily-assignment",f"## 개인 실습 · {title} ({duration}분)\n\n1. {first}\n2. {second}\n\n**스스로 확인하기** {check}\n\n[오늘의 개인 실습 노트북]({HOST}/daily/{name}) · [실습 자료 묶음]({HOST}/daily/resources.zip)"))
            file.write_bytes(encode(original))
        lesson=f'<a href="../chapter{n:02}/index.html#daily-lab">수업 교재</a> · ' if n<=116 else ''
        links.append(f'<li id="day{n:03}"><h2>{n}일 · {escape(title)}</h2><p>{duration}분 · {lesson}{link}</p><ol><li>{escape(first)}</li><li>{escape(second)}</li></ol><p><strong>자기점검</strong> {escape(check)}</p></li>')

# Keep the downloadable PDF lab notebook identical to the separately served chapter 20 notebook.
pdf_kit = OUT / "chapter20" / "chapter20-lab.zip"
if pdf_kit.exists():
    with ZipFile(pdf_kit) as previous:
        contents = {name:previous.read(name) for name in previous.namelist()}
    contents["chapter20.ipynb"] = (pdf_kit.parent/"chapter20.ipynb").read_bytes()
    with ZipFile(pdf_kit,"w") as updated:
        for name,raw in contents.items():
            put(updated,name,raw)
docs=' · '.join(f'<a href="{p.relative_to(DAILY).as_posix()}">{p.name}</a>' for p in sorted((DAILY/"daily_resources").rglob("*")) if p.suffix in (".txt",".pdf"))
header='<header><a href="../index.html" style="color:white">전체 교재</a><h1>매일 혼자 풀어 보는 실무 과제</h1><p>교육일별 60·90·120분. 전체 묶음을 풀면 노트북과 공통 자료가 함께 열립니다.</p></header>'
page='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>120일 개인 실습</title><link rel="stylesheet" href="../assets/catalog.css"></head><body>'+header+'<main><p><a href="all-labs.zip" download>120일 노트북과 자료 전체 받기</a> · <a href="resources.zip" download>PDF·텍스트·도구·스킬·MCP 실습 자료만 받기</a></p><p>'+docs+'</p><p>'+ ' · '.join(f'<a href="#day{n:03}">{n}일</a>' for n in [1,20,43,53,68,80,86,117])+'</p><ol style="list-style:none;padding:0">'+"".join(links)+'</ol></main></body></html>'
(DAILY/"index.html").write_text(page)
for index in [OUT/"index.html", OUT/"updates/index.html"]:
    s=index.read_text()
    href='daily/index.html' if index.parent==OUT else '../daily/index.html'
    index.write_text(s.replace('</header>',f'<p><a style="color:white" href="{href}">120일 개인 실습 · 과제와 원본 자료</a></p></header>',1))
