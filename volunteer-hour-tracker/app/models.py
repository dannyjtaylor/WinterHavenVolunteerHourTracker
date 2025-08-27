class Volunteer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    hours = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Volunteer {self.name}>'

    @classmethod
    def add_volunteer(cls, name, hours):
        volunteer = cls(name=name, hours=hours)
        db.session.add(volunteer)
        db.session.commit()

    @classmethod
    def get_all_volunteers(cls):
        return cls.query.all()

    @classmethod
    def get_total_hours(cls):
        return db.session.query(db.func.sum(cls.hours)).scalar() or 0