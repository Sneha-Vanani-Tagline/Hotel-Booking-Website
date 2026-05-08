from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, FileField, RadioField
from wtforms.validators import Length, DataRequired, Email, EqualTo, Regexp

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired('Name Required')])
    email = StringField('Email', validators=[DataRequired('email Required'), Email('Invalid Email')])
    # mno = StringField('Mobile No.', validators=[DataRequired('Mobile Number Required'), Regexp(r'^[6-9]\d{9}$', message='Invalid Mobile Number')])
    image = FileField('Profile Image')
    password = PasswordField('Password', validators=[DataRequired('Password required'), Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*]).{6,}$', message='Password must contain a Lowercase, an Uppercase, a digit, and a speacial char.')])
    cfmpsw = PasswordField('Confirm Password', validators=[DataRequired('Password required'), EqualTo('password', message='Password must match.')])
    identity = RadioField('Register As', choices = [('user', 'As a User'), ('host', 'As a Hotel Host')], validators = [DataRequired(message='Please select one option.')])

    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Username', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators= [DataRequired(), Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*]).{6,}$', message='Invalid Password.')])

    submit = SubmitField('Login')

class VerifyOTPForm(FlaskForm):
    otp = IntegerField('OTP', validators=[DataRequired('Required')])
    
    submit = SubmitField('Verify')

class ResetPassForm(FlaskForm):
    existing_pass = PasswordField('Existing Password', validators= [DataRequired(), Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*]).{6,}$', message='Invalid Password.')])
    new_pass = PasswordField('New Password', validators= [DataRequired(), Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*]).{6,}$', message='Invalid Password.')])
    confirm_pass = PasswordField('Confirm Password', validators= [DataRequired(), EqualTo('new_pass', message='Password must match!')])

    submit = SubmitField('Reset')

class ForgetPassResetForm(FlaskForm):
    new_pass = PasswordField('New Password', validators= [DataRequired(), Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*]).{6,}$', message='Invalid Password.')])
    confirm_pass = PasswordField('Confirm Password', validators= [DataRequired(), EqualTo('new_pass', message='Password must match!')])

    submit = SubmitField('Reset')