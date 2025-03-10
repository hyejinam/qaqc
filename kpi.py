import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import plotly.express as px
import os
import geopandas as gpd
import folium
from streamlit_folium import folium_static
from folium import CustomIcon
import streamlit as st
import time

from PIL import Image


# 한글 폰트 설정 (운영체제에 따라 다르게 설정)
import platform
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin':  # macOS
    plt.rc('font', family='AppleGothic')
else:
    plt.rc('font', family='DejaVu Sans')  # Linux 등

plt.rc('axes', unicode_minus=False)  # 마이너스 기호 깨짐 방지

# 데이터 불러오기
file_path = '진짜찐최종데이터원본.csv'
save_path = 'uploaded_data.csv'
if os.path.exists(file_path):
    df = pd.read_csv(file_path, encoding='utf-8')
elif os.path.exists(save_path):
    df = pd.read_csv(save_path)
else:
    df = None
    st.error("CSV 파일을 찾을 수 없습니다. 올바른 파일 경로를 확인해주세요.")
st.title("🐄 Main 대시보드")


if df is not None:
    # 날짜 컬럼을 datetime 형식으로 변환
    df['착유시작일시'] = pd.to_datetime(df['착유시작일시'])
    df['착유종료일시'] = pd.to_datetime(df['착유종료일시'])

    # 평균 착유 소요 시간(분) 계산
    df['착유 소요 시간(분)'] = (df['착유종료일시'] - df['착유시작일시']).dt.total_seconds() / 60



    # 농장 선택
    farm_ids = df['농장아이디'].unique()
    with st.expander("🏠 농장 필터"):
        selected_farm = st.selectbox('농장을 선택하세요:', ['전체'] + list(farm_ids), key="farm_select")



# 🔽 로딩 중일 때만 GIF 이미지를 작게 표시하도록 설정
    loading_container = st.empty()  # 빈 컨테이너 생성

    with st.spinner('데이터를 불러오는 중입니다...'):
    # HTML + CSS를 이용한 커스텀 로딩 스피너 표시
        loading_container.markdown(
        """
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; height:400px;">
            <!-- 동그란 배경과 이미지 -->
            <div style="position: relative; width: 200px; height: 200px; border-radius: 50%; background-color: #BFDDB3; overflow: hidden;">
                <img src="data:image/png;base64,{image_base64}" style="width: 100%; height: 100%; object-fit: cover;">
                <!-- 로딩 애니메이션 (흰색 막대기) -->
                <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); display: flex; gap: 5px;">
                    <div class="loading-bar"></div>
                    <div class="loading-bar"></div>
                    <div class="loading-bar"></div>
                    <div class="loading-bar"></div>
                    <div class="loading-bar"></div>
                </div>
            </div>
            <!-- 로딩 텍스트 -->
            <h2 style="color: white; margin-top: 20px;">로딩중입니다.</h2>
            <p style="color: white;">잠시만 기다려주십시오</p>
        </div>

        <!-- CSS 애니메이션 정의 -->
        <style>
        .loading-bar {
            width: 8px;
            height: 30px;
            background-color: white;
            animation: loading 1s infinite;
        }
        .loading-bar:nth-child(1) { animation-delay: 0s; }
        .loading-bar:nth-child(2) { animation-delay: 0.2s; }
        .loading-bar:nth-child(3) { animation-delay: 0.4s; }
        .loading-bar:nth-child(4) { animation-delay: 0.6s; }
        .loading-bar:nth-child(5) { animation-delay: 0.8s; }

        @keyframes loading {
            0%, 100% { transform: scaleY(1); }
            50% { transform: scaleY(2); }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    time.sleep(3)  # 데이터 처리 시간을 시뮬레이션




    # 선택한 농장 데이터 필터링
    farm_data = df if selected_farm == '전체' else df[df['농장아이디'] == selected_farm]

     # KPI 지표 계산
    total_cattle = farm_data['개체번호'].nunique()
    total_milk = farm_data['착유량(L)'].sum()
    avg_milk = round(farm_data['착유량(L)'].mean(), 2)
    avg_milking_rounds = round(farm_data['착유회차'].mean(), 2) if '착유회차' in farm_data.columns else 'N/A'
    avg_milking_time = round(farm_data['착유 소요 시간(분)'].mean(), 2)

    # 전체 평균 계산
    overall_avg_milk = round(df['착유량(L)'].mean(), 2)
    overall_avg_rounds = round(df['착유회차'].mean(), 2) if '착유회차' in df.columns else 'N/A'
    overall_avg_time = round(df['착유 소요 시간(분)'].mean(), 2)

    def format_change(value, avg_value, unit=""):
        change = round(abs(value - avg_value), 2)
        arrow = "▲" if value >= avg_value else "▼"
        color = "red" if value >= avg_value else "blue"
        return f'<span style="color:{color}">전체 대비 {arrow} {change} {unit}</span>'


    # KPI 표시
    st.subheader(f'📈 "{selected_farm}" 농장 KPI')
    col1, col2, col3, col4, col5 = st.columns(5)

    col1.markdown(f'<h5 style="font-size:16px; margin:0;">개체수</h5><h1 style="font-size:40px; margin:0;">{total_cattle}</h1>', unsafe_allow_html=True)
    col2.markdown(f'<h5 style="font-size:16px; margin:0;">총 착유량</h5><h1 style="font-size:40px; margin:0;">{total_milk:,.0f}L</h1>', unsafe_allow_html=True)
    col3.markdown(f'<h5 style="font-size:16px; margin:0;">평균 착유량</h5><h1 style="font-size:40px; margin:0;">{avg_milk} L</h1><p>' + format_change(avg_milk, overall_avg_milk, 'L') + '</p>', unsafe_allow_html=True)
    col4.markdown(f'<h5 style="font-size:16px; margin:0;">평균 착유 회차</h5><h1 style="font-size:40px; margin:0;">{avg_milking_rounds} 회</h1><p>' + format_change(avg_milking_rounds, overall_avg_rounds, '회') + '</p>', unsafe_allow_html=True)
    col5.markdown(f'<h5 style="font-size:16px; margin:0;">평균 착유 소요 시간</h5><h1 style="font-size:40px; margin:0;">{avg_milking_time} 분</h1><p>' + format_change(avg_milking_time, overall_avg_time, '분') + '</p>', unsafe_allow_html=True)



# 날짜 선택 (달력을 드롭다운으로 감추기)
with st.expander("📅 날짜 필터"):
    selected_date = st.date_input("날짜를 선택하세요:")

# 선택한 날짜에 해당하는 데이터 필터링
df['날짜'] = pd.to_datetime(df['착유시작일시']).dt.date
filtered_data = df[(df['날짜'] == selected_date) & (df['농장아이디'] == selected_farm if selected_farm != '전체' else True)]

# 데이터가 없는 경우에만 경고 메시지 출력
if filtered_data.empty:
    st.warning("선택한 날짜에 해당하는 데이터가 없습니다.")



# 📊 2열 2행 구조로 지도, 시간 필터, 기온/습도/THI 값을 배치
st.subheader("📍 농장 위치 및 기온/습도/THI")
col1, col2 = st.columns([1, 1])

# 🌍 지도 시각화 (1열)
with col1:
    shp_path = "ctprvn.shp"
    gdf_korea = gpd.read_file(shp_path).to_crs(epsg=4326)
    
# 📍 농장 선택 시 해당 위치로 지도 확대 (기본은 한국 중심)
    if selected_farm != '전체' and selected_farm in farm_data['농장아이디'].values:
    # 선택한 농장 ID의 좌표 가져오기
        selected_farm_data = farm_data[farm_data['농장아이디'] == selected_farm].iloc[0]
        map_center = [selected_farm_data['위도'], selected_farm_data['경도']]
        zoom_level = 12  # 선택한 농장에 집중
    else:
        map_center = [36.5, 127.5]  # 기본 지도 중심 (대한민국)
        zoom_level = 7

# 지도 생성 (선택된 농장에 맞게 중심과 확대 설정)
    m = folium.Map(location=map_center, zoom_start=zoom_level, tiles="OpenStreetMap", max_bounds=True, width='50%', height='50%')



    # # 지도 생성
    # # m = folium.Map(location=[36.5, 127.5], zoom_start=7, tiles="cartodbpositron", max_bounds=True) # 소희님이 만들어주신거_근데 영어어
    # m = folium.Map(location=[36.5, 127.5], zoom_start=7, tiles="OpenStreetMap", max_bounds=True) # 한글로는 나오는데 바다나옴


    # 대한민국 행정구역 지도 추가
    folium.GeoJson(
        gdf_korea,
        name="South Korea",
        style_function=lambda x: {
            "fillColor": "#BFDDB3",
            "color": "black",
            "weight": 1,
            "fillOpacity": 0.6
        },
    ).add_to(m)


     # 🔍 농장별 개체수 계산 및 좌표 데이터 준비
    farm_data = df[['농장아이디', '위도', '경도', '개체번호', '농장별 평균 유지방', '농장별 평균 유단백']].drop_duplicates()
    farm_counts = farm_data.groupby('농장아이디')['개체번호'].nunique().reset_index()
    farm_counts.columns = ['농장아이디', '개체수']
    
    farm_locations = farm_data.groupby(['농장아이디', '위도', '경도', '농장별 평균 유지방', '농장별 평균 유단백']).size().reset_index().drop(columns=0)
    farm_locations = farm_locations.merge(farm_counts, on='농장아이디')

    

    # 사용자 정의 아이콘 설정 (개체수에 따라 크기 조절)
    icon_path = "cowicon.png"
   
    if not os.path.exists(icon_path):
        st.error("아이콘 이미지가 존재하지 않습니다. 올바른 파일 경로를 확인해주세요.")
    else:
        min_count = farm_locations["개체수"].min()
        max_count = farm_locations["개체수"].max()
        
        for _, row in farm_locations.iterrows():
            size = 30 + (row["개체수"] - min_count) / (max_count - min_count) * 30 if max_count > min_count else 30
            custom_icon = CustomIcon(icon_path, icon_size=(int(size), int(size)))
            
            # 📝 팝업 콘텐츠에 기존 CSV 컬럼의 평균 유지방 및 평균 유단백 사용
            popup_content = f"""
            <div style="width: 250px; font-size: 18px;">
                <strong>농장 ID:</strong> {int(row['농장아이디'])}<br>
                <strong>개체수:</strong> {int(row['개체수'])}<br>
                <strong>평균 유지방:</strong> {row['농장별 평균 유지방']:.2f}%<br>
                <strong>평균 유단백:</strong> {row['농장별 평균 유단백']:.2f}%
            </div>
            """
            
            folium.Marker(
                location=[row["위도"], row["경도"]],
                icon=custom_icon,
                popup=folium.Popup(popup_content, max_width=300),  # 팝업 크기 및 스타일 조정
            ).add_to(m)

# 지도 렌더링은 마지막에 한 번만 호출
    folium_static(m)




# 시간 (Hour) 컬럼 추가
filtered_data['시간'] = filtered_data['착유시작일시'].dt.hour


# 🕒 24시간 체제 시간 선택 필터를 드롭다운 스타일로 변경하고 기온/습도/THI 값 (2열)
with col2:
    df['시간'] = df['착유시작일시'].dt.hour

    with st.expander("⏰ 시간 필터"):
        selected_hour = st.selectbox('시간을 선택하세요 (24시간 체제)', list(range(24)), key='hour_select')



    # 선택한 시간에 해당하는 데이터 필터링
    selected_data = df[(df['시간'] == selected_hour) & (df['농장아이디'] == selected_farm if selected_farm != '전체' else True)]





 # 📊 2열 2행: 기온, 습도, THI 값을 가로로 표시 (항목 이름 추가 및 동일한 반지름의 원형 표시)
    if not filtered_data.empty:
        row = filtered_data.iloc[0]
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<h4 style="text-align:center;">🌡️ 기온</h4>', unsafe_allow_html=True)
            st.markdown(f'<div style="text-align:center; font-size:40px; padding:30px; border-radius:50%; background-color:#FFD1DC; color:white; width:100px; height:100px; margin:auto; display:flex; align-items:center; justify-content:center;">{row["기온(℃)"]:.1f}°C</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<h4 style="text-align:center;">💧 습도</h4>', unsafe_allow_html=True)
            st.markdown(f'<div style="text-align:center; font-size:40px; padding:30px; border-radius:50%; background-color:#BDE4F4; color:white; width:100px; height:100px; margin:auto; display:flex; align-items:center; justify-content:center;">{row["습도(%)"]:.1f}%</div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<h4 style="text-align:center;">📈 THI</h4>', unsafe_allow_html=True)
            st.markdown(f'<div style="text-align:center; font-size:40px; padding:30px; border-radius:50%; background-color:#C4E3CB; color:white; width:100px; height:100px; margin:auto; display:flex; align-items:center; justify-content:center;">{row["THI"]:.1f}</div>', unsafe_allow_html=True)
    

    # 날짜 및 시간 정보 표시 (둥근 네모 도형으로 표시, 크림색 배경 적용)
        st.markdown('<div style="height:80px;"></div>', unsafe_allow_html=True)  # 간격 추가
        st.markdown(f'<div style="text-align:center; font-size:30px; padding:20px; border-radius:15px; background-color:#F5F5F5; color:black; width:800px; margin:auto; display:flex; align-items:center; justify-content:center;">{selected_date} {selected_hour:02d}:00 경</div>', unsafe_allow_html=True)
    else:
        st.warning("선택한 시간에 해당하는 데이터가 없습니다.")


# 로딩이 완료되면 GIF를 숨김
loading_container.empty()


