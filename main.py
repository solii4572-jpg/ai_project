import streamlit as st 
st.title( ' 나의 첫 웹 서비스 만들기')
a=st.text_input('이름을 입력하세요')
b=st.selectbox('좋아하는 음식을 선택하세요',['치킨','마라탕','떡볶이'])
if st.button('인삿말 생성'):
  st.write(a+'님, 안녕하세요')
  st.info('반갑습니다')
  st.warning(b+'음식을 좋아하시나봐요!')
  sterror('잘 부탁합니다')
