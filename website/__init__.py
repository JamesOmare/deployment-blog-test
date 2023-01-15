from flask import Flask
from flask_login import LoginManager
from .views import views
from .auth import auth
from .models.user import User
from .utils import db, migrate, login_manager
from .config.config import Config
import os


def create_app(config = Config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login_manager.init_app(app)
    

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    with app.app_context():
        db.create_all()
    

    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(id):
       return User.query.get(int(id))

    return app
