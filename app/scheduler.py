from apscheduler.schedulers.background import BackgroundScheduler
from app.news import (News)

sched = BackgroundScheduler(daemon=True)
sched.add_job(News().get_financial_news,'interval',hours=24)
sched.start()