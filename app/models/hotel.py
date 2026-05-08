from app import db

class Hotels(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(500), nullable = False)
    type = db.Column(db.String(50), nullable = False)
    city = db.Column(db.String(50), nullable = False)
    location = db.Column(db.String(200), nullable = False)
    images = db.Column(db.String(100), default = 'default_hotel.avif')
    total_rooms = db.Column(db.Integer, nullable = False)
    

    host_id = db.Column(db.Integer, db.ForeignKey('user_cred.id'))
    rooms = db.relationship('Rooms', backref='hotel')
    bookings = db.relationship('Bookings', backref='hotel')