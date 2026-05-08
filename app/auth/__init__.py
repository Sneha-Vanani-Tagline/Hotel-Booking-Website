from flask import Blueprint

auth = Blueprint(
        'auth', 
        __name__, 
        template_folder='templates'     # By writting this flask will find html files inseide this folder's templates, otherwise it finds html files in main templates folder outside the auth folder
    )     

from . import routes