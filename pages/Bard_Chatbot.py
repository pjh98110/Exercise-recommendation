import streamlit as st
from streamlit_chat import message
from bardapi import Bard
import os
import requests
from streamlit_extras.colored_header import colored_header
import pandas as pd


if "page" not in st.session_state:
    st.session_state.page = "Home"

if 'selected_gender' not in st.session_state:
    st.session_state.selected_gender = "남성" # 기본값

if 'selected_age' not in st.session_state:
    st.session_state.selected_age = "20대" # 기본값

if 'bard_input' not in st.session_state:
    st.session_state.bard_input = None   

DATA_PATH = "./"


# 데이터 불러오기
data = pd.read_csv(f"{DATA_PATH}운동목록.csv")

exercise1 = data['준비운동'].dropna()
exercise2 = data['본운동'].dropna()
exercise3 = data['마무리운동'].dropna()


API_KEY = st.sidebar.text_input(":blue[Enter Your Bard API-KEY :key:]", 
                placeholder="Bard API 키를 입력하세요!",
                type="password", key= "password", help="[바드 API KEY 가져오는 방법] 구글 로그아웃 --> 로그인 --> bard.google.com --> F12(개발자 모드) --> 애플리케이션 --> 쿠키(bard.google.com) --> __Secure-1PSID --> 값을 복사하기 입력하기")

os.environ["_BARD_API_KEY"] = API_KEY


session = requests.Session()
session.headers = {
            "Host": "bard.google.com",
            "X-Same-Domain": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Origin": "https://bard.google.com",
            "Referer": "https://bard.google.com/",
        }
session.cookies.set("__Secure-1PSID", os.getenv("_BARD_API_KEY")) 


selected_chatbot = st.selectbox(
    "원하는 챗봇을 선택하세요.",
    options=["바드 API를 활용한 운동 추천 챗봇", "바드 API를 활용한 운동 설명 챗봇"],
    placeholder="하나를 선택하세요.",
    help="선택한 값에 따라 다른 챗봇을 제공합니다."
)



if selected_chatbot == "바드 API를 활용한 운동 추천 챗봇":
    colored_header(
        label='운동 추천 Chatbot',
        description=None,
        color_name="orange-70",)
    # 'generated'와 'past' 키 초기화
    st.session_state.setdefault('generated', [{'type': 'normal', 'data': "추천할 운동 개수를 알려주세요.(최대 5개)"}])
    st.session_state.setdefault('past', ['나에게 맞춤형 운동을 추천해줄 수 있어?'])
    st.session_state.setdefault('chat_stage', 1)

    chat_placeholder = st.empty()

    def on_btn_click():
        st.session_state['past'] = ['나에게 맞춤형 운동을 추천해줄 수 있어?']
        st.session_state['generated'] = [{'type': 'normal', 'data': "추천할 운동 개수를 알려주세요.(최대 5개)"}]
        st.session_state['chat_stage'] = 1

    if 'user_input' not in st.session_state: # user_input 키 초기화
        st.session_state['user_input'] = ""

    def on_input_change():
        user_input = st.session_state.user_input
        st.session_state.past.append(user_input)
        # 사용자 입력 후, 입력 필드 초기화
        st.session_state['user_input'] = ""

        # target 키 초기화
        st.session_state.setdefault('target', '')   

        if st.session_state['chat_stage'] == 1:
            st.session_state['target'] = user_input # 추천하는 최대 운동 개수

            target_str = f"""의사로서 답변한다. {st.session_state.selected_age} {st.session_state.selected_gender} 환자의 체력 측정 값은 {st.session_state.bard_input}이며, 
                주어진 체력 측정 값만을 활용해서 운동을 추천하는 task이다. 환자의 체력 측정 값의 출력은 생략한다.
                운동은 다음 목록에 있는 운동만 추천해야한다. 운동 목록:{list(exercise2)}이며, 추천해야하는 운동은 {st.session_state['target']}개다. 
                각각의 운동마다 운동 순서, 방법, 효과를 자세하게 설명한다.
                """
            try:
                # Home에서 작성한 체력 측정 값과 Few shot learning 예시(운동 목록)를 Bard API에 함께 전달
                bard = Bard(token=os.environ["_BARD_API_KEY"], token_from_browser=True, session=session, timeout=30)
                response = bard.get_answer(target_str)
                st.session_state['generated'].append({"type": "normal", "data": response['content']})
                    
            except Exception as e:
                st.error(f"API 요청 중 오류가 발생했습니다.쿠키를 초기화하고 새로운 API 키를 입력해 주세요. ")
                response = {'content': 'API 요청에 문제가 발생했습니다. 쿠키를 초기화하고 새로운 API 키를 입력해 주세요..'}

    with chat_placeholder.container():
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=f"{i}_user")
            message(
                st.session_state['generated'][i]['data'],
                key=f"{i}",
                allow_html=True,
                is_table=True if st.session_state['generated'][i]['type'] == 'table' else False
            )
        
        st.button("대화 초기화", on_click=on_btn_click, key="clear_key")

    with st.container():
        st.text_input("챗봇과 대화하기:", value=st.session_state['user_input'], on_change=on_input_change, key="user_input", help="대화 초기화 버튼을 누르면 초기화면으로 돌아옵니다.")



elif selected_chatbot == "바드 API를 활용한 운동 설명 챗봇":

    # 'generated'와 'past' 키 초기화
    st.session_state.setdefault('generated2', [{'type': 'normal', 'data': "궁금한 운동을 입력해주세요."}])
    st.session_state.setdefault('past2', ['운동하는 방법에 대해 자세하게 알고 싶어, 어떻게 하면 될까?'])
    st.session_state.setdefault('chat_stage2', 1)

    colored_header(
        label='운동 설명 Chatbot',
        description=None,
        color_name="orange-70",)

    chat_placeholder = st.empty()

    def on_btn_click():
        st.session_state['past2'] = ['운동하는 방법에 대해 자세하게 알고 싶어, 어떻게 하면 될까?']
        st.session_state['generated2'] = [{'type': 'normal', 'data': "궁금한 운동을 입력해주세요."}]
        st.session_state['chat_stage2'] = 1

    if 'user_input2' not in st.session_state: # user_input2 키 초기화
        st.session_state['user_input2'] = ""

    def on_input_change():
        user_input2 = st.session_state.user_input2
        if user_input2:  # 사용자가 입력한 경우에만 처리
            st.session_state.past2.append(user_input2)
            st.session_state['user_input2'] = ""  # 입력 필드 초기화

        # target 키 초기화
        st.session_state.setdefault('target2', '')   

        if st.session_state['chat_stage2'] == 1:
            st.session_state['target2'] = user_input2 # 추천하는 최대 운동 개수

            target_str_2 = f"""헬스 트레이너로서 답변한다. 주어진 예시를 참고하여 운동을 자세하게 설명하는 task이다.
                예시: [가슴 스트레칭 운동 순서와 방법
                1. 준비 자세
                운동 시작 전, 편안한 서 있는 자세 또는 의자에 앉은 상태에서 시작합니다.
                어깨를 펴고, 등을 곧게 펴서 안정적인 기반을 만들어줍니다.
                2. 팔 벌리기
                양팔을 양 옆으로 벌려 수평이 되도록 합니다.
                손바닥은 앞을 향하고, 팔은 똑바로 뻗어 어깨 높이에 맞춥니다.
                3. 팔 뒤로 뻗기
                양팔을 천천히 뒤로 뻗으면서 가슴을 앞으로 밀어냅니다.
                이때 어깨와 팔의 위치를 조절하여 가슴 근육에 적절한 스트레칭이 되도록 합니다.
                4. 호흡 조절
                스트레칭 동안 깊고 천천히 숨을 쉬면서 긴장을 풀어줍니다.
                이 때, 깊은 호흡을 통해 근육 이완에 도움을 줍니다.
                5. 자세 유지
                이 자세를 20-30초 동안 유지하면서 가슴 근육이 이완되는 것을 느낍니다.
                스트레칭이 끝난 후 천천히 자세를 풀고, 필요에 따라 반복합니다.
                운동 효과 및 요약
                가슴 근육 이완: 가슴 스트레칭은 가슴 근육을 효과적으로 이완시켜, 근육의 긴장과 뻣뻣함을 완화합니다.
                자세 개선: 꾸준한 가슴 스트레칭은 어깨와 등의 자세를 개선하는 데 도움을 줍니다.
                호흡 개선: 가슴을 활짝 열어 폐의 확장을 돕고, 호흡이 더욱 편안해집니다.
                스트레스 완화: 긴장된 가슴 근육을 이완시켜 전반적인 스트레스와 긴장감을 완화할 수 있습니다.
                가슴 스트레칭은 특별한 장비가 필요 없고, 언제 어디서나 쉽게 할 수 있는 효과적인 운동 방법입니다.]

                예시: [바벨 당겨올리기 운동 순서와 방법
                1. 준비 자세
                발을 어깨 너비로 벌리고 서서, 바벨을 두 발 앞에 놓습니다.
                무릎을 살짝 구부려 가며, 허리는 곧게 펴고 바벨을 잡습니다.
                2. 바벨 잡기
                손은 어깨 너비보다 약간 넓게 바벨을 오버핸드 그립(손바닥이 앞을 향하도록)으로 잡습니다.
                손목이 바벨에 단단히 고정되도록 주의합니다.
                3. 당겨올리기
                바벨을 가슴 높이까지 당겨 올리면서 팔꿈치는 상체보다 높게 위치하도록 합니다.
                이때 어깨와 등 상부 근육을 사용해 바벨을 당기는 느낌을 가져야 합니다.
                4. 천천히 내리기
                바벨을 천천히 내려놓으면서 근육에 힘을 유지합니다.
                내려놓을 때도 허리가 굽지 않도록 주의합니다.
                5. 반복
                동작을 원하는 횟수만큼 반복합니다.
                운동 초보자는 가벼운 무게로 시작하여 점차 무게를 늘려가는 것이 좋습니다.
                운동 효과 및 요약
                등 근육 강화: 바벨 당겨올리기는 등 상부와 어깨 근육을 집중적으로 강화하는데 효과적입니다.
                포스쳐 개선: 정확한 자세로 운동을 수행하면 자세 개선에 도움이 됩니다.
                체력 및 지구력 향상: 규칙적인 바벨 당겨올리기는 전반적인 체력과 지구력을 향상시킬 수 있습니다.
                운동 요약: 바벨 당겨올리기는 등 근육을 강화하고 전반적인 체력을 향상시키는 효과적인 운동입니다. 정확한 자세와 적절한 무게 조절이 중요합니다. 초보자는 전문가의 지도 아래 안전하게 운동을 시작해야 합니다.]

                예시: [볼 튕기면서 스쿼트 운동 순서와 방법
                1. 준비 자세
                발을 어깨 너비로 벌리고 섭니다. 볼은 양손으로 가슴 앞에서 쥐고 있습니다.
                2. 볼 튕기기
                볼을 바닥에 가볍게 튕깁니다. 이 때, 팔은 약간 구부려주면서 볼을 튕겨주는 것이 좋습니다.
                3. 스쿼트 자세
                볼이 바닥에서 튕겨 올라오는 동안, 스쿼트 자세를 취합니다. 이때, 무릎이 발끝을 넘지 않도록 주의합니다.
                4. 상체 유지
                스쿼트 자세에서 상체는 가능한 곧게 유지합니다. 등과 허리가 굽지 않도록 주의하세요.
                5. 반복 운동
                볼을 다시 잡고 일어서면서 시작 자세로 돌아갑니다. 이 동작을 원하는 횟수만큼 반복합니다.
                운동 효과 및 요약
                하체 근력 강화: 스쿼트 자세는 특히 대퇴근과 둔근을 강화하는 데 도움이 됩니다.
                코디네이션 향상: 볼을 튕기는 동작과 스쿼트를 동시에 수행함으로써 균형 감각과 협응력이 향상됩니다.
                재미 요소 추가: 볼을 사용함으로써 운동에 재미를 더하고, 집중력을 높일 수 있습니다.
                운동 요약: '볼 튕기면서 스쿼트'는 하체 근력을 강화하고 균형 감각을 향상시키는 재미있고 효과적인 운동입니다. 볼을 사용함으로써 일상적인 스쿼트 운동에 새로운 변화를 줄 수 있습니다.]
                자세하게 설명해야하는 운동은 {st.session_state['target2']}이다. 이 운동에 대해 예시를 참고하여 운동 순서, 방법, 효과를 설명한다.
                """
            try:
                # Home에서 작성한 체력 측정 값과 Few shot learning 예시(운동 목록)를 Bard API에 함께 전달
                bard = Bard(token=os.environ["_BARD_API_KEY"], token_from_browser=True, session=session, timeout=30)
                response = bard.get_answer(target_str_2)
                st.session_state['generated2'].append({"type": "normal", "data": response['content']})
                    
            except Exception as e:
                st.error(f"API 요청 중 오류가 발생했습니다.쿠키를 초기화하고 새로운 API 키를 입력해 주세요. ")
                response = {'content': 'API 요청에 문제가 발생했습니다. 쿠키를 초기화하고 새로운 API 키를 입력해 주세요..'}

    # 챗봇 대화 표시
    with chat_placeholder.container():
        min_length = min(len(st.session_state['generated2']), len(st.session_state['past2']))
        for i in range(min_length):
            message(st.session_state['past2'][i], is_user=True, key=f"{i}_user")
            message(
                st.session_state['generated2'][i]['data'],
                key=f"{i}",
                allow_html=True,
                is_table=True if st.session_state['generated2'][i]['type'] == 'table' else False
            )
        
        st.button("대화 초기화", on_click=on_btn_click, key="clear_key2")


    with st.container():
        st.text_input("챗봇과 대화하기:", value=st.session_state['user_input2'], on_change=on_input_change, key="user_input2", help="대화 초기화 버튼을 누르면 초기화면으로 돌아옵니다.")

