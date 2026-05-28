import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 데이터 로딩 및 캐싱
@st.cache_data
def load_data():
    return pd.read_csv("countriesMBTI_16types.csv")

def main():
    st.title("🌍 MBTI별 상위 10개국 대시보드")
    st.markdown("특정 MBTI 유형을 선택하면, 전 세계에서 해당 유형의 비율이 가장 높은 상위 10개 국가를 시각화합니다.")

    try:
        df = load_data()
    except Exception as e:
        st.error("데이터 파일('countriesMBTI_16types.csv')을 찾을 수 없습니다. 파일이 스크립트와 같은 폴더에 있는지 확인해 주세요.")
        return

    # MBTI 유형 선택 리스트 추출 (Country 열 제외)
    mbti_types = [col for col in df.columns if col != 'Country']
    mbti_types = sorted(mbti_types)
    selected_mbti = st.selectbox("🎯 분석할 MBTI 유형을 선택하세요:", mbti_types, index=0)

    # 선택된 MBTI에 대해 국가별 데이터 추출, 퍼센트(%) 변환 및 상위 10개 추출
    df_mbti = df[['Country', selected_mbti]].copy()
    df_mbti[selected_mbti] = df_mbti[selected_mbti].astype(float) * 100
    df_top10 = df_mbti.sort_values(by=selected_mbti, ascending=False).head(10).reset_index(drop=True)

    # 주요 상위 지표 요약 표시 (Metric)
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label=f"🥇 {selected_mbti} 비율 1위 국가", value=df_top10.loc[0, 'Country'], delta=f"{df_top10.loc[0, selected_mbti]:.2f}%")
    with col2:
        st.metric(label=f"🔟 상위 10위 국가 ({df_top10.loc[9, 'Country']}) 비율", value=f"{df_top10.loc[9, selected_mbti]:.2f}%")

    # 🎨 색상 그라데이션 생성 (1등: 핫핑크, 나머지 9개국: 점점 흐려지는 초록색)
    colors_list = ["#FF69B4"] # 1등 Hot Pink 고정
    for i in range(9):
        mix = i / 8.0 if i > 0 else 0.0
        # 진한 초록색(rgb(46, 125, 50))에서 연한 초록색(rgb(200, 235, 200))으로 순위에 따라 보간
        r = int(46 + (200 - 46) * mix)
        g = int(125 + (235 - 125) * mix)
        b = int(50 + (200 - 50) * mix)
        colors_list.append(f"rgb({r}, {g}, {b})")

    # Plotly 막대그래프 생성
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_top10['Country'],
        y=df_top10[selected_mbti],
        text=[f"{val:.2f}%" for val in df_top10[selected_mbti]],
        textposition='auto',
        marker_color=colors_list,
        hovertemplate="<b>%{x}</b>: %{y:.2f}%<extra></extra>"
    ))

    fig.update_layout(
        title=f"<b>전 세계 {selected_mbti} 비율 상위 10개국 순위</b>",
        xaxis_title="국가",
        yaxis_title="비율 (%)",
        template="plotly_white",
        height=500,
        yaxis=dict(ticksuffix="%")
    )

    st.plotly_chart(fig, use_container_width=True)

    # 데이터 상세 보기 테이블
    with st.expander("📊 상위 10개국 원본 데이터 보기"):
        details_df = df_top10.copy()
        details_df.columns = ['국가명', f'비율 (%)']
        details_df.index = details_df.index + 1
        st.dataframe(details_df, use_container_width=True)

if __name__ == "__main__":
    main()
