from flask_wtf import FlaskForm, RecaptchaField
from wtforms import Form, StringField, validators, DecimalField, SelectField, TextAreaField
from wtforms.fields.simple import PasswordField, SubmitField
from markupsafe import Markup
from flask import current_app
import os

def recaptcha_config():
    config={}
    config['RECAPTCHA_USE_SSL']= False
    config['RECAPTCHA_PUBLIC_KEY']= os.environ['RECAPTCHA_PUBLIC_KEY']
    config['RECAPTCHA_PRIVATE_KEY']=os.environ['RECAPTCHA_PRIVATE_KEY']
    config['RECAPTCHA_OPTIONS'] = {'theme':'white'}
    return config

class SearchForm(FlaskForm) :
    vehicle = SelectField(u'Vehicle ', choices=[(1, 'Car'), (2, 'Bikes')])
    brand = StringField('Brand',render_kw={"placeholder": "Brand"}, validators=[validators.required(), validators.Length(min=2, max=20)])
    model = StringField('Vehicle Model',render_kw={"placeholder": "Vehicle Model"}, validators=[validators.required(), validators.Length(min=2, max=30)])

class LoginForm(FlaskForm) :
    username = StringField('Username ', render_kw={"placeholder": "username"}, validators=[validators.required(), validators.Length(min=2, max=20)])
    password = PasswordField('Password ', render_kw={"placeholder": "Enter password"}, validators=[validators.required(), validators.Length(min=2, max=20)])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    firstname = StringField('First Name ',  render_kw={"placeholder": "First Name"}, validators=[validators.required(), validators.Length(min=2,max=20)])
    lastname = StringField('Last Name ',  render_kw={"placeholder": "Last Name"}, validators=[validators.required(), validators.Length(min=2,max=20)])
    email = StringField('Email ',  render_kw={"placeholder": "Email"}, validators=[validators.Email(), validators.required()])
    username = StringField('Username ', render_kw={"placeholder": "username"}, validators=[validators.required(), validators.Length(min=2, max=20)])
    password = PasswordField('Password ', render_kw={"placeholder": "Enter password"}, validators=[validators.required(), validators.Length(min=2, max=20)])
    repassword = PasswordField('repassword ', render_kw={"placeholder": "Re-enter password"}, validators=[validators.required(), validators.Length(min=2, max=20)])
    submit = SubmitField('Login')

class ContactUsForm(FlaskForm):
    fullname = StringField('Full Name', render_kw={"placeholder": "Full Name"}, validators=[validators.required(), validators.Length(min=2,max=40)])
    email = StringField('Email ',  render_kw={"placeholder": "Email"}, validators=[validators.Email(), validators.required()])
    phone = StringField('Phone ',  render_kw={"placeholder": "Phone"}, validators=[validators.required()])
    message = TextAreaField('Message', render_kw={'placeholder':'Message'})
    recaptcha = RecaptchaField()
    # submit_value = Markup('<i class="fa fa-phone"></i>')
    # submit = SubmitField(submit_value)
