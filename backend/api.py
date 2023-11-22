from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv
from PIL import Image
import io
import base64
import cv2
import tempfile

app = Flask(__name__)
CORS(app)  # CORS를 활성화하여 React 앱에서 요청을 허용합니다.

# 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
openai_api_key = os.getenv("OPENAI_API_KEY") or 'your-openai-api-key'
openai.api_key = openai_api_key

def encode_image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_byte = buffered.getvalue()
    img_base64 = base64.b64encode(img_byte).decode()
    return img_base64

def get_first_frame(video_bytes):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmpfile:
        tmpfile.write(video_bytes)
        video_path = tmpfile.name

    video = cv2.VideoCapture(video_path)
    success, frame = video.read()
    if success:
        return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    return None

@app.route('/api/upload_video', methods=['POST'])
def analyze_image():
    if 'file' not in request.files:
        return jsonify(error="missing file"), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify(error="no file selected"), 400

    if file and file.content_type.startswith('image/'):
        image = Image.open(file.stream)
        encoded_image = encode_image_to_base64(image)
    elif file and file.content_type.startswith('video/'):
        image = get_first_frame(file.read())
        if image is None:
            return jsonify(error="could not extract the first frame from the video"), 400
        encoded_image = encode_image_to_base64(image)
    else:
        return jsonify(error="invalid file type"), 400

    system_prompt = "You are an expert at analyzing images."
    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What’s in this image?"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
                ],
            },
        ],
        max_tokens=30,
    )
    return jsonify(result=response.choices[0].message.content)

if __name__ == '__main__':
    app.run(debug=True)
