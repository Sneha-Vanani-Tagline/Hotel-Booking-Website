from app import db

class Facilities(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable = False)
    room_facility = db.relationship('Room_facilities', backref = 'facility')

class Room_facilities(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    facility_id = db.Column(db.Integer, db.ForeignKey('facilities.id'))