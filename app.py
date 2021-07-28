import os
from flask import Blueprint
from flask_login import LoginManager
from flask import Flask, redirect, url_for, render_template, request, jsonify
from api.routes import api
from home.routes import site
from classes.login import User
def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(12)
    
    app.register_blueprint(api)
    app.register_blueprint(site)
    return app
#app.register_blueprint(site)

app = create_app()
login_manager = LoginManager(app)
login_manager.init_app(site)
login_manager.login_view = "site.login"
@login_manager.user_loader
def load_user(user_id):
    return User(id=user_id)
# ======== Main ============================================================== #
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, port=5000)