from flask import Blueprint

room = Blueprint(
    'room',
    __name__,
    template_folder='templates'
)

from . import routes