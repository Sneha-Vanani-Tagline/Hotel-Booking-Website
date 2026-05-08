from flask import Blueprint

hotel = Blueprint(
    'hotel',
    __name__,
    template_folder='templates'
)

from . import routes