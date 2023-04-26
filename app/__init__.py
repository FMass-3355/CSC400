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
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import random

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
#-----
# app.static_folder = "static"
# app.config.from_pyfile('config.cfg')
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
#===================================================================================================
app.config["MAIL_SERVER"]='smtp.gmail.com'
app.config["MAIL_USERNAME"]='fitemail420@gmail.com'
app.config["MAIL_PASSWORD"]='dcaqhvkurlllfpfn'
#csc400!!
app.config["MAIL_PORT"]=465
app.config["MAIL_USE_TLS"]=False
app.config["MAIL_USE_SSL"]=True
#app.config["SECURITY_CONFIRMABLE"] = True
mail = Mail()
mail.init_app(app)
s = URLSafeTimedSerializer('Thisisasecret!')
otp = random.randint(000000,999999)
#s = Serializer('sercret', 30)
#token = s.dumps({'user_id': 1}).decode('utf-8')
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
            user_admin = User(username='fm', role='admin', date_of_birth='1999-03-03', fname='Franklin', lname='Massimi', email='FMass3355@hotmail.com', gender='m', is_confirmed=True)
            user_admin.set_password('csc400sp23', False)
            db.session.add(user_admin)
            db.session.commit()

        user = User.query.filter_by(username='kb').first()
        if user is None:
            user_regular_1 = User(username='kb', role='regular', date_of_birth='1998-05-07', fname='Kari', lname='Bevis', email='k.bevis01@gmail.com', gender='f', is_confirmed=True)
            user_regular_1.set_password('csc400sp23', False)
            db.session.add(user_regular_1)
            db.session.commit()

        user = User.query.filter_by(username='ej').first()
        if user is None:
            user_regular_2 = User(username='ej', role='regular', date_of_birth='2001-09-09', fname='Emma', lname='Jamieson', email='ejamieson747@gmail.com', gender='f', is_confirmed=True)
            user_regular_2.set_password('csc400sp23', False)
            db.session.add(user_regular_2)
            db.session.commit()

        #TRACK#
        #height maybe done in cm?
        track = Track.query.filter_by(fk_user_id=1).first()
        if track is None:
            track_1 = Track(fk_user_id=1, height=71, weight=165)
            db.session.add(track_1)
            db.session.commit()

        # track = Track.query.filter_by(t_input_date='2022-12-22', fk_user_id=1).first()
        # if track is None:
        #     track_2 = Track(fk_user_id=1, height=30, weight=60, t_input_date='2022-12-22')
        #     db.session.add(track_2)
        #     db.session.commit()

        # track = Track.query.filter_by(t_input_date='2023-01-12', fk_user_id=1).first()
        # if track is None:
        #     track_3 = Track(fk_user_id=1, height=4, weight=300, t_input_date='2023-01-12')
        #     db.session.add(track_3)
        #     db.session.commit()

        track = Track.query.filter_by(fk_user_id=2).first()
        if track is None:
            track_4 = Track(fk_user_id=2, height=180, weight=100)
            db.session.add(track_4)
            db.session.commit()

        # track = Track.query.filter_by(t_input_date='2023-02-06', fk_user_id=2).first()
        # if track is None:
        #     track_5 = Track(fk_user_id=2, height=190, weight=100, t_input_date='2023-02-06')
        #     db.session.add(track_5)
        #     db.session.commit()

        track = Track.query.filter_by(fk_user_id=3).first()
        if track is None:
            track_6 = Track(fk_user_id=3, height=167, weight=125)
            db.session.add(track_6)
            db.session.commit()

        #EXERCISE#
        exercise = Exercise.query.filter_by(e_input_date='2021-02-02', fk_user_id=1).first()
        if exercise is None:
            exercise_1 = Exercise(fk_user_id=1, e_name = 'rowing', e_input_date='2023-04-02', e_calories_per_hour=10.5, e_duration_minutes=60, e_total_calories=130.6)
            db.session.add(exercise_1)
            db.session.commit()
        
        exercise_1 = Exercise(fk_user_id=1, e_name = 'rowing', e_input_date='2023-04-05', e_calories_per_hour=10.5, e_duration_minutes=60, e_total_calories=145.6)
        db.session.add(exercise_1)
        db.session.commit()

        exercise_1 = Exercise(fk_user_id=1, e_name = 'rowing', e_input_date='2023-04-14', e_calories_per_hour=10.5, e_duration_minutes=60, e_total_calories=150.6)
        db.session.add(exercise_1)
        db.session.commit()

        exercise_1 = Exercise(fk_user_id=1, e_name = 'rowing', e_input_date='2023-04-19', e_calories_per_hour=10.5, e_duration_minutes=60, e_total_calories=142.6)
        db.session.add(exercise_1)
        db.session.commit()



        exercise_1 = Exercise(fk_user_id=2, e_name = 'rowing', e_input_date='2023-04-05', e_calories_per_hour=10.5, e_duration_minutes=60, e_total_calories=145.6)
        db.session.add(exercise_1)
        db.session.commit()

        exercise_1 = Exercise(fk_user_id=2, e_name = 'rowing', e_input_date='2023-04-14', e_calories_per_hour=10.5, e_duration_minutes=60, e_total_calories=150.6)
        db.session.add(exercise_1)
        db.session.commit()

        exercise_1 = Exercise(fk_user_id=2, e_name = 'rowing', e_input_date='2023-04-19', e_calories_per_hour=10.5, e_duration_minutes=60, e_total_calories=142.6)
        db.session.add(exercise_1)
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

        calorie = Calorie.query.filter_by(c_input_date='2023-04-02', fk_user_id=1).first()
        if calorie is None:
            calorie_1 = Calorie(fk_user_id=1, c_name = 'pancakes', c_input_date='2023-04-19')
            db.session.add(calorie_1)
            db.session.commit()
        
        calorie_1 = Calorie(fk_user_id=1, c_name = 'pancakes', c_input_date='2023-04-19', c_total_calories='130')
        db.session.add(calorie_1)
        db.session.commit()

        calorie_1 = Calorie(fk_user_id=1, c_name = 'pancakes', c_input_date='2023-04-15', c_total_calories='145')
        db.session.add(calorie_1)
        db.session.commit()

        calorie_1 = Calorie(fk_user_id=1, c_name = 'pancakes', c_input_date='2023-04-13', c_total_calories='135')
        db.session.add(calorie_1)
        db.session.commit()

        calorie_1 = Calorie(fk_user_id=1, c_name = 'pancakes', c_input_date='2023-04-08', c_total_calories='150')
        db.session.add(calorie_1)
        db.session.commit()

        calorie_1 = Calorie(fk_user_id=1, c_name = 'pancakes', c_input_date='2023-04-05', c_total_calories='130')
        db.session.add(calorie_1)
        db.session.commit()

        calorie_1 = Calorie(fk_user_id=1, c_name = 'pancakes', c_input_date='2023-04-01', c_total_calories='145')
        db.session.add(calorie_1)
        db.session.commit()

        

        calorie_1 = Calorie(fk_user_id=2, c_name = 'pancakes', c_input_date='2023-04-19', c_total_calories='130')
        db.session.add(calorie_1)
        db.session.commit()

        calorie_1 = Calorie(fk_user_id=2, c_name = 'pancakes', c_input_date='2023-04-15', c_total_calories='145')
        db.session.add(calorie_1)
        db.session.commit()

        calorie_1 = Calorie(fk_user_id=2, c_name = 'pancakes', c_input_date='2023-04-13', c_total_calories='135')
        db.session.add(calorie_1)
        db.session.commit()

        calorie_1 = Calorie(fk_user_id=2, c_name = 'pancakes', c_input_date='2023-04-08', c_total_calories='150')
        db.session.add(calorie_1)
        db.session.commit()

        calorie_1 = Calorie(fk_user_id=2, c_name = 'pancakes', c_input_date='2023-04-05', c_total_calories='130')
        db.session.add(calorie_1)
        db.session.commit()

        calorie_1 = Calorie(fk_user_id=2, c_name = 'pancakes', c_input_date='2023-04-01', c_total_calories='145')
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
