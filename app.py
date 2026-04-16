from flask import Flask, render_template, request, jsonify
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import yt_dlp
import os

app = Flask(__name__)

# ভিডিও সেভ করার জন্য ফোল্ডার
UPLOAD_FOLDER = 'static'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    video_url = data.get('url')
    
    try:
        # ভিডিও ডাউনলোডের অপশন
        ydl_opts = {'format': 'best', 'outtmpl': 'static/input.mp4'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        # ভিডিও এডিটিং (লোগো বসানো)
        clip = VideoFileClip("static/input.mp4")
        txt = TextClip("DIGITAL XPRES PRO", fontsize=50, color='white', font='Arial-Bold')
        txt = txt.set_pos(('right', 'top')).set_duration(clip.duration)
        
        final = CompositeVideoClip([clip, txt])
        final.write_videofile("static/output.mp4", codec="libx264")
        
        return jsonify({"status": "success", "message": "এডিটিং সম্পন্ন! এখন আউটপুট রেডি।"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run()
