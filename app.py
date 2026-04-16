import os
# Numpy ভার্সন সমস্যা এড়াতে এটি আগে ইমপোর্ট করুন
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

from flask import Flask, render_template, request, jsonify
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    video_url = data.get('url')
    return jsonify({"status": "success", "message": "ইঞ্জিন রেডি! ভিডিও প্রসেসিং শুরু হচ্ছে..."})

if __name__ == '__main__':
    app.run()
