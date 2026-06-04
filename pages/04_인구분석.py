import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. 페이지 초기 설정
st.set_page_config(page_title="서울시 인구 분석", layout="wide")

# 2. 파이썬 3.14 호환용 안전한 폰트 기본 설정 (오류 방어)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

# 3. 타이틀 표시
st.title("🍵 서울시 행정구별 연령대 인구수 분석")
st.write("상위 루트 폴더에 위치한 인구 데이터 파일을 자동으로 읽어와 분석합니다.")

# 4. 파일 경로 설정 (스트림릿 클라우드 실행 기준 최상위 경로)
csv_path = "population.csv"

# 여러 인코딩 방식으로 파일 읽기 시도
df = None
for enc in ['utf-8', 'cp949', 'euc-kr', 'utf-8-sig']:
    try:
        df = pd.read_csv(csv_path, encoding=enc)
        break
    except Exception:
        continue

# 파일 로드 실패 시 예외 처리 및 안내
if df is None:
    st.error("❌ 최상위 폴더에서 population.csv 파일을 찾을 수 없거나 읽는데 실패했습니다. 파일 이름과 위치를 확인해 주세요.")
    st.stop()

try:
    # 5. 데이터 값 정제 (콤마 제거 후 정수형 변환)
    for col in df.columns[1:]:
        df[col] = df[col].astype(str).str.replace(',', '', regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
        
    # '서울특별시' 전체 행을 제외한 자치구 데이터만 필터링
    df_districts = df[df['행정구역'].str.contains('전체') == False].copy()
    
    # 행정구역 컬럼에서 구 이름만 깔끔하게 분리 추출
    df_districts['구이름'] = df_districts['행정구역'].apply(lambda x: str(x).split()[1] if len(str(x).split()) > 1 else str(x))
    
    # 6. 사이드바 자치구 선택 기능
    st.sidebar.header("🌿 필터 설정")
    selected_district = st.sidebar.selectbox("행정구를 선택하세요", df_districts['구이름'].unique())
    
    # 선택된 구 데이터 1행 추출
    district_data = df_districts[df_districts['구이름'] == selected_district].iloc[0]
    
    # 7. CSV 원본 컬럼명과 가로축 매핑
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
            
    # 8. 녹차색 대시보드 꺾은선 그래프 구현
    st.subheader(f"📈 {selected_district} 연령별 인구수 추이")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('#ECEEAF')  # 외부 배경색 (연녹차색)
    ax.set_facecolor('#F3F4ED')        # 플롯 내부 배경색 (말차라떼색)
    
    # 꺾은선 그리기 스타일링 (녹차색 조합)
    ax.plot(x_data, y_data, color='#4F6F52', linestyle='-', linewidth=3, marker='o', markersize=8, markerfacecolor='#E8FFCE', markeredgecolor='#4F6F52')
    
    ax.grid(True, linestyle='--', alpha=0.5, color='#B5CB99')
    ax.set_title(f"{selected_district} Population Distribution", fontsize=14, fontweight='bold', color='#3A4D39')
    
    # 세로축 숫자 천단위 컴마 포맷 적용
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    
    # 그래프 포인트 상단에 인구수 텍스트 표기
    for i, val in enumerate(y_data):
        ax.text(i, val, "{:,}".format(val), color='#2C3D2E', fontsize=9, fontweight='bold', ha='center', va='bottom')
        
    st.pyplot(fig)
    
    # 9. 하단에 가로형 데이터 테이블 출력
    st.subheader("📋 상세 데이터 표")
    st.dataframe(pd.DataFrame([y_data], columns=x_data, index=[selected_district]), use_container_width=True)
    
except Exception as e:
    st.error(f"데이터를 처리하는 도중 문제가 발생했습니다: {e}")
