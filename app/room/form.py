from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FileField, RadioField, MultipleFileField
from wtforms.validators import Length, DataRequired, EqualTo, Regexp

class RoomForm(FlaskForm):
    category = StringField('Room Category', validators=[DataRequired('Required')])
    bedrooms = IntegerField('Total bedrooms', validators=[DataRequired('Required')])
    beds = IntegerField('Total beds', validators=[DataRequired('Required')])
    person_capacity = IntegerField('Total Guest Capacity', validators=[DataRequired('Required')])
    price_per_night = IntegerField('Price per Night', validators=[DataRequired('Required')])
    no_rooms = IntegerField('Total rooms', validators=[DataRequired('Required')])

    image = MultipleFileField('Room Images')
    
    
