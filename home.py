import streamlit as st
# 배경 이미지 및 텍스트 스타일 설정
st.markdown("""
    <style>
        .background {
            background-image: url('https://ifh.cc/g/pflQNT.webp');  /* 새로운 이미지 URL 적용 */
            background-size: cover;
            background-position: center;
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
        }
        .title {
            font-size: 55px;
            color: black;
            font-weight: bold;
            margin-bottom: 40px;
        }
        .sub-title {
            font-size: 35px;
            color: black;
            font-weight: normal;
        }
        .names {
            font-size: 25px;
            color: black;
            font-weight: light;
            line-height: 1.6; /* 줄 간격 조정 */
        }
    </style>
    <div class="background">
        <div class="title">젖소들의 건강한 착유를 위하여</div>
        <div class="sub-title">백5픈 아이들</div>
        <div class="names">
            <strong>팀장:</strong> 홍유택<br>  <!-- 줄바꿈 -->
            <strong>팀원:</strong> 김학열, 남혜지, 문소희, 정지원
        </div>
    </div>
            """, unsafe_allow_html=True)