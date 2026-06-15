from . import auth
from flask import flash, session, render_template, redirect, url_for, request, abort
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
# from .decorator import auth_required, login_required
from app.tasks import createMail
import os
from dotenv import load_dotenv
from app.extensions import socketio
import uuid
from app.extensions import cache
from flask_login import login_required, logout_user, login_user
from urllib.parse import urljoin, urlparse


load_dotenv()
sender_mail = os.getenv('MAIL_USERNAME')


UPLOAD_FOLDER = 'app/static/images'

# OTP Generator
def genrateOTP():
    return int(random.randint(100000, 999999))

# Register route
@auth.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()

    if request.method == 'GET':
        return render_template('register.html', form = form)

    if form.validate_on_submit():
        session['name'] = form.name.data
        session['email'] = form.email.data
        session['psw'] = generate_password_hash(form.password.data)
        session['role'] = form.identity.data

        f = form.image.data
        if f and f.filename != '':
            fname = secure_filename(f.filename)
            f.save(os.path.join(UPLOAD_FOLDER, fname))
            session['image'] = fname

        else:
            session['image'] = None
      
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

        createMail.delay(subject='OTP Verification', send=sender_mail, receiver=session['email'], content=f'Your OTP is {otp} from Hotel Booking Website to verify user.')

        return render_template('verify.html', form = form)

    elif session['email']:
        if form.validate_on_submit():
            otp = form.otp.data

            if session['otp'] == otp:
                session.pop('otp', None)

                # for forget password
                if 'forgetPsw' in session:
                    return redirect(url_for('auth.reset_password'))
                
                if session['image']:
                    
                    User_S.insertUser(name = session['name'], email = session['email'], image=session['image'], psw = session['psw'], role = session['role'])
                else:
                    User_S.insertUser(name = session['name'], email = session['email'], psw = session['psw'], role = session['role'])
                
                user = User_S.getUserByMail(session['email'])

                User_S.updateVerifyMail(user)

                socketio.emit('new_user_registered', user.name, to='super_admin')
                socketio.emit('update_admin_dashboard', to='super_admin')

                # remove cached data
                cache.delete('user_list')

                session.pop('name', None)
                session.pop('email', None)
                session.pop('psw', None)
                session.pop('role', None)

                flash('You Registered Successfully', 'flash-success')

                createMail.delay(subject='Registeration Success', send=sender_mail, receiver=session['email'], content=f'You are Registered successfully in Hotel Booking Website')

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


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    target_url = urlparse(urljoin(request.host_url, target))

    return (
        target_url.scheme in ['http', 'https'] and
        ref_url.netloc == target_url.netloc
    )

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

        if user:
            if check_password_hash(user.password, password):

                login_user(user)

                flash('Loged In.','flash-success')

                next_page = request.args.get('next')

                print(next_page)

                if next_page and not is_safe_url(next_page):  
                    abort(400)
                
                if next_page:
                    return redirect(next_page)

                if user.role == 'host':
                    return redirect(url_for('host.dashboard'))
                elif user.role == 'admin':
                    return redirect(url_for('admin_bp.dashboard'))
                else:
                    return redirect(url_for('user.home'))
            else:
                flash('Invalid Details', 'flash-err')
        else:
            flash('User not found!', 'flash-err')
        return render_template('login.html', form = form)
    else:
        return render_template('login.html', form = form)
    
# Logout
@auth.route('/logout')
@login_required
def logout():

    logout_user()

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
                return redirect(url_for('profile.view'))
                
        else: 
            flash('Invalid existing Password', 'flash-err')

    if 'forgetPsw' in session:
        return render_template('reset-password.html', forgetForm = forgetForm)
        
    return render_template('reset-password.html', resetForm = resetForm)