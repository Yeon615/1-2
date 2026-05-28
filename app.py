import streamlit as st
st.title('최고')
st.write('굳굳')
import streamlit as st
from datetime import datetime
import pytz

st.title("🌍 세계 시간 확인 앱")

# 나라 선택
cities = {
    "서울": "Asia/Seoul",
    "도쿄": "Asia/Tokyo",
    "뉴욕": "America/New_York",
    "런던": "Europe/London",
    "파리": "Europe/Paris"
}

selected_city = st.selectbox("도시를 선택하세요", list(cities.keys()))

# 시간 가져오기
timezone = pytz.timezone(cities[selected_city])
current_time = datetime.now(timezone)

# 출력
st.subheader(f"{selected_city} 현재 시간")
st.write(current_time.strftime("%Y-%m-%d %H:%M:%S"))
