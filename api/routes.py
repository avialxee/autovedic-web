from flask import Blueprint

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/', methods=['GET', 'POST'])
def index():
    return {"hello":"world"}

# ------------ TODO: use classes --------- #

def models(brand):
    if brand == 'Maruti':
        return {1: 'Alto200', 2: 'Alto800'}

@api.route('cars/<brand>', methods=['GET'])
def show_model(brand):
    if brand == 'Maruti':
            return models(brand), 200
    else:
        return {'error': 'vehicle not found'}, 404
