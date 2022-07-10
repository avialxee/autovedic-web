from fileinput import filename
from flask import Blueprint, redirect, url_for, request, flash, render_template, abort, current_app
from flask_login import login_user, current_user, login_required, logout_user
from requests import session
from home.forms import RegisterForm, LoginForm
from classes.database import db_session
from classes.url import is_url_safe
from classes.registration import BackendAdmin, Role, User
import bcrypt
from admin import AdminTemplatesView
from functools import wraps
from classes.contact_details import read_contact_details, remove_contact_details
from pandas import read_json
from classes.smtp import set_smtp_settings, fetch_smtp_settings, mail
from admin.forms import SetSMTP
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
# @admin_only
def before_request():
    """ Protect all of the admin endpoints. """
    pass

@admin_bp.route('/')
def index():
    df=read_contact_details()
    df.index+=1
    serial=df.index.set_names("#")
    df.index=serial
    df.columns.name = df.index.name
    df.index.name = None
    # df.drop(inplace=True, index=False)
    url_deleterow=url_for('admin_bp.delete_row_forcontactus')
    return render_template('admin_index.html', contact_details=df.to_html(table_id='contact-us-table',classes='table table-striped table-responsive table-bordered'), urldelrow=url_deleterow,)

@admin_bp.route('/test')
def test_admin():
    if current_user.is_authenticated:
        if current_user.is_administrator:
            return current_user.get_id()
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

@admin_bp.route('/logout')
def admin_logout():
    logout_user()
    next_url = request.args.get('next')
    return redirect(next_url or url_for('site.index'))

@admin_bp.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm()
    next_url = request.args.get('next')
    if current_user.is_administrator:
        return redirect(url_for('admin_bp.index'))
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
        
        if not is_url_safe(next_url):
            return abort(400)
        return redirect(next_url or url_for('admin_bp.index'))
    return render_template('admin-login.html', form=form)

@admin_bp.route('/admin-register', methods=['GET', 'POST'])
def admin_register():
    form = RegisterForm()
    if current_user.is_administrator:
        return redirect(url_for('admin_bp.index'))
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
        return redirect(next_url or url_for('admin_bp.admin_register') or url_for('admin_bp.index'))
    return AdminTemplatesView().render('admin-register.html', form=form)

@admin_bp.route('/profile', methods=['GET', 'POST'])
def admin_profile():
    return render_template('admin_profile.html')

@admin_bp.route('/settings', methods=['GET', 'POST'])
def admin_settings():
    # envfile=url_for('site.static', filename='rootmedia/.env', _external=True)
    envfile='home/site-static/rootmedia/.env'
    fss=fetch_smtp_settings(envfile)
    sform=SetSMTP()
    if request.method=='POST':
        print(request.form)
        fss['MAIL_SERVER']=request.form['MAIL_SERVER']
        fss['MAIL_PORT']=request.form['MAIL_PORT']
        fss['MAIL_USERNAME']=request.form['MAIL_USERNAME']
        fss['MAIL_PASSWORD']=request.form['MAIL_PASSWORD']
        fss['MAIL_DEFAULT_SENDER']=request.form['MAIL_DEFAULT_SENDER']
        fss['MAIL_NOTIFY_TO']=request.form['MAIL_NOTIFY_TO']
        fss['MAIL_USE_TLS']=request.form['MAIL_USE_TLS'].lower() == 'true'
        fss['MAIL_USE_SSL']=request.form['MAIL_USE_SSL'].lower() == 'true'
        fss['MAIL_NOTIFICATION_ON']=request.form['MAIL_NOTIFICATION_ON'].lower() == 'true'

        # try:
        set_smtp_settings(envfile,**fss)
        flash('Success!')
        current_app.config.update(fss)
        print(fss)
        mail.init_app(current_app)
        # except:
        #     flash('Failed!')
    return render_template('settings.html', sform=sform, fss=fss)

# delete row from a csv file
@admin_bp.route('/delete-row-contactus/', methods=['POST'])
def delete_row_forcontactus():
    if request.method == 'POST':
        print('method is POST')
        row_no=request.form['rowno']
        res=remove_contact_details(row_no)
        return 'success', 200






# error handlers
@admin_bp.app_errorhandler(404)
def page_not_found(e):
    referrer_log = request.referrer
    return render_template('404.html', log = referrer_log), 404

@admin_bp.app_errorhandler(400)
def page_not_found(e):
    referrer_log = request.referrer
    return render_template('400.html', log = referrer_log), 400