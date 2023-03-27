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
def reset_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        #USER#
        user = User.query.filter_by(username='fm').first()
        if user is None:
            user_admin = User(username='fm', role='admin', date_of_birth='1960-12-12', fname='f', lname='m', email='fm@email.com', gender='m')
            user_admin.set_password('csc400sp23')
            db.session.add(user_admin)
            db.session.commit()

        user = User.query.filter_by(username='kb').first()
        if user is None:
            user_regular_1 = User(username='kb', role='regular', date_of_birth='1998-05-07', fname='k', lname='b', email='kb@email.com', gender='f')
            user_regular_1.set_password('csc400sp23')
            db.session.add(user_regular_1)
            db.session.commit()

        user = User.query.filter_by(username='ej').first()
        if user is None:
            user_regular_2 = User(username='ej', role='regular', date_of_birth='2001-09-09', fname='e', lname='j', email='ej@email.com', gender='f')
            user_regular_2.set_password('csc400sp23')
            db.session.add(user_regular_2)
            db.session.commit()

        #TRACK#
        #height maybe done in cm?
        track = Track.query.filter_by(t_input_date='2021-02-02', fk_user_id=1).first()
        if track is None:
            track_1 = Track(fk_user_id=1, height=169, weight=200, t_input_date='2021-02-02')
            db.session.add(track_1)
            db.session.commit()

        track = Track.query.filter_by(t_input_date='2022-12-22', fk_user_id=1).first()
        if track is None:
            track_2 = Track(fk_user_id=1, height=30, weight=60, t_input_date='2022-12-22')
            db.session.add(track_2)
            db.session.commit()

        track = Track.query.filter_by(t_input_date='2023-01-12', fk_user_id=1).first()
        if track is None:
            track_3 = Track(fk_user_id=1, height=4, weight=300, t_input_date='2023-01-12')
            db.session.add(track_3)
            db.session.commit()

        track = Track.query.filter_by(t_input_date='2022-02-02', fk_user_id=2).first()
        if track is None:
            track_4 = Track(fk_user_id=2, height=180, weight=100, t_input_date='2022-02-02')
            db.session.add(track_4)
            db.session.commit()

        track = Track.query.filter_by(t_input_date='2023-02-06', fk_user_id=2).first()
        if track is None:
            track_5 = Track(fk_user_id=2, height=190, weight=100, t_input_date='2023-02-06')
            db.session.add(track_5)
            db.session.commit()

        track = Track.query.filter_by(t_input_date='2023-01-29', fk_user_id=3).first()
        if track is None:
            track_6 = Track(fk_user_id=3, height=167, weight=125, t_input_date='2023-01-29')
            db.session.add(track_6)
            db.session.commit()

        #EXERCISE#
        exercise = Exercise.query.filter_by(e_input_date='2021-02-02', fk_user_id=1).first()
        if exercise is None:
            exercise_1 = Exercise(fk_user_id=1, e_name = 'rowing', e_input_date='2021-02-02', e_calories_per_hour=10.5, e_duration_minutes=60, e_total_calories=110.6)
            db.session.add(exercise_1)
            db.session.commit()

        exercise = Exercise.query.filter_by(e_input_date='2022-12-22', fk_user_id=1).first()
        if exercise is None:
            exercise_2 = Exercise(fk_user_id=1, e_name = 'push ups', e_input_date='2022-12-22')
            db.session.add(exercise_2)
            db.session.commit()

        exercise = Exercise.query.filter_by(e_input_date='2023-01-12', fk_user_id=1).first()
        if exercise is None:
            exercise_3 = Exercise(fk_user_id=1, e_name = 'running', e_input_date='2023-01-12')
            db.session.add(exercise_3)
            db.session.commit()

        exercise = Exercise.query.filter_by(e_input_date='2022-02-02', fk_user_id=2).first()
        if exercise is None:
            exercise_4 = Exercise(fk_user_id=2, e_name = 'biking', e_input_date='2022-02-02')
            db.session.add(exercise_4)
            db.session.commit()

        exercise = Exercise.query.filter_by(e_input_date='2023-02-06', fk_user_id=2).first()
        if exercise is None:
            exercise_5 = Exercise(fk_user_id=2, e_name = 'boxing', e_input_date='2023-02-06')
            db.session.add(exercise_5)
            db.session.commit()

        exercise = Exercise.query.filter_by(e_input_date='2023-01-29', fk_user_id=3).first()
        if exercise is None:
            exercise_6= Exercise(fk_user_id=3, e_name = 'tennis', e_input_date='2023-01-29')
            db.session.add(exercise_6)
            db.session.commit()

        #CALORIE#

        calorie = Calorie.query.filter_by(c_input_date='2021-02-02', fk_user_id=1).first()
        if calorie is None:
            calorie_1 = Calorie(fk_user_id=1, c_name = 'pancakes', c_input_date='2021-02-02')
            db.session.add(calorie_1)
            db.session.commit()

        calorie = Calorie.query.filter_by(c_input_date='2022-12-22', fk_user_id=1).first()
        if calorie is None:
            calorie_2 = Calorie(fk_user_id=1, c_name = 'lettuce', c_input_date='2022-12-22')
            db.session.add(calorie_2)
            db.session.commit()

        calorie = Calorie.query.filter_by(c_input_date='2023-01-12', fk_user_id=1).first()
        if calorie is None:
            calorie_3 = Calorie(fk_user_id=1, c_name = 'berries', c_input_date='2023-01-12')
            db.session.add(calorie_3)
            db.session.commit()

        calorie = Calorie.query.filter_by(c_input_date='2022-02-02', fk_user_id=2).first()
        if calorie is None:
            calorie_4 = Calorie(fk_user_id=2, c_name = 'rice', c_input_date='2022-02-02')
            db.session.add(calorie_4)
            db.session.commit()

        calorie = Calorie.query.filter_by(c_input_date='2023-02-06', fk_user_id=2).first()
        if calorie is None:
            calorie_5 = Calorie(fk_user_id=2, c_name = 'gum', c_input_date='2023-02-06')
            db.session.add(calorie_5)
            db.session.commit()

        calorie = Calorie.query.filter_by(c_input_date='2023-01-29', fk_user_id=3).first()
        if calorie is None:
            calorie_6= Calorie(fk_user_id=3, c_name = 'cereal', c_input_date='2023-01-29')
            db.session.add(calorie_6)
            db.session.commit()

        #FRIEND#
        friend = Friend.query.filter_by(fk_user_id=1, fk_friend_id=2).first()
        if friend is None:
            friendship_1_1 = Friend(fk_user_id=1, fk_friend_id=2, status=2)
            friendship_1_2 = Friend(fk_user_id=2, fk_friend_id=1, status=2)
            db.session.add(friendship_1_1)
            db.session.add(friendship_1_2)
            db.session.commit()

        friend = Friend.query.filter_by(fk_user_id=1, fk_friend_id=3).first()
        if friend is None:
            friendship_2_1 = Friend(fk_user_id=1, fk_friend_id=3, status=0)
            friendship_2_2 = Friend(fk_user_id=3, fk_friend_id=1, status=1)
            db.session.add(friendship_2_1)
            db.session.add(friendship_2_2)
            db.session.commit()

        friend = Friend.query.filter_by(fk_user_id=2, fk_friend_id=3).first()
        if friend is None:
            friendship_3_1 = Friend(fk_user_id=2, fk_friend_id=3, status=1)
            friendship_3_2 = Friend(fk_user_id=3, fk_friend_id=2, status=0)
            db.session.add(friendship_3_1)
            db.session.add(friendship_3_2)
            db.session.commit()

        #status(0) = u  <-  f
        #status(1) = u  ->  f
        #status(2) = u <-> f

reset_db()