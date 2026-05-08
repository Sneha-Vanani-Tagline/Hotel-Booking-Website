from flask import Blueprint

user = Blueprint(
    'user',
    __name__,
    template_folder = 'templates',
    static_folder = 'static',
    static_url_path= '/user/static'     # sometime flask dosen't find the path, if we use module static folder, so we have to define the path manually
)

from . import routes