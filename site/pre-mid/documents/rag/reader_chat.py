"""13장의 send(history, question) 호출 규약으로 설명서 답변을 돌려준다."""
import streamlit as st

from portfolio import load_step
from rag_lab import answer_from_documents, open_index, rerank, retrieve


def setup(root, observe=False):
    st.session_state.rag_root = root
    st.session_state.rag_observe = observe
    mode = st.sidebar.radio("답변 자료", ["공지", "설명서 기본 검색", "설명서 재정렬"])
    if st.session_state.get("rag_chat_mode") != mode:
        st.session_state.messages = []
        st.session_state.calls = 0
    st.session_state.rag_chat_mode = mode


@st.cache_resource
def cached_index(chunks, directory):
    return open_index(chunks, directory=directory)


def answer_once(index, question, mode):
    candidates = retrieve(index, question, k=4)
    if mode == "설명서 재정렬":
        candidates = rerank(question, candidates)
    documents = candidates[:2]
    reply = answer_from_documents(question, documents)
    ids = ", ".join(r["id"] for r in documents)
    return f"{reply}\n\n답변에 보낸 문단: {ids}"


def send(history, question):
    mode = st.session_state.rag_chat_mode
    if mode == "공지":
        from notice_chat import send as send_notice
        return send_notice(history, question)

    root = st.session_state.rag_root
    rows = load_step(root, "chunks")
    directory = str(root / "my-course/rag/chroma")
    if st.session_state.rag_observe:
        from langsmith import traceable

        index = cached_index(rows, directory)
        run = traceable(name="내 챗봇의 설명서 답변",
                        process_inputs=lambda data: {k: v for k, v in data.items() if k != "index"})(answer_once)
        answer = run(index, question, mode)
    else:
        answer = answer_once(open_index(rows, directory=directory), question, mode)
    history.extend([{"role": "user", "content": question},
                    {"role": "assistant", "content": answer}])
    return answer
