import streamlit as st
import pandas as pd
import numpy as np
import os

# CSV 파일 불러오기 🗂️
def load_data(file_path):
    df = pd.read_csv(file_path)
    # 필요 없는 컬럼 제거 🧹
    if "축종코드" in df.columns:
        df.drop(columns=["축종코드"], inplace=True)
    # 날짜 변환 및 추가 📅
    df["착유시작일시"] = pd.to_datetime(df["착유시작일시"], errors="coerce")
    df["날짜"] = df["착유시작일시"].dt.date  # 날짜만 추출
    return df

# MinMaxScaler 역변환 함수 🔄
def inverse_minmax(scaled_value, min_val, max_val):
    return scaled_value * (max_val - min_val) + min_val

# 농장별 최적 변수 설정 📊
optimal_variables = {
    20261: {"착유 소요 시간": (3, 80), "공기흐름": (0.5, 7.8), "THI": (61.064, 94.084), "습도(%)": (43, 100), "전도도": (4.0, 8.28)},
    20264: {"착유 소요 시간": (3, 33.95), "공기흐름": (0.39, 9.4), "유단백": (2.6, 4.6), "전도도": (4.02, 8.30), "유지방": (1.2, 6.7), "기온": (15.6, 29.8)},
    20279: {"착유 소요 시간": (3, 19.94), "공기흐름": (0.5, 6.80), "THI": (61.064, 93.695), "전도도": (3.79, 10), "기온": (1, 5)},
    20332: {"착유 소요 시간": (3, 26.95), "공기흐름": (0.29, 7.5), "THI": (61.301, 93.930), "습도(%)": (45, 100), "전도도": (5.37, 8.53), "착유회차": (1, 5)},
    20338: {"착유 소요 시간": (3, 80), "공기흐름": (0.09, 7.8), "전도도": (0.2, 7.3), "기온": (15.5, 29.8), "온도": (31.82, 41.83)},
    21133: {"착유 소요 시간": (3, 26.95), "공기흐름": (0.29, 7.5), "THI": (61.301, 93.930), "전도도": (5.37, 8.53), "착유회차": (1, 5)},
    20278: {"착유 소요 시간": (3, 16.78), "공기흐름": (0.80, 6.90), "THI": (61.289, 93.776), "전도도": (3.79, 10), "유지방": (0.2, 6.9)}
}

# 데이터 불러오기 📥
file_path = '진짜찐최종데이터원본.csv'
save_path = 'uploaded_data.csv'
if os.path.exists(file_path):
    df = load_data(file_path)
elif os.path.exists(save_path):
    df = load_data(save_path)
else:
    df = pd.DataFrame()
    st.error("❌ CSV 파일을 찾을 수 없습니다. 올바른 파일 경로를 확인해주세요.")

st.title("🐄 Main 대시보드")
st.title("📊 생산 관리 대시보드")

# 필수 컬럼 확인 🔍
required_columns = ["날짜", "농장아이디"]
missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    st.error(f"❌ 다음 컬럼들이 누락되었습니다: {', '.join(missing_columns)}")
else:
    # 날짜 선택 필터 📅
    min_date = df["날짜"].min()
    max_date = df["날짜"].max()
    selected_date = st.date_input("📅 날짜 선택", value=min_date, min_value=min_date, max_value=max_date)

    # 농장아이디 선택 필터 🏠
    unique_farms = sorted(df["농장아이디"].unique())
    selected_farm = st.selectbox("🏠 농장아이디 선택", unique_farms)

    # 데이터 필터링 ⚙️
    filtered_df = df[(df["날짜"] == selected_date) & (df["농장아이디"] == selected_farm)]

    if not filtered_df.empty:
        numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            avg_values = filtered_df[numeric_cols].mean()
            if selected_farm in optimal_variables:
                optimal_vars = optimal_variables[selected_farm]
                st.subheader(f"🏆 농장 {selected_farm} 최적 변수")
                cols = st.columns(3)
                for idx, (var, (min_val, max_val)) in enumerate(optimal_vars.items()):
                    if var in avg_values.index:
                        original_value = avg_values[var]
                        if var in ["착유 소요 시간", "공기흐름", "전도도", "온도"]:
                            original_value = inverse_minmax(original_value, min_val, max_val)
                        text_color = "green" if min_val <= original_value <= max_val else "red"
                        warning_msg = "⚠️ 주의" if not (min_val <= original_value <= max_val) else ""
                        cols[idx % 3].write(f"<h3 style='font-size: 20px; color: {text_color};'>{var}</h3>", unsafe_allow_html=True)
                        cols[idx % 3].write(f"📏 최적범위: {min_val} ~ {max_val}")
                        cols[idx % 3].write(f"<p style='color: {text_color};'>{var} 평균값: {original_value:.2f}</p>", unsafe_allow_html=True)
                        if warning_msg:
                            cols[idx % 3].write(f"<p style='color: red;'>{warning_msg}</p>", unsafe_allow_html=True)
                    else:
                        st.warning(f"❌ '{var}' 컬럼을 찾을 수 없습니다.")
        else:
            st.warning("📉 숫자형 컬럼이 없습니다.")
    else:
        st.warning("❌ 선택한 날짜와 농장아이디에 해당하는 데이터가 없습니다.")
