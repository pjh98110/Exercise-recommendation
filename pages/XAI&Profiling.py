import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
import numpy as np
import random
import os
import datetime as dt
from streamlit_extras.switch_page_button import switch_page

from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report



if "page" not in st.session_state:
    st.session_state.page = "Home"

DATA_PATH = "./"
SEED = 42

data = pd.read_csv(f"{DATA_PATH}KS_NFA_FTNESS_MESURE_MVN_PRSCRPTN_GNRLZ_INFO_202304.csv")


st.markdown(f"""
            <span style='font-size: 24px;'>
            <div style=" color: #000000;">
                <strong>Explainer_dashboard
            </strong>
            </div>
            """, unsafe_allow_html=True)


selected_xai = st.selectbox(
    label = "원하는 XAI_분석을 선택하세요.",
    options=["XAI_분류", "Pandas_Profiling"],
    placeholder="하나를 선택하세요.",
    help="선택한 XAI에 따라 다른 분석 결과를 제공합니다.",
    key="xai_key",)



if selected_xai == "XAI_분류":
    if st.button("XAI 분류 실행"):
        st.components.v1.html(
            """
            <iframe src="http://20.214.137.21:7777/" style="width:100%; height:600px;"></iframe>
            """,
            height=600,
        )


elif selected_xai == "Pandas_Profiling":
    if st.button("Pandas_Profiling 실행"):
        # Pandas Profiling 보고서 생성
        sample_data = data.sample(frac=0.5) # 샘플 50%
        profile = ProfileReport(sample_data, explorative=True)

        # 스트리밋에 보고서 표시
        st_profile_report(profile)
