# 개념 애니메이션 · 1–116장

기준 커밋 `7a7021f`. 각 그림은 장의 실습에서 가져온 질문 하나를 설명한다. 124개 그림을 116개 장의 해당 단원에 배치했다. 웹에서는 시간을 되돌려 두 입력을 대조할 수 있고, 노트북에서는 같은 장면을 GIF로 읽을 수 있다.

| 장 | 수업 중 바로 열기 | 장면에서 확인할 것 |
|---:|---|---|
| 1 | [고친 이름은 언제 커널에 찍힐까요?](https://langchain-lecture.vercel.app/chapter01/index.html#motion-kernel-imprint) | 셀에서 이름을 고쳐도 커널의 값은 그대로입니다. 이름 셀을 실행한 뒤에야 다음 인사가 새 이름을 사용합니다. |
| 2 | [어떤 기록이 70분에 들어갈까요?](https://langchain-lecture.vercel.app/chapter02/index.html#motion-minute-sieve) | 완료했고 30분 이상인 두 기록만 합계에 들어갑니다. Git 연습은 미완료이고 20분이어서 합계에서 빠집니다. |
| 3 | [480분과 481분을 가르는 한 칸](https://langchain-lecture.vercel.app/chapter03/index.html#motion-minute-boundary) | 480까지는 정수를 돌려줍니다. 바로 다음 눈금인 481에서는 범위 검사에서 ValueError가 발생합니다. |
| 4 | [같은 설계도로 만든 두 기록의 스위치](https://langchain-lecture.vercel.app/chapter04/index.html#motion-independent-switches) | 두 객체는 같은 클래스에서 만들어져도 각자의 done 값을 기억합니다. 한쪽 스위치를 눌러도 옆 기록은 그대로입니다. |
| 5 | [두 번째 4번 행은 합계에 또 들어갈까요?](https://langchain-lecture.vercel.app/chapter05/index.html#motion-id-overlay) | 유효한 행의 ID는 1, 2, 4, 4입니다. 같은 ID를 포개면 세 건이 남아 총 90분이 됩니다. |
| 6 | [200 응답 안에 JSON이 없을 수도 있을까요?](https://langchain-lecture.vercel.app/chapter06/index.html#motion-http-envelope) | 상태 코드는 봉투 겉면의 정보입니다. HTTP 응답을 받은 뒤에도 본문을 JSON으로 읽을 수 없으면 별도의 파싱 오류가 납니다. |
| 6 | [따옴표 속 false가 왜 참으로 읽힐까요?](https://langchain-lecture.vercel.app/chapter06/index.html#motion-string-false) | 문자열 "false"에는 글자가 다섯 개 있습니다. bool은 비어 있는지를 검사하므로 True이고, JSON의 논리값 false를 읽으면 False입니다. |
| 7 | [초기화를 한 줄 옮기면 왜 합계가 40일까요?](https://langchain-lecture.vercel.app/chapter07/index.html#motion-reset-tank) | 30, 20, 40을 더할 때마다 누적값을 비우면 마지막 40만 남습니다. 반복문 밖에서 한 번만 비운 쪽에는 90이 남습니다. |
| 8 | [회의에서 무엇을 정했고 무엇을 남겨 두었을까요?](https://langchain-lecture.vercel.app/chapter08/index.html#motion-meeting-ink) | “아직 합의하지 않았다”는 비용이 확정됐다는 근거가 될 수 없습니다. 결정한 항목과 검토 중인 항목의 서술어를 따로 읽습니다. |
| 9 | [무료라는 가격표는 어디까지 붙일 수 있을까요?](https://langchain-lecture.vercel.app/chapter09/index.html#motion-price-label) | 원문의 무료는 설명회 참가비에 붙습니다. 교육과정 수강료 칸에는 발표 전까지 금액을 쓸 근거가 없습니다. |
| 10 | [성인 20명과 30석을 같은 숫자로 읽어도 될까요?](https://langchain-lecture.vercel.app/chapter10/index.html#motion-seats-and-people) | 의자는 시설 자료의 좌석 수이고 점은 행사 안내에서 정한 모집 인원입니다. 같은 방을 가리켜도 두 숫자의 단위와 출처가 다릅니다. |
| 11 | [응답 문자열만 보면 실제 모델 호출을 알 수 있을까요?](https://langchain-lecture.vercel.app/chapter11/index.html#motion-offline-response) | 수업용 고정 응답도 SDK가 읽을 수 있는 모양으로 돌아옵니다. 같은 문장이 보여도 이 예제에서 응답을 제공한 곳은 모의 전송기입니다. |
| 12 | [형식 검사를 통과한 제목도 틀릴 수 있을까요?](https://langchain-lecture.vercel.app/chapter12/index.html#motion-schema-stencil) | “요리 모임”도 문자열이라 형식 검사를 통과합니다. 공지에 적힌 “독서 모임”과 나란히 읽어야 내용 오류가 드러납니다. |
| 13 | [다음 호출에 들어가는 문장은 어디서 왔을까요?](https://langchain-lecture.vercel.app/chapter13/index.html#motion-summary-strip) | 첫 호출이 만든 영수증 문의 요약을 다음 호출의 입력에 끼웁니다. 요약이 비어 있으면 분류할 문장도 없습니다. |
| 14 | [분류가 불분명하면 어떤 호출이 남을까요?](https://langchain-lecture.vercel.app/chapter14/index.html#motion-route-rail) | technical은 기술 문의 단계로 갑니다. 분류 오류 사례에서는 후속 호출 수가 0이므로 임의의 담당자에게 보내지 않습니다. |
| 15 | [도구가 받을 수 있는 요일은 어느 쪽일까요?](https://langchain-lecture.vercel.app/chapter15/index.html#motion-enum-wheel) | day의 허용값은 weekday와 weekend입니다. 주말 조회에는 weekend가 들어가며, 명세에 없는 Friday는 허용값 밖입니다. |
| 16 | [도구 결과는 어느 요청의 영수증일까요?](https://langchain-lecture.vercel.app/chapter16/index.html#motion-matching-stubs) | 요청과 결과에 같은 call_id가 남습니다. 주말 시간 10:00~16:00을 읽을 때도 이 표식으로 원래 요청을 찾습니다. |
| 17 | [도구 두 번을 썼는데 모델은 왜 세 번 불렀을까요?](https://langchain-lecture.vercel.app/chapter17/index.html#motion-call-abacus) | 첫 두 판단은 조회를 요청하고 마지막 판단은 두 결과로 답합니다. 각 기록의 역할을 따로 세면 모델 3회와 도구 2회가 됩니다. |
| 18 | [빈 객체와 빈 호출 ID는 같은 빈칸일까요?](https://langchain-lecture.vercel.app/chapter18/index.html#motion-empty-argument-socket) | 인자가 없는 get_loan_rule은 {}를 받습니다. call_id까지 비면 반환 결과를 요청과 연결할 수 없습니다. |
| 19 | [조각으로 받은 답은 어디에서 한 문장이 될까요?](https://langchain-lecture.vercel.app/chapter19/index.html#motion-stream-typesetter) | 먼저 도착한 글자는 자리에 남고 다음 조각이 뒤에 붙습니다. 마지막에 이어 읽은 문자열과 조각 한 개를 구별해 보세요. |
| 20 | [휴관일의 근거는 어느 쪽에 꽂혀 있을까요?](https://langchain-lecture.vercel.app/chapter20/index.html#motion-source-bookmark) | library-2는 원문의 2쪽을 가리킵니다. 책갈피를 따라가면 월요일 휴관이라는 문장을 다시 읽을 수 있습니다. |
| 21 | [가위가 네 글자 되돌아가면 어느 부분이 두 번 남을까요?](https://langchain-lecture.vercel.app/chapter21/index.html#motion-overlap-scissors) | 첫 청크는 처음 16글자입니다. 다음 시작점을 16에서 12로 되돌리면 “일입니다” 네 글자가 두 청크에 모두 남습니다. |
| 21 | [잘린 조각으로 원문의 자리를 되찾을 수 있을까요?](https://langchain-lecture.vercel.app/chapter21/index.html#motion-source-offset) | 조각에 원문 ID와 위치를 붙이면 짧은 “일입니다.”도 원래 문장의 어느 부분인지 찾을 수 있습니다. |
| 22 | [대출과 휴관 사이의 제곱거리 2는 어디서 나올까요?](https://langchain-lecture.vercel.app/chapter22/index.html#motion-squared-tiles) | 세 축은 대출·휴관·반납입니다. [1,0,0]과 [0,1,0]은 두 축에서 1씩 달라서 차이의 제곱을 더하면 2가 됩니다. |
| 22 | [검색 위치 0은 문서 번호 0일까요?](https://langchain-lecture.vercel.app/chapter22/index.html#motion-faiss-index) | FAISS가 돌려준 위치를 저장 순서에 맞춘 목록에서 읽습니다. 이 예제의 위치 0에 대응하는 문서 ID는 library-1입니다. |
| 23 | [질문이 바뀌면 첫 번째 문서는 어떻게 바뀔까요?](https://langchain-lecture.vercel.app/chapter23/index.html#motion-query-compass) | 대출 기간이라는 질문은 library-1, 휴관일 질문은 library-2를 첫 근거로 찾습니다. 바뀐 단어를 따라 나침반이 다른 원문을 가리킵니다. |
| 24 | [검색 울타리 안에 인용 ID가 있을까요?](https://langchain-lecture.vercel.app/chapter24/index.html#motion-citation-ring) | 휴관일 질문으로 찾은 집합에는 library-2가 있습니다. library-1도 존재하는 문서지만 이번 집합 밖의 인용이라 검사를 통과하지 못합니다. |
| 25 | [틀린 검색 결과는 어느 원문과 대조할까요?](https://langchain-lecture.vercel.app/chapter25/index.html#motion-regression-tracing) | 휴관 요일 질문에서 잘못 찾은 library-1과 직접 확인한 library-2의 2쪽을 대조합니다. 원문을 찾은 뒤에는 검색기도 같은 문서를 찾는지 따로 확인해야 합니다. |
| 26 | [한 필드만 돌려주면 나머지 필드는 지워질까요?](https://langchain-lecture.vercel.app/chapter26/index.html#motion-state-patch) | 질문의 공백을 정리하는 노드는 question만 갱신합니다. documents의 빈 목록과 answer의 빈 문자열은 원래 칸에 남습니다. |
| 27 | [검색을 더 할 수 있는 횟수가 얼마나 남았나요?](https://langchain-lecture.vercel.app/chapter27/index.html#motion-retry-tokens) | 시도할 때마다 표 한 장을 씁니다. 최대 두 번이면 두 장을 모두 쓴 뒤에는 같은 실패가 돌아와도 세 번째 검색을 시작하지 않습니다. |
| 28 | [같은 ID로 오타를 고치면 말풍선이 늘어날까요?](https://langchain-lecture.vercel.app/chapter28/index.html#motion-message-id-edit) | 질문 한 건이 든 initial에 같은 h1으로 수정한 질문을 넣습니다. 기존 말풍선의 문장이 바뀌고 개수는 한 개로 유지됩니다. |
| 29 | [같은 그래프에서 이전 질문은 어디에 남을까요?](https://langchain-lecture.vercel.app/chapter29/index.html#motion-thread-spools) | A의 두 발화는 같은 thread_id의 이력에 감깁니다. B를 열어도 A의 발화가 B의 새 이력으로 옮겨가지 않습니다. |
| 30 | [문장을 건넬 때 출처 꼬리표는 따라갈까요?](https://langchain-lecture.vercel.app/chapter30/index.html#motion-evidence-luggage) | 검색 결과에는 문장과 문서 ID·쪽 번호가 함께 들어 있습니다. 답변 노드가 근거 위치를 읽으려면 꼬리표까지 전달해야 합니다. |
| 31 | [빈 목록과 시간 초과는 어떻게 구별할까요?](https://langchain-lecture.vercel.app/chapter31/index.html#motion-empty-or-timeout) | []는 검색을 마치고 받은 빈 결과입니다. 시간 초과에서는 결과를 받지 못했습니다. 두 경우 모두 근거 문장은 없지만 관찰한 사건이 다릅니다. |
| 32 | [두 구현은 어느 값에서 처음 달라질까요?](https://langchain-lecture.vercel.app/chapter32/index.html#motion-aligned-traces) | 같은 대출 질문에서 LCEL과 그래프 모두 library-1과 14일을 반환합니다. 입력을 맞추고 위아래의 같은 항목을 짝지어 대조합니다. |
| 33 | [search-1과 library-1은 각각 무엇을 가리킬까요?](https://langchain-lecture.vercel.app/chapter33/index.html#motion-reply-envelope) | 답장 봉투의 search-1은 도구 호출 ID입니다. 봉투 안에서 꺼낸 library-1은 검색한 문서 ID입니다. |
| 34 | [도구 요청이 없으면 검색기는 움직일까요?](https://langchain-lecture.vercel.app/chapter34/index.html#motion-unused-tool) | 도구 호출 목록이 비어 있으면 검색 노드를 실행하지 않고 끝냅니다. 도구를 사용할 수 있다는 사실만으로 호출 횟수가 늘지는 않습니다. |
| 35 | [설정을 고르는 동안 어느 질문을 덮어 둘까요?](https://langchain-lecture.vercel.app/chapter35/index.html#motion-sealed-holdout) | 개발 문항을 보며 설정을 조정하고 확인용 문항은 따로 보관합니다. 확인 문항을 미리 열어 설정을 고르면 마지막 비교의 의미가 달라집니다. |
| 36 | [정답이 두 번째여도 찾은 비율은 1일까요?](https://langchain-lecture.vercel.app/chapter36/index.html#motion-rank-reciprocal) | 기대 문서가 하나이고 앞 두 건 안에서 찾았습니다. Recall@2는 1이고 첫 정답 순위의 역수는 1/2입니다. |
| 36 | [근거 ID가 맞으면 999일이라는 답도 통과할까요?](https://langchain-lecture.vercel.app/chapter36/index.html#motion-number-under-citation) | [library-1]이 들어 있는지는 참입니다. 하지만 원문은 14일이라고 하므로 답의 999일은 틀렸습니다. |
| 37 | [k만 늘리면 청크 경계도 바뀔까요?](https://langchain-lecture.vercel.app/chapter37/index.html#motion-topk-aperture) | 같은 순위에서 k를 1에서 2로 늘리면 둘째 조각도 보입니다. 이미 잘라 둔 조각의 내용과 경계는 그대로입니다. |
| 38 | [마침표와 대출 문장 중 어느 조각이 1위일까요?](https://langchain-lecture.vercel.app/chapter38/index.html#motion-candidate-race) | 첫 후보는 마침표 한 글자입니다. 같은 두 후보의 순위를 다시 매기면 대출 기간을 담은 문장이 위로 오릅니다. 새 문서를 추가한 것은 아닙니다. |
| 38 | [두 표현으로 찾은 첫 후보가 같으면 두 건일까요?](https://langchain-lecture.vercel.app/chapter38/index.html#motion-union-of-hits) | 두 검색이 모두 library-1:0을 찾았습니다. 같은 청크 ID를 합치면 최종 후보는 한 건만 남습니다. |
| 39 | [24라는 숫자가 남으면 문장 전체도 남았을까요?](https://langchain-lecture.vercel.app/chapter39/index.html#motion-clipped-answer) | 반납함 사례는 24시간이라는 숫자를 찾았지만 문장이 잘렸습니다. 숫자 일치와 근거 문장을 온전히 읽을 수 있는지를 따로 봅니다. |
| 40 | [입력하다 멈춘 글도 제출한 질문일까요?](https://langchain-lecture.vercel.app/chapter40/index.html#motion-form-carbon) | 폼의 입력 초안은 제출할 때 복사됩니다. 그전까지 앱이 보관한 마지막 질문은 바뀌지 않습니다. |
| 41 | [새 대화를 열면 이전 기록도 지워질까요?](https://langchain-lecture.vercel.app/chapter41/index.html#motion-new-chat-window) | 새 ID의 화면은 비어 있습니다. 기존 ID로 저장된 질문들은 그 대화에 남습니다. |
| 42 | [검색은 맞았는데 화면 쪽수가 틀리다면?](https://langchain-lecture.vercel.app/chapter42/index.html#motion-stale-page-tab) | 휴관일을 찾은 결과는 library-2의 2쪽입니다. 화면의 출처 탭을 현재 결과에 맞추면 이전 질문의 1쪽이 남는 문제를 찾을 수 있습니다. |
| 43 | [운영 안내로 내 점수까지 알 수 있을까요?](https://langchain-lecture.vercel.app/chapter43/index.html#motion-answer-territory) | 과제 제출 위치는 안내 문서 안에 있습니다. 개인 점수는 이 자료에 없어 숫자를 만들어 답할 수 없습니다. |
| 44 | [평일 오전 9시를 토요일에도 옮겨 적을 수 있을까요?](https://langchain-lecture.vercel.app/chapter44/index.html#motion-calendar-reach) | 문단 p1은 평일 시작 시각만 정합니다. 토·일 칸에는 시각이 없어 Q04의 답은 문서에서 확인할 수 없습니다. |
| 45 | [빈 검색 목록 뒤에도 원문은 남아 있을까요?](https://langchain-lecture.vercel.app/chapter45/index.html#motion-missed-shelf) | Q03의 업로드 실패 안내는 p3에 있습니다. 검색 목록이 비었다는 사실만으로 문서에도 답이 없다고 결론 내릴 수 없습니다. |
| 46 | [p3을 찾았는데 왜 답을 보류할까요?](https://langchain-lecture.vercel.app/chapter46/index.html#motion-wrong-citation-pin) | 검색으로 가져온 문단은 p3입니다. 고정 생성기가 인용한 p2를 그 위에 맞춰 봐도 문단 번호가 일치하지 않습니다. |
| 47 | [같은 검색을 반복하면 어디서 끊길까요?](https://langchain-lecture.vercel.app/chapter47/index.html#motion-search-fuse) | 반복 정책에서 검색을 두 번 하고 남은 탐색 횟수가 0이 되면 step_limit으로 끝납니다. 같은 요청이 돌아와도 횟수는 다시 채워지지 않습니다. |
| 48 | [문단 p2가 원문 1쪽에 있을 수 있을까요?](https://langchain-lecture.vercel.app/chapter48/index.html#motion-page-and-paragraph) | course-guide-v1:p2의 p2는 문단 식별자입니다. 수업용 페이지판을 펴면 그 문단이 적힌 실제 위치는 1쪽입니다. |
| 49 | [호출 수 0과 비용 미측정은 같은 눈금일까요?](https://langchain-lecture.vercel.app/chapter49/index.html#motion-instrument-blanks) | 로컬 규칙에서 외부 모델 호출은 0회입니다. 모델 비용과 지연은 재지 않았으므로 계기판에 0을 채우지 않습니다. |
| 50 | [한 곳을 고친 뒤 어느 문항을 다시 당겨 볼까요?](https://langchain-lecture.vercel.app/chapter50/index.html#motion-regression-stitches) | Q03이 p3을 인용하도록 수정한 뒤 기존 Q01의 p2도 검사합니다. 새 사례의 성공만으로 기존 답이 보존됐는지는 알 수 없습니다. |
| 51 | [새 폴더에서 성공하면 새 컴퓨터에서도 검증됐을까요?](https://langchain-lecture.vercel.app/chapter51/index.html#motion-nested-environments) | 재현한 것은 같은 컴퓨터의 새 경로입니다. 새 설치, 다른 운영체제, 동료의 재현은 각각 별도 확인이 필요합니다. |
| 52 | [세 기록에서 오류 위치는 어떻게 달라졌을까요?](https://langchain-lecture.vercel.app/chapter52/index.html#motion-failure-crosssection) | 동일한 Q03에서도 빈 검색, 잘못된 인용, 근거가 맞는 답의 기록이 남았습니다. 발표에서 어떤 수정을 말할지 실제 기록과 맞춰 보세요. |
| 53 | [이름 옆의 질문 수는 어떻게 생길까요?](https://langchain-lecture.vercel.app/chapter53/index.html#motion-join-threads) | 질문 행의 owner를 같은 사용자의 행에 연결합니다. 연결된 줄을 이름별로 세면 학습자 A는 2건, 학습자 B는 1건입니다. |
| 54 | [취소할 수 있는 수정은 어느 종이에 적혀 있을까요?](https://langchain-lecture.vercel.app/chapter54/index.html#motion-carbon-rollback) | 확정된 제목은 초안입니다. 같은 연결에서 수정한 제목을 읽어도 commit 전이라면 rollback이 임시 수정을 걷어내 원래 제목이 다시 보입니다. |
| 55 | [결과 하나가 도착했는데 어떤 호출이 남았을까요?](https://langchain-lecture.vercel.app/chapter55/index.html#motion-unpaired-return) | c1에 주말 운영 시간이 도착해도 c2의 대출 기간은 아직 비어 있습니다. 반환된 ID를 맞춘 뒤에야 어느 요청이 끝났는지 알 수 있습니다. |
| 56 | [검색 개수 k의 첫 허용 눈금은 어디일까요?](https://langchain-lecture.vercel.app/chapter56/index.html#motion-positive-k) | 이 도구는 양의 정수 k를 받습니다. 0에서는 입력 오류가 나고 1은 이 조건을 만족합니다. 출처와 호출 한도는 별도로 검사합니다. |
| 57 | [이름이 비슷한 지침 중 어떤 본문을 펼칠까요?](https://langchain-lecture.vercel.app/chapter57/index.html#motion-skill-bookcase) | 근거를 찾아 답하는 작업에서는 원문 대조 지침을 엽니다. 비교 보고서 지침은 두 실행 기록을 대조하는 다른 작업에 쓰입니다. |
| 58 | [참고자료는 언제 펼쳐 읽을까요?](https://langchain-lecture.vercel.app/chapter58/index.html#motion-foldout-reference) | 선택한 SKILL.md가 원문 대조를 요구할 때 references/source-check.md를 엽니다. 읽은 파일의 크기는 각각 2,511바이트와 1,049바이트입니다. |
| 59 | [최근 두 턴만 남기면 회의실 B를 찾을 수 있을까요?](https://langchain-lecture.vercel.app/chapter59/index.html#motion-memory-aperture) | 네 턴을 전부 볼 때는 장소가 있습니다. 최근 두 턴에는 기한과 슬라이드 수만 남으므로 그 두 턴에서 회의실 B를 다시 찾을 수 없습니다. |
| 59 | [대화를 요약하면 기한도 자동으로 남을까요?](https://langchain-lecture.vercel.app/chapter59/index.html#motion-summary-hole) | 원문에는 금요일 18시라는 제출 기한이 있습니다. 요약에서 그 사실을 빼면 요약만 읽는 다음 호출은 기한을 확인할 수 없습니다. |
| 60 | [서랍 이름이 language로 같아도 값은 누구 것일까요?](https://langchain-lecture.vercel.app/chapter60/index.html#motion-double-key) | 사용자 이름까지 맞아야 같은 기억입니다. alice의 language에는 한국어가 있고, 이 예제에서 bob의 같은 키는 None입니다. |
| 61 | [파이썬 함수는 언제 도구 목록에 나타날까요?](https://langchain-lecture.vercel.app/chapter61/index.html#motion-registered-tool) | 시간표 함수를 서버에 등록하면 클라이언트가 get_library_hours라는 이름을 조회할 수 있습니다. 목록에 이름이 보이는 것과 주말 시간을 실제 조회하는 것은 다른 관찰입니다. |
| 62 | [형식이 맞는 시간표도 틀린 답일 수 있을까요?](https://langchain-lecture.vercel.app/chapter62/index.html#motion-weekday-dial) | 평일 요청에 주말 시각을 반환해도 필드 자체는 있을 수 있습니다. 요청한 요일과 맞춰 읽으면 평일에는 09:00~18:00이 대응합니다. |
| 63 | [검색 근거가 비면 생성 호출도 줄어들까요?](https://langchain-lecture.vercel.app/chapter63/index.html#motion-generation-stop) | 근거가 한 건도 없는 경로는 답변 생성 전에 멈춥니다. 계산한 호출 수는 0이며, 근거 없이 만든 문장을 화면에 붙이지 않습니다. |
| 64 | [문의 내용이 보이는 순간 등록도 끝났을까요?](https://langchain-lecture.vercel.app/chapter64/index.html#motion-approval-latch) | 승인 대기 중 등록 건수는 0입니다. 같은 실행을 승인해 재개한 뒤에만 등록 건수가 1로 바뀝니다. |
| 65 | [기술 문의에 열리는 도구 칸은 어디일까요?](https://langchain-lecture.vercel.app/chapter65/index.html#motion-tool-apertures) | 기술 문의로 분류한 예제는 technical_faq를 사용합니다. 분류값이 정해졌다고 모든 도구가 허용되는 것은 아닙니다. |
| 66 | [다음 역할에 ID만 주면 무엇이 빠질까요?](https://langchain-lecture.vercel.app/chapter66/index.html#motion-handoff-bundle) | 질문, 근거 원문, 출처 ID를 함께 넘겨야 다음 역할이 원문을 다시 찾지 않고 답을 쓸 수 있습니다. |
| 67 | [맞는 인용 ID 아래 틀린 답이 숨을 수 있을까요?](https://langchain-lecture.vercel.app/chapter67/index.html#motion-fact-check-xray) | 답은 개인 메신저를 가리키지만 인용한 p2 원문은 학습 관리 페이지의 과제함을 가리킵니다. ID 검사를 통과한 뒤에도 행동 지시가 일치하는지 읽습니다. |
| 68 | [422와 빈 근거는 어디에서 갈라질까요?](https://langchain-lecture.vercel.app/chapter68/index.html#motion-two-verdicts) | 공백 질문은 입력 검사에서 422가 됩니다. 형식이 맞는 질문으로 검색을 마쳤지만 문서가 없었다면 입력 오류로 고칠 이유가 없습니다. |
| 69 | [받은 조각의 끝이 이벤트의 끝일까요?](https://langchain-lecture.vercel.app/chapter69/index.html#motion-newline-framer) | NDJSON은 줄바꿈을 만났을 때 한 줄을 읽습니다. 네트워크가 JSON 중간에서 나눠 보내면 뒷조각이 올 때까지 그 줄을 버퍼에 둡니다. |
| 70 | [접수한 문서가 곧바로 검색될까요?](https://langchain-lecture.vercel.app/chapter70/index.html#motion-ready-index) | received 상태의 문서를 접수한 뒤 본문을 준비해 ready로 바꿉니다. 준비 전후를 나누어야 아직 비어 있는 문서를 검색 근거로 쓰지 않습니다. |
| 71 | [이미지에 적힌 CMD는 언제 실행될까요?](https://langchain-lecture.vercel.app/chapter71/index.html#motion-image-imprint) | 이미지는 시작 명령을 보관합니다. 컨테이너를 시작하면 그 명령으로 프로세스가 생깁니다. 이 그림은 원리 설명이며 실제 Docker 실행 여부는 셀 출력에서 확인합니다. |
| 72 | [두 컨테이너에서 localhost는 같은 곳일까요?](https://langchain-lecture.vercel.app/chapter72/index.html#motion-localhost-mirrors) | 각 컨테이너의 localhost는 자기 자신을 가리킵니다. 같은 Compose 네트워크에서 API가 DB를 찾을 때 쓰는 주소는 db:5432입니다. |
| 72 | [컨테이너를 바꿀 때 데이터는 어디에 남을까요?](https://langchain-lecture.vercel.app/chapter72/index.html#motion-persistent-volume) | 기존 볼륨에 있던 데이터를 새 DB 컨테이너가 같은 위치에 다시 연결해 읽습니다. 같은 이름의 새 컨테이너만 만들어서는 이 연결이 보장되지 않습니다. |
| 73 | [좌표 두 칸이 다르면 거리는 왜 1.414일까요?](https://langchain-lecture.vercel.app/chapter73/index.html#motion-distance-triangle) | p1은 질문과 같은 점이라 거리가 0입니다. p2는 두 축에서 각각 1만큼 달라 직각삼각형의 빗변 길이 √2만큼 떨어져 있습니다. |
| 74 | [외부에서 보이는 포트와 안쪽 포트는 같을까요?](https://langchain-lecture.vercel.app/chapter74/index.html#motion-published-port) | 프록시의 443만 호스트에 공개합니다. 안쪽의 api:8000은 공통 네트워크에서 프록시가 찾는 목적지입니다. |
| 75 | [같은 행 수 아래 무엇이 달라졌을까요?](https://langchain-lecture.vercel.app/chapter75/index.html#motion-row-diff) | 원본과 복구본에 모두 한 행이 있어도 같은 키의 본문이 다르면 복구 검사는 실패합니다. 확대경은 개수가 아닌 실제 행 내용을 대조합니다. |
| 76 | [검사 프로그램이 1을 돌려주면 게시 작업은?](https://langchain-lecture.vercel.app/chapter76/index.html#motion-ci-barrier) | 종료 코드 1은 검사 실패입니다. check에 의존하는 publish는 건너뜁니다. 게시를 실행했다가 실패한 경우와 구별하세요. |
| 77 | [태그를 옮겨도 이미지 내용의 지문이 바뀔까요?](https://langchain-lecture.vercel.app/chapter77/index.html#motion-floating-tag) | 같은 태그가 다른 이미지 바이트를 가리킬 수 있습니다. 검토한 후보를 다시 지정할 때는 그 내용의 digest를 대조합니다. |
| 77 | [정상 응답 200 뒤에도 버전을 되돌릴 수 있을까요?](https://langchain-lecture.vercel.app/chapter77/index.html#motion-rollback-switch) | 후보 B는 200을 돌려줘도 필수 출처가 없습니다. 이 수업용 상태에서는 출처를 되찾기 위해 이전 A로 바꿉니다. |
| 78 | [레이블을 눌렀을 때 커서는 어디에 생길까요?](https://langchain-lecture.vercel.app/chapter78/index.html#motion-label-focus) | for와 id가 같으면 레이블을 눌러도 연결된 입력칸에 초점이 갑니다. 두 값이 다르면 그 관계가 끊깁니다. |
| 79 | [응답이 도착하면 답 문장도 곧바로 읽을 수 있을까요?](https://langchain-lecture.vercel.app/chapter79/index.html#motion-response-unfold) | 응답 상태를 받은 것과 본문을 파싱해 answer를 꺼낸 것은 다른 관찰입니다. 본문을 펼쳐야 답 문장과 출처가 보입니다. |
| 80 | [빈 제목을 거절하면 목록에는 몇 건이 남을까요?](https://langchain-lecture.vercel.app/chapter80/index.html#motion-blank-title) | 공백뿐인 제목을 정리하면 쓸 글자가 없습니다. INVALID_TITLE을 돌려주고 저장 목록에는 새 행을 만들지 않습니다. |
| 81 | [없는 항목의 수정을 요청하면 기존 목록도 바뀔까요?](https://langchain-lecture.vercel.app/chapter81/index.html#motion-status-card) | 1번 항목을 완료로 바꾸면 200입니다. 없는 999번을 수정하면 404가 돌아오지만 화면에 있던 1번 행은 그대로 남습니다. |
| 82 | [연결을 닫으면 저장한 할 일도 사라질까요?](https://langchain-lecture.vercel.app/chapter82/index.html#motion-reopen-database) | 파일 DB에 커밋한 복습 50% 행은 연결 객체를 새로 만들어도 같은 파일에서 읽을 수 있습니다. |
| 83 | [같은 완료 요청을 두 번 보내면 스위치는 어디에 있을까요?](https://langchain-lecture.vercel.app/chapter83/index.html#motion-toggle-rocker) | 현재 값을 뒤집으면 첫 요청 뒤 True, 재전송 뒤 False입니다. 요청에 적힌 최종값 True를 대입하면 재전송 뒤에도 True가 남습니다. |
| 84 | [기존 행에 새 열을 붙이면 어떤 값이 생길까요?](https://langchain-lecture.vercel.app/chapter84/index.html#motion-schema-extension) | 기존 제목 복습은 남습니다. 마감일은 None, 우선순위는 기본값 normal로 시작해 새 스키마에서도 행을 읽을 수 있습니다. |
| 85 | [앱을 새로 띄워도 같은 행을 읽을 수 있을까요?](https://langchain-lecture.vercel.app/chapter85/index.html#motion-shared-record) | 새 앱 인스턴스가 같은 DB를 읽으면 저장했던 복습, 2027-04-02, high가 함께 돌아옵니다. 앱의 수명과 행의 수명을 따로 볼 수 있습니다. |
| 86 | [교대 담당자가 가리켜야 할 물체는 무엇일까요?](https://langchain-lecture.vercel.app/chapter86/index.html#motion-handover-lamp) | 장비 A의 규정 2.1은 점검 전에 전원 표시등을 확인하라고 합니다. 막연한 “점검”을 실제로 확인할 물체와 원문 위치까지 좁힌 예입니다. |
| 87 | [장비 이름이 빠졌을 때 왜 다음 행동이 질문일까요?](https://langchain-lecture.vercel.app/chapter87/index.html#motion-missing-equipment) | “점검 전 확인 사항은?”에는 장비가 지정되지 않았습니다. A와 B의 서로 다른 규정 중 하나를 임의로 고르지 않고 장비명을 다시 묻습니다. |
| 88 | [“출처가 있다”를 무엇으로 확인할까요?](https://langchain-lecture.vercel.app/chapter88/index.html#motion-source-ruler) | 수용 기준에는 문서 이름과 쪽·절·개정일·판본이 있습니다. 규정 이름만 보이는 상태와 원문 위치까지 다시 찾을 수 있는 상태를 구분합니다. |
| 89 | [연결이 끊기면 어떤 규정을 읽을 수 있을까요?](https://langchain-lecture.vercel.app/chapter89/index.html#motion-offline-copy) | 수업에서 미리 확보한 허용 규정 RULE-A와 RULE-B는 사본으로 확인할 수 있습니다. 사본 밖 자료를 읽었다고 기록할 수는 없습니다. |
| 90 | [기대하는 답과 출처를 왜 한 쌍으로 둘까요?](https://langchain-lecture.vercel.app/chapter90/index.html#motion-expected-pair) | Q01의 답을 평가할 때 RULE-A도 함께 대조합니다. 답할 근거가 없는 문항에는 출처를 비워 둬야 만들어 낸 인용을 발견할 수 있습니다. |
| 91 | [장비 A가 같으면 교체 일정도 알 수 있을까요?](https://langchain-lecture.vercel.app/chapter91/index.html#motion-intent-key) | 점검 전 확인 사항과 교체 일정은 서로 다른 질문입니다. 장비 이름만 맞추는 첫 구현은 두 질문에 같은 점검 문장을 반환해 일정 질문에서 틀립니다. |
| 92 | [7문항 중 두 개를 맞힌 기록에서 어디를 고칠까요?](https://langchain-lecture.vercel.app/chapter92/index.html#motion-baseline-error) | Q03의 기대는 no_evidence와 빈 출처입니다. 첫 구현은 장비명만 보고 answered와 RULE-A를 반환했습니다. 전체 점수에서 이 한 행을 꺼내야 오류가 보입니다. |
| 93 | [출처 칸은 답변 상태와 어떻게 맞물릴까요?](https://langchain-lecture.vercel.app/chapter93/index.html#motion-paired-status) | 답을 근거로 확인한 Q01에는 RULE-A가 붙습니다. 근거가 없는 질문을 표시할 때는 상태를 바꾸면서 현재 출처 목록도 비워야 합니다. |
| 94 | [같은 검색 문장에 왜 서로 다른 원문 지문이 붙을까요?](https://langchain-lecture.vercel.app/chapter94/index.html#motion-byte-fingerprint) | UTF-8에서 공백 한 바이트 0x20과 줄바꿈 한 바이트 0x0A는 다릅니다. 원문을 해시하면 지문이 달라지고, 공백을 정리한 검색 문장은 같습니다. |
| 95 | [검색 목록이 비면 모든 자료에 답이 없다는 뜻일까요?](https://langchain-lecture.vercel.app/chapter95/index.html#motion-allowed-library) | 검색은 현재 그룹에 허용된 자료 안에서만 이뤄집니다. 빈 목록은 이번 검색 범위 안에서 근거를 찾지 못했다는 결과입니다. |
| 96 | [RULE-A만 보고 원문의 한 줄을 다시 찾을 수 있을까요?](https://langchain-lecture.vercel.app/chapter96/index.html#motion-section-zoom) | 문서에서 1쪽 2.1절로 좁히면 전원 표시등을 확인하라는 근거가 나옵니다. 개정일과 rules-v1은 어느 판본에서 읽었는지 남깁니다. |
| 97 | [새 질문이 와도 예전 턴의 근거까지 지워질까요?](https://langchain-lecture.vercel.app/chapter97/index.html#motion-turn-filmstrip) | 화면은 현재 턴의 출처만 읽습니다. Q03에서 빈 목록이 보이더라도 이력의 Q01은 RULE-A를 유지하고, Q04에는 RULE-B가 붙습니다. |
| 98 | [A 뒤에 B가 더 있으면 틈을 내도 될까요?](https://langchain-lecture.vercel.app/chapter98/index.html#motion-word-boundary) | A·B 뒤가 문자열 끝이거나 다음 글자가 영문·숫자가 아닐 때만 공백을 넣습니다. “장비A의”는 바뀌지만 “장비AB”에는 A 뒤에 B가 이어져 원문이 유지됩니다. |
| 99 | [똑같이 두 번 시도했는데 끝 상태가 왜 다를까요?](https://langchain-lecture.vercel.app/chapter99/index.html#motion-retry-budget-clock) | 첫 시간 초과 뒤에는 한 번 더 시도할 수 있습니다. 두 번째 결과가 성공이면 완료하고 다시 시간 초과면 예산을 소진해 중단합니다. |
| 100 | [여섯 번째 턴을 쓰면 어느 기록이 밀릴까요?](https://langchain-lecture.vercel.app/chapter100/index.html#motion-five-turn-window) | 이 설계는 세션 안에서 최근 다섯 턴만 유지합니다. 새 턴이 들어오면 가장 오래된 턴이 빠집니다. 세션 전체의 300초 만료 조건은 별도로 적용됩니다. |
| 101 | [규정 문서로 근무 교대표를 채울 수 있을까요?](https://langchain-lecture.vercel.app/chapter101/index.html#motion-missing-roster) | 장비 규정과 개인 근무 일정은 다른 자료입니다. 일정 자료와 조회 권한을 확인하기 전에는 교대표를 채워 넣지 않고 연동을 보류합니다. |
| 102 | [답을 만들었다는 영수증이 저장까지 보장할까요?](https://langchain-lecture.vercel.app/chapter102/index.html#motion-split-receipt) | 계산한 답과 저장 결과는 독립된 필드입니다. 저장 실패 사례에서는 답이 있어도 저장을 완료했다고 표시할 수 없습니다. |
| 103 | [힌트를 받은 뒤 찾은 근거를 자력 성공으로 셀까요?](https://langchain-lecture.vercel.app/chapter103/index.html#motion-hint-divider) | 가상 관찰에서는 답을 읽고 멈췄다가 힌트 뒤에 2.1절을 선택했습니다. 힌트 시점 앞뒤를 나누어야 다음 화면에서 무엇을 고칠지 판단할 수 있습니다. |
| 104 | [새 요청이 대기하는 동안 무엇을 지워야 할까요?](https://langchain-lecture.vercel.app/chapter104/index.html#motion-clear-on-send) | 직전 질문의 답과 출처를 함께 비웁니다. 새 요청의 결과가 도착한 뒤에야 그 요청의 답과 근거를 표시합니다. |
| 105 | [응답이 끊기면 저장 실패로 단정할 수 있을까요?](https://langchain-lecture.vercel.app/chapter105/index.html#motion-lost-ack) | 응답을 받지 못한 클라이언트는 저장 결과를 알 수 없습니다. 같은 요청을 다시 보내기 전에 해당 요청의 기록을 확인하는 안내가 필요합니다. |
| 106 | [답은 있는데 저장에 실패한 요청은 어떻게 보일까요?](https://langchain-lecture.vercel.app/chapter106/index.html#motion-two-indicators) | 계산 완료와 저장 완료를 두 표시등으로 봅니다. 저장 실패 사례에서는 답 계산 쪽만 켜지고 저장 완료 쪽은 켜지지 않습니다. |
| 107 | [과업을 시작한 횟수와 성공한 횟수는 같을까요?](https://langchain-lecture.vercel.app/chapter107/index.html#motion-observed-attempts) | 가상 과업은 세 번 시작했고 한 번 성공했습니다. 시작한 세 건을 분모로 두어야 완료한 한 건의 뜻을 읽을 수 있습니다. |
| 108 | [ID가 다른 질문이 같은 평가 문항일 수 있을까요?](https://langchain-lecture.vercel.app/chapter108/index.html#motion-trim-overlay) | PUBLIC-DUP-01은 Q01 문장의 양끝에 공백을 붙인 예입니다. 양끝을 정리한 두 문장을 겹치면 ID가 달라도 질문 내용은 같습니다. |
| 109 | [다른 사람의 대화를 막아도 내 대화는 열릴까요?](https://langchain-lecture.vercel.app/chapter109/index.html#motion-owner-pocket) | 예시에서 bob은 자기 대화의 장비 B 근거 RULE-B를 읽습니다. 본인 기록을 읽을 수 있다는 정상 사례도 함께 점검합니다. |
| 110 | [12와 15.5라는 눈금 사이에서 잰 값은 무엇일까요?](https://langchain-lecture.vercel.app/chapter110/index.html#motion-stopwatch-span) | 서비스 시작과 종료에 찍은 합성 시각의 차이는 3.5ms입니다. 브라우저에서 요청을 보내고 답을 그리는 시간은 이 두 눈금 밖에 있습니다. |
| 111 | [확장 문항 세 개를 맞히면 바로 출시할 수 있을까요?](https://langchain-lecture.vercel.app/chapter111/index.html#motion-release-evidence) | 공개 기본 7문항은 전후 모두 통과했습니다. 확장 세 문항 중 통과가 1개에서 3개로 늘었지만 운영 근거가 남아 후보의 출시 결정은 보류입니다. |
| 112 | [컨테이너 경로와 자료 볼륨은 어떻게 이어질까요?](https://langchain-lecture.vercel.app/chapter112/index.html#motion-mount-bridge) | 시안은 p1-json을 앱의 runtime-data 위치에 연결합니다. 재배포 뒤 데이터 보존 여부는 같은 볼륨을 연결하고 실제 세션을 다시 읽어 확인합니다. |
| 113 | [복구한 목록만으로 오래된 중복까지 알 수 있을까요?](https://langchain-lecture.vercel.app/chapter113/index.html#motion-replay-window) | 가상 복구 기록에는 r2부터 r6까지 남습니다. r6은 기록에서 찾을 수 있지만 이미 밀려난 r0의 처리 여부는 이 다섯 칸만 보고 알 수 없습니다. |
| 114 | [“안 돼요” 대신 어느 지점까지 읽었는지 알려 주면?](https://langchain-lecture.vercel.app/chapter114/index.html#motion-handover-checkpoint) | 인수자가 직접 확인한 마지막 출력과 아직 실행하지 않은 연결을 구분합니다. Q01에서 RULE-A 2.1절을 읽었다는 기록은 다음 확인 위치를 좁혀 줍니다. |
| 115 | [발표에서 답을 읽은 뒤 어디를 가리킬까요?](https://langchain-lecture.vercel.app/chapter115/index.html#motion-demo-spotlight) | 장비 A의 점검 답을 보여 준 뒤 규정 2.1절과 개정일을 짚습니다. 관객은 그 표식으로 답의 근거를 다시 찾을 수 있습니다. |
| 116 | [세 질문으로 확인한 기여의 범위는 어디까지일까요?](https://langchain-lecture.vercel.app/chapter116/index.html#motion-claim-radius) | 두 장비의 붙여쓰기와 모호한 장비AB는 공개 개발 사례입니다. 이 세 입력에서 확인한 수정 효과와 실제 사용자 질문 전체의 품질을 구분해 인계합니다. |

## 검수 기록

작화와 노트북의 수치·조건을 네 구간에서 독립적으로 대조했다. 검수에서 발견한 7장 누적값, 19장 문자 경계, 22장 제곱거리, 70장 저장 시점, 81장 404 응답 뒤의 기존 행, 92장 기준선의 문항별 통과 여부 등을 수정한 뒤 프레임을 다시 읽었다.

기존 노트북의 코드·실행 횟수·저장 출력 429셀과 기존 첨부 자료를 기준 커밋과 대조했다. HTML 127개의 내부 링크, 웹 프레임 파일, 116개 노트북 첨부를 검사했다. 새 GIF는 커널이나 외부 모델 없이 재생된다. 이번 검수는 설명 장면을 대상으로 했으며 학생의 학습 효과나 모든 외부 서비스의 실행까지 평가한 결과는 아니다.
