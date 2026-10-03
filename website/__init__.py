import os
from dotenv import load_dotenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

load_dotenv()

db=SQLAlchemy()

def create_app():

    app=Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    database_url = os.getenv("DATABASE_URL")

    if database_url.startswith("mysql://"):
        database_url = database_url.replace(
        "mysql://", "mysql+pymysql://", 1
    )

    database_url = database_url.replace(
        "ssl-mode=REQUIRED", "ssl=true"
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

    db.init_app(app)
    migrate=Migrate(app,db)

    from .home import views
    from .auth import auth
    from .models import User

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    login_manager=LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        if not id or id == "None":
            return None
        return User.query.get(int(id))

    return app