"""Cell-level reading and workflow plans for the LangGraph sequence, chapters 26–34."""


def placements(*groups):
    return {
        'reading-' + topic: anchor
        for anchor, topics in groups
        for topic in topics.split()
    }


PLACEMENTS = {
    26: placements(('nb-three-fields', 'concept'), ('code-1', 'state'), ('code-2', 'nodes'),
                   ('code-3', 'edges observe')),
    27: placements(('code-1', 'branch setup'), ('code-2', 'attempts graph'),
                   ('code-3', 'trace'), ('code-4', 'limit assignment handoff')),
    28: placements(('code-1', 'messages schema'), ('code-2', 'node run'),
                   ('code-3', 'ids practice handoff')),
    29: placements(('code-1', 'roles setup compile'), ('code-2', 'send'),
                   ('code-3', 'observe practice handoff')),
    30: placements(('code-1', 'contract state-bridge chroma'), ('code-2', 'nodes'),
                   ('code-3', 'failures')),
    31: placements(('code-1', 'states setup'), ('code-2', 'search'),
                   ('code-3', 'sources practice')),
    32: placements(('code-1', 'contract lcel'), ('code-2', 'graph'),
                   ('code-3', 'trace practice')),
    33: placements(('code-1', 'entry environment spec wrap'), ('code-2', 'request counts'),
                   ('code-3', 'message roundtrip empty errors citations handoff sources')),
    34: placements(('code-1', 'routing entry state environment'), ('code-2', 'baseline compare'),
                   ('code-3', 'normal nodes failure'), ('code-4', 'limit errors troubleshooting handoff sources')),
}

# Missing entries retain the relevant original topic, including its example table.
# None removes obsolete instructions about files and APIs outside the student notebook.
TOPIC_COPY = {
    26: {
        'reading-observe': ('노드 반환값과 invoke()의 최종 상태',
                          'normalize(initial)은 question 한 칸을 돌려줍니다. graph.invoke(initial)은 세 노드를 거친 뒤 question·documents·answer를 모두 돌려줍니다. 셀 03에서 마지막에 선택한 키는 answer입니다. 휴관 문서 자체를 확인할 때는 documents를 읽습니다.'),
    },
    27: {
        'reading-setup': None,
        'reading-assignment': ('분기 하나를 바꾼 뒤 비교할 세 입력',
                             '대출 기간?, 책을 빌리는 기간?, 주차장은?을 각각 실행하면 즉시 성공, 재작성 후 성공, 두 번째 검색 후 종료를 구별할 수 있습니다. 종료 안내가 맞아도 검색 횟수가 예상과 다르면 route의 조건 순서를 다시 보세요.'),
        'reading-handoff': None,
    },
    28: {
        'reading-ids': ('같은 ID를 주었을 때 목록 길이 예측하기',
                      'initial에는 h1 한 개가 있습니다. 그 발화를 반납 질문으로 정정하려면 같은 h1을 붙입니다. 내용만 똑같이 쓰고 다른 ID를 주면 add_messages는 별개의 발화로 처리합니다.'),
        'reading-handoff': None,
    },
    29: {
        'reading-setup': None,
        'reading-observe': ('두 번째 대화가 읽는 기록',
                          'graph를 그대로 두고 config의 thread_id만 B로 바꾸세요. A의 두 질문을 보관한 저장소를 공유해도 B가 시작하는 메시지 목록에는 그 질문들이 없습니다. 출력의 사용자 발화 수로 구별할 수 있습니다.'),
        'reading-handoff': None,
    },
    30: {
        'reading-contract': ('retrieve(question, k)의 반환값',
                           '검색에 쓰는 세 낱말은 대출·휴관·반납입니다. 하나도 들어 있지 않으면 빈 리스트를 돌려줍니다. 일치하는 낱말이 있으면 거리와 문서 ID로 정렬한 뒤 앞의 k개를 반환합니다. 셀 01은 k=1의 첫 레코드를 출력합니다.'),
        'reading-state-bridge': ('문장에 출처와 쪽 번호를 함께 보관하기',
                               '26장에서는 documents의 원소가 문자열이었습니다. 여기서는 한 문서를 id·text·source·page 네 필드로 받습니다. 답변에는 text를 쓰고, 어떤 자료의 몇 쪽인지 확인할 때는 같은 레코드에서 source와 page를 읽습니다.'),
        'reading-nodes': ('검색 노드가 쓰는 필드와 답변 노드가 읽는 필드',
                        'search_node는 documents만 반환합니다. 다음 compose 노드는 그 목록에서 첫 문서의 text를 꺼내 answer를 씁니다. 마지막 print에서 page를 읽을 수 있는 이유는 검색 노드가 넘긴 문서가 결과 상태에 남기 때문입니다.'),
        'reading-chroma': None,
        'reading-failures': ('검색에 성공했지만 근거가 없을 때',
                           '주차 질문에는 자료의 세 낱말이 없습니다. search가 빈 리스트를 기록해도 고정 간선은 compose로 이어집니다. compose가 빈 리스트를 읽고 안내를 씁니다. 다음 장에서는 검색 함수가 예외를 낸 경우와 비교합니다.'),
    },
    31: {
        'reading-states': ('정상 반환과 예외를 나누는 기준',
                         '주차 질문은 검색을 마친 뒤 빈 리스트를 돌려줍니다. 검색 시간이 초과되면 함수는 리스트를 반환하기 전에 멈춥니다. 두 경우를 모두 근거 없음으로 처리하면 검색 서비스를 복구해야 하는 순간을 놓칩니다.'),
        'reading-setup': None,
        'reading-search': ('TimeoutError가 전달되는 위치',
                          'slow_search는 대출 질문을 받아도 자료를 돌려주지 못합니다. 실행은 except TimeoutError로 이동합니다. 이 셀이 출력하는 것은 예외 이름과 메시지입니다. 재검색이나 답변 생성은 이 코드에서 실행되지 않습니다.'),
        'reading-sources': ('이번 요청에서 받은 문서 ID 집합',
                           '대출 질문으로 찾은 레코드에서 id를 하나씩 꺼내 집합을 만듭니다. 답변의 인용 ID는 이번 집합과 대조해야 합니다. 도서관 자료 전체에 존재하는 ID라도 이번에 검색하지 않은 문서를 가리킬 수 있습니다.'),
        'reading-practice': ('ID 대조 다음에 확인할 문장',
                            '인용 ID가 일치하면 해당 문서가 검색되었다는 사실을 확인할 수 있습니다. 답변이 대출 기간을 999일이라고 썼다면 올바른 ID가 붙어 있어도 원문의 14일과 어긋납니다. 마지막에는 답변과 해당 문장의 뜻을 대조하세요.'),
    },
    32: {
        'reading-contract': ('같은 입력과 같은 검색 함수로 비교하기',
                           '두 구현 모두 대출 질문, 같은 세 문서, k=1에서 출발합니다. search_change는 documents 한 칸을, answer_change는 answer 한 칸을 반환합니다. 이 두 변경분을 누가 기존 상태와 합치는지 따라가 보세요.'),
        'reading-lcel': ('LCEL 래퍼에서 기존 키를 보존하는 위치',
                       '파이프 오른쪽은 왼쪽이 반환한 값을 그대로 받습니다. 각 RunnableLambda에서 {**state, **변경분}을 돌려주므로 이전 question과 documents가 다음 단계에도 들어갑니다.'),
        'reading-graph': ('StateGraph가 노드 변경분을 반영하는 위치',
                         'graph_search가 반환한 documents가 공유 상태에 합쳐진 뒤 compose가 실행됩니다. compose가 answer만 반환해도 최종 상태에는 검색한 문서가 남습니다. 셀 02는 답과 문서 ID를 두 구현에서 나란히 확인합니다.'),
        'reading-trace': ('stream_mode="updates"의 첫 항목',
                         'next()로 꺼낸 첫 갱신은 search라는 노드 이름 아래 documents를 담고 있습니다. 이 시점의 library-1은 검색의 반환값입니다. invoke가 끝난 뒤 받는 전체 상태와 구별해 읽으세요.'),
        'reading-practice': None,
    },
    33: {
        'reading-entry': ('필수 검색에서 호출 가능한 도구로',
                        '앞 장의 검색 함수는 고정된 순서에서 실행됐습니다. 여기서는 같은 retrieve를 이름이 있는 도구로 감쌉니다. 등록하고 요청을 만드는 셀까지는 검색 결과가 아직 없습니다.'),
        'reading-environment': None,
        'reading-request': ('AIMessage.tool_calls에서 요청 읽기',
                          '이 예제는 AIMessage를 코드에서 직접 만듭니다. tool_calls[0]에는 도구 이름·인자·요청 ID가 들어 있습니다. args를 출력하는 줄까지 실행해도 search_documents의 본문은 호출되지 않습니다.'),
        'reading-wrap': ('content_and_artifact의 두 반환값',
                       '도구 함수는 검색 문장들을 줄바꿈으로 이은 문자열과 원래 레코드 리스트를 쌍으로 돌려줍니다. 첫 값은 읽을 내용, 둘째 값은 id와 page까지 갖춘 구조화된 근거입니다.'),
        'reading-message': ('요청 ID와 근거 문서 ID',
                          'ToolMessage의 tool_call_id는 어떤 요청의 응답인지 식별합니다. artifact 안의 id는 어느 문서를 찾았는지 식별합니다. 요청이 search-1이고 문서가 library-1인 두 값은 용도가 다릅니다.'),
        'reading-roundtrip': ('호출 정보를 통째로 invoke()에 넘기는 이유',
                            'call에는 type="tool_call"과 id가 들어 있습니다. call 전체를 넘기면 프레임워크가 도구 결과를 ToolMessage로 감싸고 요청의 ID를 연결합니다. args만 따로 출력한 직전 셀과 비교해 보세요.'),
        'reading-empty': ('빈 결과를 돌려준 호출',
                        '대출·휴관·반납이 없는 질문이면 이 검색 함수는 빈 리스트를 돌려줍니다. 그때도 도구를 호출했다면 요청 ID가 있는 결과를 받을 수 있습니다. 호출하기 전에는 결과 메시지 자체가 없습니다.'),
        'reading-errors': ('잘못된 인자가 검색에 도달하기 전',
                         'SearchArgs에서 k는 1 이상의 StrictInt입니다. 문자열 "1"이나 정수 0을 k로 넣으면 인자 검증에서 멈춥니다. 자료가 없어 빈 목록을 반환한 정상 검색과 발생 지점이 다릅니다.'),
        'reading-citations': None, 'reading-counts': None, 'reading-handoff': None, 'reading-sources': None,
    },
    34: {
        'reading-routing': ('decide()가 반환하는 두 경로',
                          'model 노드는 빈 변경분을 반환합니다. model 뒤의 조건 함수 decide가 rounds와 질문을 읽어 search 또는 finish를 반환합니다. 등록한 대응표에 따라 search는 tool로, finish는 END로 이어집니다.'),
        'reading-entry': None, 'reading-environment': None,
        'reading-state': ('반복을 결정하는 상태 세 칸',
                        'question은 어떤 자료가 필요한지 판단할 입력이고, documents는 방금 찾은 문서입니다. rounds는 tool을 실행할 때마다 1 증가합니다. 판단 함수 자체는 이 값을 변경하지 않습니다.'),
        'reading-nodes': ('tool 다음에 model로 되돌아가는 이유',
                        'tool은 documents와 rounds를 함께 갱신합니다. tool → model 간선을 통해 다시 판단할 때에는 같은 질문이어도 rounds가 1입니다. 상한 조건이 먼저 적용되어 finish로 갑니다.'),
        'reading-normal': ('검색에 쓰인 근거가 결과 상태에 남는 시점',
                         '대출 질문에서는 tool이 library-1을 찾습니다. 이 셀의 마지막 출력은 검색 회차와 문서 ID입니다. 이 그래프에는 별도의 답변 생성 노드가 없으므로, 문서를 찾은 시점과 답변 생성 시점을 혼동하지 마세요.'),
        'reading-limit': ('종료 조건 rounds >= 1',
                        '첫 검색 후 결과 상태를 decide에 그대로 넣어 보세요. 질문에 대출이 있어도 rounds >= 1 검사가 먼저 실행됩니다. 이 순서 덕분에 같은 검색으로 되돌아가지 않습니다.'),
        'reading-errors': None,
        'reading-baseline': ('같은 주차 질문을 고정 간선에 넣으면',
                           '필수 검색 그래프는 START에서 search로 곧장 들어갑니다. 조건 간선이 없으므로 주차 질문도 한 번 검색해 rounds=1, documents=[]가 됩니다. 선택 그래프의 rounds=0과 구별할 수 있습니다.'),
        'reading-compare': None,
        'reading-failure': ('검색 생략이 적절했는지 판단하기',
                           '규칙은 실제 의도 대신 질문에 대출·휴관·반납이라는 낱말이 있는지만 봅니다. 예를 들어 “책을 빌릴 수 있는 기간?”은 대출 질문이지만 이 조건에서는 검색을 생략합니다. rounds=0만 보고 올바른 응답이라고 결론짓기 어렵습니다.'),
        'reading-troubleshooting': None, 'reading-handoff': None, 'reading-sources': None,
    },
}


def scene(anchor, slug, title, caption, nodes, edges, steps):
    return dict(anchor=anchor, slug=slug, title=title, caption=caption,
                nodes=nodes, edges=edges, steps=steps)


def linear(anchor, slug, title, caption, sequence, *, after_code=False):
    """Create a chain when the example really has just one possible successor."""
    keys = [item[0] for item in sequence]
    return dict(scene(anchor, slug, title, caption,
                      [(key, label) for key, label, *_ in sequence], list(zip(keys, keys[1:])),
                      [(key, field, value, note) for key, _, field, value, note in sequence]),
                after_code=after_code)


RETRY_NODES = [('s', 'search'), ('r', 'rewrite'), ('a', 'answer_node'), ('f', 'fallback'), ('e', 'END')]
RETRY_EDGES = [('s','r'), ('r','s'), ('s','a'), ('s','f'), ('a','e'), ('f','e')]
TOOL_NODES = [('s','START'), ('m','model'), ('t','tool'), ('e','END')]
TOOL_EDGES = [('s','m'), ('m','t'), ('t','m'), ('m','e')]

WORKFLOWS = {
    26: [
        linear('nb-run-graph', 'build-before-run', 'compile()까지는 어떤 노드도 실행되지 않습니다',
               '빌더에서 이름과 간선을 등록해 실행 경로를 완성합니다. 첫 상태는 graph.invoke(initial)에서 들어갑니다.', [
            ('n','add_node','등록한 이름','normalize · lookup · compose','함수 세 개에 그래프 안에서 쓸 이름을 붙입니다.'),
            ('l','add_edge','연결한 간선','START → normalize → lookup','이어 lookup → compose → END를 연결합니다.'),
            ('c','compile','반환 객체','graph','여기까지 문서 검색은 0회입니다.'),
            ('i','invoke','첫 실행 입력','initial','이제 START를 거쳐 normalize가 호출됩니다.'),
        ]),
        linear('code-3', 'question-to-answer', '같은 상태에서 세 노드가 한 칸씩 채웁니다',
               '실행 중인 노드가 바뀔 때 반환 키도 바뀝니다. lookup이 찾은 문장은 compose가 answer를 쓴 뒤에도 documents에 남습니다.', [
            ('s','START','question','"  대출 기간은?  "','documents는 빈 목록, answer는 빈 문자열에서 출발합니다.'),
            ('n','normalize','question','"대출 기간은?"','앞뒤 공백만 지우고 question을 반환합니다.'),
            ('l','lookup','documents[0]','도서 대출 기간은 14일입니다.','검색 결과는 문자열 한 개가 든 리스트입니다.'),
            ('c','compose','answer','도서 대출 기간은 14일입니다.','리스트의 문장을 이어 답변 문자열을 만듭니다.'),
            ('e','END','최종 상태','question · documents · answer','invoke는 세 필드가 남은 상태를 돌려줍니다.'),
        ], after_code=True),
    ],
    27: [
        scene('nb-decision','success-first-time','첫 검색에서 문서가 있으면 재작성 간선을 건너뜁니다',
              '질문에 대출이라는 낱말이 이미 있습니다. route에 들어온 attempts가 1이어도 documents를 먼저 검사하므로 rewrite로 가지 않습니다.',
              RETRY_NODES, RETRY_EDGES, [
            ('s','attempts=1','documents 1건','대출 기간?으로 바로 검색해 문장 한 개를 찾습니다.'),
            ('a','경로 이름','answer → answer_node','문장이 있으므로 바로 answer_node에서 문장을 답변으로 씁니다.'),
            ('e','검색 횟수','1','rewrite와 fallback 모두 실행하지 않은 경로입니다.'),
        ]),
        scene('code-3','rewrite-and-recover','한 번 고친 질문이 두 번째 검색에서 성공합니다',
              'route의 retry는 rewrite 노드를 선택합니다. 다음 search가 비어 있지 않은 documents를 돌려주면 answer 경로로 바뀝니다.',
              RETRY_NODES, RETRY_EDGES, [
            ('s','attempts=1','documents = []','책을 빌리는 기간?에는 대출이라는 낱말이 없습니다.'),
            ('r','question','대출을 빌리는 기간?','replace("책", "대출")로 질문이 바뀝니다.'),
            ('s','attempts=2','documents 1건','같은 search를 다시 실행해 이번에는 대출 문장을 찾습니다.'),
            ('a','answer','도서 대출 기간은 14일입니다.','route는 문서 유무를 횟수보다 먼저 검사합니다.'),
            ('e','검색 횟수','2','문서가 있으므로 fallback은 실행하지 않았습니다.'),
        ]),
        scene('code-4','retry-budget','주차 질문은 같은 간선을 돌고도 fallback으로 끝납니다',
              '같은 재검색 경로에서 질문이 바뀌지 않을 수 있습니다. 두 번째 빈 결과에서는 route가 stop을 반환해 fallback으로 이어집니다.',
              RETRY_NODES, RETRY_EDGES, [
            ('s','attempts=1','documents = []','주차장은?에는 대출 낱말이 없어 아직 근거가 없습니다.'),
            ('r','question','주차장은?','바꿀 책이라는 글자가 없어 같은 질문을 유지합니다.'),
            ('s','attempts=2','documents = []','문서는 비었고 재검색 횟수는 상한에 닿았습니다.'),
            ('f','경로 이름','stop → fallback','두 번 검색했지만 근거가 없다는 안내를 만듭니다.'),
            ('e','검색 횟수','2','세 번째 search와 answer_node는 실행하지 않습니다.'),
        ]),
    ],
    28: [
        linear('code-1','plain-update','PlainState에서 사용자의 질문이 사라지는 순간',
               'respond는 두 스키마에서 똑같이 동작합니다. 기본 갱신에서는 반환한 리스트가 messages 필드 전체를 대체합니다.', [
            ('s','START','messages','[h1]','사용자의 대출 질문 한 건을 입력합니다.'),
            ('r','respond','노드의 반환','messages = [a1]','기존 h1을 읽고 응답 한 건만 반환합니다.'),
            ('e','END','최종 messages','[a1]','기본 갱신을 적용하므로 출력 역할은 ai 하나입니다.'),
        ]),
        linear('code-2','reducer-update','add_messages가 있는 그래프는 같은 응답을 누적합니다',
               'ChatState에서는 h1이 있는 목록에 새 ID a1을 합칩니다. 달라진 것은 노드 코드가 아니라 messages의 갱신 규칙입니다.', [
            ('s','START','messages','[h1]','PlainState와 똑같은 사용자 메시지에서 시작합니다.'),
            ('r','respond','노드의 반환','messages = [a1]','노드는 전체 이력을 복사하지 않습니다.'),
            ('e','END','최종 messages','[h1, a1]','add_messages가 새 ID를 추가해 human과 ai가 남습니다.'),
        ]),
    ],
    29: [
        linear('code-2','restore-before-respond','A의 두 번째 invoke 전에 어떤 상태가 복원될까요?',
               '같은 graph와 thread_id를 다시 사용합니다. 첫 질문과 응답을 복원한 뒤 이번 사용자 질문만 더해 respond에 전달합니다.', [
            ('a','A 선택','thread_id','A','이번 send에 들어온 질문은 반납 방법? 한 건입니다.'),
            ('p','상태 복원','직전 messages','사용자 1 · 응답 1','같은 체크포인터에서 A의 직전 상태를 읽습니다.'),
            ('h','입력 병합','사용자 발화 수','2','기존 대출 질문에 새 반납 질문이 더해집니다.'),
            ('r','respond','최근 질문','반납 방법?','사용자 메시지만 세어 2개라고 응답합니다.'),
            ('e','상태 보관','A의 messages','사용자 2 · 응답 2','뒤의 호출도 같은 저장소와 같은 A를 써야 이어집니다.'),
        ]),
        linear('code-3','isolate-new-thread','같은 그래프가 B의 첫 질문에는 1개라고 답합니다',
               'A에 이미 저장된 네 메시지는 A에 남습니다. 이번 config가 B를 가리키므로 respond는 B의 입력만 셉니다.', [
            ('a','B 선택','thread_id','B','graph를 다시 만들지 않고 ID만 바꿉니다.'),
            ('p','B의 상태','기존 메시지','0개','B로 저장한 기록이 아직 없습니다.'),
            ('r','respond','사용자 발화','휴관일? · 1개','A에서 주고받은 질문 두 개는 이 목록에 없습니다.'),
            ('e','상태 보관','B의 messages','사용자 1 · 응답 1','A의 네 메시지와 별도로 B의 첫 왕복을 보관합니다.'),
        ]),
    ],
    30: [
        linear('code-2','record-survives-compose','같은 레코드의 본문과 페이지가 서로 다른 곳으로 갑니다',
               '그래프 이름 compose에 등록한 함수는 answer_node입니다. 이 함수는 answer만 반환합니다. 쪽 번호는 END의 documents에서 읽습니다.', [
            ('s','START','question','휴관 요일은 언제인가요?','documents와 answer는 아직 비어 있습니다.'),
            ('r','search','documents[0]','library-2 · page 2','검색 노드가 휴관 문장의 전체 레코드를 넘깁니다.'),
            ('a','compose','answer','도서관은 월요일에 휴관합니다.','첫 레코드의 text를 꺼내 답변으로 씁니다.'),
            ('e','END','documents[0]["page"]','2','compose가 변경하지 않은 documents에서 쪽 번호를 읽습니다.'),
        ]),
        linear('code-3','empty-still-composes','검색 결과가 비어도 고정 간선은 compose로 갑니다',
               '빈 리스트는 정상 반환값입니다. search에서 종료하지 않고 compose가 목록 길이에 맞는 안내를 고릅니다.', [
            ('s','START','question','주차 요금은?','이 질문에는 대출·휴관·반납이 없습니다.'),
            ('r','search','documents','[]','검색을 실행한 뒤 근거가 없음을 반환합니다.'),
            ('a','compose','answer','제공된 자료에서 확인할 수 없습니다.','docs가 비었으므로 첫 레코드에 접근하지 않습니다.'),
            ('e','END','최종 documents','[]','처음과 똑같이 빈 목록이어도 검색과 답변 노드는 모두 실행됐습니다.'),
        ]),
    ],
    31: [
        linear('code-2','timeout-unwinds','검색 시간이 초과되면 리스트 대신 except로 이동합니다',
               '여기서는 Python 함수와 예외 처리문의 실행 위치를 따릅니다. 앞 셀의 정상 빈 리스트와 달리 slow_search에서 돌려받은 결과는 없습니다.', [
            ('c','호출','question','대출 기간은?','검색어가 있는 질문을 slow_search에 넘깁니다.'),
            ('s','slow_search','발생 예외','TimeoutError','함수가 리스트를 반환하기 전에 raise가 실행됩니다.'),
            ('x','except','출력할 메시지','검색 시간이 초과되었습니다.','예외 이름과 메시지를 출력하며 이번 셀을 마칩니다.'),
        ]),
        linear('code-3','citation-against-retrieval','이번 검색에서 나온 ID만 인용 대조에 사용합니다',
               '이 그림은 파이썬 집합 검사 순서입니다. 라이브러리에 존재하는 문서라도 이번 요청에서 반환하지 않은 ID이면 포함 검사 결과가 달라집니다.', [
            ('r','retrieve','질문','대출 기간은?','가상 문서 세 개에서 대출 질문에 맞는 첫 레코드를 고릅니다.'),
            ('i','ID 집합','retrieved_ids',"{'library-1'}",'검색한 레코드에서 id만 추출합니다.'),
            ('t','포함 검사','cited','library-2','이번 답변이 붙인 휴관 문서 ID를 왼쪽 집합과 대조합니다.'),
            ('e','출력','cited in retrieved_ids','False','인용할 수 있는 집합에 library-2가 없습니다.'),
        ]),
    ],
    32: [
        linear('code-1','lcel-explicit-state','LCEL 파이프에서 다음 함수가 받는 값은 누가 조립할까요?',
               '두 RunnableLambda가 같은 방식으로 기존 상태와 부분 변경분을 합칩니다. 첫 단계가 넘기는 딕셔너리가 둘째 단계의 입력이 됩니다.', [
            ('i','invoke','question','대출 기간은?','documents=[]와 빈 answer를 포함해 입력합니다.'),
            ('s','첫 Runnable','search_change의 반환','documents: [library-1 레코드]','검색 함수는 documents만 돌려줍니다.'),
            ('m','상태 병합','{**state, **변경분}','question · documents · answer','첫 래퍼가 합친 세 필드가 파이프 오른쪽으로 전달됩니다.'),
            ('a','둘째 Runnable','answer','도서 대출 기간은 14일입니다.','답변 변경분도 기존 상태와 합쳐 최종 딕셔너리를 돌려줍니다.'),
        ]),
        linear('code-2','graph-merged-state','StateGraph에서는 노드가 변경한 키만 반환합니다',
               '같은 검색·답변 함수를 이번에는 노드에 등록했습니다. 검색 결과와 답변의 적용을 그래프가 맡으므로 각 노드에서 전체 딕셔너리를 새로 조립할 필요가 없습니다.', [
            ('s','START','question','대출 기간은?','LCEL 예제와 똑같은 request입니다.'),
            ('r','search','이번 반환 키','documents','library-1 한 건이 포함된 레코드 목록이 상태에 합쳐집니다.'),
            ('a','compose','이번 반환 키','answer','검색한 문서의 text만 읽어 답변을 기록합니다.'),
            ('e','END','right == left','True','전체 상태가 같고 두 documents의 문서 ID도 library-1입니다.'),
        ]),
        linear('code-3','first-stream-event','스트림의 첫 갱신에서 어디까지 관찰했을까요?',
               '애니메이션은 next()를 한 번 호출한 관찰자 시점입니다. 첫 항목은 실행 전체의 최종 상태가 아니라 search가 방금 반환한 변경분입니다.', [
            ('g','stream','모드','updates','대출 기간은?으로 그래프의 갱신을 관찰합니다.'),
            ('r','search','갱신한 키','documents','첫 검색 노드가 library-1의 전체 레코드를 반환합니다.'),
            ('y','첫 항목','바깥 키','search','search 아래에 documents가 들어 있습니다.'),
            ('o','첫 ID 출력','documents[0]["id"]','library-1','이번 next()로 관찰한 항목에 compose의 답변은 없습니다.'),
        ]),
    ],
    33: [
        linear('code-2','tool-call-is-a-request','AIMessage를 만들어도 검색은 아직 0회입니다',
               '셀 02의 흐름은 요청을 만드는 데서 끝납니다. 모델 API나 retrieve를 호출하지 않고도 요청의 이름·인자·ID를 검사할 수 있습니다.', [
            ('m','AIMessage','content','빈 문자열','대출 질문을 인자로 삼는 도구 요청을 직접 만듭니다.'),
            ('r','tool_calls[0]','요청 ID','search-1','도구 이름은 search_documents입니다.'),
            ('a','args 출력','question · k','대출 기간은? · 1','값을 꺼내 출력했을 뿐 아직 검색 도구를 실행하지 않았습니다.'),
        ]),
        linear('code-3','invoke-to-tool-message','도구를 실제로 실행하면 두 종류의 ID가 만납니다',
               '프레임워크가 요청의 id를 결과 메시지에 연결합니다. artifact 안의 문서 id는 검색 레코드로부터 옵니다.', [
            ('c','invoke(call)','요청 ID','search-1','args만 꺼내지 않고 요청 전체를 전달합니다.'),
            ('r','retrieve','찾은 문서','library-1','k=1이고 대출 문서가 가장 가깝습니다.'),
            ('p','도구 반환','content','도서 대출 기간은 14일입니다.','문장과 레코드 목록을 한 쌍으로 돌려줍니다.'),
            ('m','ToolMessage','tool_call_id · artifact[0].id','search-1 · library-1','왼쪽은 요청, 오른쪽은 근거 문서를 가리킵니다.'),
        ]),
    ],
    34: [
        scene('code-1','no-search-route','주차 질문이 tool을 건너뛰는 조건부 간선',
              'model은 이 실습의 빈 노드입니다. model 뒤에서 decide가 주차 질문을 읽어 finish를 반환하면 tool 쪽 간선은 실행되지 않습니다.',
              TOOL_NODES, TOOL_EDGES, [
            ('s','question','주차 요금은 얼마인가요?','rounds=0, documents=[]로 시작합니다.'),
            ('m','decide의 반환','finish','인지하는 세 낱말이 질문에 없어 검색 요청이 생기지 않습니다.'),
            ('e','rounds','0','도구를 건너뛰었으므로 빈 목록은 검색 전의 초기값입니다.'),
        ]),
        linear('code-2','mandatory-empty','같은 질문을 필수 검색 그래프에 보내면 한 번 실행됩니다',
               '고정 간선은 판단 함수를 거치지 않습니다. 선택 그래프와 documents는 같아도 실제 검색 횟수는 다릅니다.', [
            ('s','START','question','주차 요금은 얼마인가요?','앞 셀과 똑같은 입력입니다.'),
            ('r','search','run_tool의 반환','rounds=1 · documents=[]','등록 이름은 search이고 함수 본문은 run_tool입니다.'),
            ('e','END','출력','1 []','이 빈 리스트는 한 번 검색한 결과입니다.'),
        ]),
        scene('code-3','return-to-model','도구가 돌려준 뒤 같은 model에서 종료 경로를 고릅니다',
              'model → tool → model로 한 바퀴 도는 동안 rounds가 0에서 1로 바뀝니다. 두 번째 decide가 finish를 반환하므로 tool에 다시 들어가지 않습니다.',
              TOOL_NODES, TOOL_EDGES, [
            ('s','question','대출 기간은 며칠인가요?','rounds=0인 새 요청입니다.'),
            ('m','decide의 반환','search','대출이 들어 있고 아직 도구를 실행하지 않았습니다.'),
            ('t','documents[0].id','library-1','도구가 찾은 문서를 기록하며 rounds를 1로 늘립니다.'),
            ('m','decide의 반환','finish','같은 질문이어도 rounds >= 1 조건이 먼저 적용됩니다.'),
            ('e','출력','1 library-1','도구가 한 번 남긴 마지막 상태로 끝납니다.'),
        ]),
    ],
}

CASE_COPY = {
    33: {'flow-5': ('요청을 보낸 뒤 학생 셀이 멈추는 위치',
                    '셀 03은 ToolMessage에서 tool_call_id와 artifact의 첫 문서 ID를 읽습니다. 도구 결과를 LLM에 다시 보내거나 새 답을 생성하는 호출은 이 셀에 없습니다.')},
    34: {'flow-6': ('종료 후 읽을 수 있는 값',
                    '대출 질문의 최종 상태에서 rounds는 1, documents의 첫 id는 library-1입니다. 조건부 간선이 model에서 END로 이어진 뒤에는 추가 검색이나 답변 생성을 실행하지 않습니다.')},
}
