from flask import Blueprint, redirect, url_for, abort
from flask_admin.contrib.sqla import ModelView
from classes.registration import User, Role
from flask_login import current_user, login_required
from flask_admin import BaseView, expose, AdminIndexView, Admin

class AdminTemplatesView(BaseView):
    def __init__(self, *args, **kwargs):
        self._default_view = True
        super(AdminTemplatesView, self).__init__(*args, **kwargs)
        self.admin = Admin()


class AdminModelView(ModelView):
    def is_accessible(self):        
        if current_user.is_authenticated:
            return current_user.is_administrator
        else:
            return False
    
    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible():
            abort(404)

class AdminDashboard(AdminIndexView):
    def is_accessible(self):        
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        abort(404)
            
admin = Admin(name='Dashboard', template_mode='bootstrap4', index_view=AdminDashboard())
class AnalyticsView(BaseView):
    def is_accessible(self):        
        if current_user.is_authenticated:
            return current_user.is_administrator
        else:
            return False
    
    def inaccessible_callback(self, name, **kwargs):
        abort(404)
    #def is_accessible(self):
    #    if current_user.is_authenticated:
    #        return current_user.is_administrator
    #    else:
    #        return False
    #from .routes import admin_bp
    @expose('/')
    @login_required
    def index(self):
        return self.render('analytics_index.html')

class VendorView(BaseView):
    #def is_accessible(self):
    #    if current_user.is_authenticated:
    #        return current_user.is_administrator
    #    else:
    #        return False
    #from .routes import admin_bp
    @expose('/')
    @login_required
    def index(self):
        return self.render('analytics_index.html')

#admin.add_view(AnalyticsView(name='Analytics'))
# admin.add_view(VendorView(name='Vendors', endpoint='vendors'))
def register_admin(db_session):
    #admin.add_view(ModelView(AdminModelView, db_session))
    admin.add_view(AdminModelView(User, db_session))
    admin.add_view(AdminModelView(Role, db_session))
    admin.add_view(AnalyticsView(name='Analytics'))
    