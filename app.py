from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import os 

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/paste_bin"
mongo = PyMongo(app)

@app.route('/')
def index():
    pastes = mongo.db.pastes.find()
    return render_template('index.html', pastes=pastes)

@app.route('/create', methods=['POST'])
def create():
    code = request.form.get('code')
    paste_id = mongo.db.pastes.insert_one({'code': code}).inserted_id
    return redirect(url_for('paste', paste_id=paste_id))

@app.route('/paste/<paste_id>')
def paste(paste_id):
    paste = mongo.db.pastes.find_one({'_id': ObjectId(paste_id)})
    return render_template('paste.html', paste=paste)

@app.route('/delete/<paste_id>')
def delete(paste_id):
    mongo.db.pastes.delete_one({'_id': ObjectId(paste_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

