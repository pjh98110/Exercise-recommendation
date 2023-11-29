import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
import numpy as np
import os
import datetime as dt
from streamlit_extras.switch_page_button import switch_page
import streamlit.components.v1 as components 
import sweetviz as sv


if "page" not in st.session_state:
    st.session_state.page = "Home"

DATA_PATH = "./"
SEED = 42

data = pd.read_csv(f"{DATA_PATH}KS_NFA_FTNESS_MESURE_MVN_PRSCRPTN_GNRLZ_INFO_202304.csv")


st.markdown(f"""
            <span style='font-size: 24px;'>
            <div style=" color: #000000;">
                <strong>XAI&Profiling
            </strong>
            </div>
            """, unsafe_allow_html=True)


selected_xai = st.selectbox(
    label="원하는 XAI_분석을 선택하세요.",
    options=["XAI_분류", "Sweetviz_Profiling"],
    placeholder="하나를 선택하세요.",
    help="선택한 XAI에 따라 다른 분석 결과를 제공합니다.",
    key="xai_key")




# XAI 분류 실행
if selected_xai == "XAI_분류":
    if st.button("XAI 분류 실행"):
        # 임베디드 iframe
        components.iframe("http://20.214.137.21:7777/", height=600)

# Sweetviz 프로파일링 실행
elif selected_xai == "Sweetviz_Profiling":
    if st.button("Sweetviz_Profiling 실행"):
        # Sweetviz 보고서 생성
        report = sv.analyze(data)
        # HTML 파일로 보고서 저장
        report.show_html(filepath='report.html', open_browser=False)
        # 보고서 표시
        HtmlFile = open('report.html', 'r', encoding='utf-8')
        source_code = HtmlFile.read() 
        components.html(source_code, height=800)
