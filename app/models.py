from app import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True) 
    username = db.Column(db.String(20), unique=True, nullable=False) 
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    banker = db.Column(db.Integer, nullable=False)
    contactno = db.Column(db.Integer)
    dateofbirth = db.Column(db.Integer)
    photo = db.Column(db.String)
    address = db.Column(db.String)
    NRIC = db.Column(db.String)

class client(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    userid = db.Column(db.Integer)
    bankerid = db.Column(db.Integer)
    portfolioid = db.Column(db.Integer)

class banker(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    userid = db.Column(db.Integer)
    portfolioid = db.Column(db.Integer)
    clientid = db.Column(db.Integer)

class portfolio(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    portfoliotype = db.Column(db.String(60))
    risk = db.Column(db.Integer)
    mininvest = db.Column(db.Integer)
    description =  db.Column(db.String(240))
    assettype = db.Column(db.String(60))
    
class financialdec(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    clientid = db.Column(db.Integer)
    investmentgoal = db.Column(db.String(120))
    yeartorealisegoal = db.Column(db.Integer)
    endgoal = db.Column(db.Integer)
    age = db.Column(db.Integer)
    annualincome = db.Column(db.Integer)
    estimatednetworth = db.Column(db.Integer)
    initialamount = db.Column(db.Integer)
    topupamountmonthly = db.Column(db.Integer)
    valueofcurrentinvestment = db.Column(db.Integer)
    currentasset = db.Column(db.Integer)
    currentasset = db.Column(db.Integer)
    equity = db.Column(db.Integer)
    fixedincome = db.Column(db.Integer)
    forexcommodities = db.Column(db.Integer)
    mutualfund = db.Column(db.Integer)
    crypto = db.Column(db.Integer)
    realestate = db.Column(db.Integer)
    otherinvestment = db.Column(db.Integer)
    prioritiesofinvestment = db.Column(db.String(120))
    riskappetite = db.Column(db.Integer)
    dropvalue = db.Column(db.String(120))


    #def get_reset_token(self, expires_sec=1800):
    #    s = Serializer(app.config['SECRET_KEY'], expires_sec)
    #    return s.dumps({'user_id': self.id}).decode('utf-8')

    #@staticmethod 
    #def verify_reset_token(token):
    #    s = Serializer(app.config['SECRET_KEY'])
    #    try:
    #        userid = s.loads(token)['user_id']
    #    except:
    #        return None
    #    return User.query.get(username)
    
# class Voucher(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     username = db.Column(db.String(20), nullable=False)
#     cashiername = db.Column(db.String(20), nullable=False)
#     expiry = db.Column(db.Integer, nullable=False)
#     value = db.Column(db.Integer, nullable=False)
#     transfer = db.Column(db.Integer, nullable=False)
#     status = db.Column(db.Integer, nullable=False)

# class VoucherCat(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     value = db.Column(db.Integer, nullable=False)
#     transfer = db.Column(db.Integer, nullable=False)
#     cost = db.Column(db.Integer, nullable=False)
#     expirydur = db.Column(db.Integer, nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)
#     cashiername = db.Column(db.String(20), unique=True, nullable=False)
#     sold = db.Column(db.Integer, nullable=False)

    def __repr__(self): 
        return f"User('{self.username}', '{self.email}')"