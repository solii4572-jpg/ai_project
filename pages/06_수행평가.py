import streamlit as st

# 페이지 설정
st.set_page_config(page_title="MBTI별 드라마&음악 추천", page_icon="🎬", layout="centered")

# 제목 및 소개
st.title("✨ MBTI별 찰떡 드라마 & 음악 추천소 ✨")
st.write("너의 MBTI를 선택해 봐! 네 성향에 딱 맞는 대한민국 드라마와 명곡을 추천해 줄게 😎")

# MBTI 16가지 데이터 정의 (실제 존재하는 한국 드라마 & 음악)
mbti_data = {
    "INTJ": {
        "drama": "비밀의 숲", "drama_review": "치밀한 두뇌 싸움과 설계가 너의 완벽주의적 성향을 저격할 거야!",
        "music": "서태지와 아이들 - 발해를 꿈꾸며", "music_review": "웅장한 스케일과 사회적인 메시지가 깊은 생각을 자극해."
    },
    "INTP": {
        "drama": "시그널", "drama_review": "무전기로 연결된 과거와 현재, 미스터리를 추리하는 재미에 밤새울걸?",
        "music": "악뮤(AKMU) - DINOSAUR", "music_review": "독특한 상상력과 신선한 멜로디가 네 호기심 가득한 뇌를 깨워줄 거야."
    },
    "ENTJ": {
        "drama": "이태원 클라쓰", "drama_review": "밑바닥에서부터 목표를 향해 거침없이 질주하는 야망이 딱 네 스타일이야.",
        "music": "싸이(PSY) - 예술이야", "music_review": "열정적이고 당당하게 무대를 장악하는 에너지가 리더인 너와 어울려."
    },
    "ENTP": {
        "drama": "빈센조", "drama_review": "악당을 악으로 처단하는 짜릿하고 변칙적인 스토리가 네 흥미를 유발할걸?",
        "music": "블락비(Block B) - HER", "music_review": "톡톡 튀고 장난기 넘치면서도 천재적인 리듬감이 완전 매력적이야."
    },
    "INFJ": {
        "drama": "나의 아저씨", "drama_review": "인간의 깊은 내면과 따뜻한 위로를 담아 네 섬세한 감성을 울릴 드라마야.",
        "music": "아이유(IU) - 밤편지", "music_review": "잔잔하면서도 깊은 울림을 주는 가사가 네 마음을 편안하게 감싸줄 거야."
    },
    "INFP": {
        "drama": "그 해 우리는", "drama_review": "풋풋하고 아련한 청춘의 감성이 네 몽글몽글한 상상력을 자극해.",
        "music": "잔나비 - 주저하는 연인들을 위해", "music_review": "레트로하면서도 시적인 가사가 네 감수성을 폭발하게 만들 거야."
    },
    "ENFJ": {
        "drama": "슬기로운 의사생활", "drama_review": "따뜻한 동료애와 주변 사람들을 챙기는 다정한 모습이 딱 네 이야기야.",
        "music": "방탄소년단(BTS) - 봄날", "music_review": "함께하는 이들을 그리워하고 위로하는 따뜻한 메시지가 마음에 와닿을 거야."
    },
    "ENFP": {
        "drama": "스물다섯 스물하나", "drama_review": "통통 튀는 청춘들의 에너지와 열정이 네 가슴을 두근거리게 만들 거야!",
        "music": "볼빨간사춘기 - 여행", "music_review": "어디론가 훌쩍 떠나고 싶게 만드는 밝고 청량한 에너지가 너랑 똑 닮았어."
    },
    "ISTJ": {
        "drama": "미생", "drama_review": "현실적인 직장 생활과 원칙을 지키며 성장하는 모습에 깊은 공감을 느낄 거야.",
        "music": "이적 - 같이 걸을까", "music_review": "묵묵하고 성실하게 한 걸음씩 나아가는 이들을 위한 최고의 응원가야."
    },
    "ISFJ": {
        "drama": "응답하라 1988", "drama_review": "가족과 이웃 간의 따뜻한 정과 소소한 일상이 네 다정한 마음을 채워줄 거야.",
        "music": "폴킴 - 모든 날, 모든 순간", "music_review": "늘 곁에서 묵묵히 지켜주겠다는 가사가 네 헌신적인 성격과 딱 맞아."
    },
    "ESTJ": {
        "drama": "스카이 캐슬", "drama_review": "체계적인 계획과 목표를 향해 치열하게 달려가는 현실에 몰입하게 될 거야.",
        "music": "보아(BoA) - No.1", "music_review": "완벽한 무대와 프로페셔널한 에너지가 당당한 너의 모습 같아."
    },
    "ESFJ": {
        "drama": "갯마을 차차차", "drama_review": "마을 사람들과 소통하며 정을 나누는 힐링 스토리가 네 따뜻한 오지랖을 자극해.",
        "music": "소녀시대 - 힘 내!", "music_review": "주변 사람들에게 긍정적인 에너지를 팍팍 전해주는 신나는 응원곡이야."
    },
    "ISTP": {
        "drama": "모범택시", "drama_review": "말보단 행동으로! 깔끔하고 시원하게 사건을 해결하는 액션 카타르시스를 느껴봐.",
        "music": "투애니원(2NE1) - 내가 제일 잘 나가", "music_review": "남의 시선 신경 안 쓰고 마이웨이로 질주하는 쿨함의 정석 같은 곡이야."
    },
    "ISFP": {
        "drama": "멜로가 체질", "drama_review": "소소하고 잔잔한 일상 속 찰진 대사들이 네 감성적인 영혼을 툭 건드릴 거야.",
        "music": "10cm - 아메리카노", "music_review": "편안하게 누워서 들을 수 있는 여유롭고 위트 있는 분위기가 딱이야."
    },
    "ESTP": {
        "drama": "태양의 후예", "drama_review": "스펙터클한 액션과 직진하는 로맨스가 한순간도 지루할 틈을 안 줄 거야.",
        "music": "빅뱅(BIGBANG) - 붉은 노을", "music_review": "심장을 뛰게 만드는 신나는 비트와 폭발하는 에너지가 네 열정과 어울려."
    },
    "ESFP": {
        "drama": "사내맞선", "drama_review": "유쾌하고 유머러스한 전개 덕분에 보는 내내 웃음이 멈추지 않을 거야!",
        "music": "트와이스(TWICE) - Cheer Up", "music_review": "듣기만 해도 기분이 업되고 축제 분위기를 만들어주는 인간 비타민 같은 곡이야."
    }
}

# 드롭다운 선택 상자
selected_mbti = st.selectbox("👇 너의 MBTI를 골라봐!", list(mbti_data.keys()))

st.markdown("---")

# 결과 출력
if selected_mbti:
    st.subheader(f"🎉 {selected_mbti} 유형을 위한 추천 결과!")
    
    data = mbti_data[selected_mbti]
    
    # 표 데이터 구성
    table_data = {
        "분류": ["📺 드라마", "🎵 음악"],
        "추천 작품": [data["drama"], data["music"]],
        "이유 (한줄평)": [data["drama_review"], data["music_review"]]
    }
    
    # 스트림릿 표(Table)로 깔끔하게 출력
    st.table(table_data)
