import sqlite3
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from roles import course_model

def make_desk(database, request_id, branch):
    @tool
    def register(request_id: str, branch: str) -> str:
        """승인된 가상 자료 재발급 요청을 지점별로 접수합니다."""
        with sqlite3.connect(database) as db:
            db.execute("INSERT INTO desk VALUES (?, ?) ON CONFLICT(id) DO NOTHING", (request_id, branch))
            saved, = db.execute("SELECT branch FROM desk WHERE id=?", (request_id,)).fetchone()
        return "registered" if saved == branch else "conflict"

    with sqlite3.connect(database) as db:
        db.execute("CREATE TABLE IF NOT EXISTS desk(id TEXT PRIMARY KEY, branch TEXT NOT NULL)")
    model = course_model()
    review = HumanInTheLoopMiddleware(interrupt_on={"register":{"allowed_decisions":["approve","edit","reject"]}})
    return create_agent(model, tools=[register], system_prompt=f"접수 요청이면 register로 신청하세요. 요청 번호 {request_id}, 지점 {branch}. 처리 후 결과를 안내하세요.", middleware=[review], checkpointer=InMemorySaver())
