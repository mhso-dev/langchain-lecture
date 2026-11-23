# P1 인계 API와 오류

원래 API는 input106/project-ui/backend/API_CONTRACT.md, 화면은 input106/project-ui/serve_ui.py와 web입니다. 102의 전체 python_response·job·출처는 보존합니다. 정상 네 상태 answered/need_clarification/no_evidence/invalid_input은 HTTP 200으로 완료·저장될 수 있습니다. Q06 공백 질문은 422로 바꾸지 않습니다. 소유 세션 없음은 404, 보유 request ID 중복/미완료는 409, 생성 후 300초 만료는 410, 저장 실패는 503이며 계산 결과와 저장 실패를 함께 보존합니다. 내부/손상 오류를 no_evidence로 합치지 않습니다.

owner+session이 파일 키이며 alice/bob의 같은 세션 문자열은 다른 파일입니다. 최근 완료 5회만 유지합니다. 스트림은 결과와 저장이 끝난 뒤 고정 문자열을 나누며 실제 모델 토큰 스트림이 아닙니다. 끊겨도 이미 저장한 결과를 되돌리지 않습니다. 공개 토큰은 수업용 신원 선택이고 인증이 아닙니다. Q07 관리자 예시는 신뢰된 로컬 호출뿐입니다.

이번 112 inspect_plan(dict)는 고정 준비 정책을 검사하고 hold_pending_evidence를 반환합니다. 정책 위반은 ValueError이며 실제 배포 호출이 없습니다. 113 backup/restore는 신뢰한 운영자의 쓰기 중지된 디렉터리만 받습니다. ValueError/UnicodeError/PermissionError/KeyError/TypeError는 형식·정책·경로의 거부, OSError 계열은 파일 작업 실패입니다. 발생한 예외를 성공이나 정상 비답변으로 변환하지 않습니다. 검사가 현재 결과의 출처 계약을 확인하더라도 답변 문장의 의미적 정답을 보장하지는 않습니다.

114 handoff.verify는 목록 바이트의 일치만 판정합니다. 누락은 FileNotFoundError, 변경/경로/해시는 ValueError입니다. 새 폴더 결과를 다른 사람의 수행으로 집계하지 않습니다. 114의 operations113/p1_input.py는 공통 P1 사본을 루트 input106/project-ui/backend에서 읽도록 경로 한 줄만 옮긴 파생 파일이며 원본 113과의 차이를 input-source-summary.json에 기록합니다. 정책/복구 함수/제공 관찰은 그대로입니다.
