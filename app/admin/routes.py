from . import admin_bp
from flask import flash, session, render_template, redirect, url_for, request
from app.admin.form import LoginForm
import random
from datetime import date, datetime, timezone
from app import mail,db
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User_cred, Bookings, Hotels, Rooms
import app.services.user_service as User_S
import app.services.hotel_service as Hotel_S
from app.auth.decorator import auth_required
from app.tasks import cancelBooking_Mail
import os
from dotenv import load_dotenv
from app.extensions import socketio
from app.extensions import cache
from flask_login import current_user, login_user


load_dotenv()
sender_mail = os.getenv('MAIL_USERNAME')


# # Get Admin User
# def getUser(mail):
#     return user

# Login Route
@admin_bp.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'GET':
        return render_template('login.html', form = form)
    
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User_cred.query.filter_by(email=mail).first()

        if check_password_hash(user.password, password):

            login_user(user)

            flash('✅ Successfully Loged In.','flash-success')
            return redirect(url_for('admin_bp.dashboard'))     # One bug here: it is redirected to the auth/result route after login
        
        else:
            flash('Invalid Details', 'flash-err')
            return render_template('login.html', form = form)

@admin_bp.route('/dashboard')
@auth_required('admin')
def dashboard():
    today = date.today()
    users = User_cred.query.filter(User_cred.role != 'admin').count()
    hotels = db.session.query(Hotels).count()
    bookings = Bookings.query.filter(Bookings.status == 'confirmed', Bookings.date_of_departure >= today).count()
    completedBooking = Bookings.query.filter(Bookings.status == 'confirmed', Bookings.date_of_departure < today).count()
    cancelBooking = Bookings.query.filter(Bookings.status == 'cancelled').count()

    return render_template('dashboard.html', users=users, hotels=hotels, bookings=bookings, cancelBookings = cancelBooking, completedBooking = completedBooking)

# user list
@admin_bp.route('/userlist')
@auth_required('admin')
@cache.cached(120, key_prefix='user_list')
def userlist():
    users = User_cred.query.filter(User_cred.role != 'admin', User_cred.role != 'host').all()
    hosts = User_cred.query.filter(User_cred.role != 'admin', User_cred.role != 'user').all()

    return render_template('userlist.html', users = users, hosts = hosts)

# booking list
@admin_bp.route('/bookinglist', methods = ['POST', 'GET'])
@auth_required('admin')
@cache.cached(120, key_prefix='admin_booking_list')
def bookinglist():
    bookings = Hotel_S.getAllBookings()

    # cancel booking
    if request.method == 'POST':
        bid = request.form.get('bookingid')
        current_booking = Hotel_S.getBooking_ById(bid)
        reason = request.form.get('cancel_reason')
        cancelled_by = 'admin'

        Hotel_S.cancelBooking(bid=bid, reason=reason, cancelledBy=cancelled_by)
        
        cancelBooking_Mail.delay(subject='Booking Cancelled', send=sender_mail, receiver=current_booking.user.email, uname=current_booking.user.name, bid=current_booking.id, hotel_name=current_booking.hotel.name, room=current_booking.rooms.category, cancel_by= 'Super Admin', price=current_booking.total_price, reason = reason)

        event_data = {
                'room': current_booking.rooms.category,
                'hotelName': current_booking.hotel.name
            }
        
        socketio.emit('booking_cancelled', event_data, to=f'user_{current_booking.user_id}')
        socketio.emit('update_host_dashboard', to=f'host_{current_booking.hotel.host_id}')
        socketio.emit('update_myBookings', to=f'user_{current_booking.user_id}')

        cache.delete('host_booking_list')
        cache.delete('admin_booking_list')

        flash('Booking cancelled!', 'flash-success')

    return render_template('bookinglist.html', bookings=bookings)

# hotel request
@admin_bp.route('/hotellist')
@auth_required('admin')
@cache.cached(100, key_prefix='admin_hotel_list')
def hotellist():
    Hotels = Hotel_S.getAllHotels()

    return render_template('hotellist.html', Hotels=Hotels)