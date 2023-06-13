from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .events import socketio

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'untamahumannatanan15'
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://appdev:password@localhost/chat"
    
    db.init_app(app)


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Message

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(str(id))

    socketio.init_app(app)

    return app
