from flask import Blueprint

host = Blueprint(
    'host',
    __name__,
    template_folder='templates'
)

from . import routes