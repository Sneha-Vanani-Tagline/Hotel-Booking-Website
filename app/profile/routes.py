from . import profile
from .form import UserForm
from flask import request, redirect, url_for, render_template, flash, session
import os
from werkzeug.utils import secure_filename
import app.services.hotel_service as HotelS
import app.services.user_service as UserS
from app.auth.decorator import auth_required, login_required

UPLOAD_FOLDER = 'app/static/images/'

@profile.route('/<int:id>')
@auth_required('user', 'host')
def view(id):
    user = UserS.getUserById(id)
    return render_template('profile.html', data = user)

@profile.route('/edit/<int:id>', methods = ['GET', 'POST'])
@auth_required('user', 'host')
def edit(id):
    user = UserS.getUserById(id)
    form = UserForm(obj = user)
    
    if form.validate_on_submit():
        name = form.name.data
        image = form.image.data

        result = check_profile_changes(name, image, user)

        if result:
                UserS.updateUser(result, id)
                flash('Details Updated', 'flash-success')
                return redirect(url_for('profile.view', id = id))
        else:
            flash('No changes found!', 'flash-warn')
            return render_template('edit-user.html', form = form, data=user,userImage=user.image)
    
    return render_template('edit-user.html', form = form, data=user, userImage=user.image)
    
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