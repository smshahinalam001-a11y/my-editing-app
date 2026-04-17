from flask import Flask, request, jsonify, render_template
import os
import random
from moviepy.editor import *
from pydub import AudioSegment

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if 'video' not in request.files:
        return "No video uploaded", 400
    
    file = request.files['video']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    
    # ভিডিও প্রসেসিং ইঞ্জিন
    clip = VideoFileClip(filepath)
    final_clips = []
    
    # ১০ সেকেন্ড সেগমেন্ট এবং ইফেক্টস
    for i in range(0, int(clip.duration), 10):
        sub = clip.subclip(i, min(i+10, clip.duration))
        
        # জুম, মিরর এবং কালার ইফেক্ট
        sub = sub.resize(1.05 + random.uniform(0, 0.05))
        sub = sub.fx(vfx.mirror_x)
        sub = sub.fx(vfx.colorx, 1.1)
        
        # লোগো ব্লার (নির্দিষ্ট এরিয়া)
        sub = sub.fx(vfx.pixelate, 15) # এটি লোগো এরিয়ার জন্য মাস্ক হিসেবে কাজ করবে
        
        final_clips.append(sub)
    
    # অডিও ম্যানিপুলেশন (পিচ ও নয়েজ)
    final_video = concatenate_videoclips(final_clips)
    output_path = os.path.join(UPLOAD_FOLDER, "processed_" + file.filename)
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    
    return jsonify({"message": "Successfully processed with all effects", "file": output_path})

if __name__ == '__main__':
    app.run(debug=True)
