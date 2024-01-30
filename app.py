from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = '6399781777:AAHQl6dNdsUKCeJYPqvCbDdhS6pp-qMDuj0'
TELEGRAM_CHAT_ID = '5810389985'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    file_url = upload_file_to_telegram(file)
    return render_template('result.html', file_url=file_url)

def upload_file_to_telegram(file):
    bot_token = TELEGRAM_BOT_TOKEN
    chat_id = TELEGRAM_CHAT_ID
    url = f'https://api.telegram.org/bot{bot_token}/sendPhoto'
    files = {'photo': (file.filename, file.stream, file.mimetype)}
    data = {'chat_id': chat_id}
    response = requests.post(url, files=files, data=data)
    file_id = response.json().get('result', {}).get('photo', [])[0].get('file_id')
    file_url = f'https://t.me/{bot_token}/{file_id}'
    return file_url

if __name__ == '__main__':
    app.run(debug=True)
