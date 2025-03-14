from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from flask_login import LoginManager, login_required, current_user


db = SQLAlchemy()
DB_NAME = "database.db"
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'qkfhuiqhwfu'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")

    db.init_app(app)

    from .views import views
    from.auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Profile, DepartmentOntologyAssociation, Ontology, GameInformation, DefinitionScores

    #create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app



def create_database(app):

    with app.app_context():
        if not path.exists('website/' + DB_NAME):
            db.create_all()
            print('Created Database!')


