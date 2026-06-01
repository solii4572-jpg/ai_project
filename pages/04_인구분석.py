import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. 페이지 설정
st.set_page_config(page_title="서울시 인구 분석", layout="wide")

# 2. 파이썬 3.14 호환용 가장 안전한 폰트 기본 설정 (오류 발생 소지 원천 차단)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

# 3. 녹차색 테마 스타일 적용 (가장 단순한 단일 라인 문자열로 SyntaxError 방지)
st.markdown("<style>.stApp {background-color: #D2E0FB;} h1, h2, h3 {color: #3A4D39;}</style>", unsafe_allow_html=True)

st.title("🍵 서울시 행정구별 연령대 인구수 분석")
st.markdown("population.csv 파일을 업로드하면 꺾은선 그래프를 확인할 수 있습니다.")

# 4. 파일 업로드 기능
uploaded_file = st.file_uploader("CSV 파일을 업로드 하세요", type=["csv"])

if uploaded_file is not None:
    # 5. 다중 인코딩 지원 파일 읽기
    df = None
    for enc in ['utf-8', 'cp949', 'euc-kr', 'utf-8-sig']:
        try:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, encoding=enc)
            break
        except Exception:
            continue
            
    if df is None:
        st.error("파일을 읽을 수 없습니다. CSV 파일 형식을 확인해주세요.")
        st.stop()
        
    try:
        # 6. 데이터 정제 및 숫자 변환 (쉼표 제거)
        for col in df.columns[1:]:
            df[col] = df[col].astype(str).str.replace(',', '', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
            
        # '서울특별시' 전체 행 제거 (순수 구 데이터만 남김)
        df_districts = df[df['행정구역'].str.contains('전체') == False].copy()
        
        # 행정구역 이름에서 구 이름만 깔끔하게 분리
        df_districts['구이름'] = df_districts['행정구역'].apply(lambda x: str(x).split()[1] if len(str(x).split()) > 1 else str(x))
        
        # 7. 사이드바 필터 설정
        st.sidebar.header("🌿 필터 설정")
        selected_district = st.sidebar.selectbox("행정구를 선택하세요", df_districts['구이름'].unique())
        
        # 선택된 구의 데이터 매핑
        district_data = df_districts[df_districts['구이름'] == selected_district].iloc[0]
        
        # 8. CSV 원본 컬럼명과 그래프에 표시할 나이 이름 1:1 매치
        age_map = {
            '0~9세': '0-9세',
            '2026년04월_거주자_10~19세': '10-19세',
            '2026년04월_거주자_20~29세': '20-29세',
            '2026년04월_거주자_30~39세': '30-39세',
            '2026년04월_거주자_40~49세': '40-49세',
            '2026년04월_거주자_50~59세': '50-59세',
            '2026년04월_거주자_60~69세': '60-69세',
            '2026년04월_거주자_70~79세': '70-79세',
            '2026년04월_거주자_80~89세': '80-89세',
            '2026년04월_거주자_90~99세': '90-99세',
            '100세 이상': '100세이상'
        }
        
        x_data = []
        y_data = []
        for csv_col, target_label in age_map.items():
            if csv_col in district_data.index:
                x_data.append(target_label)
                y_data.append(int(district_data[csv_col]))
                
        # 9. 꺾은선 그래프 그리기 (녹차색 설정)
        st.subheader(f"📈 {selected_district} 연령별 인구수 추이")
        
        fig, ax = plt.subplots(figsize=(12, 6))
        fig.patch.set_facecolor('#ECEEAF')  # 바탕색: 연한 녹차색
        ax.set_facecolor('#F3F4ED')        # 표 안쪽: 말차 라떼색
        
        # 꺾은선 스타일
        ax.plot(x_data, y_data, color='#4F6F52', linestyle='-', linewidth=3, marker='o', markersize=8, markerfacecolor='#E8FFCE', markeredgecolor='#4F6F52')
        
        ax.grid(True
