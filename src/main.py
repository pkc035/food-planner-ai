import streamlit as st
from streamlit_geolocation import streamlit_geolocation
from agents.graph import agent_executor

st.set_page_config(page_title="오늘 뭐 먹지? AI 미식 가이드", page_icon="🍽️")
st.title("🍽️ 오늘 뭐 먹지? AI 미식 가이드")

# 1. 위치 정보 수집
st.sidebar.title("📍 내 위치")
location = streamlit_geolocation()
if location and location.get("latitude"):
    # 세션에 위치 저장 (에이전트 도구 내부에서 st.session_state.user_loc 호출 예정)
    st.session_state.user_loc = (location["latitude"], location["longitude"])
    st.sidebar.success(f"현재 위치 감지됨")
else:
    st.session_state.user_loc = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# 대화 기록 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("오늘 뭐 먹을까?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("에이전트가 고민 중..."):
            # 위치 정보를 명시적으로 시스템 메시지에 포함
            sys_info = f"사용자의 현재 위치: {st.session_state.user_loc}" if st.session_state.user_loc else "위치 정보 없음"
            
            input_data = {
                "messages": [
                    ("system", f"당신은 맛집/날씨 가이드입니다. {sys_info}"),
                    ("user", prompt)
                ]
            }
            response = agent_executor.invoke(input_data)
            
            # [시각화] 에이전트 사고 과정
            with st.expander("🔍 에이전트 판단 과정 확인"):
                for msg in response["messages"]:
                    if hasattr(msg, 'tool_calls') and msg.tool_calls:
                        st.write(f"🛠 도구 호출: {msg.tool_calls[0]['name']}")
                    st.write(f"💭 내용: {msg.content}")

            # 답변 추출 및 파싱
            ai_messages = [m for m in response["messages"] if m.type == "ai"]
            last_message = ai_messages[-1] if ai_messages else response["messages"][-1]
            answer = last_message.content
            
            if isinstance(answer, list):
                answer = "\n".join([str(item.get("text", item)) if isinstance(item, dict) else str(item) for item in answer])
            
            if not answer or answer.strip() == "[]":
                st.warning("맛집이나 날씨 정보를 찾지 못했어요.")
            else:
                st.markdown(answer)
        
    st.session_state.messages.append({"role": "assistant", "content": answer})