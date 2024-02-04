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

@app.route('/get_message_content', methods=['POST'])
def get_message_content():
    message_link = request.json.get('messageLink')
    try:
        with bot:
            message = get_message_details(message_link)
            if message:
                message_content = message.text if message.text else "No text content."
                photos = [photo.file_id for photo in message.photo]
                return jsonify({
                    'success': True,
                    'messageContent': message_content,
                    'photos': photos
                })
            else:
                return jsonify({
                    'success': False,
                    'errorMessage': 'Message not found.'
                })
    except Exception as e:
        return jsonify({
            'success': False,
            'errorMessage': str(e)
        })
        
def get_message_details(message_link):
    link_parts = message_link.split('/')
    if len(link_parts) == 6 and link_parts[3] == 'c':
        try:
            chat_id = int(link_parts[4])
            message_id = int(link_parts[5])
            with bot:
                chat = bot.get_chat(chat_id)
                message = bot.get_messages(chat_id, message_id)       
                return message
        except (ValueError, IndexError):
            return None
    else:
        return None

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    bot.run()
