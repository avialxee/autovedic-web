from wtforms import Form, StringField, validators, DecimalField, SelectField

from wtforms.fields.simple import PasswordField, SubmitField


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
    submit = SubmitField('Login')