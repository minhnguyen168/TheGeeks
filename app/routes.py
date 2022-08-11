from re import A
from flask_login.mixins import UserMixin
from app import app, db, bcrypt, login_manager, socketio
from flask_socketio import SocketIO, join_room
from flask import render_template
from flask import url_for, Response 
from flask import flash, session
from flask import redirect
from flask import request, abort
from flask import jsonify
from flask import json
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import or_, and_
from flask_sqlalchemy import Pagination
from app.forms import (ClientRegistrationForm, ClientLoginForm, BankerRegistrationForm,BankerLoginForm, NewsFilterForm, FinancialGoalForm, SchedulerForm)
from app.models import (User, Client, Banker, FinancialGoal, Portfolio, client_cluster, client_portfolio)
from app.news import (News)
from app import trade
import yfinance as yf
import stripe
import pandas as pd
import os
import matplotlib.pyplot as plt
from app.cluster_model import (clustering)
from icalendar import Calendar, Event, vCalAddress, vText
import pytz
from datetime import datetime
from pathlib import Path
import dateutil.tz

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
@app.route('/banker_login',methods=['GET', 'POST'])
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




#chat

@app.route('/chat/<id>')
@login_required
def sessions(id):
    session['id'] = id
    return render_template('session.html',url='/chat/'+str(id))

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('connect')
def connect():
    print('joining room'+str(session['id']))
    room = session["id"]
    join_room(session['id'])
    json = {'user_name': current_user.name, 'message': 'is connected.'}
    socketio.emit("my response", json, callback=messageReceived, room=room)

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    room = session["id"]
    join_room(room)
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived, room=room)
#endchat

#Scheduling page
@app.route('/banker/schedule/<clientid>', methods=['GET', 'POST'])
@login_required
def scheduler(clientid):
    scheduler_form=SchedulerForm()
    
    if scheduler_form.validate_on_submit():
        
        a=(str(scheduler_form.startdate_field.data).replace("-", ""))
        b=(str(scheduler_form.starttime_field.data).replace(":", ""))
        c=(str(scheduler_form.enddate_field.data).replace("-", ""))
        d=(str(scheduler_form.endtime_field.data).replace(":", ""))
        return redirect(url_for('calendarapi',clientid=clientid,startYYYYMMDDHHMM=a+b,endYYYYMMDDHHMM=c+d))
    return render_template('scheduler.html',scheduler_form=scheduler_form)

#

#Calendar invite miniAPI
@app.route('/banker/schedule/<clientid>/<startYYYYMMDDHHMM>/<endYYYYMMDDHHMM>')
@login_required
def calendarapi(clientid,startYYYYMMDDHHMM,endYYYYMMDDHHMM):
    cal = Calendar()
    startYYYYMMDDHHMM=str(startYYYYMMDDHHMM)
    endYYYYMMDDHHMM=str(endYYYYMMDDHHMM)
    clientfromid=Client.query.filter_by(client_id=clientid).first()
    client=User.query.filter_by(id=clientfromid.userid).first()
    bankername=current_user.name
    
    cal.add(current_user.name, 'MAILTO:'+current_user.email)
    cal.add(client.name, 'MAILTO:'+client.email)

    event = Event()
    event.add('summary', 'TheGeeks Wealth Management Consulting Session with '+current_user.name+' and '+client.name)
    event.add('dtstart', datetime(int(startYYYYMMDDHHMM[0:4]), int(startYYYYMMDDHHMM[4:6]), int(startYYYYMMDDHHMM[6:8]), int(startYYYYMMDDHHMM[8:10]), int(startYYYYMMDDHHMM[10:12]), 0, tzinfo=dateutil.tz.gettz('Asia/Singapore')))
    event.add('dtend', datetime(int(endYYYYMMDDHHMM[0:4]), int(endYYYYMMDDHHMM[4:6]), int(endYYYYMMDDHHMM[6:8]), int(endYYYYMMDDHHMM[8:10]), int(endYYYYMMDDHHMM[10:12]), 0, tzinfo=dateutil.tz.gettz('Asia/Singapore')))
    event.add('dtstamp', datetime.now())

    organizer = vCalAddress('MAILTO:'+current_user.email)
    organizer.params['cn'] = vText(current_user.name)
    organizer.params['role'] = vText('Banker')
    event['organizer'] = organizer
    event['location'] = vText('http://127.0.0.1:5000/chat/'+str(clientid))

    # Adding events to calendar
    cal.add_component(event)

    # directory = str(Path(__file__).parent.parent) + "/"
    # print("ics file will be generated at ", directory)
    # f = open(os.path.join(directory, str(clientid)+'.ics'), 'wb')
    # f.write(cal.to_ical())
    # f.close()
    flash('Meeting Scheduled!')
    return Response(cal.to_ical(), mimetype='text/calendar')

#end calendar invite miniAPI

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

#Banker_view_client page
@app.route('/banker/viewclients',methods=['GET', 'POST'])
# @login_required 
def banker_view_client():
    a=current_user.id
    client=db.session.execute('SELECT DISTINCT c.client_id FROM User u, Banker b, BankerClientRelation r, Client c WHERE u.id ='+ current_user.get_id() +' AND u.banker=1 AND b.userid=u.id AND r.banker_id=b.banker_id AND r.client_id= c.client_id')
    client=pd.DataFrame(client)
    nam= db.session.execute('SELECT u.name FROM Client c, User u WHERE c.client_id='+ str(client.iloc[0,0]) + ' AND c.userid=u.id')
    result=db.session.execute('SELECT f.investmentgoal, f.yeartorealisegoal, f.endgoal, f.annualincome, f.estimatednetworth, f.topupamountmonthly, f.valueofcurrentinvestment, f.equity, f.fixedincome, f.forexcommodities, f.mutualfund, f.crypto, f.realestate, f.otherinvestment, f.prioritiesofinvestment, f.riskappetite, f.dropvalue  FROM Client c, FinancialGoal f WHERE c.client_id=' + str(client.iloc[0,0]) +  ' AND c.client_id=f.client_id')
    nam=pd.DataFrame(nam)
    result=pd.DataFrame(result)
    for i in range(1,client.shape[0]):
        holder1=db.session.execute('SELECT f.investmentgoal, f.yeartorealisegoal, f.endgoal, f.annualincome, f.estimatednetworth, f.topupamountmonthly, f.valueofcurrentinvestment, f.equity, f.fixedincome, f.forexcommodities, f.mutualfund, f.crypto, f.realestate, f.otherinvestment, f.prioritiesofinvestment, f.riskappetite, f.dropvalue  FROM Client c, FinancialGoal f WHERE c.client_id=' + str(client.iloc[i,0]) +  ' AND c.client_id=f.client_id')
        holder1=pd.DataFrame(holder1)
        result=result.append(holder1)
    for i in range(1,nam.shape[0]):  
        holder2=db.session.execute('SELECT u.name FROM Client c, User u WHERE c.client_id='+ str(client.iloc[i,0]) + ' AND c.userid=u.id')
        holder2=pd.DataFrame(holder2)
        nam=nam.append(holder2)
    return render_template('banker_view_client.html',result=result,nam=nam)
#Banker view client detail
@app.route('/banker/viewclients/detail',methods=['GET', 'POST'])
# @login_required 
def banker_view_client_details():
    nam= db.session.execute('SELECT u.name FROM Client c, User u WHERE c.client_id='+ str(client.iloc[0,0]) + ' AND c.userid=u.id')
    result=db.session.execute('SELECT f.investmentgoal, f.yeartorealisegoal, f.endgoal, f.annualincome, f.estimatednetworth, f.topupamountmonthly, f.valueofcurrentinvestment, f.equity, f.fixedincome, f.forexcommodities, f.mutualfund, f.crypto, f.realestate, f.otherinvestment, f.prioritiesofinvestment, f.riskappetite, f.dropvalue  FROM Client c, FinancialGoal f WHERE c.client_id=' + str(client.iloc[0,0]) +  ' AND c.client_id=f.client_id')
    nam=pd.DataFrame(nam)
    result=pd.DataFrame(result)
    for i in range(1,client.shape[0]):
        holder1=db.session.execute('SELECT f.investmentgoal, f.yeartorealisegoal, f.endgoal, f.annualincome, f.estimatednetworth, f.topupamountmonthly, f.valueofcurrentinvestment, f.equity, f.fixedincome, f.forexcommodities, f.mutualfund, f.crypto, f.realestate, f.otherinvestment, f.prioritiesofinvestment, f.riskappetite, f.dropvalue  FROM Client c, FinancialGoal f WHERE c.client_id=' + str(client.iloc[i,0]) +  ' AND c.client_id=f.client_id')
        holder1=pd.DataFrame(holder1)
        result=result.append(holder1)
    for i in range(1,nam.shape[0]):  
        holder2=db.session.execute('SELECT u.name FROM Client c, User u WHERE c.client_id='+ str(client.iloc[i,0]) + ' AND c.userid=u.id')
        holder2=pd.DataFrame(holder2)
        nam=nam.append(holder2)
    return render_template('banker_client_details',result=result,nam=nam)
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
    return render_template('banker_dashboard.html')

@app.route('/banker/dashboard',methods=['GET', 'POST'])
# @login_required 
def bankerdashboard():
    images_list = []
    if request.method == "POST":  
        num_topics = request.form["topics"]
        usergroup = request.form["usergroups"]
        users_df = pd.read_sql('SELECT client_id FROM client_cluster WHERE Cluster_AC = {}'.format(usergroup), db.session.bind)
        users_list = users_df['client_id'].tolist()

        news_obj = News()
        news_df = pd.read_sql('SELECT news_id FROM NewsRecord WHERE client_id IN {}'.format(str(users_list).replace("[", "(").replace("]", ")")), db.session.bind)
        news_list = news_df['news_id'].tolist()
        filtered_news_df = pd.read_sql('SELECT * FROM Insight WHERE news_id IN {}'.format(str(news_list).replace("[", "(").replace("]", ")")), db.session.bind)
        print(filtered_news_df)
        print(news_df)
        if filtered_news_df.shape[0] > 0:
            topics = news_obj.topic_modelling(filtered_news_df, num_topics)
            news_obj.topics_wordcloud(topics)
            for index in range(int(num_topics)):
                try:
                    images_list.append([index+1, "wordcloud_{}.jpg".format(index+1)])
                except:
                    continue
    return render_template('banker_dashboard.html', images_list=images_list)



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
        cluster=client_cluster(client_id=int(result.iloc[i,0]),dateofbirth=str(result.iloc[i,1]),city=str(result.iloc[i,2]),investmentgoal=str(result.iloc[i,3]),yeartorealisegoal=int(result.iloc[i,4]),endgoal=int(result.iloc[i,5]),	annualincome=int(result.iloc[i,6]),estimatednetworth=int(result.iloc[i,7]),topupamountmonthly=int(result.iloc[i,8]),valueofcurrentinvestment=int(result.iloc[i,9]),equity=int(result.iloc[i,10]),fixedincome=int(result.iloc[i,11]),forexcommodities=int(result.iloc[i,12]),mutualfund=int(result.iloc[i,13]),crypto=int(result.iloc[i,14]),realestate=int(result.iloc[i,15]),otherinvestment=int(result.iloc[i,16]),prioritiesofinvestment=str(result.iloc[i,17]),riskappetite=int(result.iloc[i,18]),dropvalue=str(result.iloc[i,19]),age=int(result.iloc[i,20]),Cluster_AC=int(result.iloc[i,21]))
        db.session.add(cluster)
        db.session.commit()
        db.session.refresh(cluster)
    return render_template('customer_segmentation.html',result=result)

#Client academy
@app.route("/client/academy", methods=['GET','POST'])
def client_academy():
    flash('Purchased Successfully!')
    return render_template('client_academy.html')

#Banker Academy
@app.route("/banker/academy", methods=['GET','POST'])
def banker_academy():
    flash('Purchased Successfully!')
    return render_template('banker_academy.html')

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

@app.route('/banker/news', methods=['GET', 'POST'])
def news_banker():
    news_obj = News()
    news_df = pd.read_sql('SELECT * FROM Insight', db.session.bind)
    #news_summary = news_obj.get_news_summary(news_df)

    news_form = NewsFilterForm()
    if news_form.validate_on_submit():
        start_date = int(str(news_form.startdate.data).replace("-", ""))
        end_date = int(str(news_form.enddate.data).replace("-", ""))
        news_df = pd.read_sql('SELECT * FROM Insight WHERE published_date >= {} AND published_date <= {}'.format(start_date, end_date), db.session.bind)
        #news_summary = news_obj.get_news_summary(news_df)

    # All below to be moved to dashboard page
    num_topics = 4
    images_list = []
    topics = news_obj.topic_modelling(news_df, num_topics)
    news_obj.topics_wordcloud(topics)
    for index in range(num_topics):
        try:
            images_list.append([index+1, os.path.join("app/static/images", "wordcloud_{}.jpg".format(index+1))])
            # images_list.append([index+1, "images/wordcloud_{}.jpg".format(index+1)])
        except:
            continue
    return render_template('banker_news.html', news_df=news_df, news_summary="news_summary", news_form=news_form, images_list=images_list)

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
    user = User.query.filter_by(id=current_user.get_id()).first()
    client_id = Client.query.filter_by(userid=current_user.get_id()).first().client_id

    client_portfolios_df = pd.read_sql('SELECT * FROM client_portfolio c WHERE c.client_id =' + str(client_id),
                                       db.session.bind)

    portfolioIDs = client_portfolios_df.portfolio_id.unique()

    #print(portfolioIDs) # in an array
    df = db.session.execute('SELECT * FROM Portfolio where portfolio_id NOT IN (%s)' % tuple(portfolioIDs))
    df = pd.DataFrame(df)

    return render_template('shopPortfolio.html', df=df, port_id=portfolioIDs)

@app.route('/client/portfolio_details', methods=['GET', 'POST'])
def show_port_details():
    #
    # ## Calculating Statistics
    # client_portfolios_df = pd.read_sql('SELECT * FROM client_portfolio c WHERE c.client_id =' + str(client_id),
    #                                    db.session.bind)
    if request.method == "POST":
        port_id = request.form.get('port_detail')
        #print(port_id)
        df = db.session.execute('SELECT * FROM Portfolio where portfolio_id = ' + str(port_id)) # one particular row
        df = pd.DataFrame(df)
        today = trade.get_today()
        periods = trade.get_holding_periods(today)
        prev_5_yr = periods[3] # third element returns date for 5 years ago
        num_assets = 10 # we assume that all portfolio have 10 assets
        asset_list = []
        weight_list = [] # store corresponding weight for each asset for a particular portfolio
        asset_hist_df = []
        asset_adj_close = [] # [[] for i in range(num_assets)]
        port_name = ''

        for key, value in df.iterrows(): # will only iterate once -> to populate the asset and its weights
            port_name = value['name']
            asset_list.append(value['asset1'])
            asset_list.append(value['asset2'])
            asset_list.append(value['asset3'])
            asset_list.append(value['asset4'])
            asset_list.append(value['asset5'])
            asset_list.append(value['asset6'])
            asset_list.append(value['asset7'])
            asset_list.append(value['asset8'])
            asset_list.append(value['asset9'])
            asset_list.append(value['asset10'])

            weight_list.append(value['asset1_percentage'])
            weight_list.append(value['asset2_percentage'])
            weight_list.append(value['asset3_percentage'])
            weight_list.append(value['asset4_percentage'])
            weight_list.append(value['asset5_percentage'])
            weight_list.append(value['asset6_percentage'])
            weight_list.append(value['asset7_percentage'])
            weight_list.append(value['asset8_percentage'])
            weight_list.append(value['asset9_percentage'])
            weight_list.append(value['asset10_percentage'])

        for i in range(num_assets):
            asset_hist_df.append(yf.download(asset_list[i], start=prev_5_yr, end=today))
            asset_adj_close.append((asset_hist_df[i])['Adj Close'].tolist()) # each element in the list will be a list of the adj close of the particular asset

        date_list = (asset_hist_df[0]).index.tolist()
        # test = asset_adj_close[0][0]
        #
        # print(test)

        print(len(date_list))
        # for i in range(len(date_list)):
        #     for j in range(len(asset_list)):
        #         print(asset_adj_close[j][i])
        #         print(i)
        #         print(j)
        #         print(asset_list[j])

        price_list = [] # contain the portfolio market price sum

        for index in range(len(date_list)):
            price_sum = 0
            for asset in range(len(asset_list)):
                price_sum = price_sum + asset_adj_close[asset][index]
            price_list.append(price_sum)

        plt.switch_backend('Agg')
        # fig, ax = plt.subplots(nrows=1, ncols=1)  # create figure & 1 axis
        # ax.plot(date_list, price_list)
        # fig.savefig('static/images/portfolio.png')  # save the figure to file
        # plt.close(fig)

        plt.plot(date_list, price_list)
        plt.xlabel('Year')
        plt.ylabel('Portfolio value')
        plt.title('Changes in Portfolio Market Price Over the Past 5 Years')
        plt.legend(['Market Price'])

        # save the figure
        plt.savefig('app/static/images/portfolio.png', dpi=300, bbox_inches='tight')
        plt.show()

        plt.close()
        # print(len(price_list))
        # print(len(date_list))
        # print(price_list[5])
        # print(date_list[5])
    return render_template('port_details.html', asset_list=asset_list, weight_list=weight_list, asset_hist_df=asset_hist_df, port_name=port_name, date_list=date_list, asset_adj_close=asset_adj_close)