import sqlite3
from flask import Flask, render_template, request, jsonify, g

app = Flask(__name__)

DATABASE = 'volunteers.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS volunteers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                hours INTEGER NOT NULL
            )
        ''')
        db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    db = get_db()
    cur = db.execute('SELECT name, SUM(hours) as total_hours FROM volunteers GROUP BY name')
    volunteers = [{'name': row[0], 'hours': row[1]} for row in cur.fetchall()]
    return jsonify(volunteers)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    hours = int(request.form['hours'])
    db = get_db()
    cur = db.execute('SELECT id FROM volunteers WHERE name = ?', (name,))
    row = cur.fetchone()
    if row:
        db.execute('UPDATE volunteers SET hours = hours + ? WHERE name = ?', (hours, name))
    else:
        db.execute('INSERT INTO volunteers (name, hours) VALUES (?, ?)', (name, hours))
    db.commit()
    return ('', 204)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8000, debug=True)