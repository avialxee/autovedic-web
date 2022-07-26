from flask import Blueprint, redirect, url_for, abort
from flask_admin.contrib.sqla import ModelView
from classes.registration import BackendAdmin, Role, User
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
    
    

class UserView(AdminModelView):
    column_editable_list = ['email', 'first_name', 'last_name']
    column_searchable_list = column_editable_list
    column_exclude_list = ['password']
    #form_excluded_columns = column_exclude_list
    column_details_exclude_list = column_exclude_list
    column_filters = column_editable_list
    

class AdminDashboard(AdminIndexView):
    def is_accessible(self):        
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        abort(404)
    
    
            
admin = Admin(name='Dashboard', template_mode='bootstrap4', index_view=AdminDashboard(name='Home', url='/TownHall'), url='/TownHall')


def register_admin(db_session):
    # admin.add_view(ModelView(AdminModelView, db_session))
    admin.add_view(AdminModelView(BackendAdmin, db_session, category="Team"))
    admin.add_view(AdminModelView(User, db_session, category="Team", endpoint='/Team'))
    admin.add_view(AdminModelView(Role, db_session, category="Team"))
    