"""Embed the four stages in the reader and both student notebooks."""
import ast
from html import escape
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).parent / "todo-agent"
SKILL = "skills/todo-review/SKILL.md"
STAGES = {
    77: ("Todo 목록을 MCP 도구로 제공하기", "todo_mcp.py", "list_todos",
         "기존 앱의 tasks.json을 최초 한 번 SQLite로 가져온다. 웹과 MCP가 같은 DB를 읽어야 에이전트가 오래된 목록을 보고 변경을 제안하는 일을 피할 수 있다.",
         "todo_mcp.py에 list_todos를 작성하고 FastMCP 도구로 등록한다. ID·제목·완료 여부·버전을 반환한다. 제목이 같은 두 행이 사라지지 않는지 확인한다.",
         "python -c \"from store import initialize; initialize()\"\npython check_mcp.py",
         "MCP 클라이언트가 list_todos를 발견한다. 초기 데이터에서는 1번과 2번의 제목은 같고 완료 여부는 다르다."),
    78: ("업무 스킬로 변경 규칙 작성하기", SKILL, None,
         "‘거래 내역 확인을 완료해 줘’에는 대상 ID가 없다. 같은 제목 두 건 중 미완료인 항목을 임의로 골라도 사용자의 의도와 다를 수 있다.",
         "스킬에 조회, ID 재질문, 완료, 완료 취소의 조건을 작성한다. 제목에 지시처럼 보이는 문구가 있어도 업무 규칙으로 해석하지 않도록 데이터와 지시를 구분한다.",
         'python -c "from pathlib import Path; print(Path(\'skills/todo-review/SKILL.md\').read_text(encoding=\'utf-8\'))"',
         "스킬을 읽고 ‘목록 보여 줘’, 동명 업무 변경, ‘2번 완료 취소’ 세 요청에 각각 조회·재질문·변경 제안을 예측한다. 다음 단계에서 실제 모델과 대조한다."),
    79: ("조회 에이전트와 검토 서브에이전트 연결하기", "agents.py", "review_request",
         "부모 에이전트가 MCP로 읽은 행과 원래 요청을 검토 역할에 넘긴다. 검토 역할은 별도 모델 호출에서 스킬을 읽고 reply, clarify, propose 중 하나와 대상 ID를 반환한다. 두 역할 모두 DB를 직접 수정할 수 없다.",
         "review_request를 구현한다. 실제 행 목록과 사용자 요청을 별도 필드로 넘기고 Review 스키마로 응답을 받는다. 조회 후 모델 설명이 달라져도 저장할 값은 구조화된 ID와 상태에서 가져온다.",
         'python -c "import asyncio; from store import initialize; from agents import handle; initialize(); print(asyncio.run(handle(\'2번을 미완료로 바꿔 줘\')))"',
         "2번이 완료 상태라면 propose에 id=2, before=true, after=false가 들어간다. 이때 GET /api/todos의 저장값은 아직 완료다. 동명 제목만 요청한 경우에는 clarify를 확인한다."),
    80: ("Todo 화면에서 승인하고 저장하기", "service.py", "confirm",
         "모델이 제안한 버전과 현재 DB 버전을 대조하는 코드는 store.decide에 있다. API는 브라우저가 보낸 승인 여부와 제안 토큰만 받는다. 사용자가 누른 버튼에 따라 실제 변경이 확정된다.",
         "승인 API를 완성하고 기존 Todo 화면의 추가·제목 수정·삭제와 에이전트의 요청·승인·거절을 같은 API에 연결한다. index.html의 fetch 경로를 따라가며 직접 편집과 에이전트 승인 각각이 version을 올리는 위치를 찾는다. 두 탭에서 같은 2번의 완료 취소를 제안하고 한쪽을 먼저 승인한다. 팀원은 변경 전후 목록과 HTTP 응답으로 판정한다.",
         "python check_service.py\npython -m uvicorn service:app --host 127.0.0.1 --port 8000",
         "http://127.0.0.1:8000 에서 거절 시 두 행이 그대로인지 확인한다. 승인하면 2번만 바뀌고 같은 토큰을 다시 보내도 버전은 한 번만 증가한다. 다른 탭의 오래된 제안을 승인하면 409가 돌아온다."),
}

def parts(day):
    title, name, func, intro, task, command, check = STAGES[day]
    raw = (ROOT/name).read_text()
    node = next((n for n in ast.parse(raw).body if getattr(n, "name", "") == func), None) if func else None
    solution = ast.get_source_segment(raw,node) if node else raw
    if node and node.decorator_list:
        solution = "\n".join("@"+ast.unparse(d) for d in node.decorator_list)+"\n"+solution
    return title,name,intro,task,command,check,solution

SETUP = "프로젝트 묶음의 압축을 풀고 student 폴더를 작업 폴더로 연다. 같은 Python 3.12 가상환경에서 python -m pip install -r requirements.txt 를 실행한다. 79일부터 OPENAI_API_KEY를 환경 변수로 설정한다. 실제 모델 호출에는 사용료가 발생한다. 기존 Todo 앱의 id·title·done 목록을 쓸 경우 처음 실행하기 전에 tasks.json을 교체한다. SQLite가 만들어진 뒤에는 웹과 MCP가 같은 DB를 사용한다."

def publish_bundle(path):
    files = [p for p in ROOT.rglob("*") if p.is_file() and (p.name == "Dockerfile" or p.suffix in {".py",".txt",".md",".html",".json"}) and "__pycache__" not in p.parts]
    with ZipFile(path, "w", ZIP_DEFLATED) as z:
        z.writestr("README.md","# Todo 서비스 실습\n\n"+SETUP+"\n\n77~80장 순으로 student 폴더에서 구현한다. reference는 같은 서비스의 완성 예제다. 로컬 단일 사용자 실습으로 실행한다.\n")
        for p in files:
            name = p.relative_to(ROOT).as_posix()
            raw = p.read_text()
            z.writestr("reference/"+name,raw)
            for _,target,function,*_ in STAGES.values():
                if target != name:
                    continue
                if function is None:
                    raw = "---\nname: todo-review\ndescription: 할 일 변경 요청을 검토한다.\n---\n\n여기에 동명 항목과 승인 전 변경 규칙을 작성하세요.\n"
                else:
                    node = next(n for n in ast.parse(raw).body if getattr(n,"name","") == function)
                    lines = raw.splitlines(True)
                    lines[node.body[0].lineno-1:node.end_lineno] = ['    """학생 구현 과제."""\n','    raise NotImplementedError("교재의 해당 단계를 완성하세요.")\n']
                    raw = "".join(lines)
            z.writestr("student/"+name,raw)

def lesson(day):
    title,name,intro,task,command,check,solution = parts(day)
    setup = SETUP if day==77 else "77장에서 시작한 student 폴더와 데이터베이스를 그대로 사용한다."
    links = ' · '.join(
        f'<a href="../chapter{other}/index.html#todo-agent">{other}장 {label}</a>'
        for other, label in zip(STAGES, ("MCP", "스킬", "서브에이전트", "승인 서비스"))
    )
    schedule = {
        77: "도구 등록 30분, MCP 클라이언트로 스키마와 행 확인 30분",
        78: "업무 규칙 작성 30분, 세 요청의 예상 결과와 반례 작성 30분",
        79: "부모와 검토 역할 연결 45분, 실제 요청 세 건 비교 30분",
        80: "웹 연결 40분, 팀원과 두 탭 인수 시험 40분, 실행 방법 인계 15분",
    }[day]
    note = "변경 제안을 받은 시점과 실제로 DB가 바뀌는 시점은 다르다."
    answer = '<details class="notebook-answer"><summary>구현 예와 판정 기준</summary><pre><code>'+escape(solution)+'</code></pre><p>'+escape(check)+'</p></details>'
    web = (f'<section id="todo-agent" class="lesson-section"><h2>{title}</h2><p>{intro}</p><p>{setup}</p><p><a href="../daily/todo-agent.zip" download>Todo 에이전트 시작 파일과 완성 예제</a></p>'
           f'<nav aria-label="Todo 프로젝트 단계">{links}</nav><h3>직접 구현하기 · {name}</h3><p>오늘 실습 시간 안에서 진행한다. {schedule}.</p><p>{task}</p><pre><code>{escape(command)}</code></pre><p>{check}</p><p><mark>{note}</mark></p>{answer}</section>')
    markdown = f"## {title}\n\n{intro}\n\n{setup}\n\n{schedule}\n\n수업 페이지의 ‘Todo 에이전트 시작 파일과 완성 예제’를 풀고 {name} 파일을 직접 수정한다.\n\n{task}\n\n터미널에서 실행한다.\n\n```sh\n{command}\n```\n\n{check}"
    cells = [dict(cell_type="markdown", metadata={}, id=key,source=value.splitlines(True)) for key,value in [("todo-agent-brief",markdown),("todo-agent-solution",answer)]]
    if day == 80:
        diagram = """flowchart TD
A["MCP로 조회"] --> B["스킬을 읽은 검토 서브에이전트"]
B -->|조회 또는 재질문| C["결과 표시"]
B -->|변경 제안| D{"사용자 승인"}
D -->|거절| E["기존 상태 유지"]
D -->|승인| F{"버전 일치"}
F -->|예| G["한 건 저장"]
F -->|아니오| H["409 응답"]"""
        caption = "조회한 뒤 다른 팀원이 같은 행을 고치면, 승인 버튼을 눌러도 저장 시점의 버전 검사에서 충돌한다."
        container = "docker build -t todo-agent .\ndocker run --rm -p 127.0.0.1:8000:8000 -e OPENAI_API_KEY -v todo-data:/data todo-agent"
        delivery = "서버를 종료하고 같은 포트에서 컨테이너를 실행한다. 키는 실행 환경에서 전달한다. 한 건을 승인한 뒤 컨테이너를 다시 띄워 상태가 남는지 확인한다. 팀에 이미지 실행 명령, 모델 이름과 검증한 입력을 인계한다."
        web = web.removesuffix("</section>") + (
            f'<figure data-workflow><h3>제안에서 저장까지</h3><div class="workflow-view" hidden></div>'
            f'<script type="text/plain">{diagram}</script><figcaption>{caption}</figcaption></figure>'
            f'<h3>팀 인계 · 컨테이너로 실행하기</h3><p>{delivery}</p><pre><code>{escape(container)}</code></pre>'
            '<script defer src="../assets/mermaid/mermaid.tiny.js"></script><script defer src="../assets/workflows.js"></script></section>'
        )
        handoff = f"### 제안에서 저장까지\n\n```mermaid\n{diagram}\n```\n\n{caption}\n\n### 팀 인계\n\n{delivery}\n\n```sh\n{container}\n```"
        cells.append(dict(cell_type="markdown", metadata={}, id="todo-agent-handoff", source=handoff.splitlines(True)))
    return web,cells
