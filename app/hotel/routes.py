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

UPLOAD_FOLDER = 'app/static/images'

# Display list of hotel
@hotel.route('/list')
@auth_required('host')
def list():
    data = Hotel.getHotelsData()
    return render_template('hotel.html', data = data)

@hotel.route('/edit/<int:id>', methods = ['GET', 'POST'])
@auth_required('host')
def editHotel(id):
    data = Hotel.getHotelDataById(id)
    form = HotelForm(obj = data)

    if request.method == 'GET':

        return render_template('hotel_form.html', form = form, action='Edit', submit = 'Update')
    
    if form.validate_on_submit():
        name = form.name.data
        desc = form.description.data
        type = form.type.data
        city = form.city.data
        location = form.location.data
        images = form.images.data
        rooms = form.total_rooms.data

        if images and images.filename != '':
            fname = secure_filename(images.filename)
            images.save(os.path.join(UPLOAD_FOLDER, fname))
            Hotel.updateData(id= id,name=name, description=desc, type=type, city=city, location=location, images=fname, rooms=rooms)
        else:
            Hotel.updateData(id=id, name=name, description=desc, type=type, city=city, location=location, rooms=rooms)
        return redirect(url_for('hotel.list'))

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
        city = form.city.data
        location = form.location.data
        rooms = form.total_rooms.data

        img = form.images.data
        print(img)
        if img and img.filename != '':
            fname = secure_filename(img.filename)
            img.save(os.path.join(UPLOAD_FOLDER, fname))
            Hotel.createHotel(name= name, description=desc, type=type, city=city, location=location, images=fname, rooms=rooms, host_id = host.id)
        else:
            Hotel.createHotel(name= name, description=desc, type=type, city=city, location=location, rooms=rooms, host_id = host.id)
        flash('Hotel Added Successfully', 'flash-success')
        return redirect(url_for('hotel.list'))
    else:
        flash('Invalid Details', 'flash-err')
        return render_template('hotel_form.html', form = form, action='Add', submit = 'Add')

# need check again
@hotel.route('/view/<int:id>')
def view(id):
    hotelData = Hotel.getHotelDataById(id)
    rooms = Hotel.getRoomsByHotelId(id)

    return render_template('hotel-view.html', hotel = hotelData, rooms = rooms)


