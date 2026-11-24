# 개념·문법 중심 교재 개정 · 2026-11-24

116장의 목차, 본문, 실습 노트북에 같은 학습 용어를 사용했다. 아래 절 수에는 실행 환경·복습·참고 자료가 포함된다. 정규 셀 수는 기존 실습과 과제의 제목 수다. 12장의 추가 비교 예제 4개는 별도다.

독립 교육 검수 결과는 accept다. 노트북 코드·저장 출력 429쌍을 이전 커밋과 대조했다. 문법 설명과 사례의 혼동을 수정한 예로 45장은 질문 전체 일치 비교, 79장은 모의 객체의 textContent 대입, 82장은 SQLite instr() 부분 문자열 검색을 다룬다. 심화 읽기 제목 758개와 4단계 제목 152개를 대조했다.

12장은 Python 3.12, langchain-classic 1.0.8, langchain-core 1.6.12, Pydantic 2.14.1, openai 3.35.1, httpx 0.28.1에서 고정 입력·모의 전송으로 코드 셀 20개를 순서대로 실행했다. 같은 문자열의 everyone 값은 StructuredOutputParser에서 그대로 나왔고 Literal을 지정한 PydanticOutputParser에서 OutputParserException이 발생했다. 새 예제 4개의 표준 출력이 노트북과 일치했다.

Higgsfield에서 직접 만든 GIF 17편의 첫·중간·마지막 장면을 확인하고 같은 장면을 512×288 H.264 MP4로 변환했다. 모두 4.8초이며 오디오 트랙은 없다. 재생·정지는 기본 동영상 컨트롤을 사용한다. Three.js 실험 12곳은 입력에 따라 계산하며, WebGL을 쓸 수 없는 환경에서도 수치를 읽을 수 있다. 그 경로에서 경계값을 포함한 25개 입력·출력을 검사했다.

검증 명령은 node scripts/build.mjs 및 python3 scripts/check.py다. 참조와 링크 검사는 HTML 119개와 노트북 116개에서 통과했다. 실제 Three.js 장면과 카메라 구성 12개, 좌표축 회전 이벤트 2개를 검사했다. 이 검사는 GPU 렌더러 대역을 사용했다. 로컬 브라우저 실행 제한으로 실제 GPU 화면과 학생 기기의 화면은 미확인이다. 전 장의 기존 API·DB·배포 실행, 학생용 Windows/WSL과 8시간 학습 소요는 이번 검수의 관측 대상에서 제외했다. 기존 장별 검증 상태를 유지한다. 외부 맞춤법 서비스에는 원고를 전송하지 않았다.

| 장 | 주제 | 목차 절 | 정규 셀 | 심화 절 | 시각 자료 |
|---:|---|---:|---:|---:|---|
| 1 | [Jupyter 커널과 Python 코드 실행](../site/chapter01/index.html) | 8 | 9 | 5 | 4.8초 영상 |
| 2 | [Python의 리스트·딕셔너리와 조건 반복](../site/chapter02/index.html) | 7 | 7 | 8 | Three.js 실험 |
| 3 | [함수의 반환값·타입 힌트·예외 처리](../site/chapter03/index.html) | 7 | 6 | 7 | 4.8초 영상 |
| 4 | [Python 클래스와 모듈](../site/chapter04/index.html) | 7 | 7 | 7 | 4.8초 영상 |
| 5 | [CSV 읽기와 데이터 정제](../site/chapter05/index.html) | 8 | 6 | 9 |  |
| 6 | [HTTP 요청과 JSON 응답 처리](../site/chapter06/index.html) | 7 | 6 | 9 |  |
| 7 | [Python 디버깅과 Git 변경 이력](../site/chapter07/index.html) | 7 | 5 | 7 |  |
| 8 | [LLM 서비스 비교와 응답 평가](../site/chapter08/index.html) | 7 | 6 | 10 |  |
| 9 | [프롬프트 설계와 버전 비교](../site/chapter09/index.html) | 6 | 6 | 9 |  |
| 10 | [LLM 답변의 주장과 근거 검증](../site/chapter10/index.html) | 6 | 5 | 8 |  |
| 11 | [OpenAI Responses API의 요청·응답 구조](../site/chapter11/index.html) | 7 | 5 | 8 |  |
| 12 | [구조화된 출력이란?](../site/chapter12/index.html) | 14 | 16 | 0 | 4.8초 영상 |
| 13 | [순차 워크플로의 입력·출력 연결](../site/chapter13/index.html) | 7 | 5 | 7 |  |
| 14 | [분류 함수와 조건부 라우팅](../site/chapter14/index.html) | 7 | 5 | 9 |  |
| 15 | [Function Calling의 도구 명세와 호출 요청](../site/chapter15/index.html) | 7 | 5 | 9 | 4.8초 영상 |
| 16 | [Function Calling의 실행과 결과 반환](../site/chapter16/index.html) | 7 | 6 | 10 |  |
| 17 | [도구 호출 루프와 종료 조건](../site/chapter17/index.html) | 7 | 5 | 10 |  |
| 18 | [도구 요청의 인자 검증과 실행 차단](../site/chapter18/index.html) | 6 | 5 | 9 |  |
| 19 | [LCEL 체인과 출력 파서](../site/chapter19/index.html) | 7 | 5 | 9 | 4.8초 영상 |
| 20 | [RAG 문서 로딩과 근거 메타데이터](../site/chapter20/index.html) | 7 | 6 | 9 | 4.8초 영상 |
| 21 | [문자열 청킹과 원문 오프셋](../site/chapter21/index.html) | 6 | 6 | 9 | Three.js 실험 |
| 22 | [벡터 거리와 Chroma·FAISS 검색](../site/chapter22/index.html) | 7 | 6 | 12 | Three.js 실험 |
| 23 | [Retriever의 검색 입력과 반환 형식](../site/chapter23/index.html) | 7 | 5 | 8 |  |
| 24 | [LCEL로 구성하는 RAG와 인용 검증](../site/chapter24/index.html) | 7 | 5 | 8 |  |
| 25 | [RAG 입력 계약과 오류 진단](../site/chapter25/index.html) | 7 | 5 | 9 |  |
| 26 | [LangGraph StateGraph의 상태와 노드](../site/chapter26/index.html) | 6 | 4 | 5 |  |
| 27 | [LangGraph 조건부 간선과 재검색](../site/chapter27/index.html) | 6 | 4 | 8 | 4.8초 영상, Three.js 실험 |
| 28 | [LangGraph의 메시지 리듀서 add_messages](../site/chapter28/index.html) | 6 | 3 | 7 |  |
| 29 | [체크포인터와 thread_id를 이용한 대화 저장](../site/chapter29/index.html) | 6 | 3 | 7 |  |
| 30 | [LangGraph의 검색 노드와 답변 노드](../site/chapter30/index.html) | 6 | 3 | 5 |  |
| 31 | [RAG 검색 예외와 인용 검사](../site/chapter31/index.html) | 6 | 3 | 5 |  |
| 32 | [LCEL과 LangGraph의 상태 전달](../site/chapter32/index.html) | 6 | 3 | 5 |  |
| 33 | [LangChain 검색 도구와 ToolMessage](../site/chapter33/index.html) | 6 | 3 | 13 |  |
| 34 | [LangGraph의 선택적 도구 호출과 반복](../site/chapter34/index.html) | 6 | 4 | 14 |  |
| 35 | [RAG 평가 데이터셋 구성](../site/chapter35/index.html) | 6 | 3 | 13 |  |
| 36 | [검색 평가 지표와 답변 근거 검증](../site/chapter36/index.html) | 6 | 4 | 13 | Three.js 실험 |
| 37 | [청크 크기·중첩·top-k 비교 실험](../site/chapter37/index.html) | 6 | 4 | 13 | Three.js 실험 |
| 38 | [재정렬과 다중 질의 검색](../site/chapter38/index.html) | 6 | 4 | 13 | Three.js 실험 |
| 39 | [RAG 개선안의 품질과 비용 비교](../site/chapter39/index.html) | 6 | 3 | 15 |  |
| 40 | [Streamlit 폼으로 만드는 RAG 질의 화면](../site/chapter40/index.html) | 6 | 4 | 10 | 4.8초 영상 |
| 41 | [Streamlit 세션과 LangGraph 체크포인트](../site/chapter41/index.html) | 7 | 5 | 11 |  |
| 42 | [RAG 화면의 출처 추적과 회귀 검사](../site/chapter42/index.html) | 5 | 3 | 11 |  |
| 43 | [RAG 프로젝트의 문제 정의와 수용 기준](../site/chapter43/index.html) | 4 | 1 | 0 |  |
| 44 | [평가 문항과 정답 근거 매핑](../site/chapter44/index.html) | 4 | 2 | 0 |  |
| 45 | [질문 전체 일치 검색의 기준선과 빈 결과](../site/chapter45/index.html) | 4 | 2 | 0 |  |
| 46 | [검색 규칙 변경과 실패 단계 진단](../site/chapter46/index.html) | 4 | 2 | 0 |  |
| 47 | [필수 검색과 선택 검색의 종료 조건](../site/chapter47/index.html) | 4 | 2 | 0 |  |
| 48 | [RAG 결과 화면과 출처 초기화](../site/chapter48/index.html) | 4 | 2 | 0 |  |
| 49 | [검색·인용 품질과 비용 측정 조건](../site/chapter49/index.html) | 4 | 2 | 0 |  |
| 50 | [인용 오류 수정과 회귀 검증](../site/chapter50/index.html) | 4 | 2 | 0 |  |
| 51 | [실험 재현을 위한 README와 실행 기록](../site/chapter51/index.html) | 4 | 2 | 0 |  |
| 52 | [실패 사례를 이용한 프로젝트 시연과 회고](../site/chapter52/index.html) | 4 | 1 | 0 |  |
| 53 | [SQL SELECT·JOIN·GROUP BY](../site/chapter53/index.html) | 7 | 4 | 12 |  |
| 54 | [SQL 매개변수 바인딩과 트랜잭션](../site/chapter54/index.html) | 7 | 6 | 14 |  |
| 55 | [create_agent의 도구 등록과 메시지 왕복](../site/chapter55/index.html) | 7 | 7 | 10 |  |
| 56 | [에이전트 입력 검증과 도구 호출 제한](../site/chapter56/index.html) | 7 | 6 | 9 |  |
| 57 | [SKILL.md의 설명·입력·작업 지침](../site/chapter57/index.html) | 7 | 5 | 12 |  |
| 58 | [Progressive Disclosure와 Skill 로더](../site/chapter58/index.html) | 7 | 5 | 13 |  |
| 59 | [대화 문맥의 최근 턴과 요약 메모리](../site/chapter59/index.html) | 6 | 4 | 11 | Three.js 실험 |
| 60 | [사용자별 장기 기억과 SQL 저장](../site/chapter60/index.html) | 7 | 5 | 11 |  |
| 61 | [FastMCP 도구 등록과 클라이언트 호출](../site/chapter61/index.html) | 5 | 4 | 11 |  |
| 62 | [MCP 도구와 LangChain 에이전트 연결](../site/chapter62/index.html) | 6 | 5 | 11 |  |
| 63 | [RAG 서비스 함수와 응답 계약](../site/chapter63/index.html) | 6 | 3 | 13 |  |
| 64 | [LangGraph interrupt와 승인 후 재개](../site/chapter64/index.html) | 6 | 4 | 13 | 4.8초 영상 |
| 65 | [의도 라우팅과 LangChain 도구 선택](../site/chapter65/index.html) | 7 | 5 | 9 |  |
| 66 | [역할별 함수 분리와 호출 비용](../site/chapter66/index.html) | 6 | 3 | 13 |  |
| 67 | [서비스 평가의 인용 정확성과 분모](../site/chapter67/index.html) | 6 | 3 | 12 |  |
| 68 | [FastAPI 요청 모델과 POST 엔드포인트](../site/chapter68/index.html) | 6 | 4 | 10 |  |
| 69 | [FastAPI StreamingResponse와 줄 단위 JSON](../site/chapter69/index.html) | 6 | 4 | 11 | 4.8초 영상 |
| 70 | [SQLite 문서 상태와 대화 턴 저장](../site/chapter70/index.html) | 6 | 4 | 11 |  |
| 71 | [Dockerfile과 컨테이너 수명 주기](../site/chapter71/index.html) | 6 | 3 | 12 | 4.8초 영상 |
| 72 | [Docker Compose 네트워크와 볼륨](../site/chapter72/index.html) | 7 | 4 | 12 | 4.8초 영상 |
| 73 | [벡터의 L2 거리와 pgvector 검색](../site/chapter73/index.html) | 6 | 3 | 11 | Three.js 실험 |
| 74 | [EC2 배포 구성과 프록시 경로](../site/chapter74/index.html) | 5 | 3 | 12 |  |
| 75 | [SQLite 백업과 복구 검증](../site/chapter75/index.html) | 5 | 3 | 12 |  |
| 76 | [GitHub Actions의 작업 의존성과 실행 조건](../site/chapter76/index.html) | 6 | 3 | 12 |  |
| 77 | [컨테이너 이미지 digest와 롤백 기준](../site/chapter77/index.html) | 6 | 3 | 12 | 4.8초 영상 |
| 78 | [HTML 입력 요소와 반응형 CSS](../site/chapter78/index.html) | 5 | 3 | 13 |  |
| 79 | [JavaScript 폼 이벤트와 fetch 응답 처리](../site/chapter79/index.html) | 5 | 4 | 11 |  |
| 80 | [Codex 요청의 수용 기준과 JavaScript 상태 변경](../site/chapter80/index.html) | 6 | 3 | 12 |  |
| 81 | [FastAPI로 구현하는 할 일 CRUD](../site/chapter81/index.html) | 5 | 5 | 12 |  |
| 82 | [SQLite 영속성과 instr() 부분 문자열 검색](../site/chapter82/index.html) | 5 | 4 | 12 |  |
| 83 | [멱등적인 완료 상태 갱신](../site/chapter83/index.html) | 5 | 3 | 12 | Three.js 실험 |
| 84 | [SQLite 스키마 변경과 부분 업데이트](../site/chapter84/index.html) | 5 | 4 | 12 |  |
| 85 | [FastAPI 앱 재시작과 DB 호환성](../site/chapter85/index.html) | 5 | 4 | 12 |  |
| 86 | [서비스 문제 정의와 최소 시연 범위](../site/chapter86/index.html) | 4 | 2 | 0 |  |
| 87 | [사용자 시나리오와 추가 질문 조건](../site/chapter87/index.html) | 4 | 2 | 0 |  |
| 88 | [인수 기준과 작업 분해](../site/chapter88/index.html) | 4 | 2 | 0 |  |
| 89 | [자료 접근 범위와 대체 데이터](../site/chapter89/index.html) | 4 | 2 | 0 |  |
| 90 | [평가 기준선과 보류 문항](../site/chapter90/index.html) | 4 | 2 | 0 |  |
| 91 | [키워드 조회 함수의 최소 구현](../site/chapter91/index.html) | 4 | 3 | 0 |  |
| 92 | [기준선 통과율과 오류 분석](../site/chapter92/index.html) | 4 | 2 | 0 |  |
| 93 | [서비스 상태와 종료 조건](../site/chapter93/index.html) | 4 | 2 | 0 |  |
| 94 | [텍스트 정규화와 원문 해시](../site/chapter94/index.html) | 4 | 2 | 0 | 4.8초 영상 |
| 95 | [검색 모듈의 권한 필터와 빈 결과](../site/chapter95/index.html) | 4 | 3 | 0 |  |
| 96 | [출처 표기 함수와 응답 카드](../site/chapter96/index.html) | 4 | 2 | 0 |  |
| 97 | [대화 턴의 현재 출처와 이전 기록](../site/chapter97/index.html) | 4 | 2 | 0 | 4.8초 영상 |
| 98 | [정규표현식 치환과 경계 조건](../site/chapter98/index.html) | 4 | 2 | 0 |  |
| 99 | [시간 초과의 재시도와 중단 조건](../site/chapter99/index.html) | 4 | 2 | 0 |  |
| 100 | [소유자·세션별 기록과 보존 한도](../site/chapter100/index.html) | 4 | 2 | 0 | Three.js 실험 |
| 101 | [Skill·외부 도구 도입 기준](../site/chapter101/index.html) | 4 | 2 | 0 |  |
| 102 | [POST 요청·응답 계약과 저장 상태](../site/chapter102/index.html) | 4 | 3 | 0 |  |
| 103 | [알파 사용성 검사의 관찰 기록](../site/chapter103/index.html) | 4 | 2 | 0 |  |
| 104 | [답변 카드와 요청 대기 상태](../site/chapter104/index.html) | 4 | 2 | 0 |  |
| 105 | [RAG 화면의 오류 상태와 안내 문구](../site/chapter105/index.html) | 4 | 2 | 0 |  |
| 106 | [요청별 실행 추적과 저장 실패 진단](../site/chapter106/index.html) | 4 | 2 | 0 |  |
| 107 | [베타 사용성 평가와 과업 성공률](../site/chapter107/index.html) | 4 | 2 | 0 |  |
| 108 | [평가 문항 중복 제거와 오답 분석](../site/chapter108/index.html) | 4 | 2 | 0 |  |
| 109 | [소유자 권한과 응답 노출 검증](../site/chapter109/index.html) | 4 | 2 | 0 |  |
| 110 | [응답 지연 시간 계산과 호출 비용의 측정 조건](../site/chapter110/index.html) | 4 | 2 | 0 | Three.js 실험 |
| 111 | [최소 재현 입력과 회귀 테스트](../site/chapter111/index.html) | 4 | 2 | 0 |  |
| 112 | [배포 설정의 포트·볼륨과 확인 절차](../site/chapter112/index.html) | 4 | 2 | 0 |  |
| 113 | [파일 백업과 세션 데이터 복원](../site/chapter113/index.html) | 4 | 2 | 0 | 4.8초 영상 |
| 114 | [재현 가능한 README와 인수인계](../site/chapter114/index.html) | 4 | 2 | 0 |  |
| 115 | [근거 중심 데모와 실패 시 대체 시연](../site/chapter115/index.html) | 4 | 2 | 0 |  |
| 116 | [프로젝트 기여 검증과 후속 인계](../site/chapter116/index.html) | 4 | 2 | 0 |  |
