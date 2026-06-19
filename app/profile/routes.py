from . import profile
from .form import UserForm
from flask import request, redirect, url_for, render_template, flash, session
import os
from werkzeug.utils import secure_filename
import app.services.hotel_service as HotelS
import app.services.user_service as UserS
from app.auth.decorator import auth_required
from flask_login import current_user

UPLOAD_FOLDER = 'app/static/images/'

@profile.route('/')
@auth_required('user', 'host')
def view():

    return render_template('profile.html', data = current_user)

@profile.route('/edit', methods = ['GET', 'POST'])
@auth_required('user', 'host')
def edit():

    form = UserForm(obj = current_user)
    
    if form.validate_on_submit():
        name = form.name.data
        image = form.image.data

        result = check_profile_changes(name, image, current_user)

        if result:
                UserS.updateUser(result, current_user.id)
                flash('Details Updated', 'flash-success')
                return redirect(url_for('profile.view'))
        else:
            flash('No changes found!', 'flash-warn')
            return render_template('edit-user.html', form = form, data=current_user,userImage=current_user.image)
    
    return render_template('edit-user.html', form = form, data=current_user, userImage=current_user.image)
    
def check_profile_changes(name, image, userData):
    changeFlag = False
    changed = {}

    if name and name != userData.name:
        changed['name'] = name
        changeFlag = True

    if image and image.filename != '' and image != userData.image:
        
        fname = secure_filename(image.filename)
        image.save(os.path.join(UPLOAD_FOLDER, fname))
        changed['image'] = fname
        changeFlag = True

    if changeFlag:
        return changed
    else:
        return changeFlag