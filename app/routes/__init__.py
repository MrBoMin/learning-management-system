from flask import Blueprint

main = Blueprint('main', __name__)

from .auth import auth as auth_blueprint
from .classroom import classroom as classroom_blueprint


main.register_blueprint(auth_blueprint, url_prefix='/auth')
main.register_blueprint(classroom_blueprint)