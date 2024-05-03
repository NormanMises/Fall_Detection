# streamlit run app.py

import streamlit as st
st.title("人体跌倒检测系统")

video_file = open('video/detect.mp4', 'rb')
video_bytes = video_file.read()

st.video(video_bytes, loop=True)

if st.sidebar.button("主页"):
    st.switch_page("app.py")
if st.sidebar.button("登录"):
    st.switch_page("pages/login.py")
if st.sidebar.button("注册"):
    st.switch_page("pages/register.py")