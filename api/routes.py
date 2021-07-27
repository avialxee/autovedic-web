from flask import Blueprint
from classes.vehicles.vehicle import load_vehicles
api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/', methods=['GET', 'POST'])
def index():
    return {"hello":"world"}

# ------------ TODO: use classes --------- #

def models(brand):
    if brand == 'Maruti':
        return load_vehicles()['Model']

@api.route('cars/<brand>', methods=['GET'])
def show_model(brand):
    if brand == 'Maruti':
            return models(brand), 200
    else:
        return {'error': 'vehicle not found'}, 404
