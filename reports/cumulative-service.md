# 68~85장 서비스와 평가 실습

67장의 테스트 입력을 HTTP 요청으로 보내고, 80장의 승인 로그와 82장의 후보 판본을 85장의 팀 인수 파일까지 이어 쓴다. 선행 파일이 없을 때는 장별 제공 입력을 사용한다. [새 커널의 장별 실행 출력](cumulative-service-execution.json) · [실습 입출력과 장별 경로](cumulative-service-cases.json)

| 장 | 처음 확인할 기능 | 저장할 파일 | 예제와 변형의 실제 관찰값 | 시작본·풀이 코드 셀 |
|---:|---|---|---|---:|
| 68 | TestClient로 대출 문의 한 건 보내기 | `service-lab/api.json` | 200 loan-01 · 422 k | 11 / 11 |
| 69 | StreamingResponse의 완료 사건에서 답변 확정하기 | `service-lab/stream.json` | ['start', 'delta', 'done'] · False True | 10 / 10 |
| 70 | SQLite에 완료한 대화 한 건 저장하기 | `service-lab/stored.json` | loan-demo loan-01 · 1 | 10 / 10 |
| 71 | Dockerfile에 API 시작 모듈과 포트 지정하기 | `service-lab/container.json` | loan-demo loan-01 · main:app 8000 | 10 / 10 |
| 72 | Compose에서 포트와 DB 볼륨 확인하기 | `service-lab/compose.json` | 127.0.0.1:8080:8000 course-pg:/var/lib/postgresql/data · course-pg True | 11 / 11 |
| 73 | 문서 ID와 거리로 pgvector 검색 결과 검산하기 | `service-lab/nearest.json` | [('loan-01', 0.0), ('return-note', 1.41)] · return-note | 11 / 11 |
| 74 | 배포 점검에서 HTTP 상태와 본문 따로 검사하기 | `service-lab/probe.json` | http://127.0.0.1:8080/turn True · False | 11 / 11 |
| 75 | SQLite 백업 사본에서 원문까지 대조하기 | `service-lab/restore.json` | True loan-01 · False | 11 / 11 |
| 76 | unittest로 복원 확인을 CI 검사로 옮기기 | `service-lab/ci.json` | test_restore.RestoreTest.test_restored_row 0 · True True | 12 / 12 |
| 77 | SHA-256으로 승인한 후보와 실행할 후보 대조하기 | `service-lab/candidate.json` | True 64 · False | 10 / 10 |
| 78 | HTML 폼에서 검사할 후보 식별하기 | `service-lab/form.json` | ['1', '2'] · 2 revision-b | 9 / 9 |
| 79 | fetch 요청 본문에 선택한 ID 담기 | `service-lab/selection.json` | {'id': 2, 'done': True} revision-b · True True | 10 / 10 |
| 80 | 버전 검사로 투두 변경 한 번만 승인하기 | `service-lab/approval.json` | 200 409 1 · False 0 | 9 / 9 |
| 81 | 검색 단계에서 처음 틀린 값을 기록하기 | `service-lab/evaluation/baseline.json` | A1 30 [200, 409] · A1 | 7 / 7 |
| 82 | 동일 질문에서 정답 순위와 인용 지지 나눠 채점하기 | `service-lab/evaluation/ranking.json` | {'recall': 1.0, 'mrr': 0.5} {'recall': 1.0, 'mrr': 1.0} · True False | 7 / 7 |
| 83 | 승인 경로와 실제 변경 횟수 함께 검사하기 | `service-lab/evaluation/trajectory.json` | True 1 · False | 7 / 7 |
| 84 | 같은 시험 사례로 배포 후보의 회귀 판정하기 | `service-lab/evaluation/gate.json` | july-deadline 시험 배포 · 보류 | 6 / 6 |
| 85 | 실패 질문 재실행 뒤 팀 인수 파일 만들기 | `service-lab/evaluation/release.json` | 인계 90 [30, 90] · True | 7 / 7 |

독립 검수자가 54장에서 기간을 21일로 바꾼 자료를 67장과 68장의 요청으로 넘겼다. 75장의 복원 검사는 실제 SQLite 사본을 읽었고, 76장의 테스트는 제목이 같은 투두 두 개 중 ID 2만 바꿔야 통과했다. 80장의 재승인 거절은 중복 쓰기를 남기지 않았다. 83장이 80장의 사건을 다시 읽고 85장은 82장의 후보 판본으로 별도 질문을 풀었다. 86장이 읽은 실제 결과는 [프로젝트 검수 기록](cumulative-projects.md)에 있다.

처음 재실행할 때 75장에서 닫힌 연결을 다시 사용하고 82장에서 다른 셀의 변수를 덮어쓰는 오류를 바로잡았다. 학생용·풀이용 노트북 각각 18개를 새 커널에서 다시 실행하고 최종 배포 파일의 SHA-256과 비교했다. 69·73·76·77장은 출력 해설 네 문장의 주어와 검사 대상을 명확히 했다. 한국어 전후 비교의 수치·인용·격식 검사는 통과했고 전체 문자 변경률은 0.4%였다. 낮은 변경률 경고 뒤 직접 정독했다. 공개 범위가 확인되지 않아 외부 맞춤법 검사는 생략했다.

## 확인 필요 항목

Docker 소켓에 연결할 권한이 없어 컨테이너 실행을 검증하지 못했다. 실제 PostgreSQL·pgvector, EC2·레지스트리·GitHub Actions, 학생의 Codex 계정, LangSmith의 원격 평가·추적과 시험 배포는 각각 수업 환경에서의 확인이 남았다. 로컬 테스트 결과와 팀이 클라우드에서 관찰할 결과는 구분해 기록했다.
