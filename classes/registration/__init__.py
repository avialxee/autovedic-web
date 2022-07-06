from email.policy import default
from re import L
from unicodedata import name
from sqlalchemy.sql.sqltypes import Boolean, DateTime, FLOAT, Time
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import column_property
from sqlalchemy.sql.expression import cast
from wtforms.fields import DateField
from flask_login import UserMixin
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.sql import func
from classes.database import Base, db_session, ForeignKey, relationship
import bcrypt
import time
import datetime

role_association = Table('role_association', Base.metadata,
    Column('user_id', ForeignKey('users.userid'), primary_key=True),
    Column('role_id', ForeignKey('roles.id'), primary_key=True),
   
)

class User(Base, UserMixin):
    query = db_session.query_property()
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    
    # primary keys are required by SQLAlchemy
    userid = Column(Integer, primary_key=True)
    

    # details
    email = Column(String(60), unique=True, nullable=False)
    mobile = Column(String(15), unique=True)
    fullname = Column(String(100))
    address1 = Column(String(100))
    address2 = Column(String(100))
    city = Column(String(30))
    pincode = Column(String(6))
    lat = Column(FLOAT(precision=10, decimal_return_scale=None))
    lon = Column(FLOAT(precision=10, decimal_return_scale=None))
    vehicle_details = Column(String(450)) # list of gid | use json format: {gid: {'reg_no': reg_no , 'year': year}}

    # user_experience
    cart_id = Column(String(5))
    last_vehicle_gid = Column(String(5)) # only one gid
    last_vehicle_model_nm = Column(String(15)) # corresponding to gid

    # time_calculations
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    session_up = Column(String(20), server_default=cast(time.time(), Integer), onupdate=cast(time.time(), Integer))
    
    @hybrid_property
    def sessionid(self):
        # id = 'U'+str(self.userid)+str(int(time.mktime(datetime.datetime.fromisoformat(str(self.session_up)).timetuple())))
        id = 'U'+str(self.userid)+str(self.session_up)
        return id
    @sessionid.expression
    def sessionid(cls):
        return 'U'+cast(cls.userid, String)+cast(cls.session_up, String) 

    # authorisation
    password = Column(String(100))
    name = Column(String(15), unique=True, nullable=False)
    is_auth = Column(Boolean, default=False)
    
    # # relationships
    role_id = Column(Integer, ForeignKey("roles.id"))
    role = Column(String(20), ForeignKey("roles.role"))

    def __repr__(self):
        return f'<User {self.name!r}>'

    def is_active(self):
        return True

    def is_authenticated(self):
        return self.is_auth

    def get_id(self):
        return self.sessionid

    def is_anonymous(self):
        if self.auth == True:
            return False
        else:
            return True 
    @property
    def is_administrator(self):
        if self.role=='admin':
            return True
        else:
            return False
    
    

class Role(Base):
    query = db_session.query_property()
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    role = Column(String(20), nullable=False, default='user' )
        
    def is_user(self):
        return True
    
    def is_vendor(self):
        return False
    
    def is_content_creator(self):
        return False
    
    def is_admin(self):
        return self.is_admin
    
    def is_developer(self):
        return False

    def is_root(self):
        return False

class BackendAdmin(Base, UserMixin):
    query = db_session.query_property()
    __tablename__ = 'admins'
    __table_args__ = {'extend_existing': True}
    
    # primary keys are required by SQLAlchemy
    adminid = Column(Integer, primary_key=True) 

    # details
    email = Column(String(60), unique=True, nullable=False)
    mobile = Column(String(15), unique=True)
    fullname = Column(String(100))

    # auth
    password = Column(String(100))
    name = Column(String(15), unique=True, nullable=False)

    # on update
    session_up = Column(String(20), server_default=cast(time.time(), Integer), onupdate=cast(time.time(), Integer))
    
    @hybrid_property
    def sessionid(self):
        # id = 'U'+str(self.userid)+str(int(time.mktime(datetime.datetime.fromisoformat(str(self.session_up)).timetuple())))
        id = 'B'+str(self.adminid)+str(self.session_up)
        return id
    @sessionid.expression
    def sessionid(cls):
        return 'B'+cast(cls.adminid, String)+cast(cls.session_up, String) 

    # roles
    is_admin = Column(Boolean, default=False)
    is_content_creator = Column(Boolean, default=False)
    is_auth = Column(Boolean, default=False)    
    is_active = Column(Boolean, default=False)

    # relationship
    # role_id = Column(Integer, ForeignKey("roles.id"))
    role_id = Column(Integer, ForeignKey("roles.id"))

    def is_active(self):
        return self.is_active

    def is_authenticated(self):
        return self.is_auth

    def get_id(self):
        # adminsessionid='A'+str(self.adminid)+str(self.session_id)
        return self.sessionid

    def is_anonymous(self):
        if self.auth == True:
            return False
        else:
            return True 

    def is_administrator(self):
        return self.is_admin

def add_role(role_name):
    role_session=Role(role=role_name)
    db_session.add(role_session)
    db_session.commit()
    return f'created role:{role_name}', 200

def default_admin():
    try:
        role_id=Role.query.filter_by(role='admin').first().id
    except:
        add_role(role_name='admin')
        role_id=Role.query.filter_by(role='admin').first().id
    db_session.commit()
    if not BackendAdmin.query.filter_by(name='admin').first():# -- password hashing and checking
        salt = bcrypt.gensalt()
        default_pwd='admin'
        password_hash = bcrypt.hashpw(default_pwd.encode('utf-8'), salt)
        admin=BackendAdmin(name='admin', password=password_hash, email='admin@example.com', role_id=role_id)
        db_session.add(admin)
        db_session.commit()

def default_user():
    try:
        role_id=Role.query.filter_by(role='user').first().id
    except:
        add_role(role_name='user')
        role_id=Role.query.filter_by(role='user').first().id
    db_session.commit()
    if not User.query.filter_by(name='user').first():# -- password hashing and checking
        salt = bcrypt.gensalt()
        default_pwd='user'
        password_hash = bcrypt.hashpw(default_pwd.encode('utf-8'), salt)
        user=User(name='user', password=password_hash, email='user@example.com', role_id=role_id)
        db_session.add(user)
        db_session.commit()
