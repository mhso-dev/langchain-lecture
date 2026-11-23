# 115–116 공개 인계 요약 · 114 정식 교재

프로젝트는 PROJECT-EQUIPMENT-01, 문서 rules-v1, 모듈 normalization-v1입니다. 공개 개발 기본 eval-v1 7개와 확장 eval-v1-dev98-v1 3개를 보존합니다. 새 인증·DB·외부 모델을 추가하지 않았습니다.

## 전달 파일과 경로

- 이 요약: materials/chapter114/examples/HANDOFF_PUBLIC.md
- 현재 입력·검수 범위: CURRENT_INPUTS.md와 FULL_INPUT_JOIN.json
- 정식 소비 목록: OPERATIONS_CONSUMER.json. files의 모든 상대 경로와 manifest 자체를 examples 기준으로 복사합니다.
- 같은 앱: input106/project-ui/serve_ui.py, 진입 serve_ui:create_app. UI /ui/index.html, API /p1입니다. 받은 106 PACKAGE는 8f6cfb470eb464f1a24ef42d054f89f0e547b71701d0f21a33a70bcbec311b6f이며 runtime e5e290d7…와 같은 102 backend를 보존합니다.
- 111 정식 후보 기록: input111-full/QUALITY_CONSUMER.json, SHA 32e1824f41bf9d85cb473009d9d9e725ad4ee74e5a951aed16aa79099b38a4de.

이 문서의 상대 경로는 114 examples 원본 기준입니다. 115가 요약과 source-consumer manifest만 정확 복사해 읽는 경우 앱 전체를 다시 인수했다고 쓰지 않습니다. 114 examples/index.html과 앱 경로를 직접 참조하고, 실제 받은 문서·SHA·인수 범위를 기록합니다.

## 확인한 범위와 미확인

106 독립 full/로컬 배포 PASS와 112–114 독립 설계 PASS를 바탕으로 정식 원고·예제·학생/강사 자료를 작성했습니다. 111 정식 자료의 현재 독립 상태는 PASS_FULL_TEXT_LOCAL_PREPARATION_DISTRIBUTION_SCOPE_ACTUAL_RUNTIME_HOLD입니다. 112–114 정식 원고의 독립 최종 판정은 후속 검수 보고서에서 확인해야 합니다.

순수 로컬 계획 검사, 가상 JSON 별도 경로 복구, 소비 목록 바이트 비교와 새 시연을 확인했습니다. 작성자가 같은 머신의 새 폴더에서 재현한 결과이며 실제 다른 사람의 수행이 아닙니다. 근거 파일과 명령은 VALIDATION/작성 보고서에 남습니다.

111 후보는 local_candidate=true이지만 decision=hold_pending_evidence, actual_release_candidate=null입니다. actual_HTTP/user/performance_cost는 not_run입니다. 실제 이미지·CI·배포·HTTP/화면·운영 복구·사용자/학생·비용·성능은 수행하지 않았습니다. 강사 예시를 실제 성취로 채우지 않습니다.

## 운영·보존 책임

한 프로세스 JSON, owner+session, 생성 후 300초, 최근 완료 5회를 유지합니다. 공개 수업 토큰은 실제 인증이 아니고 한 worker는 동시 쓰기 잠금이 아닙니다. 정상 비답변·작업 미완료·접근·저장 오류를 구별하며 전체 결과·출처를 보존합니다.

복구는 쓰기 중지 확인 후 별도 새 대상에 수행할 계획입니다. 교재 작성에서는 운영 원본을 수정·삭제하지 않았고 임시 가상 자료만 사용했습니다. 이미지 롤백과 자료 복구를 나누며 만료를 늘리거나 영구 중복 방지를 주장하지 않습니다.

학생의 실제 인수·다른 사람 재현은 student/reproduction.md와 student/final/handoff.md의 빈 양식에서 시작합니다. 인수 담당자·환경·직접 관찰·실패·미확인을 기록해야 완료 범위를 말할 수 있습니다. 비밀과 실제 업무 원문은 이 공개 인계에 포함하지 않습니다.
