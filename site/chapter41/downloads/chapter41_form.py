records = [{'id': 'library-1',
  'text': '도서 대출 기간은 14일입니다.',
  'source': '가상 도서관 이용 안내',
  'page': 1},
 {'id': 'library-2',
  'text': '도서관은 월요일에 휴관합니다.',
  'source': '가상 도서관 이용 안내',
  'page': 2},
 {'id': 'library-3',
  'text': '무인 반납함은 24시간 이용할 수 있습니다.',
  'source': '가상 도서관 이용 안내',
  'page': 3}]
terms = ("대출", "휴관", "반납")

def retrieve(question, k=1):
    query = [int(term in question) for term in terms]
    if not any(query):
        return []
    def distance(row):
        vector = [int(term in row["text"]) for term in terms]
        return sum((a-b)**2 for a, b in zip(query, vector)), row["id"]
    return sorted(records, key=distance)[:k]

from typing import TypedDict
from uuid import uuid4
import streamlit as st
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from typing import Annotated
from operator import add

class Chat(TypedDict):
    question: str
    note: dict | None
    sources: list[dict]
    history: Annotated[list[str], add]

def process(state):
    question = state["question"]
    note = state["note"]
    if note and note["keyword"] in question:
        sources = [note]
    else:
        sources = retrieve(question, 1)
    return {"sources": sources, "history": [question]}

@st.cache_resource
def prepare_engine():
    builder = StateGraph(Chat)
    builder.add_node("process", process)
    builder.add_edge(START, "process")
    builder.add_edge("process", END)
    return builder.compile(checkpointer=InMemorySaver())

new_chat = st.button("새 대화")
if "thread" not in st.session_state or new_chat:
    st.session_state.thread = str(uuid4())
    st.session_state.current = None
engine = prepare_engine()
with st.form("ask"):
    question = st.text_input("질문")
    keyword = st.text_input("추가 문서 검색어 (선택)").strip()
    notice = st.text_area("추가 안내문 (선택)").strip()
    submit = st.form_submit_button("질문 보내기")
if submit and question.strip():
    config = {"configurable": {"thread_id": st.session_state.thread}}
    if bool(keyword) != bool(notice) or (keyword and keyword not in notice):
        st.session_state.current = None
        st.warning("추가 안내문과 그 안에 들어 있는 검색어를 함께 입력하세요.")
    else:
        note = {"id": "session-note", "keyword": keyword, "text": notice} if notice else None
        with st.spinner("안내문 검색 중"):
            st.session_state.current = engine.invoke({"question": question, "note": note}, config)
if st.session_state.current:
    state = st.session_state.current
    st.text("지난 질문: " + " / ".join(state["history"]))
    if state["sources"]:
        current = state["sources"][0]
        st.write(current["text"])
        location = f"{current['page']}쪽" if "page" in current else "직접 입력한 안내문"
        st.caption(f"근거 [{current['id']}] {location}")
    else:
        st.info("제공된 자료에서 확인할 수 없습니다.")
