from dotenv import load_dotenv
import os
from celery.schedules import crontab

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    # Database connection
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File uploading path
    UPLOAD_FOLDER = 'app/static/images'

    # Mail Config
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    CELERY = {
        'broker_url': 'redis://localhost:6379/0',
        'result_backend': 'redis://localhost:6379/0',
        
        'timezone': 'Asia/Kolkata',
        'enable_utc': False,
    
        'beat_schedule' : {
            'check-for-reminder-every-morning' : {
                'task' : 'app.tasks.check_booking_reminder',
                'schedule' : crontab(hour=8, minute=0),
            }
        }
    }
