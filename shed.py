from flask import Flask, render_template, request, redirect, url_for, jsonify
from tinydb import TinyDB, Query
from werkzeug.utils import secure_filename
from PIL import Image
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max file size
db = TinyDB('shed.json')
Player = Query()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/games')
def games():
    return render_template('games.html')

@app.route('/shed')
def shed():
    return render_template('shed.html')

@app.route('/players')
def players():
    players = db.table('players').all()
    return render_template('players.html', players=players)

@app.route('/admin')
def admin():
    players = db.table('players').all()
    return render_template('admin.html', players=players)

@app.route('/radio')
def radio():
    return render_template('radio.html')

@app.route('/add_player', methods=['POST'])
def add_player():
    name = request.form['name']
    wins = int(request.form['wins'])
    shedcoins = int(request.form['shedcoins'])
    picture = request.files.get('picture')  # Use .get() to avoid KeyError
    picture_filename = None

    if picture and picture.filename != '':
        picture_filename = secure_filename(picture.filename)
        picture_path = os.path.join(app.config['UPLOAD_FOLDER'], picture_filename)
        picture.save(picture_path)
        resize_image(picture_path)

    db.table('players').insert({'name': name, 'picture': picture_filename, 'wins': wins, 'shedcoins': shedcoins})
    return redirect(url_for('players'))

@app.route('/edit_player/<int:player_id>', methods=['POST'])
def edit_player(player_id):
    picture = request.files.get('picture')  # Use .get() to avoid KeyError
    picture_filename = None

    if picture and picture.filename != '':
        picture_filename = secure_filename(picture.filename)
        picture_path = os.path.join(app.config['UPLOAD_FOLDER'], picture_filename)
        picture.save(picture_path)
        resize_image(picture_path)
        db.table('players').update({'picture': picture_filename}, doc_ids=[player_id])

    return redirect(url_for('admin'))

@app.route('/update_shedcoins/<int:player_id>', methods=['POST'])
def update_shedcoins(player_id):
    shedcoins = int(request.form['shedcoins'])
    db.table('players').update({'shedcoins': shedcoins}, doc_ids=[player_id])
    return redirect(url_for('admin'))

@app.route('/add_win/<int:player_id>', methods=['POST'])
def add_win(player_id):
    player = db.table('players').get(doc_id=player_id)
    new_wins = player['wins'] + 1
    db.table('players').update({'wins': new_wins}, doc_ids=[player_id])
    return redirect(url_for('admin'))

@app.route('/reset_stats/<int:player_id>', methods=['POST'])
def reset_stats(player_id):
    db.table('players').update({'wins': 0, 'shedcoins': 0}, doc_ids=[player_id])
    return redirect(url_for('admin'))

def resize_image(image_path):
    with Image.open(image_path) as img:
        img = img.resize((500, 500))
        img.save(image_path)

@app.route('/get_players')
def get_players():
    players = db.table('players').all()
    return jsonify(players)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)