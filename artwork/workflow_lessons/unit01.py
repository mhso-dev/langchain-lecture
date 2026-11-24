"""Reading placements and worked process traces for chapters 1–25."""

PLACEMENTS = {
    1: {
        "reading-setup": "start",
        "reading-environment": "code-7",
        "reading-configuration": "code-8",
        "reading-git": "code-11",
        "reading-review": "recap",
    },
    2: {
        "reading-values": "code-1",
        "reading-text": "code-2",
        "reading-collections": "nb-one-record",
        "reading-control": "code-6",
        "reading-nested": "code-1",
        "reading-json": "code-9",
        "reading-challenge": "code-3",
        "reading-sources": "sources",
    },
    3: {
        "reading-functions": "code-2",
        "reading-contract": "nb-contract",
        "reading-errors": "code-3",
        "reading-boundary": "code-6",
        "reading-tests": "code-4",
        "reading-challenge": "code-7",
        "reading-sources": "sources",
    },
    4: {
        "reading-objects": "code-2",
        "reading-choice": "nb-service",
        "reading-modules": "code-8",
        "reading-entry": "code-9",
        "reading-settings": "nb-imports",
        "reading-verify": "code-3",
        "reading-sources": "sources",
    },
    5: {
        "reading-paths": "nb-save-read",
        "reading-formats": "code-1",
        "reading-table": "code-6",
        "reading-clean": "code-2",
        "reading-duplicates": "code-3",
        "reading-pipeline": "code-7",
        "reading-verification": "nb-save-read",
        "reading-challenge": "code-4",
        "reading-sources": "sources",
    },
    6: {
        "reading-http": "code-1",
        "reading-response": "code-6",
        "reading-contract": "code-7",
        "reading-client": "code-5",
        "reading-mock": "nb-failures",
        "reading-live": "nb-request",
        "reading-verify": "code-3",
        "reading-challenge": "recap",
        "reading-sources": "sources",
    },
    7: {
        "reading-git": "nb-merge-conflict",
        "reading-branch": "code-5",
        "reading-conflict": "code-6",
        "reading-collaboration": "code-4",
        "reading-debug": "code-1",
        "reading-pytest": "code-2",
        "reading-sources": "sources",
    },
    8: {
        "reading-concept": "nb-compare",
        "reading-prepare": "code-3",
        "reading-first": "code-6",
        "reading-second": "code-6",
        "reading-third": "code-6",
        "reading-compare": "nb-choice",
        "reading-repair": "code-4",
        "reading-submit": "code-8",
        "reading-offline": "code-2",
        "reading-sources": "sources",
    },
    9: {
        "reading-baseline": "code-1",
        "reading-elements": "nb-baseline",
        "reading-rewrite": "code-2",
        "reading-examples": "code-6",
        "reading-failure": "code-4",
        "reading-verify": "code-8",
        "reading-version": "nb-versions",
        "reading-review": "recap",
        "reading-sources": "sources",
    },
    10: {
        "reading-scope": "nb-evidence",
        "reading-claims": "code-1",
        "reading-image": "code-5",
        "reading-search": "code-2",
        "reading-ui-api": "start",
        "reading-workflow": "code-6",
        "reading-deliver": "nb-approval",
        "reading-sources": "sources",
    },
    11: {
        "reading-concept": "nb-request-input",
        "reading-setup": "code-2",
        "reading-request": "code-3",
        "reading-response": "code-4",
        "reading-context": "code-1",
        "reading-failures": "code-6",
        "reading-practice": "nb-request-input",
        "reading-sources": "sources",
    },
    12: {
    },
    13: {
        "reading-why": "code-1",
        "reading-flow": "code-3",
        "reading-code": "code-6",
        "reading-run": "code-2",
        "reading-failure": "code-5",
        "reading-loss": "nb-summary",
        "reading-sources": "sources",
    },
    14: {
        "reading-entry": "nb-route",
        "reading-roles": "code-1",
        "reading-routes": "code-4",
        "reading-code": "code-5",
        "reading-run": "code-2",
        "reading-sdk": "nb-classify",
        "reading-edges": "nb-policy",
        "reading-task": "code-6",
        "reading-sources": "sources",
    },
    15: {
        "reading-entry": "nb-schema",
        "reading-concept": "code-1",
        "reading-schema": "code-2",
        "reading-call": "code-4",
        "reading-inspect": "code-5",
        "reading-sdk": "nb-request-item",
        "reading-cases": "nb-observe",
        "reading-task": "code-6",
        "reading-sources": "sources",
    },
    16: {
        "reading-entry": "nb-execute",
        "reading-flow": "code-6",
        "reading-function": "code-1",
        "reading-validate": "code-2",
        "reading-result": "code-3",
        "reading-history": "nb-follow-up",
        "reading-run": "code-7",
        "reading-errors": "code-5",
        "reading-task": "recap",
        "reading-sources": "sources",
    },
    17: {
        "reading-loop": "nb-loop",
        "reading-tools": "code-1",
        "reading-state": "code-2",
        "reading-input": "nb-two-tools",
        "reading-code": "code-3",
        "reading-limits": "code-4",
        "reading-run": "code-3",
        "reading-trace": "code-2",
        "reading-records": "code-6",
        "reading-sources": "sources",
    },
    18: {
        "reading-diagnose": "nb-inspect",
        "reading-paths": "code-2",
        "reading-contract": "nb-repair",
        "reading-implement": "code-3",
        "reading-integrate": "code-5",
        "reading-peer": "code-6",
        "reading-assessment": "nb-explain",
        "reading-handoff": "recap",
        "reading-sources": "sources",
    },
    19: {
        "reading-concept": "nb-chain",
        "reading-prompt": "code-1",
        "reading-model": "code-5",
        "reading-invoke": "code-5",
        "reading-stream": "code-6",
        "reading-types": "code-4",
        "reading-errors": "nb-inputs",
        "reading-task": "code-2",
        "reading-sources": "sources",
    },
    20: {
        "reading-entry": "nb-sources",
        "reading-concept": "code-2",
        "reading-data": "code-1",
        "reading-questions": "code-7",
        "reading-text": "code-4",
        "reading-pdf": "code-6",
        "reading-source-check": "nb-loaders",
        "reading-manifest": "nb-unanswerable",
        "reading-sources": "sources",
    },
    21: {
        "reading-entry": "nb-window",
        "reading-clean": "code-1",
        "reading-concept": "code-2",
        "reading-code": "code-5",
        "reading-run": "code-6",
        "reading-compare": "nb-location",
        "reading-tests": "code-3",
        "reading-handoff": "code-8",
        "reading-sources": "sources",
    },
    22: {
        "reading-entry": "code-1",
        "reading-concept": "nb-dimensions",
        "reading-embedding-contract": "nb-chroma",
        "reading-distance": "code-2",
        "reading-chroma": "code-5",
        "reading-query": "code-6",
        "reading-persist": "code-6",
        "reading-faiss": "code-7",
        "reading-real": "nb-dimensions",
        "reading-troubleshooting": "nb-chroma",
        "reading-task": "nb-faiss",
        "reading-sources": "sources",
    },
    23: {
        "reading-contract": "nb-search",
        "reading-search": "code-1",
        "reading-topk": "code-5",
        "reading-context": "code-6",
        "reading-fixture": "code-2",
        "reading-run": "code-4",
        "reading-limits": "nb-context",
        "reading-sources": "sources",
    },
    24: {
        "reading-entry": "nb-prepare",
        "reading-connect": "code-2",
        "reading-prompt": "code-1",
        "reading-empty": "code-6",
        "reading-citation": "code-3",
        "reading-run": "code-2",
        "reading-questions": "code-4",
        "reading-sources": "sources",
    },
    25: {
        "reading-diagnose": "code-1",
        "reading-data": "code-2",
        "reading-contract": "nb-repair",
        "reading-implement": "code-4",
        "reading-run": "code-3",
        "reading-debug": "nb-baseline",
        "reading-peer": "code-6",
        "reading-finish": "nb-handoff",
        "reading-sources": "sources",
    },
}

# These former asides named instructor-only scripts or described a different exercise.
# Keep the concepts, using objects that are actually available in the student notebook.
TOPIC_COPY = {day: {"reading-sources": None} for day in PLACEMENTS if day not in (1, 12)}

def replace_topics(day, replacements):
    TOPIC_COPY.setdefault(day, {}).update(
        {"reading-" + key: value for key, value in replacements.items()}
    )


replace_topics(3, {
    "errors": ("ValueError를 받는 호출자", "함수 안에서 raise ValueError(...)가 실행되면 그 함수의 나머지 줄은 건너뜁니다. 호출한 쪽의 try 블록에서 예외가 발생한 위치를 찾고, except ValueError가 어떤 메시지를 출력하는지 이어서 읽어 보세요."),
})
replace_topics(5, {
    "challenge": ("ID 중복을 언제 판정할까요?", "시간 칸이 빈 ID 2 행 뒤에 20분이 적힌 ID 2 행이 있습니다. 유효한 시간인지 먼저 검사하면 두 번째 행이 살아남습니다. 어느 순서에서 20분까지 사라지는지 두 행을 직접 따라가 보세요."),
})
replace_topics(7, {
    "debug": ("누적 변수의 마지막 값을 추적하기", "30, 20, 40을 더했는데 40만 남았습니다. total = 0이 언제 실행되는지 세 바퀴에 각각 표시해 보세요. 초기화를 반복문 바깥으로 옮기면 두 번째 바퀴는 첫 번째 바퀴가 남긴 30에서 시작합니다."),
})
replace_topics(8, {
    "concept": ("서비스·모델·대화", "서비스는 질문을 입력하는 화면을 제공하고, 모델은 입력을 바탕으로 답을 생성합니다. 같은 서비스라도 모델이나 이전 대화에 따라 답이 달라질 수 있습니다. 비교하려는 서비스마다 새 대화를 열고 같은 회의록을 넣어 보세요."),
    "prepare": ("비교할 입력과 기준 고정하기", "request에는 요청 문장과 회의록 전문이 함께 들어 있습니다. 각 서비스에 같은 내용을 보내고, 결정 사항·담당자·마감일이 원문과 맞는지 항목별로 기록하세요."),
    "first": ("서비스 응답과 실행일 기록하기", "ChatGPT에서 실행했다면 기록표의 ChatGPT 칸에 사용일과 모델 표시, 받은 문장 한 줄을 옮기세요. ‘하늘’에게 마감일을 부여했다면 회의록에서 이를 뒷받침하는 문장을 찾을 수 있는지 확인하세요."),
    "offline": ("제공된 응답에서 근거 확인하기", "서비스에 접속할 수 없어도 ‘참가비는 무료다’라는 제공 문장을 회의록과 대조할 수 있습니다. ‘아직 합의하지 않았다’는 원문을 찾아 차이를 적고, 출처를 ‘제공 예시’로 표시하세요."),
})
replace_topics(10, {
    "scope": ("공유 가능한 입력 고르기", "예제의 가상 안내문에서 정원과 예약일에 관한 문장만 골라 봅니다. 실제 업무 자료를 사용할 때는 연락처나 계정 정보처럼 이 판단에 필요 없는 부분을 제외하세요."),
    "claims": ("하나의 주장을 하나의 근거와 짝짓기", "한 답에 정원과 예약 가능일이 함께 적혀 있으면 둘을 떼어 확인합니다. 정원을 입증하는 문장을 찾았더라도 예약 가능일까지 확인한 것은 아닙니다."),
    "workflow": ("게시 전에 미확인 주장 인계하기", "검토 요청에는 확인할 주장과 대조한 원문을 함께 적으세요. 예약일을 찾지 못했다면 날짜 칸을 미확인으로 남기면 다음 사람이 확인해야 할 지점을 알 수 있습니다."),
})
replace_topics(11, {
    "failures": ("완료 상태를 확인한 뒤 본문 읽기", "예제의 partial에는 짧은 text가 있지만 status는 incomplete입니다. 미리 받은 글자가 있어도 완성된 답변으로 표시하기 전에는 상태를 확인해야 합니다. 이 셀의 출력은 ‘미완료 응답’입니다."),
})
replace_topics(13, {
    "flow": ("작성 함수로 함께 전달되는 두 값", "분류 함수에는 앞서 만든 summary 하나가 들어갑니다. 작성 함수에는 summary와 category가 모두 필요해 두 값을 JSON 문자열로 묶습니다. 로그의 classify 입력과 write 입력에서 이 차이를 찾아보세요."),
})
replace_topics(14, {
    "entry": ("순차 실행에서 조건부 실행으로", "13장에서는 정상적인 문의가 요약·분류·작성 단계를 모두 거쳤습니다. 여기서는 먼저 route를 판정한 뒤 작성 호출을 할지 결정합니다. technical이면 해당 작성 규칙을 사용하고 clarify이면 추가 질문을 곧바로 반환합니다."),
    "code": ("분류 예외와 정상적인 추가 질문", "분류 함수가 TimeoutError를 내면 reason은 classification_error입니다. 두 분야의 단서가 함께 있어 분류 함수가 clarify를 돌려주면 needs_clarification입니다. 두 경우 모두 writes는 0이지만 원인 기록이 다릅니다."),
})
replace_topics(15, {
    "entry": ("출력 형식과 호출할 함수", "12장의 출력 스키마가 응답 데이터의 모양을 정했다면, 여기서는 get_library_hours가 받을 인자의 모양을 기술합니다. parameters에서 day가 필수인지, 어떤 값을 받을 수 있는지 찾아보세요."),
    "sdk": ("요청의 tools와 응답의 호출 항목", "모델에 전달할 tools 목록에는 이 장의 TOOL처럼 이름·설명·인자 규칙을 담습니다. 모델이 도구를 요청하면 응답 항목에서 name, arguments, call_id를 읽습니다. 이 장의 예제는 준비된 응답 항목을 직접 검사합니다."),
})
replace_topics(16, {
    "entry": ("호출 요청을 실행 함수로 넘기기", "이 장의 call에는 get_library_hours, 문자열 인자, call_1이 있습니다. 이름과 인자를 검사해 주말 시간표를 조회하고, 결과에는 바로 이 call_1을 붙여 원래 요청과 연결합니다."),
    "result": ("function_call_output의 두 층", "reply의 call_id는 바깥 딕셔너리에서 바로 읽습니다. 반면 output에는 성공 여부와 조회 데이터가 JSON 문자열로 들어 있습니다. json.loads(reply['output'])을 거치면 data에서 hours를 꺼낼 수 있습니다."),
    "history": ("질문 뒤에 호출 항목과 결과 붙이기", "history에는 사용자 질문, 모델의 호출 요청, 프로그램이 만든 결과가 차례대로 들어갑니다. 마지막 항목에서 function_call_output을 읽고 같은 call_id의 이전 요청을 찾아 연결해 보세요."),
    "run": ("파이썬 함수의 실제 반환값 확인", "get_library_hours('weekend')는 이 노트북의 가상 시간표를 조회합니다. 10:00~16:00은 함수가 읽어 낸 값입니다. 마지막 셀에서는 이 값을 사용해 한국어 문장을 조립합니다."),
})
replace_topics(17, {
    "input": ("모델 호출 예산과 도구 실행", "한 번의 모델 응답은 도구 요청일 수도 있고 최종 문장일 수도 있습니다. 두 도구 결과를 읽고 최종 문장까지 받으려면 이 예제의 max_calls가 3이어야 합니다."),
    "records": ("같은 호출 ID를 다시 받았을 때", "seen에 c1을 넣고 첫 요청의 ID를 대조하면 True가 나옵니다. 이 셀은 중복 검사 한 가지를 따로 실행합니다. run_script에서도 같은 요청의 재실행을 막으려면 도구를 부르기 전에 이 검사를 연결해야 합니다."),
})
replace_topics(18, {
    "diagnose": ("요청에서 확인할 세 필드", "get_loan_rule 요청 한 건을 놓고 name과 call_id, arguments를 각각 읽어 보세요. 도구에 인자가 없어도 요청을 식별하는 ID는 필요합니다."),
    "integrate": ("검증 결과에서 실행 여부 결정하기", "bad에서는 call_id가 c1이지만 name이 other_lookup입니다. 허용된 이름과 다르면 도구 함수를 호출하지 않습니다. 이후 진단에는 이 요청의 ID와 받은 이름을 함께 남깁니다."),
    "handoff": ("검사할 데이터의 경계", "검사 함수는 전달받은 요청을 읽고 True 또는 False를 돌려줍니다. 요청 원본을 그대로 두면 어떤 필드 때문에 실행을 중단했는지 나중에도 같은 입력으로 대조할 수 있습니다."),
})
replace_topics(20, {
    "entry": ("문서 레코드에서 본문 찾기", "documents[0]은 문서 하나를 나타내는 딕셔너리입니다. text에서 대출 기간을, id와 page에서 이 문장을 다시 찾을 단서를 읽습니다. 이 세 값을 구분해 두면 이후 검색 결과의 근거를 확인할 수 있습니다."),
    "manifest": ("질문과 기대 근거 함께 기록하기", "‘주차 요금은 얼마인가요?’에는 연결할 문서 ID가 없어 expected_document_ids가 빈 목록이고 answerable은 False입니다. 문서에 금액이 없다는 사실을 0원이라는 답으로 바꾸지 마세요."),
})
replace_topics(21, {
    "run": ("원문 끝에서 짧아지는 조각", "원문을 인덱스 16부터 잘라 보면 온점 한 글자가 남습니다. 겹침을 4로 주면 둘째 조각이 12부터 시작해 ‘일입니다.’를 담습니다. 같은 마지막 글자가 두 설정에서 어떤 주변 문맥을 얻는지 비교해 보세요."),
    "handoff": ("원문 ID와 청크 ID 구분", "library-1은 문서 전체, library-1:1은 그 문서에서 잘라낸 조각의 ID입니다. 다음 실험에 넘길 때 원문 ID와 시작·끝 인덱스를 함께 보존하면 조각의 문장을 원문에서 다시 찾을 수 있습니다."),
})
replace_topics(22, {
    "entry": ("문서를 같은 어휘 순서로 변환하기", "terms의 순서는 대출, 휴관, 반납입니다. 세 문서와 질문이 모두 같은 순서로 좌표를 만들기 때문에 첫 좌표끼리, 둘째 좌표끼리 비교할 수 있습니다."),
    "embedding-contract": ("저장 벡터와 질의 벡터의 좌표", "저장할 때와 질의할 때 terms의 순서를 같게 유지하세요. 어휘 순서를 바꾸면 길이가 3으로 같아도 각 숫자의 뜻이 달라집니다. 어휘나 표현 방법을 바꿀 때는 문서 벡터도 다시 계산합니다."),
    "persist": ("같은 디렉터리에서 컬렉션 다시 열기", "두 번째 PersistentClient에 첫 번째 클라이언트와 같은 chroma_folder.name을 전달합니다. 같은 이름의 컬렉션을 다시 열어 검색할 수 있는지 확인하세요. 여기서 선택한 폴더는 TemporaryDirectory가 관리합니다."),
    "faiss": ("FAISS의 결과 위치를 문서로 연결하기", "IndexFlatL2에는 벡터가 입력 순서대로 들어갑니다. positions[0][0]이 0이면 documents[0]의 ID를 읽어 library-1을 얻습니다. 검색 거리는 distances[0][0]에 따로 들어 있습니다."),
    "real": ("어휘 포함 벡터와 학습된 임베딩", "teaching_vector는 어휘가 글자 그대로 들어 있는지만 셉니다. 따라서 뜻이 비슷해도 표현이 다르면 가까운 벡터가 되지 않을 수 있습니다. 학습된 임베딩으로 비교할 때도 같은 모델로 문서와 질문을 모두 변환하세요."),
    "troubleshooting": ("저장소 미실행과 검색 결과 구분", "chromadb가 설치되지 않은 커널에서는 설치 안내 문장이 출력되고 검색은 실행되지 않습니다. 컬렉션을 실제로 연 뒤 후보를 얻지 못한 경우와 구분해 결과를 읽어 보세요."),
})
replace_topics(23, {
    "search": ("질의 번호와 결과 순위 읽기", "raw['ids'][0][0]에서 첫 번째 0은 첫 질의, 두 번째 0은 첫 후보를 뜻합니다. 본문과 메타데이터에서도 같은 두 위치를 골라야 한 문서의 정보가 됩니다."),
    "fixture": ("준비된 결과로 반환 모양 확인하기", "raw는 첫 검색 결과를 미리 담아 둔 딕셔너리입니다. 이 값으로 ID·본문·출처·쪽을 연결하는 코드를 먼저 확인한 뒤, 다음 셀에서 retrieve가 실제 후보 순서를 정하는 과정을 살펴봅니다."),
    "run": ("후보를 거른 뒤 거리순으로 정렬하기", "retrieve는 documents에서 page 조건에 맞는 후보를 고른 뒤 질의와의 제곱 거리, 문서 ID 순으로 정렬하고 앞의 k개를 반환합니다. page=1이면 휴관 문서가 정렬 대상에서 이미 빠집니다."),
})
replace_topics(24, {
    "entry": ("검색 결과를 LCEL 입력으로 바꾸기", "검색 결과인 문서 목록에서 ID·출처·쪽·본문을 묶어 context를 만듭니다. question은 질문 칸에 그대로 넣습니다. 두 입력이 프롬프트의 서로 다른 변수로 들어가는지 확인하세요."),
    "prompt": ("질문과 근거가 들어가는 메시지", "system 메시지에는 ‘다음 근거만 읽고 사용한 ID를 표시하세요.’라는 지시와 context가 들어갑니다. human 메시지에는 question이 들어갑니다. 모델의 답을 받은 뒤에는 인용 ID도 실제 검색 목록과 대조합니다."),
    "run": ("고정 모델을 이용해 연결 확인하기", "FakeListChatModel은 준비된 휴관 안내를 돌려줍니다. 질문·문맥·파서를 연결해 최종 문자열이 나오는지 시험할 수 있습니다. 고정 응답을 사용했으므로 다른 질문에 답하는 능력까지 평가한 결과는 아닙니다."),
    "questions": ("기대 근거와 실제 인용 구분하기", "휴관일 질문의 기준 근거는 library-2입니다. 검색 결과에 이 ID가 있는지, 답변이 실제로 이 ID를 인용했는지 따로 확인하세요. 마지막으로 ‘월요일’이라는 문장이 원문의 내용과 맞는지 읽습니다."),
})
replace_topics(25, {
    "diagnose": ("오류가 처음 생긴 단계 찾기", "휴관일 질문에서 기대 문서는 library-2인데 retrieved에는 library-1이 들어 있습니다. 모델에 보낼 문맥을 만들기 전부터 근거가 바뀌었으므로 먼저 검색 결과를 확인합니다."),
    "data": ("기준 문서와 질문 고정하기", "dev-02의 expected_document_ids에는 휴관일을 담은 library-2가 있습니다. 비교 중에는 질문과 기대 ID를 고정하고, 실제로 받은 문서 ID와 본문을 나란히 읽으세요."),
    "implement": ("검증된 문서에서 문맥 만들기", "prepare_inputs는 먼저 질문과 문서 목록을 각각 검사합니다. 유효한 문서가 있을 때 question과 context 두 키를 돌려줍니다. context에 쪽 번호와 원문 한 줄이 함께 담겼는지 출력에서 확인하세요."),
    "run": ("오류 입력 하나로 쪽 번호 검사", "bad_page는 정상 휴관 문서의 page만 0으로 바꾼 입력입니다. 문서 검사가 ‘페이지는 1 이상의 정수여야 합니다.’를 돌려준다면 검색이나 모델 호출 없이도 잘못된 필드를 찾아낸 것입니다."),
})

def scene(anchor, slug, title, caption, nodes, edges, steps):
    return dict(anchor=anchor, slug=slug, title=title, caption=caption,
                nodes=nodes, edges=edges, steps=steps)


WORKFLOWS = {
    8: [scene("nb-source", "meeting-claim", "‘무료’라는 요약을 원문에서 확인하기",
              "회의록과 요약에 ‘참가비’가 모두 있어도 두 문장이 같은 사실을 말하는지 따로 읽어야 합니다.",
              [('claim','요약 문장'),('search','원문 찾기'),('compare','의미 대조'),('record','판정')],
              [('claim','search'),('search','compare'),('compare','record')],
              [('claim','요약이 주장한 값','참가비는 무료다.','교육용 응답에서 확인할 주장을 한 문장으로 떼어 냅니다.'),
               ('search','검색어','참가비','같은 단어가 있는 회의록의 줄을 찾습니다.'),
               ('compare','원문의 결정 상태','아직 합의하지 않았다.','금액이 정해지지 않아 무료라고 단정할 근거가 없습니다.'),
               ('record','근거에 맞는 기록','참가비 미합의','기록에는 실제로 확인할 수 있는 상태를 적습니다.')])],
    11: [scene("nb-usage","partial-response","응답 조각이 있어도 완료 상태를 먼저 확인하기",
               "partial의 text에는 ‘가상 안’이 남아 있습니다. 상태가 incomplete인 이 실행에서는 미완료 안내가 출력됩니다.",
               [('reply','응답 받기'),('status','status 검사'),('show','본문 표시'),('wait','미완료 안내')],
               [('reply','status'),('status','show'),('status','wait')],
               [('reply','partial.text','가상 안','짧은 본문이 이미 들어 있는 응답을 읽습니다.'),
                ('status','partial.status','incomplete','completed와 다르므로 완성된 본문을 출력하는 분기를 건너뜁니다.'),
                ('wait','print()','미완료 응답','학생이 보는 화면에는 상태 안내가 남습니다.')])],
    12: [scene("langchain-parsers","parser-value","같은 everyone을 두 파서가 다르게 처리하는 이유",
               "StructuredOutputParser에서 통과한 입력을 PydanticOutputParser에 그대로 넣습니다. 이번에는 EventSummary의 Literal 규칙까지 적용됩니다.",
               [('raw','같은 JSON'),('keys','키 확인'),('dict','dict 반환'),('model','모델 검증'),('reject','예외')],
               [('raw','keys'),('keys','dict'),('raw','model'),('model','reject')],
               [('raw','outside_scope','audience = everyone','title과 audience 두 키는 모두 있습니다.'),
                ('model','EventSummary.audience','허용값 adult','PydanticOutputParser는 값까지 모델 규칙과 비교합니다.'),
                ('reject','parse()','OutputParserException','everyone은 허용된 값이 아니어서 모델 인스턴스를 받을 수 없습니다.')])],
    14: [scene("nb-route","classifier-timeout","분류기의 시간 초과는 어느 경로로 돌아올까요?",
               "timed_out을 분류 함수로 넣으면 결제 단서가 있는 질문도 작성 함수까지 도달하지 못합니다. 여기서 clarify의 원인은 classification_error입니다.",
               [('in','질문'),('classify','분류 호출'),('write','작성'),('except','예외 처리'),('return','결과')],
               [('in','classify'),('classify','write'),('classify','except'),('except','return'),('write','return')],
               [('in','question','영수증이 필요합니다','질문에 문자열이 있으므로 입력 검사를 통과합니다.'),
                ('classify','timed_out()','TimeoutError','분류 레이블을 받기 전에 예외가 발생합니다.'),
                ('except','reason','classification_error','예외를 잡은 경로에서 안내를 구성합니다.'),
                ('return','writes','0','작성 함수를 건너뛰고 clarify 경로의 결과를 돌려줍니다.')])],
    15: [scene("nb-request-item","scan-output","같은 output 목록에서 호출 항목만 모으기",
               "inspect_calls는 먼저 type을 확인합니다. message에서 건너뛴 자리에 가짜 호출을 채우지 않고, function_call에서만 이름과 인자를 읽습니다.",
               [('items','항목 순회'),('type','type 확인'),('skip','계속'),('decode','JSON 해석'),('store','호출 추가')],
               [('items','type'),('type','skip'),('skip','items'),('type','decode'),('decode','store')],
               [('type','items[0].type','message','첫 항목은 함수 호출이 아닙니다.'),
                ('skip','calls','[]','continue로 넘어가며 호출 목록은 비어 있습니다.'),
                ('items','items[1]','function_call','이번에는 호출 ID와 arguments가 있는 항목입니다.'),
                ('type','function_call 여부','True','함수 호출이므로 인자를 해석하는 경로로 갑니다.'),
                ('decode','arguments의 day','weekend','JSON 문자열을 딕셔너리로 읽습니다.'),
                ('store','추가한 call_id','call_demo_1','해석한 인자를 이름과 ID에 묶어 호출 목록에 넣습니다.')])],
    16: [scene("nb-id-match","invalid-day","허용하지 않은 요일에도 요청 ID가 남는 이유",
               "day가 Friday인 요청은 조회 함수를 실행하기 전에 걸러집니다. 결과의 ok는 False이지만 바깥 call_id에는 원래 요청 ID가 남습니다.",
               [('call','요청'),('validate','day 검사'),('lookup','시간 조회'),('error','오류 구성'),('output','결과 연결')],
               [('call','validate'),('validate','lookup'),('validate','error'),('lookup','output'),('error','output')],
               [('call','call_id','call_1','기존 요청에서 arguments만 바꾼 복사본입니다.'),
                ('validate','day','Friday','지원하는 weekday와 weekend 어느 쪽에도 일치하지 않습니다.'),
                ('error','error','invalid_tool_request','운영 시간을 조회하는 대신 오류 값을 구성합니다.'),
                ('output','call_id','call_1','오류 결과도 어떤 요청에 답하는지 구별할 수 있습니다.')])],
    17: [scene("nb-loop","last-call","요청 c2가 이력에 있어도 실행 결과가 없는 이유",
               "max_calls를 2로 낮추면 두 번째 모델 응답을 기록한 뒤 상한에 걸립니다. 마지막 이력 항목은 c2의 호출 요청입니다.",
               [('model','모델 응답'),('append','이력 추가'),('budget','예산 확인'),('execute','도구 실행'),('stop','상한 종료')],
               [('model','append'),('append','budget'),('budget','execute'),('execute','model'),('budget','stop')],
               [('model','두 번째 응답','get_loan_rule','첫 요청 c1의 주말 시간은 이미 이력에 있습니다.'),
                ('append','history의 마지막 ID','c2','모델이 요청한 항목을 먼저 history에 추가합니다.'),
                ('budget','number / max_calls','2 / 2','마지막 기회를 사용해 도구 결과를 읽을 다음 모델 호출이 없습니다.'),
                ('stop','status','model_limit','c2를 실행하기 전에 반환하므로 대출 기간 결과는 추가되지 않습니다.')])],
    18: [scene("nb-explain","reject-name","알 수 없는 도구 이름은 인자를 읽기 전에 멈춥니다",
               "name만 other_lookup으로 바꾼 bad의 call_id는 c1으로 유지됩니다. 실패를 기록할 때 어떤 요청에서 이름 검사가 막혔는지 함께 남길 수 있습니다.",
               [('input','요청 받기'),('name','허용 이름'),('id','ID 검사'),('args','인자 검사'),('reject','이름 거부')],
               [('input','name'),('name','id'),('id','args'),('name','reject')],
               [('input','call_id','c1','기존 요청을 복사한 뒤 name만 바꿉니다.'),
                ('name','받은 이름','other_lookup','허용된 get_loan_rule과 다릅니다.'),
                ('reject','allowed','False','이 이름으로 도구를 실행하지 않고 c1의 실패 원인을 기록합니다.')])],
    20: [scene("nb-unanswerable","unanswerable","질문과 근거가 만나는 곳",
               "세 문서는 대출 기간·휴관일·반납함을 설명합니다. 주차 요금을 물었을 때 빈 기대 목록을 쓰는 이유는 자료 안에서 금액을 확인할 수 없기 때문입니다.",
               [('q','주차 질문'),('scope','자료 대조'),('link','근거 연결'),('empty','근거 없음')],
               [('q','scope'),('scope','link'),('scope','empty')],
               [('q','question_id','dev-03','주차 요금이 얼마인지 묻는 문항입니다.'),
                ('scope','문서의 주제','대출 · 휴관 · 반납','세 안내 중 주차 요금을 담은 자료를 찾을 수 없습니다.'),
                ('empty','expected_document_ids','[]','answerable은 False로 기록합니다. 무료라는 뜻이 아닙니다.')])],
    22: [scene("nb-chroma","reopen-collection","다시 연 Chroma 컬렉션에서 원래 쪽 번호 찾기",
               "Chroma가 설치된 커널에서 실행하는 경로입니다. 벡터와 함께 넣어 둔 메타데이터가 재조회 결과에서도 같은 문서를 가리킵니다.",
               [('write','upsert'),('disk','컬렉션'),('open','다시 열기'),('query','query'),('read','첫 후보')],
               [('write','disk'),('disk','open'),('open','query'),('query','read')],
               [('write','레코드 수','3','각 ID와 같은 위치에 본문·벡터·출처를 넣습니다.'),
                ('disk','저장 위치','chroma_folder.name','임시 디렉터리 안에 같은 이름의 컬렉션이 남습니다.'),
                ('open','컬렉션 이름','library_course_v1_e1','새 클라이언트가 같은 경로와 이름으로 기존 데이터를 엽니다.'),
                ('query','query / n_results','[1, 0, 0] / 1','대출 질문에 가까운 후보 하나를 요청합니다.'),
                ('read','첫 ID / 쪽','library-1 / 1','ids와 metadatas에서 똑같이 [0][0] 위치를 읽습니다.')])],
    24: [scene("nb-empty","skip-generator","검색 결과가 비었을 때 생성 호출 수 추적",
               "주차 요금 질문에 no_hits가 빈 목록을 돌려줍니다. 생성기로 넘긴 함수가 무엇이든 이 실행에서는 한 번도 불리지 않습니다.",
               [('q','질문'),('search','검색'),('check','근거 검사'),('generate','답변 생성'),('none','근거 없음')],
               [('q','search'),('search','check'),('check','generate'),('check','none')],
               [('q','question','주차 요금은 얼마인가요?','질문 문자열을 확인한 뒤 검색 함수로 전달합니다.'),
                ('search','no_hits()','[]','검색 함수가 빈 문서 목록을 반환합니다.'),
                ('check','if not docs','True','생성기에 줄 문맥이 없어 바로 반환하는 경로를 택합니다.'),
                ('none','generation_calls','0','status는 no_evidence이고 sources도 빈 목록입니다.')])],
    25: [scene("nb-handoff","baseline-evidence","검색 실패와 올바른 문서를 직접 넣은 결과 구분",
               "같은 dev-02 질문에서 첫 검색 후보와 기대 근거를 대조합니다. 올바른 문서를 손으로 넣어 본 성공은 실제 검색기를 고쳤다는 증거와 구별합니다.",
               [('case','기준 질문'),('found','기존 후보'),('compare','ID 대조'),('inspect','기대 문서'),('record','기록')],
               [('case','found'),('found','compare'),('case','inspect'),('compare','inspect'),('inspect','record')],
               [('case','expected_document_ids','[library-2]','기준 문항은 휴관 요일을 확인해야 합니다.'),
                ('found','retrieved[0].id','library-1','처음 후보는 대출 기간 문서입니다.'),
                ('compare','기대 ID 포함 여부','False','시작부터 다른 근거가 선택되었음을 확인합니다.'),
                ('inspect','hits[0]의 ID / 쪽','library-2 / 2','올바른 문서를 직접 지정해 후속 입력을 점검합니다.'),
                ('record','기대 문서의 본문','도서관은 월요일에 휴관합니다.','수정한 검색기가 같은 문서를 찾아오는지는 별도 실행으로 확인합니다.')])],
}

CASE_COPY = {10: {"flow-8": ("안내문을 게시하기 전 확인할 값", "정원과 예약일을 따로 확인합니다. 좌석 수에 대한 근거만 있으면 참가 정원으로 바꾸어 쓰지 않고, 확정되지 않은 예약일은 검토할 항목에 남깁니다.")}}

replace_topics(3, {
    "challenge": ("숫자가 아닌 문자열 처리하기", "text에 들어 있는 ‘내일’은 int로 바꿀 수 없습니다. parse_minutes(text)를 try 안에서 호출하고 except ValueError에서 사용자가 고쳐야 할 입력을 안내해 보세요."),
})
replace_topics(4, {
    "entry": ("import로 불러온 함수 실행하기", "셀 07에서는 임시 패키지 안에 models와 service 모듈을 둡니다. service가 models의 StudyRecord를 불러와 객체를 만들고, 호출한 쪽에서 제목을 출력합니다. 화면에 나타난 ‘Git 연습’이 어느 객체의 값인지 찾아보세요."),
    "settings": ("패키지 안의 상대 import", "from .models import StudyRecord에서 점 하나는 같은 패키지를 가리킵니다. service 모듈은 클래스 정의를 복사하지 않고 models에 있는 정의를 사용합니다."),
    "verify": ("서로 다른 객체의 상태 확인", "first.mark_done()을 실행한 뒤 first.done과 second.done을 차례로 읽어 보세요. 같은 클래스의 메서드를 사용했지만 완료로 표시된 기록은 first 하나입니다."),
})
replace_topics(5, {
    "clean": ("정수 변환과 유효한 행의 조건", "clean_row는 먼저 제목의 공백을 정리하고 minutes를 int로 바꿉니다. 시간이 빈 문자열이면 변환에서 ValueError가 나서 None을 반환합니다. 정수로 바뀌었더라도 제목이 없거나 시간이 0~480 밖이면 결과에 넣지 않습니다."),
    "pipeline": ("같은 파일에서 UTF-8 JSON 복원", "문자열을 JSON으로 직렬화한 뒤 임시 폴더의 record.json에 씁니다. 같은 경로에서 다시 읽어 json.loads로 복원하면 첫 번째 유효 행의 ‘Python 기초’와 정수 30을 확인할 수 있습니다."),
})
replace_topics(6, {
    "response": ("MockTransport가 돌려준 HTTP 응답", "예제의 missing 함수는 요청을 받으면 상태 404인 httpx.Response를 만듭니다. 클라이언트의 raise_for_status()에서 HTTPStatusError가 발생하며, except 블록에서 error.response.status_code를 읽으면 404입니다."),
    "client": ("HTTP 상태와 JSON 디코딩 따로 확인하기", "서버 상태를 확인하는 raise_for_status()와 본문을 해석하는 json.loads()는 실패 지점이 다릅니다. 점검용 HTML처럼 JSON이 아닌 본문은 JSONDecodeError 경로에서 확인합니다."),
    "verify": ("응답 ID가 원래 요청과 같은지 확인", "이 실습은 1번을 요청했지만 received에는 id가 2인 응답을 넣습니다. 응답 본문을 읽을 수 있어도 다른 번호의 자료일 수 있으므로 받은 id와 todo_id를 직접 대조하세요."),
})
replace_topics(13, {
    "run": ("고정 응답으로 함수 연결 시험하기", "mock_call은 단계 이름으로 미리 저장한 값을 찾아 반환합니다. 입력 문장을 바꾸어도 같은 문자열을 돌려주므로 분류 정확도는 측정할 수 없습니다. 여기서는 요약 반환값이 실제로 다음 호출의 입력에 들어갔는지 로그로 확인합니다."),
})
replace_topics(17, {
    "loop": ("도구를 실행한 뒤의 다음 응답", "주말 시간과 대출 기간을 함께 묻는 질문에 첫 응답은 운영 시간, 둘째 응답은 대출 규칙을 요청합니다. 이 장은 세 모델 응답을 script에 미리 담아 두고, 어떤 입력에서 history가 늘어나거나 루프가 끝나는지 관찰합니다."),
    "tools": ("서로 다른 두 도구의 인자", "get_hours는 day가 weekday 또는 weekend인지 확인한 후 hours를 반환합니다. get_loan_rule은 빈 인자 객체를 받아 loan_days에 14를 넣습니다. 한 도구의 인자 규칙을 다른 도구에 그대로 적용할 수 없습니다."),
    "state": ("도구 요청과 결과가 쌓이는 이력", "history의 첫 항목은 사용자 질문입니다. 그 뒤에는 c1의 호출과 결과가 한 쌍으로 들어 있고, 이어서 c2의 호출과 결과가 추가됩니다. 마지막 결과 안쪽의 loan_days를 읽으면 14입니다."),
    "code": ("응답 종류와 호출 상한 검사 순서", "run_script는 응답 항목을 history에 넣은 뒤 type을 확인합니다. message이면 completed로 끝납니다. 도구 요청이고 이미 max_calls에 도달했다면 model_limit을 반환합니다. 예산이 남을 때만 도구를 실행해 결과를 history에 붙입니다."),
    "limits": ("호출 예산이 3일 때와 2일 때", "max_calls가 3이면 두 도구를 실행한 뒤 세 번째 모델 응답에서 최종 문장을 얻습니다. 2이면 두 번째 요청 c2를 받은 시점에 model_limit을 반환해 c2의 도구 결과는 생성되지 않습니다."),
})
replace_topics(18, {
    "paths": ("빈 인자 객체와 빈 호출 ID", "get_loan_rule은 별도로 받을 인자가 없어 문자열 '{}'를 풀면 빈 딕셔너리가 됩니다. 반면 공백만 있는 call_id는 strip()한 뒤 비어 있으므로 나중에 결과와 짝지을 수 없습니다."),
    "assessment": ("원본 요청의 필드를 하나씩 바꿔 검사", "원본 item에서 도구 이름, 호출 ID, arguments 중 하나만 바꾸어 실행하세요. 어떤 필드가 True를 False로 바꾸었는지 바로 알아볼 수 있습니다. 특히 문자열 'null'과 '{}'를 각각 넣었을 때의 차이를 확인하세요."),
})
replace_topics(19, {
    "stream": ("조각을 도착 순서대로 이어 붙이기", "pieces에는 ‘가상 ’과 ‘안내’ 두 문자열이 들어 있습니다. 빈 문자열로 join하면 첫 조각 끝에 들어 있던 공백을 보존한 ‘가상 안내’가 됩니다. 이 셀은 조각을 다시 합치는 연습으로, 실제 모델이 언제 어떤 길이로 보냈는지는 측정하지 않습니다."),
})
replace_topics(20, {
    "pdf": ("페이지 인덱스와 사람이 읽는 쪽 번호", "PdfReader(pdf).pages[0]은 첫 번째 페이지 객체입니다. 추출 기록의 page에는 사람이 읽는 1쪽을 표시합니다. 이 셀은 글자가 직접 들어 있는 가상 PDF를 읽으며, 스캔 사진 속 글씨를 인식하는 작업은 수행하지 않습니다."),
})
replace_topics(21, {
    "entry": ("원문과 문서 ID 함께 읽기", "doc의 text에는 대출 기간 문장이 있고 id는 library-1입니다. 글자를 자르기 전 원문 ID를 기록해 두면 잘린 문장이 어느 문서에서 나왔는지 거슬러 올라갈 수 있습니다."),
    "code": ("청크의 시작·끝 위치로 원문 복원", "location['start']는 12, end는 원문 길이입니다. text[start:end]로 자른 값이 둘째 청크인 ‘일입니다.’와 같은지 확인해 보세요. end가 가리키는 위치는 결과에 포함되지 않습니다."),
    "tests": ("나란한 청크의 겹친 문자열 확인", "first[-4:]와 second[:4]를 비교합니다. 두 값이 같은 ‘일입니다’이면 네 글자가 보존된 채 두 청크에 중복되어 있음을 확인할 수 있습니다. 두 값의 일치는 검색 품질까지 측정한 결과는 아닙니다."),
})
replace_topics(24, {
    "empty": ("빈 문서 목록에서 생성 생략", "answer_question은 문서 검증 직후 docs가 비었는지 확인합니다. 빈 목록이면 no_evidence와 빈 sources를 바로 반환해 generation_calls가 0이 됩니다. 검색 함수가 예외를 낸 상황과는 다른 경로입니다."),
})
replace_topics(3, {
    "boundary": ("문자열 정리와 화면 출력 분리", "normalize_title은 정리한 문자열을 돌려주고 화면 출력은 호출한 쪽의 print가 맡습니다. 따라서 같은 함수의 반환값을 그대로 표시할 수도 있고, 다른 함수의 인자로 넘길 수도 있습니다."),
})
replace_topics(7, {
    "git": ("두 브랜치가 같은 줄을 바꿨을 때", "브랜치가 갈라진 뒤 서로 같은 줄을 다르게 고치면 Git이 어떤 문장을 남길지 자동으로 정하지 못할 수 있습니다. 이 셀에는 그때 볼 수 있는 충돌 내용을 문자열로 담았습니다."),
    "conflict": ("충돌 마커 안의 두 지시 합치기", "HEAD 쪽 문장은 ‘전체 셀을 실행하세요.’이고 partner 쪽 문장은 ‘새 커널에서 시작하세요.’입니다. 실행 순서를 생각해 새 커널을 먼저 시작하고 전체 셀을 실행하라는 한 문장으로 합치세요. 결과 문장에는 충돌 마커를 넣지 않습니다."),
    "pytest": ("테스트에서 확인할 두 합계", "total_minutes에 세 기록을 넣으면 기대 합계는 90입니다. 빈 목록을 넣었을 때는 0이어야 합니다. 노트북에서 두 결과를 각각 확인하고, 이후 pytest로 옮길 때도 두 입력의 기대값을 따로 적으세요."),
})
replace_topics(14, {
    "sdk": ("명시적 거절과 분류기 오류", "route_request는 ClassificationRefusalError를 만나면 classification_refusal을, 그 밖의 예외를 만나면 classification_error를 반환합니다. 두 경우 모두 작성기를 호출하지 않습니다. 셀의 timed_out은 TimeoutError를 일으켜 두 번째 경로를 보여 줍니다."),
})
replace_topics(15, {
    "call": ("호출 ID와 JSON 인자 문자열", "call의 arguments는 문자열이라 json.loads를 거쳐야 day를 읽을 수 있습니다. call_id는 그대로 남겨 둡니다. 모델이 같은 이름의 함수를 두 번 요청해도 각각의 결과가 원래 요청으로 돌아가려면 ID가 필요합니다."),
})
replace_topics(16, {
    "validate": ("ID와 인자를 거부하는 방법의 차이", "execute_call은 호출 ID가 비어 있으면 ValueError를 일으킵니다. ID가 있어 결과를 연결할 수 있지만 이름이나 day가 잘못됐다면, 호출 ID가 포함된 function_call_output에 invalid_tool_request를 담아 반환합니다."),
})
