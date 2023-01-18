from os import path

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()
DB_NAME = 'tabernacle.sqlite3'
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'social event management app'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Content
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(str(user_id))

    create_database(app)
    return app

#Create Database
def create_database(app):
    if not path.exists('app/'+ DB_NAME):
        with app.app_context():
            db.create_all()
        print('Database Created!')