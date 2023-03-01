#Imports
from operator import methodcaller
#from app import app as appl
from app import app
#-------environment-------#
from dotenv import load_dotenv
from os import environ
#------SQLAlchemy---------#
from app import db
from app.models import *
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

from flask_wtf.file import FileField
import json

# #API 
#------------------------------------------------------------ API ----------------------------------------------------------------#
#API_KEY=environ.get('API_KEY')
#API_HOST=environ.get('API_HOST')
#CALORIES_API_URL= environ.get('CALORIES_API_URL')
#NUTRITION_API_URL= environ.get('NUTRITION_API_URL')
#EMAIL= environ.get('EMAIL')
EMAIL='k.bevis01@gmail.com'
API_HOST='https://api-ninjas.com/'
API_KEY='lAoyv2xDhzmedTOJc6bn9A==XUdmv84oWvckWrhN'
#---------------------------------workout----------------------------------------------------------------------------------
CALORIES_API_URL='https://api.api-ninjas.com/v1/caloriesburned'
#--------------------------------nutrition---------------------------------------------------------------------------------
NUTRITION_API_URL='https://api.api-ninjas.com/v1/nutrition'



#------------------------------------------------------------ Static Webpages ----------------------------------------------------------------#
@app.route('/homepage')
def homepage():
    return render_template('homepage.html')
  
  
@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html')
#------------------------------------------------------------ Static Webpages ----------------------------------------------------------------#



#------------------------------------------------------------- Logging in and Out-----------------------------------------------#
#Start with here
@app.route('/')
def index():
    return redirect(url_for('login'))
    
#Login Method
@app.route('/login', methods=['GET', 'POST'])
def login():
    #Authenticated users are redirected to home page.
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
        
    form = LoginForm()
    if form.validate_on_submit():
        # Query DB for user by username
        user = db.session.query(User).filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            print('Login failed', file=sys.stderr)
            flash("Wrong username and/or password. Please make sure your account details are correct and try again.")
            return redirect(url_for('login'))
        # login_user is a flask_login function that starts a session
        else:
            login_user(user)
            print('Login successful', file=sys.stderr)
            return redirect(url_for('homepage'))
    return render_template('login.html', form=form)

#Logging out
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
#------------------------------------------------------------- Logging in and Out-----------------------------------------------#




#------------------------------------------------------------- Account Methods ----------------------------------------------------------------#
#Profile Settings
@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

#Change Password
@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if current_user.is_authenticated:
        user = db.session.query(User).filter_by(username=current_user.username).first()
        form = ChangePasswordForm()
    if form.validate_on_submit():
        old_pass = form.old_pass.data
        new_pass = form.new_pass.data
        new_pass_retype = form.new_pass_retype.data
        
        if user.check_password(old_pass):
            print('old password correct', file=sys.stderr)
            if new_pass == new_pass_retype:
                print('password & retype match', file=sys.stderr)
                user.set_password(new_pass)
                db.session.add(user)
                db.session.commit()
            else:
                print('password & retype do not match', file=sys.stderr)
        else:
            print('old password incorrect', file=sys.stderr)
        return redirect(url_for('index'))
    '''
    Implement this function for Activity 9.
    Verify that old password matches and the new password and retype also match.
    '''
    return render_template('change_password.html', form = form)
  
  
#Create user (User Method)
@app.route('/create_user', methods=['GET', 'POST'])
def create_user(): 
    form = CreateUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        role = form.role.data
        fname = form.fname.data
        lname = form.lname.data
        mname = form.mname.data
        company_name = form.company_name.data
        date_of_birth = form.date_of_birth.data
        
        email_exists = db.session.query(User).filter_by(email=email).first()
        user_exists = db.session.query(User).filter_by(username=username).first()   
        if (email_exists is None) and (user_exists is None):
            user = User(username=username, email=email, role=role, fname=fname, lname=lname, mname=mname,date_of_birth=date_of_birth)
            user.set_password(password)
            db.session.add(user)
            if role == 'recruiter': 
                Comp_exist = Company.query.filter_by(company_name=company_name).first()
                if Comp_exist is None:
                    company = Company(company_name=company_name)
                    db.session.add(company)
                else:
                    company = db.session.query(Company.id).filter_by(company_name=company_name).first()
                if (user is not None and company is not None) and Recruiter.query.filter_by(fk_user_id=user.id, fk_company_id=company.id).first() is None:
                    recruiter_Add=Recruiter(fk_user_id=user.id, fk_company_id=company.id)
                    db.session.add(recruiter_Add)
                    db.session.commit()
            
            
            db.session.commit()
            
            return redirect(url_for('login'))
        else:
            # print("user already exists", file=sys.stderr)
            flash("user already exists")
        
        
    all_usernames= db.session.query(User.username).all()
    print(all_usernames, file=sys.stderr)
    return render_template('create_user.html', form=form)

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
            #mname = form.mname.data
            role = form.role.data
            company_name = form.company_name.data 
            date_of_birth = form.date_of_birth.data
            

            email_exists = db.session.query(User).filter_by(email=email).first()
            user_exists = db.session.query(User).filter_by(username=username).first()   
            if (email_exists is None) and (user_exists is None):
                user = User(username=username, email=email, role=role, fname=fname, lname=lname, mname=mname, date_of_birth=date_of_birth)
                user.set_password(password)
                db.session.add(user)
                if role == 'recruiter': 
                    Comp_exist = Company.query.filter_by(company_name=company_name).first()
                    if Comp_exist is None:
                        company = Company(company_name=company_name)
                        db.session.add(company)
                    else:
                        company = db.session.query(Company.id).filter_by(company_name=company_name).first()
                    if (user is not None and company is not None) and Recruiter.query.filter_by(fk_user_id=user.id, fk_company_id=company.id).first() is None:
                        recruiter_Add=Recruiter(fk_user_id=user.id, fk_company_id=company.id)
                        db.session.add(recruiter_Add)
                        db.session.commit()
                db.session.commit()
                flash('User added successfully')
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
    form = RemoveUser()
    if form.validate_on_submit():
        is_recruiter = db.session.query(Recruiter.id).filter_by(fk_user_id=user_id).first()
        is_student = db.session.query(User.id).filter_by(id=user_id, role='student').first()
        if is_recruiter:
            for item in db.session.query(Job).filter_by(fk_recruiter_id=is_recruiter.id):
                db.session.query(Associations_Application).filter_by(fk_job_id=item.id).delete()
            db.session.query(Job).filter_by(fk_recruiter_id=is_recruiter.id).delete()
            db.session.query(Recruiter).filter_by(fk_user_id=user_id).delete()
            db.session.query(User).filter_by(id=user_id).delete()
            db.session.commit()
        elif is_student:
            db.session.query(Associations_Application).filter_by(fk_user_id=is_student.id).delete()
            db.session.query(Upload).filter_by(user_id=user_id).delete()
            db.session.query(User).filter_by(id=user_id).delete()   
            db.session.commit()
        else:
            db.session.query(User).filter_by(id=user_id).delete()
            db.session.commit()
        # Job.query.filter(id=job_id).delete()
        return redirect(url_for('view_users'))

    return render_template('close_job.html', form=form)

@app.route('/view_users', methods=['GET', 'POST'])
def view_users():
    query_users = []
    # Rec_id = db.session.query(Recruiter.id).filter_by(fk_user_id=current_user.id)
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
        username = current_user.username
        email = current_user.email
        role = current_user.role
        fname = current_user.fname
        lname = current_user.lname

        dob = current_user.date_of_birth

    return render_template('profile.html', fname=fname, lname=lname, email=email, username=username, 
                            date_of_birth=dob, role=role)

@app.route('/account_recovery', methods=['GET', 'POST'])
def recover_account():
    form = AccountRecovery()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        if (db.session.query(User).filter_by(username=username).first()) and (db.session.query(User).filter_by(email=email).first()):
            password = db.session.query(User.password_hash).first()
            print(password)
    return render_template('account_recovery.html', form=form)
    
    
#Edit
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(state=current_user.state, user_bio=current_user.user_bio)
    if form.validate_on_submit():
        #---------------------------# 
        address = form.address.data
        city = form.city.data
        state = form.state.data
        zip_code = form.zip_code.data
        #---------------------------# 
        phone_number = form.phone_number.data
        fname = form.fname.data
        mname = form.mname.data
        lname = form.lname.data
        user_bio = form.user_bio.data
        #---------------------------# 
        if fname == '':
            current_user.fname = current_user.fname
        else:
            current_user.fname = fname
            
        if mname == '':
            current_user.mname = current_user.mname
        else:
            current_user.mname = mname

        if lname == '':
            current_user.lname = current_user.lname
        else:
            current_user.lname = lname

        if zip_code == '':
            current_user.zip_code = current_user.zip_code
        else:
            current_user.zip_code = zip_code

        if phone_number == '':
            current_user.phone_number = current_user.phone_number
        else:
            current_user.phone_number = phone_number

        if user_bio == '':
            current_user.user_bio = current_user.user_bio
        else:
            current_user.user_bio = user_bio

        if state == '':
            current_user.state = current_user.state
        else:
            current_user.state = state

        if city == '':
            current_user.city = current_user.city       
        else:
            current_user.city = city

        if address == '':
            current_user.address = current_user.address
        else:
            current_user.address = address

        db.session.add(current_user)
        db.session.commit()

        return redirect(url_for('profile'))
    image_file = url_for('static', filename='images/' + 'profile.png')
    return render_template('edit_profile.html', form=form, image_file=image_file)
  

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
        food_name = request.args.get('name')
        response = requests.get(f"{NUTRITION_API_URL}?query={food_name}", headers={'X-Api-Key': API_KEY})
        response_data = response.json()

        if response.status_code != requests.codes.ok:
            return Response({
            "status": "error", 
            "message": "Got an error from API"
            }, mimetype="application/json")
    return Response(json.dumps(response_data),  mimetype='application/json')
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







