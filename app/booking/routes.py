from . import booking
from flask import request, redirect, url_for, render_template, flash, session
from datetime import date, datetime, timezone
import app.services.hotel_service as Hotel_S
import app.services.user_service as User_S
from app.auth.decorator import auth_required
from app.tasks import bookingSuccess_Mail,cancelBooking_Mail
import os
from dotenv import load_dotenv
# import app.socket as Socket 
from app.extensions import socketio
from app.extensions import cache
from flask_login import current_user

load_dotenv()
sender_mail = os.getenv('MAIL_USERNAME')


# save bookings
@booking.route('/saveBooking', methods=['POST'])
@auth_required('user')
def saveBooking():

    if 'rid' in session and 'booking' in session:

        user = current_user
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
    data['uid'] = current_user.id
    data['hid'] = room.hotel_id

    result = Hotel_S.addBooking(data)

    if result:
        
        data = {'hotelName' : room.hotel.name, 'bookerName': user.name, 'roomName': f'host_{room.hotel.host_id}'}

        socketio.emit('booking_created', 
                    data, 
                    to=f'host_{room.hotel.host_id}')
        socketio.emit('update_host_dashboard', to=f'host_{room.hotel.host_id}')
        
        
        data = {'hotelName' : room.hotel.name, 'bookerName': user.name, 'roomName': 'super_admin'}
        socketio.emit('booking_created', 
                    data, 
                    room='super_admin')
        socketio.emit('update_admin_dashboard', to='super_admin')
        

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

        cache.delete('host_booking_list')
        cache.delete('admin_booking_list')

        return redirect(url_for('booking.myBookings'))

    else:

        flash('Conflicted with available rooms', 'flash-err')
        return redirect(url_for('user.payment'))
    
# user panel: mybookings
@booking.route('/myBookings', methods = ['GET', 'POST'])
@auth_required('user')
def myBookings():
    user = current_user
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
            Hotel_S.cancelBooking(bid=bid, reason=reason, cancelledBy=cancelled_by)
            
            cancelBooking_Mail.delay(subject='Booking Cancelled', send=sender_mail, receiver=current_user.email, uname=user.name, bid=current_booking.id, hotel_name=current_booking.hotel.name, room=current_booking.rooms.category, cancel_by= 'You', price=current_booking.total_price, reason = reason)
            
            cache.delete('host_booking_list')
            cache.delete('admin_booking_list')

            # Updating dashboard
            socketio.emit('update_host_dashboard', to=f'host_{current_booking.hotel.host_id}')
            socketio.emit('update_admin_dashboard', to='super_admin')

            flash('Booking cancelled!', 'flash-success')
        else:
            flash('Cancellation is no longer allowed. Bookings can only be cancelled at least 2 days before the check-in date!', 'flash-err')
    
    return render_template('myBookings.html', user= user, bookings=bookings)

# host bookings
@booking.route('/allBookings', methods = ['GET', 'POST'])
@auth_required('host')
@cache.cached(100, key_prefix='host_booking_list')
def allBookings():
    hostUser = current_user
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
            
            event_data = {
                'room': current_booking.rooms.category,
                'hotelName': current_booking.hotel.name
            }

            socketio.emit('booking_cancelled', event_data, to=f'user_{current_booking.user_id}')
            socketio.emit('update_admin_dashboard', to='super_admin')
            socketio.emit('update_myBookings', to=f'user_{current_booking.user_id}')

            cache.delete('host_booking_list')
            cache.delete('admin_booking_list')

            flash('Booking cancelled!', 'flash-success')
        else:
            flash('Cancellation is no longer allowed. Bookings can only be cancelled at least 2 days before the check-in date!', 'flash-err')
        

    return render_template('hostBookings.html', hostUser = hostUser, hotels=hotels)