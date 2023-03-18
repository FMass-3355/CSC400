#Imports
#-------From SQLAlchemy---------#
from email.policy import default
from app import db, login
from sqlalchemy import*
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *
#------From Flask Login---------#
from flask_login import UserMixin, current_user
from flask import render_template, redirect, url_for, flash, request, session, jsonify, send_file
from werkzeug.security import generate_password_hash, check_password_hash
#--------Python Library---------#
import requests
from io import BytesIO



# User extends the flask_login defined UserMixin class.  UserMixin
# provides default functionality that allows us to keep track of
# authenticated user

#===================================================================================================
#Model's Python file is used to create the database stuff
#Please make sure to do db.create_all()
#do db.drop_all() to drop all the database
#===================================================================================================


#---------------- Users ----------------#
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(128), unique=True)
    gender = db.Column(db.String(32))
    role = db.Column(db.String(32))
    password_hash = db.Column(db.String(256), unique=True)
    fname = db.Column(db.String(64))
    lname = db.Column(db.String(64))
    date_of_birth = db.Column(db.Date)
    #tracks = db.relationship('Track', backref='fk_user_id')
    #friendships = relationship('Friend', collection_class=set, cascade='all, delete', backref="users")
    # primaryjoin='User.id==Friendship.user_id',
    #Password Salting
    def set_password(self, password):
        #Store hashed (encrypted) password in database
        self.password_hash = generate_password_hash(password)
    #Password Checking
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)      

class UserInfo:
    def __UserInfo__(user_id,username,email,role):
        user_id = user_id
        username = username
        email = email
        role = role

class Track(db.Model):
    __tablename__ = 'track'
    id = db.Column(db.Integer, primary_key=True)
    fk_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    t_input_date = db.Column(db.Date)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)

class Exercise(db.Model):
    __tablename__ = 'exercise'
    id = db.Column(db.Integer, primary_key=True)
    fk_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    e_input_date = db.Column(db.Date)
    e_name = db.Column(db.String(64))
    e_calories_per_hour = db.Column(db.Float)
    e_duration_minutes = db.Column(db.Float)
    e_total_calories = db.Column(db.Float)
    

class Calorie(db.Model):
    __tablename__ = 'calorie'
    id = db.Column(db.Integer, primary_key=True)
    fk_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    c_input_date = db.Column(db.Date)
    c_name = db.Column(db.String(64))
    c_total_calories = db.Column(db.Float)
    c_serving_size_g = db.Column(db.Float)
    c_fat_saturated_g = db.Column(db.Float)
    c_protein_g = db.Column(db.Float)
    c_sodium_mg = db.Column(db.Float)
    c_potassium_mg = db.Column(db.Float)
    c_cholesterol_mg = db.Column(db.Float)
    c_carbohydrates_total_g = db.Column(db.Float)
    c_fiber_g = db.Column(db.Float)
    c_sugar_g = db.Column(db.Float)
    

class Friend(db.Model):
    __tablename__ = 'friends'
    id = db.Column(db.Integer, primary_key=True)
    fk_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fk_friend_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_added = db.Column(db.Date)
    status = db.Column(db.Integer)

User.friends = relationship(User, secondary='friends', primaryjoin=User.id==Friend.fk_user_id, secondaryjoin=User.id==Friend.fk_friend_id)


#===================================================================================================
# load_user is a function that's used by flask_login to manage the session.
# It simply returns the object associated with the authenticated user.
@login.user_loader
def load_user(id):
    return db.session.query(User).get(int(id))
#===================================================================================================

class CalInfo:
    def __CalInfo__(cal_id, c_input_date, c_name):
        cal_id = cal_id
        c_input_date = c_input_date
        c_name = c_name

class ExInfo:
    def __ExInfo__(ex_id, e_input_date, e_name):
        ex_id = ex_id
        e_input_date = e_input_date
        e_name = e_name