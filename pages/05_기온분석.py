import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 스트림릿 리눅스 서버 환경 폰트 설정 및 깨짐 방지
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

st.title("🌡️ 서울 역대 특정 날짜 기온 추이")
st.markdown("특정 월과 일을 선택하면, 1907~2018년 동안 해당 날짜의 기온 변화를 보여줍니다.")

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

    # 사이드바에서 월과 일 따로 선택받기
    st.sidebar.header("📅 분석할 날짜 선택")
    
    selected_month = st.sidebar.selectbox("월을 선택하세요", list(range(1, 13)), index=9) # 기본값 10월
    selected_day = st.sidebar.selectbox("일을 선택하세요", list(range(1, 32)), index=0)   # 기본값 1일

    # 선택한 월/일에 맞는 데이터 필터링 (예: 역대 모든 해의 10월 1일 데이터 모으기)
    filtered_df = df[(df['월'] == selected_month) & (df['일'] == selected_day)].sort_values(by='연도')

    if not filtered_df.empty:
        st.subheader(f"📊 역대 {selected_month}월 {selected_day}일 기온 변화 추이 (1907 ~ 2018)")
        
        # 꺾은선 그래프 그리기
        fig, ax = plt.subplots(figsize=(11, 5))
        
        # 요구사항 반영: 최고기온(핫핑크), 최저기온(연한 하늘색), 범례 표시
        ax.plot(filtered_df['연도'], filtered_df['최고기온'], color='deeppink', marker='o', label='Max Temp (C)', linewidth=1.5, markersize=4)
        ax.plot(filtered_df['연도'], filtered_df['최저기온'], color='lightskyblue', marker='o', label='Min Temp (C)', linewidth=1.5, markersize=4)
        
        # 축 및 그리드 레이아웃 설정
        ax.set_xlabel("Year")
        ax.set_ylabel("Temperature (C)")
        ax.grid(True, linestyle='--', alpha=0.5)
        
        # 범례 표시
        ax.legend(loc='upper right')
        
        # 스트림릿 화면에 그래프 띄우기
        st.pyplot(fig)
        
        # 상세 데이터 테이블 제공
        with st.expander("📊 상세 데이터 확인하기"):
            st.dataframe(filtered_df[['연도', '최저기온', '최고기온']].reset_index(drop=True))
            
    else:
        st.warning(f"선택하신 {selected_month}월 {selected_day}일에 해당하는 데이터가 없습니다. (윤년 데이터 등 확인 필요)")

except FileNotFoundError:
    st.error("💡 `seoul.csv` 파일을 찾을 수 없습니다. 파일이 동일한 깃허브 저장소 위치에 업로드 되었는지 확인하세요.")
except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
