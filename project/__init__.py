from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import pymysql

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    #  python -c 'import secrets; print(secrets.token_hex())'
    app.config['SECRET_KEY'] = '0860211d075937aad203b0d724c80895377511d1ded661d3ffa926770bdee0e4'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb+pymysql://root:example@authdb/auth?charset=utf8mb4'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/api/#flask_sqlalchemy.SQLAlchemy.init_app
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    # app.config['SQLALCHEMY_ENGINE_OPTIONS'] = "" # https://docs.sqlalchemy.org/en/14/core/engines_connections.html
    # app.config['SQLALCHEMY_ECHO'] = False
    # app.config['SQLALCHEMY_BINDS'] = "" # https://docs.sqlalchemy.org/en/14/core/engines_connections.html
    # app.config['SQLALCHEMY_RECORD_QUERIES'] = False
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
