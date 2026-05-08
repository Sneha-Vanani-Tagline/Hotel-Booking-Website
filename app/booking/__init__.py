from flask import Blueprint

booking = Blueprint(
    'booking',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/booking/static'
)

from . import routes