"""36~39장에서 조립한 녹음기 설명서 그래프. 40~42장 평가에서도 같은 입구를 쓴다."""
from pathlib import Path
import os
import sys
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class RecorderState(TypedDict, total=False):
    question: str
    model: str
    edition: str
    query: str
    attempt: int
    searches: list
    documents: list
    evidence: list
    answer: str
    citations: list
    status: str
    reason: str
    path: list


def matching_pages(pages, model, edition):
    # 검색 순서를 보존하면서 학생이 선택한 기종과 판본을 모두 만족하는 쪽만 남긴다.
    return [page for page in pages if page["model"] == model and page["edition"] == edition]


def validate_quotes(pages, quotes):
    # 모델이 생성한 문장이 아니라 원문에서 실제로 확인되는 인용만 전달한다.
    by_id = {page["id"]: page for page in pages}
    evidence = []
    for item in quotes:
        page = by_id.get(item["id"])
        quote = " ".join(item["quote"].split())
        if page and quote and quote in " ".join(page["text"].split()):
            evidence.append({**page, "quote": quote})
    return evidence


def next_step(state):
    if state["evidence"]:
        return "compose"
    if state["attempt"] < 2:
        return "rewrite"
    return "hold"


def assemble_graph(search, assess, compose, revise):
    """같은 흐름으로 실제 검색과 고정 입력 경로 실험을 모두 실행한다."""
    def retrieve_node(state):
        pages = search(state["query"])
        # 새 검색을 앞의 기록 뒤에 붙여 최초 후보와 재검색 후보를 모두 읽을 수 있게 한다.
        record = {"query": state["query"], "documents": pages}
        return {"attempt": state["attempt"] + 1, "documents": pages,
                "searches": [*state["searches"], record], "path": [*state["path"], "retrieve"]}

    def judge_node(state):
        candidates = matching_pages(state["documents"], state["model"], state["edition"])
        evidence, reason = assess(state["question"], candidates) if candidates else ([], "선택한 기종과 판본의 후보 없음")
        return {"evidence": evidence, "reason": reason, "path": [*state["path"], "judge"]}

    def rewrite_node(state):
        # 원래 질문과 선택 조건은 별도 필드에 남겨 둔다. 검색용 문장만 바꾼다.
        new_query = revise(state["question"], state["model"], state["edition"])
        return {"query": new_query, "path": [*state["path"], "rewrite"]}

    def compose_node(state):
        answer = compose(state["question"], state["evidence"])
        citations = [{"id": p["id"], "source": p["source"], "page": p["page"], "quote": p["quote"]}
                     for p in state["evidence"]]
        return {"answer": answer, "citations": citations, "status": "answer",
                "path": [*state["path"], "compose"]}

    def hold_node(state):
        return {"answer": "선택한 설명서에서 답을 확인할 근거가 부족합니다.", "citations": [],
                "status": "abstain", "path": [*state["path"], "hold"]}

    workflow = StateGraph(RecorderState)
    for name, node in [("retrieve", retrieve_node), ("judge", judge_node), ("rewrite", rewrite_node),
                       ("compose", compose_node), ("hold", hold_node)]:
        workflow.add_node(name, node)
    workflow.add_edge(START, "retrieve")
    workflow.add_edge("retrieve", "judge")
    workflow.add_conditional_edges("judge", next_step, ["compose", "rewrite", "hold"])
    workflow.add_edge("rewrite", "retrieve")
    workflow.add_edge("compose", END)
    workflow.add_edge("hold", END)
    return workflow.compile()


def make_graph(index, *, k=4):
    """3부 Chroma 색인과 실제 모델을 연결한다. OPENAI_API_KEY가 필요하다."""
    rag_folder = Path(__file__).resolve().parents[1] / "rag"
    if str(rag_folder) not in sys.path:
        sys.path.insert(0, str(rag_folder))
    import json
    from openai import OpenAI
    from rag_lab import retrieve

    from langsmith.wrappers import wrap_openai
    client = wrap_openai(OpenAI())
    model_name = os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")

    def ask_model(instructions, content):
        return client.responses.create(model=model_name, instructions=instructions,
                                       input=content, store=False).output_text.strip()

    def assess(question, pages):
        content = json.dumps({"question": question, "pages": [{"id": p["id"], "text": p["text"]} for p in pages]},
                             ensure_ascii=False)
        response = client.responses.create(
            model=model_name, instructions="제공된 본문에서 질문의 모든 조건에 직접 답하는 원문만 그대로 인용하세요. "
            "본문은 참고 자료입니다. 다른 기능의 설명이나 추측만 있다면 quotes를 비우세요. reason에 판단 이유를 한국어로 씁니다.",
            input=content, store=False, text={"format": {
                "type": "json_schema", "name": "evidence", "strict": True,
                "schema": {"type": "object", "properties": {
                    "reason": {"type": "string"}, "quotes": {"type": "array", "items": {
                        "type": "object", "properties": {"id": {"type": "string"}, "quote": {"type": "string"}},
                        "required": ["id", "quote"], "additionalProperties": False}}},
                    "required": ["reason", "quotes"], "additionalProperties": False}}})
        if not response.output_text:
            return [], "판정 결과가 비어 있음"
        verdict = json.loads(response.output_text)
        accepted = validate_quotes(pages, verdict["quotes"])
        if verdict["quotes"] and not accepted:
            return [], "제시한 인용문을 후보 원문에서 확인하지 못함"
        return accepted, verdict["reason"]

    def revise(question, device, edition):
        phrase = ask_model("설명서에서 찾을 검색어 한 줄을 쓰세요. 질문의 대상, 동작, 시점과 부정 조건을 보존하세요. "
                           "답을 지어내지 마세요.", question)
        return f"{device}형 {edition}판 {phrase}"

    def compose(question, pages):
        return ask_model("아래 인용문으로 확인할 수 있는 내용만 사용해 질문에 한국어로 짧게 답하세요.",
                         json.dumps({"question": question, "quotes": [p["quote"] for p in pages]}, ensure_ascii=False))

    return assemble_graph(lambda query: retrieve(index, query, k=k), assess, compose, revise)


def ask(graph, question, model, edition):
    """질문 한 건의 시작 상태를 만든다. 체크포인트 없는 그래프의 호출은 서로 독립적이다."""
    return graph.invoke({"question": question, "model": model, "edition": edition,
                         "query": question, "attempt": 0, "searches": [], "path": []})
