from flask_login.mixins import UserMixin
from app import app, db, bcrypt, login_manager
from flask import render_template
from flask import url_for 
from flask import flash 
from flask import redirect
from flask import request, abort
from flask import jsonify
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import or_, and_
from flask_sqlalchemy import Pagination
from app.forms import (ClientRegistrationForm, ClientLoginForm, BankerRegistrationForm,BankerLoginForm)
from app.models import (User, client, banker, financialdec)
import stripe


stripe_keys = {
    "secret_key": 'sk_test_51LUn73DmP0YmkHd0O5l77njV0F1M1QR8LzyaFKahQ8pugfrYV2swno5R7XhipkxbYcYqAgzUCoUBby1EQGEGnhw700852bTBqN',
    "publishable_key": 'pk_test_51LUn73DmP0YmkHd0j6LTuFIx8dw7qDjpba0Jzi4pgPvwKxIWlKOK1hHzUVD5E89UfmjqyduA2xMEteTTc1biY6jv00bbsb8Ap6'
}
stripe.api_key = stripe_keys["secret_key"]

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/')

@app.route('/',methods=['GET', 'POST'])
def landing():
    return render_template('index.html')

@app.route('/client',methods=['GET', 'POST'])
def client():
    if current_user.is_authenticated: 
        return redirect(url_for('clienthome'))
    clientregister_form = ClientRegistrationForm()
    clientlogin_form=ClientLoginForm()
    if clientregister_form.validate_on_submit():
        print('valid')
        hashed_password = bcrypt.generate_password_hash(clientregister_form.password.data).decode('utf-8')
        user = User(username=clientregister_form.username.data, nric=clientregister_form.nric.data, password=hashed_password,email=clientregister_form.email.data,banker=0)
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        newclient = client(userid=user.id)
        db.session.add(newclient)
        db.session.commit()
        flash("Your account has been created! You are now able to log in", 'success') 
        return redirect('/client#login')
    if clientlogin_form.validate_on_submit():
        user = User.query.filter_by(email=clientlogin_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, clientlogin_form.password.data) and user.banker==0:
            login_user(user, remember=clientlogin_form.remember.data)
            next_page = request.args.get('next')
            return redirect(url_for('clienthome'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('client.html',clientregister_form=clientregister_form, clientlogin_form=clientlogin_form)

@app.route('/banker',methods=['GET', 'POST'])
def banker():
    if current_user.is_authenticated: 
        return redirect(url_for('bankerhome'))
    bankerregister_form = BankerRegistrationForm()
    bankerlogin_form=BankerLoginForm()
    if bankerregister_form.validate_on_submit():
        print('valid')
        hashed_password = bcrypt.generate_password_hash(bankerregister_form.password.data).decode('utf-8')
        user = User(username=bankerregister_form.username.data,nric=bankerregister_form.nric.data, password=hashed_password,email=bankerregister_form.email.data,banker=1)
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        newbanker = banker(userid=user.id)
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

@app.route('/client/home',methods=['GET', 'POST'])
@login_required 
def clienthome():
    return render_template('clientlanding.html')


@app.route('/banker/home',methods=['GET', 'POST'])
@login_required
def bankerhome():
    return render_template('bankerlanding.html')


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