from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    video_url = data.get('url')
    # ভিডিও প্রসেসিং লজিক এখানে যুক্ত হবে
    return jsonify({"status": "success", "message": f"ভিডিও প্রসেসিং শুরু হয়েছে: {video_url}"})

if __name__ == '__main__':
    app.run()
