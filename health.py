import streamlit as st
import pandas as pd
import numpy as np
import os
import datetime


# MinMaxScaler 역변환 함수
def inverse_minmax(scaled_value, min_val, max_val):
    return scaled_value * (max_val - min_val) + min_val

# 농장별 최적 변수 설정
optimal_variables = {
    20261: {"착유 소요 시간": (3, 80), "공기흐름": (0.5, 7.8), "THI": (61.064, 94.084), "습도(%)": (43, 100), "전도도": (4.0, 8.28)},
    20264: {"착유 소요 시간": (3, 33.95), "공기흐름": (0.39, 9.4), "유단백": (2.6, 4.6), "전도도": (4.02, 8.30), "유지방": (1.2, 6.7), "기온": (15.6, 29.8)},
    20279: {"착유 소요 시간": (3, 19.94), "공기흐름": (0.5, 6.80), "THI": (61.064, 93.695), "전도도": (3.79, 10), "기온": (1, 5)},
    20332: {"착유 소요 시간": (3, 26.95), "공기흐름": (0.29, 7.5), "THI": (61.301, 93.930), "습도(%)": (45, 100), "전도도": (5.37, 8.53), "착유회차": (1, 5)},
    20338: {"착유 소요 시간": (3, 80), "공기흐름": (0.09, 7.8), "전도도": (0.2, 7.3), "기온": (15.5, 29.8), "온도": (31.82, 41.83)},
    21133: {"착유 소요 시간": (3, 26.95), "공기흐름": (0.29, 7.5), "THI": (61.301, 93.930), "전도도": (5.37, 8.53), "착유회차": (1, 5)},
    20278: {"착유 소요 시간": (3, 16.78), "공기흐름": (0.80, 6.90), "THI": (61.289, 93.776), "전도도": (3.79, 10), "유지방": (0.2, 6.9)}
}


#최적 변수에 어울리는 이모티콘 매핑
variable_emojis = {
    "착유 소요 시간": "⏱️",
    "공기흐름": "💨",
    "THI": "🌡️",
    "습도(%)": "💧",
    "전도도": "📈",
    "유단백": "🥛",
    "유지방": "🧈",
    "기온": "🌤️",
    "온도": "🔥",
    "착유회차": "🚦"
}


# CSV 파일 경로
file_path = '진짜찐최종데이터원본.csv'
save_path = 'uploaded_data.csv'

# CSV 파일 불러오기
if os.path.exists(file_path):
    df = pd.read_csv(file_path, encoding='utf-8')
elif os.path.exists(save_path):
    df = pd.read_csv(save_path)
else:
    df = None
    st.error("CSV 파일을 찾을 수 없습니다. 올바른 파일 경로를 확인해주세요.")

if df is not None:
    # 날짜 타입 변환 (문자열 → datetime)
    df["착유시작일시"] = pd.to_datetime(df["착유시작일시"], errors="coerce")
    # 날짜만 추출
    df["날짜"] = df["착유시작일시"].dt.date






    # 📌 수정된 부분 시작: 필터를 카드 스타일로 표시 (이모티콘 추가)
    # 필터를 한 행에 모두 배치
    filter_cols = st.columns([1, 1, 1, 1])

        # 1. 농장아이디 선택 (드롭다운)
    with filter_cols[0]:
            selected_farm = st.selectbox("🏠 농장아이디", sorted(df["농장아이디"].unique()))

        # 2. 개체번호 선택 방법 (드롭다운)
    with filter_cols[1]:
            search_option = st.selectbox("🔍 개체번호 선택 방법", ["개체선택", "검색"])

        # 3. 개체번호 선택 또는 검색
    with filter_cols[2]:
            filtered_animals = sorted(set(df[df["농장아이디"] == selected_farm]["개체번호"].tolist()))
            if search_option == "개체선택":
                selected_animal = st.selectbox("🐮 개체번호", filtered_animals)
            else:
                search_input = st.text_input("🔢 개체번호 입력").strip()
                if search_input and search_input in map(str, filtered_animals):
                    selected_animal = search_input
                else:
                    selected_animal = None

        # 4. 날짜 선택 (달력)
    with filter_cols[3]:
            selected_date = st.date_input("📅 날짜", value=datetime.date(2021, 9, 1))
    # 📌 수정된 부분 끝

    # 선택한 개체번호 출력 및 유효성 검사
    if not selected_animal:
        st.warning("올바른 개체번호를 입력하세요.")
    else:
        # 선택한 개체번호의 정보 필터링
        animal_info = df[(df["농장아이디"] == selected_farm) & (df["개체번호"].astype(str) == str(selected_animal))]
        filtered_info = animal_info[animal_info["날짜"] == selected_date]

        # 착유횟수 (선택한 날짜의 착유 개수 카운트)
        milking_count = filtered_info.shape[0]
        # 착유량 (선택한 날짜의 총 착유량)
        total_milking_volume = filtered_info["착유량(L)"].sum()

        # 레이아웃 설정
        col1, col2 = st.columns([1, 2])

        # 첫 번째 열에 이미지와 개체번호 표시
        with col1:
            st.image("cowow.png", width=500)
            st.markdown(
                f"<h2 style='text-align:center; font-size:20px;'>개체번호: {selected_animal}</h2>",
                unsafe_allow_html=True
            )

        # 두 번째 열에 개체 정보 표시
with col2:
    if not animal_info.empty:
        info_cols = st.columns(4)
        # 축종코드
        with info_cols[0]:
            st.markdown(
                f"""
                <div style="text-align:center; font-size:20px;">
                    <b><br>축종코드</b><br>
                    <span style="font-size:30px;">{animal_info.iloc[0]['축종코드']}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        # 제조사 아이디
        with info_cols[1]:
            st.markdown(
                f"""
                <div style="text-align:center; font-size:20px;">
                    <b><br>제조사 아이디</b><br>
                    <span style="font-size:30px;">{animal_info.iloc[0]['제조사 아이디']}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        # 착유횟수
        with info_cols[2]:
            st.markdown(
                f"""
                <div style="text-align:center; font-size:20px;">
                    <b><br>착유횟수</b><br>
                    <span style="font-size:30px;">{milking_count}회</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        # 착유량
        with info_cols[3]:
            st.markdown(
                f"""
                <div style="text-align:center; font-size:20px;">
                    <b><br>착유량</b><br>
                    <span style="font-size:30px;">{total_milking_volume}L</span>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.markdown(
            "<div style='text-align:center; font-size:22px;'>정보가 없습니다.</div>",
            unsafe_allow_html=True
        )




# 선택한 데이터 필터링
filtered_df = df[(df["날짜"] == selected_date) & (df["농장아이디"] == selected_farm)]

if not filtered_df.empty:
    numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns
    avg_values = filtered_df[numeric_cols].mean()

   

   
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

    if selected_farm in optimal_variables:
        optimal_vars = optimal_variables[selected_farm]
        st.subheader(f"농장 {selected_farm} 최적 변수")
        cols = st.columns(3)
        for idx, (var, (min_val, max_val)) in enumerate(optimal_vars.items()):
            if var in avg_values:
                original_value = avg_values[var]
                if var in ["착유 소요 시간", "공기흐름", "전도도", "온도"]:
                    original_value = inverse_minmax(original_value, min_val, max_val)
                text_color = "green" if min_val <= original_value <= max_val else "red"
                warning_msg = "주의" if min_val > original_value or original_value > max_val else ""
                emoji = variable_emojis.get(var, "")
                cols[idx % 3].markdown(f"<h2 style='color: {text_color}; font-size: 24px;'>{emoji} {var}</h2>", unsafe_allow_html=True)
                cols[idx % 3].write(f"<p style='font-size: 20px;'>최적범위: {min_val} ~ {max_val}</p>", unsafe_allow_html=True)
                cols[idx % 3].write(f"<p style='font-size: 20px; color: {text_color};'>농장 평균값: {original_value:.2f}</p>", unsafe_allow_html=True)
                if warning_msg:
                    cols[idx % 3].write(f"<p style='font-size: 20px; color: red; font-weight: bold;'>⚠️ {warning_msg}</p>", unsafe_allow_html=True)
else:
    st.warning("선택한 날짜와 농장아이디에 해당하는 데이터가 없습니다.")

    
