from flask import Blueprint
from flask import Flask, redirect, url_for, render_template, request, jsonify
from api.routes import api
from home.routes import site

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api)
    app.register_blueprint(site)
    return app
#app.register_blueprint(site)

app = create_app()
# ======== Main ============================================================== #
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, port=5000)