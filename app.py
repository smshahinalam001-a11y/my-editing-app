import os
from flask import Flask, request, jsonify
from moviepy.editor import VideoFileClip, vfx
import cv2
import numpy as np

app = Flask(__name__)

# লোগো ব্লার করার ফাংশন
def detect_and_blur_logo(frame):
    h, w, _ = frame.shape
    # ভিডিওর ডান পাশের ওপরের কোণায় ব্লার
    roi = frame[0:150, w-250:w] 
    blurred_roi = cv2.GaussianBlur(roi, (51, 51), 0)
    frame[0:150, w-250:w] = blurred_roi
    return frame

def process_automation(input_path, output_path):
    clip = VideoFileClip(input_path)
    # মিরর ইফেক্ট
    clip = clip.fx(vfx.mirror_x)
    # লোগো ব্লার ইফেক্ট ভিডিওর ওপর এপ্লাই করা
    clip = clip.fl_image(detect_and_blur_logo)
    clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

@app.route('/process', methods=['POST'])
def handle_video():
    return jsonify({"status": "processing", "message": "অটোমেশন ইঞ্জিন এখন লোগো ব্লার এবং মিরর ইফেক্টসহ কাজ করছে"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
