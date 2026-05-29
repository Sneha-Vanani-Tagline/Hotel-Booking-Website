from app import db

class User_cred(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable = False)
    email = db.Column(db.String(30), nullable = False, unique = True)
    image = db.Column(db.String(100), default = 'profile1.png')
    password = db.Column(db.String(255), nullable = False)
    role = db.Column(db.String(15), nullable = False)
    is_online = db.Column(db.Boolean, default = False)
    last_seen = db.Column(db.DateTime)

    hotels = db.relationship('Hotels', backref = 'host')
    bookings = db.relationship('Bookings', backref = 'user')
    conversations = db.relationship('Conversation', backref='user')

    