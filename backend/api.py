from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv
from PIL import Image
import io
import base64
import cv2
import tempfile
import numpy as np

app = Flask(__name__)
CORS(app)

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY") or 'your-openai-api-key'
openai.api_key = openai_api_key

def encode_image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_byte = buffered.getvalue()
    img_base64 = base64.b64encode(img_byte).decode()
    return img_base64

def extract_frames(video_bytes, every_n_frame=30):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmpfile:
        tmpfile.write(video_bytes)
        video_path = tmpfile.name

    video = cv2.VideoCapture(video_path)
    frames = []
    frame_count = 0
    while True:
        success, frame = video.read()
        if not success:
            break
        if frame_count % every_n_frame == 0:
            frames.append(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        frame_count += 1
    return frames

@app.route('/api/upload', methods=['POST'])
def analyze_video():
    file = request.files.get('file')
    if not file or not file.content_type.startswith('video/'):
        return jsonify(error="invalid file type"), 400

    frames = extract_frames(file.read())
    if not frames:
        return jsonify(error="no frames extracted"), 400

    encoded_images = [encode_image_to_base64(frame) for frame in frames]

    system_prompt = "As a dog trainer, you specialize in understanding canine behavior and emotions."
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Don't mention your limitations, just answer the question to the best of your ability right away. \
                 Don't say, 'And in the first image, it looks like...' Just answer as if it's a situation. \
                 Here are several images extracted from a video of a dog. Please analyze them as a continuous sequence, not as separate moments. \
                 Describe the dog's behavior and emotional state throughout these frames, focusing on the changes and progression in its body language, facial expressions, and emotions. \
                 Consider these images as telling a story and provide a cohesive narrative of what you think is happening to the dog over time."}
            ],
        }
    ]

    for encoded_image in encoded_images:
        messages[0]["content"].append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}})

    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=messages,
        max_tokens=200,
    )
    flask_response = make_response(jsonify(result=response.choices[0].message.content))
    flask_response.headers["Access-Control-Allow-Origin"] = "*"
    return flask_response

if __name__ == '__main__':
    app.run(debug=True)
