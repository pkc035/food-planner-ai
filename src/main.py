import streamlit as st
from agents.graph import agent_executor

st.set_page_config(page_title="오늘 뭐 먹지? AI 미식 가이드", page_icon="🍽️")
st.title("🍽️ 오늘 뭐 먹지? AI 미식 가이드")

if "messages" not in st.session_state:
    st.session_state.messages = []

# 대화 기록 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("오늘 뭐 먹을까?"):
    # 1. 사용자 입력 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. 에이전트 답변 생성
    with st.chat_message("assistant"):
        with st.spinner("에이전트가 고민 중..."):
            response = agent_executor.invoke({"messages": [("user", prompt)]})
            
            with st.expander("🔍 에이전트의 사고 과정 보기"):
                # 모든 대화 상태(메시지 기록)를 출력하여 도구 호출 로그 확인
                st.write(response["messages"])
        
            answer = response["messages"][-1].content
            st.markdown(answer)
        
    st.session_state.messages.append({"role": "assistant", "content": answer})