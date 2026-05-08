from app import db
from datetime import datetime, timezone

class Bookings(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date_of_arrival = db.Column(db.Date, nullable = False)
    date_of_departure = db.Column(db.Date, nullable = False)
    nights = db.Column(db.Integer, nullable=False)
    bedrooms = db.Column(db.Integer, nullable = False)
    guest = db.Column(db.Integer, nullable = False)
    
    total_price = db.Column(db.Float, nullable = False)
    status = db.Column(db.String(20), nullable = False, default = 'Pending')  #  confirmed / cancelled

    # if status == cancelled 
    cancel_reason = db.Column(db.Text, nullable=True)
    cancelled_by = db.Column(db.String)  # 'host' or 'user'
    cancelled_at = db.Column(db.DateTime)

    booking_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    

    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user_cred.id'))
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'))

    # room = db.relationship('Rooms', backref='bookings') 
    # user = db.relationship('User_cred', backref='bookings')   

    
    