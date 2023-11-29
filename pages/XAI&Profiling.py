import streamlit as st
import pandas as pd
import sweetviz as sv

st.set_page_config(layout="wide")

# 데이터 로드
DATA_PATH = "./"
data = pd.read_csv(f"{DATA_PATH}KS_NFA_FTNESS_MESURE_MVN_PRSCRPTN_GNRLZ_INFO_202304.csv")

# 제목
st.markdown("<span style='font-size: 24px;'><strong>XAI&Profiling</strong></span>", unsafe_allow_html=True)

# XAI 선택
selected_xai = st.selectbox(
    "원하는 XAI_분석을 선택하세요.",
    ["XAI_분류", "Sweetviz_Profiling"],
    placeholder="하나를 선택하세요.",
)

# XAI 분류
if selected_xai == "XAI_분류":
    if st.button("XAI 분류 실행"):
        # iframe 대신 modal로 변경
        st.components.v1.iframe("http://20.214.137.21:7777/", height=600)

# Sweetviz 프로파일링
elif selected_xai == "Sweetviz_Profiling":
    if st.button("Sweetviz_Profiling 실행"):
        # Sweetviz 보고서 생성
        report = sv.analyze(data)
        report.show_html(filepath='report.html', open_browser=False)
        # 보고서 표시
        HtmlFile = open('report.html', 'r', encoding='utf-8')
        source_code = HtmlFile.read() 
        st.components.v1.html(source_code, height=800)
