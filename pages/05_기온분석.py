import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="서울 기온 데이터 시각화", layout="centered")
st.title("🌡️ 서울 역대 기온 데이터 조회")
st.markdown("1907년부터 2018년까지의 서울 기온 데이터를 조회하고 그래프를 확인하세요.")

# 2. 데이터 로드 및 전처리 (캐싱 처리로 속도 향상)
@st.cache_data
def load_data():
    # 데이터 불러오기
    df = pd.read_csv("seoul.csv")
    
    # '날짜' 열의 앞뒤 공백 및 탭 문자(\t) 제거 후 datetime 형식으로 변환
    df['날짜'] = df['날짜'].astype(str).str.strip()
    df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
    
    # 기온 데이터 내 혹시 모를 결측치 제거 또는 실수형 변환
    df['최저기온(℃)'] = pd.to_numeric(df['최저기온(℃)'], errors='coerce')
    df['최고기온(℃)'] = pd.to_numeric(df['최고기온(℃)'], errors='coerce')
    
    # 결측치 행 제거
    df = df.dropna(subset=['날짜', '최저기온(℃)', '최고기온(℃)'])
    return df

try:
    df = load_data()

    # 3. 사이드바 - 날짜 선택창 구성
    min_date = df['날짜'].min().to_pydatetime()
    max_date = df['날짜'].max().to_pydatetime()

    st.sidebar.header("🔍 조회 조건 설정")
    
    # 사용자가 기간을 편리하게 선택할 수 있도록 날짜 범위 입력기 제공
    date_range = st.sidebar.date_input(
        "조회할 기간을 선택하세요",
        value=(min_date, min_date + pd.Timedelta(days=30)), # 기본값: 초기 30일
        min_value=min_date,
        max_value=max_date
    )

    # 시작일과 종료일이 모두 선택되었을 때만 그래프 그리기
    if len(date_range) == 2:
        start_date, end_date = date_range
        
        # 선택한 날짜에 맞게 데이터 필터링
        filtered_df = df[(df['날짜'] >= pd.to_datetime(start_date)) & (df['날짜'] <= pd.to_datetime(end_date))]
        
        if not filtered_df.empty:
            st.subheader(f"📅 {start_date} ~ {end_date} 기온 그래프")
            
            # 4. 꺾은선 그래프 그리기 (Matplotlib)
            fig, ax = plt.subplots(figsize=(10, 5))
            
            # 최고기온: 핫핑크(deeppink), 최저기온: 연한 하늘색(lightskyblue)
            ax.plot(filtered_df['날짜'], filtered_df['최고기온(℃)'], color='deeppink', marker='o', label='최고기온(℃)', linewidth=2)
            ax.plot(filtered_df['날짜'], filtered_df['최저기온(℃)'], color='lightskyblue', marker='o', label='최저기온(℃)', linewidth=2)
            
            # 그래프 꾸미기 (X축 날짜 포맷팅)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            fig.autofmt_xdate() # 날짜 겹침 방지 회전
            
            ax.set_ylabel("기온 (℃)")
            ax.grid(True, linestyle='--', alpha=0.5)
            
            # 범례 표시
            ax.legend(loc='upper right')
            
            # 스트림릿 화면에 그래프 출력
            st.pyplot(fig)
            
            # 선택한 기간의 데이터 테이블도 함께 보여주기
            with st.expander("📊 선택한 기간 데이터 자세히 보기"):
                st.dataframe(filtered_df[['날짜', '평균기온(℃)', '최저기온(℃)', '최고기온(℃)']].reset_index(drop=True))
        else:
            st.warning("선택한 기간에 해당하는 데이터가 없습니다.")
            
except FileNotFoundError:
    st.error("💡 폴더 내에 `seoul.csv` 파일이 있는지 확인해 주세요. 스트림릿 클라우드에 깃허브를 연동할 때 깃허브 저장소(Repository) 안에도 이 파일이 함께 업로드되어 있어야 합니다.")
