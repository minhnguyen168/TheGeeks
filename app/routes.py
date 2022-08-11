from re import A
from flask_login.mixins import UserMixin
from app import app, db, bcrypt, login_manager
from flask import render_template
from flask import url_for 
from flask import flash
from flask import redirect
from flask import request, abort
from flask import jsonify
from flask import json
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import or_, and_
from flask_sqlalchemy import Pagination
from app.forms import (ClientRegistrationForm, ClientLoginForm, BankerRegistrationForm,BankerLoginForm, NewsFilterForm, FinancialGoalForm)
from app.models import (User, Client, Banker, FinancialGoal, Portfolio, client_cluster, client_portfolio)
from app.news import (News)
from app import trade
import stripe
import pandas as pd
import os
from app.cluster_model import (clustering)


stripe_keys = {
    "secret_key": 'sk_test_51LUn73DmP0YmkHd0O5l77njV0F1M1QR8LzyaFKahQ8pugfrYV2swno5R7XhipkxbYcYqAgzUCoUBby1EQGEGnhw700852bTBqN',
    "publishable_key": 'pk_test_51LUn73DmP0YmkHd0j6LTuFIx8dw7qDjpba0Jzi4pgPvwKxIWlKOK1hHzUVD5E89UfmjqyduA2xMEteTTc1biY6jv00bbsb8Ap6'
}
stripe.api_key = stripe_keys["secret_key"]

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/')



@app.route('/',methods=['GET', 'POST'])
def mainpage():
    return render_template('mainpage.html')

@app.route('/element',methods=['GET', 'POST'])
def element():
    return render_template('elements.html')


@app.route('/client_login',methods=['GET', 'POST'])
def client_login():
    if current_user.is_authenticated: 
        return redirect(url_for('clienthome'))
    clientlogin_form=ClientLoginForm()
    if clientlogin_form.validate_on_submit():
        user = User.query.filter_by(email=clientlogin_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, clientlogin_form.password.data) and user.banker==0:
            login_user(user, remember=clientlogin_form.remember.data)
            next_page = request.args.get('next')
            return redirect(url_for('clienthome'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('client_login.html',clientlogin_form=clientlogin_form)

@app.route('/banker',methods=['GET', 'POST'])
def banker():
    if current_user.is_authenticated: 
        return redirect(url_for('bankerhome'))
    bankerregister_form = BankerRegistrationForm()
    bankerlogin_form=BankerLoginForm()
    if bankerregister_form.validate_on_submit():
        print('valid')
        hashed_password = bcrypt.generate_password_hash(bankerregister_form.password.data).decode('utf-8')
        user = User(name=bankerregister_form.name.data,NRIC=bankerregister_form.nric.data, password=hashed_password,email=bankerregister_form.email.data,banker=1)
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        newbanker = Banker(userid=user.id)
        db.session.add(newbanker)
        db.session.commit()
        flash("Your account has been created! You are now able to log in", 'success') 
        return redirect('/banker#login')
    if bankerlogin_form.validate_on_submit():
        user = User.query.filter_by(email=bankerlogin_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, bankerlogin_form.password.data) and user.banker==1:
            login_user(user, remember=bankerlogin_form.remember.data)
            next_page = request.args.get('next')
            return redirect(url_for('bankerhome'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('banker.html',bankerregister_form=bankerregister_form, bankerlogin_form=bankerlogin_form)
#Banker login
@app.route('/banker_login/',methods=['GET', 'POST'])
def banker_login():
    if current_user.is_authenticated: 
        return redirect(url_for('bankerhome'))
    bankerregister_form = BankerRegistrationForm()
    bankerlogin_form=BankerLoginForm()
    if bankerlogin_form.validate_on_submit():
        user = User.query.filter_by(email=bankerlogin_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, bankerlogin_form.password.data) and user.banker==1:
            login_user(user, remember=bankerlogin_form.remember.data)
            next_page = request.args.get('next')
            return redirect(url_for('bankerhome'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('banker_login.html', bankerlogin_form=bankerlogin_form)

#Become a client page
@app.route('/become_a_client',methods=['GET', 'POST'])
def become_a_client():
    if current_user.is_authenticated: 
        return redirect(url_for('clienthome'))
    clientregister_form = ClientRegistrationForm()
    if clientregister_form.validate_on_submit():
        print('valid')
        hashed_password = bcrypt.generate_password_hash(clientregister_form.password.data).decode('utf-8')
        user = User(name=clientregister_form.name.data, NRIC=clientregister_form.nric.data, password=hashed_password,email=clientregister_form.email.data, city=clientregister_form.city.data,dateofbirth=clientregister_form.dateofbirth.data,contactno=clientregister_form.contactno.data,banker=0)
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        newclient = Client(userid=user.id)
        db.session.add(newclient)
        db.session.commit()
        flash("Your account has been created! You are now able to log in", 'success') 
    return render_template('become_a_client.html',clientregister_form=clientregister_form)

@app.route('/client/financialgoals',methods=['GET', 'POST'])
@login_required 
def fingoals():
    financialgoal_form=FinancialGoalForm()
    if financialgoal_form.validate_on_submit():
        client=Client.query.filter_by(userid=current_user.id).first()
        fingoal = FinancialGoal(
            client_id = client.client_id,
            investmentgoal = financialgoal_form.investmentgoal.data,
            yeartorealisegoal = financialgoal_form.yeartorealisegoal.data,
            endgoal = financialgoal_form.endgoal.data,
            annualincome = financialgoal_form.annualincome.data,
            estimatednetworth = financialgoal_form.estimatednetworth.data,
            initialamount = financialgoal_form.initialamount.data,
            topupamountmonthly = financialgoal_form.topupamountmonthly.data,
            valueofcurrentinvestment = financialgoal_form.valueofcurrentinvestment.data,
            equity = financialgoal_form.equity.data,
            fixedincome = financialgoal_form.fixedincome.data,
            forexcommodities = financialgoal_form.forexcommodities.data,
            mutualfund = financialgoal_form.mutualfund.data,
            crypto = financialgoal_form.crypto.data,
            realestate = financialgoal_form.realestate.data,
            otherinvestment = financialgoal_form.otherinvestment.data,
            prioritiesofinvestment = financialgoal_form.prioritiesofinvestment.data,
            riskappetite = financialgoal_form.riskappetite.data,
            dropvalue = financialgoal_form.dropvalue.data
        )
        db.session.add(fingoal)
        db.session.commit()
        flash('Goals Captured!', 'danger')
        return redirect(url_for('clientdashboard'))
        
    else:
        flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('financial_goals.html',financialgoal_form=financialgoal_form)

#Build portfolio page
@app.route('/banker/build_portfolio',methods=['GET', 'POST'])
# @login_required 
def build_portfolio():
    return render_template('banker_build_portfolio.html')

@app.route('/client/home',methods=['GET', 'POST'])
def clienthome():
    return render_template('client_mainpage.html')

@app.route('/client/dashboard',methods=['GET', 'POST'])
# @login_required 
def clientdashboard():
    user = User.query.filter_by(id=current_user.get_id()).first()
    client_id  = Client.query.filter_by(userid=current_user.get_id()).first().client_id

    ## Calculating Statistics
    client_portfolios_df = pd.read_sql('SELECT * FROM client_portfolio c WHERE c.client_id =' + str(client_id), db.session.bind)
    totalAssets = client_portfolios_df.amount_purchase.sum()
    portfolioIDs = client_portfolios_df.portfolio_id.unique()
    totalPortfolios = len(portfolioIDs)

    market_names = []

    for p in portfolioIDs:
        row  = pd.read_sql('SELECT * FROM Portfolio p WHERE p.portfolio_id =' + str(p), db.session.bind)

        for i in range(1,11):
            market = row["asset"+str(i)][0]
            market_names.append(market)

    market_names = list(set(market_names))
    
    today = trade.get_today()
    start = trade.get_one_day_period(today)

    marketChange = []

    for m in market_names:
        marketChange.append(round(trade.cal_1d_diff(m, start, today),2)) # should have two records


    return render_template('client_dashboard.html', totalAssets=totalAssets, totalPortfolios=totalPortfolios,
        markets=market_names, marketChange=marketChange)

@app.route('/banker/home',methods=['GET', 'POST'])
#@login_required
def bankerhome():
    return render_template('banker_mainpage.html')

@app.route('/banker/dashboard',methods=['GET', 'POST'])
# @login_required 
def bankerdashboard():
    return render_template('banker_dashboard.html')

@app.route('/banker/dashboard/clientDetails',methods=['GET', 'POST'])
# @login_required 
def bankerclientdetails():

    return render_template('banker_client_details.html')

@app.route('/banker/clientsegmentation',methods=['GET', 'POST'])
# @login_required 
def client_segmentation():
    df=db.session.execute('SELECT c.client_id, u.dateofbirth, u.city, f.investmentgoal, f.yeartorealisegoal, f.endgoal, f.annualincome, f.estimatednetworth, f.topupamountmonthly, f.valueofcurrentinvestment, f.equity, f.fixedincome, f.forexcommodities, f.mutualfund, f.crypto, f.realestate, f.otherinvestment, f.prioritiesofinvestment, f.riskappetite, f.dropvalue FROM User u, Client c, FinancialGoal f WHERE u.banker=0 AND u.id =c.userid AND c.client_id=f.client_id')
    df = pd.DataFrame(df)
    result=clustering().AC_cluster(df=df)
    db.session.execute("delete from client_cluster")
    for i in range(0,result.shape[0]):
        cluster=client_cluster(client_id=int(result.iloc[i,0]),dateofbirth=str(result.iloc[i,1]),city=str(result.iloc[i,2]),investmentgoal=str(result.iloc[i,3]),yeartorealisegoal=int(result.iloc[i,4]),endgoal=int(result.iloc[i,5]),	annualincome=int(result.iloc[i,6]),estimatednetworth=int(result.iloc[i,7]),topupamountmonthly=int(result.iloc[i,8]),valueofcurrentinvestment=int(result.iloc[i,9]),equity=int(result.iloc[i,10]),fixedincome=int(result.iloc[i,11]),forexcommodities=result.iloc[i,12],mutualfund=result.iloc[i,13],crypto=result.iloc[i,14],realestate=result.iloc[i,15],otherinvestment=result.iloc[i,16],prioritiesofinvestment=str(result.iloc[i,17]),riskappetite=result.iloc[i,18],dropvalue=str(result.iloc[i,19]),age=result.iloc[i,20],Cluster_AC=int(result.iloc[i,21]))
        db.session.add(cluster)
        db.session.commit()
        db.session.refresh(cluster)
    return render_template('customer_segmentation.html',result=result)

### Stripe Integration
@app.route("/checkout", methods=['GET','POST'])
@login_required
def checkout():
    try:
        checkout_session = stripe.checkout.Session.create(
                    line_items=[{'price': 'price_1LUndRDmP0YmkHd0vNgO8WpV','quantity': 1}],
                    mode='payment',success_url=url_for('success',_external=True),
                    cancel_url=url_for('cancel',_external=True))
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

@app.route("/success", methods=['GET','POST'])
def success():
    flash('Purchased Successfully!')
    return redirect(url_for('clienthome'))

@app.route("/cancel", methods=['GET','POST'])
def cancel():
    flash('Purchase Failed!')
    return redirect(url_for('clienthome'))

### End Stripe Integration


@app.route("/client/logout")
@login_required
def logoutclient():
    logout_user()
    return redirect(url_for('client'))

@app.route("/banker/logout")
@login_required
def logoutbanker():
    logout_user()
    return redirect(url_for('banker'))

@app.route('/client/news', methods=['GET', 'POST']) 
def news_client(): 
     news_obj = News()
     images_list = []
     news_df = pd.read_sql('SELECT * FROM Insight', db.session.bind)
     news_summary = news_obj.get_news_summary(news_df)
     news_form = NewsFilterForm()
     if news_form.validate_on_submit():
         start_date = int(str(news_form.startdate.data).replace("-", ""))
         end_date = int(str(news_form.enddate.data).replace("-", ""))
         news_df = pd.read_sql('SELECT * FROM Insight WHERE published_date >= {} AND published_date <= {}'.format(start_date, end_date), db.session.bind)
         news_summary = news_obj.get_news_summary(news_df)
     return render_template('news.html', news_df=news_df, news_summary=news_summary, news_form=news_form, images_list=images_list)

# @app.route('/banker/news', methods=['GET', 'POST'])
# def news_banker():
#     news_obj = News()
#     news_df = pd.read_sql('SELECT * FROM Insight', db.session.bind)
#     #news_summary = news_obj.get_news_summary(news_df)

#     news_form = NewsFilterForm()
#     if news_form.validate_on_submit():
#         start_date = int(str(news_form.startdate.data).replace("-", ""))
#         end_date = int(str(news_form.enddate.data).replace("-", ""))
#         news_df = pd.read_sql('SELECT * FROM Insight WHERE published_date >= {} AND published_date <= {}'.format(start_date, end_date), db.session.bind)
#         #news_summary = news_obj.get_news_summary(news_df)

#     # All below to be moved to dashboard page
#     num_topics = 4
#     images_list = []
#     topics = news_obj.topic_modelling(news_df, num_topics)
#     news_obj.topics_wordcloud(topics)
#     for index in range(num_topics):
#         try:
#             images_list.append([index+1, os.path.join("app/static/images", "wordcloud_{}.jpg".format(index+1))])
#             # images_list.append([index+1, "images/wordcloud_{}.jpg".format(index+1)])
#         except:
#             continue
#     return render_template('news.html', news_df=news_df, news_summary="news_summary", news_form=news_form, images_list=images_list)

@app.route('/client/trade', methods=['GET', 'POST'])
def show_markets():
    markets = ['NVDA', 'BBBY', 'GME', 'NVAX', 'MU', 'INTC', 'LMND', 'NCLH', 'VRNA', 'AMAT', 'U', 'NLSN']

    tickers = trade.get_market_details(markets)

    return render_template('trade.html', tickers=tickers, markets=markets)

@app.route('/client/trade/details', methods=['GET','POST'])
def show_market_details():
    if request.method == "POST":
        market = request.form.get('ticker_detail')
        ticker = trade.get_market_details([market])
        ticker_info = ticker[0].info # since we are only focused on one
        today = trade.get_today()
        periods = trade.get_holding_periods(today)
        hist_df = trade.get_hist_ret(market, periods, today)
        hist_ret = trade.cal_port_ret(len(periods), hist_df)
    return render_template('trade_details.html', market=market, ticker_info=ticker_info, hist_ret=hist_ret)

@app.route('/client/portfolio', methods=['GET', 'POST'])
def shop_portfolio():
    df = pd.read_sql('SELECT * FROM Portfolio', db.session.bind)
    #html_table = df.to_html()
    #shopPortfolio.show(port_df)
    #return render_template('shopPortfolio.html', html_table=html_table)
    return render_template('shopPortfolio.html', tables=[df.to_html(classes='data')], titles=df.columns.values)
