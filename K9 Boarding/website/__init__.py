from flask import Flask, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_login import current_user
from functools import wraps


db = SQLAlchemy()
DB_NAME = "database.db"



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'asdkien fiemleia' # random string (never share)
    # configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    # where to go when logged in
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .views import views
    from .auth import auth

    # register blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # create database
    from .models import User

    create_database(app)
    

    #telling flask which user to look for referencing by id
    @login_manager.user_loader
    def load_user(id):
        # looks for primary ket (get)
        return User.query.get(int(id))

    return app

def create_database(app):
    # folder you are creating database in 
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

def admin_required(func):
    """
    Modified login_required decorator to restrict access to admin group.
    """

    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.role != 'admin':        
            flash("You don't have permission to access this resource.", "warning")
            return redirect(url_for("views.home"))
        return func(*args, **kwargs)
    return decorated_view
