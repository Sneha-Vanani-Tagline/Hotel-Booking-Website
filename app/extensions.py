from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_socketio import SocketIO
from flask_caching import Cache
from flask_admin import Admin
from flask_login import LoginManager

db = SQLAlchemy()
mail = Mail()
socketio = SocketIO()
cache = Cache()
flaskAdmin = Admin()
login_manager = LoginManager()