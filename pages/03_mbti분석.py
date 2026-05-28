import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 타이틀 출력
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
# matplotlib과 seaborn을 활용하여 부드럽고 안전한 컬러 구성
colors = []
colors.append("#FF69B4")  # 1등: 핫핑크

# 2등부터 16등까지 점점 흐려지는 초록색 배열 (YlGn 맵에서 진한 영역 위주 추출)
green_palette = sns.color_palette("Greens_r", n_colors=25)  
for i in range(15):
    # 너무 투명해서 안 보이지 않도록 앞쪽(진한 쪽)의 색상들을 순서대로 매핑
    colors.append(green_palette[i+3])

# 그래프 그리기 (Matplotlib Figure)
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(mbti_sorted.index, mbti_sorted.values, color=colors, edgecolor='none')

# 그래프 스타일 설정
ax.set_title(f"{selected_country} MBTI 유형별 비율 순위 (%)", fontsize=14, pad=15, fontweight='bold')
ax.set_ylabel("비율 (%)", fontsize=11)
ax.set_xlabel("MBTI 유형", fontsize=11)
ax.grid(axis='y', linestyle='--', alpha=0.5)

# 막대 위에 숫자(텍스트) 표시
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, height + 0.1, f"{height:.1f}%", ha='center', va='bottom', fontsize=9)

# 테두리 깔끔하게 정리
sns.despine(ax=ax)
plt.tight_layout()

# Streamlit에 그래프 출력
st.pyplot(fig)

# 원본 데이터 상세 보기 테이블
with st.expander("📊 원본 데이터 테이블 보기"):
    details_df = pd.DataFrame({
        'MBTI 유형': mbti_sorted.index,
        '비율 (%)': mbti_sorted.values
    }).reset_index(drop=True)
    details_df.index = details_df.index + 1
    st.dataframe(details_df, use_container_width=True)
