import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# [방어 코드] 스트림릿 리눅스 서버에서 한글 깨짐 및 에러 방지
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="서울 기온 데이터 시각화", layout="centered")
st.title("🌡️ 서울 역대 기온 데이터 조회")
st.markdown("1907년부터 2018년까지의 서울 기온 데이터를 조회하고 그래프를 확인하세요.")

# 2. 데이터 로드 및 전처리 (캐싱 처리)
@st.cache_data
def load_data():
    # [무적의 방어 코드] 여러 인코딩 방식을 순서대로 시도하여 성공하는 것으로 읽어옵니다.
    encodings = ['cp949', 'utf-8', 'euc-kr', 'utf-8-sig']
    df = None
    
    for enc in encodings:
        try:
            df = pd.read_csv("seoul.csv", encoding=enc)
            # 만약 첫 번째 열 이름에 '날짜'라는 글자가 제대로 포함되어 있다면 성공으로 간주
            if any('날짜' in str(col) for col in df.columns):
                break
        except Exception:
            continue
            
    # 만약 모든 인코딩이 실패했을 경우를 위한 마지막 보루
    if df is None:
        df = pd.read_csv("seoul.csv", encoding='cp949', errors='ignore')

    # '날짜' 열의 이름과 데이터에 붙은 공백 및 특수기호 완벽 제거
    df.columns = df.columns.str.strip()
    
    # 실제 '날짜'가 포함된 열 찾기 (글자 깨짐 대비)
    date_col = [col for col in df.columns if '날짜' in col]
    if date_col:
        df = df.rename(columns={date_col[0]: '날짜'})
    
    df['날짜'] = df['날짜'].astype(str).str.replace(r'[\t\s"\']', '', regex=True)
    df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
    
    # 기온 데이터 열 이름 정제 (깨짐 방지 처리 포함)
    for col in df.columns:
        if '최저' in col:
            df = df.rename(columns={col: '최저기온(℃)'})
        elif '최고' in col:
            df = df.rename(columns={col: '최고기온(℃)'})
        elif '평균' in col:
            df = df.rename(columns={col: '평균기온(℃)'})

    # 숫자 변환 및 결측치 제거
    df['최저기온(℃)'] = pd.to_numeric(df['최저기온(℃)'], errors='coerce')
    df['최고기온(℃)'] = pd.to_numeric(df['최고기온(℃)'], errors='coerce')
    df = df.dropna(subset=['날짜', '최저기온(℃)', '최고기온(℃)'])
    
    return df

try:
    df = load_data()

    # 3. 사이드바 - 날짜 선택창 구성
    min_date = df['날짜'].min().to_pydatetime()
    max_date = df['날짜'].max().to_pydatetime()

    st.sidebar.header("🔍 조회 조건 설정")
    
    # 기본값으로 데이터의 첫 시작일부터 30일간을 지정
    date_range = st.sidebar.date_input(
        "조회할 기간을 선택하세요",
        value=(min_date, min_date + pd.Timedelta(days=30)),
        min_value=min_date,
        max_value=max_date
    )

    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = df[(df['날짜'] >= pd.to_datetime(
