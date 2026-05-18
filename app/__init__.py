from flask import Flask, has_request_context
# from flask_login import login_manager, login_user, logout_user,current_user
from config import Config
from .extensions import db, mail
from .auth import auth
from .admin import admin
from .host import host
from .hotel import hotel
from .user import user
from .room import room
from .profile import profile
from .booking import booking
from flask_migrate import Migrate
from flask import session
from .models import User_cred, Facilities
from celery import Celery, Task


def celery_init_app(app):
    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config['CELERY'])
    celery_app.set_default()
    app.extensions['celery'] = celery_app
    return celery_app


def create_app():
    app1 = Flask(__name__)

    # connect config
    app1.config.from_object(Config)

    # db.init
    db.init_app(app1)
    migrate = Migrate(app1, db)
    mail.init_app(app1)
    celery_init_app(app1)

    @app1.context_processor
    def inject_user():
        user = None
        # only access session during real HTTP request(to avoid error in celery)
        if has_request_context():

            if 'user_id' in session:
                user = User_cred.query.get(session['user_id'])

        return dict(current_user=user)
    
    @app1.context_processor
    def global_data():

        facility_name = []
        # only access session during real HTTP request(to avoid error in celery)
        if has_request_context():
            facilities = db.session.query(Facilities).all()

            for f in facilities:
                facility_name.append(f.name)

        return dict(global_facilities=facility_name)

    # Bluprints
    app1.register_blueprint(auth, url_prefix = '/auth')
    app1.register_blueprint(admin, url_prefix = '/admin')
    app1.register_blueprint(host, url_prefix='/host')
    app1.register_blueprint(hotel, url_prefix='/host/hotel')
    app1.register_blueprint(user)
    app1.register_blueprint(room, url_prefix = '/host/room')
    app1.register_blueprint(profile, url_prefix = '/profile')
    app1.register_blueprint(booking, url_prefix = '/booking')
    
    import app.models   # ✅ triggers all model imports
    import app.tasks

    return app1
