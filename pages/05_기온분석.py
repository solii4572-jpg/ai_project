import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 스트림릿 서버 환경 한글 깨짐 및 에러 방지 기본 설정
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

# 1. 앱 제목 및 설명
st.title("🌡️ 서울 역대 기온 데이터 조회")
st.markdown("1907년부터 2018년까지의 서울 기온 데이터를 조회합니다.")

# 2. 파일 업로더 제공 (인코딩 및 경로 오류 방지용 무적 치트키)
uploaded_file = st.file_uploader("분석할 `seoul.csv` 파일을 업로드해주세요.", type=["csv"])

if uploaded_file is not None:
    # 데이터 로드 기능 (캐싱 제거로 파일 스트림 직접 처리)
    try:
        # 안전한 인코딩 순차 탐색
        df = None
        for enc in ['cp949', 'utf-8', 'euc-kr', 'utf-8-sig']:
            try:
                uploaded_file.seek(0) # 파일 읽기 위치 초기화
                df = pd.read_csv(uploaded_file, encoding=enc)
                if any('날짜' in str(col) for col in df.columns):
                    break
            except:
                continue
        
        if df is None:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, encoding='cp949', errors='ignore')

        # 데이터 공백 정제 및 열 이름 통일
        df.columns = df.columns.str.strip()
        for col in df.columns:
            if "날짜" in str(col):
                df = df.rename(columns={col: "날짜"})
            elif "최저" in str(col):
                df = df.rename(columns={col: "최저기온"})
            elif "최고" in str(col):
                df = df.rename(columns={col: "최고기온"})

        # 날짜 내 탭(\t) 제거 및 변환
        df['날짜'] = df['날짜'].astype(str).str.strip().apply(lambda x: x.replace('\t', ''))
        df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')

        # 기온 데이터 숫자 변환 및 결측치 제거
        df['최저기온'] = pd.to_numeric(df['최저기온'], errors='coerce')
        df['최고기온'] = pd.to_numeric(df['최고기온'], errors='coerce')
        df = df.dropna(subset=['날짜', '최저기온', '최고기온'])

        # 3. 사이드바 날짜 선택 기능
        min_date = df['날짜'].min().to_pydatetime()
        max_date = df['날짜'].max().to_pydatetime()

        st.sidebar.header("🔍 조회 조건 설정")
        date_range = st.sidebar.date_input(
            "조회할 기간을 선택하세요",
            value=(min_date, min_date + pd.Timedelta(days=30)),
            min_value=min_date,
            max_value=max_date
        )

        # 4. 날짜가 제대로 범위로 선택되었을 때만 그래프 시각화
        if len(date_range) == 2:
            start_date, end_date = date_range
            filtered_df = df[(df['날짜'] >= pd.to_datetime(start_date)) & (df['날짜'] <= pd.to_datetime(end_date))]

            if not filtered_df.empty:
                st.subheader(f"📅 기온 시각화 그래프 ({start_date} ~ {end_date})")

                # 그래프 그리기
                fig, ax = plt.subplots(figsize=(10, 5))

                # [요구사항 반영] 최고기온(핫핑크: deeppink), 최저기온(연한 하늘색: lightskyblue) 및 범례 표시
                ax.plot(filtered_df['날짜'], filtered_df['최고기온'], color='deeppink', marker='o', label='Max Temp(C)', linewidth=2)
                ax.plot(filtered_df['날짜'], filtered_df['최저기온'], color='lightskyblue', marker='o', label='Min Temp(C)', linewidth=2)

                # 축 설정
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
                fig.autofmt_xdate()
                ax.set_ylabel("Temperature (C)")
                ax.grid(True, linestyle='--', alpha=0.5)
                
                # 범례 활성화
                ax.legend(loc='upper right')

                # 스트림릿 웹 화면에 출력
                st.pyplot(fig)

                # 데이터 테이블 expander
                with st.expander("📊 선택한 기간 데이터 보기 (Data Table)"):
                    st.dataframe(filtered_df[['날짜', '최저기온', '최고기온']].reset_index(drop=True))
            else:
                st.warning("선택한 기간에 해당하는 데이터가 없습니다.")

    except Exception as e:
        st.error(f"파일 처리 중 오류가 발생했습니다: {e}")
else:
    st.info("💡 왼쪽 또는 화면 중앙의 업로드 창을 통해 `seoul.csv` 파일을 올려주시면 기온 분석이 시작됩니다.")
