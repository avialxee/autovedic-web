from flask import Blueprint, render_template, session, send_from_directory
from flask import flash, redirect, url_for,abort, render_template, request
from home.forms import SearchForm, LoginForm, RegisterForm
from api.routes import show_model
from classes.url import is_url_safe
from flask_login import login_user, login_required, logout_user, current_user
from functools import wraps
import os
from classes.registration import User
from classes.database import db_session

site = Blueprint('site', __name__, template_folder='site-templates', static_folder='site-static')

# WRAPER

def auth_root(f):
    @wraps(f)
    @login_required
    def wrap(*args, **kwargs):
        if current_user.name == 'avialxee':
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
    sfield = SearchForm(request.form)
    if request.method == 'POST':
        #flash('selected {}'.format(request.form['model_brand']))
        session['search'] = 'vendor-search'
        return redirect(url_for('site.search_result'))
    return render_template('home.html', content=sfield)

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
        current_user.pincode = request.form['pincode']
        db_session.commit()
        next_url = request.args.get('next')
        if not is_url_safe(next_url):
            return abort(400)
        return redirect(next_url or url_for('site.index'))

    return render_template('select_location.html')


@site.route('/search-services', methods=['GET', 'POST'])
def search_services():
    return render_template('search_services.html')

@site.route('/s', methods=['GET','POST'])
@login_required
def search_result():
    if session['search'] == 'vendor-search':
        sfield = request.form.get('model')
        return render_template('vendor_search_result.html')

# TODO: make single user registration and login page
@site.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']
        fullname = f"{request.form['firstname']} {request.form['lastname']}"
        user = User(name=username, email=email,
                    password=password, fullname=fullname)
        try:
            db_session.add(user)
            db_session.commit()
            flash('Registered!')
            
        except:
            flash('failed!')
            
        
        next_url = request.args.get('next')
        if not is_url_safe(next_url):
            return abort(400)
        return redirect(next_url or url_for('site.index'))
    return render_template('register.html', form=form)

@site.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method=='POST':
        user = User.query.filter_by(name=request.form['username']
                        ).first()
        if user:
            if user.password == request.form['password']:
                user.is_auth = True
                db_session.add(user)
                db_session.commit()
                login_user(user, remember=True)
                
            else:
                flash('wrong password!')
        else:
            flash('failed!')
        next_url = request.args.get('next')
        if not is_url_safe(next_url):
            return abort(400)
        return redirect(next_url or url_for('site.user_account') or url_for('site.index'))
    return render_template('login.html', form=form)

@site.route('/logout', methods=['GET'])
@login_required
def logout():
    #session.clear()
    logout_user()
    return redirect(url_for('site.index'))

@site.route('/account', methods=['GET', 'POST'])
@login_required
def user_account():
    return render_template('user_account.html')

@site.route('/lrq')
@login_required
def lrq():
    return {'hello':'world'}

@site.route('/rootmedia/<path:filename>')
@auth_root
def root_media(filename):
    return send_from_directory(
            os.path.join('home'+url_for('site.static',filename='/rootmedia'), ''),
            filename
        )
