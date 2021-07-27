from flask import Blueprint, render_template
from flask import Flask, redirect, url_for, render_template, request, jsonify
from home.forms import SearchForm
from api.routes import models # from classes.search import model_search

site = Blueprint('site', __name__, template_folder='site-templates', static_folder='site-static')

@site.context_processor
def search_context():
    def model_brand(brand):
        return models(brand)
    return dict(model_brand=model_brand)

@site.route('/', methods=['GET'])
def index():
    #return 'welcome to homepage.'
    sfield = SearchForm(request.form)
    return render_template('home.html', content=sfield)
