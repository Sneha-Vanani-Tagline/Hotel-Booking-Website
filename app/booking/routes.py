from . import booking
from flask import request, redirect, url_for, render_template, flash, session
import os
from datetime import date, datetime, timezone
from werkzeug.utils import secure_filename
import app.services.hotel_service as Hotel_S
import app.services.user_service as User_S
from app.auth.decorator import auth_required, login_required


@booking.route('/saveBooking', methods = ['POST'])
@auth_required('user')
def saveBooking():
    if 'rid' in session and 'booking' in session:
        room = Hotel_S.getRoomById(session['rid'])
        bookingData = session['booking']

        session.pop('rid', None)
        session.pop('booking', None)
    else:
        flash('rid and booking data not found', 'flash-err')
    
    if request.method == 'POST':
        
        data = {}
        for i in bookingData:
            data[i] = bookingData[i]

        data['bedrooms'] = room.bedrooms
        data['rid'] = room.id
        data['uid'] = session['user_id']
        data['hid'] = room.hotel_id

        if Hotel_S.addBooking(data):
            flash('Congratulations!, Booking Successful', 'flash-success')
            return redirect(url_for('booking.myBookings', uid = session['user_id']))
        else:
            flash('Conflictaed with available rooms', 'flash-err') 
            return redirect(url_for('user.payment'))

@booking.route('/myBookings/<int:uid>', methods = ['GET', 'POST'])
@auth_required('user')
def myBookings(uid):
    user = User_S.getUserById(uid)
    bookings = user.bookings

    # cancel booking
    if request.method == 'POST':
        bid = request.form.get('bookingid')
        current_booking = []

        for b in bookings:
            if b.id == int(bid):
                current_booking=b

        reason = request.form.get('cancel_reason')
        cancelled_by = 'user'

        diff = (current_booking.date_of_arrival - datetime.now(timezone.utc).date()).days
        
        if diff >= 2:
            Hotel_S.cancelBooking(bid=bid,reason=reason,cancelledBy=cancelled_by)
            flash('Booking cancelled!', 'flash-success')
        else:
            flash('Cancellation is no longer allowed. Bookings can only be cancelled at least 2 days before the check-in date!', 'flash-err')
    
    return render_template('myBookings.html', user= user, bookings=bookings)

# host bookings
@booking.route('/allBookings', methods = ['GET', 'POST'])
@auth_required('host')
def allBookings():
    hostUser = User_S.getUserById(session['user_id'])
    hotel = hostUser.hotels
    
    
    if request.method == 'POST':
        bid = request.form.get('bookingid')
        current_booking = Hotel_S.getBooking_ById(bid)
        reason = request.form.get('cancel_reason')
        cancelled_by = 'host'
        # print(type(datetime.utcnow), lambda: datetime.now(timezone.utc))
        # print(type(datetime.now(timezone.utc)), datetime.now(timezone.utc))

        diff = (current_booking.date_of_arrival - datetime.now(timezone.utc).date()).days
        
        if diff >= 2:
            Hotel_S.cancelBooking(bid=bid,reason=reason,cancelledBy=cancelled_by)
            flash('Booking cancelled!', 'flash-success')
        else:
            flash('Cancellation is no longer allowed. Bookings can only be cancelled at least 2 days before the check-in date!', 'flash-err')
        

    return render_template('hostBookings.html', hostUser = hostUser, hotels=hotel)