from app import db
from app.extensions import login_manager
from flask_login import UserMixin

class User_cred(db.Model, UserMixin):
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
    audit_logs = db.relationship('Audit_logs', backref = 'user')

    def __str__(self):
        return self.name

    
@login_manager.user_loader
def load_user(uid):

    return User_cred.query.get(int(uid))