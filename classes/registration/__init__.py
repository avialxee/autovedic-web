from re import L
from sqlalchemy.sql.sqltypes import Boolean, DateTime, FLOAT
from wtforms.fields import DateField
from flask_login import UserMixin
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.sql import func
from classes.database import Base, db_session, ForeignKey, relationship


role_association = Table('role_association', Base.metadata,
    Column('user_id', ForeignKey('users.userid'), primary_key=True),
    Column('role_id', ForeignKey('roles.id'), primary_key=True),
    Column('admin_id', ForeignKey('admins.adminid'), primary_key=True),extend_existing=True
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

    # authorisation
    password = Column(String(100))
    name = Column(String(15), unique=True, nullable=False)
    is_auth = Column(Boolean, default=False)
    
    # # relationships
    role_id = Column(Integer, ForeignKey("roles.id"))


    def __repr__(self):
        return f'<User {self.name!r}>'

    def is_active(self):
        return True

    def is_authenticated(self):
        return self.is_auth

    def get_id(self):
        return self.userid

    def is_anonymous(self):
        if self.auth == True:
            return False
        else:
            return True 

    def is_administrator(self):
        return True#self.user_role.is_admin()

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    role = Column(String(15), nullable=False )
    

    # relationship
    user = relationship("User",
                    secondary=role_association,
                    backref="role", lazy='dynamic')

    admin_user = relationship("BackendAdmin", secondary=role_association,
                backref="role")
        
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

    # roles
    is_admin = Column(Boolean, default=False)
    is_content_creator = Column(Boolean, default=False)
    is_auth = Column(Boolean, default=False)    
    is_active = is_auth = Column(Boolean, default=False)

    # relationship
    # role_id = Column(Integer, ForeignKey("roles.id"))
    role_id = Column(Integer, ForeignKey("roles.id"))

    def is_active(self):
        return self.is_active

    def is_authenticated(self):
        return self.is_auth

    def get_id(self):
        return self.adminid

    def is_anonymous(self):
        if self.auth == True:
            return False
        else:
            return True 

    def is_administrator(self):
        return self.is_admin
