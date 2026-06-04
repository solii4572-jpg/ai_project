import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# 스트림릿 리눅스 서버 환경 폰트 설정 및 깨짐 방지
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

st.title("🌡️ 서울 역대 기온 조회 및 미래 예측")
st.markdown("특정 월/일을 선택하면 과거 기온 추이를 보여주고, 선형 회귀 모델을 통해 미래의 기온을 예측합니다.")

@st.cache_data
def load_data():
    # 인코딩 자동 탐색 알고리즘
    for enc in ['cp949', 'utf-8', 'euc-kr', 'utf-8-sig']:
        try:
            df = pd.read_csv("seoul.csv", encoding=enc)
            if any('날짜' in str(col) for col in df.columns):
                break
        except:
            continue

    # 열 이름 정제 (앞뒤 공백 제거)
    df.columns = df.columns.str.strip()
    
    # 열 이름 보정
    for col in df.columns:
        if "날짜" in str(col):
            df = df.rename(columns={col: "날짜"})
        elif "최저" in str(col):
            df = df.rename(columns={col: "최저기온"})
        elif "최고" in str(col):
            df = df.rename(columns={col: "최고기온"})
            
    # 날짜 정제 및 datetime 변환
    df['날짜'] = df['날짜'].astype(str).str.strip()
    df['날짜'] = df['날짜'].apply(lambda x: x.replace('\t', ''))
    df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
    
    # 기온 데이터 변환 및 결측치 제거
    df['최저기온'] = pd.to_numeric(df['최저기온'], errors='coerce')
    df['최고기온'] = pd.to_numeric(df['최고기온'], errors='coerce')
    df = df.dropna(subset=['날짜', '최저기온', '최고기온'])
    
    # 분석을 위한 연도, 월, 일 열 생성
    df['연도'] = df['날짜'].dt.year
    df['월'] = df['날짜'].dt.month
    df['일'] = df['날짜'].dt.day
    
    return df

try:
    df = load_data()

    # 사이드바 설정
    st.sidebar.header("📅 분석 및 예측 조건 설정")
    
    selected_month = st.sidebar.selectbox("월을 선택하세요", list(range(1, 13)), index=7) # 기본값 8월
    selected_day = st.sidebar.selectbox("일을 선택하세요", list(range(1, 32)), index=14)   # 기본값 15일
    
    # 미래 예측 연도 선택 (데이터가 2018년까지 있으므로 2019년부터 선택 가능)
    future_year = st.sidebar.slider("예측할 미래 연도를 선택하세요", min_value=2019, max_value=2060, value=2030)

    # 선택한 월/일에 맞는 과거 데이터 필터링
    filtered_df = df[(df['월'] == selected_month) & (df['일'] == selected_day)].sort_values(by='연도')

    if not filtered_df.empty:
        st.subheader(f"📊 역대 {selected_month}월 {selected_day}일 기온 추이 및 {future_year}년 예측")
        
        # --- 머신러닝 기온 예측 모듈 ---
        X = filtered_df['연도'].values.reshape(-1, 1) # 독립변수 (연도)
        y_max = filtered_df['최고기온'].values        # 종속변수 1 (최고기온)
        y_min = filtered_df['최저기온'].values        # 종속변수 2 (최저기온)
        
        # 최고기온 예측 모델 학습 및 예측
        model_max = LinearRegression()
        model_max.fit(X, y_max)
        pred_max = model_max.predict([[future_year]])[0]
        
        # 최저기온 예측 모델 학습 및 예측
        model_min = LinearRegression()
        model_min.fit(X, y_min)
        pred_min = model_min.predict([[future_year]])[0]
        
        # 예측 결과 상단에 출력
        col1, col2 = st.columns(2)
        col1.metric(label=f"🔮 {future_year}년 최고기온 예측", value=f"{pred_max:.1f} ℃")
        col2.metric(label=f"🔮 {future_year}년 최저기온 예측", value=f"{pred_min:.1f} ℃")
        
        # --- 그래프 시각화 ---
        fig, ax = plt.subplots(figsize=(11, 5))
        
        # 과거 데이터 선 그래프 (최고: 핫핑크, 최저: 연한 하늘색)
        ax.plot(filtered_df['연도'], filtered_df['최고기온'], color='deeppink', marker='o', label='Max Temp (C)', linewidth=1.5, markersize=4)
        ax.plot(filtered_df['연도'], filtered_df['최저기온'], color='lightskyblue', marker='o', label='Min Temp (C)', linewidth=1.5, markersize=4)
        
        # 미래 예측 포인트 그래프에 추가 (★ 모양 별표로 표시)
        ax.scatter(future_year, pred_max, color='red', marker='*', s=150, zorder=5, label=f'Predicted Max ({future_year})')
        ax.scatter(future_year, pred_min, color='blue', marker='*', s=150, zorder=5, label=f'Predicted Min ({future_year})')
        
        # 예측 포인트까지 추세가 이어지도록 점선 추가
        ax.plot([filtered_df['연도'].iloc[-1], future_year], [filtered_df['최고기온'].iloc[-1], pred_max], color='deeppink', linestyle='--', alpha=0.7)
        ax.plot([filtered_df['연도'].iloc[-1], future_year], [filtered_df['최저기온'].iloc[-1], pred_min], color='lightskyblue', linestyle='--', alpha=0.7)
        
        # 축 및 레이아웃 설정
        ax.set_xlabel("Year")
        ax.set_ylabel("Temperature (C)")
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend(loc='upper right')
        
        # 스트림릿 화면에 그래프 띄우기
        st.pyplot(fig)
        
        # 과거 데이터 및 예측 요약 보기
        with st.expander("📊 데이터 세부 정보 보기"):
            st.write(f"**과거 데이터 수:** {len(filtered_df)}개 연도 축적됨")
            st.dataframe(filtered_df[['연도', '최저기온', '최고기온']].reset_index(drop=True))
            
    else:
        st.warning(f"선택하신 {selected_month}월 {selected_day}일에 해당하는 데이터가 없습니다.")

except FileNotFoundError:
    st.error("💡 `seoul.csv` 파일을 찾을 수 없습니다. 파일이 동일한 깃허브 저장소 위치에 업로드 되었는지 확인하세요.")
except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
