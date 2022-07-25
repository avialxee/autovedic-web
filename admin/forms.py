from email.policy import default
from wtforms import Form, StringField, validators, DecimalField, SelectField, TextAreaField, BooleanField
from wtforms.fields.simple import PasswordField, SubmitField
from markupsafe import Markup

class SetSMTP(Form):
    fullname = StringField('Full Name', render_kw={"placeholder": "Full Name"}, validators=[validators.required(), validators.Length(min=2,max=40)])
    MAIL_SERVER=StringField('MAIL_SERVER', render_kw={'placeholder':'MAIL_SERVER'}, validators=[validators.required(), validators.Length(min=2,max=40)])
    MAIL_PORT=StringField('MAIL_PORT', render_kw={'placeholder':'MAIL_PORT'}, validators=[validators.required(), validators.Length(min=2,max=40)])
    MAIL_USERNAME=StringField('MAIL_USERNAME', render_kw={'placeholder':'MAIL_USERNAME'}, validators=[validators.required(), validators.Length(min=2,max=40)])
    MAIL_PASSWORD=StringField('MAIL_PASSWORD', render_kw={'placeholder':'MAIL_PASSWORD'}, validators=[validators.required(), validators.Length(min=2,max=40)])
    MAIL_DEFAULT_SENDER=StringField('Email ',  render_kw={"placeholder": "Email"}, validators=[validators.Email(), validators.required()])
    MAIL_NOTIFY_TO=StringField('Email ',  render_kw={"placeholder": "Email"}, validators=[validators.Email(), validators.required()])
    MAIL_USE_TLS=SelectField(choices=[(True, 'True'), (False, 'False')],validators=[validators.required()],coerce=lambda x: x == 'True')
    MAIL_USE_SSL=SelectField(choices=[(True, 'True'), (False, 'False')],validators=[validators.required()],coerce=lambda x: x == 'True')
    MAIL_NOTIFICATION_ON=SelectField(choices=[(True, 'True'), (False, 'False')],validators=[validators.required()],coerce=lambda x: x == 'True')

class Configuration(Form):
    ADMINSIGNUP=SelectField(choices=[(True, 'True'), (False, 'False')],validators=[validators.required()],coerce=lambda x: x == 'True')