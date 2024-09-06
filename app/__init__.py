from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from .config import Config


db = SQLAlchemy()
login_manager = LoginManager()



from .models import User

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(Config)



    db.init_app(app)  
    login_manager.init_app(app)

    login_manager.login_view = 'main.auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    migrate = Migrate(app,db)
    from .routes import main as routes_blueprint
    app.register_blueprint(routes_blueprint)

    return app



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))