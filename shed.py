from flask import Flask, render_template
from players import players_bp
from radio import radio_bp
from games import games_bp
from library import library_bp

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max file size

# Register blueprints
app.register_blueprint(players_bp)
app.register_blueprint(radio_bp)
app.register_blueprint(games_bp)
app.register_blueprint(library_bp)

@app.route('/')
def home():
    # Render the home page
    return render_template('index.html')

@app.route('/games')
def games():
    # Render the games page
    return render_template('games.html')

@app.route('/shed')
def shed():
    # Render the shed page
    return render_template('shed.html')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)