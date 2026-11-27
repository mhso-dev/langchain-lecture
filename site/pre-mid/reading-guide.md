# 전반부 1~42장 개정 교재

각 장에서 다룰 기능과 직접 확인할 결과를 함께 읽으세요. 1~5장은 [시작 진단](diagnostic/lesson.ipynb) 뒤 문법(A)과 디자인 패턴(B) 중 한 과정을 고르세요. 6장부터는 함께 공부합니다.

실습 묶음을 내려받았다면 압축을 모두 풀고 Jupyter에서 해당 노트북을 여세요.

## 1부 · Python과 Git

| 장 | 본문·실습 | 코드에서 확인할 것 |
|---|---|---|
| 1 | A · [문자열을 정수로 바꿔 시·분·초 더하기](python-basics/lesson.ipynb#cell-id=seconds-14)<br>B · [sorted의 key 바꾸기](python-patterns/lesson.ipynb#cell-id=b08) | 합계를 출력하고 3723과 같은지 검사합니다. B에서는 같은 목록을 두 기준으로 정렬합니다. |
| 2 | A · [리스트의 별칭과 copy() 비교하기](python-basics/lesson.ipynb#cell-id=colors-20)<br>B · [Priority의 동점 순서](python-patterns/lesson.ipynb#cell-id=rule-tie-goal) | 별칭으로 첫 색을 고친 뒤 원본과 복사본의 첫 값을 읽습니다. B에서는 우선순위가 같을 때 원래 순서가 남는지 봅니다. |
| 3 | A · [if와 for로 양수인 짝수 고르기](python-basics/lesson.ipynb#cell-id=filter-14)<br>B · [Factory와 미등록 형식](python-patterns/lesson.ipynb#cell-id=b3-transfer-04) | 0이 빠지고 두 번 나온 6이 두 번 남았는지 비교합니다. B에서는 지원하지 않는 형식이 어떤 예외를 내는지 봅니다. |
| 4 | A · [함수의 기본 인자와 전달한 목록 구분하기](python-basics/lesson.ipynb#cell-id=calls-14)<br>B · [Decorator와 예외 기록](python-patterns/lesson.ipynb#cell-id=b4-transfer-04) | 목록을 생략한 두 호출과 shared를 넘긴 호출의 결과를 비교합니다. B에서는 빈 입력을 거절할 때 기록이 남는지 확인합니다. |
| 5 | A · [한 객체의 상태만 초기화하기](python-basics/lesson.ipynb#cell-id=counter-08)<br>B · [호출 순서와 이력 비교](python-patterns/lesson.ipynb#cell-id=b5-transfer-02) | a.reset() 뒤 두 카운터에서 a만 0이 됐는지 읽습니다. B에서는 두 창구의 출력이 같아도 기록의 공백이 다른 이유를 찾습니다. |
| 6 | [두 작업 폴더에서 Git 상태 읽기](team-git/lesson.ipynb#cell-id=git-17) | 첫 폴더의 미커밋 파일과 둘째 폴더의 마지막 커밋에 든 파일을 구분합니다. |
| 7 | [받아 온 커밋을 로컬 main에 반영하기](team-git/lesson.ipynb#cell-id=git-sync-06) | fast-forward 병합 뒤 파일 내용과 최근 커밋 제목을 대조합니다. |

## 2부 · OpenAI SDK와 챗봇

| 장 | 본문·실습 | 코드에서 확인할 것 |
|---|---|---|
| 8 | [responses.create()로 첫 요청 보내기](prompt-workshop/lesson.ipynb#cell-id=walk-9-1) | ‘사과’를 번역해 reply.output_text를 읽은 뒤 입력을 ‘포도’로 바꿉니다. |
| 9 | [ask에 지시와 원문 따로 넣기](prompt-workshop/lesson.ipynb#cell-id=prompt-19) | 원문을 고정하고 회원용·진행자용 지시에서 답이 어떻게 달라지는지 봅니다. |
| 10 | [프롬프트에 빈 정보의 표기 정하기](prompt-workshop/lesson.ipynb#cell-id=prompt-27) | 제출 마감만 적힌 문장에서 모임 일시와 장소가 미정으로 나오는지 확인합니다. |
| 11 | [같은 질문을 새 대화에 보내기](chat-workshop/lesson.ipynb#cell-id=exercise11) | 빈 목록에 보낸 질문과 답의 role을 출력해 이전 대화가 섞였는지 확인합니다. |
| 12 | [st.chat_input과 재실행 관찰하기](chat-workshop/lesson.ipynb#cell-id=echo-first) | 한 문장을 보내고 체크박스를 두 번 바꿔도 말풍선이 하나인지 봅니다. |
| 13 | [버튼으로 세션 상태 초기화하기](chat-workshop/lesson.ipynb#cell-id=exercise13) | 답을 한 번 받은 뒤 새 대화를 누르고 후속 질문을 보내 요청 수 1→0→1을 확인합니다. |

## 3부 · LCEL과 문서 검색

| 장 | 본문·실습 | 코드에서 확인할 것 |
|---|---|---|
| 14 | [ChatPromptTemplate.invoke()로 두 빈칸 채우기](../chapter14.ipynb#cell-id=rag-14-09) | 단어와 언어를 딕셔너리로 넘겨 번역 요청 문장을 출력합니다. |
| 15 | [PdfReader로 지정한 쪽의 원문 읽기](../chapter15.ipynb#cell-id=rag-15-08) | 화면의 2쪽을 pages 인덱스로 바꿔 서로 다른 예외 조항을 찾습니다. |
| 16 | [page_chunks로 조각 크기 비교하기](../chapter16.ipynb#cell-id=rag-16-09) | 60과 180에서 같은 숫자가 있는 조각의 ID와 앞뒤 문장을 읽습니다. |
| 17 | [retrieve로 표현이 다른 질문 검색하기](../chapter17.ipynb#cell-id=rag-17-09) | 색인과 k를 고정하고 세 질문에서 상위 세 쪽의 ID를 비교합니다. |
| 18 | [open_index로 원본과 수정본 구별하기](../chapter18.ipynb#cell-id=rag-18-09) | 쪽 하나만 바꾼 뒤 컬렉션 이름과 문서 수를 읽습니다. |
| 19 | [rag.invoke()의 답과 근거 읽기](../chapter19.ipynb#cell-id=rag-19-10) | 서로 다른 두 질문에 나온 답을 각 실행의 문서 ID와 대조합니다. |
| 20 | [날짜로 유효한 판본 고르기](../chapter20.ipynb#cell-id=rag-20-08) | 같은 질문을 3월 31일과 4월 1일에 적용한 뒤 질문 조건만 바꿉니다. |
| 21 | [검색 결과를 근거로 답하거나 보류하기](../chapter21.ipynb#cell-id=rag-21-08) | 세 질문 각각에 대해 검색한 쪽과 실제 답이 허용하는 결론을 대조합니다. |
| 22 | [page_scores로 검색 결과 채점하기](../chapter22.ipynb#cell-id=rag-22-09) | 첫 후보가 정답인 경우에도 정답 두 쪽 중 몇 쪽을 찾았는지 따로 셉니다. |
| 23 | [rerank 전후의 순서와 후보 집합 비교하기](../chapter23.ipynb#cell-id=rag-23-09) | 정답 쪽을 제외한 뒤 재정렬하여 순위와 ID 집합을 각각 비교합니다. |
| 24 | [st.cache_data로 함수 재실행 확인하기](../chapter24.ipynb#cell-id=first-feature) | 같은 입력으로 화면을 다시 그린 뒤 새 문구를 넣고 터미널의 계산 기록을 봅니다. |

## 4부 · OpenAI SDK로 워크플로 만들기

| 장 | 본문·실습 | 코드에서 확인할 것 |
|---|---|---|
| 25 | [두 번의 ask로 번역과 예문 연결하기](../chapter25.ipynb#cell-id=first-feature) | 첫 답인 단어와 그 단어를 받아 만든 예문을 나란히 읽습니다. |
| 26 | [라벨로 분기하고 선택된 처리 확인하기](../chapter26.ipynb#cell-id=first-feature) | 분류한 라벨을 출력하고 번역·기타·예상 밖 라벨을 구분합니다. |
| 27 | [같은 원문에 서로 다른 지시 적용하기](../chapter27.ipynb#cell-id=first-feature) | 번역과 말투 판정에 각각 어떤 입력이 들어가는지 비교합니다. |
| 28 | [실패한 비동기 작업만 다시 호출하기](../chapter28.ipynb#cell-id=w28-14) | 실패 이름을 모아 재시도하고 처음 성공한 결과가 남았는지 검사합니다. |
| 29 | [read_plan으로 계획과 원문 대조하기](../chapter29.ipynb#cell-id=w29-15) | 작업마다 근거와 질문을 함께 읽고 빠진 조건을 찾습니다. |
| 30 | [평가 의견을 받아 초안 고치기](../chapter30.ipynb#cell-id=first-feature) | 첫 호출의 의견과 둘째 호출의 수정본을 각각 출력합니다. |
| 31 | [review_until의 종료 이유 읽기](../chapter31.ipynb#cell-id=w31-15) | 조건 하나를 뺀 두 번째 초안에서 종료 사유와 수정 횟수를 비교합니다. |
| 32 | [process의 단계별 기록 읽기](../chapter32.ipynb#cell-id=w32-16) | 질문 한 건에서 경로·종료·답변과 모델 호출 기록 수를 읽습니다. |

## 5부 · LangGraph로 검색과 답변 연결하기

| 장 | 본문·실습 | 코드에서 확인할 것 |
|---|---|---|
| 33 | [노드가 분류하는 경계값 확인하기](../chapter33.ipynb#cell-id=graph-33-13) | 길이 9·10·11에서 count와 label을 함께 출력합니다. |
| 34 | [조건부 간선의 종료 지점 확인하기](../chapter34.ipynb#cell-id=graph-34-12) | 항상 긴 답을 주는 함수를 연결해 실제로 거친 노드를 읽습니다. |
| 35 | [thread_id로 대화 상태 구분하기](../chapter35.ipynb#cell-id=graph-35-12) | 기록이 있는 스레드와 아직 쓰지 않은 스레드의 메시지를 비교합니다. |
| 36 | [검색 노드가 돌려준 원문의 판본 확인하기](../chapter36.ipynb#cell-id=graph-36-14) | 같은 쪽 번호라도 기간이 다른 두 문서에서 출처와 판본을 찾습니다. |
| 37 | [판본과 인용이 함께 맞는지 검사하기](../chapter37.ipynb#cell-id=graph-37-12) | 인용문은 그대로 두고 쪽 ID만 바꿔 상태값을 비교합니다. |
| 38 | [재검색도 실패한 경우의 기록 읽기](../chapter38.ipynb#cell-id=graph-38-15) | 두 번 모두 잘못된 후보를 주고 답·인용·두 검색어를 확인합니다. |
| 39 | [st.button으로 버튼 클릭만 기록하기](../chapter39.ipynb#cell-id=first-feature) | 버튼과 체크박스를 번갈아 눌러 기록이 0→1→1→2로 변하는지 확인합니다. |

## 6부 · LangSmith로 품질 확인하기

| 장 | 본문·실습 | 코드에서 확인할 것 |
|---|---|---|
| 40 | [실행 결과와 참고 답을 분리해 기록하기](../chapter40.ipynb#cell-id=ls40-17) | D03의 원문 파일·쪽·기대 행동·참고 답을 적어 실제 실행과 비교합니다. |
| 41 | [쪽을 맞힌 답의 내용도 채점하기](../chapter41.ipynb#cell-id=ls41-20) | 같은 쪽을 인용하면서 두 사실 중 하나만 틀린 답을 만들어 봅니다. |
| 42 | [정답 수가 같은 두 구현의 실패 비교하기](../chapter42.ipynb#cell-id=ls42-work-1) | 각각의 답을 따른 사용자가 어떤 행동을 하게 되는지 적고 채택 여부를 판단합니다. |
