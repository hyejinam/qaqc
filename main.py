import streamlit as st
from streamlit_option_menu import option_menu

# 페이지 설정은 메인 스크립트에서만 호출
st.set_page_config(page_title="스마트팜 대시보드", layout="wide")

# 페이지 정보 및 경로 정의
pages = {
    "소개": "home.py",
    "Main 대시보드": "kpi.py",
    "생산관리 대시보드": "health.py",
    "품질관리 대시보드": "model.py"
    }

# 사이드바 메뉴 설정
with st.sidebar:
    selected_page = option_menu(
        menu_title="스마트팜",
        options=list(pages.keys()),
        menu_icon="list",
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#BFDDB3"},
            "icon": {"color": "white", "font-size": "20px"},
            "nav-link": {
                "font-size": "15px",
                "text-align": "left",
                "margin": "0px",
                "color": "white",  # 메뉴 글씨 색상을 흰색으로 설정
                "--hover-color": "#1E90FF",
            },
            "nav-link-selected": {
                "background-color": "#1D3557",
                "color": "white",  # 선택된 메뉴 글씨 색상도 흰색으로 설정
                "font-weight": "bold",
            },
            "menu-title": {
                "font-size": "20px",
                "color": "white",  # 메뉴 타이틀 '스마트팜'의 색상을 흰색으로 설정
                "font-weight": "bold",
            },
        }
    )


# 선택된 페이지에 따라 해당 스크립트를 실행
if selected_page and selected_page in pages:
    page_path = pages[selected_page]
    try:
        with open(page_path, "r", encoding="utf-8") as f:
            code = f.read()
            # set_page_config()이 각 페이지 내에 없어야 함
            exec(code, globals())
    except FileNotFoundError:
        st.error(f"{page_path} 파일을 찾을 수 없습니다.")

