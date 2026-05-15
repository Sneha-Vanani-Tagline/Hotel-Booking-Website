from celery import shared_task
from flask_mail import Message
from flask import render_template
from datetime import date, timedelta
from app.extensions import mail
from app.models import Bookings
import random
import os
from dotenv import load_dotenv

load_dotenv()
sender_mail = os.getenv('MAIL_USERNAME')

# Mail Creation and sending
@shared_task
def createMail(send, receiver, subject, content):
    
    msg = Message(subject, sender=send, recipients=[receiver])
    msg.body = content
    mail.send(msg)

    print('auth mail sent')

@shared_task
def bookingSuccess_Mail(send, receiver, subject, uname, bid, hotel_name, room, checkin, checkout):

    msg = Message(
        subject,
        sender=send,
        recipients=[receiver]
    )

    msg.html = render_template(
        'booking-mail.html',
        user_name=uname,
        booking_id=bid,
        hotel_name=hotel_name,
        room_type=room,
        checkin=checkin,
        checkout=checkout,
        target='success'
    )

    mail.send(msg)

    print('Booking mail sent')

@shared_task
def cancelBooking_Mail(send, receiver, subject, uname, bid, hotel_name, room, cancel_by, reason, price):
 
    msg = Message(subject, sender=send, recipients=[receiver])
    msg.html = render_template(
        'booking-mail.html',
        user_name = uname,
        booking_id = bid,
        hotel_name = hotel_name,
        room_type = room,
        cancel_by = cancel_by, 
        cancel_reason= reason,
        refund_amount = price,
        target = 'cancel'
    )
    
    mail.send(msg)
    print('cancel mail sent')


@shared_task
def check_booking_reminder():
    tomorow = date.today() + timedelta(days=1)
    print(tomorow)

    bookings = Bookings.query.filter(Bookings.date_of_arrival == tomorow).all()

    for b in bookings:
        msg = Message('Check-in Reminder', sender=sender_mail, recipients=[b.user.email])
        msg.html = render_template(
            'checkin-reminder.html',
            user_name = b.user.name,
            booking_id = b.id,
            hotel_name = b.hotel.name,
            room_type = b.rooms.category,
            checkin=b.dadate_of_arrivalte_of,
            checkout=b.date_of_departure,
        )
        mail.send(msg)

    print('all check-in reminder sent')