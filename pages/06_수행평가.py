import streamlit as st

# 페이지 설정
st.set_page_config(page_title="MBTI 찰떡 플레이스", page_icon="💖", layout="centered")

# 연한 핑크색 감성을 입히기 위한 CSS 스타일링
st.markdown("""
    <style>
    .pink-table {
        width: 100%;
        border-collapse: collapse;
        background-color: #FFF0F5; /* 연한 핑크색 배경 */
        border-radius: 12px;
        overflow: hidden;
        margin-top: 20px;
    }
    .pink-table th {
        background-color: #FFB6C1; /* 헤더는 예쁜 핑크색 */
        color: white;
        padding: 15px;
        font-size: 16px;
        text-align: center;
    }
    .pink-table td {
        padding: 15px;
        border-bottom: 1px solid #FFDAE0;
        text-align: center;
        color: #4B0082;
        font-size: 15px;
        font-weight: 500;
    }
    .main-title {
        color: #FF69B4;
        text-align: center;
        font-family: 'Nanum Gothic', sans-serif;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 제목과 친근한 안내문
st.markdown("<h1 class='main-title'>🌸 MBTI별 드라마 · 음악 · 밥 추천소 🌸</h1>", unsafe_allow_html=True)
st.write("안녕 청춘들! 오늘 뭐 할지, 뭐 먹을지 고민이라면 주목! 🤔 너의 MBTI를 고르면 딱 어울리는 **대한민국 드라마, 명곡, 그리고 드라마 보면서 먹기 좋은 든든한 밥**까지 한 번에 추천해 줄게! ✨")

# MBTI 16가지 완벽 데이터베이스 (실제 존재하는 한국 드라마, 노래, 밥 메뉴)
mbti_db = {
    "ISTJ": {
        "drama": "미생", "drama_review": "현실적이고 치열한 직장 생활 이야기가 네 성실함을 자극할 거야.",
        "music": "이적 - 같이 걸을까", "music_review": "묵묵히 한 걸음씩 나아가는 이들을 위한 최고의 응원가야.",
        "food": "든든한 돼지국밥", "food_review": "정석대로 푹 끓여낸 국밥 한 그릇이 너의 꽉 찬 하루를 위로해 줄 거야."
    },
    "ISFJ": {
        "drama": "응답하라 1988", "drama_review": "가족과 이웃의 따뜻한 정과 추억이 네 다정한 마음을 채워줘.",
        "music": "폴킴 - 모든 날, 모든 순간", "music_review": "언제나 곁을 지켜주겠다는 다정다감한 가사가 딱 어울려.",
        "food": "따뜻한 집밥 제육볶음", "food_review": "정성 가득한 엄마 손맛 제육볶음에 쌈 싸 먹으면 마음까지 따뜻해져."
    },
    "INFJ": {
        "drama": "나의 아저씨", "drama_review": "인간의 깊은 내면과 상처를 치유하는 과정이 네 섬세한 감성을 울릴 거야.",
        "music": "아이유 - 밤편지", "music_review": "서정적이고 잔잔한 멜로디가 네 깊은 생각들을 편안하게 감싸 안아줄걸?",
        "food": "정갈한 버섯솥밥", "food_review": "자극적이지 않고 은은한 향이 나는 솥밥이 네 차분한 분위기와 찰떡이야."
    },
    "INTJ": {
        "drama": "비밀의 숲", "drama_review": "빈틈없는 전개와 치밀한 두뇌 싸움이 네 완벽주의적 분석력을 자극해.",
        "music": "서태지와 아이들 - 발해를 꿈꾸며", "music_review": "사회적 메시지를 담은 웅장한 스케일이 네 깊은 통찰력과 잘 맞아.",
        "food": "깔끔한 일식 초밥", "food_review": "한 입 크기로 완벽하게 계산되어 정갈하게 나오는 초밥이 네 취향일 거야."
    },
    "ISTP": {
        "drama": "모범택시", "drama_review": "말보단 행동! 빌런들을 시원하게 물리치는 액션 카타르시스를 느껴봐.",
        "music": "2NE1 - 내가 제일 잘 나가", "music_review": "남 시선 신경 안 쓰고 마이웨이로 질주하는 쿨함의 끝판왕 곡이야.",
        "food": "화끈한 마라탕", "food_review": "스트레스를 한방에 날려줄 중독성 강한 매운맛이 스릴 넘치는 드라마와 딱이야."
    },
    "ISFP": {
        "drama": "멜로가 체질", "drama_review": "소소한 일상 속 찰진 대사들이 감성적이고 아기자기한 네 마음에 쏙 들 거야.",
        "music": "10cm - 아메리카노", "music_review": "침대에 누워서 뒹굴거리며 듣기 딱 좋은 여유롭고 위트 있는 노래야.",
        "food": "부드러운 카레라이스", "food_review": "만들기 편하고 부담 없이 슥슥 비벼 먹을 수 있는 아늑한 감성의 식사지!"
    },
    "INFP": {
        "drama": "그 해 우리는", "drama_review": "풋풋하고 아련한 청춘 로맨스가 네 몽글몽글한 상상력을 자극할 거야.",
        "music": "잔나비 - 주저하는 연인들을 위해", "music_review": "레트로하면서도 한 편의 시 같은 가사가 네 예술가적 감수성을 폭발시켜.",
        "food": "촉촉한 하이라이스", "food_review": "부드럽고 달콤 쌉싸름한 맛이 드라마 속 첫사랑의 감정과 아주 닮았어."
    },
    "INTP": {
        "drama": "시그널", "drama_review": "무전기로 연결된 과거와 현재, 미스터리 추리가 네 호기심 가득한 뇌를 깨워줘.",
        "music": "악뮤 - DINOSAUR", "music_review": "독특한 상상력과 신선한 사운드가 독창적인 네 스타일과 어울려.",
        "food": "수제 치즈버거 세트", "food_review": "손에 들고 모니터를 응시하며 끊김 없이 먹을 수 있는 가장 효율적인 밥이야."
    },
    "ESTP": {
        "drama": "태양의 후예", "drama_review": "스펙터클한 스케일의 액션과 직진 로맨스가 한순간도 지루할 틈을 안 줄걸?",
        "music": "빅뱅 - 붉은 노을", "music_review": "심장을 뛰게 만드는 강렬한 비트와 폭발적인 에너지가 네 열정과 똑 닮았어.",
        "food": "철판 삼겹살 구이", "food_review": "지글지글 소리부터 침샘을 자극하는 고기 파티가 역동적인 드라마와 찰떡궁합이야."
    },
    "ESFP": {
        "drama": "사내맞선", "drama_review": "클리셰를 맛있게 비튼 유쾌 발랄한 전개 덕분에 보는 내내 웃음이 빵빵 터져!",
        "music": "트와이스 - Cheer Up", "music_review": "인간 비타민인 너에게 딱 맞는, 듣기만 해도 기분이 업되는 상큼한 곡이야.",
        "food": "매콤달콤 즉석떡볶이", "food_review": "다 같이 시끌벅적하게 끓여 먹으며 볶음밥까지 클리어해야 하는 파티용 식사지!"
    },
    "ENFP": {
        "drama": "스물다섯 스물하나", "drama_review": "통통 튀는 청춘들의 에너지와 열정이 네 가슴을 뜨겁고 두근거리게 만들 거야.",
        "music": "볼빨간사춘기 - 여행", "music_review": "어디론가 당장 떠나고 싶게 만드는 청량하고 자유로운 무드가 네 성격이랑 똑같아.",
        "food": "알록달록 수제비빔밥", "food_review": "다양한 재료가 만나 환상의 맛을 내는 비빔밥처럼 다채로운 매력을 가진 너를 위한 밥이야."
    },
    "ENTP": {
        "drama": "빈센조", "drama_review": "악당을 악으로 처단하는 변칙적이고 짜릿한 스토리가 네 흥미를 제대로 저격해.",
        "music": "블락비 - HER", "music_review": "장난기 넘치면서도 천재적인 멜로디 라인이 독특한 네 취향에 딱 맞을 거야.",
        "food": "바삭한 돈가스 김치나베", "food_review": "돈가스와 김치찌개의 이색적인 만남! 고정관념을 깨는 퓨전 요리가 어울려."
    },
    "ESTJ": {
        "drama": "스카이 캐슬", "drama_review": "체계적인 계획과 목표를 향해 치열하게 달려가는 현실감 넘치는 구도에 몰입하게 돼.",
        "music": "보아 - No.1", "music_review": "완벽하고 세련된 무대 매너가 프로페셔널하고 당당한 너의 모습 같아.",
        "food": "깔끔한 소불고기 덮밥", "food_review": "영양 밸런스가 완벽하고, 한 그릇으로 깔끔하게 끝낼 수 있는 효율적인 식사야."
    },
    "ESFJ": {
        "drama": "갯마을 차차차", "drama_review": "마을 사람들과 소통하며 정을 나누는 힐링 스토리가 다정한 네 성격에 온기를 줄 거야.",
        "music": "소녀시대 - 힘 내!", "music_review": "주변 사람들에게 밝고 긍정적인 에너지를 팍팍 전해주는 최고의 응원가야.",
        "food": "따뜻한 바지락칼국수", "food_review": "다 함께 나누어 먹기 좋고 속을 편안하게 풀어주는 정감 가는 밥 메뉴야."
    },
    "ENFJ": {
        "drama": "슬기로운 의사생활", "drama_review": "다정한 의사 친구들의 찐한 우정과 감동 스토리가 네 따뜻한 사회성을 자극해.",
        "music": "방탄소년단 - 봄날", "music_review": "소중한 사람들을 그리워하고 따뜻하게 위로하는 메시지가 깊은 울림을 줘.",
        "food": "부대찌개와 라면사리", "food_review": "햄, 소시지, 야채가 조화롭게 어우러지는 부대찌개처럼 사람들을 화합하는 너에게 딱이야."
    },
    "ENTJ": {
        "drama": "이태원 클라쓰", "drama_review": "소신을 지키며 밑바닥에서부터 정상으로 우뚝 서는 성공 신화가 리더인 너를 자극해.",
        "music": "싸이 - 예술이야", "music_review": "열정적으로 무대를 장악하고 진두지휘하는 거침없는 에너지가 딱 네 스타일이지.",
        "food": "고급스러운 큐브스테이크 덮밥", "food_review": "성공의 맛을 미리 보는 느낌! 든든하고 파워풀한 고기 토핑이 힘을 실어줄 거야."
    }
}

# 드롭다운 선택 메뉴
selected_mbti = st.selectbox("👇 너의 MBTI를 선택해봐!", list(mbti_db.keys()))

st.markdown("<br>", unsafe_allow_html=True)

if selected_mbti:
    res = mbti_db[selected_mbti]
    
    # HTML과 CSS를 활용한 연한 핑크색 커스텀 표 출력
    table_html = f"""
    <table class='pink-table'>
        <tr>
            <th style='width: 20%;'>분류</th>
            <th style='width: 25%;'>추천 아이템</th>
            <th style='width: 55%;'>✨ 한줄평 ✨</th>
        </tr>
        <tr>
            <td>📺 드라마</td>
            <td><b>{res['drama']}</b></td>
            <td>{res['drama_review']}</td>
        </tr>
        <tr>
            <td>🎵 노래</td>
            <td><b>{res['music']}</b></td>
            <td>{res['music_review']}</td>
        </tr>
        <tr>
            <td>🍚 어울리는 밥</td>
            <td><b>{res['food']}</b></td>
            <td>{res['food_review']}</td>
        </tr>
    </table>
    """
    st.markdown(table_html, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.info("실제로 존재하는 대한민국 드라마, 명곡, 그리고 맛있는 밥 메뉴로만 엄선했어! 든든하게 먹으면서 정주행해 봐! 💖")
