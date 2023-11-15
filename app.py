import streamlit as st
import os
import cv2
import base64
import tempfile
from moviepy.editor import VideoFileClip
from openai import OpenAI
from dotenv import load_dotenv

# 환경 변수 로드

load_dotenv()

def video_to_frames(video_file):
    # 동영상 파일을 임시 파일로 저장
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmpfile:
        tmpfile.write(video_file.read())
        video_filename = tmpfile.name

    # 동영상의 길이 계산
    video_duration = VideoFileClip(video_filename).duration

    # 동영상을 프레임으로 변환
    video = cv2.VideoCapture(video_filename)
    base64Frames = []
    while video.isOpened():
        success, frame = video.read()
        if not success:
            break
        _, buffer = cv2.imencode(".jpg", frame)
        base64Frames.append(base64.b64encode(buffer).decode("utf-8"))

    video.release()
    return base64Frames, video_filename, video_duration

def frames_to_dog_analysis(base64Frames):
    # GPT-4 Vision API를 사용하여 동영상의 프레임을 분석
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    messages = [
        {
            "role": "user",
            "content": [
                "Analyze the dog's behavior in these images and suggest how someone should respond:",
                *map(lambda x: {"type": "image_base64", "image_base64": x}, base64Frames[0::25]),
            ],
        },
    ]

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=messages,
        max_tokens=500,
    )

    return response.choices[0].message.content

def main():
    st.set_page_config(page_title="Dog Behavior Analysis", page_icon="🐶")

    st.header("Dog Behavior Analysis 🐶")
    uploaded_file = st.file_uploader("Upload a video of your dog")

    if uploaded_file is not None:
        st.video(uploaded_file)

        if st.button('Analyze', type="primary"):
            with st.spinner('Analyzing...'):
                base64Frames, video_filename, video_duration = video_to_frames(uploaded_file)
                analysis_result = frames_to_dog_analysis(base64Frames)
                st.write("Analysis:", analysis_result)

                # Clean up the temporary files
                os.unlink(video_filename)

if __name__ == '__main__':
    main()
