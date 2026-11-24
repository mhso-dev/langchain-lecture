# 일반 수업 교재 75장 전수검수

2026년 11월 24일 · 일반 수업 1–42장과 53–85장, 75일 600시간. 중간 프로젝트 43–52장과 최종 프로젝트 86–116장은 이번 개정에서 제외했다. 117–120일은 특강·현장 활동이다.

학생용 HTML의 본문·예제·풀이·복습·시각 자료를 같은 장의 노트북과 대조했다. 코드가 만들지 않는 결과를 설명한 문장, 선행 수업에서 제공하지 않은 파일을 요구하는 활동, 목표를 담지 못한 과제를 고쳤다. 아래 표의 링크는 장마다 대표적인 수정 한 곳을 가리킨다.

## 실행과 독립 검수

개정 전 과제는 118개였다. 개정본은 코딩 과제 163개, 서술 과제 2개로 총 165개다. macOS의 Python 3.12.15 환경에서 75권의 시작본을 실행하고, 별도 상태에서 학생 작성 부분을 정답으로 채워 다시 실행했다. 코드 412셀은 예제와 준비 셀 249개, 학생용 코딩 과제 163개로 구성된다. 7·10장의 학생 서술은 답안 예시와 평가 기준을 대조했다.

독립 교육 검수의 최종 판정은 `corrected`다. 165개 문제의 웹·노트북 지시와 풀이를 대조했다. 26장의 노드 반환, 38장의 후보 누락, 41장의 문서 변경, 85장의 기존 DB 재조회는 앞서 배운 코드를 직접 바꾸거나 실행해 판단하도록 고쳤다. 41장에서 같은 주차 질문에 보내는 근거는 안내문이 없을 때 빈 목록, 안내문을 입력하면 `session-note`, 안내문을 지우면 다시 빈 목록이 된다. 검수자는 실제 LangGraph로 이 순서를 재현했다.

일반 수업의 수동 재생 영상은 9편이다. 20장의 반납 장면처럼 근거를 다시 읽는 데 도움을 주지 않는 영상과 여러 장의 중복 단계 카드를 걷어냈다. PDF 문자층과 청크 경계는 원문 위치를 비교하는 조작을 유지했다. 목차에서 일반 수업 75장과 선택 표시한 자료 116장이 맞는지, 42장과 53장 사이를 이동하는지, 접힌 풀이 165개가 열리고 닫히는지 확인했다. 공통 조작 실험 16곳에는 총 50개 입력을 넣어 문서 안의 출력이 바뀌는지 검사했다. 이 검사는 스크립트와 문서 구조를 대상으로 했다.

## 장별 검수 범위

| 장 | 수업과 수정 위치 | 확인한 설명 또는 과제 | 실행 코드 셀 | 코딩 과제 | 서술 과제 |
|---:|---|---|---:|---:|---:|
| 1 | [Jupyter 커널과 Python 코드 실행](../site/chapter01/index.html#nb-environment) | 새 커널에서 이름을 다시 대입하고 출력하기 | 9 | 2 | 0 |
| 2 | [Python의 리스트·딕셔너리와 조건 반복](../site/chapter02/index.html#nb-one-record) | 리스트 인덱스와 딕셔너리 키 | 7 | 2 | 0 |
| 3 | [함수의 반환값·타입 힌트·예외 처리](../site/chapter03/index.html#nb-return) | print()와 return의 차이 | 6 | 2 | 0 |
| 4 | [Python 클래스와 모듈](../site/chapter04/index.html#nb-service) | 생성 함수에서 입력 검증 | 7 | 2 | 0 |
| 5 | [CSV 읽기와 데이터 정제](../site/chapter05/index.html#nb-read) | csv.DictReader와 문자열 필드 | 6 | 1 | 0 |
| 6 | [HTTP 요청과 JSON 응답 처리](../site/chapter06/index.html#nb-failures) | HTTP 상태 오류와 JSONDecodeError | 6 | 2 | 0 |
| 7 | [Python 디버깅과 Git 변경 이력](../site/chapter07/index.html#nb-merge-conflict) | 충돌 해결 후 재현 절차 | 4 | 1 | 1 |
| 8 | [LLM 서비스 비교와 응답 평가](../site/chapter08/index.html#nb-choice) | 원문 일치도를 기준으로 서비스 비교 | 6 | 3 | 0 |
| 9 | [프롬프트 설계와 버전 비교](../site/chapter09/index.html#nb-versions) | 프롬프트 변경 이력과 재시험 입력 | 6 | 2 | 0 |
| 10 | [LLM 답변의 주장과 근거 검증](../site/chapter10/index.html#nb-approval) | 미확인 주장의 검토 요청 | 4 | 1 | 1 |
| 11 | [OpenAI Responses API의 요청·응답 구조](../site/chapter11/index.html#nb-usage) | 응답 상태에 따라 표시할 본문 선택 | 6 | 2 | 0 |
| 12 | [구조화된 출력이란?](../site/chapter12/index.html#sdk-call) | responses.create()와 APITimeoutError | 20 | 6 | 0 |
| 13 | [순차 워크플로의 입력·출력 연결](../site/chapter13/index.html#nb-trace) | 작성 호출에 전달된 요약 검사 | 6 | 2 | 0 |
| 14 | [분류 함수와 조건부 라우팅](../site/chapter14/index.html#nb-policy) | clarify 경로와 추가 질문 | 5 | 2 | 0 |
| 15 | [Function Calling의 도구 명세와 호출 요청](../site/chapter15/index.html#nb-observe) | 인자 해석과 허용값 검사 | 6 | 3 | 0 |
| 16 | [Function Calling의 실행과 결과 반환](../site/chapter16/index.html#transfer-practice) | 응답 순서가 뒤집힌 두 요청 | 7 | 3 | 0 |
| 17 | [도구 호출 루프와 종료 조건](../site/chapter17/index.html#transfer-practice) | 루프에 중복 실행 방지 넣기 | 6 | 3 | 0 |
| 18 | [도구 요청의 인자 검증과 실행 차단](../site/chapter18/index.html#transfer-practice) | 실행할 요청만 골라내는 입구 함수 | 6 | 3 | 0 |
| 19 | [LCEL 체인과 출력 파서](../site/chapter19/index.html#transfer-practice) | 프롬프트가 받은 문맥 확인 | 6 | 3 | 0 |
| 20 | [RAG 문서 로딩과 근거 메타데이터](../site/chapter20/index.html#observe-source) | 운영 시간을 뒷받침하는 원문 | 12 | 4 | 0 |
| 21 | [문서 청킹과 원문 오프셋](../site/chapter21/index.html#nb-location) | 청크에서 원문 위치 복원 | 12 | 5 | 0 |
| 22 | [벡터 거리와 Chroma·FAISS 검색](../site/chapter22/index.html#nb-chroma) | Chroma 컬렉션에 쓰고 다시 열기 | 12 | 5 | 0 |
| 23 | [Retriever의 검색 입력과 반환 형식](../site/chapter23/index.html#transfer-practice) | 두 질의의 1위를 문서별로 읽기 | 6 | 3 | 0 |
| 24 | [LCEL로 구성하는 RAG와 인용 검증](../site/chapter24/index.html#transfer-practice) | 실제 출처를 달고도 틀린 답 찾기 | 6 | 3 | 0 |
| 25 | [RAG 입력 계약과 오류 진단](../site/chapter25/index.html#transfer-practice) | 빈 결과와 손상된 자료 나누기 | 6 | 3 | 0 |
| 26 | [LangGraph StateGraph의 상태와 노드](../site/chapter26/index.html#transfer-practice) | 근거 두 줄을 쓰는 답변 노드 | 5 | 2 | 0 |
| 27 | [LangGraph 조건부 간선과 재검색](../site/chapter27/index.html#transfer-practice) | 재검색이 끝나는 노드 추적 | 5 | 2 | 0 |
| 28 | [LangGraph의 메시지 리듀서 add_messages](../site/chapter28/index.html#transfer-practice) | 같은 발화의 정정이 답변에 미치는 영향 | 4 | 2 | 0 |
| 29 | [체크포인터와 thread_id를 이용한 대화 저장](../site/chapter29/index.html#transfer-practice) | 같은 대화 ID와 다른 저장소 | 4 | 2 | 0 |
| 30 | [LangGraph의 검색 노드와 답변 노드](../site/chapter30/index.html#transfer-practice) | 검색을 반복하지 않고 답변에 출처 달기 | 4 | 2 | 0 |
| 31 | [RAG 검색 예외와 인용 검사](../site/chapter31/index.html#transfer-practice) | 검색 결과에 대출 문서가 있는데 연장 기간을 묻는다면 | 4 | 2 | 0 |
| 32 | [LCEL과 LangGraph의 상태 전달](../site/chapter32/index.html#transfer-practice) | 검색 노드의 변경분과 최종 상태 비교 | 4 | 2 | 0 |
| 33 | [LangChain 검색 도구와 ToolMessage](../site/chapter33/index.html#transfer-practice) | 도구가 정상 실행됐지만 자료가 없는 요청 | 4 | 2 | 0 |
| 34 | [LangGraph의 선택적 도구 호출과 반복](../site/chapter34/index.html#transfer-practice) | 동의어 질문에서 검색 생략 진단 | 5 | 2 | 0 |
| 35 | [RAG 평가 데이터셋 구성](../site/chapter35/index.html#transfer-practice) | 확인용 문항의 근거 작성 | 4 | 2 | 0 |
| 36 | [검색 평가 지표와 답변 근거 검증](../site/chapter36/index.html#transfer-practice) | 같은 원문의 두 청크가 1·2위를 차지할 때 | 5 | 2 | 0 |
| 37 | [청크 크기·중첩·top-k 비교 실험](../site/chapter37/index.html#transfer-practice) | 휴관 요일이 청크 안에 남는 중첩 크기 | 5 | 2 | 0 |
| 38 | [재정렬과 다중 질의 검색](../site/chapter38/index.html#transfer-practice) | 정답 청크가 후보에 없을 때 | 5 | 2 | 0 |
| 39 | [RAG 개선안의 품질과 비용 비교](../site/chapter39/index.html#transfer-practice) | 개발 문항 세 건에서 늘어난 작업 계산 | 4 | 2 | 0 |
| 40 | [Streamlit 폼으로 만드는 RAG 질의 화면](../site/chapter40/index.html#transfer-practice) | 제출 결과로 출처 패널 교체 | 5 | 2 | 0 |
| 41 | [Streamlit 세션과 LangGraph 체크포인트](../site/chapter41/index.html#transfer-practice) | 다른 대화를 시작한 뒤 원래 스레드 다시 열기 | 6 | 2 | 0 |
| 42 | [RAG 화면의 출처 추적과 회귀 검사](../site/chapter42/index.html#transfer-practice) | 잘못된 인용이 섞인 응답의 회귀 검사 | 4 | 2 | 0 |
| 53 | [SQL SELECT·JOIN·GROUP BY](../site/chapter53/index.html#applied-practice) | 질문이 없는 사용자까지 집계하기 | 5 | 2 | 0 |
| 54 | [SQL 매개변수 바인딩과 트랜잭션](../site/chapter54/index.html#applied-practice) | 수정된 행이 0건일 때의 결과 확인하기 | 7 | 3 | 0 |
| 55 | [create_agent의 도구 등록과 메시지 왕복](../site/chapter55/index.html#applied-practice) | 도구 결과에서 최종 답변에 쓰인 값 찾기 | 7 | 3 | 0 |
| 56 | [에이전트 입력 검증과 도구 호출 제한](../site/chapter56/index.html#applied-practice) | 검색 결과 수에 상한 두기 | 7 | 3 | 0 |
| 57 | [SKILL.md의 설명·입력·작업 지침](../site/chapter57/index.html#applied-practice) | 비교 보고서에 빠진 입력 찾기 | 6 | 4 | 0 |
| 58 | [Progressive Disclosure와 Skill 로더](../site/chapter58/index.html#applied-practice) | 선택한 본문의 글자 수와 바이트 수 재기 | 6 | 2 | 0 |
| 59 | [대화 문맥의 최근 턴과 요약 메모리](../site/chapter59/index.html#applied-practice) | 장소가 바뀌었을 때 요약 갱신하기 | 5 | 2 | 0 |
| 60 | [사용자별 장기 기억과 SQL 저장](../site/chapter60/index.html#applied-practice) | 한 사용자의 설정만 SQL로 지우기 | 6 | 3 | 0 |
| 61 | [FastMCP 도구 등록과 클라이언트 호출](../site/chapter61/index.html#applied-practice) | 등록된 도구의 입력 계약 읽기 | 5 | 2 | 0 |
| 62 | [MCP 도구와 LangChain 에이전트 연결](../site/chapter62/index.html#applied-practice) | 서버가 다른 요일을 보냈을 때 거절하기 | 5 | 2 | 0 |
| 63 | [RAG 서비스 함수와 응답 계약](../site/chapter63/index.html#applied-practice) | 다른 사용자의 대화에서 검색 막기 | 4 | 2 | 0 |
| 64 | [LangGraph interrupt와 승인 후 재개](../site/chapter64/index.html#applied-practice) | 승인한 본문이 처음 제안과 같은지 확인하기 | 5 | 2 | 0 |
| 65 | [의도 라우팅과 LangChain 도구 선택](../site/chapter65/index.html#applied-practice) | 도구가 등록되지 않은 결제 경로 처리하기 | 6 | 3 | 0 |
| 66 | [역할별 함수 분리와 호출 비용](../site/chapter66/index.html#applied-practice) | 인계한 근거가 새 질문에도 맞는지 확인하기 | 4 | 2 | 0 |
| 67 | [서비스 평가의 인용 정확성과 분모](../site/chapter67/index.html#applied-practice) | 실행한 검색 사례의 실패율 계산하기 | 4 | 2 | 0 |
| 68 | [FastAPI 요청 모델과 POST 엔드포인트](../site/chapter68/index.html#applied-practice) | HTTP 422에서 수정할 입력 필드 찾기 | 5 | 2 | 0 |
| 69 | [FastAPI StreamingResponse와 줄 단위 JSON](../site/chapter69/index.html#nb-partial) | 다른 소유자의 조회 제한 | 4 | 2 | 0 |
| 70 | [SQLite 문서 상태와 대화 턴 저장](../site/chapter70/index.html#nb-turn) | 소유자 조건을 포함한 대화 조회 | 4 | 1 | 0 |
| 71 | [Dockerfile과 컨테이너 수명 주기](../site/chapter71/index.html#nb-dockerfile) | 빌드 단계의 RUN | 3 | 1 | 0 |
| 72 | [Docker Compose 네트워크와 볼륨](../site/chapter72/index.html#nb-compose) | 호스트 포트 매핑 | 4 | 1 | 0 |
| 73 | [벡터의 L2 거리와 pgvector 검색](../site/chapter73/index.html#nb-embed) | 질의 변경에 따른 거리 비교 | 3 | 1 | 0 |
| 74 | [EC2 배포 구성과 프록시 경로](../site/chapter74/index.html#acceptance-practice) | 프록시가 넘긴 경로와 API 응답 | 4 | 2 | 0 |
| 75 | [SQLite 백업과 복구 검증](../site/chapter75/index.html#nb-incident) | 원문 필드의 불일치 검출 | 3 | 1 | 0 |
| 76 | [GitHub Actions의 작업 의존성과 실행 조건](../site/chapter76/index.html#acceptance-practice) | 같은 단위 검사로 포트 수정 전후 비교 | 4 | 2 | 0 |
| 77 | [컨테이너 이미지 digest와 롤백 기준](../site/chapter77/index.html#acceptance-practice) | 잘못된 출처를 반환한 후보의 복구 검사 | 4 | 2 | 0 |
| 78 | [HTML 입력 요소와 반응형 CSS](../site/chapter78/index.html#nb-markup) | label과 id 연결 | 3 | 1 | 0 |
| 79 | [JavaScript 폼 이벤트와 fetch 응답 처리](../site/chapter79/index.html#nb-fetch) | HTTP 실패 시 분기 | 4 | 1 | 0 |
| 80 | [Codex 요청의 수용 기준과 JavaScript 상태 변경](../site/chapter80/index.html#nb-review) | ID별 완료 상태 변경 | 3 | 1 | 0 |
| 81 | [FastAPI로 구현하는 할 일 CRUD](../site/chapter81/index.html#nb-confirm) | DELETE 결과 검증 | 5 | 1 | 0 |
| 82 | [SQLite 영속성과 instr() 부분 문자열 검색](../site/chapter82/index.html#nb-filter) | 완료 상태와 검색 조건 결합 | 4 | 1 | 0 |
| 83 | [멱등적인 완료 상태 갱신](../site/chapter83/index.html#nb-fix) | 목표 상태 대입의 멱등성 | 3 | 1 | 0 |
| 84 | [SQLite 스키마 변경과 부분 업데이트](../site/chapter84/index.html#nb-patch) | NULL과 필드 생략 구분 | 5 | 1 | 0 |
| 85 | [FastAPI 앱 재시작과 DB 호환성](../site/chapter85/index.html#acceptance-practice) | 교체한 로컬 앱의 출시 전 기능 검사 | 5 | 2 | 0 |

## 확인 필요 항목

- Streamlit 위젯의 실제 조작, Chroma 저장·재열기, PostgreSQL·pgvector 연결과 외부 모델·Jev 호출에는 해당 패키지나 서비스 환경이 필요하다. FAISS 검색, 메모리 MCP 호출, LangGraph 상태 전이, FastAPI TestClient와 SQLite 등 실제 실행한 경로는 장별 기록에 적었다.
- Docker·EC2·GitHub Actions 등 외부 배포 실습의 실제 계정 실행, 학생 Windows·WSL 환경과 8시간 수업 실측은 이번 로컬 검수에서 확인하지 못했다.
- 이번 판의 데스크톱·모바일 브라우저 실화면과 운영 사이트 반영은 미확인이다. 실습 자료는 로컬 개정본과 오프라인 ZIP 기준이다.
- 교재의 외부 전송을 수반하는 맞춤법 검사는 공개 범위를 따로 승인받지 않아 생략했다. 한국어 설명은 코드·출력 및 원문과 대조했다.
