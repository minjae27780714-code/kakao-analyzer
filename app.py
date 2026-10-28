import streamlit as st
from openai import OpenAI

# 웹페이지 기본 설정
st.set_page_config(page_title="카카오톡 대화 분석기", page_icon="💬", layout="centered")

st.title("💬 카카오톡 / 채팅 대화 분석 AI")
st.write("채팅방 내보내기 파일(.txt)을 올리면, AI가 대화의 장단점과 고칠 점을 분석해 드립니다!")

# 1. API 키 입력 받기 (사이드바)
st.sidebar.header("🔑 설정")
api_key = st.sidebar.text_input("OpenAI API Key를 입력하세요", type="password")

# 2. 파일 업로드 창
uploaded_file = st.file_uploader("카카오톡 대화 텍스트(.txt) 파일을 업로드하세요", type=["txt"])

if uploaded_file is not None:
    # 텍스트 파일 읽기
    bytes_data = uploaded_file.getvalue()
    chat_text = bytes_data.decode("utf-8")
    
    # 대화 내용 미리보기 (일부만)
    with st.expander("📁 업로드된 대화 내용 미리보기"):
        st.text(chat_text[:1000] + "\n...(이하 생략)...")
        
    # 분석 시작 버튼
    if st.button("🚀 대화 분석 시작하기"):
        if not api_key:
            st.error("⚠️ 사이드바에 OpenAI API Key를 먼저 입력해 주세요!")
        else:
            with st.spinner("AI가 대화를 꼼꼼히 읽고 분석하는 중입니다... 잠시만 기다려주세요! ⏳"):
                try:
                    # OpenAI API 호출
                    client = OpenAI(api_key=api_key)
                    
                    prompt = f"""
                    다음은 카카오톡 대화 내용입니다. 이 대화를 바탕으로 다음 항목들을 객관적이고 친절하게 분석해 줘.
                    
                    1. 🌟 **대화의 장점** (소통 방식, 분위기, 긍정적인 면모)
                    2. ⚠️ **아쉬운 점 / 단점** (오해의 소지가 있는 부분, 소통의 답답한 점 등)
                    3. 💡 **앞으로 고치면 좋을 점 & 조언** (더 좋은 관계를 위한 행동 가이드)
                    
                    [대화 내용]
                    {chat_text[:15000]}
                    """
                    
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "당신은 전문적인 커뮤니케이션 분석가이자 친절한 상담사입니다."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    
                    result = response.choices[0].message.content
                    
                    # 결과 화면에 출력
                    st.success("🎉 분석이 완료되었습니다!")
                    st.markdown("---")
                    st.markdown(result)
                    
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")