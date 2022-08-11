from app import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True) 
    name = db.Column(db.String(20), unique=True, nullable=False) 
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    banker = db.Column(db.Integer, nullable=False)
    contactno = db.Column(db.Integer)
    dateofbirth = db.Column(db.Integer)
    photo = db.Column(db.String)
    address = db.Column(db.String)
    NRIC = db.Column(db.String)
    city = db.Column(db.String)

class Client(db.Model):
    client_id = db.Column(db.Integer, primary_key = True)
    userid = db.Column(db.Integer)

class Banker(db.Model):
    banker_id = db.Column(db.Integer, primary_key = True)
    userid = db.Column(db.Integer)
    
class BankerClientRelation(db.Model):
    relation_id = db.Column(db.Integer, primary_key = True)
    client_id = db.Column(db.Integer)
    banker_id = db.Column(db.Integer)
    private = db.Column(db.Integer)
    startdate = db.Column(db.String)
    enddate = db.Column(db.String)

class Portfolio(db.Model):
    portfolio_id = db.Column(db.Integer, primary_key = True)
    portfoliotype = db.Column(db.String(60))
    risk = db.Column(db.Integer)
    mininvest = db.Column(db.Integer)
    description = db.Column(db.String(240))
    banker_id = db.Column(db.Integer)
    asset1 = db.Column(db.String(60))
    asset1_percentage = db.Column(db.Integer)
    asset1_type = db.Column(db.String(60))
    asset2 = db.Column(db.String(60))
    asset2_percentage = db.Column(db.Integer)
    asset2_type = db.Column(db.String(60))
    asset3 = db.Column(db.String(60))
    asset3_percentage = db.Column(db.Integer)
    asset3_type = db.Column(db.String(60))
    asset4 = db.Column(db.String(60))
    asset4_percentage = db.Column(db.Integer)
    asset4_type = db.Column(db.String(60))
    asset5 = db.Column(db.String(60))
    asset5_percentage = db.Column(db.Integer)
    asset5_type = db.Column(db.String(60))
    asset6 = db.Column(db.String(60))
    asset6_percentage = db.Column(db.Integer)
    asset6_type = db.Column(db.String(60))
    asset7 = db.Column(db.String(60))
    asset7_percentage = db.Column(db.Integer)
    asset7_type = db.Column(db.String(60))
    asset8 = db.Column(db.String(60))
    asset8_percentage = db.Column(db.Integer)
    asset8_type = db.Column(db.String(60))
    asset9 = db.Column(db.String(60))
    asset9_percentage = db.Column(db.Integer)
    asset9_type = db.Column(db.String(60))
    asset10 = db.Column(db.String(60))
    asset10_percentage = db.Column(db.Integer)
    asset10_type = db.Column(db.String(60))
    
class FinancialGoal(db.Model):
    goal_id = db.Column(db.Integer, primary_key = True)
    client_id = db.Column(db.Integer)
    investmentgoal = db.Column(db.String(120))
    yeartorealisegoal = db.Column(db.Integer)
    endgoal = db.Column(db.Integer)
    annualincome = db.Column(db.Integer)
    estimatednetworth = db.Column(db.Integer)
    initialamount = db.Column(db.Integer)
    topupamountmonthly = db.Column(db.Integer)
    valueofcurrentinvestment = db.Column(db.Integer)
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

## Added by Branda
class client_portfolio(db.Model):
    client_id = db.Column(db.Integer)
    portfolio_id = db.Column(db.Integer)
    purchase_id = db.Column(db.Integer, primary_key = True)
    date_purchase = db.Column(db.String)
    amount_purchase = db.Column(db.Integer)

class Insight(db.Model):
    news_id = db.Column(db.String(500), primary_key = True)
    published_date = db.Column(db.Integer)
    news_title = db.Column(db.String(500))
    news_description = db.Column(db.String(500))
    news_content = db.Column(db.String(500))
    news_url = db.Column(db.String(500))
class client_cluster(db.Model):
    client_id = db.Column(db.Integer,primary_key=True)
    dateofbirth=db.Column(db.String(120))
    city=db.Column(db.String(120))
    investmentgoal = db.Column(db.String(120))
    yeartorealisegoal = db.Column(db.Integer)
    endgoal = db.Column(db.Integer)
    annualincome = db.Column(db.Integer)
    estimatednetworth = db.Column(db.Integer)
    initialamount = db.Column(db.Integer)
    topupamountmonthly = db.Column(db.Integer)
    valueofcurrentinvestment = db.Column(db.Integer)
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
    age = db.Column(db.Integer)
    Cluster_AC = db.Column(db.Integer)

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