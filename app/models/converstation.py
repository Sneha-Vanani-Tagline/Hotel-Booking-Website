from app import db

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_cred.id'))
    host_id = db.Column(db.Integer)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'))

    chat = db.relationship('Chat_message', backref='conversation')