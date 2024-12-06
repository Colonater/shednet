from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from tinydb import TinyDB, Query
from werkzeug.utils import secure_filename
from PIL import Image
import os

players_bp = Blueprint('players', __name__, url_prefix='/players')
db = TinyDB('shed.json')
Player = Query()

@players_bp.route('/')
def players():
    # Fetch all players from the database and render the players page
    players = db.table('players').all()
    return render_template('players.html', players=players)

@players_bp.route('/admin')
def admin():
    # Fetch all players from the database and render the admin page
    players = db.table('players').all()
    return render_template('admin.html', players=players)

@players_bp.route('/add_player', methods=['POST'])
def add_player():
    # Add a new player to the database
    name = request.form['name']
    wins = int(request.form['wins'])
    shedcoins = int(request.form['shedcoins'])
    picture = request.files.get('picture')  # Use .get() to avoid KeyError
    picture_filename = None

    if picture and picture.filename != '':
        picture_filename = secure_filename(picture.filename)
        picture_path = os.path.join('static/uploads', picture_filename)
        picture.save(picture_path)
        resize_image(picture_path)

    db.table('players').insert({'name': name, 'picture': picture_filename, 'wins': wins, 'shedcoins': shedcoins})
    return redirect(url_for('players.players'))

@players_bp.route('/edit_player/<int:player_id>', methods=['POST'])
def edit_player(player_id):
    # Edit player details
    picture = request.files.get('picture')  # Use .get() to avoid KeyError
    picture_filename = None

    if picture and picture.filename != '':
        picture_filename = secure_filename(picture.filename)
        picture_path = os.path.join('static/uploads', picture_filename)
        picture.save(picture_path)
        resize_image(picture_path)
        db.table('players').update({'picture': picture_filename}, doc_ids=[player_id])

    return redirect(url_for('players.admin'))

@players_bp.route('/update_shedcoins/<int:player_id>', methods=['POST'])
def update_shedcoins(player_id):
    # Update shedcoins for a player
    shedcoins = int(request.form['shedcoins'])
    db.table('players').update({'shedcoins': shedcoins}, doc_ids=[player_id])
    return redirect(url_for('players.admin'))

@players_bp.route('/add_win/<int:player_id>', methods=['POST'])
def add_win(player_id):
    # Increment the win count for a player
    player = db.table('players').get(doc_id=player_id)
    new_wins = player['wins'] + 1
    db.table('players').update({'wins': new_wins}, doc_ids=[player_id])
    return redirect(url_for('players.admin'))

@players_bp.route('/reset_stats/<int:player_id>', methods=['POST'])
def reset_stats(player_id):
    # Reset wins and shedcoins for a player
    db.table('players').update({'wins': 0, 'shedcoins': 0}, doc_ids=[player_id])
    return redirect(url_for('players.admin'))

def resize_image(image_path):
    # Resize the uploaded image to 500x500 pixels
    with Image.open(image_path) as img:
        img = img.resize((500, 500))
        img.save(image_path)

@players_bp.route('/get_players')
def get_players():
    # Return a JSON list of all players
    players = db.table('players').all()
    return jsonify(players)