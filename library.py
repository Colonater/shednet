
import os
from flask import Blueprint, render_template, send_file, request

library_bp = Blueprint('library', __name__)

# Path to the mock library directory
LIBRARY_PATH = 'library'

@library_bp.route('/library')
def library():
    consoles = [d for d in os.listdir(LIBRARY_PATH) if os.path.isdir(os.path.join(LIBRARY_PATH, d))]
    selected_console = request.args.get('console')
    games = []
    if selected_console:
        console_path = os.path.join(LIBRARY_PATH, selected_console)
        games = [f for f in os.listdir(console_path) if os.path.isfile(os.path.join(console_path, f))]
    return render_template('library.html', consoles=consoles, selected_console=selected_console, games=games)

@library_bp.route('/library/<console>/<game>')
def download_game(console, game):
    game_path = os.path.join(LIBRARY_PATH, console, game)
    return send_file(game_path, as_attachment=True)