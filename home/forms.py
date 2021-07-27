from wtforms import Form, StringField, validators, DecimalField, SelectField, BooleanField


class SearchForm(Form) :
    vehicle = SelectField(u'Vehicle ', choices=[(1, 'Car'), (2, 'Bikes')])
    brand = StringField('Brand',render_kw={"placeholder": "Brand"}, validators=[validators.required(), validators.Length(min=2, max=20)])
    model = StringField('Vehicle Model',render_kw={"placeholder": "Vehicle Model"}, validators=[validators.required(), validators.Length(min=2, max=30)])