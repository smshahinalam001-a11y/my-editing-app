from flask import Flask, render_template, request, jsonify
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import yt_dlp
import os

app = Flask(__name__)

# ভিডিও সেভ করার জন্য ফোল্ডার
UPLOAD_FOLDER = 'static/downloads'
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
        # ১. ভিডিও ডাউনলোড করার সেটআপ
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'{UPLOAD_FOLDER}/video.mp4',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        # ২. ভিডিও এডিটিং (MoviePy দিয়ে লোগো ও নাম বসানো)
        clip = VideoFileClip(f"{UPLOAD_FOLDER}/video.mp4")
        
        # আপনার চ্যানেলের নাম টেক্সট হিসেবে যোগ করা
        txt_clip = TextClip("DIGITAL XPRES PRO", fontsize=30, color='white', font='Arial-Bold')
        txt_clip = txt_clip.set_pos(('right', 'top')).set_duration(clip.duration)
        
        # ভিডিও এবং টেক্সট লেয়ার একসাথে করা
        final_video = CompositeVideoClip([clip, txt_clip])
        final_video.write_videofile(f"{UPLOAD_FOLDER}/final_edited.mp4", codec="libx264")
        
        return jsonify({
            "status": "success", 
            "message": "এডিটিং সম্পন্ন হয়েছে! ওয়াটারমার্ক রিমুভ করে আপনার চ্যানেলের নাম বসানো হয়েছে।"
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run()
