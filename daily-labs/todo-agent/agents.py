import json
import os
import re
import sys
from pathlib import Path
from typing import Literal
from uuid import uuid4

from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pydantic import BaseModel
from store import db_path, propose

BASE = Path(__file__).resolve().parent

class Review(BaseModel):
    action: Literal["reply", "clarify", "propose"]
    item_id: int | None
    done: bool | None
    message: str

async def review_request(model, question, observed, summary):
    """조회 에이전트의 기록에서 근거만 넘겨받는 검토 서브에이전트."""
    rules = (BASE/"skills/todo-review/SKILL.md").read_text(encoding="utf-8")
    reviewer = create_agent(model, tools=[], system_prompt=rules, response_format=Review)
    packet = {"request": question, "todos": observed, "summary": summary}
    result = await reviewer.ainvoke({
        "messages": [("user", json.dumps(packet, ensure_ascii=False))]
    })
    return result["structured_response"]


async def handle(question):
    model = ChatOpenAI(model=os.getenv("OPENAI_MODEL") or "gpt-4o-mini", timeout=45, max_retries=1)
    params = StdioServerParameters(command=sys.executable, args=[str(BASE/"todo_mcp.py")],
                                   env={"TODO_DB": str(db_path())})
    observed = []
    async with stdio_client(params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()

            @tool
            async def read_tasks() -> str:
                """MCP를 통해 현재 할 일 목록을 읽는다."""
                reply = await session.call_tool("list_todos", {})
                if reply.isError:
                    raise RuntimeError("MCP 조회 실패")
                observed[:] = reply.structuredContent["result"]
                return json.dumps(observed, ensure_ascii=False)

            parent = create_agent(model, tools=[read_tasks], system_prompt="반드시 read_tasks로 조회하고 검토 담당자에게 관련 행의 ID·제목·현재 상태만 보고하세요. 사용자의 변경 가능 여부를 대신 판단하지 마세요.")
            log = await parent.ainvoke({"messages":[("user",question)]},config={"recursion_limit":10})
    if not observed:
        return {"action":"reply","message":"조회된 할 일이 없습니다."}

    review = await review_request(model, question, observed, log["messages"][-1].content)
    if review.action != "propose":
        return {"action":review.action,"message":review.message}
    row = next((r for r in observed if r["id"] == review.item_id), None)
    if row is None or review.done is None or bool(row["done"]) == review.done:
        return {"action":"clarify","message":"변경할 ID와 현재 상태를 다시 확인하세요."}
    ids = {int(n) for n in re.findall(r"(?:\bID\s*[:#]?\s*|#)(\d+)", question, re.I)}
    ids.update(int(n) for n in re.findall(r"(\d+)\s*번", question))
    matches = [r["id"] for r in observed if r["title"] == row["title"]]
    if (ids and ids != {row["id"]}) or (len(matches) > 1 and not ids):
        return {"action": "clarify", "message": f"변경할 번호를 지정해 주세요. 같은 제목의 번호는 {matches}입니다."}
    token = uuid4().hex
    propose(token,row["id"],review.done,row["version"])
    return {"action":"propose","message":review.message,"token":token,"id":row["id"],
            "title":row["title"],"before":bool(row["done"]),"after":review.done}
