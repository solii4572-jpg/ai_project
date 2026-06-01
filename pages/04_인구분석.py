import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ------------------ 스트림릿 페이지 설정 ------------------
st.set_page_config(page_title="서울시 인구 분석", layout="wide")

# ------------------ [오류 해결] 한글 폰트 설정 ------------------
# 명시적으로 font_manager를 사용해 시스템에 설치된 폰트 목록을 가져옵니다.
font_names = [f.name for f in fm.fontManager.ttflist]

# packages.txt를 통해 설치된 'NanumGothic'이 있으면 우선 적용합니다.
if 'NanumGothic' in font_names:
    plt.rc('font', family='NanumGothic')
elif 'Malgun Gothic' in font_names:
    plt.rc('font', family='Malgun Gothic') # 로컬 윈도우 환경 테스트용
else:
    plt.rc('font', family='DejaVu Sans')   # 기본 폰트 fallback

plt.rcParams['axes.unicode_minus'] = False

# ------------------ 녹차색 테마 스타일 적용 ------------------
st.markdown("""
    <style>
    .stApp {
        background-color: #D2E0FB; /* 연한 녹차/밀크티 느낌의 베이지-그린 톤 배경 */
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
    # 데이터 로드
    df = pd.read_csv(uploaded_file)
    
    # 2. 데이터 전처리
    # 데이터 내의 콤마(,) 제거 후 정수형 변환
    columns_to_convert = df.columns[1:]
    for col in columns_to_convert:
        df[col] = df[col].astype(str).str.replace(',', '').astype(int)
        
    # '서울특별시' 전체 행 제외하고 구 데이터만 필터링
    df_districts = df[~df['행정구역'].str.contains('서울특별시  ', na=False)].copy()
    
    # 행정구역명 정제 (예: "서울특별시 종로구 (1111000000)" -> "종로구")
    df_districts['구이름'] = df_districts['행정구역'].apply(lambda x: x.split()[1] if len(x.split()) > 1 else x)
    
    # 3. 사이드바 검색 필터
    st.sidebar.header("🌿 필터 설정")
    selected_district = st.sidebar.selectbox("행정구를 선택하세요", df_districts['구이름'].unique())
    
    # 선택한 구의 데이터 추출
    district_data = df_districts[df_districts['구이름'] == selected_district].iloc[0]
    
    # 4. 연령대 매핑 (CSV 컬럼 매칭)
    age_mapping = {
        '0~9세': '0~9세',
        '2026년04월_거주자_10~19세': '10~19세',
        '2026년04월_거주자_20~29세': '20~29세',
        '2026년04월_거주자_30~39세': '30~39세',
        '2026년04월_거주자_40~49세': '40~49세',
        '2026년04월_거주자_50~59세': '50~59세',
        '2026년04월_거주자_60~69세': '60~69세',
        '2026년04월_거주자_70~79세': '70~79세',
        '2026년04월_거주자_80~89세': '80~89세',
        '2026년04월_거주자_90~99세': '90~99세',
        '100세 이상': '100세 이상'
    }
    
    # 가로축(나이)과 세로축(인구수) 데이터 구성
    age_labels = list(age_mapping.values())
    population_values = [district_data[col] for col in age_mapping.keys()]
    
    # 5. 꺾은선 그래프 시각화 (녹차색 테마 반영)
    st.subheader(f"📈 {selected_district} 연령별 인구수 추이")
    
    # 그래프 크기 및 배경색 설정
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # 배경색을 녹차색(Soft Green) 계열로 지정
    fig.patch.set_facecolor('#ECEEAF')  # 외부 배경색 (부드러운 녹차잎 색)
    ax.set_facecolor('#F3F4ED')        # 그래프 플롯 내부 배경색 (말차 라떼 색)
    
    # 꺾은선 그리기 (녹차색에 어울리는 짙은 올리브 카키색 가로선)
    ax.plot(age_labels, population_values, 
            color='#4F6F52',           # 꺾은선: 깊은 숲/녹차색
            linestyle='-', 
            linewidth=3, 
            marker='o', 
            markersize=8, 
            markerfacecolor='#E8FFCE', # 마커 중심: 연한 새싹색
            markeredgecolor='#4F6F52', # 마커 테두리
            markeredgewidth=2,
            label=f'{selected_district} 인구수')
    
    # 그리드 및 서식 설정
    ax.grid(True, linestyle='--', alpha=0.5, color='#B5CB99')
    ax.set_title(f"{selected_district} 연령대별 인구 분포", fontsize=16, fontweight='bold', color='#3A4D39', pad=15)
    ax.set_xlabel("나이 (연령대)", fontsize=12, fontweight='bold', color='#3A4D39', labelpad=10)
    ax.set_ylabel("인구수 (명)", fontsize=12, fontweight='bold', color='#3A4D39', labelpad=10)
    
    # 축 눈금 스타일 조정
    ax.tick_params(axis='x', colors='#3A4D39', labelsize=11)
    ax.tick_params(axis='y', colors='#3A4D39', labelsize=11)
    
    # 천 단위 콤마 형식으로 세로축 표시
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    
    # 각 데이터 포인트 위에 숫자 라벨 표시
    for i, txt in enumerate(population_values):
        ax.annotate(f"{txt:,}", (age_labels[i], population_values[i]), 
                    textcoords="offset points", 
                    xytext=(0,10), 
                    ha='center', 
                    fontsize=9, 
                    color='#2C3D2E',
                    fontweight='bold')

    st.pyplot(fig)
    
    # 6. 하단 데이터 테이블 노출
    st.subheader("📋 상세 데이터 표")
    df_table = pd.DataFrame([population_values], columns=age_labels, index=[selected_district])
    st.dataframe(df_table, use_container_width=True)

else:
    st.info("💡 분석을 시작하려면 `population.csv` 파일을 업로드해 주세요.")
