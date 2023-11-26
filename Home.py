import streamlit as st
# st.set_page_config(layout="wide")
import pandas as pd
import numpy as np
import random
import os
import datetime as dt
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, add_page_title
from streamlit_extras.colored_header import colored_header


# add_page_title()

show_pages(
    [
        Page("Home.py", "맞춤형 운동 추천", "✅"),
        Page("pages/Bard_Chatbot.py", "운동 추천 챗봇", "🤖"),
        Page("pages/Maps.py", "주변 지도", "🗺️"),
        Page("pages/국민체력100_Youtube.py", "국민체력100_Youtube", "📺"),
        Page("pages/XAI&Profiling.py", "XAI&Profiling", "📖"),
    ]
)


if "page" not in st.session_state:
    st.session_state.page = "Home"

DATA_PATH = "./"
SEED = 42


def reset_seeds(seed):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)


# 세션 변수에 저장
if 'type_of_case' not in st.session_state:
    st.session_state.type_of_case = None

if 'selected_gender' not in st.session_state:
    st.session_state.selected_gender = None

if 'selected_age' not in st.session_state:
    st.session_state.selected_age = None

if 'questions' not in st.session_state:
    st.session_state.questions = {}

if 'bard_input' not in st.session_state:
    st.session_state.bard_input = {}    

if 'selected_survey' not in st.session_state:
    st.session_state.selected_survey = []




# 타이틀
colored_header(
    label= '데이터 분석을 통한 맞춤형 운동 처방',
    description=None,
    color_name="green-70",
)


# [사이드바]
st.sidebar.markdown(f"""
            <span style='font-size: 20px;'>
            <div style=" color: #000000;">
                <strong>성별 및 연령대 선택</strong>
            </div>
            """, unsafe_allow_html=True)


# 사이드바에서 성별, 연령대 선택
selected_gender = st.sidebar.selectbox("(1) 당신의 성별을 선택하세요:", ('남성', '여성'))
selected_age = st.sidebar.selectbox("(2) 당신의 연령대를 선택하세요:", ('10대', '20대', '30대', '40대', '50대', '60대', '70대 이상'))


selected_survey = st.selectbox(
    "원하는 추천 방식을 선택하세요.",
    options=["추천시스템 기반 맞춤형 운동 추천", "바드 API를 활용한 맞춤형 운동 추천",],
    placeholder="하나를 선택하세요.",
    help="선택한 추천 방식에 따라 다른 결과를 제공합니다."
)

st.session_state.selected_survey = selected_survey


if selected_survey == "추천시스템 기반 맞춤형 운동 추천":

    # 문진 결과를 저장할 딕셔너리
    st_results = {}

    # 사용자의 체력측정 입력값 수집
    questions = {
        "question1" : st.number_input("[측정항목1] 신장(cm)을 입력하세요.", placeholder="키 __cm", key="p1"),
        "question2" : st.number_input("[측정항목2] 체중(kg)을 입력하세요.", placeholder="몸무게 __kg", key="p2"),
        "question3" : st.number_input("[측정항목3] 체지방률(%)을 입력하세요.", placeholder="__%", key="p3"),
        "question4" : st.number_input("[측정항목4] 허리둘레(cm)를 입력하세요.", placeholder="허리둘레 __cm", key="p4"),
        "question5" : st.number_input("[측정항목5] 이완기최저혈압(mmHg)를 입력하세요.", placeholder="최저혈압 __mmHg", key="p5"),
        "question6" : st.number_input("[측정항목6] 이완기최고혈압(mmHg)를 입력하세요.", placeholder="최고혈압 __mmHg", key="p6"),
        "question7" : st.number_input("[측정항목7] 악력_좌(kg)을 입력하세요.", placeholder="__kg", key="p7"),
        "question8" : st.number_input("[측정항목8] 악력_우(kg)을 입력하세요.", placeholder="__kg", key="p8"),
        "question9" : st.number_input("[측정항목9] 윗몸말아올리기(회)를 입력하세요.", placeholder="__회", key="p9"),
        "question10" : st.number_input("[측정항목10] 반복점프(회)를 입력하세요.", placeholder="__회", key="p10"),
        "question11" : st.number_input("[측정항목11] 앉아윗몸앞으로굽히기(cm)를 입력하세요.", placeholder="__cm", key="p11"),
        "question12" : st.number_input("[측정항목12] 일리노이(초)를 입력하세요.", placeholder="__초", key="p12"),
        "question13" : st.number_input("[측정항목13] 체공시간(초)을 입력하세요.", placeholder="__초", key="p13"),
        "question14" : st.number_input("[측정항목14] 협응력시간(초)을 입력하세요.", placeholder="__초", key="p14"),
        "question15" : st.number_input("[측정항목15] 협응력실수횟수(회)를 입력하세요.", placeholder="__회", key="p15"),
        "question16" : st.number_input("[측정항목16] 협응력계산결과값(초)을 입력하세요.", placeholder="__초", key="p16"),
        "question17" : st.number_input("[측정항목17] BMI(kg/㎡)를 입력하세요.", placeholder="__kg/m2", key="p17"),
        "question18" : st.number_input("[측정항목18] 교차윗몸일으키기(회)를 입력하세요.", placeholder="__회", key="p18"),
        "question19" : st.number_input("[측정항목19] 왕복오래달리기(회)를 입력하세요.", placeholder="__회", key="p19"),
        "question20" : st.number_input("[측정항목20] 10M 4회 왕복달리기(초)를 입력하세요.", placeholder="__초", key="p20"),
        "question21" : st.number_input("[측정항목21] 제자리 멀리뛰기(cm)를 입력하세요.", placeholder="__cm", key="p21"),
        "question22" : st.number_input("[측정항목22] 의자에앉았다일어서기(회)를 입력하세요.", placeholder="__회", key="p22"),
        "question23" : st.number_input("[측정항목23] 6분걷기(m)를 입력하세요.", placeholder="__m", key="p23"),
        "question24" : st.number_input("[측정항목24] 2분제자리걷기(회)를 입력하세요.", placeholder="__회", key="p24"),
        "question25" : st.number_input("[측정항목25] 의자에앉아 3M표적 돌아오기(초)를 입력하세요.", placeholder="__초", key="p25"),
        "question26" : st.number_input("[측정항목26] 8자보행(초)를 입력하세요.", placeholder="__초", key="p26"),
        "question27" : st.number_input("[측정항목27] 상대악력(%)를 입력하세요.", placeholder="__초", key="p27"),
        "question28" : st.number_input("[측정항목28] 피부두겹합을 입력하세요.", placeholder="__", key="p28"),
        "question29" : st.number_input("[측정항목29] 왕복오래달리기출력(VO₂max)을 입력하세요.", placeholder="__VO₂max", key="p29"),
        "question30" : st.number_input("[측정항목30] 트레드밀_안정시(bpm)를 입력하세요.", placeholder="__bpm", key="p30"),
        "question31" : st.number_input("[측정항목31] 트레드밀_3분(bpm)을 입력하세요.", placeholder="__bpm", key="p31"),
        "question32" : st.number_input("[측정항목32] 트레드밀_6분(bpm)을 입력하세요.", placeholder="__bpm", key="p32"),
        "question33" : st.number_input("[측정항목33] 트레드밀_9분(bpm)을 입력하세요.", placeholder="__bpm", key="p33"),
        "question34" : st.number_input("[측정항목34] 트레드밀출력(VO₂max)을 입력하세요.", placeholder="__VO₂max", key="p34"),
        "question35" : st.number_input("[측정항목35] 스텝검사_회복시 심박수(bpm)를 입력하세요.", placeholder="__bpm", key="p35"),
        "question36" : st.number_input("[측정항목36] 스텝검사출력(VO₂max)를 입력하세요.", placeholder="__VO₂max", key="p36"),
        "question37" : st.number_input("[측정항목37] 허벅지_좌(cm)를 입력하세요.", placeholder="__cm", key="p37"),
        "question38" : st.number_input("[측정항목38] 허벅지_우(cm)를 입력하세요.", placeholder="__cm", key="p38"),
        "question39" : st.number_input("[측정항목39] 전신반응(초)를 입력하세요.", placeholder="__초", key="p39"),
        "question40" : st.number_input("[측정항목40] 성인체공시간(초)를 입력하세요.", placeholder="__초", key="p40"),
    }





    # 제출 버튼을 누를 경우
    if st.button("제출"):

        st.markdown(f"당신의 성별은 {selected_gender}이며, 연령대는 {selected_age}입니다.")
        st.markdown(f"추천 운동을 기반으로 원하는 정보를 선택하세요")



    st.markdown(
        """
        <style>
        .stButton > button {
            background-color: #A7FFEB;
            width: 100%; /
            display: inline-block;
            margin: 0; /
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


    def page1():
        want_to_Maps = st.button("주변 지도")
        if want_to_Maps:
            st.session_state.type_of_case = "Maps"
            switch_page("주변 지도")


    def page2():
        want_to_Xai_Profiling = st.button("XAI&Profiling")
        if want_to_Xai_Profiling:
            st.session_state.type_of_case = "Xai_Profiling"
            switch_page("XAI&Profiling")

    def page3():
        want_to_국민체력100_Youtube = st.button("국민체력100_Youtube")
        if want_to_국민체력100_Youtube:
            st.session_state.type_of_case = "국민체력100_Youtube"
            switch_page("국민체력100_Youtube")


    col1, col2, col3 = st.columns(3)
    with col1:
        page1()
    with col2:
        page2()
    with col3:
        page3()


if selected_survey == "바드 API를 활용한 맞춤형 운동 추천":

    # 문진 결과를 저장할 딕셔너리
    st_results = {}

    # 사용자의 체력측정 입력값 수집
    bard_input = {
        "키(cm)" : st.number_input("[측정항목1] 신장(cm)을 입력하세요.", placeholder="키 __cm", key="p1"),
        "몸무게(kg)" : st.number_input("[측정항목2] 체중(kg)을 입력하세요.", placeholder="몸무게 __kg", key="p2"),
        "bmi" : st.selectbox("[측정항목3] bmi를 선택하세요.", ['비만', '정상', '저체중'], placeholder="하나를 선택하세요.", key="p3"),
        "유연성" : st.selectbox("[측정항목4] 유연성을 선택하세요.", ['좋음', '보통', '나쁨'], placeholder="하나를 선택하세요.", key="p4"),
        "지구력" : st.selectbox("[측정항목5] 지구력을 선택하세요.", ['좋음', '보통', '나쁨'], placeholder="하나를 선택하세요.", key="p5"),
        "근력" : st.selectbox("[측정항목6] 근력을 선택하세요.", ['좋음', '보통', '나쁨'], placeholder="하나를 선택하세요.", key="p6"),
        "운동 경험" : st.selectbox("[측정항목7] 운동 경험을 선택하세요.", ['상급자', '중급자', '초급자'], placeholder="하나를 선택하세요.", key="p7"),
        "운동 환경" : st.selectbox("[측정항목8] 선호하는 운동 환경을 선택하세요.", ['실내 운동', '실외 운동'], placeholder="하나를 선택하세요.", key="p8"),
        "운동 시간" : st.selectbox("[측정항목9] 주로 운동하는 시간을 선택하세요.", ['새벽', '아침', '점심', '저녁', '밤'], placeholder="하나를 선택하세요.", key="p9"),
        "운동 목적" : st.selectbox("[측정항목10] 운동 목적을 선택하세요.", ['체중 감량', '근력 증진', '체력 향상', '스트레스 해소'], placeholder="하나를 선택하세요.", key="p10"),

        # "체지방률(%)" : st.number_input("[측정항목3] 체지방률(%)을 입력하세요.", placeholder="__%", key="p3"),
        # "허리둘레(cm)" : st.number_input("[측정항목4] 허리둘레(cm)를 입력하세요.", placeholder="허리둘레 __cm", key="p4"),
        # "이완기최저혈압(mmHg)" : st.number_input("[측정항목5] 이완기최저혈압(mmHg)를 입력하세요.", placeholder="최저혈압 __mmHg", key="p5"),
        # "수축기최고혈압(mmHg)" : st.number_input("[측정항목6] 이완기최고혈압(mmHg)를 입력하세요.", placeholder="최고혈압 __mmHg", key="p6"),
        # "악력_좌(kg)" : st.number_input("[측정항목7] 악력_좌(kg)을 입력하세요.", placeholder="__kg", key="p7"),
        # "악력_우(kg)" : st.number_input("[측정항목8] 악력_우(kg)을 입력하세요.", placeholder="__kg", key="p8"),
        # "윗몸말아올리기(회)" : st.number_input("[측정항목9] 윗몸말아올리기(회)를 입력하세요.", placeholder="__회", key="p9"),
        # "반복점프(회)" : st.number_input("[측정항목10] 반복점프(회)를 입력하세요.", placeholder="__회", key="p10"),
        # "앉아윗몸앞으로굽히기(cm)" : st.number_input("[측정항목11] 앉아윗몸앞으로굽히기(cm)를 입력하세요.", placeholder="__cm", key="p11"),
        # "일리노이(초)" : st.number_input("[측정항목12] 일리노이(초)를 입력하세요.", placeholder="__초", key="p12"),
        # "체공시간(초)" : st.number_input("[측정항목13] 체공시간(초)을 입력하세요.", placeholder="__초", key="p13"),
        # "협응력시간(초)" : st.number_input("[측정항목14] 협응력시간(초)을 입력하세요.", placeholder="__초", key="p14"),
        # "협응력실수횟수(회)" : st.number_input("[측정항목15] 협응력실수횟수(회)를 입력하세요.", placeholder="__회", key="p15"),
        # "협응력계산결과값(초)" : st.number_input("[측정항목16] 협응력계산결과값(초)을 입력하세요.", placeholder="__초", key="p16"),
        # "BMI(kg/㎡)" : st.number_input("[측정항목17] BMI(kg/㎡)를 입력하세요.", placeholder="__kg/m2", key="p17"),
        # "교차윗몸일으키기(회)" : st.number_input("[측정항목18] 교차윗몸일으키기(회)를 입력하세요.", placeholder="__회", key="p18"),
        # "왕복오래달리기(회)" : st.number_input("[측정항목19] 왕복오래달리기(회)를 입력하세요.", placeholder="__회", key="p19"),
        # "10M 4회 왕복달리기(초)" : st.number_input("[측정항목20] 10M 4회 왕복달리기(초)를 입력하세요.", placeholder="__초", key="p20"),
        # "제자리 멀리뛰기(cm)" : st.number_input("[측정항목21] 제자리 멀리뛰기(cm)를 입력하세요.", placeholder="__cm", key="p21"),
        # "의자에앉았다일어서기(회)" : st.number_input("[측정항목22] 의자에앉았다일어서기(회)를 입력하세요.", placeholder="__회", key="p22"),
        # "6분걷기(m)" : st.number_input("[측정항목23] 6분걷기(m)를 입력하세요.", placeholder="__m", key="p23"),
        # "2분제자리걷기(회)" : st.number_input("[측정항목24] 2분제자리걷기(회)를 입력하세요.", placeholder="__회", key="p24"),
        # "의자에앉아 3M표적 돌아오기(초)" : st.number_input("[측정항목25] 의자에앉아 3M표적 돌아오기(초)를 입력하세요.", placeholder="__초", key="p25"),
        # "8자보행(초)" : st.number_input("[측정항목26] 8자보행(초)를 입력하세요.", placeholder="__초", key="p26"),
        # "상대악력(%)" : st.number_input("[측정항목27] 상대악력(%)를 입력하세요.", placeholder="__초", key="p27"),
        # "피부두겹합" : st.number_input("[측정항목28] 피부두겹합을 입력하세요.", placeholder="__", key="p28"),
        # "왕복오래달리기출력(VO₂max)" : st.number_input("[측정항목29] 왕복오래달리기출력(VO₂max)을 입력하세요.", placeholder="__VO₂max", key="p29"),
        # "트레드밀_안정시(bpm)" : st.number_input("[측정항목30] 트레드밀_안정시(bpm)를 입력하세요.", placeholder="__bpm", key="p30"),
        # "트레드밀_3분(bpm)" : st.number_input("[측정항목31] 트레드밀_3분(bpm)을 입력하세요.", placeholder="__bpm", key="p31"),
        # "트레드밀_6분(bpm)" : st.number_input("[측정항목32] 트레드밀_6분(bpm)을 입력하세요.", placeholder="__bpm", key="p32"),
        # "트레드밀_9분(bpm)" : st.number_input("[측정항목33] 트레드밀_9분(bpm)을 입력하세요.", placeholder="__bpm", key="p33"),
        # "트레드밀출력(VO₂max)" : st.number_input("[측정항목34] 트레드밀출력(VO₂max)을 입력하세요.", placeholder="__VO₂max", key="p34"),
        # "스텝검사_회복시 심박수(bpm)" : st.number_input("[측정항목35] 스텝검사_회복시 심박수(bpm)를 입력하세요.", placeholder="__bpm", key="p35"),
        # "스텝검사출력(VO₂max)" : st.number_input("[측정항목36] 스텝검사출력(VO₂max)를 입력하세요.", placeholder="__VO₂max", key="p36"),
        # "허벅지_좌(cm)" : st.number_input("[측정항목37] 허벅지_좌(cm)를 입력하세요.", placeholder="__cm", key="p37"),
        # "허벅지_우(cm)" : st.number_input("[측정항목38] 허벅지_우(cm)를 입력하세요.", placeholder="__cm", key="p38"),
        # "전신반응(초)" : st.number_input("[측정항목39] 전신반응(초)를 입력하세요.", placeholder="__초", key="p39"),
        # "성인체공시간(초)" : st.number_input("[측정항목40] 성인체공시간(초)를 입력하세요.", placeholder="__초", key="p40"),
    }


    # 제출 버튼을 누를 경우
    if st.button("제출"):
    
        st.markdown(f"당신의 성별은 {selected_gender}이며, 연령대는 {selected_age}입니다.")
        st.markdown(f"운동 추천 챗봇 버튼을 클릭하세요. 챗봇 페이지로 이동합니다.")




    st.markdown(
        """
        <style>
        .stButton > button {
            background-color: #A7FFEB;
            width: 100%; /
            display: inline-block;
            margin: 0; /
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


    def page1():
        want_to_Bard_Chatbot = st.button("운동 추천 챗봇")
        if want_to_Bard_Chatbot:
            st.session_state.type_of_case = "Bard_Chatbot"
            switch_page("운동 추천 챗봇")
            
    def page2():
        want_to_Maps = st.button("주변 지도")
        if want_to_Maps:
            st.session_state.type_of_case = "Maps"
            switch_page("주변 지도")

    def page3():
        want_to_국민체력100_Youtube = st.button("국민체력100_Youtube")
        if want_to_국민체력100_Youtube:
            st.session_state.type_of_case = "국민체력100_Youtube"
            switch_page("국민체력100_Youtube")


    col1, col2, col3 = st.columns(3)
    with col1:
        page1()
    with col2:
        page2()
    with col3:
        page3()
