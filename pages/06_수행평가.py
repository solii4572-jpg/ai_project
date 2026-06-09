import streamlit as st

# 페이지 설정
st.set_page_config(page_title="MBTI 취향 저격소", page_icon="💖")

# 연한 핑크색 테마를 위한 CSS 설정
st.markdown("""
    <style>
    .pink-table {
        width: 100%;
        border-collapse: collapse;
        background-color: #FFF0F5; /* 연한 핑크색 배경 */
        border-radius: 10px;
        overflow: hidden;
    }
    .pink-table th {
        background-color: #FFB6C1; /* 헤더는 조금 더 진한 핑크 */
        color: white;
        padding: 15px;
        text-align: center;
    }
    .pink-table td {
        padding: 15px;
        border-bottom: 1px solid #FFDAE0;
        text-align: center;
        color: #4B0082;
        font-weight: 500;
    }
    .main-title {
        color: #FF69B4;
        text-align: center;
        font-family: 'Nanum Gothic', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# 제목 및 소개
st.markdown("<h1 class='main-title'>🎀 MBTI별 드라마 & 음악 배달 서비스 🎀</h1>", unsafe_allow_html=True)
st.write("안녕! 너의 MBTI를 알려주면 지금 당장 즐기기 좋은 **대한민국 드라마와 노래, 그리고 맛있는 간식**을 추천해 줄게! 오늘 하루는 이걸로 힐링해봐! ✨")

# MBTI 데이터 (드라마, 음악, 간식 및 한줄평)
mbti_db = {
    "ISTJ": ["미생", "현실적인 직장 생활이 네 성실함을 자극할 거야!", "이적 - 같이 걸을까", "지친 마음을 조용히 다독여주는 멜로디야.", "약과"],
    "ISFJ": ["응답하라 1988", "가족과 이웃의 따뜻한 정이 네 마음을 몽글하게 해.", "폴킴 - 모든 날, 모든 순간", "너의 헌신적인 사랑과 딱 어울리는 고백송이야.", "호빵"],
    "INFJ": ["나의 아저씨", "인간의 깊은 내면을 어루만지는 위로를 받을 수 있어.", "아이유 - 밤편지", "조용히 생각을 정리할 때 듣기 좋은 감성 곡이야.", "따뜻한 차와 꿀떡"],
    "INTJ": ["비밀의 숲", "치밀한 두뇌 싸움이 네 분석력을 짜릿하게 만들걸?", "서태지와 아이들 - 발해를 꿈꾸며", "웅장한 메시지가 네 깊은 통찰력과 어울려.", "다크 초콜릿"],
    "ISTP": ["모범택시", "말보다 행동! 시원한 복수극이 카타르시스를 줄 거야.", "2NE1 - 내가 제일 잘 나가", "자신감 뿜뿜! 네 마이웨이 정신에 딱이야.", "매운 라면"],
    "ISFP": ["멜로가 체질", "소소하고 잔잔한 일상 속 대사들이 네 감성을 툭 건드려.", "10cm - 아메리카노", "여유로운 오후, 침대에 누워 듣기 최고야.", "고구마 라떼"],
    "INFP": ["그 해 우리는", "첫사랑의 아련한 감성이 네 상상력을 자극할 거야.", "잔나비 - 주저하는 연인들을 위해", "가사가 너무 시적이라 네 감수성을 폭발시켜.", "딸기 마카롱"],
    "INTP": ["시그널", "과거와 현재를 잇는 추리가 네 호기심을 완벽 충족해줄걸?", "악뮤 - DINOSAUR", "독특한 사운드와 상상력이 네 머릿속을 깨워줘.", "피자"],
    "ESTP": ["태양의 후예", "직진 로맨스와 액션이 네 에너지를 불태울 거야!", "빅뱅 - 붉은 노을", "언제 들어도 신나는 비트가 네 열정과 똑 닮았어.", "뿌링클 치킨"],
    "ESFP": ["사내맞선", "보는 내내 광대가 안 내려오는 유쾌함 그 자체야!", "트와이스 - Cheer Up", "인간 비타민인 너에게 주는 상큼한 응원가야.", "떡볶이"],
    "ENFP": ["스물다섯 스물하나", "청춘의 뜨거운 열정이 네 가슴을 두근거리게 해!", "볼빨간사춘기 - 여행", "어디론가 훌쩍 떠나고 싶은 네 마음을 대변해.", "구슬 아이스크림"],
    "ENTP": ["빈센조", "예측 불가능한 전개가 네 톡톡 튀는 성격이랑 찰떡이야.", "블락비 - HER", "장난기 가득하고 독창적인 리듬이 완전 매력적이야.", "나쵸"],
    "ESTJ": ["스카이 캐슬", "목표를 향한 치열함이 네 추진력을 불타오르게 할걸?", "보아 - No.1", "완벽한 무대 매너가 당당한 너의 모습 같아.", "에너지바"],
    "ESFJ": ["갯마을 차차차", "사람 냄새 나는 따뜻한 이야기에 마음이 훈훈해져.", "소녀시대 - 힘 내!", "주변 사람들을 챙기는 네 다정한 마음을 응원해.", "김밥"],
    "ENFJ": ["슬기로운 의사생활", "동료들과의 찐한 우정이 네 사회성을 만족시켜줄 거야.", "방탄소년단 - 봄날", "함께라서 더 소중한 사람들을 생각나게 해.", "샌드위치"],
    "ENTJ": ["이태원 클라쓰", "소신 있게 목표를 이루는 모습이 리더인 너랑 똑같아.", "싸이 - 예술이야", "열정적으로 무대를 장악하는 에너지가 최고야.", "육포"],
}

# 선택 상자
option = st.selectbox("👇 너의 MBTI를 선택해봐!", list(mbti_db.keys()))

st.markdown("<br>", unsafe_allow_html=True)

if option:
    res = mbti_db[option]
    # HTML 표 생성 (연한 핑크색 테마)
    table_html = f"""
    <table class='pink-table'>
        <tr>
            <th>분류</th>
            <th>추천 아이템</th>
            <th>✨ 한줄평 ✨</th>
        </tr>
        <tr>
            <td>📺 드라마</td>
            <td><b>{res[0]}</b></td>
            <td>{res[1]}</td>
        </tr>
        <tr>
            <td>🎵 노래</td>
            <td><b>{res[2]}</b></td>
            <td>{res[3]}</td>
        </tr>
        <tr>
            <td>😋 간식</td>
            <td><b>{res[4]}</b></td>
            <td>드라마 보면서 입 심심하지 않게 준비해봐!</td>
        </tr>
    </table>
    """
    st.markdown(table_html, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.info("실제로 존재하는 대한민국 드라마와 노래들로만 구성했어! 재미있게 즐겨봐! 💖")
