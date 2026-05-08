from . import auth
from flask import flash, session, render_template, redirect, url_for, request
from app.auth.forms import RegistrationForm, LoginForm, VerifyOTPForm, ResetPassForm, ForgetPassResetForm
import random
import os
from flask_mail import Message
from app import mail,db
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User_cred
import app.services.hotel_service as Hotel_S
import app.services.user_service as User_S
from .decorator import auth_required, login_required

UPLOAD_FOLDER = 'app/static/images'

# OTP Generator
def genrateOTP():
    return int(random.randint(100000, 999999))

# Mail Creation and sending
def createMail(send, receiver, subject, content):
    msg = Message(subject, sender=send, recipients=[receiver])
    msg.body = content
    mail.send(msg)

# Register route
@auth.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()

    if request.method == 'GET':
        return render_template('register.html', form = form)

    if form.validate_on_submit():
        name = form.name.data.lower()
        email = form.email.data
        psw = generate_password_hash(form.password.data)
        role = form.identity.data

        session['email'] = email

        f = form.image.data
        if f and f.filename != '':
            fname = secure_filename(f.filename)
            f.save(os.path.join(UPLOAD_FOLDER, fname))
            User_S.insertUser(name=name, email = email, image=fname, psw = psw, role = role)
        else:
            User_S.insertUser(name=name, email = email, psw = psw, role = role)
        # print(name, email, psw, role)
        return redirect(url_for('auth.verify'))
    else:
        flash('Invalid details or Missing fields', 'flash-err')
        return render_template('register.html', form = form)
    

# Verify OTP route
@auth.route('/verify', methods = ['GET', 'POST'])
def verify():
    form = VerifyOTPForm()

    if request.method == 'GET':
        otp = genrateOTP()
        session['otp'] = otp

        createMail(subject='OTP Verification', send='svn@taglineinfotech.com', receiver=session['email'], content=f'Your OTP is {otp} from Hotel Booking Website to verify user.')

        return render_template('verify.html', form = form)

    elif session['email']:
        if form.validate_on_submit():
            otp = form.otp.data

            if session['otp'] == otp:
                session.pop('otp', None)
                user = User_S.getUserByMail(session['email'])

                # for forget password
                if 'forgetPsw' in session:
                    return redirect(url_for('auth.reset_password'))

                User_S.updateVerifyMail(user)
                
                flash('You Registered Successfully', 'flash-success')

                createMail(subject='Registeration Success', send='svn@taglineinfotech.com', receiver=session['email'], content=f'You are Registered successfully in Hotel Booking Website')

                return redirect(url_for('auth.login'))
            else:
                flash('Wrong OTP', 'flash-err')
                return render_template('verify.html', form = form)
        else:
            flash('Invalid details', 'flash-err')
            return render_template('verify.html', form = form)
    else:
        flash('Please Login first', 'flash-err')
        return redirect(url_for('auth.login'))

# Login route
@auth.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'GET':
        return render_template('login.html', form = form)
    
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        user = User_S.getUserByMail(email)

        if check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['email'] = user.email
            session['role'] = user.role

            flash('Loged In.','flash-success')

            if user.role == 'host':
                return redirect(url_for('host.dashboard'))
            elif user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('profile.view', id = user.id))
        else:
            flash('Invalid Details', 'flash-err')
            return render_template('login.html', form = form)
    else:
        return render_template('login.html', form = form)
    
# Logout
@auth.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    session.pop('email', None)
    session.pop('role', None)
    return redirect(url_for('auth.login'))

# Forget Password
@auth.route('/forget-password', methods = ['GET', 'POST'])
def forget_password():

    if request.method == 'POST':
        mail = request.form.get('email')
        user = User_S.getUserByMail(mail)

        if user:
            session['email'] = mail
            session['forgetPsw'] = True
            return redirect(url_for('auth.verify'))
        else:
            flash('Invalid Detail!', 'flash-err')
        
    return render_template('forget-password.html')

# Reset Password
@auth.route('/reset-password', methods = ['POST', 'GET'])
def reset_password():
    resetForm = ResetPassForm()
    forgetForm = ForgetPassResetForm()

     # Forget Password reset
    if forgetForm.validate_on_submit():
  
        new_pass = forgetForm.new_pass.data
        user = User_S.getUserByMail(session['email'])
       
        if 'forgetPsw' in session:
            # print('in forgot password reset', user.id)
            session.pop('forgetPsw', None)

            if User_S.resetPass(uid=user.id, new=generate_password_hash(new_pass)):
                flash('Password Changed Successfully!', 'flash-success')
                return redirect(url_for('auth.login'))
            else:
                flash('User not found!', 'flash-err')
                return render_template('reset-password.html', forgetForm = forgetForm)


    # Reset Password
    if resetForm.validate_on_submit():
        exsiting_pass = resetForm.existing_pass.data
        new_pass = forgetForm.new_pass.data

        user = User_S.getUserByMail(session['email'])

        if check_password_hash(user.password, exsiting_pass):
            if User_S.resetPass(uid=user.id, new=generate_password_hash(new_pass)):
                flash('Password Changed Successfully!', 'flash-success')
                return redirect(url_for('profile.view', id = user.id))
                
        else: 
            flash('Invalid existing Password', 'flash-err')

    if 'forgetPsw' in session:
        return render_template('reset-password.html', forgetForm = forgetForm)
        
    return render_template('reset-password.html', resetForm = resetForm)