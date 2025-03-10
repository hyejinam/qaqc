

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
# 파일 경로
DATA_FILE = '진짜찐최종데이터원본.csv'

# 데이터 로드
data = None
if os.path.exists(DATA_FILE):  # 로컬 파일이 존재하면 불러오기
    data = pd.read_csv(DATA_FILE)
else:
    st.warning(":경고: '진짜찐최종데이터원본.csv' 파일을 찾을 수 없습니다. 데이터를 확인해주세요.")
if data is not None:
    # 🏠 농장 선택 및 날짜 선택 필터 (한 행에 표시)
    if "농장아이디" in data.columns and "착유시작일시" in data.columns:
        col1, col2 = st.columns(2)
        with col1:
            farms = data["농장아이디"].unique()
            selected_farm = st.selectbox("🌾 농장 선택", farms)
            farm_data = data[data["농장아이디"] == selected_farm]
        with col2:
            farm_data["착유시작일시"] = pd.to_datetime(farm_data["착유시작일시"])
            selected_date = st.date_input("📆 날짜 선택", farm_data["착유시작일시"].min())
            date_filtered_data = farm_data[farm_data["착유시작일시"].dt.date == selected_date]


   # 🥛 유지방, 유단백, 전도도 (총 착유량 대비 비율)
if not date_filtered_data.empty:
    col1, col2, col3 = st.columns(3)
    # :흰색_확인_표시: 스타일 적용 (폰트 크기 키우기)
    st.markdown(
        """
        <style>
        .metric-label {
            font-size: 20px !important;  /* 라벨 폰트 크기 */
            font-weight: bold;
            text-align: center;
        }
        .metric-value {
            font-size: 30px !important;  /* 값 폰트 크기 */
            font-weight: bold;
            text-align: center;
            color: #000000;  /* 값 색상 (선택 가능) */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    with col1:
        avg_fat = (date_filtered_data["유지방"].sum() / date_filtered_data["착유량(L)"].sum()) * 100 if date_filtered_data["착유량(L)"].sum() > 0 else 0
        st.markdown('<div class="metric-label">🧈 유지방 농장 평균</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{avg_fat:.2f} %</div>', unsafe_allow_html=True)
    with col2:
        avg_protein = (date_filtered_data["유단백"].sum() / date_filtered_data["착유량(L)"].sum()) * 100 if date_filtered_data["착유량(L)"].sum() > 0 else 0
        st.markdown('<div class="metric-label">🥛 유단백 농장 평균</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{avg_protein:.2f} %</div>', unsafe_allow_html=True)
    with col3:
        if "전도도" in date_filtered_data.columns:
            min_conductivity, max_conductivity = 2.1, 10.0  # 원래 전도도 최소~최대 범위
            avg_conductivity = date_filtered_data["전도도"].mean() * (max_conductivity - min_conductivity) + min_conductivity
            st.markdown('<div class="metric-label">🔌 전도도 농장 평균</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{avg_conductivity:.2f} mS/cm</div>', unsafe_allow_html=True)
        else:
                st.warning(":x: 선택한 날짜에 대한 데이터가 없습니다.")
    if "착유시작일시" in data.columns:
        data["착유시작일시"] = pd.to_datetime(data["착유시작일시"])


        
        # # 개체번호 선택 필터 추가
        # if "개체번호" in data.columns:
        #     selected_animal = st.selectbox("개체번호 선택", data["개체번호"].unique())
        #     animal_data = data[data["개체번호"] == selected_animal]
         # 🐄 개체번호 선택 방법 드롭다운으로 구현
    if not date_filtered_data.empty and "개체번호" in date_filtered_data.columns:
    col1, col2 = st.columns(2)
        with col1:
            selected_search_method = st.selectbox("🔍 개체번호 선택 방법", ("개체선택", "검색"))
        with col2:
            if selected_search_method == "개체선택":
                selected_animal = st.selectbox("개체번호 선택", date_filtered_data["개체번호"].unique())
            else:
                selected_animal = st.text_input("개체번호 입력")
            
             # 개체번호 데이터 필터링
        if selected_animal:
            animal_data = date_filtered_data[date_filtered_data["개체번호"] == selected_animal]
            if not animal_data.empty:
                st.write(f"선택된 개체번호: {selected_animal}")
            else:
                st.warning(":경고: 선택한 개체의 데이터가 없습니다.")
        else:
            st.warning(":경고: 올바른 개체번호를 입력해주세요.")



            
            
            if not animal_data.empty:
            
                #개체별 유지방, 유단백, 전도도 계산 (총 착유량 대비 비율)
                animal_fat = (animal_data["유지방"].sum() / animal_data["착유량(L)"].sum()) * 100 if animal_data["착유량(L)"].sum() > 0 else 0
                animal_protein = (animal_data["유단백"].sum() / animal_data["착유량(L)"].sum()) * 100 if animal_data["착유량(L)"].sum() > 0 else 0
                min_conductivity, max_conductivity = 1.0, 15.0  # 원래 전도도 최소~최대 범위 (예시값)
                animal_conductivity = animal_data["전도도"].mean() * (max_conductivity - min_conductivity) + min_conductivity
               
                
                # :흰색_확인_표시: 개체별 유지방, 유단백, 전도도 표시
                col1, col2, col3 = st.columns(3)
                # 스타일 적용 (폰트 크기 키우기)
                st.markdown(
                    """
                    <style>
                    .metric-label {
                        font-size: 20px !important;  /* 라벨 폰트 크기 조정 */
                        font-weight: bold;
                        text-align: center;
                    }
                    .metric-value {
                        font-size: 30px !important;  /* 값 폰트 크기 조정 */
                        font-weight: bold;
                        text-align: center;
                        color: #000000;  /* 값 색상 변경 (선택 사항) */
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )
                with col1:
                    st.markdown('<div class="metric-label">🧈 유지방 개체 평균</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-value">{animal_fat:.2f} %</div>', unsafe_allow_html=True)
                with col2:
                    st.markdown('<div class="metric-label">🥛 유단백 개체 평균</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-value">{animal_protein:.2f} %</div>', unsafe_allow_html=True)
                with col3:
                    st.markdown('<div class="metric-label">🔌 전도도 개체 평균</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-value">{animal_conductivity:.2f} mS/cm</div>', unsafe_allow_html=True)
                # :체온 원래 값 복구
                if "온도" in animal_data.columns:
                    min_temp, max_temp = 29.9, 42.6
                    animal_data["온도"] = animal_data["온도"] * (max_temp - min_temp) + min_temp
                # :흰색_확인_표시: 개체 상태 모니터링 (혈액흐름, 체온, THI) 3개의 게이지 차트 유지
                st.subheader("개체 상태 모니터링")
                if "혈액흐름" in animal_data.columns and "온도" in animal_data.columns and "THI" in animal_data.columns:
                    state_data = animal_data[["혈액흐름", "온도", "THI"]].mean()
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        fig_gauge1 = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=state_data["혈액흐름"] if not pd.isna(state_data["혈액흐름"]) else 0,
                            title={"text": "🩸 혈액흐름"},
                            gauge={"axis": {"range": [0, 100]}}
                        ))
                        st.plotly_chart(fig_gauge1)
                    with col2:
                        fig_gauge2 = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=state_data["온도"] if not pd.isna(state_data["온도"]) else 0,
                            title={"text": "🌡️ 체온"},
                            gauge={"axis": {"range": [29.9, 42.6]}}
                        ))
                        st.plotly_chart(fig_gauge2)
                    with col3:
                        fig_gauge3 = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=state_data["THI"] if not pd.isna(state_data["THI"]) else 0,
                            title={"text": "🔥 THI (스트레스 지수)"},
                            gauge={"axis": {"range": [0, 100]}}
                        ))
                        st.plotly_chart(fig_gauge3)
                else:
                    st.warning(":경고: 개체 상태 관련 데이터가 부족합니다.")
            else:
                st.warning(":경고: 선택한 개체의 데이터가 없습니다.")
        else:
            st.warning(":경고: 데이터셋에 '개체번호' 컬럼이 없습니다.")
    else:
        st.warning(":경고: 데이터셋에 '착유시작일시' 컬럼이 없습니다.")
else:
    st.warning(":열린_파일_폴더: 데이터 파일을 업로드해주세요.")
