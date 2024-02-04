from flask import Flask, render_template, request, jsonify
from pyrogram import Client
import os

app = Flask(__name__, template_folder="template")

api_id = 14688437
api_hash = "5310285db722d1dceb128b88772d53a6"
bot_token = "6162291374:AAGieKLuy_e7Id8G2pQaXRiNsuiviWgalDE"

bot = Client("santhu", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/get_channel_content', methods=['POST'])
def get_channel_content():
    link = request.json.get('channelUsername')
    try:
        with bot:
            message = get_message_details(link)
            if message:
                message_content = message.text if message.text else "No text content."
                photos = [photo.file_id for photo in message.photo]
                return jsonify({
                    'success': True,
                    'messageContent': message_content,
                    'photos': photos
                })
            else:
                return jsonify({'success': False, 'errorMessage': 'Failed to fetch message details'})
    except Exception as e:
        return jsonify({'success': False, 'errorMessage': str(e)})

def get_message_details(message_link):
    parts = message_link.rstrip('/').split('/')
    if len(parts) >= 5 and parts[0] == 'https:' and parts[1] == '' and parts[2] == 't.me' and parts[3] == 'c':
        chat_id = int(parts[4])
        message_id = int(parts[5]) if len(parts) >= 6 else 1
        try:
            with bot:
                return bot.get_messages(chat_id, message_id)
        except Exception as e:
            print(f"Error fetching message details: {e}")
    return None

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    bot.run()
