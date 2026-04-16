import os
from flask import Flask, render_template, request, jsonify

# লাইব্রেরি ইনস্টল চেক করার জন্য চেষ্টা
try:
    from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    video_url = data.get('url')
    
    if not MOVIEPY_AVAILABLE:
        return jsonify({"status": "error", "message": "সার্ভারে এডিটিং লাইব্রেরি লোড হয়নি। অনুগ্রহ করে কিছুক্ষণ অপেক্ষা করুন বা সাপোর্ট দেখুন।"})
    
    return jsonify({"status": "success", "message": "এডিটিং ইঞ্জিন সক্রিয়! ভিডিও প্রসেস হচ্ছে..."})

if __name__ == '__main__':
    app.run()
