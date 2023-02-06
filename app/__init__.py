#===================================================================================================
from flask import Flask
#===================================================================================================
# New imports
#===================================================================================================
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
from os import environ
import mysql.connector
import requests
import sys
from wtforms.validators import DataRequired
import json
#===================================================================================================





#===================================================================================================
# force loading of environment variables
load_dotenv('.flaskenv')
#===================================================================================================
#===================================================================================================
# Get the environment variables from .flaskenv
IP = environ.get('MYSQL_IP')
USERNAME = environ.get('MYSQL_USER')
PASSWORD = environ.get('MYSQL_PASS')
DB_NAME = environ.get('MYSQL_DB')
#===================================================================================================
#===================================================================================================
#API
#=================================================================================================== 
# Read values from .flaskenv
API_KEY = environ.get('API_KEY')
API_HOST = environ.get('API_HOST')
API_URL = environ.get('API_URL')
EMAIL = environ.get('EMAIL')
#===================================================================================================
#===================================================================================================
#APP initialization stuff
#===================================================================================================
app = Flask(__name__)
app.config['SECRET_KEY'] = 'csc33O'
bootstrap = Bootstrap(app)
app.static_folder = "static"
#===================================================================================================
#===================================================================================================
# Specify the connection parameters/credentials for the database
#===================================================================================================
DB_CONFIG_STR = f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{IP}/{DB_NAME}"
app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG_STR
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True
#===================================================================================================
#===================================================================================================
# Create database connection and associate it with the Flask application
db = SQLAlchemy(app)
login = LoginManager(app)
#===================================================================================================


# user=db.session.query(User).filter_by(username='ArtMar23').first()
# if user is None:
#     custom_user = User(username='ArtMar23', email='artmar80@gmail.com', role='regular', fname='Arthur', lname='Martinez', date_of_birth='1999-02-02')
#     custom_user.set_password('123')
#     db.session.add(custom_user)
#     db.session.commit()






#===================================================================================================
# enables @login_required
login.login_view = 'login'
#===================================================================================================

#===================================================================================================
# Add models
#===================================================================================================
from app import routes, models
from app.models import *


#Drop Database to refresh (Comment out later once statisfied)
db.drop_all()
db.create_all()


user = User.query.filter_by(username='fm').first()
if user is None:
    user_admin = User(username='fm', role='admin')
    user_admin.set_password('csc400sp23')
    db.session.add(user_admin)
    db.session.commit()

user = User.query.filter_by(username='kb').first()
if user is None:
    user_regular = User(username='kb', role='regular')
    user_regular.set_password('csc400sp23')
    db.session.add(user_regular)
    db.session.commit()

track = Track.query.filter_by(height=169).first()
if track is None:
    track_shit = Track(fk_user_id=1, height=169, weight=200)
    db.session.add(track_shit)
    db.session.commit()

#need to query by both id's
# friend_q1 = Friend.query.filter_by(fk_user_id=1, fk_friend_id=2).first()
# friend_q2 = Friend.query.filter_by(fk_user_id=2, fk_friend_id=1).first()
# friend_q = db.union(friend_q1, friend_q2)
# from sqlalchemy import union_all
# friend_q = union_all(select(Friend).where(Friend.fk_user_id==1, Friend.fk_friend_id==2), select(Friend).where(Friend.fk_user_id==2, Friend.fk_friend_id==1))
# friend_q = select(Friend).from_statement(friend_q)
friend_q = Friend.query.filter_by(fk_user_id=1, fk_friend_id=2).first()
if friend_q is None:
    friendship_1 = Friend(fk_user_id=1, fk_friend_id=2, status=2)
    friendship_2 = Friend(fk_user_id=2, fk_friend_id=1, status=2)
    db.session.add(friendship_1)
    db.session.add(friendship_2)
    db.session.commit()