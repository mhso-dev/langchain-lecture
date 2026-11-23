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
    sources: list[dict]
    history: Annotated[list[str], add]

def process(state):
    return {"sources": retrieve(state["question"], 1), "history": [state["question"]]}

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
    submit = st.form_submit_button("질문 보내기")
if submit and question.strip():
    config = {"configurable": {"thread_id": st.session_state.thread}}
    st.session_state.current = engine.invoke({"question": question}, config)
if st.session_state.current:
    state = st.session_state.current
    st.text("지난 질문: " + " / ".join(state["history"]))
    if state["sources"]:
        current = state["sources"][0]
        st.write(current["text"])
        st.caption(f"근거 [{current['id']}] {current['page']}쪽")
    else:
        st.info("제공된 자료에서 확인할 수 없습니다.")
