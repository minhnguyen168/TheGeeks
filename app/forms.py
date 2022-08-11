from flask_wtf import FlaskForm 
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, RadioField, SelectField, IntegerField
from wtforms.fields import DateField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError, DataRequired, NumberRange
from app.models import (User)
from flask_login import current_user



class ClientRegistrationForm(FlaskForm):
    name =  StringField("Name", validators=[InputRequired(), Length(min=2, max=20)])
    #name =  StringField("Name", validators=[Required(), Length(min=1, max=40)]) 
    nric = StringField("NRIC", validators=[InputRequired(), Length(min=2, max=20)]) 
    email = StringField('Email', validators=[InputRequired(), Email()]) 
    password = PasswordField('Password', validators=[InputRequired()])
    #contactno = StringField('Contact No.', validators=[Required(), Length(min=8, max=8)]) 

    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up') 
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first() 
        if user:
            raise ValidationError('That email is already registered. Please login with your registered account.')

class ClientLoginForm(FlaskForm):
    email =  StringField("Email", validators=[InputRequired(), Email()]) 

    password = PasswordField('Password', validators=[InputRequired()])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login') 

# class UserUpdateAccountForm(FlaskForm):
#     email = StringField('Email', validators=[Required(), Email()]) 

#     password = PasswordField('Password', validators=[Required()]) 
#     confirm_password = PasswordField('Confirm Password', validators=[Required(), EqualTo('password')])

#     submit = SubmitField('Update') 

class BankerRegistrationForm(FlaskForm):
    name =  StringField("Name", validators=[InputRequired(), Length(min=2, max=20)])
    #name =  StringField("Name", validators=[Required(), Length(min=1, max=40)]) 
    nric = StringField("NRIC", validators=[InputRequired(), Length(min=2, max=20)]) 
    email = StringField('Email', validators=[InputRequired(), Email()]) 
    password = PasswordField('Password', validators=[InputRequired()])
    #contactno = StringField('Contact No.', validators=[Required(), Length(min=8, max=8)]) 

    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up') 
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first() 
        if user:
            raise ValidationError('That email is already registered. Please login with your registered account.')

class BankerLoginForm(FlaskForm):
    email =  StringField("Email", validators=[InputRequired(), Email()]) 

    password = PasswordField('Password', validators=[InputRequired()])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login') 


class NewsFilterForm(FlaskForm):
    startdate = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    enddate = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit')

class FinancialGoalForm(FlaskForm):
    investmentgoal = SelectField("Investment Goals", validators=[InputRequired()], choices=['House','Car','Children Education','Retirement','General Investment'])
    yeartorealisegoal = IntegerField("I want to realise my goal in ...", validators=[InputRequired(), NumberRange(min=1,max=100)],render_kw={"placeholder": "Years"})
    endgoal = IntegerField("My goal requires...", validators=[InputRequired()],render_kw={"placeholder": "$"})
    age = IntegerField("I am ", validators=[InputRequired()],render_kw={"placeholder": "years old"})
    annualincome = IntegerField("My annual income (including other sources of income such as rental income) is approximately $", validators=[InputRequired()])
    estimatednetworth = IntegerField("My estimated net worth is approximately $", validators=[InputRequired()])
    initialamount = IntegerField("I am looking to invest an initial amount of $", validators=[InputRequired()])
    topupamountmonthly = IntegerField("Each month, I am looking to invest $", validators=[InputRequired()])
    valueofcurrentinvestment = IntegerField("The estimated value of my current investment portfolio is $", validators=[InputRequired()])
    # equity = 
    # fixedincome = 
    # forexcommodities = 
    # mutualfund = 
    # crypto = 
    # realestate = 
    # otherinvestment = 
    # prioritiesofinvestment = 
    # riskappetite = 
    # dropvalue = 
    