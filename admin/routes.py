from flask import Blueprint, redirect, url_for, request, flash, render_template, abort
from flask_login import login_user, current_user, login_required
from home.forms import RegisterForm, LoginForm
from classes.database import db_session
from classes.url import is_url_safe
from classes.registration import BackendAdmin, Role, User
import bcrypt
from admin import AdminTemplatesView
from functools import wraps

admin_bp = Blueprint('admin_bp', __name__, template_folder='admin-templates', static_folder='admin-static', url_prefix='/TownHall')


def admin_only(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.is_administrator:
                return f(*args, **kwargs)
            else:
                if request.endpoint != 'admin_bp.admin_login':
                    return redirect(url_for('admin_bp.admin_login'))
        else:
            return redirect(url_for('site.login'))
    return wrap

@admin_bp.before_request
@admin_only
def before_request():
    """ Protect all of the admin endpoints. """
    pass

@admin_bp.route('/')
def index():
    return render_template('admin_index.html')

@admin_bp.route('/test')
def test_admin():
    if current_user.is_authenticated:
        if current_user.is_administrator:
            return 'admin'
        else:
            return 'not admin'
    else:
        return 'anonymous'
    
        # admin_id=BackendAdmin.query.filter_by(name='avialxee').first().adminid
        # admin_user=BackendAdmin.query.get(admin_id)
        # role_id=Role.query.filter_by(role='admin').first().id
        # admin_user.role_id=role_id
        # db_session.add(admin_user)
        # db_session.commit()
        
        # if admin_user:
        #     return  str(admin_user.role_id)
        # else:
        #     return 'none'

@admin_bp.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm()
    if request.method=='POST':
        user = BackendAdmin.query.filter_by(name=request.form['username']
                        ).first()
        password = request.form['password'].encode('utf-8')
        
        if user:
            try:
                user.password.decode('utf-8')
                user_password=user.password
            except:
                user_password_encoded=user.password.encode('utf-8')
                user_password = bcrypt.hashpw(user_password_encoded, bcrypt.gensalt())

            if bcrypt.checkpw(password, user_password):
                user.is_auth = True
                user.is_admin = True
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
        return redirect(next_url or url_for('admin_bp.index'))
    return AdminTemplatesView().render('admin-login.html', form=form)

@admin_bp.route('/admin-register', methods=['GET', 'POST'])
def admin_register():
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
            return render_template('admin-register.html', form=form)

        if bcrypt.checkpw(repassword, password_hash) and password == repassword:
            user = BackendAdmin(name=username, email=email,
                    password=password_hash, fullname=fullname)
        else:
            flash("Password didn't match!")
            return render_template('admin-register.html', form=form)
        try:
            db_session.add(user)
            db_session.commit()
            flash('Registered!')
        except:
            flash('Failed!')
        
        next_url = request.args.get('next')
        if not is_url_safe(next_url):
            return abort(400)
        return redirect(next_url or url_for('admin_bp.admin_register') or url_for('admin.index'))
    return AdminTemplatesView().render('admin-register.html', form=form)


# error handlers
@admin_bp.app_errorhandler(404)
def page_not_found(e):
    referrer_log = request.referrer
    return render_template('404.html', log = referrer_log), 404

@admin_bp.app_errorhandler(400)
def page_not_found(e):
    referrer_log = request.referrer
    return render_template('400.html', log = referrer_log), 400