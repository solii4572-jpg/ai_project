import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. 페이지 설정
st.set_page_config(
    page_title="Global MBTI Dashboard",
    page_icon="📊",
    layout="centered"
)

# 2. 데이터 로드 함수
@st.cache_data
def load_data():
    # 앱과 동일한 경로에 있는 CSV 파일을 읽어옵니다.
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터 파일을 불러오지 못했습니다. 'countriesMBTI_16types.csv' 파일이 같은 폴더에 있는지 확인해주세요. 에러: {e}")
    st.stop()

# 3. 타이틀 및 설명
st.title("🌍 국가별 MBTI 분포 대시보드")
st.markdown("원하는 국가를 선택하면 16가지 MBTI 성격 유형 비율을 분석하여 시각화합니다.")

# 4. 국가 선택 사이드바/셀렉트박스
countries = sorted(df['Country'].unique())
# 기본값으로 South Korea가 있으면 선택, 없으면 첫 번째 국가 지정
default_index = countries.index("South Korea") if "South Korea" in countries else 0
selected_country = st.selectbox("📊 분석할 국가를 선택하세요:", countries, index=default_index)

# 5. 데이터 추출 및 가공
country_data = df[df['Country'] == selected_country].iloc[0]
# 국가명 제외한 MBTI 데이터만 추출 후 숫자로 변환
mbti_series = country_data.drop('Country').astype(float)
# 퍼센트 단위(%)로 변환
mbti_series = mbti_series * 100
# 비율이 높은 순서대로 정렬
mbti_sorted = mbti_series.sort_values(ascending=False)

# 6. 상위 데이터 스탯 표시
col1, col2 = st.columns(2)
with col1:
    st.metric(label=f"🥇 {selected_country}의 가장 흔한 MBTI", value=mbti_sorted.index[0], delta=f"{mbti_sorted.iloc[0]:.2f}%")
with col2:
    st.metric(label=f"🫥 {selected_country}의 가장 희귀한 MBTI", value=mbti_sorted.index[-1], delta=f"{mbti_sorted.iloc[-1]:.2f}%", delta_color="inverse")

# 7. 색상 그라데이션 생성 (1등: 핫핑크, 나머지: 흐려지는 초록색)
def get_green_gradient(n_colors):
    # 2등부터 마지막 등수까지 서서히 흐려지는 선형 그라데이션 색상 생성
    colors = []
    for i in range(n_colors):
        mix = i / max(1, (n_colors - 1))
        # 진한 초록(rgb(46, 125, 50))에서 연한 초록(rgb(232, 245, 233))으로 가중치 믹스
        r = int(46 + (232 - 46) * mix)
        g = int(125 + (245 - 125) * mix)
        b = int(50 + (233 - 50) * mix)
        colors.append(f"rgb({r}, {g}, {b})")
    return colors

# 전체 16개 유형에 적용할 색상 리스트 작성
colors_list = []
colors_list.append("#FF69B4")  # 1등 색상: 핫핑크
colors_list.extend(get_green_gradient(15))  # 나머지 15개 유형: 그라데이션 초록색

# 8. Plotly 막대그래프 생성
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
    title=f"<b>{selected_country} MBTI 유형별 비율 순위 (%)</b>",
    xaxis_title="MBTI 성격 유형",
    yaxis_title="비율 (%)",
    template="plotly_white",
    height=550,
    margin=dict(l=40, r=40, t=60, b=40),
    yaxis=dict(ticksuffix="%")
)

# 9. 그래프 출력
st.plotly_chart(fig, use_container_width=True)

# 10. 데이터 테이블 상세 보기
with st.expander("📊
