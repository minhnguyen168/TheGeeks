import os
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from app.news import (News)

sched = BackgroundScheduler(daemon=True)
sched.add_job(News().get_financial_news,'interval',hours=24)
sched.start()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'f9668b6e45f66487549fc7c385f063cf'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app) 
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from app import routes
