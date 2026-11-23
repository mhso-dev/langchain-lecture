import streamlit as st

data = {"대출": ("도서 대출 기간은 14일입니다.", "library-1", 1),
        "휴관": ("도서관은 월요일에 휴관합니다.", "library-2", 2)}

st.title("가상 도서관에 질문하기")
with st.form("question_form"):
    question = st.text_input("질문")
    submitted = st.form_submit_button("질문 보내기")
if submitted:
    hit = next((row for word, row in data.items() if word in question), None)
    st.session_state["last"] = hit
    st.session_state["asked"] = True
if st.session_state.get("asked"):
    hit = st.session_state.get("last")
    if hit is None:
        st.info("제공된 자료에서 확인할 수 없습니다.")
    else:
        st.write(hit[0])
        st.caption(f"근거 [{hit[1]}] 가상 도서관 이용 안내 / {hit[2]}쪽")
