import streamlit as st
import openai
import base64
import os
from dotenv import load_dotenv
from PIL import Image
import io
import cv2
import tempfile

# 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key is None:
    # 환경 변수가 없으면 Streamlit Secrets에서 불러오기
    config = st.secrets["openai_api_key"]
    openai_api_key = config["openai"]["api_key"]

openai.api_key = openai_api_key

# 이미지를 Base64로 인코딩하는 함수
def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_byte = buffered.getvalue()
    img_base64 = base64.b64encode(img_byte).decode()
    return img_base64

# 비디오 파일에서 첫 프레임을 추출하는 함수
def get_first_frame(video_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmpfile:
        tmpfile.write(video_file.read())
        video_path = tmpfile.name
    video = cv2.VideoCapture(video_path)
    success, frame = video.read()
    if success:
        return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    return None

# 이미지 분석을 수행하는 함수
def analyze_image(encoded_image):
    system_prompt = "You are an expert at analyzing images."
    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What’s in this image?"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}},
                ],
            },
        ],
        max_tokens=30,
    )
    return response.choices[0].message.content

# CSS 스타일 로드하는 함수
def load_css(file_name):
    # 현재 파일의 경로를 기준으로 상대 경로를 구성
    css_path = os.path.join(os.path.dirname(__file__), 'static', 'styles', file_name)
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# 이미지를 로드하는 함수
def load_images():
    base_path = os.path.dirname(__file__)  # 현재 파일의 디렉토리 경로
    st.session_state['images'] = {
        'header': Image.open(os.path.join(base_path, 'static', 'images', 'header.png')),
        'puppy': Image.open(os.path.join(base_path, 'static', 'images', 'puppy.png')),
        'startpuppy': Image.open(os.path.join(base_path, 'static', 'images', 'startpuppy.png')),
        'video': Image.open(os.path.join(base_path, 'static', 'images', 'video.png'))
    }

def set_background_color():
    # HTML/CSS를 사용하여 배경색을 설정합니다.
    background_color_style = """
    <style>
    .stApp {
        background-color: #fafafa;
    }
    </style>
    """
    st.markdown(background_color_style, unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Puppy Pal", page_icon="🐶")
    # 이미지 로드
    set_background_color()
    if 'images' not in st.session_state:
        load_images()
    # 네비게이션 상태 초기화
    if 'page' not in st.session_state:
        st.session_state['page'] = 'home'
    load_css('app.css')
    # 페이지 상태에 따라 CSS 로드
    if st.session_state['page'] == 'home':
        load_css("Home.css")
    elif st.session_state['page'] == 'add_dog':
        load_css("AddDogForm.css")
    elif st.session_state['page'] == 'view_dogs':
        load_css("Info.css")

    # 네비게이션 버튼
    if st.button('Home'):
        st.session_state['page'] = 'home'
    if st.button('강아지 추가'):
        st.session_state['page'] = 'add_dog'
    if st.button('강아지 목록'):
        st.session_state['page'] = 'view_dogs'

    # 페이지 상태에 따라 내용 표시
    if st.session_state['page'] == 'home':
        st.image(st.session_state['images']['header'], use_column_width=True)
        # 홈 페이지 관련 추가 코드...
        uploaded_file = st.file_uploader("Upload an image or video", type=["jpg", "png", "jpeg", "mp4"])
        if uploaded_file is not None:
            file_type = uploaded_file.type.split('/')[0]
            if file_type == 'image':
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image", use_column_width=True)
                encoded_image = encode_image(image)
            elif file_type == 'video':
                st.video(uploaded_file)
                image = get_first_frame(uploaded_file)
                if image:
                    st.image(image, caption="First Frame of Uploaded Video", use_column_width=True)
                    encoded_image = encode_image(image)
                else:
                    st.error("Could not extract the first frame from the video.")
                    return
            if st.button('Analyze'):
                with st.spinner('Analyzing...'):
                    # 이미지 분석 결과 표시 (이 부분은 이미지 분석 로직에 따라 다름)
                    analysis_result = analyze_image(encoded_image)
                    st.write("Analysis Result:")
                    st.write(analysis_result)
    elif st.session_state['page'] == 'add_dog':
        st.image(st.session_state['images']['puppy'], use_column_width=True)
        # 강아지 추가 페이지 관련 추가 코드...
    elif st.session_state['page'] == 'view_dogs':
        st.image(st.session_state['images']['startpuppy'], use_column_width=True)
        # 강아지 목록 페이지 관련 추가 코드...

    # 강아지 추가 페이지
    if st.session_state['page'] == 'add_dog':
        with st.form("add_dog_form"):
            # 폼 필드
            dog_name = st.text_input("Dog's Name")
            dog_age = st.number_input("Dog's Age", min_value=0, max_value=20)
            dog_breed = st.selectbox("Dog's Breed", ['Breed 1', 'Breed 2', 'Breed 3'])
            submit_button = st.form_submit_button("Submit")
            if submit_button:
                # 폼 제출 처리
                st.success(f"{dog_name} has been added to the puppy list!")

    # 강아지 목록 페이지
    if st.session_state['page'] == 'view_dogs':
        # 여기에 강아지 목록을 불러오고 표시하는 코드를 추가
        st.write("List of puppies goes here...")

if __name__ == '__main__':
    main()