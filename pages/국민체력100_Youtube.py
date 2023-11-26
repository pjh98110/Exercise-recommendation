import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
import numpy as np
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.colored_header import colored_header


if "page" not in st.session_state:
    st.session_state.page = "Home"

DATA_PATH = "./"
SEED = 42

colored_header(
    label='국민체력100 유튜브',
    description=None,
    color_name="orange-70",)

data = pd.read_csv(f"{DATA_PATH}국민체력100 운동처방 동영상주소.csv")

# 대분류 선택
category_1 = st.selectbox("국민체력100 유튜브 대분류를 선택해주세요.", data['대분류'].unique(), key="c1")

# 대분류에 따른 중분류 필터링
data_filtered_category_2 = data[data['대분류'] == category_1]
category_2 = st.selectbox("국민체력100 유튜브 중분류를 선택해주세요.", data_filtered_category_2['중분류'].unique(), key="c2")

# 중분류에 따른 소분류 필터링
data_filtered_category_3 = data_filtered_category_2[data_filtered_category_2['중분류'] == category_2]
category_3 = st.selectbox("국민체력100 유튜브 소분류를 선택해주세요.", data_filtered_category_3['소분류'].unique(), key="c3")


if category_3 == '근·골격계':
    body_part = st.selectbox("국민체력100 유튜브의 운동 부위를 선택해주세요.", ["어깨", "허리", "무릎"])

    # 제목에서 대괄호 안의 내용을 추출하여 해당 부위와 일치하는지 확인
    data_filtered_title = data_filtered_category_3[data_filtered_category_3['제목'].apply(lambda x: x.split(']')[0][1:] if ']' in x else '').str.contains(body_part)]
else:
    data_filtered_title = data_filtered_category_3[data_filtered_category_3['소분류'] == category_3]

# 제목 선택
if not data_filtered_title.empty:
    category_4 = st.selectbox("국민체력100 유튜브 제목을 선택해주세요.", data_filtered_title['제목'].unique(), key="c4")

    # 제목에 따른 동영상주소 필터링
    youtube_link = data_filtered_title[data_filtered_title['제목'] == category_4]['동영상주소'].iloc[0]

    # 유튜브 재생
    st.video(youtube_link, format="video/mp4", start_time=0)
else:
    st.warning("선택한 소분류/운동 부위에 해당하는 유튜브 제목이 없습니다.")

