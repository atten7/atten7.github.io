from flask import Flask, render_template, request, redirect, url_for
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from main import main

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'pptx_file' not in request.files:
        return '파일이 포함되지 않았습니다.'
    file = request.files['pptx_file']
    if file.filename == '':
        return '파일이 선택되지 않았습니다.'
    if file and file.filename.endswith('.pptx'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        main(filepath)
        
        return render_template('index.html', message="업로드 완료!")
    return 'pptx 파일만 업로드 가능합니다.'


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)








