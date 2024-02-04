from flask import Flask, render_template, request, jsonify
from pyrogram import Client, filters
from pyrogram.types import Message
import os

app = Flask(__name__)

api_id = 14688437
api_hash = "5310285db722d1dceb128b88772d53a6"
bot_token = "6162291374:AAGieKLuy_e7Id8G2pQaXRiNsuiviWgalDE"

bot = Client("santhu", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_channel_content', methods=['POST'])
def get_channel_content():
    channel_username = request.json.get('channelUsername')
    try:
        with bot:
            message = bot.get_chat_history(channel_username, limit=1)[0]
            message_content = message.text if message.text else "No text content."
            photos = [photo.file_id for photo in message.photo]
            return jsonify({
                'success': True,
                'messageContent': message_content,
                'photos': photos
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'errorMessage': str(e)
        })

if __name__ == '__main__':
   bot.run()