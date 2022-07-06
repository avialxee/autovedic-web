from wtforms import Form, StringField, validators, DecimalField, SelectField, TextAreaField
from wtforms.fields.simple import PasswordField, SubmitField
from markupsafe import Markup
class SearchForm(Form) :
    vehicle = SelectField(u'Vehicle ', choices=[(1, 'Car'), (2, 'Bikes')])
    brand = StringField('Brand',render_kw={"placeholder": "Brand"}, validators=[validators.required(), validators.Length(min=2, max=20)])
    model = StringField('Vehicle Model',render_kw={"placeholder": "Vehicle Model"}, validators=[validators.required(), validators.Length(min=2, max=30)])

class LoginForm(Form) :
    username = StringField('Username ', render_kw={"placeholder": "username"}, validators=[validators.required(), validators.Length(min=2, max=20)])
    password = PasswordField('Password ', render_kw={"placeholder": "Enter password"}, validators=[validators.required(), validators.Length(min=2, max=20)])
    submit = SubmitField('Login')

class RegisterForm(Form):
    firstname = StringField('First Name ',  render_kw={"placeholder": "First Name"}, validators=[validators.required(), validators.Length(min=2,max=20)])
    lastname = StringField('Last Name ',  render_kw={"placeholder": "Last Name"}, validators=[validators.required(), validators.Length(min=2,max=20)])
    email = StringField('Email ',  render_kw={"placeholder": "Email"}, validators=[validators.Email(), validators.required()])
    username = StringField('Username ', render_kw={"placeholder": "username"}, validators=[validators.required(), validators.Length(min=2, max=20)])
    password = PasswordField('Password ', render_kw={"placeholder": "Enter password"}, validators=[validators.required(), validators.Length(min=2, max=20)])
    repassword = PasswordField('repassword ', render_kw={"placeholder": "Re-enter password"}, validators=[validators.required(), validators.Length(min=2, max=20)])
    submit = SubmitField('Login')

class ContactUsForm(Form):
    fullname = StringField('Full Name', render_kw={"placeholder": "Full Name"}, validators=[validators.required(), validators.Length(min=2,max=40)])
    email = StringField('Email ',  render_kw={"placeholder": "Email"}, validators=[validators.Email(), validators.required()])
    phone = StringField('Phone ',  render_kw={"placeholder": "Phone"}, validators=[validators.Email(), validators.required()])
    message = TextAreaField('Message', render_kw={'placeholder':'Message'})
    # submit_value = Markup('<i class="fa fa-phone"></i>')
    # submit = SubmitField(submit_value)
