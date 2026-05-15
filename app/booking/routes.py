from . import booking
from flask import request, redirect, url_for, render_template, flash, session
from datetime import date, datetime, timezone
import app.services.hotel_service as Hotel_S
import app.services.user_service as User_S
from app.auth.decorator import auth_required, login_required
from app.tasks import bookingSuccess_Mail,cancelBooking_Mail
import os
from dotenv import load_dotenv

load_dotenv()
sender_mail = os.getenv('MAIL_USERNAME')


# save bookings
@booking.route('/saveBooking', methods=['POST'])
@auth_required('user')
def saveBooking():

    if 'rid' in session and 'booking' in session:

        user = User_S.getUserById(session['user_id'])
        room = Hotel_S.getRoomById(session['rid'])
        bookingData = session['booking']

        session.pop('rid', None)
        session.pop('booking', None)

    else:
        flash('Booking data not found', 'flash-err')
        return redirect(url_for('user.payment'))

    data = {}

    for i in bookingData:
        data[i] = bookingData[i]

    data['bedrooms'] = room.bedrooms
    data['rid'] = room.id
    data['uid'] = session['user_id']
    data['hid'] = room.hotel_id

    result = Hotel_S.addBooking(data)

    if result:

        bookingSuccess_Mail.delay(
            subject='Booking Successful',
            send=sender_mail,
            receiver=user.email,
            uname=user.name,
            bid=result,
            hotel_name=room.hotel.name,
            room=room.category,
            checkin=bookingData['checkin'],
            checkout=bookingData['checkout']
        )

        flash('Congratulations! Booking Successful', 'flash-success')

        return redirect(
            url_for(
                'booking.myBookings',
                uid=session['user_id']
            )
        )

    else:

        flash('Conflicted with available rooms', 'flash-err')
        return redirect(url_for('user.payment'))
    
# user panel: mybookings
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
        print(diff)

        if diff >= 2:
            Hotel_S.cancelBooking(bid=bid, reason=reason, cancelledBy=cancelled_by)
            
            cancelBooking_Mail.delay(subject='Booking Cancelled', send=sender_mail, receiver=session['email'], uname=user.name, bid=current_booking.id, hotel_name=current_booking.hotel.name, room=current_booking.rooms.category, cancel_by= 'You', price=current_booking.total_price, reason = reason)
            flash('Booking cancelled!', 'flash-success')
        else:
            flash('Cancellation is no longer allowed. Bookings can only be cancelled at least 2 days before the check-in date!', 'flash-err')
    
    return render_template('myBookings.html', user= user, bookings=bookings)

# host bookings
@booking.route('/allBookings', methods = ['GET', 'POST'])
@auth_required('host')
def allBookings():
    hostUser = User_S.getUserById(session['user_id'])
    hotels = hostUser.hotels

    # cancel booking
    if request.method == 'POST':
        bid = request.form.get('bookingid')
        current_booking = Hotel_S.getBooking_ById(bid)
        reason = request.form.get('cancel_reason')
        cancelled_by = 'host'
    
        diff = (current_booking.date_of_arrival - datetime.now(timezone.utc).date()).days
        
        if diff >= 2:
            Hotel_S.cancelBooking(bid=bid,reason=reason,cancelledBy=cancelled_by)
            
            cancelBooking_Mail.delay(subject='Booking Cancelled', send=sender_mail, receiver=current_booking.user.email, uname=current_booking.user.name, bid=current_booking.id, hotel_name=current_booking.hotel.name, room=current_booking.rooms.category, cancel_by= 'Hotel Owner', price=current_booking.total_price, reason = reason)
            flash('Booking cancelled!', 'flash-success')
        else:
            flash('Cancellation is no longer allowed. Bookings can only be cancelled at least 2 days before the check-in date!', 'flash-err')
        

    return render_template('hostBookings.html', hostUser = hostUser, hotels=hotels)