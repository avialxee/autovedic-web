from flask import Blueprint
api = Blueprint('api', __name__, url_prefix='/api')
from classes.vehicles import load_vehicles, load_brands

@api.route('/', methods=['GET', 'POST'])
def index():
    return {"hello":"world"}

# ------------ TODO: use classes --------- #

@api.route('/cars', methods=['GET'])
def show_model():
    return load_vehicles(brand=None), 200

@api.route('/cars/id/<gid>', methods=['GET'])
def show_car_details(gid):
    res1 = load_vehicles()['Company-Unique'][str(gid)]
    res2 = str(load_vehicles()['Models'][str(gid)])
    return {res1:res2}, 200

@api.route('/cars/<brand>', methods=['GET'])
def show_by_brand(brand):
    return load_vehicles(brand=str(brand)), 200

@api.route('/cars/brands', methods=['GET'])
def show_brands():
    return load_brands(), 200