from app.extensions import flaskAdmin, db
from flask_admin.contrib.sqla import ModelView
from app.models import User_cred, Hotels, Bookings, Rooms
from .views import UserView, BookingView, RoomView, HotelView
    
def init_admin():
    flaskAdmin.add_view(UserView(User_cred, db))
    flaskAdmin.add_view(HotelView(Hotels, db))
    flaskAdmin.add_view(BookingView(Bookings, db))
    flaskAdmin.add_view(RoomView(Rooms, db))