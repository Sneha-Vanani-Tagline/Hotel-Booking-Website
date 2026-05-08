from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import DataRequired, ReadOnly

class UserForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired('Required')])
    email = StringField('Email', validators=[DataRequired('Required'), ReadOnly()])
    image = FileField('Image')

    submit = SubmitField('Save')

    