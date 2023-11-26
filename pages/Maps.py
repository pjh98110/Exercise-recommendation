import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
import folium
from streamlit_folium import folium_static
from streamlit_extras.colored_header import colored_header
import chardet   

if "page" not in st.session_state:
    st.session_state.page = "Home"

# 데이터 경로
DATA_PATH = "C:/Users/Jonghyeon/Desktop/공간데이터/전처리 완료/"


# 세션 초기화
if 'seoul_local' not in st.session_state:
    st.session_state.seoul_local = None

if 'seoul_info' not in st.session_state:
    st.session_state.seoul_info = None

colored_header(
    label='서울시 체육시설 관련 지도',
    description=None,
    color_name="orange-70",)

seoul_info = st.selectbox("원하는 시설 위치와 정보를 선택하세요.", ["서울시 공공체육시설정보", "서울시 주요 공원현황", 
                            "서울시 생활체육포털 우리동네 프로그램", "서울시 체육시설 공공서비스예약 정보", "서울시 체육시설 인접 대중교통 정보","체육인증센터(서울)"], key="m1")

# 파일 인코딩 탐지
with open(f"{DATA_PATH}{seoul_info}.csv", 'rb') as file:
    result = chardet.detect(file.read())
    encoding = result['encoding']

data = pd.read_csv(f"{DATA_PATH}{seoul_info}.csv", encoding=encoding)                                        

seoul_local = st.selectbox("거주 지역을 선택해주세요.", data['지역'].unique(), key="m2")                                              

    
# 지역 필터링 함수
def filter_data_by_district(data, district):
    return data[data['지역'].str.contains(district)]

# 데이터셋 선택하는 함수
def create_popup(row, dataset_name):
    if dataset_name == "서울시 공공체육시설정보":
        return "{}".format(row['시설명'])
    elif dataset_name == "서울시 주요 공원현황":
        return "{}".format(row['공원명'])
    elif dataset_name == "서울시 생활체육포털 우리동네 프로그램":
        return "{}".format(row['장소'])
    elif dataset_name == "서울시 체육시설 공공서비스예약 정보":
        return "{}".format(row['시설명'])
    elif dataset_name == "체육인증센터(서울)":
        return "{}".format(row['센터명'])
    elif dataset_name == "서울시 체육시설 인접 대중교통 정보)":
        return "{}".format(row['대중교통시설구분명'])
        

# 지도 함수
def display_map(data):
    if not data.empty:
        # 첫 번째 데이터 포인트의 좌표를 사용하여 지도의 초기 위치 설정
        seoul_coords = [data.iloc[0]['Latitude'], data.iloc[0]['Longitude']]
        map = folium.Map(location=seoul_coords, zoom_start=12)
    
        # 각 행에 대해 마커를 추가
        for _, row in data.iterrows():
            # popup에 표시될 문자열을 생성
            popup_text = create_popup(row, seoul_info)
            folium.Marker(
                [row['Latitude'], row['Longitude']],
                popup=popup_text
            ).add_to(map)
        return map
    else:
        # 데이터가 비어 있을 경우 기본 좌표를 사용하여 지도를 반환
        return folium.Map(location=[37.5665, 126.9780], zoom_start=12)

def main():

    # 선택한 항목을 기준으로 데이터 필터링
    filtered_data = filter_data_by_district(data, seoul_local)

    # 스트리밋에 지도 표시
    if not filtered_data.empty:
        map = display_map(filtered_data)
        folium_static(map)
    
    # 지도 아래에 데이터 프레임 표시
    # st.markdown("선택한 지역의 체육시설 정보:")
    st.dataframe(filtered_data)

# 실행
if __name__ == "__main__":
    main()
