#Imports

from operator import methodcaller
#from app import app as appl
from app import API_KEY, app, otp, mail, s
#-------environment-------#
from dotenv import load_dotenv
from os import environ, path
#------SQLAlchemy---------#
from app import db
from app.models import *
from sqlalchemy import create_engine, text
#------flask------#
from flask import render_template, redirect, url_for, flash, send_file, Response, request
from flask_login import login_user, logout_user, login_required, current_user
#------WTFForms---------#
from app.forms import *
from wtforms.validators import DataRequired
#--------Externals-----#
import sys
import requests
from io import BytesIO

from datetime import date, datetime, timedelta
from flask_wtf.file import FileField
import json

#import psycopg2
import matplotlib.pyplot as plt
import pandas as pd

from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from email_validator import validate_email,EmailNotValidError
import re
from email_validator import validate_email, EmailNotValidError
# testEmail = "fitemail420@gmail.com"
# emailObject = validate_email(testEmail)
# print(emailObject.email)
# try:
#     # Validating the `testEmail`
#     emailObject = validate_email(testEmail)

#     # If the `testEmail` is valid
#     # it is updated with its normalized form
#     testEmail = emailObject.email
#     print(testEmail)
# except EmailNotValidError as errorMsg:
#     # If `testEmail` is not valid
#     # we print a human readable error message
#     print(str(errorMsg))
#API 
API_KEY = environ.get('API_KEY')
API_HOST = environ.get('API_HOST')
API_URL = environ.get('API_URL')
EMAIL = environ.get('EMAIL')
CALORIES_API_URL = environ.get('CALORIES_API_URL')
NUTRITION_API_URL = environ.get('NUTRITION_API_URL')

actualDay1 = datetime.now()
actualDay2 = actualDay1.strftime("%B %d, %Y")
thisDay = datetime.now()
today = thisDay.strftime("%B %d, %Y")
databaseToday = thisDay.strftime("%Y-%m-%d")


#------------------------------------------------------------ Static Webpages ----------------------------------------------------------------#
@app.route('/homepage')
def homepage():
    user = current_user.fname
    return render_template('homepage.html', user=user)
  
@app.route('/email', methods=['GET', 'POST'])
def email():
    return render_template('email.html')
  
@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html')
#------------------------------------------------------------ Static Webpages ----------------------------------------------------------------#

@app.route('/yesterday', methods=['GET', 'POST'])
def setYesterday():
    global actualDay2
    global thisDay

    user_id = current_user.id
    yesterday = timedelta(days=-1)
    thisDay = thisDay + yesterday
    yesterday2 = thisDay.strftime("%B %d, %Y")
    databaseYesterday = thisDay.strftime("%Y-%m-%d")

    if request.method == "GET":
        foods = db.session.query(Calorie).filter_by(c_input_date=databaseYesterday, fk_user_id=user_id)
        workouts = db.session.query(Exercise).filter_by(e_input_date=databaseYesterday, fk_user_id=user_id)
        workouts = workouts.all()
        foods = foods.all()

    if yesterday2 == actualDay2:
        return redirect(url_for('tracker'))
    else:
        return render_template('tracker.html', pdate=yesterday2, actualDay=actualDay2, workouts=workouts, foods=foods)

@app.route('/tomorrow', methods=['GET', 'POST'])
def setTomorrow():
    global actualDay2
    global thisDay

    user_id = current_user.id
    tomorrow = timedelta(days=+1)
    thisDay = thisDay + tomorrow
    tomorrow2 = thisDay.strftime("%B %d, %Y")
    databaseTomorrow = thisDay.strftime("%Y-%m-%d")

    if request.method == "GET":
        foods = db.session.query(Calorie).filter_by(c_input_date=databaseTomorrow, fk_user_id=user_id)
        workouts = db.session.query(Exercise).filter_by(e_input_date=databaseTomorrow, fk_user_id=user_id)
        foods = foods.all()
        workouts = workouts.all()

    if tomorrow2 == actualDay2:
        return redirect(url_for('tracker'))
    else:
        return render_template('tracker.html', pdate=tomorrow2, actualDay=actualDay2, workouts=workouts, foods=foods)

@app.route('/tracker', methods=['GET', 'POST'])
def tracker():
    global actualDay2
    global thisDay
    global databaseToday

    user_id = current_user.id
    thisDay = datetime.now()
    today = thisDay.strftime("%B %d, %Y")

    if request.method == "GET":
        foods = db.session.query(Calorie).filter_by(c_input_date=databaseToday, fk_user_id=user_id)
        workouts = db.session.query(Exercise).filter_by(e_input_date=databaseToday, fk_user_id=user_id)
        foods = foods.all()
        workouts = workouts.all()
    return render_template('tracker.html', pdate=today, actualDay=actualDay2, workouts=workouts, foods=foods)

@app.route('/c_delete_row/<row_id>', methods=['GET', 'POST'])
@login_required
def c_deleteRow(row_id):
    global databaseToday
    global actualDay2
    global thisDay
    print(f'row_id={row_id}')
    db.session.query(Calorie).filter_by(id=row_id).delete()
    db.session.commit()
    return redirect(url_for('edit_tracker'))

@app.route('/e_delete_row/<row_id>', methods=['GET', 'POST'])
@login_required
def e_deleteRow(row_id):
    global databaseToday
    global actualDay2
    global thisDay
    db.session.query(Exercise).filter_by(id=row_id).delete()
    db.session.commit()
    return redirect(url_for('edit_tracker'))

@app.route('/serving_size_up_1/<s_var>/<row_id>', methods=['GET', 'POST'])
@login_required
def serving_size_up_1(s_var,row_id):
    global databaseToday
    global actualDay2
    global thisDay
    #db.session.query(Friend).filter_by(fk_user_id=current_user_id, fk_friend_id=friend_id).update({'status':2})
    #user = db.session.query(User).filter_by(username=form.username.data).first()
    user_id = current_user.id 
    query_cal_row = []
    # print("in route")
    print(f'user id: {user_id}')
    print(f'row id: {row_id}')
    # for item in db.session.query(Calorie).filter(Calorie.fk_user_id==user_id, Calorie.c_input_date==databaseToday):
    for item in db.session.query(Calorie).filter(Calorie.fk_user_id==user_id, Calorie.id==row_id):
        print(f"in row {item}")
        row = CalInfo()
        row.cal_id = item.id
        row.c_input_date = item.c_input_date
        row.c_serving_size_g = item.c_serving_size_g
        row.c_total_calories = item.c_total_calories
        row.c_name = item.c_name
        row.c_total_calories_NEW = item.c_total_calories_NEW
        query_cal_row.append(row)
        new_c_serving_size_g = ((row.c_serving_size_g) + 100)/100
        new_c_total_calories = ((row.c_total_calories))* new_c_serving_size_g #if serving size is not 100 it might not work
        db.session.query(Calorie).filter(Calorie.fk_user_id==user_id, Calorie.id==row_id).update({'c_serving_size_g':new_c_serving_size_g*100})
        db.session.query(Calorie).filter(Calorie.fk_user_id==user_id, Calorie.id==row_id).update({'c_total_calories_NEW':new_c_total_calories})
        #db.session.query(Calorie).filter_by(id=row_id).delete()
        db.session.commit()
        print('COMMITED')
        print(len(query_cal_row))
    return redirect(url_for('edit_tracker'))

@app.route('/serving_size_down_1/<s_var>/<row_id>', methods=['GET', 'POST'])
@login_required
def serving_size_down_1(s_var,row_id):
    global databaseToday
    global actualDay2
    global thisDay
    #db.session.query(Friend).filter_by(fk_user_id=current_user_id, fk_friend_id=friend_id).update({'status':2})
    #user = db.session.query(User).filter_by(username=form.username.data).first()
    user_id = current_user.id 
    query_cal_row = []
    # print("in route")
    print(f'user id: {user_id}')
    print(f'row id: {row_id}')
    # for item in db.session.query(Calorie).filter(Calorie.fk_user_id==user_id, Calorie.c_input_date==databaseToday):
    for item in db.session.query(Calorie).filter(Calorie.fk_user_id==user_id, Calorie.id==row_id):
        print(f"in row {item}")
        row = CalInfo()
        row.cal_id = item.id
        row.c_input_date = item.c_input_date
        row.c_serving_size_g = item.c_serving_size_g
        row.c_total_calories = item.c_total_calories
        row.c_name = item.c_name
        row.c_total_calories_NEW = item.c_total_calories_NEW
        query_cal_row.append(row)
        new_c_serving_size_g = ((row.c_serving_size_g) - 100)/100
        new_c_total_calories = ((row.c_total_calories))* new_c_serving_size_g #if serving size is not 100 it might not work
        db.session.query(Calorie).filter(Calorie.fk_user_id==user_id, Calorie.id==row_id).update({'c_serving_size_g':new_c_serving_size_g*100})
        db.session.query(Calorie).filter(Calorie.fk_user_id==user_id, Calorie.id==row_id).update({'c_total_calories_NEW':new_c_total_calories})
        #db.session.query(Calorie).filter_by(id=row_id).delete()
        db.session.commit()
        print('COMMITED')
        print(len(query_cal_row))
    return redirect(url_for('edit_tracker'))

@app.route('/duration_min_up_1/<d_var>/<row_id>', methods=['GET', 'POST'])
@login_required
def duration_min_up_1(d_var,row_id):
    global databaseToday
    global actualDay2
    global thisDay
    #db.session.query(Friend).filter_by(fk_user_id=current_user_id, fk_friend_id=friend_id).update({'status':2})
    #user = db.session.query(User).filter_by(username=form.username.data).first()
    user_id = current_user.id 

    query_ex_row = []
    for item in db.session.query(Exercise).filter(Exercise.fk_user_id==user_id, Exercise.id==row_id):
        row = ExInfo()
        row.ex_id = item.id
        row.e_input_date = item.e_input_date
        row.e_duration_minutes = item.e_duration_minutes
        row.e_total_calories = item.e_total_calories
        row.e_name = item.e_name
        row.e_total_calories_NEW = item.e_total_calories_NEW
        query_ex_row.append(row)

        new_e_duration_minutes = ((row.e_duration_minutes)+60)
        new_e_total_calories = ((row.e_total_calories) + row.e_total_calories_NEW) #if serving size is not 100 it might not work
        db.session.query(Exercise).filter(Exercise.fk_user_id==user_id, Exercise.id==row_id).update({'e_duration_minutes':new_e_duration_minutes})
        db.session.query(Exercise).filter(Exercise.fk_user_id==user_id, Exercise.id==row_id).update({'e_total_calories_NEW':new_e_total_calories})
        #db.session.query(Calorie).filter_by(id=row_id).delete()
        db.session.commit()
        print('COMMITED')
        print(len(query_ex_row))
    return redirect(url_for('edit_tracker'))

@app.route('/duration_min_down_1/<d_var>/<row_id>', methods=['GET', 'POST'])
@login_required
def duration_min_down_1(d_var,row_id):
    global databaseToday
    global actualDay2
    global thisDay
    #db.session.query(Friend).filter_by(fk_user_id=current_user_id, fk_friend_id=friend_id).update({'status':2})
    #user = db.session.query(User).filter_by(username=form.username.data).first()
    user_id = current_user.id 

    query_ex_row = []
    for item in db.session.query(Exercise).filter(Exercise.fk_user_id==user_id, Exercise.id==row_id):
        row = ExInfo()
        row.ex_id = item.id
        row.e_input_date = item.e_input_date
        row.e_duration_minutes = item.e_duration_minutes
        row.e_total_calories = item.e_total_calories
        row.e_name = item.e_name
        row.e_total_calories_NEW = item.e_total_calories_NEW
        query_ex_row.append(row)

        new_e_duration_minutes = ((row.e_duration_minutes)-60)
        new_e_total_calories = (row.e_total_calories_NEW - (row.e_total_calories)) #if serving size is not 100 it might not work
        db.session.query(Exercise).filter(Exercise.fk_user_id==user_id, Exercise.id==row_id).update({'e_duration_minutes':new_e_duration_minutes})
        db.session.query(Exercise).filter(Exercise.fk_user_id==user_id, Exercise.id==row_id).update({'e_total_calories_NEW':new_e_total_calories})
        #db.session.query(Calorie).filter_by(id=row_id).delete()
        db.session.commit()
        print('COMMITED')
        print(len(query_ex_row))
    return redirect(url_for('edit_tracker'))



@app.route('/edit_tracker', methods=['GET', 'POST'])
def edit_tracker():
    global databaseToday
    global actualDay2
    global thisDay
    user_id = current_user.id 

    form=EditTracker()
    if form.validate_on_submit():
        c_name = form.c_name.data
        c_input_date = databaseToday
        c_serving_size_g = form.c_serving_size_g.data
        c_total_calories = c_total_calories
        c_submit = form.c_submit.data
        e_name = form.e_name.data
        e_input_date = databaseToday
        e_duration_minutes = form.e_duration_minutes.data
        e_total_calories = e_total_calories
        e_submit = form.e_submit.data
        
        if c_name != '' and c_submit:
            food = Calorie(fk_user_id=user_id, c_name=c_name, c_input_date=c_input_date, c_serving_size_g=c_serving_size_g, c_total_calories = c_total_calories)
            db.session.add(food)
            db.session.commit()
            print(c_name)
        elif e_name != '' and e_submit:
            exercise = Exercise(fk_user_id=user_id, e_name=e_name, e_input_date=e_input_date, e_duration_minutes=e_duration_minutes, e_total_calories = e_total_calories)
            db.session.add(exercise)
            db.session.commit()    
            print(e_name)

    foods = db.session.query(Calorie).filter_by(c_input_date=databaseToday, fk_user_id=user_id)
    workouts = db.session.query(Exercise).filter_by(e_input_date=databaseToday, fk_user_id=user_id)
    foods = foods.all()
    workouts = workouts.all()

    query_cal_row = []
    for item in db.session.query(Calorie).filter(Calorie.fk_user_id==user_id, Calorie.c_input_date==databaseToday):
        row = CalInfo()
        row.cal_id = item.id
        row.c_input_date = item.c_input_date
        row.c_serving_size_g = item.c_serving_size_g
        row.c_total_calories_NEW = item.c_total_calories_NEW
        row.c_total_calories = item.c_total_calories
        row.c_name = item.c_name
        query_cal_row.append(row)
    
    query_ex_row = []
    for item in db.session.query(Exercise).filter(Exercise.fk_user_id==user_id, Exercise.e_input_date==databaseToday):
        row = ExInfo()
        row.ex_id = item.id
        row.e_input_date = item.e_input_date
        row.e_duration_minutes = item.e_duration_minutes
        row.e_total_calories_NEW = item.e_total_calories_NEW
        row.e_total_calories = item.e_total_calories
        row.e_name = item.e_name
        query_ex_row.append(row)


    return render_template('edit_tracker.html', form=form, workouts=workouts, foods=foods, query_cal_row=query_cal_row, query_ex_row=query_ex_row, actualDay2=actualDay2)
    #return render_template('edit_tracker.html', form=form)
#------------------------------------------------------------- Logging in and Out-----------------------------------------------#
#Start with here
@app.route('/')
def index():
    # msg = Message("Hello", sender="fitemail420@gmail.com", recipients=["deattlecowhawk@gmail.com"])
    # msg.body = "testing"
    # mail.send(msg)
    return redirect(url_for('login'))



#Login Method
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     #Authenticated users are redirected to home page.
#     if current_user.is_authenticated:
#         return redirect(url_for('homepage'))
        
#     form = LoginForm()
#     if form.validate_on_submit():
#         # Query DB for user by username
#         user = db.session.query(User).filter_by(username=form.username.data).first()
#         # if user.is_confirmed == True:
#         if user is None or not user.check_password(form.password.data):
#             print('Login failed', file=sys.stderr)
#             flash("Wrong username and/or password.")
#             return redirect(url_for('login'))
#         # login_user is a flask_login function that starts a session
#         else:
#             query_users = []
#             for item in db.session.query(User).filter(User.username==form.username.data).all():
#                 user = UserInfo()
#                 user.user_id = item.id
#                 user.username = item.username
#                 user.email = item.email
#                 user.role = item.role
#                 user.is_confirmed = item.is_confirmed 
#                 query_users.append(user)
#                 print(user.email)
#                 print(user.is_confirmed)
#                 if user.is_confirmed == False:
#                     email = user.email
#                     print(email)
#                     flash("Must enter OTP")
#                     return redirect(url_for('get_email', email=email))
#             if user.is_confirmed == True:
#                 # email = item.email
#                 login_user(user)
#                 print('Login successful', file=sys.stderr)
#                 return redirect(url_for('homepage'))
#         # elif user.is_confirmed == False:

#         #     email = current_user.email
#         #     flash("Must enter OTP")
#         #     return redirect(url_for('verify2'), email=email)
#         #     # return render_template('v2.html', email=email)
#     return render_template('login.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    #Authenticated users are redirected to home page.
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
        
    form = LoginForm()
    if form.validate_on_submit():
        # Query DB for user by username
        user = db.session.query(User).filter_by(username=form.username.data).first()
        if user.is_confirmed == True:
            if user is None or not user.check_password(form.password.data):
                print('Login failed', file=sys.stderr)
                flash("Wrong username and/or password.")
                return redirect(url_for('login')), 401
            # login_user is a flask_login function that starts a session
            else:
                login_user(user)
                print('Login successful', file=sys.stderr)
                return redirect(url_for('homepage'))
        elif user.is_confirmed == False:
            query_users = []
            for item in db.session.query(User).filter(User.username==form.username.data).all():
                user = UserInfo()
                user.user_id = item.id
                user.username = item.username
                user.email = item.email
                user.role = item.role
                user.is_confirmed = item.is_confirmed 
                query_users.append(user)
                print(user.email)
                print(user.is_confirmed)
                email = user.email
                print(email)
                flash("Must enter OTP")
                return redirect(url_for('get_email', email=email))
    return render_template('login.html', form=form)

#Logging out
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# @app.route('/email_ver', methods=['GET', 'POST'])
# def email_ver():
#     if request.method == 'GET':
#         return '<form action="/" method="POST"><input name="email"><input type="submit"></form>'

#     email = request.form['email']
#     token = s.dumps(email, salt='email-confirm')

#     msg = Message('Confirm Email', sender='fitemail420@gmail.com', recipients=[email])

#     link = url_for('confirm_email', token=token, _external=True)

#     msg.body = 'Your link is {}'.format(link)

#     mail.send(msg)

#     return '<h1>The email you entered is {}. The token is {}</h1>'.format(email, token)


# @app.route('/confirm_email/<token>')
# def confirm_email(token):
#     try:
#         email = s.loads(token, salt='email-confirm', max_age=3600)
#     except SignatureExpired:
#         return '<h1>The token is expired!</h1>'
#     return '<h1>The token works!</h1>'

@app.route('/test',methods=['GET'])
def test():
    return render_template("test.html") 


@app.route('/get_email/<email>', methods=['GET', 'POST'])
def get_email(email):
    print(email)
    # email = email
    message = str(otp)   
    subject = 'OTP'
    msg = Message(body=message,subject=subject,sender = 'fitemail420@gmail.com', recipients = [email])  
    # msg.body = str(otp)  
    mail.send(msg)
    return redirect(url_for('verify2', email=email))

@app.route('/verify2/<email>', methods=['GET', 'POST'])
def verify2(email):
    # print(email)
    # # email = email
    # message = str(otp)   
    # subject = 'OTP'
    # msg = Message(body=message,subject=subject,sender = 'fitemail420@gmail.com', recipients = [email])  
    # # msg.body = str(otp)  
    # mail.send(msg)  
    
    if request.method == "POST":
        user_otp = request.form['otp']  
        if otp == int(user_otp):
            print(f'otp = {otp}')
            print(f'user_otp = {user_otp}')
            # message = "Email  verification is  successful"
            # return redirect(url_for('homepage'))
            db.session.query(User).filter_by(email=email).update({'is_confirmed':True})
            db.session.commit()
            return "<h3> Email  verification is  successful </h3>"  
        return "<h3>failure, OTP does not match</h3>"

    # email_exists = db.session.query(User).filter_by(email=email).first()
    # user_exists = db.session.query(User).filter_by(username=username).first()   
    # valid_email = check(email)

    # with mail.connect() as conn:
    #     email = request.form["email"]   
    #     msg = Message('Password Reset Request',sender='fitemail420@gmail.com',recipients=[email])
    #     msg.body = 'To reset your password, visit the following link: ' + "link" + '. If you did not make this request then simply ignore this email and no changes will be made.'
    #     conn.send(msg)

    return render_template('v2.html')

@app.route('/verify', methods=['POST'])
def verify():

    email = request.form["email"]
    message = str(otp)   
    subject = 'OTP'
    msg = Message(body=message,subject=subject,sender = 'fitemail420@gmail.com', recipients = [email])  
    # msg.body = str(otp)  
    mail.send(msg)  

    # email_exists = db.session.query(User).filter_by(email=email).first()
    # user_exists = db.session.query(User).filter_by(username=username).first()   
    # valid_email = check(email)

    # with mail.connect() as conn:
    #     email = request.form["email"]   
    #     msg = Message('Password Reset Request',sender='fitemail420@gmail.com',recipients=[email])
    #     msg.body = 'To reset your password, visit the following link: ' + "link" + '. If you did not make this request then simply ignore this email and no changes will be made.'
    #     conn.send(msg)

    return render_template('verify.html')  



# @app.route('/confirm_email/<token>', methods=['GET', 'POST'])
# def confirm_email(token):
#     try:
#         email = s.loads(token, salt='email-confirm', max_age=3600)
#     except SignatureExpired:
#         return '<h1>The token is expired!</h1>'
#     return '<h1>The token works!</h1>'



#------------------------------------------------------------- Logging in and Out-----------------------------------------------#

#------------------------------------------------------------- Account Methods ----------------------------------------------------------------#
#Profile Settings
@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

#Change Password
# @app.route('/change_password', methods=['GET', 'POST'])
# @login_required
# def change_password():
#     if current_user.is_authenticated:
#         user = db.session.query(User).filter_by(username=current_user.username).first()
#         form = ChangePasswordForm()
#     if form.validate_on_submit():
#         old_pass = form.old_pass.data
#         new_pass = form.new_pass.data
#         new_pass_retype = form.new_pass_retype.data
        
#         if user.check_password(old_pass):
#             print('old password correct', file=sys.stderr)
#             if new_pass == new_pass_retype:
#                 print('password & retype match', file=sys.stderr)
#                 user.set_password(new_pass, False)
#                 db.session.add(user)
#                 db.session.commit()
#             else:
#                 print('password & retype do not match', file=sys.stderr)
#         else:
#             print('old password incorrect', file=sys.stderr)
#         return redirect(url_for('index'))
#     '''
#     Implement this function for Activity 9.
#     Verify that old password matches and the new password and retype also match.
#     '''
#     return render_template('change_password.html', form = form)

#Create user (User Method)
@app.route('/create_user', methods=['GET', 'POST'])
def create_user(): 
    form = CreateUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        fname = form.fname.data
        lname = form.lname.data
        date_of_birth = form.date_of_birth.data
        gender = form.gender.data
        
        email_exists = db.session.query(User).filter_by(email=email).first()
        user_exists = db.session.query(User).filter_by(username=username).first()   
        valid_email = check(email)
        print(f'Valid Email? {valid_email}')
        if (email_exists is None) and (user_exists is None):
            if valid_email is True:
                message = str(otp)   
                subject = 'OTP'
                msg = Message(body=message,subject=subject,sender = 'fitemail420@gmail.com', recipients = [email])  
                mail.send(msg) 

                username = username
                print(f"username = {username}")
                password = password
                print(f"password = {password}")
                email = email
                print(f"email = {email}")
                fname = fname
                print(f"fname = {fname}")
                lname = lname
                print(f"lname = {lname}")
                date_of_birth = date_of_birth
                print(f"date_of_birth = {date_of_birth}")
                gender = gender
                print(f"gender = {gender}")
                if gender == 'Female':
                    gender = 'f'
                elif gender == 'Male':
                    gender = 'm'
                role = 'regular'
                print(f"role = {role}")
                user = User(username=username, email=email, fname=fname, lname=lname, date_of_birth=date_of_birth, gender=gender, role='regular', is_confirmed=False)
                user.set_password(password, False)
                db.session.add(user)
                db.session.commit()

                # user = User(username=username, email=email, fname=fname, lname=lname, date_of_birth=date_of_birth, role='regular', gender=gender)
                # password = user.set_password(password, True)
                return render_template('verify.html', email=email)
            else: 
               flash("email is not valid") 
        else:
            # print("user already exists", file=sys.stderr)
            flash("user already exists")
        
    all_usernames= db.session.query(User.username).all()
    print(all_usernames, file=sys.stderr)
    return render_template('create_user.html', form=form)


@app.route('/validate/<email>',methods=["POST"])   
def validate(email):  
    if request.method == "POST":
        email = email
        print(f"email = {email}")
        # fname = fname
        # print(f"fname = {fname}")
        # lname = lname
        # print(f"lname = {lname}")
        # date_of_birth = date_of_birth
        # print(f"date_of_birth = {date_of_birth}")
        # gender = gender
        # print(f"gender = {gender}")
        # if gender == 'Female':
        #     gender = 'f'
        # elif gender == 'Male':
        #     gender = 'm'
        # role = role
        # print(f"role = {role}")
        # fname=fname
        # print(f"fname = {fname}")
        #fname = v_form.fname.data
        #print(f"FIRST NAME: {fname}")
        user_otp = request.form['otp']  
        if otp == int(user_otp):  
            # current_user_id = current_user.id
            # user = User(is_confirmed=False)
            db.session.query(User).filter_by(email=email).update({'is_confirmed':True})
            # user.set_password(password, False)
            # db.session.add(user)
            db.session.commit()
            result = "Email verification is successful"
            return render_template('verifyResult.html', result=result)  
    result = "Failure, OTP does not match"
    return render_template('verifyResult.html', result=result) 
#------------------------------------------------------------- Account Methods ----------------------------------------------------------------#




#----------------------------------------------------------- Administrator Methods ------------------------------------------------------------#
#Admin adds an user to the database
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if is_admin():
        form = AddUserForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            email = form.email.data
            fname = form.fname.data
            lname = form.lname.data
            gender = form.gender.data
            date_of_birth = form.date_of_birth.data
            role = 'regular'
            

            email_exists = db.session.query(User).filter_by(email=email).first()
            user_exists = db.session.query(User).filter_by(username=username).first()   
            valid_email = check(email)
            print(f'Valid Email? {valid_email}')
            if (email_exists is None) and (user_exists is None):
                if valid_email is True:
                    user = User(username=username, email=email, fname=fname, lname=lname, gender=gender, date_of_birth=date_of_birth, role=role)
                    user.set_password(password, False)
                    db.session.add(user)
                    
                    db.session.commit()
                    flash('User added successfully')
                else:
                    flash("email is not valid") 
            else:
                # print("user already exists", file=sys.stderr)
                flash("user already exists")
            
        all_usernames= db.session.query(User.username).all()
        print(all_usernames, file=sys.stderr)
        return render_template('add_user.html', form=form)
    return render_template('invalid_credentials.html')

@app.route('/delete_user/<user_id>', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):

    friends1 = db.session.query(Friend).filter_by(fk_user_id=user_id)
    friends1 = friends1.all()
    len_friends1 = len(friends1)
    friends2 = db.session.query(Friend).filter_by(fk_friend_id=user_id)
    friends2 = friends2.all()
    len_friends2 = len(friends2)
    calorie = db.session.query(Calorie).filter_by(fk_user_id=user_id)
    calorie = calorie.all()
    len_calorie = len(calorie)
    exercise = db.session.query(Exercise).filter_by(fk_user_id=user_id)
    exercise = exercise.all()
    len_exercise = len(exercise)
    track = db.session.query(Track).filter_by(fk_user_id=user_id)
    track = track.all()
    len_track = len(track)
        
        # print(f'friends: {len_friends1}')
        # print(f'friends: {len_friends2}')
    for f in range(len_friends1):
        f = db.session.query(Friend).filter_by(fk_user_id=user_id).first()
        db.session.delete(f)
        db.session.commit()
    for f in range(len_friends2):
        f = db.session.query(Friend).filter_by(fk_friend_id=user_id).first()
        db.session.delete(f)
        db.session.commit()
    for c in range(len_calorie):
        c = db.session.query(Calorie).filter_by(fk_user_id=user_id).first()
        db.session.delete(c)
        db.session.commit()
    for e in range(len_exercise):
        e = db.session.query(Exercise).filter_by(fk_user_id=user_id).first()
        db.session.delete(e)
        db.session.commit()
    for t in range(len_track):
        t = db.session.query(Track).filter_by(fk_user_id=user_id).first()
        db.session.delete(t)
        db.session.commit()

    db.session.query(User).filter_by(id=user_id).delete()
    db.session.commit()
    return redirect(url_for('view_users'))
    

@app.route('/view_users', methods=['GET', 'POST'])
def view_users():
    
    query_users = []

    if is_admin():
        admin_id = current_user.id
        for item in db.session.query(User).filter(User.id!=admin_id).all():
            user = UserInfo()
            user.user_id = item.id
            user.username = item.username
            user.email = item.email
            user.role = item.role
            query_users.append(user)
        return render_template('view_users.html', query_users=query_users)
    return render_template('invalid_credentials.html')
#----------------------------------------------------------- Administrator Methods ------------------------------------------------------------#



#---------------------------------------------------------- Profiles --------------------------------------------------------------------------#
#Profile
@app.route('/profile/')
@login_required
def profile():
    if current_user.is_authenticated:
        user_id = current_user.id
        username = current_user.username
        email = current_user.email
        role = current_user.role
        fname = current_user.fname
        lname = current_user.lname
        email = current_user.email
        dob = current_user.date_of_birth
        friends = db.session.query(Friend).filter_by(fk_user_id=user_id, status=2)
        friends = friends.all()
        requests = db.session.query(Friend).filter_by(fk_user_id=user_id, status=0)
        requests = requests.all()
        sent = db.session.query(Friend).filter_by(fk_user_id=user_id, status=1)
        sent = sent.all()
        len_friends = len(friends)
        len_requests = len(requests)
        len_sent = len(sent)

        #s2 = mutual friends
        #s1 = user sent request
        #s0 = friend sent request
        query_friend_row = []
        query_requests_row = []
        query_sent_row = []
        for item in db.session.query(Friend).filter(Friend.fk_user_id==user_id):
            row = FriendInfo()
            row.row_id = item.id
            row.user_id = current_user.id
            row.f_id = item.fk_friend_id
            f_id = row.f_id
            #user_id = User.id
            name = db.session.query(User).filter_by(id=f_id).first()
            # name = row.f_name
            row.f_name = name.username
            #db.session.query(User).filter_by(username=username).first()
            row.status = item.status
            
            if row.status == 2:
                query_friend_row.append(row)
            elif row.status == 1:
                query_sent_row.append(row)
            elif row.status == 0:
                query_requests_row.append
            # print(f'row id: {row.row_id}')
            # print(f'user id: {row.user_id}')
            # print(f'friend id: {row.f_id}')
            # print(f'friend name: {row.f_name}')
            # #print(f'friend name: {name.username}')
            # print(f'status: {row.status}')
        if current_user.is_authenticated:
            current_user_id = current_user.id
        query_friend_row = []
        for item in db.session.query(Friend).filter(Friend.fk_user_id==current_user_id):
            row = FriendInfo()
            row.row_id = item.id
            row.user_id = current_user.id
            row.f_id = item.fk_friend_id
            f_id = row.f_id
            name = db.session.query(User).filter_by(id=f_id).first()
            row.f_name = name.username
            row.status = item.status
            
            if row.status == 2:
                query_friend_row.append(row)
    return render_template('profile.html', fname=fname, lname=lname, email=email, username=username, date_of_birth=dob,
                           query_friend_row=query_friend_row, friends=friends, len_friends=len_friends, query_sent_row=query_sent_row,
                           query_requests_row=query_requests_row, len_requests=len_requests, len_sent=len_sent)
    #height=height, weight=weight
    #image_file=image_file

@app.route('/search_users', methods=['GET', 'POST'])
@login_required
def search_users():
    if current_user.is_authenticated:
        current_user_id = current_user.id
        form = SearchUsers()
        request_form=FriendRequest()
        if form.validate_on_submit:
            search_username = form.username.data

            users = db.session.query(User).filter_by()
            users = users.all()
            len_users = len(users)
            #not getting all users in query below
            #for loop keeps going until it finds the user its looking for
            query_user_row = [] 
            count = 0
            for item in db.session.query(User):
                row = UserInfo()
                row.user_id = item.id
                row.username = item.username
                row.email = item.email
                row.role = item.role
                friendship = 0
                f_id = None
                # print(f"user ids: {row.user_id}")
                result = "User Not Found"
                if row.user_id != current_user_id:
                    query_user_row.append(row)
                    count+=1
                    print('++++')
                    print(row.username)
                    print(type(row.username))
                    print(search_username)
                    print(type(search_username))
                    if row.username == search_username:
                        # print("yay QUERY")
                        # print(search_username)
                        result = "User Found"
                        f_id = row.user_id
                        print(f'IN LOOP {search_username} {row.user_id}')
                        friend = Friend.query.filter_by(fk_user_id=current_user_id, fk_friend_id=f_id, status=2).first()
                        request = Friend.query.filter_by(fk_user_id=current_user_id, fk_friend_id=f_id, status=0).first()
                        sent = Friend.query.filter_by(fk_user_id=current_user_id, fk_friend_id=f_id, status=1).first()

                        print(f' {search_username} None? {friend}')
                        
                        if (friend is None) and (request is None) and (sent is None) :
                            friendship_for_user = Friend(fk_user_id=current_user_id, fk_friend_id=row.user_id, status=1)
                            friendship_for_friend = Friend(fk_user_id=row.user_id, fk_friend_id=current_user_id, status=0)
                            db.session.add(friendship_for_user)
                            db.session.add(friendship_for_friend)
                            db.session.commit()
                            friendship = 3
                            break
                        elif (friend is not None) and (request is None) and (sent is None) :
                            friendship = 2
                            break
                        elif (friend is None) and (request is not None) and (sent is None) :
                            friendship = 0
                            break
                        elif (friend is None) and (request is None) and (sent is not None) :
                            friendship = 1
                            break                       
                        
                    elif (row.username != search_username) and ((len_users-1) == count) and (search_username != None):
                        print(f'RESULT {result} {search_username}')
                        print(f'EQUALS? {row.username == search_username}')
                        flash(result)
                        # flash(len_users)
                        # flash(count)
              


            # if search_username in users:
            #     print("yay USERS")
            #     print(search_username)
            # else:
            #     print("fuck USERS") 
            #     print(search_username)
        

        all_user_row = [] 
        for item in db.session.query(User):
            row = UserInfo()
            row.user_id = item.id
            row.username = item.username
            row.email = item.email
            row.role = item.role
            # f_id = row.f_id
            print(f"user ids: {row.user_id}")
            if row.user_id != current_user_id:
                all_user_row.append(row)
        
    print(f'END OF CODE\n\tresult = {result}\n\tfriendship = {friendship}\n\tf_id = {f_id}')    
    return render_template('search_users.html', query_user_row=query_user_row, users=users, len_users=len_users, form=form, all_user_row=all_user_row, result=result, search_username=search_username, request_form=request_form, friendship=friendship, f_id=f_id)


@app.route('/view_friends', methods=['GET', 'POST'])
@login_required
def view_friends():
    if current_user.is_authenticated:
        current_user_id = current_user.id
        query_friend_row = []
        for item in db.session.query(Friend).filter(Friend.fk_user_id==current_user_id):
            row = FriendInfo()
            row.row_id = item.id
            row.user_id = current_user.id
            row.f_id = item.fk_friend_id
            f_id = row.f_id
            name = db.session.query(User).filter_by(id=f_id).first()
            row.f_name = name.username
            row.status = item.status
            
            if row.status == 2:
                query_friend_row.append(row)
        
        return render_template('friends.html', query_friend_row=query_friend_row)

@app.route('/view_requests', methods=['GET', 'POST'])
@login_required
def view_requests():
    if current_user.is_authenticated:
        current_user_id = current_user.id
        query_requests_row = []

        for item in db.session.query(Friend).filter(Friend.fk_user_id==current_user_id):
            row = FriendInfo()
            row.row_id = item.id
            row.user_id = current_user.id
            row.f_id = item.fk_friend_id
            f_id = row.f_id
            name = db.session.query(User).filter_by(id=f_id).first()
            row.f_name = name.username
            row.status = item.status
            
            if row.status == 0:
                query_requests_row.append(row)
                                 
        return render_template('requests.html', query_requests_row=query_requests_row)

@app.route('/accept_friend/<friend_id>', methods=['GET', 'POST'])
@login_required
def accept_friend(friend_id):
    if current_user.is_authenticated:
        current_user_id = current_user.id
        friend = Friend.query.filter_by(fk_user_id=current_user_id, fk_friend_id=friend_id).first()
        if friend is not None:
            # friendship_for_user = Friend(fk_user_id=current_user_id, fk_friend_id=friend_id, status=2)
            # friendship_for_friend = Friend(fk_user_id=friend_id, fk_friend_id=current_user_id, status=2)
            # db.session.update(friendship_for_user)
            # db.session.update(friendship_for_friend)
            # 
            db.session.query(Friend).filter_by(fk_user_id=current_user_id, fk_friend_id=friend_id).update({'status':2})
            db.session.query(Friend).filter_by(fk_user_id=friend_id, fk_friend_id=current_user_id).update({'status':2})
            db.session.commit()
    return render_template('requests.html')

@app.route('/decline_friend/<friend_id>', methods=['GET', 'POST'])
@login_required
def decline_friend(friend_id):
    if current_user.is_authenticated:
        current_user_id = current_user.id
        friend = Friend.query.filter_by(fk_user_id=current_user_id, fk_friend_id=friend_id).first()
        if friend is not None:
            db.session.query(Friend).filter_by(fk_user_id=friend_id, fk_friend_id=current_user_id, status=1).delete()
            db.session.query(Friend).filter_by(fk_user_id=current_user_id, fk_friend_id=friend_id, status=0).delete()
            db.session.commit()
    return render_template('requests.html')

@app.route('/remove_friend/<friend_id>', methods=['GET', 'POST'])
@login_required
def remove_friend(friend_id):
    if current_user.is_authenticated:
        current_user_id = current_user.id
        friend = Friend.query.filter_by(fk_user_id=current_user_id, fk_friend_id=friend_id).first()
        if friend is not None:
            db.session.query(Friend).filter_by(fk_user_id=friend_id, fk_friend_id=current_user_id, status=2).delete()
            db.session.query(Friend).filter_by(fk_user_id=current_user_id, fk_friend_id=friend_id, status=2).delete()
            db.session.commit()
    return redirect(url_for('profile'))

@app.route('/friend_profile/<friend_id>', methods=['GET', 'POST'])
@login_required
def friend_profile(friend_id):
    if current_user.is_authenticated:
        current_user_id = current_user.id
        #f_id = friend_id
        query_friend_row = []
        for item in db.session.query(Friend).filter(Friend.fk_user_id==current_user_id):
            row = FriendInfo()
            row.row_id = item.id
            row.user_id = current_user.id
            row.f_id = item.fk_friend_id
            f_id = row.f_id
            name = db.session.query(User).filter_by(id=f_id).first()
            row.f_name = name.username
            row.status = item.status
            row.first_name = name.fname
            row.last_name = name.lname

            friend_id = int(friend_id)

            if (row.status == 2) and (row.f_id == friend_id):
                query_friend_row.append(row)
                break
        query_friend_row = query_friend_row[0]
        return render_template('view_friend_profile.html', query_friend_row=query_friend_row, f_id=f_id)
        
@app.route('/account_recovery', methods=['GET'])
def recover_account():
    return render_template("account_recovery.html") 
    # form = AccountRecovery()
    # if form.validate_on_submit():
    #     # username = form.username.data
    #     email = form.email.data
    #     valid_email = check(email)
    #     # newPassword = form.newPassword.data
    #     # newPassword_retype = form.newPassword_retype.data
    #     if (db.session.query(User).filter_by(email=email).first()):
    #         if valid_email is True:
    #             # if newPassword == newPassword_retype:
    #             #     user = db.session.query(User).filter_by(username=username).first()
    #             #     password = db.session.query(User.password_hash).first()
    #             #     print("TEST")
    #             #     print(password)
    #             #     user.set_password(newPassword, False)
    #             #     db.session.add(user)
    #             #     db.session.commit()
    #             #     return redirect(url_for('login'))
    #             message = str(otp)   
    #             subject = 'OTP'
    #             msg = Message(body=message,subject=subject,sender = 'fitemail420@gmail.com', recipients = [email])  
    #             mail.send(msg)
    #             return render_template('verify_recover.html', email=email)
    #             # return redirect(url_for('validate_recovery', email=email))
    #         else: 
    #            print("email is not valid") 
    #     else:
    #         print("email is not associated with an account") 

    # return render_template('account_recovery.html', form=form)

@app.route('/verify_recovery', methods=['POST'])
def verify_recovery():

    email = request.form["email"]
    message = str(otp)   
    subject = 'OTP'
    msg = Message(body=message,subject=subject,sender = 'fitemail420@gmail.com', recipients = [email])  
    # msg.body = str(otp)  
    mail.send(msg)  

    # with mail.connect() as conn:
    #     email = request.form["email"]   
    #     msg = Message('Password Reset Request',sender='fitemail420@gmail.com',recipients=[email])
    #     msg.body = 'To reset your password, visit the following link: ' + "link" + '. If you did not make this request then simply ignore this email and no changes will be made.'
    #     conn.send(msg)

    return render_template('verify_recover.html', email=email)

@app.route('/validate_recovery/<email>',methods=["POST"])   
def validate_recovery(email):  
    if request.method == "POST":
        form = ChangePasswordForm()
        email = email
        print(f"email = {email}")
        
        user_otp = request.form['otp']  
        if otp == int(user_otp):
            print(f'otp = {otp}')
            print(f'user_otp = {user_otp}')
            # message = "Email  verification is  successful"
            return render_template('change_pass.html', form=form)
    return "<h3>failure, OTP does not match</h3>" 

@app.route('/change_password/<email>',methods=["POST"])   
def change_password(email):  
    if request.method == "POST":
        form = ChangePasswordForm()
        email = email
        print(f"email = {email}")
        if form.validate_on_submit():
            new_pass = form.new_pass.data
            new_pass_retype = form.new_pass_retype.data
            if new_pass == new_pass_retype:
                
                user = db.session.query(User).filter_by(email=email).first()
                user.check_password(new_pass)
                if not user.check_password(new_pass):
                    #user = db.session.query(User).filter_by(email=email).first()
                    password = user.set_password(new_pass, False)
                    # update = update(User)
                    # update = update.values({"password": })
                    # update = User.query.filter_by(email=email).update(dict(password=password))
                    db.session.add(user)
                    db.session.commit()
                    flash("Password Changed")
                    # print('password & retype match', file=sys.stderr)
                    # user.set_password(new_pass, False)
                    # db.session.add(user)
                    # db.session.commit()
                    return redirect(url_for('login'))
                else:
                    flash("cannot use previous password")
            else:
                flash("Passwords do not match")
    return render_template('change_pass.html', form=form)
#Edit
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user_id = current_user.id
    form = EditProfileForm()
    friends = db.session.query(Friend).filter_by(fk_user_id=user_id, status=2)
    friends = friends.all()
    requests = db.session.query(Friend).filter_by(fk_user_id=user_id, status=0)
    requests = requests.all()
    sent = db.session.query(Friend).filter_by(fk_user_id=user_id, status=1)
    sent = sent.all()
    len_friends = len(friends)
    len_requests = len(requests)
    len_sent = len(sent)

    #s2 = mutual friends
    #s1 = user sent request
    #s0 = friend sent request
    query_friend_row = []
    query_requests_row = []
    query_sent_row = []
    for item in db.session.query(Friend).filter(Friend.fk_user_id==user_id):
        row = FriendInfo()
        row.row_id = item.id
        row.user_id = current_user.id
        row.f_id = item.fk_friend_id
        f_id = row.f_id
        #user_id = User.id
        name = db.session.query(User).filter_by(id=f_id).first()
        # name = row.f_name
        row.f_name = name.username
        #db.session.query(User).filter_by(username=username).first()
        row.status = item.status
        
        if row.status == 2:
            query_friend_row.append(row)
        elif row.status == 1:
            query_sent_row.append(row)
        elif row.status == 0:
            query_requests_row.append
        # print(f'row id: {row.row_id}')
        # print(f'user id: {row.user_id}')
        # print(f'friend id: {row.f_id}')
        # print(f'friend name: {row.f_name}')
        # #print(f'friend name: {name.username}')
        # print(f'status: {row.status}')
    if current_user.is_authenticated:
        current_user_id = current_user.id
    query_friend_row = []
    for item in db.session.query(Friend).filter(Friend.fk_user_id==current_user_id):
        row = FriendInfo()
        row.row_id = item.id
        row.user_id = current_user.id
        row.f_id = item.fk_friend_id
        f_id = row.f_id
        name = db.session.query(User).filter_by(id=f_id).first()
        row.f_name = name.username
        row.status = item.status
        
        if row.status == 2:
            query_friend_row.append(row)
    if form.validate_on_submit():
        #---------------------------# 
        fname = form.fname.data
        lname = form.lname.data
        #height = form.height.data
        #weight = form.weight.data
        #---------------------------# 
        if fname == '':
            current_user.fname = current_user.fname
        else:
            current_user.fname = fname

        if lname == '':
            current_user.lname = current_user.lname
        else:
            current_user.lname = lname

        # if height == '':
        #     current_user.height = current_user.height
        # else:
        #     current_user.height = height

        # if weight == '':
        #     current_user.weight = current_user.weight
        # else:
        #     current_user.weight = weight

        db.session.add(current_user)
        db.session.commit()

        return redirect(url_for('profile'))
    image_file = url_for('static', filename='images/' + 'profile.png')
    return render_template('edit_profile.html', form=form, image_file=image_file, query_friend_row=query_friend_row, friends=friends, len_friends=len_friends, query_sent_row=query_sent_row,
                           query_requests_row=query_requests_row, len_requests=len_requests, len_sent=len_sent)
  

#Workouts
@app.route('/workouts', methods=['GET', 'POST'])
@login_required
def workouts():
    user_id = current_user.id
    form = WorkoutNameSearch()
    if request.method == "GET":
        workouts = db.session.query(Exercise).filter_by(fk_user_id=user_id)
        if len(request.args) > 0:
            date_of_workout = request.args.get('date')
            if date_of_workout is not None:
                workouts = workouts.filter_by(e_input_date=date_of_workout)
            exercise_name = request.args.get('name')
            if exercise_name is not None:
                workouts = workouts.filter_by(e_name=exercise_name)
            
            workouts = workouts.all()
        return render_template('workouts.html', workouts=workouts, form=form)

@app.route('/workouts_api', methods=['GET'])
@login_required
def ninja_api_search_by_activity():
    if request.method == "GET":
        activity = request.args.get('activity')
        response = requests.get(f"{CALORIES_API_URL}?activity={activity}", headers={'X-Api-Key': API_KEY})
        response_data = response.json()
        for ex in response_data:
            del ex['total_calories']

        if response.status_code != requests.codes.ok:
            return Response({
            "status": "error", 
            "message": "Got an error from API"
            }, mimetype="application/json")
    return Response(json.dumps(response_data),  mimetype='application/json')

@app.route('/food_api', methods=['GET'])
@login_required
def ninja_api_search_by_food():
    if request.method == "GET":
        user_id = current_user.id 
        food_name = request.args.get('name')
        response = requests.get(f"{NUTRITION_API_URL}?query={food_name}", headers={'X-Api-Key': API_KEY})
        response_data = response.json()

        if response.status_code != requests.codes.ok:
            return Response({
            "status": "error", 
            "message": "Got an error from API"
            }, mimetype="application/json")
                
    return Response(json.dumps(response_data),  mimetype='application/json')

@app.route('/add_food', methods=['POST'])
@login_required
def add_food():
    if request.method == "POST":
        form_data = request.json
        c_name = form_data['name']
        if not c_name: raise "name missing"

        c_total_calories = form_data['calories']
        c_total_calories_NEW = c_total_calories
        c_serving_size_g = form_data['serving_size_g']
        c_fat_saturated_g = form_data['fat_saturated_g']
        c_protein_g = form_data['protein_g']
        c_sodium_mg = form_data['sodium_mg']
        c_potassium_mg = form_data['potassium_mg']
        c_cholesterol_mg = form_data['cholesterol_mg']
        c_carbohydrates_total_g = form_data['carbohydrates_total_g']
        c_fiber_g = form_data['fiber_g']
        c_sugar_g = form_data['sugar_g']


        calorie = Calorie(fk_user_id=current_user.id,
                                c_name =c_name,
                                c_input_date=date.today(),
                                c_total_calories = c_total_calories,
                                c_total_calories_NEW = c_total_calories_NEW,
                                c_serving_size_g = c_serving_size_g,
                                c_fat_saturated_g = c_fat_saturated_g,
                                c_protein_g = c_protein_g,
                                c_sodium_mg = c_sodium_mg,
                                c_potassium_mg = c_potassium_mg,
                                c_cholesterol_mg = c_cholesterol_mg,
                                c_carbohydrates_total_g = c_carbohydrates_total_g,
                                c_fiber_g = c_fiber_g,
                                c_sugar_g = c_sugar_g)
        
        try:
            db.session.add(calorie)
            db.session.commit()
            response_data = {
                    "status": "success", 
                    "message": "Added calorie data",
                    "data": {
                        "name": calorie.c_name,
                        "serving_size": calorie.c_serving_size_g,
                        "calories": calorie.c_total_calories,
                        "id": calorie.id
                    }
                    }
            return Response(json.dumps(response_data),  mimetype='application/json')
            
        except Exception as error:
            print(error)
            response_data = {
                "status": "error", 
                "message": str(error)
                }
            return Response(json.dumps(response_data), status=500, mimetype='application/json')
        
@app.route('/add_workout', methods=['POST'])
@login_required
def add_workout():
    if request.method == "POST":
        form_data = request.json
        e_name = form_data['name']
        if not e_name: raise "name missing"

        e_total_calories_per_hour = form_data['calories_per_hour']
        e_duration_minutes = form_data['duration_minutes']
        e_total_calories = e_total_calories_per_hour * (e_duration_minutes/60)
        e_total_calories_NEW = e_total_calories

        exercise = Exercise(fk_user_id=current_user.id,
                            e_name = e_name,
                            e_input_date=date.today(),
                            e_total_calories = e_total_calories,
                            e_calories_per_hour = e_total_calories_per_hour,
                            e_duration_minutes = e_duration_minutes,
                            e_total_calories_NEW=e_total_calories_NEW)
        
        try:
            db.session.add(exercise)
            db.session.commit()
            response_data = {
                    "status": "success", 
                    "message": "Added exercise data",
                    "data": {
                        "name": exercise.e_name,
                        "calories": exercise.e_total_calories,
                        "perHour": exercise.e_calories_per_hour,
                        "duration": exercise.e_duration_minutes,
                        "id": exercise.id
                    }
                    }
            return Response(json.dumps(response_data),  mimetype='application/json')
        
        except Exception as error:
            print(error)
            response_data = {
                "status": "error", 
                "message": str(error)
                }
            return Response(json.dumps(response_data), status=500, mimetype='application/json')

            

#graphs for users progress
@app.route('/graph')
@login_required
def graph():
    plt.switch_backend('PDF')
    plt.switch_backend('PDF')
    #connecting to the database 
    IP = environ.get('MYSQL_IP')
    USERNAME = environ.get('MYSQL_USER')
    PASSWORD = environ.get('MYSQL_PASS')
    DB_NAME = environ.get('MYSQL_DB')
    DB_CONFIG_STR = f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{IP}/{DB_NAME}"
    engine = create_engine(DB_CONFIG_STR)
    
    calories_df = pd.read_sql(
    text(f"SELECT c_input_date, c_total_calories FROM calorie WHERE fk_user_id = {current_user.id}"),
    con=engine.connect())

    exercises_df = pd.read_sql(
    text(f"SELECT e_input_date, e_total_calories FROM exercise WHERE fk_user_id = {current_user.id}"),
    con=engine.connect())

    plt.plot("c_input_date", "c_total_calories", data=calories_df, label="calories consumed", color='#A469D8')
    plt.plot("e_input_date", "e_total_calories", data=exercises_df, label="calories burned", color='#000000')

    plt.xlabel("Date",  size = 20)
    plt.ylabel("Calories", size = 20)
    plt.legend()
    plt.savefig(path.join(app.root_path, 'static', 'graphs', f"{current_user.id}-graph.png"))
    user = current_user.id
    #return f"<html><body><img src='/static/graphs/{current_user.id}-graph.png' /></body></html>"
    return render_template('graph.html', user=user)

@app.route('/friendGraph/<friend_id>')
@login_required
def friendGraph(friend_id):
    plt.switch_backend('PDF')
    plt.switch_backend('PDF')
    #connecting to the database 
    IP = environ.get('MYSQL_IP')
    USERNAME = environ.get('MYSQL_USER')
    PASSWORD = environ.get('MYSQL_PASS')
    DB_NAME = environ.get('MYSQL_DB')
    DB_CONFIG_STR = f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{IP}/{DB_NAME}"
    engine = create_engine(DB_CONFIG_STR)
    
    calories_df = pd.read_sql(
    text(f"SELECT c_input_date, c_total_calories FROM calorie WHERE fk_user_id = {friend_id}"),
    con=engine.connect())

    exercises_df = pd.read_sql(
    text(f"SELECT e_input_date, e_total_calories FROM exercise WHERE fk_user_id = {friend_id}"),
    con=engine.connect())

    plt.plot("c_input_date", "c_total_calories", data=calories_df, label="calories consumed", color='#A469D8')
    plt.plot("e_input_date", "e_total_calories", data=exercises_df, label="calories burned", color='#000000')

    plt.xlabel("Date",  size = 20)
    plt.ylabel("Calories", size = 20)
    plt.legend()
    plt.savefig(path.join(app.root_path, 'static', 'graphs', f"{friend_id}-graph.png"))
    #return f"<html><body><img src='/static/graphs/{current_user.id}-graph.png' /></body></html>"
    return render_template('friendGraph.html', friend_id=friend_id)
#---------------------App Error--------------------------------------------------------------------#

#page not found
@app.errorhandler(404)
def error404(error):
    return render_template('404.html'), 404

#failed db conenction
@app.errorhandler(500)
def error500(error):
    return render_template('500.html'), 500
#---------------------App Error--------------------------------------------------------------------#



#-----------STANDALONE FUNCTION SECTION--------------#
#Role Validation-------------------------------------#
def is_admin():
    '''
    Helper function to determine if authenticated user is an admin.
    '''
    if current_user:
        if current_user.role == 'admin':
            return True
        else:
            return False
    else:
        print('User not authenticated.', file=sys.stderr)

def is_regular():
    if current_user:
        if current_user.role == "regular":
            return True
        else:
            return False
#---------------------------------------------------#
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
 
def check(email):
    try:
      # validate and get info
        v = validate_email(email)
        # replace with normalized form
        email = v["email"] 
        return True
    except EmailNotValidError as e:
        # email is not valid, exception message is human-readable
        print(str(e))
        return False




