import streamlit as st
# 배경 이미지 및 텍스트 스타일 설정
st.markdown(
    """
    <style>
        .background {
            background-image: url('https://ifh.cc/g/pflQNT.webp');
            background-size: cover;
            background-position: center;
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 20px;
        }
        .title {
            font-size: 55px;
            color: white;
            font-weight: bold;
            margin-bottom: 20px;
            text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.5);
        }
        .sub-title {
            font-size: 35px;
            color: white;
            font-weight: normal;
            margin-bottom: 20px;
            text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.5);
        }
        .names {
            font-size: 22px;
            color: white;
            font-weight: light;
            line-height: 1.6;
            background: rgba(0, 0, 0, 0.5);
            padding: 10px 20px;
            border-radius: 10px;
        }
    </style>
    <div class="background">
        <div class="title">젖소들의 건강한 착유를 위하여</div>
        <div class="sub-title">🌟 백5픈 아이들 🌟</div>
        <div class="names">
            <strong>팀장:</strong> 홍유택<br>
            <strong>팀원:</strong> 김학열, 남혜지, 문소희, 정지원
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
