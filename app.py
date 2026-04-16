from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# হোম পেজ রেন্ডার করা
@app.route('/')
def index():
    return render_template('index.html')

# ভিডিও প্রসেসিং রাউট
@app.route('/process', methods=['POST'])
def handle_video():
    return jsonify({"status": "success", "message": "প্রসেসিং শুরু হয়েছে"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
