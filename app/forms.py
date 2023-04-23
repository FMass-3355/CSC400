#imports
from wsgiref.validate import validator
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from wtforms.widgets import TextArea
from flask_wtf.file import FileField
#from app import *


#----------------------New User Creation--------------------------------------------------#
class AddUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    #role = SelectField('Role', choices=[('student', 'student'), ('faculty', 'faculty'), ('recruiter', 'recruiter'), ('regular','regular')])
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    #mname = StringField('MI')
    #company_name = StringField('Company (Not relevant if not recruiter)')
    #profile_pic = FileField('Profile Picture')
    date_of_birth = DateField('Date of Birth (YYYY/MM/DD) (In Progress)')
    gender = SelectField('Gender', choices=['', 'Male', 'Female'])
    submit = SubmitField('Create Account')

    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user:
    #         raise ValueError('TAKEN')
    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user:
    #         raise ValueError('TAKEN')
#----------------------New User Creation--------------------------------------------------#


#------------------Logging into Shrimpedin--------------------#
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message="Require a login input")])
    password = PasswordField('Password', validators=[DataRequired(message="Require a password")])
    submit = SubmitField('Sign In')
    #add the create account button
    #add the account recovery button
#------------------Logging into Shrimpedin--------------------#



#----------------------Account settings----------------------------------------------------#
class ChangePasswordForm(FlaskForm):
    new_pass = PasswordField('New Password', validators=[DataRequired(message="please enter your old password")])
    new_pass_retype = PasswordField('Retype New Password', validators=[DataRequired(message="please")])
    submit = SubmitField('Change password')

class AccountRecovery(FlaskForm):
    # username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    # newPassword = PasswordField('New Password', validators=[DataRequired()])
    # newPassword_retype = PasswordField('Retype New Password', validators=[DataRequired()])
    submit = SubmitField('Recover Account')

    
class CreateUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    fname = StringField('First Name', validators=[DataRequired()])#length(min=2, max=64) Testing stuff with min and max length
    lname = StringField('Last Name', validators=[DataRequired()])
    gender = SelectField('Gender', choices=['', 'Male', 'Female'])
    date_of_birth = DateField('Date of Birth')
    submit = SubmitField('Create Account')
    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user:
    #         raise ValueError('TAKEN')

class EditProfileForm(FlaskForm):
    # phone_number = StringField('Phone Number')
    # address = StringField('Street Address')
    # city = StringField('City')
    # state = SelectField('State', choices=['', 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 
    #                                     'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS',
    #                                      'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 
    #                                      'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 
    #                                      'WI', 'WY'])
    # zip_code = StringField('Zip Code')
    # phone_number = StringField('Phone Number')
    fname = StringField('First Name')
    # mname = StringField('Middle Initial')
    # user_bio = StringField('User Bio', widget=TextArea())
    lname = StringField('Last Name')
    #height = StringField('Height')
    #weight = StringField('Weight')
    # profile_pic = FileField('Profile Picture')
    submit = SubmitField('Update Profile')

class SearchUsers(FlaskForm):
    username = StringField('Username')
    submit = SubmitField('Search')

class FriendRequest(FlaskForm):
    friend_request = SubmitField('Send Friend Request')

class A_Friend_Request(FlaskForm):
    Accept = SubmitField('Accept')

class D_Friend_Request(FlaskForm):
    Decline = SubmitField('Decline')


class RemoveUser(FlaskForm):
    # job_id = IntegerField('Enter Job ID number', validators=[DataRequired()])
    delete = SubmitField('Delete')
#----------------------Account settings----------------------------------------------------#

class EditTracker(FlaskForm):
    c_name = StringField('Food')
    c_serving_size_g = IntegerField('Serving Size')
    c_total_calories = IntegerField('Calories')
    #c_serv = IntegerField('Serving Size')
    #c_done = BooleanField('Add Food')
    e_name = StringField('Exercise')
    e_duration_minutes = IntegerField('Minutes')
    e_total_calories = IntegerField('Exercise')
    #e_done = BooleanField('Add Exercise')
    c_submit = SubmitField('Add Food')
    e_submit = SubmitField('Add Exercise')

# --------------- Search Form -------------------------#
class WorkoutNameSearch(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    search = SubmitField('Search')
# --------------- Search Form -------------------------#
