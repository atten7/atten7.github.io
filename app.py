from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html', show_apikey_input=False)

@app.route('/upload', methods=['POST'])
def upload():
    if 'pptx_file' not in request.files:
        return 'No file part'
    file = request.files['pptx_file']
    if file.filename == '':
        return 'No selected file'
    if file and file.filename.endswith('.pptx'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return render_template('index.html', show_apikey_input=True)
    return 'pptx 파일만 업로드 가능합니다.'

app.secret_key = 'your_secret_key'

@app.route('/set_apikey', methods=['POST'])
def set_apikey():
    apikey = request.form.get('apikey')
    session['gemini_apikey'] = apikey
    return render_template('index.html', show_apikey_input=False, apikey_saved=True, apikey=apikey)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)