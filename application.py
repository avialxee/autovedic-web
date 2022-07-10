import os
from flask_login import LoginManager
from flask import Flask
from requests import session
from settings import MAIL_SERVER,MAIL_PORT,MAIL_USE_TLS,MAIL_USERNAME,MAIL_PASSWORD
from classes.smtp import fetch_smtp_settings
from home.forms import recaptcha_config

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(12)
    
    app.url_map.strict_slashes = False

    login_manager = LoginManager(app)
    
    
    
    # --- Blueprints configuration -----
    # from admin import register_admin, admin
    from admin.routes import admin_bp
    ##app.register_blueprint(admin)
    
    
    from api.routes import api
    app.register_blueprint(api)

    from home.routes import site
    app.register_blueprint(site)
    login_manager.init_app(site)

    # admin.init_app(app)    
    app.register_blueprint(admin_bp)
    
    login_manager.blueprint_login_views = {
    'admin' : 'admin_bp.admin_login',
    #'analytics' : 'admin_bp.admin_login',
    'site': 'site.login',
    }
    
    from classes.registration import User, BackendAdmin
    @login_manager.user_loader
    def load_user(userid):
        fid = User.query.filter_by(sessionid=userid).first()
        if fid == None:
            userid = userid.replace('U', 'B')
            fid = BackendAdmin.query.filter_by(sessionid=userid).first()
         
        return fid
    
    from classes import classdef
    app.register_blueprint(classdef)

    # --- mail configuration -----
    # app.config.update(dict(
    #     MAIL_SERVER = MAIL_SERVER,
    #     MAIL_PORT = MAIL_PORT,
    #     MAIL_USE_TLS = MAIL_USE_TLS,
    #     MAIL_USERNAME = MAIL_USERNAME,
    #     MAIL_PASSWORD = MAIL_PASSWORD
    # ))
    
    app.config.update(fetch_smtp_settings('home/site-static/rootmedia/.env'))
    app.testing=False
    app.config.update(recaptcha_config())
    
    from classes.smtp import mail
    mail.init_app(app)

    # --- database configuration -----
    from classes.database import db_session, init_db
    init_db()
    # register_admin(db_session)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()
    return app
application = create_app()



# ======== Main ============================================================== #
if __name__ == "__main__":
    application.run(debug=True, use_reloader=True, port=5000)