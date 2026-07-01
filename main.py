import streamlit as st
from agent import app

st.title("오늘 뭐 먹지? 맛집 추천봇")

if prompt := st.chat_input("기분이나 날씨를 말해주세요!"):
    st.chat_message("user").write(prompt)
    result = app.invoke({"input": prompt})
    st.chat_message("assistant").write(result["recommendation"])