import streamlit as st
from openai import APIError
from pathlib import Path
import sys
root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(root / 'pre-mid/documents/rag'))
from reader_chat import send, setup
setup(root)
from pathlib import Path
import json

st.title("소리채집 동아리 공지 도우미")
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.calls = 0

if st.button("새 대화"):
    st.session_state.messages = []  # 다음 질문에 보낼 이력도 비웁니다.
    st.session_state.calls = 0
if st.button("지난 수업의 대화 열기", disabled=bool(st.session_state.messages)):
    saved = Path(__file__).with_name("chat-sample.json")
    st.session_state.messages = json.loads(saved.read_text(encoding="utf-8"))

show_counts = st.checkbox("실행 정보 보기")
history = st.session_state.messages
for message in history:
    st.chat_message(message["role"]).write(message["content"])

question = st.chat_input("공지나 후속 질문을 입력하세요")
if question:
    st.session_state.calls += 1  # 보내기를 누른 입력만 집계합니다.
    st.chat_message("user").write(question)
    try:
        reply = send(history, question)
    except APIError:
        # 응답이 없어 저장하지 않았으므로 같은 질문을 다시 보낼 수 있습니다.
        st.error("응답을 받지 못했습니다. 연결과 키를 확인한 뒤 질문을 다시 보내 주세요.")
    else:
        st.chat_message("assistant").write(reply)

if show_counts:
    st.caption(f"전송한 질문 {st.session_state.calls}건 · 저장된 대화 {len(history) // 2}쌍")

# 원문 한 건과 질문 한 건을 차례로 보낸 뒤 그 입력을 내려받습니다.
if len(history) == 4:
    with st.expander("다음 수업용 시험 사례"):
        source_text = history[0]["content"]
        question_text = history[2]["content"]
        fragment = st.text_input("답에서 찾을 원문 구절")
        if fragment and fragment in source_text:
            example = {"context": source_text, "question": question_text, "expected_fragment": fragment}
            st.download_button("시험 사례 받기", json.dumps(example, ensure_ascii=False, indent=2),
                               file_name="chat-case-ui.json", mime="application/json")
        elif fragment:
            st.caption("첫 번째로 보낸 원문에 있는 구절을 입력하세요.")
