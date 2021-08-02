import os
from flask_login import LoginManager
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(12)
    
    login_manager = LoginManager(app)
    
    from classes.registration import User
    @login_manager.user_loader
    def load_user(userid):
        return User.query.get(int(userid))
    
    from api.routes import api
    app.register_blueprint(api)

    from home.routes import site
    app.register_blueprint(site)
    login_manager.init_app(site)
    login_manager.login_view = "site.login"
    
    from classes import classdef
    app.register_blueprint(classdef)

    from classes.database import db_session
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()
    return app
#app.register_blueprint(site)

app = create_app()
app.url_map.strict_slashes = False

# ======== Main ============================================================== #
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, port=5000)