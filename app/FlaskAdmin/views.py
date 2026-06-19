from flask_admin import expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import render_template, url_for, current_app, jsonify
from flask_login import current_user
from wtforms import PasswordField, SelectField, StringField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash
from app.models.user import User_cred
from app.models.facility import Facilities
from app.models.rooms import Room_Image, Rooms
from markupsafe import Markup 
from flask_admin.form import ImageUploadField
import os
from wtforms import Field, MultipleFileField
from markupsafe import Markup
from flask import url_for
import uuid
from werkzeug.utils import secure_filename
# from app.extensions import flaskAdmin
from app.admin import admin_bp



class ImageLinkWidget:
    def __call__(self, field, **kwargs):
        if field.data:
            img_url = url_for('static', filename=f'images/{field.data}')
            return Markup(
                f'<div class="form-control-static">'
                f'  <a href="{img_url}" target="_blank">{field.data}</a>'
                f'</div>'
            )
        return Markup('<div class="form-control-static text-muted">No image set.</div>')

class ImageLinkField(Field):
    widget = ImageLinkWidget()

    def process_formdata(self, valuelist):
        pass  # read-only

    def _value(self):
        return self.data or ''

class SecureAdmin:
    def is_accessible(self):
        
        return (
            current_user.is_authenticated and
            current_user.role == 'admin'
        )
    
    def inaccessible_callback(self, name, **kwargs):
        return render_template('admin/inAccessible.html')


class MyIndexView(SecureAdmin, AdminIndexView):

    @expose('/')
    def index(self):
        return self.render('admin/index.html')
    
    
class UserView(SecureAdmin, ModelView):

    column_exclude_list = ['password']

    # file_path = os.path.join(current_app.root_path, 'static', 'images')           """this needs the app context"""
    file_path = os.path.join(
        os.path.dirname( os.path.dirname(__file__)),
        'static', 'images')
    
    # Extra fields in form
    form_extra_fields = {
        'new_role' : SelectField(
            'Role',
            validators=[DataRequired()],
            choices=[
                ('host', 'Host'),
                ('user', 'User')
            ]
        ),
        'new_image_path' : ImageUploadField(
            label='New Image',
            base_path=file_path,
            # thumbnail_size=(100, 100, True)           # it stores the imageName_thumb.png file also, means saves two times one the actual image and another thumbnail size image
        ),
        'current_image' : ImageLinkField('Current Image')
    }

    # Form Columns
    form_columns = [
        'name', 
        'email',          
        'new_role',
        'current_image',          # shows clickable link
        'new_image_path',         # new image upload field
        'password'
    ]

    # called when edit form request comes
    def edit_form(self, obj=None):          # obj has the current user object
        form = super().edit_form(obj)      # Calls the super (base) class's edit_form()
        if obj and obj.image:
            form.current_image.data = obj.image

        return form


    # Changes in list view
    def _make_image_path(view, context, model, name):
        if not model.image:
            return ''

        img_url = url_for('static', filename = f'images/{model.image}')

        return Markup(f'<a href="{img_url}" target = "_blank">{model.image} </a>')


    column_formatters = {
        'image' : _make_image_path
    }

    def on_model_change(self, form, model, is_created):

        """print(os.path.dirname(__file__))
        # => /Users/mac/Desktop/Hotel Management Project/app/FlaskAdmin"""

        """print(current_app.root_path)
        # => /Users/mac/Desktop/Hotel Management Project/app"""

        if form.password:
            model.password = generate_password_hash(form.password.data)

        if form.new_role.data:
            model.role = form.new_role.data

        if form.new_image_path.data:
            file = form.new_image_path.data
            fname = secure_filename(file.filename)

            model.image = fname

@admin_bp.route('/hotel-rooms/<int:hid>')
def getHotelRooms(hid):
    rooms = Rooms.query.filter_by(hotel_id = hid).all()

    room_json = []

    for r in rooms:
        room_json.append({
            
            'id' : r.id,
            'category' : r.category
        })

    return jsonify(room_json)


class BookingView(SecureAdmin, ModelView):
    
    # display only selected hotel's rooms
    def create_form(self, obj = None):
        form =  super().create_form(obj)
    
        del form.cancel_reason
        del form.cancelled_by
        del form.cancelled_at
        del form.status
        del form.booking_date

        form.user.query = User_cred.query.filter_by(role = 'user').all()
        
        self.extra_js = ['/static/js/flask_admin.js']

        return form
    
    def edit_form(self, obj = None):                                                                    
        form =  super().edit_form(obj)     

        form.user.query = User_cred.query.filter_by(role = 'user').all()

        hotel = form.hotel.data
        form.rooms.query = Rooms.query.filter_by(hotel_id = hotel.id).all()

        self.extra_js = ['/static/js/flask_admin.js']
        return form                                                         


class HotelView(SecureAdmin, ModelView):

    file_path = os.path.join(
        os.path.dirname(
            os.path.dirname(__file__)
        ),
        'static', 'images'
    )

    form_excluded_columns = ['conversations']

    form_extra_fields = {
        'new_image_path' : ImageUploadField(
            label='New Image',
            base_path=file_path
        ),
        'current_image' : ImageLinkField('Existing Image')
    }

    form_columns = [
        'name',
        'description',
        'type',
        'rooms',
        'city',
        'location',
        'current_image',
        'new_image_path',
        'host',
        'bookings'
    ]

    def _make_image_path(view, context, model, name):
        if not model.images:
            return ''
        
        img_url = url_for('static', filename = f'images/{model.images}')

        return Markup(f'<a href={img_url} target="_blank">{model.images}</a>')

    # Changes the form data formate
    form_args = {
        'host' : {
            'query_factory' : lambda: User_cred.query.filter_by(role = 'host').all()
        }
    }

    column_formatters = {
        'images' : _make_image_path
    }

    def edit_form(self, obj = None):
        form =  super().edit_form(obj)

        if obj and obj.images:
            form.current_image.data = obj.images

        return form
    
    def create_form(self, obj = None):
        form = super().create_form(obj)

        del form.bookings

        return form
    
    def on_model_change(self, form, model, is_created):
        
        if form.new_image_path.data:
            file = form.new_image_path.data
            model.images = secure_filename(file.filename)


class RoomView(SecureAdmin, ModelView):
    
    file_path = os.path.join(
        os.path.dirname( os.path.dirname(__file__)),
        'static', 'images', 'rooms'
    )

    form_extra_fields = {
        
        'new_image_path' : MultipleFileField('New Image')
    }

    form_columns = [
        'category',
        'bedrooms',
        'beds',
        'facilities',
        'person_capacity',
        'price_per_night',
        'no_rooms',
        'images',
        'new_image_path',
        'hotel'
    ]

    column_list = [

        'category',
        'bedrooms',
        'beds',
        'person_capacity',
        'price_per_night',
        'no_rooms',
        'images',
        'facilities',
        'hotel'
    ]

    def _make_image_path(view, context, model, name):
        if not model.images:
            return ''
        
        html = ''
        for img in model.images:

            img_url = url_for('static', filename = f'images/rooms/{img}')
            html += f'<a href={img_url} target="_blank">{img}</a> <br>'

        return Markup(html)
    

    column_formatters = {
        'images' : _make_image_path
    }


    def on_model_change(self, form, model, is_created):

        if form.new_image_path.data:
            files = form.new_image_path.data

            for f in files:
                if not f or not f.filename:
                    continue

                fname = secure_filename(f.filename)
              
                obj = Room_Image(image = fname)

                model.images.append(obj)

class AuditLogView(SecureAdmin, ModelView):
    pass
