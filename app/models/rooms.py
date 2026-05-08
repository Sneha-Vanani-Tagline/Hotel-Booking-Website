from app import db

class Rooms(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    category = db.Column(db.String(30), nullable = False)
    bedrooms = db.Column(db.Integer, nullable = False)
    beds = db.Column(db.Integer, nullable = False)
    person_capacity = db.Column(db.Integer, nullable = False)
    price_per_night = db.Column(db.Integer, nullable = False)
    no_rooms = db.Column(db.Integer, nullable = False)
    # available_rooms = db.Column(db.Integer, nullable = False)
    
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'))        # Foreign Keys
    
    
    bookings = db.relationship('Bookings', backref='rooms')                  # Relationships
    facilities = db.relationship('Room_facilities', backref = 'room')       # Relationships
    images = db.relationship('Room_Image', backref = 'room')                # Relationships

class Room_Image(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))      # Foreign Keys
    image = db.Column(db.String, nullable = False)