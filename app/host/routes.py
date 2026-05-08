from . import host
from flask import redirect, url_for, render_template, flash, session, request
from app import mail,db
from datetime import datetime, date, timezone
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User_cred,Hotels, Rooms, Room_Image, Facilities, Room_facilities, Bookings
import app.services.hotel_service as hotel_S
import app.services.user_service as User_S
from app.auth.decorator import auth_required, login_required


@host.route('/dashboard')
@auth_required('host')
def dashboard():
    if session['user_id']:
        
        user = User_S.getUserById(session['user_id'])
        hotel = Hotels.query.filter(Hotels.host_id == user.id).count()
        total_rooms = 0

        for h in user.hotels:
            room = Rooms.query.filter(Rooms.hotel_id == h.id).count()
            total_rooms = total_rooms + room

        active_bookings = 0
        completed_bookings = 0
        cancelled_bookings = 0
        
        for h in user.hotels:
            today = date.today()
            active = Bookings.query.filter(Bookings.hotel_id == h.id, Bookings.status == 'confirmed', Bookings.date_of_departure >= today).count()
            active_bookings = active_bookings + active
            
            completed = Bookings.query.filter(Bookings.hotel_id == h.id, Bookings.status == 'confirmed', Bookings.date_of_departure < today).count()
            completed_bookings = completed_bookings + completed

            cancel = Bookings.query.filter(Bookings.hotel_id == h.id, Bookings.status == 'cancelled').count()
            cancelled_bookings = cancelled_bookings + cancel

        return render_template('hostDashboard.html', hostUser = user, hotels = hotel, rooms = total_rooms, active_bookings = active_bookings, completed_bookings = completed_bookings, cancelled_bookings = cancelled_bookings)
        
    
    
    






