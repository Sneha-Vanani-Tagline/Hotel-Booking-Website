from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FileField, RadioField
from wtforms.validators import Length, DataRequired, EqualTo, Regexp

class HotelForm(FlaskForm):
    name = StringField('Hotel Name', validators=[DataRequired('Required')])
    type = StringField('Hotel Type', validators=[DataRequired('Required'), Length(max=50)])
    description = StringField('Hotel Description', validators=[DataRequired('Required'), Length(max=500)])
    total_rooms = IntegerField('No. of Rooms', validators=[DataRequired('Required')])
    images = FileField('Hotel Image')
    location = StringField('Address', validators=[DataRequired('Required'), Length(max=200)])
    city = StringField('City', validators=[DataRequired('Required'), Length(max=50)])

   
    
    