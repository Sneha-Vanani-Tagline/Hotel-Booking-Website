from . import user
from flask import request, redirect, url_for, render_template, flash, session
import os
from datetime import date, datetime, timezone
from werkzeug.utils import secure_filename
import app.services.hotel_service as Hotel_S
import app.services.user_service as User_S
from app.auth.decorator import auth_required, login_required
from app.models import User_cred, Rooms, Room_facilities, Room_Image, Hotels

UPLOAD_FOLDER = 'app/static/images/'

@user.route('/home')
def home():
    rooms = Hotel_S.getAllRooms()
    images = Hotel_S.getAllRoomImages()
    
    cityWise_room = {}
    for r in rooms:
        city = r.hotel.city

        if city not in cityWise_room:
            cityWise_room[city] = []
        
        cityWise_room[city].append(r)

    roomImg = {}
    for i in images:
        if i.room_id not in roomImg:
            # print(i.room_id)
            roomImg[i.room_id] = i.image
        
    return render_template('home.html', cityWise_room = cityWise_room, roomImg = roomImg)
    
@user.route('/rooms/<string:city>')
def rooms(city):
    roomsData = Hotel_S.getAllRooms()
    images = Hotel_S.getAllRoomImages()
    facilities = Hotel_S.getAllRoomFacility()
    city = city.lower()

    cityRoom = []
    roomWise_img = {}
  
    for r in roomsData:
        if r.hotel.city == city:
            cityRoom.append(r)
            # fetch image names
            roomWise_img[r.id] = Hotel_S.getRoomImageName_list(r.images)

    return render_template('rooms.html', city=city, rooms = cityRoom, images = roomWise_img)

# Search route
@user.route('/search_rooms', methods = ['GET'])
def search_rooms():
    
    city = request.args.get('city')
    guest = request.args.get('guest')
    checkin = request.args.get('checkin')   # returns string
    checkout = request.args.get('checkout') # returns string

    # base query
    query = Rooms.query.join(Rooms.hotel)

    # city filter
    if city:
        query = query.filter(Hotels.city == city)

    # guest filter
    if guest:
        query = query.filter(Rooms.person_capacity >= int(guest))

    rooms = query.all()

    room_list = []
    roomwise_img = {}

    # date filter
    if checkin and checkout:
        checkin_date = datetime.strptime(checkin, '%Y-%m-%d').date()   # gives date formate
        checkout_date = datetime.strptime(checkout, '%Y-%m-%d').date() 

        for room in rooms:
            if Hotel_S.checkAvailability(room.id, room.category, checkin_date, checkout_date):

                room_list.append(room)
                # fetch rooms images
                roomwise_img[room.id] = Hotel_S.getRoomImageName_list(room.images)
    else:
        for room in rooms:
            room_list.append(room)
            # fetch rooms images
            roomwise_img[room.id] = Hotel_S.getRoomImageName_list(room.images)

    # current_date=date.isoformat() #gives date in yyyy-mm-dd formate in string
        
    return render_template('rooms.html', rooms = room_list, images = roomwise_img)

@user.route('/room/<int:rid>', methods = ['GET', 'POST'])
def room(rid):
    roomData = Hotel_S.getRoomById(rid)
    roomImages = roomData.images
    roomFacilities = roomData.facilities
    images = []
    facilities = []

    for img in roomImages:
        images.append(img.image)

    for f in roomFacilities:
        facilities.append(f.facility.name)

    if request.method == 'POST':

        checkin = datetime.strptime(
            request.form.get('checkin'), '%Y-%m-%d').date()
        checkout = datetime.strptime(
            request.form.get('checkout'), '%Y-%m-%d').date()

        if not(Hotel_S.checkAvailability(rid = rid, rcategory=roomData.category, checkin=checkin, checkout=checkout)):
            flash('Room is not Available in these dates!', 'flash-err')
            return render_template('detail-room.html', room = roomData, images = images, facilities = facilities)
        else:
            guest = request.form.get('person')
            total_priceForm = request.form.get('totalPrice')
            nights = (checkout - checkin).days
            totalPrice = nights * roomData.price_per_night

            if int(total_priceForm) != totalPrice:
                print('difference in total price')
            
            bookingData = {
                'checkin' : checkin,
                'checkout' : checkout,
                'guest' : guest,
                'nights' : nights,
                'totalPrice' : totalPrice
            }
            session['booking'] = bookingData
            session['rid'] = roomData.id

            return redirect(url_for('user.payment'))
    
    return render_template('detail-room.html', room = roomData, images = images, facilities = facilities)

@user.route('/payment')
@auth_required('user')
def payment():

    if 'rid' in session and 'booking' in session:
        room = Hotel_S.getRoomById(session['rid'])
        bookingData = session['booking']
    else:
        flash('rid and booking data not found','flash-err')

    return render_template('payment.html', room = room, booking = bookingData)
   








