from functools import wraps
from app.models import User_cred
from flask import session, url_for, redirect, render_template, request
from flask_login import current_user


def auth_required(*role):
    def wrapper(func):
        @wraps(func)        # this prevents to change the calling function name to wrapper function(remains the orginial name)
        
        def check_authentication_role(*args, **kwargs):

            if not current_user.is_authenticated:
                return redirect(url_for('auth.login', next = request.url))
                # return render_template('unathourize.html')
            
            if role and current_user.role not in role:
                
                return 'Access Denied!', 403
                
            return func(*args, **kwargs)
        
        return check_authentication_role
    
    return wrapper
