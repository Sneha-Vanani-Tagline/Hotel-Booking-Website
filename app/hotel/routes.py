from . import hotel
from flask import redirect, url_for, render_template, flash, session, request
from .form import HotelForm
import random
import os
from flask_mail import Message
from app import mail,db
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User_cred,Hotels, Rooms, Room_Image, Facilities, Room_facilities
import app.services.hotel_service as Hotel
import app.services.user_service as User
from app.auth.decorator import auth_required, login_required
from app.extensions import socketio

UPLOAD_FOLDER = 'app/static/images'

# Display list of hotel
@hotel.route('/list')
@auth_required('host')
def list():
    host = User.getUserById(session['user_id'])
    hotels = host.hotels
    
    return render_template('hotel.html', data = hotels)

@hotel.route('/edit/<int:id>', methods = ['GET', 'POST'])
@auth_required('host')
def editHotel(id):
    data = Hotel.getHotelDataById(id)
    form = HotelForm(obj = data)
    
    if form.validate_on_submit():
        name = form.name.data
        desc = form.description.data
        type = form.type.data
        city = form.city.data.lower()
        location = form.location.data
        images = form.images.data       #this gives file object

        result = check_data_changes(name,desc,type, city, location, images, data)

        if result:
            if 'image' in result:
                # image = result['image']       #this gives string, so not using this varialble to store image
                fname = secure_filename(images.filename)
                images.save(os.path.join(UPLOAD_FOLDER, fname))
            
            Hotel.updateHotelData(id, result)

            flash('Hotel Edited Successfully', 'flash-success')
            return redirect(url_for('hotel.list'))
        else:
            flash('No changes found!', 'flash-warn')
    
    return render_template('hotel_form.html', form = form, action='Edit', submit = 'Update', hotelImage = data.images)

# deletes hotel
@hotel.route('/delete/<int:id>')
@auth_required('host')
def deleteHotel(id):
    Hotel.deleteHotel(id)
    flash('Hotel Deleted', 'flash-success')
    return redirect(url_for('hotel.list'))

# Adds New Hotel
@hotel.route('/add', methods = ['GET', 'POST'])
@auth_required('host')
def addHotel():
    form = HotelForm()

    if request.method == 'GET':
        return render_template('hotel_form.html', form = form, action='Add', submit = 'Add')
    
    if form.validate_on_submit():
        host = User.getUserByMail(session['email'])

        name = form.name.data
        desc = form.description.data
        type = form.type.data
        city = form.city.data.lower()
        location = form.location.data

        img = form.images.data
        
        if img and img.filename != '':
            fname = secure_filename(img.filename)
            img.save(os.path.join(UPLOAD_FOLDER, fname))
            Hotel.createHotel(name= name, description=desc, type=type, city=city, location=location, images=fname, host_id = host.id)
        else:
            Hotel.createHotel(name= name, description=desc, type=type, city=city, location=location, host_id = host.id)
        
        socketio.emit('update_admin_dashboard', to='super_admin')
        
        flash('Hotel Added Successfully', 'flash-success')
        return redirect(url_for('hotel.list'))
    else:
        flash('Invalid Details', 'flash-err')
        return render_template('hotel_form.html', form = form, action='Add', submit = 'Add')


# check updates for edit hotel
def check_data_changes(name, desc, type, city, location, image, hotelData):
    changeFlag = False
    changed = {}

    if name and name != hotelData.name:
        changed['name'] = name
        changeFlag = True

    if desc and desc != hotelData.description:
        changed['desc'] = desc
        changeFlag = True

    if type and type != hotelData.type:
        changed['type'] = type
        changeFlag = True

    if city and city.lower() != hotelData.city.lower():
        changed['city'] = city.lower()
        changeFlag = True

    if location and location != hotelData.location:
        changed['location'] = location
        changeFlag = True

    if image and image.filename != '' and image != hotelData.images:
        changed['image'] = image.filename
        changeFlag = True

    if changeFlag:
        return changed
    else:
        return changeFlag
