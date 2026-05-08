from . import host
from flask import redirect, url_for, render_template, flash, session, request
from ..hotel.form import HotelForm
import random
import os
from flask_mail import Message
from app import mail,db
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User_cred,Hotels, Rooms, Room_Image, Facilities, Room_facilities, Bookings
import app.services.hotel_service as hotel
import app.services.user_service as User
from app.auth.decorator import auth_required, login_required


@host.route('/dashboard')
@auth_required('host')
def dashboard():
    if session['user_id']:
        
        user = User.getUserById(session['user_id'])
        hotel = Hotels.query.filter(Hotels.host_id == user.id).count()
        total_rooms = 0

        for h in user.hotels:
            room = Rooms.query.filter(Rooms.hotel_id == h.id).count()
            total_rooms = total_rooms + room

        total_bookings = 0
        for h in user.hotels:
            booking = Bookings.query.filter(Bookings.hotel_id == h.id, Bookings.status == 'confirmed').count()
            total_bookings = total_bookings + booking

        print(total_rooms, total_bookings)

        if user.role == 'host':
            return render_template('hostDashboard.html', hostUser = user, hotels = hotel, rooms = total_rooms, bookings = total_bookings)
        else:
            flash('Access Denied!', 'flash-err')
            return redirect(url_for('auth.login'))
        
    else:
        flash('Please Login First!', 'flash-err')
        return redirect(url_for('auth.login'))
    
    
    






