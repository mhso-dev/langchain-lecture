"""Notes and execution traces verified against the student notebooks for lessons 55–69."""

# Each row specifies a reading's new position. A row without prose removes a
# duplicate or an instruction involving files that the notebook does not ship.
PLACEMENTS = {}
TOPIC_COPY = {}


def lesson(day, rows):
    placements = {}
    replacements = {}
    for line in rows.strip().splitlines():
        topic, cell, *copy = line.split('|')
        reading = 'reading-' + topic
        placements[reading] = f'cell-{int(cell):02d}'
        replacements[reading] = tuple(copy) if copy else None
    PLACEMENTS[day] = placements
    TOPIC_COPY[day] = replacements


lesson(55, """
start|5|모델과 도구 사이에서 누가 함수를 실행할까?|모델이 내보낸 tool_calls에는 함수 이름과 인자, 요청 ID가 들어갑니다. create_agent는 등록한 Python 함수를 실행하고 그 결과를 대화에 붙여 다시 모델을 부릅니다. 마지막 모델 응답에 도구 요청이 없으면 이번 실행이 끝납니다.
entry|2
environment|5
responsibility|1|요청에서 함수 인자 꺼내기|request 전체에는 이름과 ID도 있습니다. get_hours에 넘기는 값은 request["args"] 안의 day 하나입니다. ID는 결과를 돌려줄 요청을 찾을 때 씁니다.
model|5|같은 도구 요청을 다시 관찰하기|ClassroomModel이 내놓을 세 응답은 코드에 미리 적혀 있습니다. 그래서 노트북을 다시 실행해도 첫 도구는 get_hours, 두 번째 도구는 get_loan_rule입니다. 여기서 비교할 수 있는 것은 실행 순서입니다.
roundtrip|6|tool_call_id로 결과 찾기|첫 번째 ToolMessage의 c1은 주말 시간에 대한 결과를, 두 번째 메시지의 c2는 대출 일수에 대한 결과를 가리킵니다. 도구 두 개를 등록해도 어느 요청의 결과인지 ID로 찾아낼 수 있습니다.
comparison|3|역할별 메시지 세기|roles에서 ai는 세 번, tool은 두 번 나타납니다. 마지막 ai는 두 도구의 결과를 받은 뒤 답변만 쓰기 때문에 ToolMessage가 하나 더 생기지 않습니다.
boundaries|4
task|4
exit|6
""")

lesson(56, """
start|1|실행 전후에 검사할 값|도구를 부르기 전에는 요청한 k가 허용되는지 확인합니다. 답변을 돌려줄 때에는 실제로 찾은 문서와 초안에 적힌 문서가 일치하는지 따로 확인합니다.
entry|1
environment|5
tool|1|양의 정수 k 판별하기|이 함수는 type(value) is int와 1 이상의 값이라는 두 조건을 모두 봅니다. 문자열 "2"는 숫자처럼 보여도 통과하지 않고, True도 bool이므로 통과하지 않습니다.
structured|3|검색 결과에 없는 인용 ID|draft_ids에서 returned_ids를 빼면 검색에서 돌려주지 않은 출처만 남습니다. library-9가 보이면 초안에 등장한 그 ID를 검색 결과에서 확인할 수 없다는 뜻입니다. 문장 자체가 원문과 맞는지는 따로 읽어야 합니다.
context|5
policy|6|도구 요청과 실제 실행 횟수|모델 대본에는 s1과 s2 두 요청이 있지만 run_limit은 1입니다. executed에는 함수 본문에 들어갈 때만 문자열이 추가되므로 ['대출']은 두 번째 검색이 실행되지 않았다는 증거입니다.
failures|4
handoff|6
""")

lesson(57, """
goals|1
entry|3
concept|1|요청·작업 지침·도구를 구분하기|사용자는 지금 해결할 질문을 보냅니다. Skill에는 그 종류의 질문을 반복해서 처리할 때 지킬 절차를 적습니다. 원문을 읽거나 검색하는 동작은 그 절차를 수행하는 코드가 맡습니다.
metadata|2|description에 선택 기준 적기|문서에서 사실을 찾아 답하는 요청과 두 실행 기록을 비교하는 요청은 필요한 입력이 다릅니다. 두 설명을 읽고 어느 쪽에 질문과 원문을 주고, 어느 쪽에 실행 기록 두 개를 줄지 판단할 수 있게 씁니다.
structure|4
answer-skill|3|인용 ID와 원문 수치를 함께 읽기|셀에서 답변에 붙인 library-1은 문서의 위치를 가리킵니다. 그 문서를 열어 대출 기간 14일이 답변과 같은지 확인해야 합니다. 같은 ID를 붙이고 숫자만 999일로 바꾼 문장은 이 대조에서 걸립니다.
comparison-skill|5|비교 가능한 입력 고르기|두 기록의 question_id는 dev-01로 같지만 k는 2와 1입니다. 검색 개수를 다르게 둔 채 호출 수가 달라지면 그 원인을 실행 방식 하나로 설명하기 어렵습니다.
references|3
check|5
write|2
failure|3
handoff|5
""")

lesson(58, """
goals|1
entry|1
disclosure|1|이름으로 본문 하나 열기|chosen에는 Skill 이름만 들어 있습니다. 이 이름에 /SKILL.md를 붙여 files에서 값을 꺼내는 순간에만 선택한 지침이 나옵니다. 다른 Skill의 본문은 그대로 남아 있습니다.
tools|4|load_skill의 인자와 반환값|load_skill("comparison-report")에 넘긴 것은 파일 경로 전체가 아니라 이름입니다. 반환값은 그 이름으로 찾은 본문의 문자열입니다. 이 셀의 files는 파일 읽기를 재현한 딕셔너리입니다.
agent|4
normal|2|읽은 문자 수 합치기|reads에는 본문 2,511자와 참조 자료 1,049자가 별도 항목으로 남아 있습니다. 두 값을 더한 3,560자는 기록에 있는 두 자료의 분량입니다. 아래 짧은 예시 문자열의 len이나 토큰 수와 단위·대상이 다릅니다.
compare-paths|3|참조 파일을 열었는지 확인하기|Skill 본문에 참조 파일 이름이 적힌 것과 실제 읽기 기록에 그 파일이 남은 것은 다른 관찰입니다. reads에서 경로를 키로 찾아 두 번째 동작까지 일어났는지 확인하세요.
comparison|4
policy|3
failure|4
meaning|5|선택한 본문의 분량 비교|마지막 셀은 본문 하나와 두 본문을 줄바꿈으로 합친 문자열의 길이를 비교합니다. 48과 70은 파일 접근 횟수가 아닌 문자열의 글자 수입니다.
practice|5
handoff|5
""")

lesson(59, """
goals|1
entry|2
state|2|원본 이력과 선택한 입력|recent를 만든 뒤에도 turns[0]은 회의실 B라는 문장을 돌려줍니다. 원본에서 예전 발화를 지운 것이 아니라 모델에 전달할 후보를 마지막 두 항목으로 좁혔기 때문입니다.
turns|1
recent|1|마지막 두 발화가 남기는 단서|turns[-2:]에는 제출 기한과 슬라이드 수가 들어갑니다. 이 목록만 읽고 발표 장소를 물으면 회의실 B라는 단서를 찾을 수 없습니다.
summary|3|요약이 잃어버린 사실|요약에는 회의실 B와 한국어가 남았지만 금요일 18시는 빠졌습니다. 원본에서 문자열을 찾을 수 있다는 것과 이번 입력에 그 정보가 들어 있다는 것을 나눠 확인합니다.
budget|4
probe|3
errors|3
practice|4|요약과 최근 발화를 함께 쓰기|장소·언어는 요약에서, 기한·슬라이드 수는 recent에서 확인할 수 있습니다. 두 입력을 이어 붙인 뒤 네 가지 질문에 필요한 단서가 실제로 있는지 찾아보세요.
handoff|4
""")

lesson(60, """
goals|1|대화를 넘어 사용할 설정|language 같은 설정을 다시 쓰려면 누구의 선호인지 함께 저장해야 합니다. 이 셀에서 조회의 기준은 두 값으로 만든 키 ("alice", "language")입니다.
entry|5
roles|1
identity|2|같은 설정 이름과 다른 소유자|alice의 language가 저장되어 있어도 ("bob", "language")는 다른 키입니다. 빈 조회의 None을 다른 사용자의 값으로 채우면 소유자 분리가 깨집니다.
schema|5|복합 기본 키와 조회 조건|PRIMARY KEY(owner, memory_key)는 같은 사용자의 같은 설정이 두 행이 되는 것을 막습니다. SELECT의 WHERE에도 같은 두 열을 써서 같은 이름의 남의 설정을 제외합니다.
crud|3|한 사용자 설정만 수정하기|딕셔너리에서 ("bob", "language")에 값을 대입하면 그 키의 항목만 생기거나 바뀝니다. 삭제할 때도 (사용자, 설정 이름) 두 값을 모두 지정합니다.
conversation|4
local|5
postgres|5
errors|2
handoff|5
""")

lesson(61, """
entry|1
roles|2|도구를 제공하는 쪽과 호출하는 쪽|서버에는 get_library_hours가 등록되어 있습니다. 클라이언트는 세션으로 도구의 명세를 조회하거나 인자를 담아 호출합니다. 이 노트북의 연결은 메모리 안에서 이루어집니다.
local|1|같은 함수의 기준 결과|Python에서 get_library_hours('weekend')를 직접 부르면 10:00~16:00을 읽을 수 있습니다. 뒤의 세션 호출에서 같은 요일이 같은 값을 내는지 비교할 기준입니다.
schema|1
server|1
stdio|2|목록 조회와 실제 호출|list_tools()가 돌려주는 것은 호출 가능한 도구의 명세입니다. 운영 시간을 받으려면 새로 연 세션의 call_tool()에 이름과 day 값을 함께 보냅니다.
result|3|구조화된 필드에서 응답 읽기|reply.structuredContent에서 day와 hours를 각각 읽습니다. 출력 첫 값이 weekend인지 먼저 보면, 다른 요일의 시간을 실수로 주말 응답으로 읽는 일을 피할 수 있습니다.
failures|4
practice|4
protocol-check|2
handoff|4
""")

lesson(62, """
entry|1
environment|4
direct|2|LangChain 도구가 호출하는 MCP 도구|lookup.ainvoke에 weekend를 주면 어댑터가 같은 day를 MCP의 get_library_hours에 보냅니다. Python 쪽 lookup과 서버에서 등록한 도구의 이름은 서로 달라도 됩니다.
adapter|2|응답의 어느 값을 모델에 넘길까?|MCP는 day와 hours 등이 담긴 결과를 돌려줍니다. lookup은 reply.isError를 먼저 확인하고 반환된 day가 요청과 일치할 때에만 hours 문자열을 넘깁니다.
policy|3|정상처럼 보이는 다른 요일의 결과|받은 hours가 그럴듯해도 requested가 weekend이고 받은 day가 weekday이면 해당 요청의 답으로 쓸 수 없습니다. 이 경우 어댑터는 result_day_mismatch로 중단합니다.
session|2|열린 세션의 수명|make_lookup(session)은 도구가 쓸 세션을 기억합니다. 실제 lookup.ainvoke도 async with 블록 안에서 실행해야 합니다. 블록이 끝나면 연결 수명도 끝납니다.
http|1
failures|3
comparison|4|최종 문장과 도구의 반환값|고정 모델의 마지막 답은 ‘조회가 끝났습니다.’입니다. 실제 운영 시간은 요청 hours-1과 짝인 ToolMessage의 content에서 읽습니다.
practice|3
handoff|4
""")

lesson(63, """
entry|1
envelope|2|처리 결과와 답변 상태를 따로 읽기|run_status는 요청 처리가 끝났는지를, result.status는 문서로 답할 수 있었는지를 나타냅니다. 주차 질문은 처리가 끝나도 no_evidence입니다.
owner|2|검색보다 먼저 확인하는 소유자|answer는 owners에서 대화의 소유자를 조회해 전달받은 owner와 비교합니다. 일치하지 않으면 PermissionError가 발생하므로 search가 그 요청의 자료를 읽지 않습니다.
project-data|1|문서 ID와 페이지의 표기|문서의 id는 course-guide-v1:p2이고 page 필드의 값은 1입니다. 코드가 출력하는 정수와 사람이 보는 ID 안의 표기를 그대로 구분해서 읽습니다.
mandatory-search|3|근거가 없을 때의 분기|주차 질문에는 ‘과제’가 없어 search가 빈 리스트를 돌려줍니다. answer는 즉시 sources=[]와 generation_calls=0을 반환합니다. 원문 없이 제출 방법을 추측하는 단계는 없습니다.
limited-agent|2
project-skill|2
feature-choice|1
run-all|3
failure|3
meaning|2|생성 횟수 필드 읽기|이 셀은 문서 한 건이 있으면 f 문자열로 답변을 만들고 generation_calls에 1을 적습니다. 외부 모델의 실제 사용량을 측정한 값은 아닙니다.
practice|3
handoff|3
""")

lesson(64, """
entry|1
read-write|1|문의를 보여 주는 시점과 등록하는 시점|문의 내용은 먼저 상태에 담깁니다. inquiries에 등록되는 줄은 interrupt 뒤에 있습니다. 학생이 문의 내용을 볼 수 있어도 아직 등록 건수는 0일 수 있습니다.
proposal|2|사람에게 보이는 승인 대상|interrupt는 approval_id와 inquiry_text를 담아 호출자에게 돌려줍니다. 호출자는 __interrupt__의 value에서 문구를 읽고 이 문의를 등록할지 판단합니다.
context|3
interrupt|2|confirm에서 멈춘 실행|그래프에는 START → confirm → END가 등록되어 있지만 첫 invoke는 confirm 안에서 중단됩니다. InMemorySaver가 대기 상태를 보관하고, chat-a-demo는 그 상태를 다시 찾을 때 쓰는 thread_id입니다.
resume|3|같은 스레드에서 결정을 전달하기|Command(resume="approve")를 처음과 같은 config로 전달합니다. 중단됐던 confirm 노드는 처음부터 다시 실행되고 interrupt 자리는 이번에 받은 결정을 돌려줍니다. 등록 코드를 그 뒤에 두면 대기 시점에 부작용이 생기지 않습니다.
decline-expiry|4|승인과 거절에서 달라지는 쓰기 횟수|approve 이외의 결정을 받으면 함수는 declined를 바로 반환합니다. 새 문의를 거절했을 때 건수는 거절 직전과 같습니다. 승인 실험을 먼저 했다면 기존 한 건까지 사라지는 것은 아닙니다.
changed-duplicate|3|같은 승인 ID가 가리키는 항목|inquiries.setdefault는 해당 ID가 없을 때만 새 값을 넣습니다. 이 예제의 중복 방지는 현재 커널의 딕셔너리 안에서 같은 키를 다시 쓸 때의 동작입니다.
budgets|4
write-failure|3
all-cases|4
practice|4
handoff|4
""")

lesson(65, """
goals|1
boundaries|1|분류 결과는 다음 단계의 입력|rule_route의 반환값은 billing, technical, clarify 중 한 문자열입니다. 기술 문서를 실제로 읽거나 답변을 제공하는 일은 뒤의 분기와 도구 코드가 맡습니다.
agent|3|선택한 도구를 실행하는 위치|allowed에는 technical_faq가 technical 경로에만 등록되어 있습니다. route가 그 키와 일치할 때 selected.invoke를 호출합니다. 이 실습에서는 Python의 조건문이 도구를 선택합니다.
baselines|2|단서가 섞이면 추가 질문|결제 단서만 있으면 billing이고 기술 단서만 있으면 technical입니다. 두 단서가 함께 있거나 둘 다 없으면 clarify가 됩니다. 단지 먼저 발견된 단어로 결정하지 않습니다.
jev|4|선택 실습의 실제 호출 조건|기본값 run_jev=False에서는 분류 서비스를 호출하지 않습니다. True로 실행해 응답을 받은 경우에만 선택지, 해당 선택지의 확률, confidence를 실제 반환값으로 읽습니다.
connect|3
verify|5|분류가 맞아 보여도 확신도가 낮을 때|과제는 technical과 함께 probability 0.80, confidence 0.49를 제공합니다. 선택지 문자열 하나로 도구를 바로 부르지 말고, 주어진 수용 조건을 둘 다 만족하는지 확인합니다.
project-transfer|3
wrap|5
""")

lesson(66, """
entry|3
roles|1|두 역할 사이의 인계값|evidence_role의 출력은 question·id·text를 담은 딕셔너리입니다. answer_role은 그중 text와 id를 읽어 한 문장으로 묶습니다. 이 셀의 역할은 일반 Python 함수입니다.
conditions|3|같은 단위끼리 호출 수 비교하기|두 관찰값 모두 동일 질문에서 필수 검색을 한 번 수행했습니다. model_calls의 차이와 mandatory_retrieval_calls의 차이를 따로 계산하면 무엇이 늘었는지 알 수 있습니다.
single|3
two-roles|2|질문이 다음 역할까지 같은지 확인하기|인계받은 근거가 다른 질문의 것이라면 형식이 맞아도 답변을 만들 수 없습니다. answer_role을 부르기 전에 handoff["question"]과 원래 질문을 대조합니다.
plan|2
budgets|3|역할이 늘 때 들인 비용|기록에 적힌 모델 호출은 단일 경로에서 2회, 역할 분리 경로에서 4회입니다. 이 셀은 기록의 차이 2를 계산합니다. 두 모델을 새로 호출해 재측정하지는 않습니다.
failure|2
run-all|3
meaning|1
integration|2
practice|3
handoff|3
""")

lesson(67, """
entry|3
scope|3|평가에 실제로 들어가는 기록|observed에는 execution_status가 executed_local인 행만 남습니다. 검색이 실패한 E67-search-error는 실행했으므로 포함하고, E67-memory-unselected는 실행하지 않아 제외합니다.
a1|1
policy|1
approval|3
failure-states|3|실패가 일어난 단계를 보존하기|선택한 행의 failure_stage는 retrieval입니다. 단순히 답변이 없었다고만 적으면 검색 단계에서 실패한 사례와 평가에서 제외한 사례를 나눌 수 없습니다.
before-after|2
regression|2
service-functions|3
selection|3
practice|1|출처 ID와 문장 내용을 따로 대조하기|예측 답변과 원문은 모두 course-guide-v1:p2를 가리키지만 제출 장소가 다릅니다. 답변의 ‘개인 메신저’와 원문의 ‘학습 관리 페이지의 과제함’을 직접 대조해야 이 오류가 보입니다.
handoff|3
""")

lesson(68, """
http|1|POST 요청을 읽는 순서|TestClient는 POST /ask에 JSON 본문을 보냅니다. FastAPI는 먼저 AskRequest로 본문을 검사하고 통과한 모델을 경로 함수 ask에 넘깁니다.
entry|2
request|1|공백 질문과 k 검증|question에 공백만 있으면 strip() 결과가 비어서 검증이 실패합니다. k를 생략하면 2를 쓰고, 보내는 경우에는 1~10 사이의 정수여야 합니다. 문자열 "2"는 StrictInt 검사를 통과하지 않습니다.
response|2|HTTP 200 안의 답변 상태|200은 이 요청에 대한 HTTP 처리가 성공했다는 뜻입니다. 실제 근거를 찾았는지는 result.status와 sources를 보고 판별합니다.
route|2
same-input|2
business|4|유효한 주차 질문과 빈 검색 결과|주차 질문은 유효한 문자열이므로 경로 함수를 호출합니다. 과제 문서에 근거가 없어도 검색 경로는 정상 종료하며, JSON에는 no_evidence와 빈 sources가 담깁니다.
errors|3|검증 실패가 끝나는 지점|공백만 보낸 요청의 422는 검색이 실패했다는 표시가 아닙니다. 입력 모델이 요청을 거부해 서비스 함수 answer에 질문이 전달되지 않았습니다.
practice|4
handoff|4
""")

lesson(69, """
identity|4|대화 조회에 쓰는 수업용 헤더|소유 표에서 chat-a의 값은 course-alice입니다. 경로에 같은 chat-a가 들어 있어도 헤더의 값이 다르면 이 예제는 404를 반환합니다. 이 고정 문자열은 수업용 식별 값입니다.
ownership|1|첫 이벤트보다 앞선 소유자 확인|stream 함수는 먼저 owners.get(cid)의 결과와 요청 헤더를 비교합니다. 여기서 요청이 거절되면 이벤트 생성기에 들어가지 않아 답변 조각이나 대화 이력이 생기지 않습니다.
canonical|1
ask|2
preflight|1
events|2|NDJSON 한 줄과 이벤트 하나|line은 JSON 객체 하나에 줄바꿈을 붙입니다. 응답을 받는 쪽은 iter_lines로 한 줄씩 읽고 json.loads로 복원합니다. 이번 delta는 이미 정해진 답변 전체 한 조각이며 모델 토큰이 아닙니다.
cancellation|3|부분 수신과 저장 여부|partial = events[:2]는 완료한 응답의 앞 두 이벤트만 따로 보는 관찰입니다. 이 목록에 done이 없으므로 화면은 완료를 확인할 수 없습니다. 이 슬라이스가 이미 저장된 history를 취소하지는 않습니다.
failure|2
practice|3
http-check|4
handoff|2|저장한 뒤 보내는 done|서버는 delta를 보낸 다음 history에 질문과 답을 추가하고 done을 보냅니다. 전체 스트림을 끝까지 읽은 셀에서 이력이 한 건인 이유입니다.
""")

WORKFLOWS = {}


def scene(day, cell, slug, title, caption, nodes, edges, steps):
    WORKFLOWS.setdefault(day, []).append({
        'anchor': f'cell-{cell:02d}', 'slug': slug, 'title': title, 'caption': caption,
        'nodes': nodes, 'edges': edges, 'steps': steps,
    })


scene(55, 6, 'tool-id-roundtrip', '같은 모델로 돌아가는 두 도구 요청',
      '두 도구는 차례로 실행됩니다. 결과를 모델에게 돌려줄 때까지 c1과 c2가 각각 어느 요청의 ID인지 따라가세요.',
      [('model', '고정 모델'), ('hours', 'get_hours'), ('loan', 'get_loan_rule'), ('end', '최종 응답')],
      [('model', 'hours'), ('hours', 'model'), ('model', 'loan'), ('loan', 'model'), ('model', 'end')],
      [('model', '첫 요청 ID', 'c1', '주말 운영 시간을 요청합니다.'),
       ('hours', 'c1 반환', '10:00~16:00', 'ToolMessage가 첫 결과를 운반합니다.'),
       ('model', '다음 요청 ID', 'c2', '이번에는 대출 기간을 요청합니다.'),
       ('loan', 'c2 반환', '14', '두 번째 요청과 결과가 연결됩니다.'),
       ('model', '다음 도구 요청 수', '0', '두 값을 이용해 답변을 냅니다.'),
       ('end', '답변의 두 값', '10:00~16:00 · 14일', '도구 호출 루프가 끝났습니다.')])

scene(56, 6, 'tool-budget', 's2가 있어도 검색이 한 번인 이유',
      '모델이 요청을 생성하는 위치와 검색 함수가 executed에 기록하는 위치를 구분해 보세요.',
      [('model', '고정 모델'), ('gate', '호출 한도'), ('tool', '검색 함수'), ('skip', '실행 생략'), ('end', '최종 답변')],
      [('model', 'gate'), ('gate', 'tool'), ('tool', 'model'), ('gate', 'skip'), ('skip', 'end')],
      [('model', '검색 요청', 's1 · 대출', '고정 모델의 첫 번째 요청입니다.'),
       ('gate', '사용한 실행 횟수', '0 / 1', '첫 번째 검색은 한도 안입니다.'),
       ('tool', 'executed', "['대출']", '함수 안에서 질문을 기록합니다.'),
       ('model', '검색 요청', 's2 · 다시 검색', '두 번째 요청도 모델에서 나옵니다.'),
       ('gate', '사용한 실행 횟수', '1 / 1', '이미 이번 실행 한도를 채웠습니다.'),
       ('skip', 'executed', "['대출']", '검색 함수에 다시 진입하지 않습니다.')])

scene(58, 5, 'select-skill-body', '이름 하나로 선택한 본문만 전달하기',
      '같은 files에서 선택한 문자열과 전체 문자열의 길이를 셉니다. len의 단위는 글자입니다.',
      [('files', '두 Skill 본문'), ('pick', 'load_skill'), ('one', '선택 본문'), ('both', '전체 연결')],
      [('files', 'pick'), ('pick', 'one'), ('files', 'both')],
      [('files', '사전의 본문 수', '2', '두 Skill이 서로 다른 지침을 갖습니다.'),
       ('pick', 'name', 'evidence-answer', '이름으로 한 경로를 고릅니다.'),
       ('one', 'len(selected)', '48', '전체를 연결했을 때의 70자와 비교하세요.')])

scene(59, 2, 'history-window', '잘라 낸 입력과 그대로인 대화 기록',
      'recent를 만든 뒤 turns[0]을 읽습니다. 어디에 장소가 남았는지를 따라가세요.',
      [('history', 'turns'), ('slice', '최근 두 문장'), ('prompt', '선택 입력'), ('read', '원본 조회')],
      [('history', 'slice'), ('slice', 'prompt'), ('history', 'read')],
      [('history', '원본 항목', '4개', '장소·언어·기한·분량을 모두 보관합니다.'),
       ('slice', '선택', 'turns[-2:]', '끝의 두 항목을 골라 recent를 만듭니다.'),
       ('prompt', 'recent가 담은 단서', '금요일 18시 · 5장', '장소는 선택 입력에서 빠졌습니다.')])

scene(60, 5, 'owner-key-select', '두 사용자의 language 중 하나만 조회하기',
      'SQLite가 두 조건을 동시에 만족하는 행에서 value를 가져옵니다.',
      [('table', '기억 테이블'), ('filter', 'WHERE 조건'), ('alice', 'alice 행'), ('bob', 'bob 행'), ('value', 'fetchone')],
      [('table', 'filter'), ('filter', 'alice'), ('filter', 'bob'), ('alice', 'value'), ('bob', 'value')],
      [('table', 'language 행', 'alice · bob', '두 행의 memory_key는 같습니다.'),
       ('filter', '매개변수', 'alice · language', '소유자와 설정 이름을 함께 대조합니다.'),
       ('alice', 'value', '한국어', '영어가 적힌 bob 행은 선택하지 않습니다.'),
       ('value', 'row[0]', '한국어', '조회 결과의 첫 열을 출력합니다.')])

scene(61, 3, 'mcp-call', '세션을 통해 MCP 도구의 구조화 결과 받기',
      '이 호출은 노트북 안의 메모리 연결을 사용합니다. 목록 조회 결과인 도구 이름과 실제 호출 결과를 비교하세요.',
      [('client', '클라이언트'), ('session', '열린 세션'), ('server', '등록한 도구'), ('reply', '구조화 결과')],
      [('client', 'session'), ('session', 'server'), ('server', 'reply')],
      [('client', 'day', 'weekend', 'call_tool의 인자로 요일을 보냅니다.'),
       ('session', '도구 이름', 'get_library_hours', '이 이름으로 서버 도구를 호출합니다.'),
       ('server', 'hours[day]', '10:00~16:00', '주말 시간을 사전에서 꺼냅니다.'),
       ('reply', 'day와 hours', 'weekend · 10:00~16:00', '구조화 결과의 두 필드를 읽습니다.')])

scene(62, 4, 'mcp-tool-message', '에이전트의 호출 ID가 MCP 왕복을 마칠 때',
      'MCP가 조회한 시각을 ToolMessage에 넣을 때에는 모델이 발급한 hours-1이 다시 붙습니다. 이 이름은 모델의 요청 ID입니다.',
      [('model', '고정 모델'), ('adapter', 'lookup'), ('server', 'MCP 도구'), ('msg', 'ToolMessage'), ('end', '최종 응답')],
      [('model', 'adapter'), ('adapter', 'server'), ('server', 'adapter'), ('adapter', 'msg'), ('msg', 'model'), ('model', 'end')],
      [('model', 'tool_call_id', 'hours-1', '모델이 평일 시간을 요청합니다.'),
       ('adapter', 'day', 'weekday', '연결된 MCP 세션에 인자를 전달합니다.'),
       ('server', 'hours', '09:00~18:00', '가상 도서관의 평일 시간을 반환합니다.'),
       ('adapter', 'day 대조', 'weekday = weekday', '요청한 요일과 받아 온 요일이 같습니다.'),
       ('msg', '요청 ID · 내용', 'hours-1 · 09:00~18:00', '에이전트 기록에 도구 결과가 추가됩니다.'),
       ('model', '최종 문장', '조회가 끝났습니다.', '조회한 시간은 바로 앞 도구 메시지에도 남습니다.')])

scene(62, 3, 'mcp-check-day', '요일이 어긋나면 시간 전달 중단',
      '과제에서 주어진 받은 값을 어댑터의 검사에 대입해 봅니다. 출력 가능한 문자열도 요청한 요일과 맞아야 합니다.',
      [('request', '요청 요일'), ('received', '받은 결과'), ('check', '요일 대조'), ('ok', '시간 반환'), ('fail', '불일치 오류')],
      [('request', 'received'), ('received', 'check'), ('check', 'ok'), ('check', 'fail')],
      [('request', 'requested', 'weekend', '원래 요청은 주말입니다.'),
       ('received', 'day · hours', 'weekday · 09:00~18:00', '평일의 실제 시각처럼 보입니다.'),
       ('check', 'day 일치', 'False', '시간 필드만 보면 이 오류를 놓칩니다.'),
       ('fail', '오류 코드', 'result_day_mismatch', '어댑터는 hours를 반환하기 전에 멈춥니다.')])

scene(63, 2, 'rag-answered', '소유자 확인을 지나 원문과 인용이 답변이 될 때',
      '이 예제의 answer는 로컬 함수입니다. 답변과 generation_calls 필드를 노트북에서 어떻게 만드는지 보세요.',
      [('owner', '소유자 확인'), ('search', '문서 검색'), ('hit', '근거 선택'), ('none', '근거 없음'), ('result', '응답 반환')],
      [('owner', 'search'), ('search', 'hit'), ('search', 'none'), ('hit', 'result'), ('none', 'result')],
      [('owner', '대화 · 소유자', 'chat-a · alice', '요청한 사람이 대화의 소유자와 같습니다.'),
       ('search', '질문의 검색 단서', '과제', '한 건의 문서를 찾습니다.'),
       ('hit', '문서 ID', 'course-guide-v1:p2', '첫 문서의 본문과 ID를 답변으로 묶습니다.'),
       ('result', '상태 · generation_calls', 'answered · 1', 'sources 목록에도 같은 문서가 남습니다.')])

scene(63, 3, 'rag-no-evidence', '질문이 주차로 바뀌면 검색에서 끝나는 경로',
      '검색이 정상 종료된 빈 결과입니다. 작성 단계에 전달할 자료가 없으므로 답변 생성 횟수는 0입니다.',
      [('owner', '소유자 확인'), ('search', '문서 검색'), ('hit', '근거 선택'), ('none', '근거 없음'), ('result', '응답 반환')],
      [('owner', 'search'), ('search', 'hit'), ('search', 'none'), ('hit', 'result'), ('none', 'result')],
      [('owner', '대화 · 소유자', 'chat-a · alice', '같은 소유자 조건을 통과합니다.'),
       ('search', '질문', '주차는 무료인가요?', '검색 기준인 ‘과제’가 없습니다.'),
       ('none', 'docs', '[]', '빈 목록 분기로 들어가 즉시 응답을 만듭니다.'),
       ('result', '상태 · generation_calls', 'no_evidence · 0', 'run_status는 여전히 completed입니다.')])

scene(64, 2, 'graph-approval-pause', 'START에서 confirm으로 들어가 중단하는 순간',
      '그래프에 등록된 실제 노드는 confirm 한 개입니다. 체크포인트와 사람 확인은 노드 안의 interrupt가 호출자와 만나는 위치를 표시합니다.',
      [('start', 'START'), ('confirm', 'confirm 노드'), ('wait', 'interrupt 대기'), ('end', 'END')],
      [('start', 'confirm'), ('confirm', 'wait'), ('wait', 'confirm'), ('confirm', 'end')],
      [('start', 'approval_id', 'A1', 'chat-a-demo의 첫 입력을 전달합니다.'),
       ('confirm', '검토 문구', '과제 등록 오류를 확인해 주세요.', '등록 함수보다 앞에서 interrupt를 만납니다.'),
       ('wait', 'len(inquiries)', '0', '__interrupt__로 문구를 돌려주고 대기합니다.')])

scene(64, 3, 'graph-approve-resume', '같은 confirm을 다시 실행한 뒤 A1 등록',
      '같은 thread_id로 Command를 보내면 confirm 안의 interrupt가 결정을 반환합니다. 등록은 그 뒤에 한 번 일어납니다.',
      [('wait', '승인 대기'), ('confirm', 'confirm 재실행'), ('decision', 'interrupt 반환'), ('write', '문의 등록'), ('skip', '거절 반환'), ('end', 'END')],
      [('wait', 'confirm'), ('confirm', 'decision'), ('decision', 'write'), ('decision', 'skip'), ('write', 'end'), ('skip', 'end')],
      [('wait', 'thread_id', 'chat-a-demo', 'A1이 대기 중인 실행을 찾습니다.'),
       ('confirm', '재개 입력', 'Command(resume="approve")', 'confirm을 처음부터 다시 실행합니다.'),
       ('decision', 'decision', 'approve', '이제 interrupt가 승인 값을 반환합니다.'),
       ('write', 'inquiries의 새 키', 'A1', 'setdefault가 승인받은 문의를 저장합니다.'),
       ('end', 'status · 총 건수', 'completed · 1', '노드가 종료되어 END에 도착합니다.')])

scene(64, 4, 'graph-decline-resume', '다른 스레드에서 A2를 거절하면',
      '승인 실험의 A1과 거절 과제의 A2는 서로 다른 문의입니다. 이번에는 등록 줄에 닿기 전에 confirm이 반환합니다.',
      [('wait', '승인 대기'), ('confirm', 'confirm 재실행'), ('decision', 'interrupt 반환'), ('write', '문의 등록'), ('skip', '거절 반환'), ('end', 'END')],
      [('wait', 'confirm'), ('confirm', 'decision'), ('decision', 'write'), ('decision', 'skip'), ('write', 'end'), ('skip', 'end')],
      [('wait', 'thread_id', 'chat-decline', '새로 시작한 A2 문의가 대기합니다.'),
       ('confirm', '재개 입력', 'Command(resume="decline")', '이번 스레드의 confirm으로 돌아옵니다.'),
       ('decision', 'decision', 'decline', 'approve와 다르므로 거절 분기로 갑니다.'),
       ('skip', 'status', 'declined', 'setdefault 줄까지 실행하지 않습니다.'),
       ('end', 'A2 in inquiries', 'False', '기존 A1과 별개로 A2의 부재를 확인합니다.')])

scene(65, 3, 'technical-route', '단일 기술 의도에서 허용된 도구로',
      '분류 함수가 반환한 문자열은 답변이 아닙니다. 허용 목록에서 도구를 찾고 invoke를 호출해야 안내 문장이 나옵니다.',
      [('text', '질문'), ('route', 'rule_route'), ('clarify', '추가 질문'), ('tool', 'technical_faq'), ('reply', '도구 결과')],
      [('text', 'route'), ('route', 'clarify'), ('route', 'tool'), ('tool', 'reply')],
      [('text', 'question', 'API 인증 오류가 납니다.', '기술 단서는 있고 결제 단서는 없습니다.'),
       ('route', 'route', 'technical', 'allowed의 technical 목록을 고릅니다.'),
       ('tool', 'selected.name', 'technical_faq', '원래 질문을 query 인자로 넘깁니다.'),
       ('reply', '안내 내용', '키 설정과 실행 환경', '도구가 고정된 401 안내를 반환합니다.')])

scene(65, 2, 'mixed-route', '영수증과 401이 한 질문에 들어오면',
      '각 분야 단서가 한 개 이상일 때 rule_route는 어느 도구도 선택하지 않습니다. 뒤 셀의 분기에서는 이 결과가 추가 질문으로 연결됩니다.',
      [('input', '복합 문의'), ('billing', '결제 검사'), ('tech', '기술 검사'), ('clarify', '추가 질문'), ('tool', '도구 선택')],
      [('input', 'billing'), ('billing', 'tech'), ('tech', 'clarify'), ('tech', 'tool')],
      [('input', '질문 속 단서', '영수증 · 401 오류', '두 분야 단서를 같은 문의에서 읽습니다.'),
       ('billing', 'billing', 'True', '영수증이 결제 단서에 포함됩니다.'),
       ('tech', 'technical', 'True', '401과 오류가 기술 단서에 포함됩니다.'),
       ('clarify', '반환값', 'clarify', '어느 한쪽만 참이라는 조건이 성립하지 않습니다.')])

scene(66, 1, 'evidence-handoff', '두 함수가 같은 근거를 넘기는 위치',
      '이 셀은 모델을 호출하지 않습니다. 근거 함수가 만든 딕셔너리에서 답변 함수가 어떤 값을 이어받는지 볼 수 있습니다.',
      [('input', '질문'), ('lookup', 'evidence_role'), ('handoff', '인계 객체'), ('write', 'answer_role')],
      [('input', 'lookup'), ('lookup', 'handoff'), ('handoff', 'write')],
      [('input', '질문', '과제는 어디에 내나요?', '문자열을 근거 함수에 전달합니다.'),
       ('lookup', '근거 ID', 'course-guide-v1:p2', '같은 객체에 질문과 원문을 넣습니다.'),
       ('handoff', '전달 필드', 'question · id · text', '두 번째 함수의 입력이 됩니다.'),
       ('write', '답변에서 사용한 값', 'text + [id]', '원문과 같은 문서 ID가 한 줄에 남습니다.')])

scene(67, 3, 'observed-cohort', '실패한 실행과 실행하지 않은 항목 나누기',
      '실패했더라도 실제로 실행한 사례는 분모에 남습니다. 평가 행을 고르는 조건을 따라가세요.',
      [('rows', '평가 2행'), ('test', '실행 여부'), ('observed', '관찰 행'), ('omit', '미실행 제외'), ('stage', '실패 단계')],
      [('rows', 'test'), ('test', 'observed'), ('test', 'omit'), ('observed', 'stage')],
      [('rows', '기록 수', '2', '검색 오류와 미선택 항목이 각각 한 행입니다.'),
       ('test', '선택 기준', 'executed_local', 'not_selected인 기억 항목을 제외합니다.'),
       ('observed', 'case_id', 'E67-search-error', '검색 실패는 실제로 실행했으므로 남습니다.'),
       ('stage', 'failure_stage', 'retrieval', '실패한 위치를 함께 출력합니다.')])

scene(68, 3, 'http-validation', '공백 질문이 검색 함수에 닿지 않는 이유',
      '공백 요청과 올바른 요청이 갈라지는 위치는 FastAPI의 본문 검증 단계입니다.',
      [('post', 'POST /ask'), ('check', 'AskRequest'), ('reject', 'HTTP 422'), ('ask', 'ask 함수'), ('service', 'answer 함수')],
      [('post', 'check'), ('check', 'reject'), ('check', 'ask'), ('ask', 'service')],
      [('post', 'question', '"   "', '본문에 공백 세 개가 들어 있습니다.'),
       ('check', 'value.strip()', '""', '검증 함수가 빈 질문을 거부합니다.'),
       ('reject', '응답 상태', '422', 'ask와 answer는 호출되지 않습니다.')])

scene(69, 2, 'ndjson-commit', 'delta 이후 이력을 저장하고 done 전송하기',
      '클라이언트가 본 답변 조각, 서버에 생긴 대화 한 건, 완료 신호의 순서를 확인하세요.',
      [('owner', '소유자 확인'), ('start', 'start 전송'), ('delta', 'delta 전송'), ('save', 'history 추가'), ('done', 'done 전송')],
      [('owner', 'start'), ('start', 'delta'), ('delta', 'save'), ('save', 'done')],
      [('owner', 'X-Course-Token', 'course-alice', 'chat-a의 소유자와 같습니다.'),
       ('start', 'request_id', 'demo-1', 'llm_token_stream은 False입니다.'),
       ('delta', 'text', '과제함에 제출하세요.', '수신자에게 답변 한 조각이 도착합니다.'),
       ('save', 'len(history["chat-a"])', '1', '서버가 질문과 답변을 한 쌍으로 넣습니다.'),
       ('done', '수신한 이벤트', 'start · delta · done', '수신자가 완료 신호를 확인합니다.')])

scene(69, 4, 'stream-owner-denied', '다른 사용자라면 start를 보내기 전에 중단',
      'course-bob이 chat-a를 요청한 과제의 경로입니다. 404는 NDJSON의 오류 행이 아니라 HTTP 응답입니다.',
      [('request', '스트림 요청'), ('owner', '소유자 조회'), ('reject', 'HTTP 404'), ('stream', '이벤트 시작')],
      [('request', 'owner'), ('owner', 'reject'), ('owner', 'stream')],
      [('request', '헤더', 'course-bob', '요청 경로의 대화는 chat-a입니다.'),
       ('owner', '요청한 대화의 소유자', 'course-alice', '표의 값이 헤더와 일치하지 않습니다.'),
       ('reject', 'status_code', '404', '이 요청에서는 첫 start조차 보내지 않습니다.')])


CASE_COPY = {
    57: {'flow-9': ('설명에서 필요한 입력 찾기',
                    'evidence-answer에는 답할 질문과 판단의 근거가 될 문서를 줍니다. comparison-report에는 비교할 두 실행 기록을 줍니다. 같은 dev-01이어도 k=2인 행과 k=1인 행은 검색 조건이 다릅니다.')},
    58: {'flow-7': ('Skill 이름, 선택한 본문, 읽기 기록',
                    'chosen 값 evidence-answer로 files에서 지정한 본문을 찾습니다. 본문에는 references/source-check.md를 읽으라는 지시가 있습니다. 그 파일을 실제로 읽었는지 확인하려면 별도 자료인 reads에서 그 경로를 찾으세요. 본문에 경로가 등장하는 것만으로는 읽었다고 판단할 수 없습니다.')},
    61: {'flow-6': ('메모리 세션에서 조회할 수 있는 두 결과',
                    '셀 02의 세션에서 list_tools()가 반환한 첫 명세의 이름은 get_library_hours입니다. 셀 03에서는 새 메모리 세션을 열고 같은 이름과 day="weekend"를 call_tool에 보냅니다. 이번에는 도구 명세 대신 weekend와 10:00~16:00이 담긴 structuredContent를 읽습니다.')},
    63: {'flow-5': ('소유자 확인 뒤에 나뉘는 검색 경로',
                    'answer는 대화 소유자가 다르면 search를 호출하기 전에 PermissionError를 냅니다. alice가 chat-a에서 과제 질문을 하면 문서 course-guide-v1:p2를 담아 answered를 반환합니다. 같은 대화에 주차 질문을 보내면 빈 검색 결과에서 즉시 no_evidence와 generation_calls=0을 반환합니다.')},
    64: {'flow-6': ('A1 승인과 A2 거절의 결과 읽기',
                    'chat-a-demo에서 A1을 보낸 첫 invoke는 문의 문구를 돌려주고 멈춥니다. 등록은 0건입니다. 같은 config에 Command(resume="approve")를 전달하면 confirm 노드가 재실행되고 A1이 저장됩니다. 별도의 chat-decline에서 A2를 거절하면 declined가 반환되며 A2는 inquiries에 없습니다.')},
    66: {'flow-5': ('역할 사이에 전달되는 딕셔너리',
                    'evidence_role은 질문·문서 ID·원문을 한 객체에 넣고 answer_role은 그중 text와 id로 답을 만듭니다. 두 함수는 모델을 호출하지 않습니다. 뒤의 model_calls 2회와 4회는 셀에 따로 제공한 두 경로의 관찰 기록입니다.')},
    67: {'flow-5': ('답변 오류와 실행 오류는 어떻게 다른가?',
                    '첫 셀은 답이 만들어졌어도 원문과 제출 장소가 어긋날 수 있음을 보여줍니다. 마지막 셀에서 E67-search-error는 실제로 실행했지만 retrieval에서 실패한 사례입니다. 답변이 틀린 경우, 검색에서 실패한 경우, 아직 실행하지 않은 경우를 나누어 평가하세요.')},
}
