import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

st.title("🌡️ 서울 역대 기온 데이터 조회")
st.markdown("1907년부터 2018년까지의 서울 기온 데이터를 조회합니다.")

@st.cache_data
def load_data():
    # 여러 인코딩을 순차적으로 시도하여 안전하게 로드
    for enc in ['cp949', 'utf-8', 'euc-kr', 'utf-8-sig']:
        try:
            df = pd.read_csv("seoul.csv", encoding=enc)
            if any('날짜' in str(col) for col in df.columns):
                break
        except:
            continue

    # 열 이름 정제 (앞뒤 공백 제거)
    df.columns = df.columns.str.strip()
    
    # 깨진 열 이름이 있을 경우를 대비해 수동 매핑
    for col in df.columns:
        if "날짜" in str(col):
            df = df.rename(columns={col: "날짜"})
        elif "최저" in str(col):
            df = df.rename(columns={col: "최저기온"})
        elif "최고" in str(col):
            df = df.rename(columns={col: "최고기온"})
            
    # 데이터 정제 (주석이나 정규식 에러 방지를 위해 간단한 함수 사용)
    df['날짜'] = df['날짜'].astype(str).str.strip()
    df['날짜'] = df['날짜'].apply(lambda x: x.replace('\t', ''))
    df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
    
    df['최저기온'] = pd.to_numeric(df['최저기온'], errors='coerce')
    df['최고기온'] = pd.to_numeric(df['최고기온'], errors='coerce')
    df = df.dropna(subset=['날짜', '최저기온', '최고기온'])
    
    return df

try:
    df = load_data()

    min_date = df['날짜'].min().to_pydatetime()
    max_date = df['날짜'].max().to_pydatetime()

    st.sidebar.header("🔍 조회 조건 설정")
    date_range = st.sidebar.date_input(
        "조회할 기간을 선택하세요",
        value=(min_date, min_date + pd.Timedelta(days=30)),
        min_value=min_date,
        max_value=max_date
    )

    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = df[(df['날짜'] >= pd.to_datetime(start_date)) & (df['날짜'] <= pd.to_datetime(end_date))]
        
        if not filtered_df.empty:
            st.subheader(f"📅 기온 시각화 그래프")
            
            fig, ax = plt.subplots(figsize=(10, 5))
            
            # 요구사항: 최고기온(핫핑크), 최저기온(연한 하늘색), 범례 표시
            ax.plot(filtered_df['날짜'], filtered_df['최고기온'], color='deeppink', marker='o', label='Max Temp (C)', linewidth=2)
            ax.plot(filtered_df['날짜'], filtered_df['최저기온'], color='lightskyblue', marker='o', label='Min Temp (C)', linewidth=2)
            
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            fig.autofmt_xdate()
            
            ax.set_ylabel("Temperature (C)")
            ax.grid(True, linestyle='--', alpha=0.5)
            ax.legend(loc='upper right')
            
            st.pyplot(fig)
            
            with st.expander("📊 데이터 테이블 보기"):
                st.dataframe(filtered_df[['날짜', '최저기온', '최고기온']].reset_index(drop=True))
        else:
            st.warning("선택한 기간에 해당하는 데이터가 없습니다.")

except FileNotFoundError:
    st.error("💡 `seoul.csv` 파일을 찾을 수 없습니다. 파일이 스크립트와 동일한 저장소 위치에 있는지 확인해 주세요.")
except Exception as e:
    st.error(f"오류 발생: {e}")
