from flask import Blueprint, render_template
from flask import Flask, flash, redirect, url_for, render_template, request, jsonify
from home.forms import SearchForm
from api.routes import show_model # from classes.search import model_search
from classes.vehicles.vehicle import load_vehicles

site = Blueprint('site', __name__, template_folder='site-templates', static_folder='site-static')

@site.context_processor
def search_context():
    def model_brand():
        val, http = show_model()
        return val['Models']
    return dict(model_brand=model_brand)

@site.route('/', methods=['GET', 'POST'])
def index():
    sfield = SearchForm(request.form)
    if request.method == 'POST':
        flash('selected {}'.format(request.form['model_brand']))
    return render_template('home.html', content=sfield)

@site.route('/vendors', methods=['POST'])
def search_vendor():
    return render_template('home.html')