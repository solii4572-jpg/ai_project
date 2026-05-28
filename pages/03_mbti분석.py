import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("🌍 국가별 MBTI 분포 대시보드")

try:
    df = pd.read_csv("countriesMBTI_16types.csv")
except Exception as e:
    st.error("데이터 파일('countriesMBTI_16types.csv')을 찾을 수 없습니다.")
    st.stop()

countries = sorted(df['Country'].unique())
default_idx = countries.index("South Korea") if "South Korea" in countries else 0
selected_country = st.selectbox("📊 분석할 국가를 선택하세요:", countries, index=default_idx)

country_data = df[df['Country'] == selected_country].iloc[0]
mbti_data = country_data.drop('Country').astype(float) * 100
mbti_sorted = mbti_data.sort_values(ascending=False)

col1, col2 = st.columns(2)
with col1:
    st.metric(label=f"🥇 {selected_country} 최다 MBTI", value=mbti_sorted.index[0], delta=f"{mbti_sorted.iloc[0]:.2f}%")
with col2:
    st.metric(label=f"🫥 {selected_country} 최소 MBTI", value=mbti_sorted.index[-1], delta=f"{mbti_sorted.iloc[-1]:.2f}%", delta_color="inverse")

colors_list = ["#FF69B4"]
for i in range(15):
    mix = i / 14.0
    r = int(46 + (220 - 46) * mix)
    g = int(125 + (240 - 125) * mix)
    b = int(50 + (220 - 50) * mix)
    colors_list.append(f"rgb({r}, {g}, {b})")

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
