import json
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
import os
from langchain_core.tools import tool
from langsmith import tracing_context
from policy import lookup_policy, check_evidence, choose_skill, load_skill

def course_model():
    return ChatOpenAI(model=os.getenv("OPENAI_MODEL") or "gpt-4o-mini", timeout=45, max_retries=1)

def run_roles(request, override_citations=None):
    name = choose_skill(request["topic"])
    if not name:
        return {"status":"unsupported","trace":[]}
    instructions = load_skill(name)
    def execute(role, func, args):
        action = tool(func)
        agent = create_agent(course_model(), tools=[action], system_prompt=instructions + "\n등록된 도구로 주어진 입력을 검사하고 그 결과로 답하세요.")
        with tracing_context(enabled=False):
            log = agent.invoke({"messages":[("user",json.dumps(args,ensure_ascii=False))]})["messages"]
        output = next((m for m in reversed(log) if m.type=="tool"), None)
        if output is None:
            return {"status":"hold","reason":"no_tool_result"}, [role+":"+m.type for m in log]
        return json.loads(output.content), [role+":"+m.type for m in log]

    def research(branch: str, audience: str, as_of: str, topic: str) -> dict:
        """기준일에 유효한 문서 후보를 조회합니다."""
        return lookup_policy(branch,audience,as_of,topic)
    def review(citations: list[str]) -> dict:
        """인계받은 근거가 원 요청의 범위에 속하는지 검사합니다."""
        return check_evidence(request,{"citations":citations})

    found, trace = execute("research",research,request)
    if found["status"]!="ok":
        return {"status":found["status"],"trace":trace}
    citations = [found["items"][0]["chunk_id"]] if override_citations is None else override_citations
    result, checks = execute("review",review,{"citations":citations})
    return {**result,"skill":name,"trace":trace+checks}
