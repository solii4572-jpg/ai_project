import streamlit as st
import folium
from streamlit_folium import st_folium

# 1. 페이지 설정
st.set_page_config(
    page_title="서울 외국인 인기 관광지 TOP 10",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ 외국인이 좋아하는 서울 주요 관광지 TOP 10")
st.markdown("지도의 **노란색 마커에 마우스를 올리면(Hover)** 가장 가까운 지하철역을 확인할 수 있습니다.")

# 2. 서울 관광지 데이터 정의 (이름, 위도, 경도, 가까운 지하철역, 놀거리)
tourist_spots = [
    {
        "name": "경복궁", "lat": 37.5796, "lng": 126.9770, "station": "경복궁역 (3호선)",
        "desc": "한복을 대여해 입고 고궁을 거닐며 한국 전통 예절과 건축의 미를 체험하고 사진을 남기기 좋습니다."
    },
    {
        "name": "명동 쇼핑 거리", "lat": 37.5634, "lng": 126.9846, "station": "명동역 (4호선)",
        "desc": "K-뷰티 화장품 쇼핑의 중심지이며, 저녁이 되면 길거리 음식(길거리 떡볶이, 회오리감자 등) 투어를 즐길 수 있습니다."
    },
    {
        "name": "홍대거리", "lat": 37.5568, "lng": 126.9238, "station": "홍대입구역 (2호선, 공항철도)",
        "desc": "젊은이들의 버스킹 공연을 관람하고, 트렌디한 인생네컷 사진관, 이색 테마 카페 및 패션 로드샵을 탐방합니다."
    },
    {
        "name": "N서울타워", "lat": 37.5512, "lng": 126.9882, "station": "명동역 (4호선) -> 케이블카 탑승",
        "desc": "남산 케이블카를 타고 올라가 서울 시내 전경을 한눈에 감상하고, 유명한 사랑의 자물쇠 존에서 추억을 남깁니다."
    },
    {
        "name": "북촌 한옥마을", "lat": 37.5829, "lng": 126.9835, "station": "안국역 (3호선)",
        "desc": "실제 주민들이 거주하는 전통 한옥 골목길을 조용히 산책하며 옛 서울의 정취를 느끼고 전통 찻집을 경험합니다."
    },
    {
        "name": "인사동 문화의거리", "lat": 37.5744, "lng": 126.9856, "station": "안국역 (3호선) 또는 종각역 (1호선)",
        "desc": "쌈지길 복합문화공간에서 한국 전통 공예품과 기념품을 쇼핑하고, 전통 붓글씨나 한지 공예 체험을 즐깁니다."
    },
    {
        "name": "동대문 디자인 플라자 (DDP)", "lat": 37.5665, "lng": 127.0092, "station": "동대문역사문화공원역 (2, 4, 5호선)",
        "desc": "자하 하디드가 설계한 우주선 모양의 전위적인 건축물을 관람하고, 밤에는 디지털 미디어 아트와 야경을 감상합니다."
    },
    {
        "name": "강남역 & 별마당 도서관", "lat": 37.5118, "lng": 127.0592, "station": "삼성역 (2호선) 또는 봉은사역 (9호선)",
        "desc": "코엑스몰 내부에 위치한 거대한 별마당 도서관 서가를 배경으로 인증샷을 찍고, 대형 쇼핑몰 내부를 탐험합니다."
    },
    {
        "name": "이태원 관광특구", "lat": 37.5345, "lng": 126.9942, "station": "이태원역 (6호선)",
        "desc": "세계 각국의 다양한 미식을 맛볼 수 있는 레스토랑 가를 방문하고, 이색적인 수입 구제 옷과 소품 쇼핑을 즐깁니다."
    },
    {
        "name": "광장시장", "lat": 37.5701, "lng": 126.9997, "station": "종로5가역 (1호선) 또는 을지로4가역 (2, 5호선)",
        "desc": "외국인 필수 코스인 빈대떡, 마약김밥, 육회, 떡볶이를 활기찬 전통시장 노판에 앉아 라이브로 맛보는 재미가 있습니다."
    }
]

# 3. 폴리움 지도 생성 (서울 중심부 위치)
m = folium.Map(location=[37.555, 126.985], zoom_start=12)

# 4. 지도 위에 마커 추가 (조건: 노란색 마커, 마우스 오버 시 지하철역 표시)
for spot in tourist_spots:
    folium.Marker(
        location=[spot["lat"], spot["lng"]],
        popup=folium.Popup(f"<b>{spot['name']}</b>", max_width=200),
        tooltip=f"🚉 가장 가까운 역: {spot['station']}",  # 마우스 호버(Hover) 시 작동
        icon=folium.Icon(color="darkblue", icon_color="yellow", icon="info-sign")  # 바깥은 네이비, 아이콘 및 내부 포인트는 노란색
    ).add_to(m)

# 5. 스트림릿 화면에 지도 렌더링
st_folium(m, width="100%", height=500)

st.markdown("---")

# 6. 지도 밑 하단 상세 설명 레이아웃
st.subheader("📋 관광지 10곳 상세 가이드 (지하철 및 놀거리)")

# 2열(Column) 구조로 깔끔하게 배치
col1, col2 = st.columns(2)

for idx, spot in enumerate(tourist_spots):
    # 1~5번은 첫 번째 열, 6~10번은 두 번째 열에 나누어 배치
    with col1 if idx < 5 else col2:
        with st.container(border=True):
            st.markdown(f"### {idx+1}. {spot['name']}")
            st.caption(f"🚉 **가까운 지하철역:** {spot['station']}")
            st.markdown(f"✨ **추천 놀거리:** {spot['desc']}")
