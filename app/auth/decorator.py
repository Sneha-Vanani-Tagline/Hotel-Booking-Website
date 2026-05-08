from functools import wraps
from app.models import User_cred
from flask import session, url_for, redirect, render_template

def auth_required(*role):
    def wrapper(func):
        @wraps(func)        # this prevents to change the calling function name to wrapper function(remains the orginial name)
        def check_authentication_role(*args, **kwargs):
            if 'user_id' not in session:
                return render_template('unathourize.html')
            
            if role:
                user = User_cred.query.get(session['user_id'])
                if user.role not in role:
                    return 'Access Denied!'
            return func(*args, **kwargs)
        return check_authentication_role
    return wrapper

def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'user_id' not in session:
            return render_template('unathourize.html')
        return func(*args, **kwargs)
    return inner
