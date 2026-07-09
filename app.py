import streamlit as st
import pandas as pd
import plotly.express as px

# 웹페이지 기본 설정
st.set_page_config(page_title="탄소 발자국 계산기", page_icon="🌍", layout="centered")

st.title("🌍 나의 탄소 발자국 계산기")
st.write("월간 에너지 사용량과 교통수단 이용량을 입력하여 나의 탄소 배출량을 확인해보세요!")

# 한국 기준 대략적인 탄소 배출 계수 (kg CO2 단위)
CO2_FACTOR = {
    'electricity': 0.478,  # kWh당
    'gas': 2.176,          # m³당
    'gasoline': 2.32,      # 리터당
    'diesel': 2.62,        # 리터당
    'public_transit': 0.06 # km당
}

# 왼쪽 사이드바: 사용자 입력 창
st.sidebar.header("📊 월간 사용량 입력")

st.sidebar.subheader("1. 가정 내 에너지")
electricity = st.sidebar.number_input("⚡ 전기 사용량 (kWh)", min_value=0, value=200, step=10)
gas = st.sidebar.number_input("🔥 도시가스 사용량 (m³)", min_value=0, value=50, step=5)

st.sidebar.subheader("2. 교통 및 이동")
car_type = st.sidebar.selectbox("🚗 주 이용 차량 연료", ["휘발유", "경유", "차량 없음"])

if car_type != "차량 없음":
    fuel_usage = st.sidebar.number_input("⛽ 월간 연료 사용량 (L)", min_value=0, value=50, step=5)
else:
    fuel_usage = 0

public_transit = st.sidebar.number_input("🚌 대중교통 이용 거리 (km)", min_value=0, value=100, step=10)

# 계산하기 버튼
if st.sidebar.button("계산하기", type="primary"):
    # 항목별 탄소 배출량 계산
    co2_elec = electricity * CO2_FACTOR['electricity']
    co2_gas = gas * CO2_FACTOR['gas']
    
    co2_car = 0
    if car_type == "휘발유":
        co2_car = fuel_usage * CO2_FACTOR['gasoline']
    elif car_type == "경유":
        co2_car = fuel_usage * CO2_FACTOR['diesel']
        
    co2_transit = public_transit * CO2_FACTOR['public_transit']
    
    # 총 배출량
    total_co2 = co2_elec + co2_gas + co2_car + co2_transit
    
    # 결과 출력
    st.success(f"한 달 동안 발생한 총 탄소 배출량은 **{total_co2:,.1f} kg CO2** 입니다.")
    
    # 데이터프레임 생성 및 파이 차트 시각화
    data = {
        '항목': ['전기', '도시가스', '자가용', '대중교통'],
        '배출량 (kg CO2)': [co2_elec, co2_gas, co2_car, co2_transit]
    }
    df = pd.DataFrame(data)
    
    # 배출량이 0인 항목은 차트에서 제외
    df = df[df['배출량 (kg CO2)'] > 0]
    
    st.subheader("📈 배출량 분석")
    fig = px.pie(df, values='배출량 (kg CO2)', names='항목', 
                 title='영역별 탄소 배출 비율', hole=0.4,
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)
    
    # 가장 많이 배출한 항목 찾기 및 맞춤형 피드백
    st.subheader("💡 탄소 줄이기 팁")
    max_category = df.loc[df['배출량 (kg CO2)'].idxmax()]['항목']
    
    if max_category == '전기':
        st.info("현재 **전기 사용**으로 인한 탄소 배출이 가장 많습니다. 안 쓰는 플러그를 뽑고, 에너지 효율 1등급 가전을 사용해 보세요.")
    elif max_category == '도시가스':
        st.info("현재 **가스 사용**으로 인한 탄소 배출이 가장 많습니다. 겨울철 실내 적정 온도(18~20도)를 유지하고 온수 사용을 줄여보세요.")
    elif max_category == '자가용':
        st.info("현재 **자가용 이용**으로 인한 배출량이 가장 많습니다. 가까운 거리는 걷거나 자전거를 타고, 일주일에 하루는 대중교통을 이용해 보는 건 어떨까요?")
    elif max_category == '대중교통':
        st.info("대중교통 위주로 이동하고 계시군요! 자가용 대비 탄소 배출을 획기적으로 줄이는 훌륭한 친환경 실천입니다.")
        
else:
    st.info("👈 왼쪽 사이드바에 정보를 입력하고 '계산하기' 버튼을 눌러주세요.")
