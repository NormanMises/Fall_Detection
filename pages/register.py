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

try:
    email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(pre_authorization=False, fields={'Form name':'注册', 'Name':'昵称', 'Email':'邮箱', 'Username':'用户名', 'Password':'密码', 'Repeat password':'重复密码', 'Register':'注册'})
    if email_of_registered_user:
        st.success('注册成功，现在可以登录了！')
        with open('config.yaml', 'w') as file:
            yaml.dump(config, file, default_flow_style=False)
        st.switch_page("pages/login.py")
except Exception as e:
    st.error(e)




