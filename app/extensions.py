from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_socketio import SocketIO
from flask_caching import Cache

db = SQLAlchemy()
mail = Mail()
socketio = SocketIO()
cache = Cache()