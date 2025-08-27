from flask import Blueprint, render_template, request, jsonify
from .models import Volunteer, db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    volunteers = Volunteer.query.all()
    total_hours = sum(volunteer.hours for volunteer in volunteers)
    return render_template('index.html', volunteers=volunteers, total_hours=total_hours)

@main.route('/add', methods=['POST'])
def add_volunteer_hours():
    name = request.form.get('name')
    hours = request.form.get('hours', type=int)
    if name and hours is not None:
        new_volunteer = Volunteer(name=name, hours=hours)
        db.session.add(new_volunteer)
        db.session.commit()
        return jsonify({'message': 'Volunteer hours added successfully!'}), 201
    return jsonify({'error': 'Invalid input'}), 400

@main.route('/data')
def get_volunteer_data():
    volunteers = Volunteer.query.all()
    volunteer_data = [{'id': v.id, 'name': v.name, 'hours': v.hours} for v in volunteers]
    return jsonify(volunteer_data)