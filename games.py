from flask import Blueprint, render_template, request, redirect, url_for
from database import get_db_connection

games_bp = Blueprint('games', __name__, url_prefix='/games')

@games_bp.route('/')
def games():
    conn = get_db_connection()
    games = conn.execute('SELECT * FROM games').fetchall()
    conn.close()
    return render_template('games.html', games=games)

@games_bp.route('/manage')
def manage_games():
    conn = get_db_connection()
    games = conn.execute('SELECT * FROM games').fetchall()
    conn.close()
    return render_template('manage_games.html', games=games)

@games_bp.route('/add_game', methods=['POST'])
def add_game():
    gamename = request.form['gamename']
    release_year = request.form['release_year']
    playerscount = request.form['playerscount']
    consoles = request.form['consoles']
    location = request.form['location']
    
    conn = get_db_connection()
    conn.execute('INSERT INTO games (gamename, release_year, playerscount, consoles, location) VALUES (?, ?, ?, ?, ?)',
                 (gamename, release_year, playerscount, consoles, location))
    conn.commit()
    conn.close()
    return redirect(url_for('games.manage_games'))

@games_bp.route('/edit_game/<int:game_id>', methods=['POST'])
def edit_game(game_id):
    gamename = request.form['gamename']
    release_year = request.form['release_year']
    playerscount = request.form['playerscount']
    consoles = request.form['consoles']
    location = request.form['location']
    
    conn = get_db_connection()
    conn.execute('UPDATE games SET gamename = ?, release_year = ?, playerscount = ?, consoles = ?, location = ? WHERE id = ?',
                 (gamename, release_year, playerscount, consoles, location, game_id))
    conn.commit()
    conn.close()
    return redirect(url_for('games.manage_games'))

@games_bp.route('/delete_game/<int:game_id>', methods=['POST'])
def delete_game(game_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM games WHERE id = ?', (game_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('games.manage_games'))