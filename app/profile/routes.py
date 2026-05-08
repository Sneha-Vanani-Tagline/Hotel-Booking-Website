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

    if request.method == 'GET':
        return render_template('edit-user.html', form = form, data=user)
    
    if form.validate_on_submit():
        name = form.name.data
        image = form.image.data

        # print(user.id)
        if image and image.filename != '':
            fname = secure_filename(image.filename)
            image.save(os.path.join(UPLOAD_FOLDER, fname))
            UserS.updateUser(name=name, image=fname, id=id)
            flash('Details Updated', 'flash-success')
        else:
            UserS.updateUser(name=name, id=id)
            flash('Details Updated', 'flash-success')
        return redirect(url_for('profile.view', id = id))
    else:
        return render_template('edit-user.html', form = form, data=user)