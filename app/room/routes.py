from . import room
from flask import redirect, url_for, render_template, flash, session, request
from .form import RoomForm
import os
from flask_mail import Message
from app import mail,db
from werkzeug.utils import secure_filename
from app.models import User_cred,Hotels, Rooms, Room_Image, Facilities, Room_facilities
import app.services.hotel_service as HotelS
import app.services.user_service as UserS
from app.auth.decorator import auth_required, login_required


UPLOAD_FOLDER = 'app/static/images/rooms/'

def authenticate():
    if session.get('email', None) != None:
        return True
    else:
        return False

@room.route('/roomlist')
@auth_required('host')
def roomlist():
    if authenticate():
        hotelData = HotelS.getHotelsData()
        rooms = HotelS.getAllRooms()
        facility = HotelS.getAllFacility()
        rImages = HotelS.getAllRoomImages()
        rFacility = HotelS.getAllRoomFacility()

        return render_template('room-list.html', hotel = hotelData, room = rooms, facility = facility, images = rImages, rfacility = rFacility)

    else:
        flash('Access Denied', 'flash-err')
        return redirect(url_for('auth.login'))
    
@room.route('/add/<int:hid>', methods = ['GET', 'POST'])
@auth_required('host')
def add(hid):
    form = RoomForm()
    hotelData = HotelS.getHotelsData()
    facility = HotelS.getAllFacility()

    if form.validate_on_submit():
        category = form.category.data
        bedrooms = form.bedrooms.data
        beds = form.beds.data
        person = form.person_capacity.data
        price = form.price_per_night.data
        rooms = form.no_rooms.data
        images = []

        if form.image.data:
            for i in form.image.data:
                f = secure_filename(i.filename)
                i.save(os.path.join(UPLOAD_FOLDER, f))
                images.append(f)
            
        facility = request.form.getlist('facility')
        HotelS.addRoom(category=category, bedrooms=bedrooms, beds=beds, person=person, price=price, rooms=rooms, hid=hid, images=images, facility = facility)
        
        flash('New Room Added', 'flash-success')
        return redirect(url_for('room.roomlist'))

    elif request.method == 'GET':
        return render_template('room-form.html', form = form, hotel = hotelData, facility = facility, action='Add', submit='Add')
    
@room.route('/edit/<int:rid>', methods = ['GET', 'POST'])
@auth_required('host')
def edit(rid):
    roomData = HotelS.getRoomById(rid)
    form = RoomForm(obj = roomData)
    facility = HotelS.getAllFacility()
    currentFacility = HotelS.getRoomFacilityByRoomId(rid)
    roomImages = HotelS.getRoomImageById(rid)

    cFacilityId = []
    for f in currentFacility:
        cFacilityId.append(f.facility_id)

    cImagesName = []
    for i in roomImages:
        cImagesName.append(i.image)

    if form.validate_on_submit():
        category = form.category.data
        bedrooms = form.bedrooms.data
        beds = form.beds.data
        person = form.person_capacity.data
        price = form.price_per_night.data
        rooms = form.no_rooms.data
        images = []

        
        for i in form.image.data:
            if i and i.filename != '':
                f = secure_filename(i.filename)
                
                # file = UPLOAD_FOLDER + f
                # print(os.path.isfile(file))       # to check is it file or not
                i.save(os.path.join(UPLOAD_FOLDER, f))
                images.append(f)

        # print('images in route : ',images)
        deleteImages = request.form.getlist('delete_images')
            
        facility = request.form.getlist('facility')
   
        updatedData = checkUpdate(roomData, cFacilityId, cImagesName, category=category, bedrooms=bedrooms, beds=beds, person_capacity=person, price_per_night=price, no_rooms=rooms, images=images, facility = facility)
        HotelS.editRoom(rid,deleteImages, updatedData)

        flash('Room Updated', 'flash-succcess')
        return redirect(url_for('room.roomlist'))

    elif request.method == 'GET':
        return render_template('room-form.html',form=form, roomImages=roomImages, facility = facility, currentFacility=cFacilityId, action='Edit', submit='Update')
    
@room.route('/delete/<int:rid>')
@auth_required('host')
def delete(rid):
    HotelS.deleteRoomById(id)
    flash('Room Deleted', 'flash-warn')
    return redirect(url_for('room.roomlist'))

# edit same data validation
def checkUpdate(existingRoomData, existingFacilityId, existingImagesName, **newData):
    updatedFields = {}
    updateFlag = False

    # Rooms table fields
    if existingRoomData.category != newData['category']:
        updatedFields['category'] = newData['category']
        updateFlag = True

    if existingRoomData.bedrooms != newData['bedrooms']:
        updatedFields['bedrooms'] = newData['bedrooms']
        updateFlag = True

    if existingRoomData.beds != newData['beds']:
        updatedFields['beds'] = newData['beds']
        updateFlag = True

    if existingRoomData.person_capacity != newData['person_capacity']:
        updatedFields['person_capacity'] = newData['person_capacity']
        updateFlag = True

    if existingRoomData.price_per_night != newData['price_per_night']:
        updatedFields['price_per_night'] = newData['price_per_night']
        updateFlag = True

    if existingRoomData.no_rooms != newData['no_rooms']:
        updatedFields['no_rooms'] = newData['no_rooms']
        updateFlag = True

    # Room Images table 
    if existingImagesName != newData['images']:
        updatedFields['images'] = newData['images']
        updateFlag = True

    # Room facilities table 
    if existingFacilityId != newData['facility']:
        # getlist() gives as a string, so we have to convert it into a integer
        updatedFields['facility'] = list(map(int, newData['facility']))
        updateFlag = True

    if updateFlag == False:
        flash('Please change the details first!', 'flash-err')
    else:
        return updatedFields

