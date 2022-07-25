from flask import Blueprint, render_template, session, send_from_directory
from flask import flash, redirect, url_for,abort, render_template, request
from home.forms import SearchForm, LoginForm, RegisterForm, ContactUsForm
from api.routes import show_model
from classes.url import is_url_safe
from flask_login import login_user, login_required, logout_user, current_user
from functools import wraps
import os
from classes.smtp import fetch_smtp_settings
from classes.smtp.test_mail import test_msg
from classes.smtp.new_contactus import send_mail_newcontact
from classes.registration import BackendAdmin, User
from classes.database import db_session
import bcrypt
from classes.contact_details import record_contact_details
from datetime import datetime
import time            
site = Blueprint(name='site', import_name= __name__, template_folder='site-templates', static_folder='site-static')
from flask_wtf import csrf
# WRAPER

def auth_root(f):
    @wraps(f)
    @login_required
    def wrap(*args, **kwargs):
        if current_user.is_auth:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('site.lrq'))
        #except:
        #    abort(403)
    return wrap

# CONTEXTS
#@site.context_processor
#def search_context():
#    def model_brand():
#        val, http = show_model() # url='api/cars' key='Models' ||  show_model()['Models]
#        return val['Models']
#    return dict(model_brand=model_brand)

# ROUTES
@site.route('/', methods=['GET', 'POST'])
def index():
    sform = SearchForm(request.form)
    cform = ContactUsForm()
    csrf.generate_csrf()
    if request.method == 'POST':
        if cform.validate_on_submit():
            #flash('selected {}'.format(request.form['model_brand']))
            # session['search'] = 'vendor-search'
            # return redirect(url_for('site.search_result', service_gid=request.form['service_sname']))
                if all(val in request.form for val in ['car_model']):
                    date = str(datetime.now())
                    
                    formd={'brand':request.form['car_brand'], 
                            'model':request.form['car_model'],
                            'fullname':request.form['fullname'],
                            'email':request.form['email'],
                            'phone':request.form['phone'],
                            'time':date,
                            'ip':str(request.environ['REMOTE_ADDR'] if request.environ.get('HTTP_X_FORWARDED_FOR') is None else request.environ['HTTP_X_FORWARDED_FOR'])
                            }
                    # if formd['ip'] in 
                    df=record_contact_details(formd)
                    flash('Sent! We will contact you ASAP.', 'success')
                    fss=fetch_smtp_settings()
                    if fss['MAIL_NOTIFICATION_ON']:
                        send_mail_newcontact(fss['MAIL_DEFAULT_SENDER'],[fss['MAIL_NOTIFY_TO']], HTML=df.to_html())
                else:
                    flash('Failed! Please select Car Model', 'danger')
        else:
            flash('Try Again! All fields are compulsory.', 'danger')
    return render_template('home.html', content=sform, cform=cform, endpoint=request.endpoint)


# TODO: write this properly
@site.route('/test-mail',methods=['GET', 'POST'])
def test_mail_send():
    if test_msg('avialxee@gmail.com',['avialxee@gmail.com']):
        return {'mail':'not sent'}
    else:
        return {'mail':'sent'}

@site.route('/select-vehicle', methods=['GET', 'POST'])
@login_required
def select_vehicle():
    sfield = SearchForm(request.form)
    if request.method == 'POST':
        #flash('selected {}'.format(request.form['model_brand']))
        current_user.last_vehicle_model_nm = request.form['car_model']
        db_session.commit()
        next_url = request.args.get('next')
        if not is_url_safe(next_url):
            return abort(400)
        return redirect(next_url or url_for('site.index'))
    return render_template('select_vehicle.html')

@site.route('/select-location', methods=['GET', 'POST'])
@login_required
def select_location():
    if request.method == 'POST':
        current_user.pincode = request.form['map_pincode']
        db_session.commit()
        next_url = request.args.get('next')
        if not is_url_safe(next_url):
            return abort(400)
        return redirect(next_url or url_for('site.index'))

    return render_template('select_location.html')

@site.app_errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    referrer_log = request.referrer
    return render_template('404.html', log = referrer_log), 404

@site.route('/s/<service_gid>', methods=['GET','POST'])
@login_required
def search_result(service_gid):
    if 'search' in session:
        if session['search'] == 'vendor-search':
            flash (f'{service_gid}:working')
    else :
        abort(400)
    return render_template('vendor_search_result.html')

# TODO: make single user registration and login page
@site.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        repassword = request.form['repassword'].encode('utf-8')
        username = request.form['username']
        fullname = f"{request.form['firstname']} {request.form['lastname']}"
        
        # -- username validation
        special_characters = "!@#$%^&*()-+?=,<>/"
        
        # -- password hashing and checking
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password, salt)

        if any(c in special_characters for c in username):
            flash("Special characters are not allowed in username!")
            return render_template('register.html', form=form)

        if bcrypt.checkpw(repassword, password_hash) and password == repassword:
            user = User(name=username, email=email,
                    password=password_hash, fullname=fullname)
        else:
            flash("Password didn't match!")
            return render_template('register.html', form=form)
        try:
            db_session.add(user)
            db_session.commit()
            flash('Registered!')
        except:
            flash('Failed!')
        
        next_url = request.args.get('next')
        if not is_url_safe(next_url):
            return abort(400)
        return redirect(next_url or url_for('site.register') or url_for('site.index'))
    return render_template('register.html', form=form)

@site.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method=='POST':
        user = User.query.filter_by(name=request.form['username']
                        ).first()
        password = request.form['password'].encode('utf-8')
        if user:
            if bcrypt.checkpw(password, user.password):
                user.is_auth = True
                # db_session.add(user)
                db_session.commit()
                try:
                    login_user(user, remember=True)
                except:
                    user.is_auth = False
                    db_session.commit()
                
            else:
                flash('wrong password!')
        else:
            flash('failed!')
        next_url = request.args.get('next')
        if not is_url_safe(next_url):
            return abort(400)
        return redirect(next_url or url_for('site.user_account') or url_for('site.index'))
    return render_template('login.html', form=form)

@site.route('/account/edit-profile', methods=['GET', 'POST'])
@login_required
def user_account_edit():
    if request.method=='POST':
        print(request.form)
        if request.form['submit']=='profile':
            user = User.query.filter_by(name=current_user.name).first()
            if user is not None:
                # user=User(name=current_user.name, fullname=fullname,mobile=mobile,email=email)
                user.fullname=request.form['fullname']
                user.email=request.form['email']
                user.mobile=request.form['mobile']
                db_session.commit()
        if request.form['submit']=='password':
            password=request.form['password'].encode('utf-8')
            newpassword=request.form['newpassword'].encode('utf-8')
            repassword=request.form['repassword'].encode('utf-8')
            user = User.query.filter_by(name=current_user.name).first()
            if user:
                if bcrypt.checkpw(password, user.password):
                    # -- password hashing and checking
                    salt = bcrypt.gensalt()
                    password_hash = bcrypt.hashpw(newpassword, salt)
                    if bcrypt.checkpw(repassword, password_hash) and newpassword == repassword:
                        user.password=password_hash
                        db_session.commit()
                    else:
                        flash("Password didn't match!")
                        print('error')
            
    return render_template('user_account_edit.html')

@site.route('/logout', methods=['GET'])
@login_required
def logout():
    #session.clear()
    # print(current_user.userid)
    user = User.query.filter_by(sessionid=current_user.sessionid).first() or BackendAdmin.query.filter_by(sessionid=current_user.sessionid).first()
    user.is_auth=False
    db_session.commit()
    logout_user()
    return redirect(url_for('site.index'))

@site.route('/account', methods=['GET', 'POST'])
@login_required
def user_account():
    return render_template('user_account.html')

@site.route('/lrq')
@login_required
def lrq():
    user_id_str='USER'+str(int(time.time()))
    return {'hello':'world', 'user_id':user_id_str}

@site.route('/rootmedia/<path:filename>')
@auth_root
def root_media(filename):
    return send_from_directory(
            os.path.join('home'+url_for('site.static',filename='/rootmedia'), ''),
            filename
        )
@site.route('/home')
def home1():
    cform = ContactUsForm()

    if request.method == 'POST':
        #flash('selected {}'.format(request.form['model_brand']))
        session['search'] = 'vendor-search'
        return redirect(url_for('site.search_result', service_gid=request.form['service_sname']))
    return render_template('home.html', cform=cform)

# miscelleneous
@site.route('/contact-us')
def contactus():
    form = ContactUsForm()
    return render_template('contact_us.html', form=form)