from flask import Flask, render_template, jsonify
from tinydb import TinyDB, Query

app = Flask(__name__)
db = TinyDB('shed.json')
Item = Query()

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
    return render_template('players.html')

@app.route('/add_item/<name>')
def add_item(name):
    db.insert({'name': name})
    return jsonify({'message': 'Item added'})

@app.route('/radio')
def radio():
    return render_template('radio.html')

@app.route('/get_items')
def get_items():
    items = db.all()
    return jsonify(items)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')