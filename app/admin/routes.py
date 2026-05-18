from . import admin
from flask import flash, session, render_template, redirect, url_for, request
from app.admin.form import LoginForm
import random
from datetime import date, datetime, timezone
from flask_mail import Message
from app import mail,db
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User_cred, Bookings, Hotels, Rooms
import app.services.user_service as User_S
import app.services.hotel_service as Hotel_S
from app.auth.decorator import auth_required, login_required
from app.tasks import cancelBooking_Mail
import os
from dotenv import load_dotenv

load_dotenv()
sender_mail = os.getenv('MAIL_USERNAME')


# Get Admin User
def getUser(mail):
    user = User_cred.query.filter_by(email=mail).first()
    return user

# Login Route
@admin.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'GET':
        return render_template('login.html', form = form)
    
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = getUser(email)

        if check_password_hash(user.password, password):
            flash('✅ Successfully Loged In.','flash-success')
            return redirect(url_for('admin.dashboard'))     # One bug here: it is redirected to the auth/result route after login
        else:
            flash('Invalid Details', 'flash-err')
            return render_template('login.html', form = form)

@admin.route('/dashboard')
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
@admin.route('/userlist')
@auth_required('admin')
def userlist():
    users = User_cred.query.filter(User_cred.role != 'admin', User_cred.role != 'host').all()
    hosts = User_cred.query.filter(User_cred.role != 'admin', User_cred.role != 'user').all()

    return render_template('userlist.html', users = users, hosts = hosts)

# booking list
@admin.route('/bookinglist', methods = ['POST', 'GET'])
@auth_required('admin')
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

        flash('Booking cancelled!', 'flash-success')
        

    return render_template('bookinglist.html', bookings=bookings)

# hotel request
@admin.route('/hotellist')
@auth_required('admin')
def hotellist():
    Hotels = Hotel_S.getAllHotels()

    return render_template('hotellist.html', Hotels=Hotels)