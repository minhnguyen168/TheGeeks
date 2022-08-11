from flask_wtf import FlaskForm 
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, RadioField, SelectField, IntegerField
from wtforms.fields import DateField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError, DataRequired, NumberRange
from app.models import (User)
from flask_login import current_user
from wtforms import Form, StringField
from wtforms.widgets import TimeInput
import datetime

class ClientRegistrationForm(FlaskForm):
    name =  StringField("Name", validators=[InputRequired(), Length(min=2, max=20)])
    #name =  StringField("Name", validators=[Required(), Length(min=1, max=40)]) 
    nric = StringField("NRIC", validators=[InputRequired(), Length(min=2, max=20)]) 
    email = StringField('Email', validators=[InputRequired(), Email()]) 
    password = PasswordField('Password', validators=[InputRequired()])
    city=SelectField("City",validators=[InputRequired()],choices=['Singapore','Hongkong'])
    contactno = StringField('Contact No.', validators=[InputRequired(), Length(min=8, max=8)]) 
    dateofbirth = DateField('DOB', format='%Y/%m/%d', validators=[DataRequired()])
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
    dateofbirth = DateField('DOB', format='%Y-%m-%d', validators=[DataRequired()])
    contactno = StringField('Contact No.', validators=[InputRequired(), Length(min=8, max=8)]) 
    city=SelectField("City",validators=[InputRequired()],choices=['Singapore','Hongkong'])
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

class BankerBuildForm(FlaskForm):
    name =  StringField("Name", validators=[InputRequired()]) 
    risk = IntegerField("Risk Level",validators=[InputRequired()])
    mininvest= IntegerField("Minimum Invesment Amount",validators=[InputRequired()])
    description = StringField("Description",validators=[InputRequired()])
    asset1 =  StringField("Asset 1", validators=[InputRequired()]) 
    asset1_percentage =  IntegerField("Percentage of Asset 1", validators=[InputRequired()])
    asset1_type =  SelectField("Type of Asset ", validators=[InputRequired()], choices=['Bond','Stock','Reits','Mutual Fund'])
    asset2 =  StringField("Asset 2", validators=[InputRequired()]) 
    asset2_percentage =  IntegerField("Percentage of Asset 2", validators=[InputRequired()])
    asset2_type =  SelectField("Type of Asset ", validators=[InputRequired()], choices=['Bond','Stock','Reits','Mutual Fund'])
    asset3 =  StringField("Asset 3", validators=[InputRequired()]) 
    asset3_percentage =  IntegerField("Percentage of Asset 3", validators=[InputRequired()])
    asset3_type =  SelectField("Type of Asset ", validators=[InputRequired()], choices=['Bond','Stock','Reits','Mutual Fund']) 
    asset4 =  StringField("Asset 4", validators=[InputRequired()]) 
    asset4_percentage =  IntegerField("Percentage of Asset 4", validators=[InputRequired()])
    asset4_type =  SelectField("Type of Asset ", validators=[InputRequired()], choices=['Bond','Stock','Reits','Mutual Fund'])
    asset5 =  StringField("Asset 5", validators=[InputRequired()]) 
    asset5_percentage =  IntegerField("Percentage of Asset 5", validators=[InputRequired()])
    asset5_type =  SelectField("Type of Asset ", validators=[InputRequired()], choices=['Bond','Stock','Reits','Mutual Fund'])
    asset6 =  StringField("Asset 6", validators=[InputRequired()]) 
    asset6_percentage =  IntegerField("Percentage of Asset 6", validators=[InputRequired()])
    asset6_type =  SelectField("Type of Asset ", validators=[InputRequired()], choices=['Bond','Stock','Reits','Mutual Fund'])
    asset7 =  StringField("Asset 7", validators=[InputRequired()]) 
    asset7_percentage =  IntegerField("Percentage of Asset 7", validators=[InputRequired()])
    asset7_type =  SelectField("Type of Asset ", validators=[InputRequired()], choices=['Bond','Stock','Reits','Mutual Fund'])
    asset8 =  StringField("Asset 8", validators=[InputRequired()]) 
    asset8_percentage =  IntegerField("Percentage of Asset 8", validators=[InputRequired()])
    asset8_type =  SelectField("Type of Asset ", validators=[InputRequired()], choices=['Bond','Stock','Reits','Mutual Fund'])
    asset9 =  StringField("Asset 9", validators=[InputRequired()]) 
    asset9_percentage =  IntegerField("Percentage of Asset 9", validators=[InputRequired()])
    asset9_type =  SelectField("Type of Asset ", validators=[InputRequired()], choices=['Bond','Stock','Reits','Mutual Fund'])
    asset10 =  StringField("Asset 10", validators=[InputRequired()]) 
    asset10_percentage =  IntegerField("Percentage of Asset 10", validators=[InputRequired()])
    asset10_type =  SelectField("Type of Asset ", validators=[InputRequired()], choices=['Bond','Stock','Reits','Mutual Fund'])






class TimeField(StringField):
    """HTML5 time input."""
    widget = TimeInput()

    def __init__(self, label=None, validators=None, format='%H:%M:%S', **kwargs):
        super(TimeField, self).__init__(label, validators, **kwargs)
        self.format = format

    def _value(self):
        if self.raw_data:
            return ' '.join(self.raw_data)
        else:
            return self.data and self.data.strftime(self.format) or ''

    def process_formdata(self, valuelist):
        if valuelist:
            time_str = ''.join(valuelist)
            try:
                components = time_str.split(':')
                hour = 0
                minutes = 0
                seconds = 0
                if len(components) in range(2,4):
                    hour = int(components[0])
                    minutes = int(components[1])

                    if len(components) == 3:
                        seconds = int(components[2])
                else:
                    raise ValueError
                self.data = datetime.time(hour, minutes, seconds)
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Not a valid time string'))


class SchedulerForm(FlaskForm):
    startdate_field = DateField('Start Date',validators=[InputRequired()])
    starttime_field = TimeField('Start Time',validators=[InputRequired()])
    enddate_field = DateField('End Date',validators=[InputRequired()])
    endtime_field = TimeField('End Time',validators=[InputRequired()])
    submit = SubmitField('Submit')



class NewsFilterForm(FlaskForm):
    startdate = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    enddate = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit')

class FinancialGoalForm(FlaskForm):
    investmentgoal = SelectField("Investment Goals - I am investing for ", validators=[InputRequired()], choices=['House','Car','Children Education','Retirement','General Investment'])
    yeartorealisegoal = IntegerField("I want to realise my goal in ...", validators=[InputRequired(), NumberRange(min=1,max=100)],render_kw={"placeholder": "Number of Years"})
    endgoal = IntegerField("My goal requires...", validators=[InputRequired()],render_kw={"placeholder": "$"})
    annualincome = IntegerField("My annual income (including other sources of income such as rental income) is approximately $", validators=[InputRequired()])
    estimatednetworth = IntegerField("My estimated net worth is approximately $", validators=[InputRequired()])
    initialamount = IntegerField("I am looking to invest an initial amount of $", validators=[InputRequired()])
    topupamountmonthly = IntegerField("Each month, I am looking to invest $", validators=[InputRequired()])
    valueofcurrentinvestment = IntegerField("The estimated value of my current investment portfolio is $", validators=[InputRequired()])
    equity = IntegerField("Equity (Stocks)", validators=[InputRequired()],render_kw={"placeholder": "%"})
    fixedincome = IntegerField("Fixed Income (Bonds)", validators=[InputRequired()],render_kw={"placeholder": "%"})
    forexcommodities = IntegerField("Commodities / Forex / Derivatives", validators=[InputRequired()],render_kw={"placeholder": "%"})
    mutualfund = IntegerField("Mutual Funds (Unit Trust) / Financial Planner", validators=[InputRequired()],render_kw={"placeholder": "%"})
    crypto = IntegerField("Cryptocurrency", validators=[InputRequired()],render_kw={"placeholder": "%"})
    realestate = IntegerField("Real Estate", validators=[InputRequired()],render_kw={"placeholder": "%"})
    otherinvestment = IntegerField("Others", validators=[InputRequired()],render_kw={"placeholder": "%"})
    prioritiesofinvestment = RadioField("When investing, my priorities are ", validators=[InputRequired()], choices=[('Maximise my potential gain','Maximise Gain'),('Equal emphasis on maximising gain & minimising loss','Equal Emphasis'),('Minimise my potential loss','Minimise Loss')])
    riskappetite = IntegerField("I rate my risk appetite (1-12)", validators=[InputRequired()],render_kw={"placeholder": "1 being safest, 12 being riskiest."})
    dropvalue = RadioField("I understand that markets are at times volatile. If my investment portfolio loses 10 percent of its value, I would ", validators=[InputRequired()], choices=[('Buy More','Buy More'),('Do Nothing','Do Nothing'),('Sell parts of my portfolio','Sell parts of my portfolio'),('Sell Everything','Sell Everything')])
    submit = SubmitField('Submit')