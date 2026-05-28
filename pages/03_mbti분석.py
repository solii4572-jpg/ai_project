import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 타이틀 및 설명
st.title("🌍 국가별 MBTI 분포 대시보드")
st.markdown("원하는 국가를 선택하면 16가지 MBTI 성격 유형 비율을 분석하여 시각화합니다.")

# 데이터 불러오기
try:
    df = pd.read_csv("countriesMBTI_16types.csv")
except Exception as e:
    st.error("데이터 파일('countriesMBTI_16types.csv')을 찾을 수 없습니다. 파일이 같은 폴더에 있는지 확인해 주세요.")
    st.stop()

# 국가 선택 박스
countries = sorted(df['Country'].unique())
default_idx = countries.index("South Korea") if "South Korea" in countries else 0
selected_country = st.selectbox("📊 분석할 국가를 선택하세요:", countries, index=default_idx)

# 선택된 국가의 데이터 추출 및 정렬 (퍼센트 변환)
country_data = df[df['Country'] == selected_country].iloc[0]
mbti_data = country_data.drop('Country').astype(float) * 100
mbti_sorted = mbti_data.sort_values(ascending=False)

# 상위 요약 지표 (Metric)
col1, col2 = st.columns(2)
with col1:
    st.metric(label=f"🥇 {selected_country} 최다 MBTI", value=mbti_sorted.index[0], delta=f"{mbti_sorted.iloc[0]:.2f}%")
with col2:
    st.metric(label=f"🫥 {selected_country} 최소 MBTI", value=mbti_sorted.index[-1], delta=f"{mbti_sorted.iloc[-1]:.2f}%", delta_color="inverse")

# 🎨 색상 그라데이션 생성 (1등: 핫핑크, 나머지: 흐려지는 초록색)
colors_list = ["#FF69B4"] # 1등 Hot Pink
for i in range(15):
    mix = i / 14.0
    # 진한 초록색(46, 125, 50)에서 연한 초록색(220, 240, 220)으로 보간
    r = int(46 + (220 - 46) * mix)
    g = int(125 + (240 - 125) * mix)
    b = int(50 + (220 - 50) * mix)
    colors_list.append(f"rgb({r}, {g}, {b})")

# Plotly 차트 생성
fig = go.Figure()
fig.add_trace(go.Bar(
    x=mbti_sorted.index,
    y=mbti_sorted.values,
    text=[f"{val:.2f}%" for val in mbti_sorted.values],
    textposition='auto',
    marker_color=colors_list,
    hovertemplate="<b>%{x}</b>: %{y:.2f}%<extra></extra>"
))

fig.update_layout(
    title=f"<b>{selected_country} MBTI 유형별 비율 순위</b>",
    xaxis_title="MBTI 유형",
    yaxis_title="비율 (%)",
    template="plotly_white",
    height=500,
    yaxis=dict(ticksuffix="%")
)

st.plotly_chart(fig, use_container_width=True)

# 데이터 상세 보기 테이블
with st.expander("📊 원본 데이터 테이블 보기"):
    details_df = pd.DataFrame({
        'MBTI 유형': mbti_sorted.index,
        '비율 (%)': mbti_sorted.values
    }).reset_index(drop=True)
    details_df.index = details_df.index + 1
    st.dataframe(details_df, use_container_width=True)
