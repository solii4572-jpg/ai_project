import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ------------------ 스트림릿 페이지 설정 ------------------
st.set_page_config(page_title="서울시 인구 분석", layout="wide")

# ------------------ 한글 폰트 설정 (오류 완벽 방어) ------------------
try:
    font_names = [f.name for f in fm.fontManager.ttflist]
    if 'NanumGothic' in font_names:
        plt.rc('font', family='NanumGothic')
    elif 'Malgun Gothic' in font_names:
        plt.rc('font', family='Malgun Gothic') 
    else:
        plt.rc('font', family='DejaVu Sans')
except Exception:
    # 폰트 매니저가 오작동하더라도 앱이 멈추지 않도록 기본 설정으로 우회
    plt.rc('font', family='sans-serif')

plt.rcParams['axes.unicode_minus'] = False

# ------------------ 녹차색 테마 스타일 적용 ------------------
st.markdown("""
    <style>
    .stApp {
        background-color: #D2E0FB; /* 연한 녹차/밀크티 느낌의 배경 */
    }
    h1, h2, h3 {
        color: #3A4D39; /* 짙은 녹차색 타이틀 */
    }
    </style>
""", unsafe_allow_html=True)

st.title("🍵 서울시 행정구별 연령대 인구수 분석")
st.markdown("`population.csv` 파일을 업로드하면 지정된 테마의 꺾은선 그래프를 확인할 수 있습니다.")

# 1. 파일 업로드 기능
uploaded_file = st.file_uploader("CSV 파일을 업로드 하세요", type=["csv"])

if uploaded_file is not None:
    # ------------------ 인코딩 예외 처리 구현 ------------------
    df = None
    encodings = ['utf-8', 'cp949', 'euc-kr', 'utf-8-sig']
    
    for encoding in encodings:
        try:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, encoding=encoding)
            break
        except Exception:
            continue
            
    if df is None:
        st.error("❌ 파일의 인코딩을 인식할 수 없습니다. UTF-8 또는 CP949 형식의 CSV 파일인지 확인해 주세요.")
        st.stop()
        
    try:
        # 2. 데이터 전처리 (콤마 및 문자열 전처리 완벽 방어)
        columns_to_convert = df.columns[1:]
        for col in columns_to_convert:
            # 숫자가 아닌 문자열이나 결측치가 섞여 있을 경우를 대비해 예외 처리 변환
            df[col] = df[col].astype(str).str.replace(',', '', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
            
        # '서울특별시' 전체 행(가장 상단 데이터) 제외하고 구 데이터만 필터링
        # 공백이 여러 개 들어간 경우(\s+)까지 정규식으로 안전하게 걸러냅니다.
        df_districts = df[~df['행정구역'].str.contains('서울특별시\s+', na=False, regex=True)].copy()
        
        # 행정구역명 정제 (예: "서울특별시 종로구 (1111000000)" -> "종로구")
        def extract_gu_name(x):
            parts = str(x).split()
            if len(parts) > 1:
                return parts[1]  # '종로구' 추출
            return str(x)
            
        df_districts['구이름'] = df_districts['행정구역'].apply(extract_gu_name)
        
        # 3. 사이드바 검색 필터
        st.sidebar.header("🌿 필터 설정")
        unique_gus = df_districts['구이름'].unique()
        selected_district = st.sidebar.selectbox("행정구를 선택하세요", unique_gus)
        
        # 선택한 구의 데이터 추출
        district_data = df_districts
