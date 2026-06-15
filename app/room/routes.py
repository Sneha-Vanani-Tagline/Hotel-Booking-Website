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
from app.auth.decorator import auth_required
from app.extensions import cache
from flask_login import current_user

UPLOAD_FOLDER = 'app/static/images/rooms/'

@room.route('/roomlist')
@auth_required('host')
@cache.cached(100, key_prefix='room_list')
def roomlist():
    
    hotelData = current_user.hotels

    return render_template('room-list.html', hotel = hotelData)

    
@room.route('/add/<int:hid>', methods = ['GET', 'POST'])
@auth_required('host')
def add(hid):
    form = RoomForm()
    hotelData = HotelS.getAllHotels()
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
        
        cache.delete('room-list')
        flash('New Room Added', 'flash-success')
        return redirect(url_for('room.roomlist'))

    return render_template('room-form.html', form = form, hotel = hotelData, facility = facility, action='Add', submit='Add')
    
@room.route('/edit/<int:rid>', methods = ['GET', 'POST'])
@auth_required('host')
def edit(rid):
    roomData = HotelS.getRoomById(rid)
    form = RoomForm(obj = roomData)
    allFacility = HotelS.getAllFacility()
    currentFacility = roomData.facilities
    roomImages = roomData.images

    cFacilityId = []
    for f in currentFacility:
        cFacilityId.append(f.facility_id)

    cImagesName = []
    for i in roomImages:
        cImagesName.append(i.image)

    if form.validate_on_submit():
        category = form.category.data
        bedrooms = int(form.bedrooms.data)
        beds = int(form.beds.data)
        person = int(form.person_capacity.data)
        price = int(form.price_per_night.data)
        rooms = int(form.no_rooms.data)
        images = form.image.data

        deleteImagesId = request.form.getlist('delete_images')
        newFacility = request.form.getlist('facility')
        newFacility = list(map(int, newFacility))
        print('new facility: ', newFacility)

        updatedData = checkUpdate(roomData, cFacilityId, cImagesName, category=category, bedrooms=bedrooms, beds=beds, person_capacity=person, price_per_night=price, no_rooms=rooms, images=images, facility = newFacility, deleteImages = deleteImagesId)
        print('Changed room data ',updatedData)

        if updatedData:
          
            HotelS.editRoom(rid, updatedData)

            cache.delete('room-list')
            flash('Room Updated', 'flash-success')
            return redirect(url_for('room.roomlist'))
        else:
            flash('No changes found!', 'flash-warn')

    return render_template('room-form.html',form=form, roomImages=roomImages, facility = allFacility, currentFacility=cFacilityId, action='Edit', submit='Update')
    
@room.route('/delete/<int:rid>')
@auth_required('host')
def delete(rid):
    HotelS.deleteRoomById(id)

    cache.delete('room-list')

    flash('Room Deleted', 'flash-warn')
    return redirect(url_for('room.roomlist'))

# edit same data validation
def checkUpdate(existingRoomData, existingFacilityId, existingImagesName, category, bedrooms, beds, person_capacity, price_per_night, no_rooms, images, facility, deleteImages):
    updatedFields = {}
    newImg = []
    newFacility = []
    updateFlag = False

    # Rooms table fields
    if existingRoomData.category != category:
        updatedFields['category'] = category
        updateFlag = True

    if existingRoomData.bedrooms != bedrooms:
        updatedFields['bedrooms'] = bedrooms
        updateFlag = True

    if existingRoomData.beds != beds:
        updatedFields['beds'] = beds
        updateFlag = True

    if existingRoomData.person_capacity != person_capacity:
        updatedFields['person_capacity'] = person_capacity
        updateFlag = True

    if existingRoomData.price_per_night != price_per_night:
        updatedFields['price_per_night'] = price_per_night
        updateFlag = True

    if existingRoomData.no_rooms != no_rooms:
        updatedFields['no_rooms'] = no_rooms
        updateFlag = True

    # Room Images
    if images:
        for img in images:
            imgName = img.filename
            if imgName != '' and (imgName not in existingImagesName):
                print(existingImagesName)
                f = secure_filename(imgName)
                img.save(os.path.join(UPLOAD_FOLDER, f))
                newImg.append(imgName)
                updateFlag = True
    
    if newImg:
        updatedFields['newImages'] = newImg
        
    if deleteImages:
        updatedFields['deleteImages'] = deleteImages
        updateFlag = True

    # Room facilities
    addId = list(set(facility) - set(existingFacilityId))
    removeId = list(set(existingFacilityId) - set(facility))
                
    if addId:  
        updateFlag = True
        updatedFields['newFacilities'] = addId

    if removeId:
        updateFlag = True
        updatedFields['deleteFacilities'] = removeId
        

    if updateFlag == False:
        return False
    else:
        return updatedFields

