"""Each entry is a reading, an executable example, and an observation beside its output."""
from textwrap import dedent

def lesson(title, reading, code, observation):
    return title, reading, dedent(code).strip(), observation

HAND = """from pathlib import Path
import csv
from pypdf import PdfReader
source = Path('daily_resources/handbook')
pdf = PdfReader(source / 'operations.pdf')
pages = list(csv.DictReader((source / 'pages.csv').open(encoding='utf-8')))
def page_text(n):
    return pdf.pages[n - 1].extract_text()
"""
INIT = """from pathlib import Path
import sys, json, shutil, subprocess
kit = Path('daily_resources/codex-kit').resolve()
repo = Path('my-codex-desk').resolve()
repo.mkdir(exist_ok=True)
def create_file(relative, content):
    target = repo / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        target.write_text(content, encoding='utf-8')
    return target
"""
AGENT = """from pathlib import Path
import sys
for folder in ('reference','agent-lab'):
    root = Path('daily_resources', folder).resolve()
    if str(root) not in sys.path: sys.path.insert(0, str(root))
from approval import make_desk
from tempfile import TemporaryDirectory
from langgraph.types import Command
import sqlite3
"""
HOOK = {"hooks":{"SessionStart":[{"hooks":[{"type":"command","command":"""python3 "$(git rev-parse --show-toplevel)/session_event.py" """ .strip()}]}]}}
SKILL = """---
name: todo-change
description: 할 일 완료나 삭제가 잘못된 ID에 적용되는 결함을 재현하고 수정할 때 사용한다.
---
1. 동명 항목 두 개를 준비하고 선택한 ID와 유지할 ID를 적는다.
2. 작업 폴더에서 python -m unittest -v 로 실패한 검사를 확인한다.
3. 변경 후 같은 검사와 기존 행을 확인한다. 실행 결과와 바뀐 파일을 남긴다.
"""
ROLE = '''name = "case_reader"
description = "동명 항목의 상태 변화와 실패 테스트를 읽어 인계한다."
sandbox_mode = "read-only"
developer_instructions = """
파일 편집 없이 tasks.json과 test_todo.py를 읽는다.
선택한 ID, 보존할 ID, 기대 상태 및 근거 파일을 반환한다.
테스트를 실행하지 않았다면 그렇게 적는다.
"""
'''
def codex(title, reading, body, output):
    return lesson(title, reading, INIT + body, output)

READINGS = {
20:lesson('36쪽 원문에서 검색 가능한 단위 만들기','운영 편람에는 정책과 업무 일지가 한 파일에 섞여 있다. PDF 전체에 서울이라는 태그를 붙이면 부산 조항도 서울 검색에 들어간다. PDF의 물리적 쪽 번호와 대장의 쪽 번호를 먼저 맞춘다.',HAND+"""records = [{**meta, 'text':page_text(int(meta['page']))} for meta in pages]
print(len(records), records[6]['branch'], records[21]['kind'])
print(records[21]['text'][:180])""",'36개 중 7쪽은 서울 정책이고 22쪽은 제주 교육 자료다. 제주라는 단어가 검색돼도 정책의 존재를 뜻하지 않는다. 직접 25쪽의 표도 추출해서 열의 순서가 보존되는지 확인한다.'),
21:lesson('쪽 단위 메타데이터를 조각마다 상속하기','헤더와 푸터는 모든 쪽에 나오고, 시각과 숫자는 표에서도 여러 번 나타난다. 검색에 넣는 문자열과 학생에게 보여 줄 원문 위치를 따로 보관한다.',HAND+"""n = 7
text = page_text(n)
start = text.index('서울 개인 앱에서는')
chunk = {'page':n, 'offset':start, 'text':text[start:start+95], **{'kind':pages[n-1]['kind']}}
print(chunk)
assert page_text(n)[start:start+95] == chunk['text']""",'offset은 직접 추출한 이 페이지 문자열 안의 위치다. 줄바꿈을 지우고 다시 만든 문자열에서 얻은 위치를 원문에 그대로 적용하면 인용이 어긋날 수 있다. 다음 조각에는 문단 경계와 겹침 길이를 직접 정한다.'),
22:lesson('검색 범위를 먼저 좁힌 뒤 상위 후보 찾기','날짜 양 끝을 포함한 지점·대상·문서 종류 필터를 만든다. 표시용 날짜를 YYYY-MM-DD로 통일했으므로 이 자료에서는 문자열 순서와 날짜 순서가 일치한다.',HAND+"""def eligible(row, branch, audience, as_of):
    return (row['kind']=='정책' and row['branch']==branch and row['audience']==audience
            and row['valid_from'] <= as_of <= row['valid_to'])
for date in ('2026-06-30','2026-07-01'):
    print(date,[r['page'] for r in pages if eligible(r,'서울','개인',date)])""",'6월 30일에는 1쪽, 7월 1일에는 7쪽이 남는다. 같은 필드를 Chroma 청크에 저장하고 날짜를 정수로 바꿔 필터를 적용한다. 벡터 검색의 반환 ID가 같은 쪽으로 연결되는지 확인한다.'),
23:lesson('단어가 정확히 일치해도 근거가 될 수 없는 경우','제주 초안에는 열람 기한의 후보 숫자가 인쇄돼 있다. 필터 적용 전후 같은 질의의 후보를 열어 문서의 종류를 읽는다.',HAND+"""for row in pages:
    if row['branch']=='제주':
        print(row['page'],row['kind'],'90일' in page_text(int(row['page'])))""",'22쪽에서 True가 나온다. 조회 대상에는 맞지만 초안이므로 정책 필터를 적용하면 후보는 0개다. 검색 결과가 비었을 때 정책을 추정하지 않고 보류하는 분기를 구현한다.'),
24:lesson('답의 숫자와 근거 쪽을 함께 검산하기','같은 90이라는 숫자는 서울 개인 정책, 행사 사진 보관, 창고 재고에 등장한다. 학생이 만든 답변에 문서명과 한 쪽의 근거 문장을 같이 표시한다.',HAND+"""for n in (7,8,23):
    print(n,pages[n-1]['kind'],next((s for s in page_text(n).splitlines() if '90' in s),''))""",'7쪽의 단위는 열람 일수, 8쪽은 행사 사진 보관 일수, 23쪽은 재고 롤이다. 숫자만 맞았을 때도 오답으로 잡으려면 응답의 근거 쪽과 원문을 기록해야 한다.'),
25:lesson('부분 개정 뒤 과거·현행 질문을 함께 검사하기','대전의 변경 공지는 시간표만 바꾼다. 구판을 통째로 버렸을 때 놓치는 업무 절차가 있는지 세 질문으로 확인한다.',HAND+"""for n in (14,15,17):
    print(n,pages[n-1]['valid_from'],pages[n-1]['valid_to'],page_text(n).splitlines()[1])""",'연말 시간 질문은 14쪽, 연초 시간 질문은 17쪽, 행 수 불일치 질문은 두 기간 모두 15쪽이다. 별도 텍스트 공지를 색인에 추가하고 편람과 공지에서 같은 판정을 얻는지 확인한다.'),
35:lesson('긴 편람으로 검색 전후를 채점하기','evaluation.csv는 채점할 때만 연다. 먼저 B01~B10에 대한 자기 검색 결과를 만든 뒤, 근거 없는 B10은 보류 항목으로 따로 집계한다.',HAND+"""gold = list(csv.DictReader((source/'evaluation.csv').open(encoding='utf-8')))
print([(r['case_id'],r['page'] or '보류') for r in gold[-4:]])""",'B07·B08은 날짜 경계, B09는 유지된 조항, B10은 자료 없음이다. 검색 설정 한 가지를 바꾸고 답 있는 9개 중 정답 쪽이 top 3에 있는 비율과 B10의 보류 성공 여부를 각각 기록한다.'),
55:lesson('create_agent가 실제로 도구를 실행한 지점','한 번의 에이전트 실행에도 모델의 호출 제안, 도구의 반환, 최종 메시지가 따로 남는다. 고정 모델로 호출 순서를 고정한 뒤 ToolMessage와 tool_call_id가 어디서 생기는지 본다.',AGENT+"""from roles import ClassroomModel
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_core.messages import AIMessage
@tool
def read_case(case_id: str) -> str:
    \"\"\"접수 번호의 가상 상태를 조회한다.\"\"\"
    return '접수' if case_id == 'T01' else '없음'
ask = AIMessage(content='',tool_calls=[dict(name='read_case',args={'case_id':'T01'},id='call1')])
agent = create_agent(ClassroomModel(responses=[ask,AIMessage(content='조회 종료')]),tools=[read_case])
messages = agent.invoke({'messages':[('user','T01 상태')]})['messages']
print([(m.type,getattr(m,'tool_call_id',None),m.content) for m in messages])""",'tool 메시지의 call1이 앞선 모델 제안과 짝을 이룬다. 도구 인수를 T99로 바꾸고 어떤 메시지만 달라지는지 예측한다. 실모델로 바꿀 때는 고정 응답 대신 실제 선택 여부를 이 기록으로 확인한다.'),
56:lesson('하네스에서 도구 호출 상한을 적용하기','호출 횟수는 실제 도구에 진입하기 직전에 센다. 모델이 같은 요청을 반복해도 한 요청의 예산 안에서 끝나야 한다.',"""def budgeted(limit):
    trace = []
    def dispatch(tool, value):
        if len([e for e in trace if e == 'executed']) >= limit:
            trace.append('blocked')
            return '한도 도달'
        trace.append('executed')
        return tool(value)
    return dispatch, trace
call, trace = budgeted(1)
print(call(str.upper, 'desk'), call(str.upper, 'desk'), trace)""",'첫 호출만 실행된다. 새 문의에 새 dispatch를 만들고, 실패한 실제 호출도 예산을 쓰도록 유지한다. create_agent의 도구 래퍼에 연결해 재시도 횟수와 차단 사유를 따로 남긴다.'),
64:lesson('create_agent 도구의 승인·수정·거절','쓰기가 일어나기 전에 사람이 제안을 확인한다. 메모리 체크포인터는 이 프로세스에서만 유지된다. 같은 에이전트와 thread_id로 재개하고 DB는 별도로 조회한다.',AGENT+"""temp = TemporaryDirectory()
db = Path(temp.name)/'desk.sqlite'
def saved():
    with sqlite3.connect(db) as conn:
        return conn.execute('SELECT id, branch FROM desk ORDER BY id').fetchall()
def pause(number, branch, thread):
    agent = make_desk(db, number, branch)
    cfg = {'configurable':{'thread_id':thread}}
    result = agent.invoke({'messages':[('user','가상 자료 재발급')]},cfg)
    print(result['__interrupt__'][0].value['action_requests'][0]['args'],saved())
    return agent,cfg
desk,cfg = pause('D1','서울','review-1')
decision = {'type':'edit','edited_action':{'name':'register','args':{'request_id':'D1','branch':'부산'}}}
reply = desk.invoke(Command(resume={'decisions':[decision]}),cfg)
print(saved())""",'일시정지 시에는 빈 목록, 수정 승인 후에는 D1·부산 한 행이다. 새 thread로 D2를 거절하고 D1·부산을 다시 승인한 뒤 행 수를 예상한다. D1·서울로 재접수하면 ToolMessage의 conflict와 보존된 행을 함께 확인한다.'),
66:lesson('서브에이전트의 인계 데이터 바꿔보기','조회와 검토는 서로 다른 create_agent 그래프다. 검토 역할에는 원 요청과 인용 ID를 준다. 다른 지점이나 만료된 근거가 넘어오면 부모는 답변을 보류한다.',AGENT+"""from roles import run_roles
request = dict(branch='서울',audience='개인',as_of='2026-07-01',topic='receipt')
for evidence in (None,['R01-1']):
    result = run_roles(request,evidence)
    print(result['status'],result['trace'])""",'자동 조회는 accepted, 구판을 인계하면 hold가 된다. 두 결과 모두 조회·검토 도구를 호출했는지 trace를 확인하고, 부모가 근거를 바꿀 때 어느 역할에서 처음 오류를 감지하는지 설명한다.'),
67:lesson('승인 대기와 도구 장애를 구별하는 회귀 검사','하네스의 회귀 표에는 예상 상태와 쓰기 횟수를 함께 둔다. 단순히 최종 응답이 왔다는 조건으로는 거절 뒤의 잘못된 저장을 잡을 수 없다.',AGENT+"""temp = TemporaryDirectory()
db = Path(temp.name)/'audit.sqlite'
for i,kind in enumerate(['reject','approve','approve']):
    app = make_desk(db,'CASE-7','서울')
    cfg = {'configurable':{'thread_id':f'run-{i}'}}
    app.invoke({'messages':[('user','가상 접수')]},cfg)
    app.invoke(Command(resume={'decisions':[{'type':kind}]}),cfg)
    with sqlite3.connect(db) as conn:
        print(kind,conn.execute('SELECT count(*) FROM desk').fetchone()[0])""",'거절 0건, 승인 1건, 중복 승인 뒤에도 1건이다. 조회 실패와 운영자 거절의 재시도 조건을 학생이 각각 정의하고, 변경 전후에 같은 표를 다시 실행한다.'),
}
READINGS.update({
80:codex('내 Codex 작업 저장소와 실패 기준 만들기','WSL 또는 macOS에서 노트북과 daily_resources를 같은 폴더에 둔다. 이 셀은 그 옆에 수업용 Git 저장소를 만든다. 빈 저장소에서 시작하려면 다른 폴더에 실습 묶음을 푼다. 노트북의 Python과 Codex를 같은 운영체제 안에서 사용한다.',"""subprocess.run(['git','init','-q'],cwd=repo,check=True)
for name in ('tasks.json','todo.py','test_todo.py'):
    create_file(name,(kit/name).read_text(encoding='utf-8'))
create_file('AGENTS.md','동명 항목을 ID로 구분한다. 변경 전에 재현하고 변경 뒤 같은 테스트를 실행한다.\\n')
baseline = subprocess.run([sys.executable,'-m','unittest','-v'],cwd=repo,capture_output=True,text=True)
print(repo,baseline.returncode,baseline.stderr[-550:])""",'시작 테스트는 ID 2 대신 ID 1이 완료되어 실패한다. 터미널에서 출력된 경로로 이동해 codex를 열고 “파일을 고치기 전에 두 ID의 기대·실제 상태를 설명해 줘”라고 요청한다. 학생이 직접 세 번째 동명 항목 조건을 AGENTS.md에 추가한다.'),
81:codex('Codex가 발견할 프로젝트 스킬 작성하기','80일 저장소를 연다. 언제 이 작업 절차를 읽어야 하는지는 description에 쓰고, 테스트 순서는 본문에 쓴다. 아래 초안을 만든 뒤 누락된 ID의 기대 동작과 학생 자신의 회귀 기준을 본문에 직접 추가한다.',
"skill = create_file('.agents/skills/todo-change/SKILL.md',"+repr(SKILL)+")\nprint(skill.read_text())",
'저장소 루트에서 새 Codex 세션을 열어 “$todo-change 동명 항목 완료 결함을 재현만 해줘”라고 요청한다. 테스트 이름과 실패한 ID를 기록한다. 이어 평범한 문서 제목 변경 요청을 보내 스킬을 언제 명시해야 하는지 비교한다.'),
82:codex('세션 시작 훅을 설치하고 실제 이벤트 구별하기','훅은 이벤트가 발생할 때 프로그램이 호출한다. 함수만 수동 실행해서 얻은 로그와 새 Codex 세션이 남긴 로그를 따로 관찰한다. 명령이 가리키는 스크립트를 읽고 이 저장소에서 사용할 훅 정의를 검토한다.',
"create_file('session_event.py',(kit/'session_event.py').read_text())\nconfig = "+repr(HOOK)+"\ncreate_file('.codex/hooks.json',json.dumps(config,indent=2))\nsubprocess.run([sys.executable,'session_event.py'],cwd=repo,input=json.dumps({'hook_event_name':'SessionStart','source':'fixture'}),text=True,check=True)\nprint((repo/'hook-events.jsonl').read_text().splitlines()[-1])",
'fixture 한 줄은 수동 시험이다. 프로젝트 루트에서 로컬 codex를 열고 /hooks에서 명령과 경로를 확인해 해당 정의를 신뢰한다. 종료 후 새 세션을 열어 fixture와 다른 source를 가진 새 행을 찾는다. 내 훅에서 기록할 필드를 하나 바꾸고 새 세션으로 다시 확인한다.'),
83:codex('읽기 전용 서브에이전트에 오류 재현을 위임하기','부모는 수정 권한과 통합 테스트를 맡는다. 자식은 파일을 읽어 입력·기대 상태·근거 위치만 돌려준다. 세션을 열기 전에 학생이 인계 지침에 “실제 상태”와 그 증거를 추가한다.',
"role = create_file('.codex/agents/case_reader.toml',"+repr(ROLE)+")\nprint(role.read_text())",
'새 Codex 세션에서 “case_reader 서브에이전트를 실제로 호출해 ID 2의 기대값과 근거 파일을 받아. 인계를 받을 때까지 수정하지 마”라고 요청한다. 자식 실행 기록과 반환값을 확인한다. 부모가 직접 같은 설명을 쓴 경우와 구별한다. 인계 후 부모에게 todo.py 한 파일만 고치게 하고 80일 테스트를 다시 돌린다.'),
84:codex('자기 MCP 서버를 Codex 도구 목록에 등록하기','노트북 커널에 mcp 패키지가 있어야 한다. 제공된 get_task를 읽고 반환값에 요청한 ID를 직접 추가한다. 수업용 config.toml이 이미 있다면 아래 출력의 서버 블록만 기존 파일에 합친다. TOML 문자열 경로를 절대 경로로 생성하므로 공백이 있는 폴더에서도 동작한다.',"""for name in ('catalog_server.py','probe.py'):
    create_file(name,(kit/name).read_text())
block = '[mcp_servers.todo_catalog]\\ncommand = '+json.dumps(sys.executable,ensure_ascii=False)+'\\nargs = ['+json.dumps(str(repo/'catalog_server.py'),ensure_ascii=False)+']\\n'
create_file('.codex/config.toml',block)
print(block)
print(subprocess.run([sys.executable,'probe.py'],cwd=repo,capture_output=True,text=True,check=True).stdout)""",
'프로토콜 검사에서 get_task, 2 found, 999 missing이 보인다. 저장소를 신뢰한 로컬 Codex의 새 세션에서 /mcp로 todo_catalog를 확인한다. “등록한 MCP 도구로 2번과 999번을 각각 조회해”라고 요청하고 실제 호출 기록을 연다. 파일을 직접 읽어 답한 경우에는 MCP 연결 검사를 통과한 것으로 세지 않는다.'),
85:codex('내 하네스로 변경 요청을 처음부터 끝까지 처리하기','80~84일 저장소를 같은 폴더에서 연다. 업무 요청은 “동명 항목이 세 개일 때 3번만 완료한다”이다. 학생이 새 실패 테스트와 스킬의 완료 기준을 먼저 작성한 뒤 Codex에 요청한다. 입력 예시가 바뀌어도 역할·도구·훅이 실제로 작동하는지 확인한다.',"""tasks_path = repo/'tasks.json'
if tasks_path.is_file():
    items = json.loads(tasks_path.read_text(encoding='utf-8'))
    if not any(row['id'] == 3 for row in items):
        items.append(dict(id=3,title=items[0]['title'],done=False))
        tasks_path.write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding='utf-8')
    print('작업 원본 ID', [row['id'] for row in items])
expected = ['AGENTS.md','.agents/skills/todo-change/SKILL.md','.codex/hooks.json',
            '.codex/agents/case_reader.toml','.codex/config.toml','test_todo.py']
print('준비할 파일', [p for p in expected if not (repo/p).is_file()])
if (repo/'test_todo.py').exists():
    run = subprocess.run([sys.executable,'-m','unittest','-v'],cwd=repo,capture_output=True,text=True)
    print(run.stderr)""",
'새 세션의 훅 기록, $todo-change 선택, case_reader 인계, get_task의 기존 ID 조회, 부모의 변경 diff와 회귀 테스트를 한 요청에 연결한다. 승인자 역할은 학생이다. 학생이 변경 계획을 읽고 적용을 승인한 뒤 진행한다. 거절할 요청에서는 먼저 작업 파일 세 개의 내용을 저장하고 거절 후 동일한지 검사한다. 세션 훅 이벤트는 별도로 증가할 수 있다. 이 대화상 승인과 64일의 프로그램 수준 쓰기 차단은 서로 다른 보장이다.'),
})
LINKS = {55:'https://docs.langchain.com/oss/python/langchain/agents',64:'https://docs.langchain.com/oss/python/langchain/human-in-the-loop',81:'https://developers.openai.com/codex/skills',82:'https://developers.openai.com/codex/hooks',83:'https://developers.openai.com/codex/subagents',84:'https://developers.openai.com/codex/mcp'}
CHARTS = {64:'''flowchart TD
  P["쓰기 도구 제안"] --> I{"사람의 결정"}
  I -->|거절| R["저장 없이 종료"]
  I -->|인자 수정| E["수정한 인자"]
  I -->|승인| W["요청 ID로 저장"]
  E --> W
  W --> C{"기존 ID와 일치"}
  C -->|다른 내용| H["충돌 반환"]
  C -->|신규 또는 동일| A["접수 한 건"]''',85:'''flowchart TD
  S["세션 시작 훅"] --> P["부모가 스킬 선택"]
  P --> D["서브에이전트 재현 보고"]
  P --> M["MCP로 업무 ID 조회"]
  D --> G{"학생이 계획 확인"}
  M --> G
  G -->|승인| T["부모 수정 후 테스트"]
  G -->|거절| N["수정 없이 종료"]'''}

# Keep the baseline runnable without a model download. Chroma receives explicit vectors.
heading, reading, program, observation = READINGS[22]
READINGS[22] = heading,reading,program+"""
from importlib.util import find_spec
if find_spec("chromadb"):
    import chromadb
    import sys
    sys.path.insert(0,str(Path("daily_resources/reference").resolve()))
    from chroma_lab import lexical_vectors, day_number
    client = chromadb.PersistentClient(path="handbook-chroma")
    collection = client.get_or_create_collection("handbook_pages_v1")
    texts = [page_text(int(r['page'])) for r in pages]
    metadata = [dict(page=int(r['page']),branch=r['branch'],audience=r['audience'],kind=r['kind'],
                     start=day_number(r['valid_from']),end=day_number(r['valid_to'])) for r in pages]
    collection.upsert(ids=[f"HB-{r['page']}" for r in pages],documents=texts,
                      embeddings=lexical_vectors(texts),metadatas=metadata)
    where={'$and':[{'kind':'정책'},{'branch':'서울'},{'audience':'개인'},
                   {'start':{'$lte':20260701}},{'end':{'$gte':20260701}}]}
    result=collection.query(query_embeddings=lexical_vectors(["영수증 열람 기한"]),where=where,n_results=1)
    print(result['ids'])
else:
    print("영속 벡터 검색은 수업의 chromadb·scikit-learn 환경에서 실행하세요.")
""",observation+" 제공한 벡터는 글자 n-gram 기준선이다. 21일에 직접 나눈 조각과 수업 임베딩을 새 컬렉션에 넣고 같은 질문으로 비교한다."
heading, reading, program, observation = READINGS[35]
READINGS[35] = heading,reading,program+"""
from collections import Counter
from math import sqrt
def grams(s):
    return Counter(s[i:i+2] for i in range(len(s)-1))
vectors=[grams(page_text(int(r['page']))) for r in pages]
def search(q, filtered):
    query=grams(q['question'])
    candidates=[]
    for r,v in zip(pages,vectors):
        if filtered and not (r['kind']=='정책' and r['branch']==q['branch'] and
            r['audience']==q['audience'] and r['valid_from']<=q['as_of']<=r['valid_to']):
            continue
        score=sum(count*v[t] for t,count in query.items())/sqrt(sum(k*k for k in v.values()) or 1)
        candidates.append((score,int(r['page'])))
    return [page for _,page in sorted(candidates,reverse=True)[:3]]
for q in gold:
    inputs={k:q[k] for k in ('question','branch','audience','as_of')}
    print(q['case_id'],search(inputs,False),search(inputs,True),'기대',q['page'] or '보류')
""",observation+" 출력 왼쪽은 어휘 유사도 기준선, 오른쪽은 메타데이터를 적용한 순위다. 같은 후보라도 질문이 바뀌면 유사도와 순서가 달라진다."
