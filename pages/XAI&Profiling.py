import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
import numpy as np
import os
import datetime as dt
from streamlit_extras.switch_page_button import switch_page


if "page" not in st.session_state:
    st.session_state.page = "Home"


st.markdown(f"""
            <span style='font-size: 20px;'>
            <div style=" color: #000000;">
                <strong>XAI
            </strong>
            </div>
            """, unsafe_allow_html=True)


st.components.v1.html(
    """
    <iframe src="http://20.214.137.21:7777/" style="width:100%; height:600px;"></iframe>
    """,
    height=600,
)

