import streamlit as st
import openai
import base64
import os
from dotenv import load_dotenv
from PIL import Image
import io
import cv2
import tempfile
import toml

config = toml.load("파일경로/config.toml")
# 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key is None:
    # 환경 변수가 없으면 TOML 파일에서 불러오기
    config = toml.load("파일경로/config.toml")
    openai_api_key = config["openai"]["api_key"]

openai.api_key = openai_api_key

#def encode_image(image):
#    buffer = BytesIO()
#  image.save(buffer, format="JPEG")
#    return base64.b64encode(buffer.getvalue()).decode("utf-8")

def encode_image(image):
  # Create a buffer to hold the image data
    buffered = io.BytesIO()

    # Save the image to the buffer in JPEG format
    image.save(buffered, format="JPEG")

    # Get the byte data from the buffer
    img_byte = buffered.getvalue()

    # Encode the byte data to base64
    img_base64 = base64.b64encode(img_byte).decode()

    return img_base64

def get_first_frame(video_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmpfile:
        tmpfile.write(video_file.read())
        video_path = tmpfile.name

    video = cv2.VideoCapture(video_path)
    success, frame = video.read()
    if success:
        return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    return None

def analyze_image(encoded_image):
    system_prompt = "You are an expert at analyzing images."
    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What’s in this image?"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}"
                        }
                        },
                ],
            },
        ],
        max_tokens=30,
    )
    return response.choices[0].message.content




def main():
    st.set_page_config(page_title="Dog-Themed Image and Video Analysis", page_icon="🐶")
    st.title("🐶 Dog-Themed Image and Video Analysis 🐾")
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
                analysis_result = analyze_image(encoded_image)
                st.write("Analysis Result:")
                st.write(analysis_result)

if __name__ == '__main__':
    main()
