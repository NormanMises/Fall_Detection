import os
import cv2
import streamlit as st
from deep_list import *
import torch
from icecream import ic
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)


if st.session_state["authentication_status"]:
    authenticator.logout("登出", location='sidebar')
elif st.session_state["authentication_status"] is None:
    st.switch_page("app.py")

st.title("跌倒检测系统")
inference_msg = st.empty()

st.sidebar.title("配置")

# 先扫描当前目录下的pt模型，然后设置一个下拉菜单来选择pt模型，自动从当前目录下加载
model_files = [f for f in os.listdir('./pt') if f.endswith('.pt')]
model_selection = f"./pt/{st.sidebar.selectbox('选择模型', model_files)}"
    
input_source = st.sidebar.radio("选择输入源",('网络摄像头', '本地视频'))

conf_thres = st.sidebar.slider("Conf 阈值", 0.0, 1.0, 0.25, 0.01)

iou_thres = st.sidebar.slider("NMS IoU 阈值", 0.0, 1.0, 0.45, 0.01)

conf_thres_drift = st.sidebar.slider("漂移检测的类别置信度阈值", 0.0, 1.0, 0.75, 0.01)

fps_drop_warn_thresh = st.sidebar.slider("FPS降低警告阈值", 0, 30, 8, 1)

save_output_video = st.sidebar.radio("保存输出视频？",('是', '否'))
if save_output_video == '是':
    nosave = False
    display_labels = False
else:
    nosave = True
    display_labels = True

save_poor_frame = st.sidebar.radio("保存性能差的帧？",('是', '否'))
if save_poor_frame == "是":
    save_poor_frame__ = True
else:
    save_poor_frame__ = False

# ------------------------- LOCAL VIDEO ------------------------------
if input_source == "本地视频":
    video = st.sidebar.file_uploader("选择输入视频", type=["mp4"], accept_multiple_files=False)
    
    if st.sidebar.button("开始检测"):

        stframe = st.empty()

        st.subheader("检测统计")
        kpi1, kpi2, kpi3 = st.columns(3)

        st.subheader("系统统计")
        js1, js2, js3 = st.columns(3)

        # 更新推理结果
        
        with kpi1:
            st.markdown("**帧率**")
            kpi1_text = st.markdown("0")
            fps_warn = st.empty()
        
        with kpi2:
            st.markdown("**当前帧中检测到的对象**")
            kpi2_text = st.markdown("0")
        
        with kpi3:
            st.markdown("**总共检测到的对象**")
            kpi3_text = st.markdown("0")
        
        # 更新系统统计
        
        with js1:
            st.markdown("**内存使用**")
            js1_text = st.markdown("0")

        with js2:
            st.markdown("**CPU使用率**")
            js2_text = st.markdown("0")

        with js3:
            st.markdown("**GPU内存使用**")
            js3_text = st.markdown("0")

        st.subheader("检测概览")
        inf_ov_1, inf_ov_2, inf_ov_3, inf_ov_4 = st.columns(4)

        with inf_ov_1:
            st.markdown("**性能差的类别（置信度 < {0}）**".format(conf_thres_drift))
            inf_ov_1_text = st.markdown("0")
        
        with inf_ov_2:
            st.markdown("**性能差的帧数**")
            inf_ov_2_text = st.markdown("0")
        
        with inf_ov_3:
            st.markdown("**最低帧率**")
            inf_ov_3_text = st.markdown("0")
        
        with inf_ov_4:
            st.markdown("**最高帧率**")
            inf_ov_4_text = st.markdown("0")

        detect(weights=model_selection, source=f"video/{video.name}", stframe=stframe, kpi1_text=kpi1_text, kpi2_text=kpi2_text, kpi3_text=kpi3_text, js1_text=js1_text, js2_text=js2_text, js3_text=js3_text, conf_thres=float(conf_thres), iou_thres=float(iou_thres), nosave=nosave, display_labels=display_labels, conf_thres_drift = float(conf_thres_drift), save_poor_frame__= save_poor_frame__, inf_ov_1_text=inf_ov_1_text, inf_ov_2_text=inf_ov_2_text, inf_ov_3_text=inf_ov_3_text, inf_ov_4_text=inf_ov_4_text, fps_warn=fps_warn, fps_drop_warn_thresh = float(fps_drop_warn_thresh))

        inference_msg.success("检测完成！")

# -------------------------- WEBCAM ----------------------------------
if input_source == "网络摄像头":
    
    if st.sidebar.button("开始检测"):

        stframe = st.empty()

        st.subheader("检测统计")
        kpi1, kpi2, kpi3 = st.columns(3)

        st.subheader("系统统计")
        js1, js2, js3 = st.columns(3)

        # 更新推理结果
        
        with kpi1:
            st.markdown("**帧率**")
            kpi1_text = st.markdown("0")
            fps_warn = st.empty()
        
        with kpi2:
            st.markdown("**当前帧中检测到的对象**")
            kpi2_text = st.markdown("0")
        
        with kpi3:
            st.markdown("**总共检测到的对象**")
            kpi3_text = st.markdown("0")
        
        # 更新系统统计
        
        with js1:
            st.markdown("**内存使用**")
            js1_text = st.markdown("0")

        with js2:
            st.markdown("**CPU使用率**")
            js2_text = st.markdown("0")

        with js3:
            st.markdown("**GPU内存使用**")
            js3_text = st.markdown("0")

        st.subheader("检测概览")
        inf_ov_1, inf_ov_2, inf_ov_3, inf_ov_4 = st.columns(4)

        with inf_ov_1:
            st.markdown("**性能差的类别（置信度 < {0}）**".format(conf_thres_drift))
            inf_ov_1_text = st.markdown("0")
        
        with inf_ov_2:
            st.markdown("**性能差的帧数**")
            inf_ov_2_text = st.markdown("0")
        
        with inf_ov_3:
            st.markdown("**最低帧率**")
            inf_ov_3_text = st.markdown("0")
        
        with inf_ov_4:
            st.markdown("**最高帧率**")
            inf_ov_4_text = st.markdown("0")

        detect(weights=model_selection, source='0', stframe=stframe, kpi1_text=kpi1_text, kpi2_text=kpi2_text, kpi3_text=kpi3_text, js1_text=js1_text, js2_text=js2_text, js3_text=js3_text, conf_thres=float(conf_thres), iou_thres=float(iou_thres), nosave=nosave, display_labels=display_labels, conf_thres_drift = float(conf_thres_drift), save_poor_frame__= save_poor_frame__, inf_ov_1_text=inf_ov_1_text, inf_ov_2_text=inf_ov_2_text, inf_ov_3_text=inf_ov_3_text, inf_ov_4_text=inf_ov_4_text, fps_warn=fps_warn, fps_drop_warn_thresh = float(fps_drop_warn_thresh))


# torch.cuda.empty_cache()

