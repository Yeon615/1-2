import streamlit as st
from datetime import datetime

st.title("세계 시간 앱")

now = datetime.utcnow()

st.write("현재 UTC 시간")
st.write(now.strftime("%Y-%m-%d %H:%M:%S"))
