# 33장 수업 예시를 적용한 115장 개정

일반 수업 74장과 중간·최종 프로젝트 41장을 개정했다. 승인된 33장은 기존 학생본을 사용한다. 교육일 117–120의 특강·현장 활동은 이번 집필 범위 밖이다.

[장별 개정 절](../site/updates/index.html#workshop-edition)

## 강의 흐름과 실습

앞 장에서 만든 함수를 다시 설명하던 47개 장의 52곳을 고쳤다. 해당 장의 입력이나 예외로 바로 들어가고, 개념 정의가 필요한 학생은 선수 절로 돌아갈 수 있게 했다. 34장에서는 검색 결과가 모델로 돌아오는 경로를, 55장에서는 같은 도구를 다시 호출하는 조건을, 66장에서는 조회 모델의 근거를 작성 모델로 넘기는 위치를 코드와 Mermaid로 대조한다. 38장에서는 같은 후보 세 건에서 질문 표현에 따라 재정렬 순위가 달라지는 실제 CPU 측정값을 확인한다.

장별로 예제 125개와 직접 코딩 과제 74개를 추가했다. 프로젝트에는 완성 사례표 20개와 팀별 적용 지시 39개가 있다. 웹과 노트북 양쪽에서 시작 코드 바로 아래의 정답을 펼쳐 풀이와 출력을 읽을 수 있다.

## 실행·검수 범위

- 최종 학생 노트북 115개를 macOS의 Python 3.12 커널에서 빈 작업 폴더로 열었다. 시작 코드 699셀과 정답을 채운 699셀을 각각 순서대로 실행했다. 독립 교육 검수에서 86장은 다른 입력·경계 조건도 대조했다.
- 독립 검수자는 장별 목표와 선수 개념, 코드·출력·프로젝트 사례, 정답의 위치를 대조했다. 50장의 혼합 인용, 57장의 문자열, 62장의 MCP 서버 재실행 문제를 고쳐 다시 실행했다. 115장 모두 교육 검수에서 수용 판정을 받았다.
- `node scripts/build.mjs`와 `python3 scripts/check.py`로 HTML 120개와 노트북 116개, 내부 링크, 앵커 및 복사 대상, 학생 페이지의 미디어 제외를 확인했다. 33장을 포함한 Mermaid 차트 77개를 배포 번들로 SVG 렌더링했다. DOM 에뮬레이션에서 정답 266개와 조작형 실습 18개를 확인했다.
- 출판 원고와 최종본에서 새 설명·제목·표·캡션 1,522개를 대조했다. 대조에는 외부 맞춤법 서비스를 사용하지 않았다. 수식이 쓰인 6개 장은 웹 MathML을 유지하고 노트북에는 LaTeX를 제공한다.
- API 비용이 들지 않는 기본 경로를 기준으로 삼았다. 에이전트의 모델 응답을 고정한 예제와 외부 모델을 쓰는 선택 셀은 본문에서 구분한다. 로컬 MCP와 FAISS는 실행했다. Docker 컨테이너·EC2·PostgreSQL·Chroma 및 외부 모델을 사용하는 선택 경로 전체, 수강생 Windows·WSL과 실제 8시간 수업은 미검증이다. 개별 장의 이전 검수 기록에는 해당 장에서 수행한 별도 검사가 남아 있다.

## 장별 확인 내역

코드 셀 수는 시작본 한 번의 실행 분량이다. 풀이본에서도 동일한 개수의 셀을 실행했다.

| 장 | 개정 절 | 코드 셀 | 추가 반례·재풀이 | Mermaid |
|---|---|---:|---|---:|
| 1 | [수강생 이름을 바꿨는데 인사말은 왜 그대로일까요?](../site/chapter01/index.html#workshop) | 12 | 검증 | 0 |
| 2 | [완료한 공부 시간의 분모 정하기](../site/chapter02/index.html#workshop) | 9 | 검증 | 0 |
| 3 | [잘못된 입력 한 줄을 남기고 다음 기록 읽기](../site/chapter03/index.html#workshop) | 8 | 검증 | 0 |
| 4 | [저장한 학습 기록을 새 객체로 복원하기](../site/chapter04/index.html#workshop) | 9 | 검증 | 0 |
| 5 | [같은 ID의 두 시간이 다를 때 합계에서 보류하기](../site/chapter05/index.html#workshop) | 8 | 검증 | 0 |
| 6 | [페이지가 둘로 나뉜 할 일 목록 조회하기](../site/chapter06/index.html#workshop) | 8 | 검증 | 0 |
| 7 | [고친 코드와 커밋할 코드가 다른 경우](../site/chapter07/index.html#workshop) | 6 | 검증 | 0 |
| 8 | [두 요약에서 회의 결정의 범위 대조하기](../site/chapter08/index.html#workshop) | 8 | 검증 | 1 |
| 9 | [같은 지시문으로 바뀐 안내문 다시 요약하기](../site/chapter09/index.html#workshop) | 8 | 검증 | 0 |
| 10 | [담당자에게 보낼 행사 안내 초안 완성하기](../site/chapter10/index.html#workshop) | 6 | 검증 | 0 |
| 11 | [후속 질문이 어느 응답을 이어받는지 확인하기](../site/chapter11/index.html#workshop) | 8 | 검증 | 1 |
| 12 | [완성돼 보이는 JSON을 언제 공지로 넘길까요?](../site/chapter12/index.html#workshop) | 22 | 검증 | 1 |
| 13 | [요약에서 빠진 조건을 작성 요청에 되살리기](../site/chapter13/index.html#workshop) | 8 | 검증 | 1 |
| 14 | [복합 문의를 되묻고 선택한 경로로 이어 보내기](../site/chapter14/index.html#workshop) | 7 | 검증 | 1 |
| 15 | [도구 명세에 새 인자를 넣고 기존 요청 검사하기](../site/chapter15/index.html#workshop) | 8 | 검증 | 1 |
| 16 | [대출 권수 조회를 기존 시간표 도구 옆에 연결하기](../site/chapter16/index.html#workshop) | 10 | 검증 | 1 |
| 17 | [한 번의 모델 응답에 도구 요청이 두 개라면?](../site/chapter17/index.html#workshop) | 8 | 검증 | 2 |
| 18 | [검사에서 막힌 요청과 자료가 없는 조회 구별하기](../site/chapter18/index.html#workshop) | 8 | 검증 | 1 |
| 19 | [자료와 출처를 함께 돌려주는 LCEL 체인 만들기](../site/chapter19/index.html#workshop) | 8 | 검증 | 1 |
| 20 | [두 PDF에 모두 있는 ‘1쪽’ 구별하기](../site/chapter20/index.html#workshop) | 14 | 검증 | 1 |
| 21 | [검색한 두 조각에서 원문 한 구간 복원하기](../site/chapter21/index.html#workshop) | 14 | 검증 | 0 |
| 22 | [FAISS의 검색 번호를 청크 ID에 고정하기](../site/chapter22/index.html#workshop) | 14 | 검증 | 0 |
| 23 | [두 문서가 검색됐을 때 답변용 문맥 고르기](../site/chapter23/index.html#workshop) | 8 | 검증 | 0 |
| 24 | [생성 단계 직전에 빈 문맥 우회하기](../site/chapter24/index.html#workshop) | 9 | 검증 | 1 |
| 25 | [오답의 원인을 검색 전후 두 지점에서 좁히기](../site/chapter25/index.html#workshop) | 9 | 검증 | 0 |
| 26 | [문서 수를 세는 노드를 그래프에 끼워 넣기](../site/chapter26/index.html#workshop) | 7 | 검증 | 1 |
| 27 | [검색어가 그대로면 다시 검색하기 전에 끝내기](../site/chapter27/index.html#workshop) | 7 | 검증 | 2 |
| 28 | [두 번째 답변이 첫 번째 답변을 덮는 문제 고치기](../site/chapter28/index.html#workshop) | 6 | 검증 | 1 |
| 29 | [현재 대화와 바로 전 체크포인트를 따로 열기](../site/chapter29/index.html#workshop) | 6 | 검증 | 1 |
| 30 | [검색과 답변에서 서로 다른 문서가 쓰이지 않게 연결하기](../site/chapter30/index.html#workshop) | 6 | 검증 | 1 |
| 31 | [연장 질문의 근거가 충분한지 검사하는 단계 만들기](../site/chapter31/index.html#workshop) | 7 | 검증 | 1 |
| 32 | [최종 답이 같은 두 구현에서 처음 달라진 단계 찾기](../site/chapter32/index.html#workshop) | 7 | 검증 | 1 |
| 34 | [도구 결과를 모델 노드로 되돌려 루프 완성하기](../site/chapter34/index.html#workshop) | 10 | 검증 | 2 |
| 35 | [평가 질문을 나누기 전에 원문 겹침 찾기](../site/chapter35/index.html#workshop) | 6 | 검증 | 0 |
| 36 | [여러 근거가 필요한 질문의 Recall@k 계산하기](../site/chapter36/index.html#workshop) | 7 | 검증 | 0 |
| 37 | [중첩을 늘려 답의 단서가 같은 청크에 남는지 실험하기](../site/chapter37/index.html#workshop) | 7 | 검증 | 0 |
| 38 | [실제 재정렬기가 ‘예약 3일’을 ‘대출 14일’보다 높게 고른 경우](../site/chapter38/index.html#workshop) | 8 | 검증 | 1 |
| 39 | [평균이 같은 두 설정에서 새로 틀린 문항 찾아내기](../site/chapter39/index.html#workshop) | 6 | 검증 | 0 |
| 40 | [폼을 다시 그려도 지난 답이 중복되지 않는 대화 기록 만들기](../site/chapter40/index.html#workshop) | 9 | 검증 | 1 |
| 41 | [새 대화를 눌렀을 때 화면과 체크포인트의 연결 확인하기](../site/chapter41/index.html#workshop) | 10 | 검증 | 1 |
| 42 | [고정한 질문으로 팀원의 첫 RAG를 인수하기](../site/chapter42/index.html#workshop) | 7 | 검증 | 0 |
| 43 | [과제 제출 안내를 동료가 시험할 수 있는 의뢰로 바꾸기](../site/chapter43/index.html#workshop) | 1 | 기본 입력 검증 | 0 |
| 44 | [정답 근거를 달 수 없는 문항을 평가 묶음에서 찾기](../site/chapter44/index.html#workshop) | 4 | 검증 | 0 |
| 45 | [검색한 문단으로 답과 출처를 함께 만드는 기준선](../site/chapter45/index.html#workshop) | 4 | 기본 입력 검증 | 1 |
| 46 | [Q03을 고친 뒤 처음 보는 표현으로 다시 시험하기](../site/chapter46/index.html#workshop) | 3 | 검증 | 0 |
| 47 | [검색을 한 번만 허용하는 그래프를 실제로 실행하기](../site/chapter47/index.html#workshop) | 4 | 검증 | 2 |
| 48 | [다음 질문에는 이전 답변의 출처가 남지 않게 하기](../site/chapter48/index.html#workshop) | 3 | 검증 | 0 |
| 49 | [실패한 한 요청의 검색과 인용을 따로 채점하기](../site/chapter49/index.html#workshop) | 3 | 검증 | 0 |
| 50 | [후보 원문에 없는 인용으로 회귀 실패 재현하기](../site/chapter50/index.html#workshop) | 4 | 검증 | 1 |
| 51 | [새 폴더에서 같은 입력으로 결과 파일 재현하기](../site/chapter51/index.html#workshop) | 3 | 기본 입력 검증 | 0 |
| 52 | [질문 한 건으로 수정 전후를 설명하는 팀 시연](../site/chapter52/index.html#workshop) | 1 | 기본 입력 검증 | 0 |
| 53 | [사용자별 마지막 문의 한 건 조회하기](../site/chapter53/index.html#workshop) | 7 | 검증 | 0 |
| 54 | [수정 내용을 저장할지 되돌릴지 정하기](../site/chapter54/index.html#workshop) | 9 | 검증 | 1 |
| 55 | [create_agent가 검색 도구를 다시 부르는 순간](../site/chapter55/index.html#workshop) | 10 | 검증 | 1 |
| 56 | [모델이 요청한 검색과 실행한 검색 대조하기](../site/chapter56/index.html#workshop) | 9 | 검증 | 1 |
| 57 | [Skill 문서에 입력·중단 조건·반환 예 작성하기](../site/chapter57/index.html#workshop) | 8 | 검증 | 0 |
| 58 | [요청 한 건에서 실제로 연 Skill 파일 기록하기](../site/chapter58/index.html#workshop) | 8 | 검증 | 1 |
| 59 | [체크포인트에 보관한 기록과 모델에 보낼 대화 창 나누기](../site/chapter59/index.html#workshop) | 7 | 검증 | 0 |
| 60 | [새 대화에서 같은 사람의 선호만 불러오기](../site/chapter60/index.html#workshop) | 9 | 검증 | 1 |
| 61 | [별도 프로세스의 도구를 stdio로 호출하기](../site/chapter61/index.html#workshop) | 7 | 기본 입력 검증 | 1 |
| 62 | [같은 MCP 도구를 HTTP 경유 에이전트에 연결하기](../site/chapter62/index.html#workshop) | 7 | 검증 | 1 |
| 63 | [필수 근거 검색에 선택 도구 하나 연결하기](../site/chapter63/index.html#workshop) | 7 | 검증 | 2 |
| 64 | [재개하면 어느 노드부터 다시 실행될까요?](../site/chapter64/index.html#workshop) | 7 | 기본 입력 검증 | 1 |
| 65 | [분류 후보를 실제 호출 가능 목록과 맞추기](../site/chapter65/index.html#workshop) | 8 | 검증 | 1 |
| 66 | [두 역할 사이에서 근거가 잘못 넘어온 지점 찾기](../site/chapter66/index.html#workshop) | 8 | 검증 | 2 |
| 67 | [같은 사례로 인용 오류 수정 전후 재검증하기](../site/chapter67/index.html#workshop) | 6 | 검증 | 0 |
| 68 | [검색 개수 k를 서비스 함수까지 전달하기](../site/chapter68/index.html#workshop) | 7 | 검증 | 1 |
| 69 | [잘려 도착한 NDJSON 응답에서 답변 복원하기](../site/chapter69/index.html#workshop) | 6 | 검증 | 1 |
| 70 | [문서 업로드에서 공개 가능한 본문까지 한 요청으로 잇기](../site/chapter70/index.html#workshop) | 6 | 검증 | 1 |
| 71 | [이미지 시작 명령과 FastAPI 모듈 연결하기](../site/chapter71/index.html#workshop) | 6 | 검증 | 1 |
| 72 | [DB 준비를 기다리는 Compose 의존성 작성하기](../site/chapter72/index.html#workshop) | 7 | 검증 | 1 |
| 73 | [사용자 필터를 적용한 뒤 가장 가까운 문서 찾기](../site/chapter73/index.html#workshop) | 6 | 검증 | 0 |
| 74 | [EC2 인스턴스와 실제 서비스 주소를 대조하기](../site/chapter74/index.html#workshop) | 7 | 기본 입력 검증 | 1 |
| 75 | [복원한 DB에서 빠진 문서의 소유자와 번호 찾기](../site/chapter75/index.html#workshop) | 5 | 기본 입력 검증 | 1 |
| 76 | [CI가 실제로 회귀 검사를 발견하는지 확인하기](../site/chapter76/index.html#workshop) | 6 | 기본 입력 검증 | 1 |
| 77 | [배포 후보와 복귀 버전에 같은 질문 보내기](../site/chapter77/index.html#workshop) | 6 | 기본 입력 검증 | 1 |
| 78 | [입력 오류를 같은 폼 안에서 설명하기](../site/chapter78/index.html#workshop) | 5 | 기본 입력 검증 | 0 |
| 79 | [요청이 끝나기 전에 다시 눌린 제출 버튼 처리하기](../site/chapter79/index.html#workshop) | 6 | 기본 입력 검증 | 1 |
| 80 | [동일한 제목의 할 일을 구분해 삭제하기](../site/chapter80/index.html#workshop) | 5 | 기본 입력 검증 | 0 |
| 81 | [제목 수정 API에 빈 문자열이 들어오면 어떻게 될까요?](../site/chapter81/index.html#workshop) | 7 | 검증 | 1 |
| 82 | [동일한 검색 조건을 새 DB 연결에서 재현하기](../site/chapter82/index.html#workshop) | 7 | 검증 | 1 |
| 83 | [삭제 뒤 순번이 바뀐 목록에서 잘못된 수정 재현하기](../site/chapter83/index.html#workshop) | 5 | 검증 | 1 |
| 84 | [PATCH에서 생략한 날짜와 지운 날짜 구분하기](../site/chapter84/index.html#workshop) | 7 | 검증 | 1 |
| 85 | [이전 버전 DB로 새 앱을 띄운 뒤 같은 ID 복구하기](../site/chapter85/index.html#workshop) | 7 | 검증 | 1 |
| 86 | [첫 시연 계약서에 질문과 사용자의 마지막 행동 적기](../site/chapter86/index.html#workshop) | 2 | 기본 입력 검증 | 0 |
| 87 | [한 문장이 빠진 대화로 되묻기와 종료를 구분하기](../site/chapter87/index.html#workshop) | 2 | 기본 입력 검증 | 1 |
| 88 | [누락된 출처와 잘못 채운 출처를 따로 검수하기](../site/chapter88/index.html#workshop) | 3 | 검증 | 0 |
| 89 | [공개 시연용 파일에 넣을 열과 행 고르기](../site/chapter89/index.html#workshop) | 3 | 검증 | 0 |
| 90 | [답은 유보했지만 출처가 남은 응답 채점하기](../site/chapter90/index.html#workshop) | 3 | 검증 | 1 |
| 91 | [검색 함수를 요청 한 건을 받는 API에 붙이기](../site/chapter91/index.html#workshop) | 4 | 검증 | 1 |
| 92 | [같은 기준선에서 첫 수정 하나를 고르는 회의](../site/chapter92/index.html#workshop) | 3 | 기본 입력 검증 | 0 |
| 93 | [라우터가 종료시킨 요청을 노드 방문 기록으로 확인하기](../site/chapter93/index.html#workshop) | 3 | 검증 | 1 |
| 94 | [재처리한 문서가 검색 테이블에 중복되는지 확인하기](../site/chapter94/index.html#workshop) | 3 | 검증 | 0 |
| 95 | [조회 함수를 공개용 도구로 감싸고 노출된 인자 확인하기](../site/chapter95/index.html#workshop) | 4 | 기본 입력 검증 | 1 |
| 96 | [근거 카드의 표시와 원문 데이터를 서로 검산하기](../site/chapter96/index.html#workshop) | 4 | 기본 입력 검증 | 1 |
| 97 | [세 턴을 넘긴 뒤 과거 카드의 출처가 그대로인지 검사하기](../site/chapter97/index.html#workshop) | 3 | 기본 입력 검증 | 1 |
| 98 | [입력 정규화 한 줄이 바꾼 문자 범위 남기기](../site/chapter98/index.html#workshop) | 3 | 검증 | 0 |
| 99 | [시간 초과를 한 번 겪은 검색을 같은 요청으로 다시 실행하기](../site/chapter99/index.html#workshop) | 3 | 검증 | 1 |
| 100 | [세션의 마지막 다섯 턴과 최초 만료 시각을 따로 유지하기](../site/chapter100/index.html#workshop) | 3 | 기본 입력 검증 | 1 |
| 101 | [외부 연동 제안에 답하는 기술 결정 메모](../site/chapter101/index.html#workshop) | 2 | 기본 입력 검증 | 0 |
| 102 | [API 소비자가 전송 실패와 답변 유보를 다르게 처리하는지 시험하기](../site/chapter102/index.html#workshop) | 4 | 기본 입력 검증 | 1 |
| 103 | [알파 시연 뒤 한 가지 화면 변경을 고르는 메모](../site/chapter103/index.html#workshop) | 2 | 기본 입력 검증 | 0 |
| 104 | [늦게 도착한 응답이 새 화면을 덮어쓰지 못하게 하기](../site/chapter104/index.html#workshop) | 3 | 검증 | 0 |
| 105 | [사용자가 다시 눌러도 되는지 결정하는 오류 문안](../site/chapter105/index.html#workshop) | 2 | 기본 입력 검증 | 1 |
| 106 | [저장소를 닫았다 다시 열어 요청 기록 찾기](../site/chapter106/index.html#workshop) | 3 | 기본 입력 검증 | 1 |
| 107 | [도움을 받아 찾은 절을 베타 성공으로 셀지 합의하기](../site/chapter107/index.html#workshop) | 2 | 기본 입력 검증 | 0 |
| 108 | [검색 성공과 답변 성공을 한 문항에서 따로 채점하기](../site/chapter108/index.html#workshop) | 3 | 검증 | 1 |
| 109 | [거부 응답에서 공개할 필드를 좁히기](../site/chapter109/index.html#workshop) | 3 | 검증 | 1 |
| 110 | [같은 답을 유지하면서 문서를 준비한 횟수 비교하기](../site/chapter110/index.html#workshop) | 3 | 검증 | 0 |
| 111 | [후보판을 넘기기 전에 기대 문자열을 세 건으로 고정하기](../site/chapter111/index.html#workshop) | 3 | 검증 | 1 |
| 112 | [배포 담당자가 직접 확인할 접속 경로와 데이터 위치](../site/chapter112/index.html#workshop) | 3 | 검증 | 1 |
| 113 | [파일은 읽히지만 마지막 요청이 빠진 복구본 찾아내기](../site/chapter113/index.html#workshop) | 3 | 검증 | 0 |
| 114 | [설명자 없이 실행하는 인수 문서의 첫 화면](../site/chapter114/index.html#workshop) | 2 | 기본 입력 검증 | 0 |
| 115 | [정상 답변 뒤 근거가 없는 질문으로 전환하는 시연 대본](../site/chapter115/index.html#workshop) | 2 | 기본 입력 검증 | 1 |
| 116 | [발표 질의에 답하고 다음 담당자에게 재현 입력 넘기기](../site/chapter116/index.html#workshop) | 2 | 기본 입력 검증 | 0 |
