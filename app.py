from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
pastes = []

@app.route('/')
def index():
    return render_template('templates/index.html', pastes=pastes)

@app.route('/create', methods=['POST'])
def create():
    try:
        code = request.form.get('code')
        paste_id = len(pastes) + 1  # Assign a simple numerical ID
        paste = {'_id': paste_id, 'code': code}
        pastes.append(paste)
        return redirect(url_for('paste', paste_id=paste_id))
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/paste/<int:paste_id>')
def paste(paste_id):
    try:
        paste = next((p for p in pastes if p['_id'] == paste_id), None)
        if paste:
            return render_template('templates/paste.html', paste=paste)
        else:
            return "Paste not found."
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/delete/<int:paste_id>')
def delete(paste_id):
    global pastes
    pastes = [p for p in pastes if p['_id'] != paste_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
