from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__, template_folder="../app/templates", static_folder="../app/static")
CORS(app)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../volunteers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Volunteer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20))
    # Add more fields as needed
    time_entries = db.relationship('TimeEntry', backref='volunteer', lazy=True, cascade="all, delete-orphan")

class TimeEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    volunteer_id = db.Column(db.Integer, db.ForeignKey('volunteer.id'), nullable=False)
    clock_in = db.Column(db.DateTime, nullable=False)
    clock_out = db.Column(db.DateTime)
    note = db.Column(db.String(255))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/volunteers', methods=['GET', 'POST'])
def volunteers():
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        v = Volunteer(name=name, email=email, phone=phone)
        db.session.add(v)
        db.session.commit()
        return jsonify({'id': v.id, 'name': v.name, 'email': v.email, 'phone': v.phone}), 201
    else:
        all_vols = Volunteer.query.all()
        return jsonify([
            {'id': v.id, 'name': v.name, 'email': v.email, 'phone': v.phone} for v in all_vols
        ])

@app.route('/volunteers/<int:volunteer_id>', methods=['GET', 'PUT', 'DELETE'])
def volunteer_detail(volunteer_id):
    v = Volunteer.query.get_or_404(volunteer_id)
    if request.method == 'GET':
        return jsonify({'id': v.id, 'name': v.name, 'email': v.email, 'phone': v.phone})
    elif request.method == 'PUT':
        data = request.get_json()
        v.name = data.get('name', v.name)
        v.email = data.get('email', v.email)
        v.phone = data.get('phone', v.phone)
        db.session.commit()
        return jsonify({'id': v.id, 'name': v.name, 'email': v.email, 'phone': v.phone})
    elif request.method == 'DELETE':
        db.session.delete(v)
        db.session.commit()
        return '', 204

@app.route('/clockin', methods=['POST'])
def clock_in():
    data = request.get_json()
    volunteer_id = data['volunteer_id']
    note = data.get('note')
    entry = TimeEntry(volunteer_id=volunteer_id, clock_in=datetime.utcnow(), note=note)
    db.session.add(entry)
    db.session.commit()
    return jsonify({'entry_id': entry.id, 'clock_in': entry.clock_in.isoformat()})

@app.route('/clockout/<int:entry_id>', methods=['POST'])
def clock_out(entry_id):
    entry = TimeEntry.query.get_or_404(entry_id)
    if entry.clock_out:
        return jsonify({'error': 'Already clocked out'}), 400
    entry.clock_out = datetime.utcnow()
    db.session.commit()
    return jsonify({'entry_id': entry.id, 'clock_in': entry.clock_in.isoformat(), 'clock_out': entry.clock_out.isoformat()})

@app.route('/volunteers/<int:volunteer_id>/entries', methods=['GET'])
def get_entries(volunteer_id):
    entries = TimeEntry.query.filter_by(volunteer_id=volunteer_id).all()
    return jsonify([
        {
            'id': e.id,
            'clock_in': e.clock_in.isoformat(),
            'clock_out': e.clock_out.isoformat() if e.clock_out else None,
            'note': e.note
        } for e in entries
    ])

@app.route('/entries', methods=['GET'])
def all_entries():
    entries = TimeEntry.query.all()
    return jsonify([
        {
            'id': e.id,
            'volunteer_id': e.volunteer_id,
            'clock_in': e.clock_in.isoformat(),
            'clock_out': e.clock_out.isoformat() if e.clock_out else None,
            'note': e.note
        } for e in entries
    ])

if __name__ == '__main__':
    if not os.path.exists('../volunteers.db'):
        db.create_all()
    app.run(host='0.0.0.0', port=8000, debug=True)
