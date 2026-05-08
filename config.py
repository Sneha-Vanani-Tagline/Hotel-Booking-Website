
class Config:
    SECRET_KEY = 'my-secret-key-1'

    # Database connection
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:server1@localhost:5433/hotelDB'        # database system: // password @ port / database name
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File uploading path
    UPLOAD_FOLDER = 'app/static/images'

    # Mail Config
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'svn@taglineinfotech.com'
    MAIL_PASSWORD = "tzni ywqu dqcr omyr"
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
