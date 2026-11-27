"""Starter observations and acceptance examples for the six-session Codex project."""
CASES = {
75: ("복구가 끝난 뒤 확인할 데이터", """import sqlite3
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE todo(id INTEGER PRIMARY KEY, title TEXT)")
db.execute("INSERT INTO todo VALUES (7, '견적 보내기')")
print(db.execute("SELECT 1").fetchone())""",
"SELECT 1은 빈 데이터베이스에서도 성공한다. Codex가 만든 복구 검사에 기존 항목의 ID와 제목을 전달해 첫 번째 실패를 재현한다.",
"""def recovered(connection):
    return connection.execute("SELECT title FROM todo WHERE id=?", (7,)).fetchone() == ("견적 보내기",)
print(recovered(db))
db.execute("DELETE FROM todo WHERE id=7")
print(recovered(db))""", "True 다음 False. 두 번째에도 DB 연결 자체는 살아 있다."),
76: ("동명이 있는 목록의 회귀 테스트", """rows = [{"id":1,"title":"검토","done":False},{"id":2,"title":"검토","done":False}]
def completed_ids(items):
    return [row["id"] for row in items if row["done"]]
print(completed_ids(rows))""",
"두 번째 항목만 완료 처리하는 테스트부터 작성한다. codex-kit의 todo.py에서 실패를 재현하고 고친 변경 줄을 확인한다.",
"""def complete_id(items, target):
    for row in items:
        if row["id"] == target:
            row["done"] = True
complete_id(rows, 2)
assert completed_ids(rows) == [2]
print(completed_ids(rows))""", "[2]. 제목으로 먼저 찾은 구현은 [1]이 되어 탈락한다."),
77: ("검사한 이미지와 배포 이미지 비교", """candidate = {"commit":"b92","image":"app:b92","tests":"passed"}
deploy = {"image":"app:latest"}
print(candidate["image"] == deploy["image"])""",
"Codex에 CI의 빌드 결과를 CD의 입력으로 전달하게 한다. 테스트가 실패하거나 검사한 이미지가 다르면 배포 요청을 만들지 않는 검사를 먼저 작성한다.",
"""def may_deploy(build, target):
    return build["tests"] == "passed" and build["image"] == target["image"]
print(may_deploy(candidate, deploy))
print(may_deploy(candidate, {"image":"app:b92"}))
print(may_deploy(dict(candidate, tests="failed"), {"image":"app:b92"}))""", "False, True, False. 배포 실습에서는 이전에 성공한 이미지 태그도 함께 기록한다."),
78: ("필터 후에도 같은 항목 선택하기", """items = [{"id":8,"title":"정리","done":True},{"id":21,"title":"정리","done":False}]
visible = [row for row in items if not row["done"]]
print(visible[0]["id"], items[0]["id"])""",
"화면 목록에서 첫 번째로 보이는 행을 눌러도 id=21을 보내야 한다. Codex에 HTML 버튼의 data-id와 클릭 이벤트를 연결하게 하고 필터 전후를 직접 눌러 본다.",
"""from html import escape
def item_button(row):
    return f'<button type="button" data-id="{row["id"]}">{escape(row["title"])}</button>'
print(item_button(visible[0]))""", "렌더링된 버튼에 data-id가 21로 남는다. JS에서 dataset.id는 문자열이므로 API 계약에 맞춰 변환한다."),
79: ("충돌 응답 뒤 화면 복구", """saved = {"id":21,"title":"정리","version":3}
draft = {"id":21,"title":"정리 완료","version":2}
print(draft["version"] == saved["version"])""",
"두 탭에서 같은 항목을 열고 먼저 저장한 뒤 오래된 탭에서 저장한다. Codex에 실패 화면을 구현하도록 하고 서버 값과 사용자 초안을 모두 확인한다.",
"""def resolve_edit(old, edited):
    if old["version"] != edited["version"]:
        return 409, old.copy(), edited["title"]
    return 200, dict(edited, version=old["version"]+1), ""
print(resolve_edit(saved, draft))""", "409일 때 서버 제목은 ‘정리’, 사용자가 다시 적용할 초안은 ‘정리 완료’다."),
80: ("완료 취소 기능 인수 시험", """tasks = [{"id":1,"done":True},{"id":2,"done":True}]
before = [row.copy() for row in tasks]
print(before)""",
"의뢰자는 완료 취소의 기대 동작을 세 문장으로 작성한다. 개발자는 Codex로 구현하고 같은 요청을 두 번 보내도 다른 항목과 결과가 바뀌지 않는지 확인한다.",
"""def undo(items, item_id):
    for row in items:
        if row["id"] == item_id:
            row["done"] = False
undo(tasks, 2)
once = [row.copy() for row in tasks]
undo(tasks, 2)
assert tasks == once and tasks[0] == before[0]
print(tasks)""", "1번만 완료 상태다. 실제 앱에서도 새로고침 뒤 같은 상태가 보이는지 상대 팀원이 확인한다."),
}
