Python
import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="보건실 AI 챗봇", page_icon="🏥", layout="centered")
st.title("🏥 스마트 보건실 AI 챗봇")
st.write("아픈 곳이 있거나 보건실 이용에 대해 궁금한 점이 있다면 무엇이든 물어보세요!")

# 2. Streamlit Secrets에서 API 키 불러오기 및 클라이언트 초기화
# 예외 처리를 통해 API 키가 없을 때의 에러를 방지합니다.
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ 오류: Streamlit Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다. 배포 설정을 확인해주세요.")
    st.stop()

try:
    # 2026년 기준 최신 google-genai SDK 초기화 방식
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error(f"❌ 클라이언트 초기화 실패: {e}")
    st.stop()

# 3. 세션 상태(Session State)를 이용한 채팅 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "안녕하세요! 보건실 AI 도우미입니다. 어디가 아프신가요? 혹은 도움이 필요한 부분을 말씀해주세요! (예: 머리가 아파요, 보건실 위치가 어디에요?)"
        }
    ]

# 4. 저장된 대화 기록을 화면에 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. 사용자 입력 받기
if user_input := st.chat_input("증상이나 질문을 입력하세요..."):
    
    # 사용자가 입력한 메시지를 화면에 표시하고 기록에 추가
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 챗봇의 답변을 생성하는 동안 로딩 표시
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # 보건실 컨텍스트를 부여하기 위한 시스템 지침(System Instruction) 설정
        system_instruction = (
            "당신은 학교 보건실에 근무하는 친절하고 전문적인 보건 선생님입니다. "
            "학생들이 증상(두통, 복통, 상처 등)을 말하면 공감해주고, 안전한 일차 대처법을 안내하세요. "
            "단, 심각한 증상일 경우 반드시 즉시 보건실을 방문하거나 병원에 가야 함을 강조하세요. "
            "친절하고 따뜻한 말투(~요, ~습니다)를 사용하세요."
        )
        
        try:
            # gemini-2.5-flash-lite 모델을 호출하여 답변 생성
            response = client.models.generate_content(
                model='gemini-2.5-flash-lite',
                contents=user_input,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.7,
                )
            )
            
            # 답변 출력 및 기록 저장
            ai_response = response.text
            message_placeholder.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except APIError as ae:
            # 구글 API 관련 에러 처리
            error_msg = f"⚠️ Gemini API 오류가 발생했습니다: {ae.message}"
            message_placeholder.markdown(error_msg)
        except Exception as e:
            # 기타 예상치 못한 에러 처리
            error_msg = f"⚠️ 답변을 생성하는 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요. ({str(e)})"
            message_placeholder.markdown(error_msg)
