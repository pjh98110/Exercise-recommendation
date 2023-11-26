import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
import numpy as np
import random
import os
import datetime as dt
from streamlit_extras.switch_page_button import switch_page

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from explainerdashboard import ClassifierExplainer, ExplainerDashboard, RegressionExplainer
from explainerdashboard.datasets import titanic_embarked, titanic_fare, feature_descriptions
import dash_bootstrap_components as dbc
import threading
import graphviz
import socket


if "page" not in st.session_state:
    st.session_state.page = "Home"

DATA_PATH = "./"
SEED = 42

# 데이터 불러오는 함수(캐싱)
@st.cache_data # 캐싱 데코레이터 (ttl=900)
def load_csv(path):
    return pd.read_csv(path)


st.markdown(f"""
            <span style='font-size: 24px;'>
            <div style=" color: #000000;">
                <strong>Explainer_dashboard
            </strong>
            </div>
            """, unsafe_allow_html=True)

# 포트가 사용 가능한지 확인하는 함수
def check_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    return result == 0

# 사용 가능한 포트를 찾는 함수
def find_available_port(start_port, end_port):
    for port in range(start_port, end_port):
        if not check_port(port):
            return port
    return None

# 대시보드를 실행하는 함수
def run_dashboard(port, dashboard):
    if not check_port(port):
        dashboard.run(port=port, host='0.0.0.0')  # 모든 인터페이스에서 접근 가능하게 설정
    else:
        st.error(f"Port {port} is already in use!")


selected_xai = st.selectbox(
    label = "원하는 XAI_분석을 선택하세요.",
    options=["XAI_분류", "XAI_회귀"],
    placeholder="하나를 선택하세요.",
    help="선택한 XAI에 따라 다른 분석 결과를 제공합니다.",
    key="xai_key",)



if selected_xai == "XAI_분류":
    if st.button("XAI 분류 실행"):
        port1 = find_available_port(8055, 8100)
        if port1 is not None:
            X_train, y_train, X_test, y_test = titanic_embarked()
            model = RandomForestClassifier(n_estimators=50, max_depth=10).fit(X_train, y_train)
            explainer = ClassifierExplainer(model, X_test, y_test, cats=['Sex', 'Deck'], descriptions=feature_descriptions, labels=['Queenstown', 'Southampton', 'Cherbourg'])
            dashboard = ExplainerDashboard(explainer, title="XAI Classification Dashboard", bootstrap=dbc.themes.MORPH)
            t = threading.Thread(target=lambda: run_dashboard(port1, dashboard))
            t.start()
            st.components.v1.html(
                f'<iframe src="http://localhost:{port1}" style="width:100%; height:600px;"></iframe>',
                height=600
            )
        else:
            st.error("No available ports found!")

elif selected_xai == "XAI_회귀":
    if st.button("XAI 회귀 실행"):
        port2 = find_available_port(8060, 8100)
        if port2 is not None:
            X_train, y_train, X_test, y_test = titanic_fare()
            model_2 = RandomForestRegressor(n_estimators=50, max_depth=10).fit(X_train, y_train)
            explainer_2 = RegressionExplainer(model_2, X_test, y_test, cats=['Sex', 'Deck', 'Embarked'], descriptions=feature_descriptions, units="$")
            dashboard2 = ExplainerDashboard(explainer_2, title="Simplified Regression Dashboard", bootstrap=dbc.themes.MORPH)
            t = threading.Thread(target=lambda: run_dashboard(port2, dashboard2))
            t.start()
            st.components.v1.html(
                f'<iframe src="http://localhost:{port2}" style="width:100%; height:600px;"></iframe>',
                height=600
            )
        else:
            st.error("No available ports found!")



# if selected_xai == "XAI_분류":
#     if st.button("XAI 분류 실행"):  
#         port1 = find_available_port(8055, 8100) # 사용 가능한 포트 찾기
#         if port1 is not None:
#             t = threading.Thread(target=lambda: run_dashboard(port1, dashboard))
#             t.start()

#             # 분류 대시보드
#             X_train, y_train, X_test, y_test = titanic_embarked()
#             model = RandomForestClassifier(n_estimators=50, max_depth=10).fit(X_train, y_train)

#             explainer = ClassifierExplainer(model, X_test, y_test, 
#                                             cats=['Sex', 'Deck'], 
#                                             descriptions=feature_descriptions,
#                                             labels=['Queenstown', 'Southampton', 'Cherbourg'])


#             # 대시보드 생성
#             dashboard = ExplainerDashboard(explainer, title="XAI Classification Dashboard", bootstrap=dbc.themes.MORPH)

#             # 스레드를 사용하여 대시보드 실행
#             t = threading.Thread(target=lambda: run_dashboard(port1))
#             t.start()

#             st.components.v1.html(
#                 f"""
#                 <iframe src="http://localhost:{port1}" style="width:100%; height:600px;"></iframe>
#                 """,
#                 height=600,
#             )
#         else:
#             st.error("No available ports found!")


# elif selected_xai == "XAI_회귀":
#     if st.button("XAI 회귀 실행"):

#         # 사용 가능한 포트 찾기
#         port2 = find_available_port(8060, 8100)
#         if port2 is None:
#             st.error("No available ports found!")

#         # 회귀 대시보드
#         X_train, y_train, X_test, y_test = titanic_fare()
#         model_2 = RandomForestRegressor(n_estimators=50, max_depth=10).fit(X_train, y_train)

#         explainer_2 = RegressionExplainer(model_2, X_test, y_test, 
#                                         cats=['Sex', 'Deck', 'Embarked'], 
#                                         descriptions=feature_descriptions,
#                                         units="$")

#         # 대시보드 생성
#         dashboard2 = ExplainerDashboard(explainer_2, title="Simplified Regression Dashboard",  bootstrap=dbc.themes.MORPH)

#         # 함수로 대시보드를 실행
#         def run_dashboard2(port):
#             dashboard2.run(port=port)

#         # 스레드를 사용하여 대시보드 실행
#         t = threading.Thread(target=lambda: run_dashboard2(port2))
#         t.start()

#         st.components.v1.html(
#             f"""
#             <iframe src="http://localhost:{port2}" style="width:100%; height:600px;"></iframe>
#             """,
#             height=600,
#         )

