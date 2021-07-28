from flask import Blueprint, render_template
from flask import Flask, flash, redirect, url_for,abort, render_template, request, jsonify
from home.forms import SearchForm, LoginForm, RegisterForm
from api.routes import show_model
from classes.vehicles.vehicle import load_vehicles
from is_safe_url import is_safe_url
from flask_login import login_user, login_required
from classes.login import User

site = Blueprint('site', __name__, template_folder='site-templates', static_folder='site-static')

# CONTEXTS
@site.context_processor
def search_context():
    def model_brand():
        val, http = show_model() # url='api/cars' key='Models' ||  show_model()['Models]
        return val['Models']
    return dict(model_brand=model_brand)

# ROUTES
@site.route('/', methods=['GET', 'POST'])
def index():
    sfield = SearchForm(request.form)
    if request.method == 'POST':
        flash('selected {}'.format(request.form['model_brand']))
    return render_template('home.html', content=sfield)

@site.route('/vendors', methods=['POST'])
def search_vendor():
    return render_template('vendor_search_result.html')

# TODO: make single user registration and login page
@site.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method=='POST':
        flash('Registered!')
        next_url = request.args.get('next')
        return redirect(next_url or url_for('site.index'))
    return render_template('register.html', form=form)

@site.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method=='POST':
        # Login and validate the user.
        # user should be an instance of your `User` class
        user = User(id=1, name=request.form['username'],
                        password=request.form['password'])
        login_user(user)

        flash(f'hey! {user.name}')

        next = request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        #if not is_safe_url(next):
        #    return abort(400)

        return redirect(next or url_for('site.index'))
    return render_template('login.html', form=form)

@site.route('/lrq')
@login_required
def login_require():
    return {'hello':'world'}
