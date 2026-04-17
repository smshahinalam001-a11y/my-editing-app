from flask import Flask, request, jsonify, render_template
import os
from moviepy.editor import *
import random

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    file = request.files['video']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    
    # ভিডিও প্রসেসিং
    clip = VideoFileClip(filepath)
    
    # ১০ সেকেন্ডে কাটা এবং ইফেক্ট যোগ করা
    clips = []
    for i in range(0, int(clip.duration), 10):
        subclip = clip.subclip(i, min(i+10, clip.duration))
        # ইফেক্ট: জুম, মিরর এবং কালার ফিল্টার
        subclip = subclip.resize(1.05 + random.uniform(-0.02, 0.02))
        subclip = subclip.fx(vfx.mirror_x)
        subclip = subclip.fx(vfx.colorx, 1.1)
        clips.append(subclip)
    
    final = concatenate_videoclips(clips)
    output = "final_output.mp4"
    final.write_videofile(output, codec="libx264", audio_codec="aac")
    
    return jsonify({"message": "Processed successfully"})

if __name__ == '__main__':
    app.run(debug=True)
