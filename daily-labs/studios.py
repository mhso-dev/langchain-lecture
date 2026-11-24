"""Student-facing work orders and starter inputs for independent practice."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def records(name):
    with (ROOT/name).open(encoding="utf-8") as stream:
        return list(csv.reader(stream, delimiter="|",quoting=csv.QUOTE_NONE))

NOTES = {int(n): (goal, method, probe) for name in ('field_notes.txt','middle.txt')
         for n,goal,method,probe in records(name)}

SHIFT = """shift = read_table("cases/shift.csv")
print(len(shift), shift[0])
print([r for r in shift if r['ticket'] == 'D01'])"""
STARTERS = {
    2: SHIFT + "\ncurrent, seen = {}, set()\n# event 중복을 검사한 뒤 유효 사건만 current[ticket]에 반영하세요.",
    3: SHIFT + "\nfor line, row in enumerate(shift, start=2):\n    if row['event'] in ('E15','E19'):\n        print(line, repr(row['minutes']))",
    4: SHIFT + "\ntraces = {key:[r for r in shift if r['ticket']==key] for key in ('D01','D02')}\nprint(traces['D02'])",
    5: SHIFT + "\noutput_dir = Path('handoff')\noutput_dir.mkdir(exist_ok=True)\n# csv.DictWriter로 파일마다 고정 열 이름과 머리글을 씁니다.",
    6: """import httpx
ids = ['D07','D08','D10','D11','D13']
attempts = dict.fromkeys(ids, 0)
def respond(request):
    ticket = request.url.path.split('/')[-1]
    attempts[ticket] += 1
    if ticket == 'D07' and attempts[ticket] == 1:
        raise httpx.ReadTimeout('교육용 일시 지연', request=request)
    if ticket == 'D08':
        return httpx.Response(404)
    return httpx.Response(200,json={'ticket': ticket,'owner':'야간지원'})
client = httpx.Client(base_url='https://desk.example',transport=httpx.MockTransport(respond))
# 여기서 각 ID를 조회하는 배치를 작성하고 마지막에 client.close()를 호출하세요.""",
    7: SHIFT + "\nprint((data_dir/'cases'/'shift_reference.py').resolve())\n# 이 파일을 임시 Git 저장소에 복사한 뒤 D02를 대상으로 실패하는 테스트를 작성합니다.",
    53: """import sqlite3
db = sqlite3.connect(':memory:')
db.execute('CREATE TABLE tickets(request_id TEXT, branch TEXT, audience TEXT, topic TEXT, status TEXT, minutes INTEGER)')
db.executemany('INSERT INTO tickets VALUES (?,?,?,?,?,?)',[(r['request_id'],r['branch'],r['audience'],r['topic'],r['status'],int(r['minutes'])) for r in tickets])
print(db.execute('SELECT request_id,count(*) FROM tickets GROUP BY request_id').fetchall())
# SQLite에서 집계 SQL을 검산한 후 수업 DB의 임시 테이블에서도 같은 결과를 확인하세요.""",
    54: """import sqlite3
db_path = Path('training-transactions.sqlite')
changes = [('A','접수','완료'),('B','접수','보류')]
print(db_path.resolve(),changes)
# requests와 audit에 서로 다른 기본 키를 정하고 첫 쓰기와 감사 INSERT를 한 트랜잭션으로 묶으세요.""",
    59: """turns = [('seoul-june','서울','2026-06-30'),('busan','부산','2026-07-01'),('seoul-june','','')]
for thread,branch,day in turns:
    print(thread, branch or '후속 질문', day)""",
    60: """sessions = [('A','a-1','서울'),('B','b-1','부산'),('A','a-2',None)]
# 마지막 세션에서 A의 기본 지점을 복원한 뒤 수정·삭제하고 B를 다시 조회하세요.
print(sessions)""",
    61: """import sys, shutil
sys.path.insert(0,str((data_dir/'reference').resolve()))
from mcp_client import sample
my_dir = Path('my-policy-server').resolve()
my_dir.mkdir(exist_ok=True)
for path in (data_dir/'starter').glob('*.py'):
    target = my_dir/path.name
    if not target.exists():
        shutil.copy2(path,target)
server = my_dir/'my_server.py'
source_data = (data_dir/'chunks.json').resolve()
print(server, source_data)
# my_policy.py에서 source_data에 해당하는 실제 경로의 JSON을 읽고 my_server.py에 함수를 등록하세요.""",
    62: """request = dict(branch='서울', audience='개인', as_of='2026-07-01', topic='receipt')
http_cases = [request, dict(request,branch='제주')]
# 62장 with_http_session의 서버를 내 정책 서버로 바꾸고 두 요청을 session.call_tool에 전달하세요.""",
    63: """by_id = {r['qid']:r for r in questions}
handoffs = [(key,{k:by_id[key][k] for k in ('branch','audience','as_of','topic')}) for key in ('Q06','Q01')]
print(handoffs)""",
    64: """decisions = [('reissue-1','approve','서울'),('reissue-2','reject','부산'),('reissue-3','edit','부산'),('reissue-1','approve','서울')]
# 승인·거절·편집·재전송에 서로 다른 thread_id를 쓰되 업무 ID는 위 값을 보존하세요.
print(decisions)""",
    65: """cases = ['영수증은 며칠 보나요?', '정산 파일은요?', '영수증이랑 정산 시간 둘 다요', '언제 나오나요?']
# 사례 열 개를 채우고 기대 경로를 작성한 뒤 라우터 반환값과 비교하세요.""",
    67: """faults = ['wrong_skill','skip_tool','stale_revision','empty_search']
report = []
# 장애 하나당 하나의 요청을 실행하고 최초 실패 단계·기대값·관찰값을 report에 추가하세요.""",
    68: """body = dict(branch='서울',audience='개인',topic='receipt',as_of='2026-09-01')
payloads = [body,dict(body,branch='제주'),{k:v for k,v in body.items() if k!='branch'}]
print(payloads)""",
    69: """sessions = {'window-A':'req-a','window-B':'req-b'}
events = {'req-a':[],'req-b':[]}
# A에서는 첫 근거를 받은 후 소비를 중단하고 B의 마지막 event를 수집하세요.""",
    70: """files = [('opening.txt',b'weekday 09:00'),('copy.txt',b'weekday 09:00'),('empty.txt',b'')]
# 업로드 응답의 ID와 상태 조회가 같은 업무를 가리키는지 기록하세요.""",
    71: """image_tags = ['desk:working','desk:broken-entry']
probe_request = next(r['question'] for r in questions if r['qid']=='Q01')
print(image_tags,probe_request)""",
    72: """projects = ['desk-persist','desk-empty']
test_id = 'volume-check-01'
# 첫 스택에서 쓴 ID를 서비스 재생성 뒤 두 스택에서 각각 조회하세요.""",
    73: """for q in questions:
    if q['qid'] in ('Q06','Q07'):
        print(q['branch'], q['as_of'], q['question'])
# 검색 SQL에는 정답 열을 전달하지 않습니다.""",
    74: """deployment_record = dict(image_tag='',container_id='',internal_health='',public_response='')
print(next(r['question'] for r in questions if r['qid']=='Q01'))""",
    75: """before_backup, after_backup = 'training-restore-A','training-restore-B'
# A를 저장한 시점에 백업하고 이후 B를 추가합니다. 새 대상 DB에서 각각 조회하세요.""",
    76: """boundaries = [('2026-06-30','R01-1'),('2026-07-01','R02-1')]
# 두 기대값으로 실제 조회 함수의 반환값을 검사하는 테스트를 작성하세요.""",
    77: """release_checks = [('health',200),('Q01','R02-1')]
# 후보판과 복구판에 같은 요청을 보내 각각 실제 응답을 남기세요.""",
    78: """screens = {'empty':[], 'normal':['같은 이름의 업무 '*5,'같은 이름의 업무 '*5], 'loading':None,'failed':'조회 실패'}
print(screens)""",
    79: """actions = ['추가 두 번 클릭','지연 후 정상 응답','서버 실패','재시도']
# 각 동작에서 개발자 도구 Network의 요청 수, 서버 ID, 화면에 남은 행 수를 기록하세요.""",
}
def starter(day, existing):
    if day in STARTERS:
        return STARTERS[day]
    if day in existing:
        return existing[day]
    if day in (26,27,28,29,30,31,32,34,36,37,38,39,40,41,42):
        return """inputs = [{k:v for k,v in q.items() if k not in ('gold_chunk','key')} for q in questions]
print(inputs[0])
# 이 장에서 만든 파이프라인에 업무 입력을 전달하고 변형 실행의 첫 차이를 기록하세요."""
    goal,method,probe = NOTES[day]
    return '# '+goal+'\n# '+method

def variation(day):
    if day == 61:
        return """request = dict(branch='서울', audience='개인', as_of='2026-07-01', topic='receipt')
# 내 서버에 도구를 등록한 뒤 아래 함수 호출의 주석을 풀어 검사하세요.
async def verify_my_server(server):
    for branch, expected in [('서울','ok'),('제주','no_evidence'),('','clarify')]:
        names, reply = await sample(dict(request,branch=branch), server)
        assert 'lookup_policy' in names and reply['status'] == expected, (names,reply)
        if branch == '서울':
            assert reply['items'][0]['chunk_id'] == 'R02-1'
        print(branch or '(누락)',reply['status'])
# await verify_my_server(server)"""
    if day in (2,3,4,5):
        return """from copy import deepcopy
changed = deepcopy(shift)
changed = [r for r in changed if r['event'] != 'E14']
# 같은 구현에 shift, changed를 각각 넣으세요. D01의 마지막 사건이 달라졌습니다.
print([(r['event'],r['kind']) for r in changed if r['ticket']=='D01'])"""
    if day == 85:
        return """from hashlib import sha256
def work_files():
    return {name:sha256((repo/name).read_bytes()).hexdigest()
            for name in ('todo.py','tasks.json','test_todo.py')}
# 거절 요청을 보내기 직전에 before = work_files() 를 실행하세요.
# 거절한 뒤 assert work_files() == before 로 확인하세요. hook-events.jsonl은 별도로 읽습니다."""
    return '# '+NOTES[day][2]+'\n# 실험 조건, 예상값, 실제 반환값과 근거 파일을 아래에 기록하세요.'
