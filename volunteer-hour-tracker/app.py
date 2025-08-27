import sqlite3
from flask import Flask, render_template, request, jsonify, g

app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

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

