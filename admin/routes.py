from flask import Blueprint, redirect, url_for, request, flash, render_template, abort
from flask_login import login_user, current_user, login_required
from home.forms import RegisterForm, LoginForm
from classes.database import db_session
from classes.url import is_url_safe
from classes.registration import BackendAdmin
import bcrypt
from admin import AdminTemplatesView

admin_bp = Blueprint('admin_bp', __name__, template_folder='admin-templates', static_folder='admin-static', url_prefix='/admin')

@admin_bp.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm()
    if request.method=='POST':
        user = BackendAdmin.query.filter_by(name=request.form['username']
                        ).first()
        password = request.form['password'].encode('utf-8')
        if user:
            if bcrypt.checkpw(password, user.password):
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
        return redirect(next_url or url_for('admin.index'))
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