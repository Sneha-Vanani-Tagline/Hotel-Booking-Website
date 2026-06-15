from flask import Flask, has_request_context
from flask_admin.theme import Bootstrap4Theme
# from flask_login import login_manager, login_user, logout_user,current_user
from config import Config
from .extensions import db, mail, socketio, cache, flaskAdmin, login_manager
from .auth import auth
from .admin import admin_bp
from .host import host
from .hotel import hotel
from .user import user
from .room import room
from .profile import profile
from .booking import booking
from .chat import chat
from flask_migrate import Migrate
from flask import session
from .models import User_cred, Facilities, Bookings, Hotels, Rooms
from celery import Celery, Task
from flask_socketio import SocketIO
from .FlaskAdmin import init_admin
from .FlaskAdmin.views import MyIndexView


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

    # Initialization
    db.init_app(app1)
    migrate = Migrate(app1, db)
    mail.init_app(app1)
    celery_init_app(app1)
    socketio.init_app(app1, cors_allowed_origins="*")
    cache.init_app(app1)
    flaskAdmin.init_app(
        app1,
        index_view=MyIndexView()
    )
    login_manager.init_app(app1)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please Login First!'


    # Global Data
    @app1.context_processor
    def global_data():

        facility_name = []
        # only access session during real HTTP request(to avoid error in celery)
        if has_request_context():
            facilities = db.session.query(Facilities).all()

            for f in facilities:
                facility_name.append(f.name)

        return dict(global_facilities=facility_name)


    # Register Bluprints
    app1.register_blueprint(auth, url_prefix = '/auth')
    app1.register_blueprint(admin_bp, url_prefix = '/admin')
    app1.register_blueprint(host, url_prefix='/host')
    app1.register_blueprint(hotel, url_prefix='/host/hotel')
    app1.register_blueprint(user)
    app1.register_blueprint(room, url_prefix = '/host/room')
    app1.register_blueprint(profile, url_prefix = '/profile')
    app1.register_blueprint(booking, url_prefix = '/booking')
    app1.register_blueprint(chat, url_prefix = '/chat')


    # Imports 
    import app.models 
    import app.tasks
    import app.socket
    init_admin()


    return app1
