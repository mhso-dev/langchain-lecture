# 1–116장 개념 애니메이션 전수 검수

2026-11-24 · 비교 기준 `6ab77b5`. 학생용 HTML 116장과 대응 노트북 116권을 장별로 대조했다. 같은 입력에서 결과가 달라지는 이유를 화면으로 읽을 수 있는지, 절차 재생을 없앤 뒤에도 원래 예제와 출력이 남는지 확인했다.

본문의 기존 개념 장면 275개 중 255개를 걷어내고 예제 설명을 남겼다. 상태·경계·순위의 변화를 보여 주는 20개는 보존했다. 별도로 재생하던 보충 사례 35개는 웹에서 펼쳐 읽고 노트북에서도 같은 값을 읽을 수 있게 바꿨다. 새 웹 실험은 11개다. 116장의 기존 띄어쓰기 실험, 12장의 그림 모음, 별도 시뮬레이션 진입점 8곳도 검사했다.

| 장 | 대조한 개념 | 기존 장면 제거 / 보존 | 보충 사례 전환 | 실험·자료 |
|---|---|---:|---:|---|
| [1](../site/chapter01/index.html) | 셀의 편집 내용·커널 값·마지막 출력 | 4 / 0 | 0 | [새 실험](https://langchain-lecture.vercel.app/chapter01/index.html#concept-lab) · 사례 화면 |
| [2](../site/chapter02/index.html) | 조건에 맞는 행을 더한 70 | 3 / 0 | 1 | 본문 예제 |
| [3](../site/chapter03/index.html) | 출력 30과 반환값 None, 반환한 30으로 계산한 40 | 3 / 0 | 1 | [새 실험](https://langchain-lecture.vercel.app/chapter03/index.html#concept-lab) |
| [4](../site/chapter04/index.html) | 두 인스턴스의 서로 다른 done 값 | 3 / 0 | 1 | 사례 화면 |
| [5](../site/chapter05/index.html) | 중복을 뺀 ID와 합계 90분 | 4 / 0 | 1 | 본문 예제 |
| [6](../site/chapter06/index.html) | 요청 실패·JSON 오류·필드 값 false | 3 / 0 | 1 | 본문 예제 |
| [7](../site/chapter07/index.html) | 반복문 안에서 합계를 초기화하면 남는 마지막 값 | 3 / 0 | 0 | 본문 예제 |
| [8](../site/chapter08/index.html) | 회의의 확정 일정과 미확정 비용 | 3 / 0 | 0 | 본문 예제 |
| [9](../site/chapter09/index.html) | 참가비와 공개되지 않은 신청 주소 | 3 / 0 | 0 | 본문 예제 |
| [10](../site/chapter10/index.html) | 참가자 20명과 좌석 30석이 가리키는 대상 | 3 / 0 | 1 | 사례 화면 |
| [11](../site/chapter11/index.html) | 모의 응답과 실제 요청의 구별 | 3 / 0 | 0 | 본문 예제 |
| [12](../site/chapter12/index.html) | null이 든 항목과 누락된 키, 완료 이벤트 유무 | 9 / 1 | 0 | 별도 그림 모음·완료 이벤트 GIF · 내려받기 자료 |
| [13](../site/chapter13/index.html) | 첫 응답에서 다음 입력으로 이어지는 필드 | 3 / 0 | 1 | 본문 예제 |
| [14](../site/chapter14/index.html) | 결제·기술·보충 질문별 호출 차이 | 3 / 0 | 1 | 본문 예제 |
| [15](../site/chapter15/index.html) | 도구 명세의 weekday와 weekend | 3 / 0 | 0 | 본문 예제 |
| [16](../site/chapter16/index.html) | 요청과 도구 결과를 연결하는 call_id | 3 / 0 | 2 | 본문 예제 |
| [17](../site/chapter17/index.html) | 중복 호출 ID와 모델 3회·도구 2회 | 3 / 0 | 1 | 본문 예제 |
| [18](../site/chapter18/index.html) | 잘못된 도구 입력과 빈 조회 결과 | 3 / 0 | 0 | 본문 예제 |
| [19](../site/chapter19/index.html) | 스트림 조각과 합친 문자열 | 3 / 0 | 0 | 본문 예제 |
| [20](../site/chapter20/index.html) | library-2의 근거가 있는 답과 답변 유보 | 3 / 0 | 1 | 본문 예제 |
| [21](../site/chapter21/index.html) | 크기 16·겹침 4에서 경계에 남는 어절 | 2 / 1 | 0 | 별도 조작 화면 |
| [22](../site/chapter22/index.html) | 세 축의 거리, 벡터 위치와 문서 ID | 2 / 1 | 0 | 별도 조작 화면 |
| [23](../site/chapter23/index.html) | 질문별 첫 결과의 ID와 쪽 | 3 / 0 | 0 | 본문 예제 |
| [24](../site/chapter24/index.html) | 인용 ID 포함 여부와 빈 검색의 모델 호출 0회 | 3 / 0 | 1 | 본문 예제 |
| [25](../site/chapter25/index.html) | 수정 전후 같은 질문의 기대 근거 비교 | 3 / 0 | 0 | 본문 예제 |
| [26](../site/chapter26/index.html) | 부분 갱신 뒤에 남는 question·documents·answer | 2 / 0 | 1 | 본문 예제 |
| [27](../site/chapter27/index.html) | 두 번 시도한 뒤 종료하는 조건 | 1 / 1 | 0 | 본문 예제 |
| [28](../site/chapter28/index.html) | 메시지 덮어쓰기·누적과 같은 ID로 수정하기 | 1 / 1 | 0 | 본문 예제 |
| [29](../site/chapter29/index.html) | 스레드 A와 B에 보관한 대화 이력 | 1 / 1 | 1 | 본문 예제 |
| [30](../site/chapter30/index.html) | 검색 문장에 대응하는 출처 필드 | 2 / 0 | 0 | 본문 예제 |
| [31](../site/chapter31/index.html) | 빈 목록·시간 초과·인용 불일치 | 2 / 0 | 0 | [새 실험](https://langchain-lecture.vercel.app/chapter31/index.html#concept-lab) |
| [32](../site/chapter32/index.html) | 같은 입력에서 LCEL과 그래프가 처음 달라지는 위치 | 2 / 0 | 0 | 본문 예제 |
| [33](../site/chapter33/index.html) | 도구 명세와 요청·응답 ID의 짝 | 2 / 0 | 1 | 본문 예제 |
| [34](../site/chapter34/index.html) | 도구 호출 0회인 경우의 종료 조건 | 2 / 0 | 1 | 본문 예제 |
| [35](../site/chapter35/index.html) | 기대 문서 ID와 개발·보류 평가 문항 | 2 / 0 | 0 | 본문 예제 |
| [36](../site/chapter36/index.html) | 기대 근거 위치에 따라 달라지는 지표 | 1 / 1 | 0 | 별도 조작 화면 |
| [37](../site/chapter37/index.html) | 문자 경계와 겹침 길이가 바꾸는 청크 | 1 / 2 | 0 | 별도 조작 화면 |
| [38](../site/chapter38/index.html) | 후보 안 순위 역전과 후보 밖 문서 | 1 / 1 | 2 | 별도 조작 화면 |
| [39](../site/chapter39/index.html) | 개발 문항 기준선과 후보의 결과 | 2 / 0 | 0 | 본문 예제 |
| [40](../site/chapter40/index.html) | 입력 중인 질문과 제출된 질문 | 2 / 0 | 0 | 내려받기 자료 |
| [41](../site/chapter41/index.html) | 화면 세션과 thread_id | 3 / 0 | 0 | 내려받기 자료 |
| [42](../site/chapter42/index.html) | 검색 결과와 표시된 출처의 일치 | 2 / 0 | 0 | 본문 예제 |
| [43](../site/chapter43/index.html) | 답변할 수 있는 문서 범위 | 2 / 0 | 0 | 본문 예제 |
| [44](../site/chapter44/index.html) | Q01의 2쪽 근거와 Q04의 무근거 질문 | 2 / 0 | 0 | 본문 예제 |
| [45](../site/chapter45/index.html) | 근거 문서가 있는데도 검색 결과가 빈 Q03 | 2 / 0 | 0 | 본문 예제 |
| [46](../site/chapter46/index.html) | 검색한 3쪽과 인용한 2쪽 | 2 / 0 | 0 | 본문 예제 |
| [47](../site/chapter47/index.html) | 재시도 조건과 남은 탐색 횟수 | 2 / 0 | 0 | 본문 예제 |
| [48](../site/chapter48/index.html) | 다음 질문에서 직전 출처가 남는 오류 | 1 / 1 | 0 | 내려받기 자료 |
| [49](../site/chapter49/index.html) | 검색·인용 실패와 비용·지연 미측정 | 2 / 0 | 0 | 본문 예제 |
| [50](../site/chapter50/index.html) | Q03 수정 뒤 Q01에서 발생할 수 있는 회귀 | 2 / 0 | 0 | 본문 예제 |
| [51](../site/chapter51/index.html) | 새 폴더 실행과 새 환경 검증의 범위 | 2 / 0 | 0 | 본문 예제 |
| [52](../site/chapter52/index.html) | 발표와 개인 회고의 근거 기록 | 2 / 0 | 0 | 본문 예제 |
| [53](../site/chapter53/index.html) | 행을 한정하고 결합한 뒤 집계한 값 | 3 / 0 | 1 | 본문 예제 |
| [54](../site/chapter54/index.html) | 확정 직전 값과 rollback으로 돌아가는 값 | 3 / 0 | 0 | [새 실험](https://langchain-lecture.vercel.app/chapter54/index.html#concept-lab) |
| [55](../site/chapter55/index.html) | c1·c2 요청과 반환 결과의 짝 | 3 / 0 | 1 | 본문 예제 |
| [56](../site/chapter56/index.html) | 양수 k·허용 출처·호출 한도 | 3 / 0 | 0 | 본문 예제 |
| [57](../site/chapter57/index.html) | 작업에 맞는 스킬 본문 | 3 / 0 | 1 | 본문 예제 |
| [58](../site/chapter58/index.html) | 선택한 본문과 참고자료의 공개 범위 | 3 / 0 | 1 | 본문 예제 |
| [59](../site/chapter59/index.html) | 최근 대화 창에서 빠지는 장소와 요약에서 누락된 기한 | 1 / 1 | 0 | 별도 조작 화면 |
| [60](../site/chapter60/index.html) | 사용자와 language로 구성한 복합 키 | 3 / 0 | 0 | [새 실험](https://langchain-lecture.vercel.app/chapter60/index.html#concept-lab) |
| [61](../site/chapter61/index.html) | 등록한 함수와 주말 시간표 | 2 / 0 | 1 | 본문 예제 |
| [62](../site/chapter62/index.html) | 세션 수명과 요일 정합성 | 3 / 0 | 1 | 본문 예제 |
| [63](../site/chapter63/index.html) | 근거 0건에서 생성을 생략할 조건 | 2 / 0 | 1 | 본문 예제 |
| [64](../site/chapter64/index.html) | 승인 전과 승인 뒤의 등록 건수 | 0 / 2 | 1 | 본문 예제 |
| [65](../site/chapter65/index.html) | 분류별 허용 도구 | 3 / 0 | 0 | 본문 예제 |
| [66](../site/chapter66/index.html) | 같은 질문에서 역할별로 달라지는 호출 수 | 2 / 0 | 1 | 본문 예제 |
| [67](../site/chapter67/index.html) | 인용 ID의 유효성과 주장의 정확성, 평가 분모 | 2 / 0 | 1 | 본문 예제 |
| [68](../site/chapter68/index.html) | 형식 오류와 빈 근거 | 2 / 0 | 0 | 본문 예제 |
| [69](../site/chapter69/index.html) | 전부 보이는 문장과 클라이언트가 확인한 done | 2 / 0 | 1 | [새 실험](https://langchain-lecture.vercel.app/chapter69/index.html#concept-lab) · 별도 조작 화면 |
| [70](../site/chapter70/index.html) | 문서 상태와 현재 턴 출처 | 2 / 0 | 0 | 본문 예제 |
| [71](../site/chapter71/index.html) | 이미지 변경과 컨테이너 재시작 | 2 / 0 | 1 | 본문 예제 |
| [72](../site/chapter72/index.html) | 컨테이너 교체 뒤 볼륨에 남은 데이터 | 3 / 0 | 1 | 본문 예제 |
| [73](../site/chapter73/index.html) | 벡터 거리 0과 1.414 및 순위 | 1 / 0 | 0 | 별도 조작 화면 · 노트북 거리 GIF |
| [74](../site/chapter74/index.html) | 로컬 이미지와 EC2에서 관찰한 증거 | 2 / 0 | 0 | 본문 예제 |
| [75](../site/chapter75/index.html) | 행 수가 같아도 달라진 본문 값 | 2 / 0 | 0 | [새 실험](https://langchain-lecture.vercel.app/chapter75/index.html#concept-lab) |
| [76](../site/chapter76/index.html) | 실패·건너뛰기·PR 게시 조건 | 2 / 0 | 1 | 본문 예제 |
| [77](../site/chapter77/index.html) | 태그와 digest, 복원할 버전 | 2 / 0 | 1 | 본문 예제 |
| [78](../site/chapter78/index.html) | 입력칸과 버튼의 실제 간격과 줄바꿈 | 2 / 0 | 0 | [새 실험](https://langchain-lecture.vercel.app/chapter78/index.html#concept-lab) |
| [79](../site/chapter79/index.html) | 응답 도착과 응답 본문 읽기 | 2 / 0 | 1 | 본문 예제 |
| [80](../site/chapter80/index.html) | 수용 조건과 변경 diff | 2 / 0 | 0 | 본문 예제 |
| [81](../site/chapter81/index.html) | T1과 HTTP 반환별 화면 상태 | 2 / 0 | 0 | 내려받기 자료 |
| [82](../site/chapter82/index.html) | 제목 속 문자 %와 LIKE의 % | 2 / 0 | 0 | [새 실험](https://langchain-lecture.vercel.app/chapter82/index.html#concept-lab) |
| [83](../site/chapter83/index.html) | 같은 요청을 두 번 보낸 뒤의 toggle과 대입 | 0 / 2 | 0 | 본문 예제 |
| [84](../site/chapter84/index.html) | 기존 행에 새 필드를 적용할 때 허용할 열 | 2 / 0 | 0 | 본문 예제 |
| [85](../site/chapter85/index.html) | DB 버전과 새 인스턴스에서 읽은 데이터 | 2 / 0 | 0 | 본문 예제 |
| [86](../site/chapter86/index.html) | 교대 담당자의 질문과 인계 메모 | 2 / 0 | 0 | 본문 예제 |
| [87](../site/chapter87/index.html) | 답을 받은 뒤 사용자가 취하는 행동 | 2 / 0 | 0 | 본문 예제 |
| [88](../site/chapter88/index.html) | 출처 하나를 표시하는 수용 조건 | 2 / 0 | 0 | 본문 예제 |
| [89](../site/chapter89/index.html) | 허용 자료 범위와 오프라인 사본 | 2 / 0 | 0 | 본문 예제 |
| [90](../site/chapter90/index.html) | Q01–RULE-A의 짝과 보류 문항 | 2 / 0 | 0 | 본문 예제 |
| [91](../site/chapter91/index.html) | 점검 일정에 따른 RULE-A의 적용 조건 | 2 / 0 | 0 | 본문 예제 |
| [92](../site/chapter92/index.html) | 첫 평가 2/7의 기대 출처와 실제 출처 | 2 / 0 | 0 | 본문 예제 |
| [93](../site/chapter93/index.html) | 근거 유무에 따른 답변 상태와 출처 | 2 / 0 | 0 | 본문 예제 |
| [94](../site/chapter94/index.html) | 공백과 개행의 원문 지문·정규화된 본문 | 2 / 0 | 0 | [새 실험](https://langchain-lecture.vercel.app/chapter94/index.html#concept-lab) |
| [95](../site/chapter95/index.html) | 허용한 문서 안에서 0건을 해석하는 기준 | 2 / 0 | 0 | 본문 예제 |
| [96](../site/chapter96/index.html) | 답의 절·쪽·개정판과 모호한 설비명 | 2 / 0 | 0 | 본문 예제 |
| [97](../site/chapter97/index.html) | Q01에서 Q03·Q04로 바뀔 때 현재 질문의 근거 | 1 / 1 | 0 | 본문 예제 |
| [98](../site/chapter98/index.html) | 기존 7문항과 추가 3문항 점수 | 2 / 0 | 0 | 본문 예제 |
| [99](../site/chapter99/index.html) | 두 번째 시도의 성공과 횟수 소진 | 0 / 2 | 0 | 본문 예제 |
| [100](../site/chapter100/index.html) | 같은 세션 이름을 쓴 사용자 사이의 격리·만료 | 2 / 0 | 0 | 본문 예제 |
| [101](../site/chapter101/index.html) | 일정 데이터와 조회 권한의 유무 | 2 / 0 | 0 | 본문 예제 |
| [102](../site/chapter102/index.html) | /p1/ask 입력과 저장 실패 응답 | 2 / 0 | 0 | 본문 예제 |
| [103](../site/chapter103/index.html) | 힌트 유무에 따른 §2.1 찾기 모의 관찰 | 2 / 0 | 0 | 본문 예제 |
| [104](../site/chapter104/index.html) | 새 질문 대기 중 이전 답·출처 초기화 | 1 / 1 | 0 | 사례 화면 |
| [105](../site/chapter105/index.html) | 출처 없음과 저장 여부 불확실에 맞는 후속 행동 | 2 / 0 | 0 | 본문 예제 |
| [106](../site/chapter106/index.html) | 답변 생성과 저장 실패의 독립된 상태 | 2 / 0 | 0 | 본문 예제 |
| [107](../site/chapter107/index.html) | 관찰과 해석, 시도 수와 완료 수 | 2 / 0 | 0 | 본문 예제 |
| [108](../site/chapter108/index.html) | 서로 다른 ID에서 정규화 뒤 같은 질문 | 2 / 0 | 0 | 본문 예제 |
| [109](../site/chapter109/index.html) | 자기 기록을 조회할 수 있는 소유자 범위 | 2 / 0 | 0 | 본문 예제 |
| [110](../site/chapter110/index.html) | 고정된 서비스 측정 구간과 추가 대기 시간 | 2 / 0 | 0 | [새 실험](https://langchain-lecture.vercel.app/chapter110/index.html#concept-lab) |
| [111](../site/chapter111/index.html) | 회귀 입력 JSON과 배포 결정 기록 | 2 / 0 | 0 | 내려받기 자료 |
| [112](../site/chapter112/index.html) | 공개 주소 응답과 재배포 뒤 데이터 보존 | 2 / 0 | 0 | 본문 예제 |
| [113](../site/chapter113/index.html) | r2~r6 복원과 r0의 중복 방지 한계 | 2 / 0 | 0 | 본문 예제 |
| [114](../site/chapter114/index.html) | 새 담당자의 점검 질문과 인계 문서 두 개 | 2 / 0 | 0 | 내려받기 자료 |
| [115](../site/chapter115/index.html) | 일반 질문과 근거 없는 질문의 발표 사례 | 2 / 0 | 0 | 본문 예제 |
| [116](../site/chapter116/index.html) | 장비A·장비B·장비AB의 띄어쓰기 수정 전후 | 0 / 0 | 0 | 기존 띄어쓰기 실험 |

## 검증 범위

네 구간(1–30, 31–60, 61–90, 91–116)을 독립적으로 재검수했다. 변경 전후 코드 셀 429개의 코드, 저장된 출력과 실행 횟수를 대조했다. 웹의 127개 HTML에서 내부 링크·앵커·노트북·시뮬레이션 경로를 검사하고 노트북의 마크다운 첨부 참조도 검사했다. 기존 예제의 외부 API 호출과 실제 수업 환경에서의 학습 효과는 이번 시각 자료 검수 범위 밖이다.

새 실험 11개는 배포용 HTML과 JavaScript를 DOM 환경에 로드해 버튼·슬라이더의 입력과 출력을 확인했다. 116장의 세 질문은 수정 전후 6가지 답과 규정 ID를 기준 기록과 대조했다. 한국어 문안은 수업용 산문으로 읽으며 노트북의 조건·수치·코드와 최종 화면 문구를 다시 대조했다. 외부 맞춤법 서비스에는 원문을 전송하지 않았다.
