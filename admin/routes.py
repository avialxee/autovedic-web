from distutils.command.config import config
from email.policy import default
import pandas as pd
from werkzeug.utils import secure_filename
from flask import Blueprint, redirect, url_for, request, flash, render_template, abort, current_app, Response
from flask_login import login_user, current_user, login_required, logout_user
from requests import session
from home.forms import RegisterForm, LoginForm
from classes.database import db_session
from classes.url import is_url_safe
from classes.registration import BackendAdmin, Role, User
from classes.contact_details import read_contact_details, remove_contact_details
from classes.vehicles import load_car_table,remove_car_details
from classes.services import load_service_table
from classes.maps import load_map_table
import bcrypt
from admin import AdminTemplatesView, AdminModelView
from functools import wraps
from pandas import read_json
from classes.smtp import set_smtp_settings, fetch_smtp_settings, mail
from admin.forms import SetSMTP,Configuration
import os
import dotenv
admin_bp = Blueprint('admin_bp', __name__, template_folder='admin-templates', static_folder='admin-static', url_prefix='/TownHall')


def admin_only(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.is_administrator:
                return f(*args, **kwargs)
            else:
                if not request.endpoint in ['admin_bp.admin_login','admin_bp.admin_register']:
                    return redirect(url_for('admin_bp.admin_login'))
        else:
            return redirect(url_for('site.login'))
    return wrap

@admin_bp.before_request
@admin_only
def before_request():
    dotenv_file='home/site-static/rootmedia/.env'
    current_app.config.update({'ROOTFOLDER':'home'+url_for('site.static', filename='rootmedia'),
    })
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
    url_deleterow=url_for('admin_bp.delete_row_forcontactus')
    return render_template('admin_index.html', contact_details=df.to_html(table_id='contact-us-table',classes='table table-striped table-responsive table-bordered'), urldelrow=url_deleterow,)

def dffromtable(tablename):
    df=None
    if tablename=='car-table':
        df=load_car_table()
    elif tablename=='service-table':
        df=load_service_table()
    elif tablename=='map-table':
        df=load_map_table()
    return df

def exportcsvhead(df,tablename):
    return Response(
        df.to_csv(index=False),
        mimetype="text/csv",
        headers={"Content-disposition":
        f"attachment; filename={tablename}.csv"})

@admin_bp.route('/downloaddf/<tablename>', defaults={'list_all':None})
@admin_bp.route('/downloaddf/<tablename>/<list_all>')
def download_tempcsv(tablename, list_all):
    df=dffromtable(tablename)
    if list_all is None:
        return exportcsvhead(df.head(), tablename)
    else:
        return exportcsvhead(df, tablename)



@admin_bp.route('/products/<tablename>')
def products(tablename):
    df=dffromtable(tablename=tablename)
    if df is None: abort(404)
    df.columns.name = df.index.name
    df.index.name = None

    url_delete_product=url_for('admin_bp.delete_product', tablename=tablename)
    table_details=df.to_html(table_id=tablename,classes='table table-striped table-responsive table-bordered')
    return render_template('admin_products.html', table_details=table_details, urldelrow=url_delete_product, tablename=tablename, exportcsv=url_for('admin_bp.download_tempcsv', tablename=tablename))

def compare_df(f1,f2):
    dfc=None
    try:
        df=pd.read_csv(f1)
        dfc=pd.read_csv(f2)
        compare_heading = list(df)==list(dfc)
        
    except:
        compare_heading=False
    return dfc,compare_heading
@admin_bp.route('/upload-rootmedia/<filename>', methods=['POST'])
def uploadto_rootmedia(filename):
    if request.method=='POST':
        file = request.files['file']
        uploadfile=os.path.join('home'+url_for('site.static', filename=f'rootmedia'), filename)
        if 'csv' in filename:
            # df=pd.read_csv(file)
            df,comparedf=compare_df(uploadfile,file)
            if file and comparedf:
                    # file1 = request.files['file']
                    # file1.save(uploadfile)
                    df.to_csv(uploadfile, index=False)
                    return 'success', 200
            else:
                return 'check file', 400
    

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
    if str(current_app.config['ADMINSIGNUP']).lower() == 'false':
        return redirect(url_for('admin_bp.admin_login'))
    else:
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
        return render_template('admin-register.html', form=form)


@admin_bp.route('/profile', methods=['GET', 'POST'])
def admin_profile():
    if request.method=='POST':
        print(request.form)
        if request.form['submit']=='profile':
            user = BackendAdmin.query.filter_by(name=current_user.name).first()
            if user is not None:
                # user=User(name=current_user.name, fullname=fullname,mobile=mobile,email=email)
                user.fullname=request.form['fullname']
                user.email=request.form['email']
                user.mobile=request.form['mobile']
                try:
                    db_session.commit()
                except:
                    print('check input')
        if request.form['submit']=='password':
            password=request.form['password'].encode('utf-8')
            newpassword=request.form['newpassword'].encode('utf-8')
            repassword=request.form['repassword'].encode('utf-8')
            user = BackendAdmin.query.filter_by(name=current_user.name).first()
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
    return render_template('admin_profile.html')

@admin_bp.route('/settings', methods=['GET', 'POST'])
def admin_settings():
    # envfile=url_for('site.static', filename='rootmedia/.env', _external=True)
    envfile='home/site-static/rootmedia/.env'
    fss=fetch_smtp_settings(envfile)
    fcf=current_app.config['ADMINSIGNUP']
    sform=SetSMTP()
    confform=Configuration()
    if request.method=='POST':
        print(request.form)
        if request.form['submit']=='SMTP':
            fss['MAIL_SERVER']=request.form['MAIL_SERVER']
            fss['MAIL_PORT']=request.form['MAIL_PORT']
            fss['MAIL_USERNAME']=request.form['MAIL_USERNAME']
            fss['MAIL_PASSWORD']=request.form['MAIL_PASSWORD']
            fss['MAIL_DEFAULT_SENDER']=request.form['MAIL_DEFAULT_SENDER']
            fss['MAIL_NOTIFY_TO']=request.form['MAIL_NOTIFY_TO']
            fss['MAIL_USE_TLS']=request.form['MAIL_USE_TLS'].lower() == 'true'
            fss['MAIL_USE_SSL']=request.form['MAIL_USE_SSL'].lower() == 'true'
            fss['MAIL_NOTIFICATION_ON']=request.form['MAIL_NOTIFICATION_ON'].lower() == 'true'
        if request.form['submit']=='Configure':
            fcf=fss['ADMINSIGNUP']=request.form['ADMINSIGNUP'].lower()=='true'
        # try:
        set_smtp_settings(envfile,**fss)
        flash('Success!')
        current_app.config.update(fss)
        print(fss)
        mail.init_app(current_app)
        # except:
        #     flash('Failed!')
    return render_template('settings.html', sform=sform, fss=fss, fcf=fcf, confform=confform)

# delete row from a csv file
@admin_bp.route('/delete-row-contactus/', methods=['POST'])
def delete_row_forcontactus():
    if request.method == 'POST':
        row_no=request.form['rowno']
        res=remove_contact_details(row_no)
        return 'success', 200

@admin_bp.route('/delete-product/<tablename>', methods=['POST'])
def delete_product(tablename):
    if request.method == 'POST':
        row_no=int(request.form['rowno'])
        url_db = current_app.config['ROOTFOLDER']+f'/{tablename}.csv'
        df = pd.read_csv(url_db)
        rows =  row_no
        print(f'deleting : {rows}')
        print(df.columns)
        df.drop(rows, inplace=True)
        df.to_csv(url_db, index=False)
    
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