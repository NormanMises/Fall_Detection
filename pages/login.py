import yaml
from yaml.loader import SafeLoader
import streamlit as st
import streamlit_authenticator as stauth

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

if st.sidebar.button("主页"):
    st.switch_page("app.py")
if st.sidebar.button("登录"):
    st.switch_page("pages/login.py")
if st.sidebar.button("注册"):
    st.switch_page("pages/register.py")

authenticator.login(fields={'Form name':'登录', 'Username':'用户名', 'Password':'密码', 'Login':'登录'})

if st.session_state["authentication_status"]:
    st.switch_page("pages/detect.py")
elif st.session_state["authentication_status"] == False:
    st.error('用户名或密码错误')