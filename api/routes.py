from flask import Blueprint
from classes.vehicles.vehicle import load_vehicles
api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/', methods=['GET', 'POST'])
def index():
    return {"hello":"world"}

# ------------ TODO: use classes --------- #

@api.route('/cars', methods=['GET'])
def show_model():
    return load_vehicles(), 200

@api.route('/cars/<gid>', methods=['GET'])
def show_car_details(gid):
    res1 = load_vehicles()['Company-Unique'][str(gid)]
    res2 = str(load_vehicles()['Models'][str(gid)])
    return {res1:res2}, 200