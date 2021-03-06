from flask import Blueprint
api = Blueprint('api', __name__, url_prefix='/api')
from classes.vehicles import load_vehicles, load_brands
from classes.maps import load_maps, load_pincodes
from classes.services import load_services, load_stype_id, load_services_byid
from classes.dtext import chooseus_textbysno

@api.route('/', methods=['GET', 'POST'])
def index():
    return {"hello":"world"}

# ------------ cars --------- #
@api.route('/cars', methods=['GET'])
def show_model():
    return load_vehicles(brand=None), 200

@api.route('/cars/id/<gid>', methods=['GET'])
def cars_by_id(gid):
    res1 = load_vehicles()['Company-Unique'][str(gid)]
    res2 = str(load_vehicles()['Models'][str(gid)])
    return {res1:res2}, 200

@api.route('/cars/<brand>', methods=['GET'])
def cars_by_brand(brand):
    return load_vehicles(brand=str(brand)), 200

@api.route('/cars/brands', methods=['GET'])
def cars_load_brands():
    return load_brands(), 200

# ------------ maps --------- #
@api.route('/maps', methods=['GET'])
def show_maps():
    return load_maps(), 200   

@api.route('/maps/<pincode>', methods=['GET'])
def maps_by_pincodes(pincode):
    return load_maps(pincode=pincode), 200    

@api.route('/maps/pincodes', methods=['GET'])
def maps_load_pincodes():
    return load_pincodes(), 200


# ------------ services --------- #
@api.route('/services/id/<stype_id>', methods=['GET'])
def services_by_id(stype_id):
    return load_services_byid(stype_id=stype_id), 200    

@api.route('/services/', methods=['GET'])
def services_load_allservices():
    return load_services(), 200

@api.route('/services/id', methods=['GET'])
def services_load_id():
    return load_stype_id(), 200

# ------------ vendors --------- #
#@api.route('/vendors', methods=['GET'])
#def show_vendors():
#    return load_vendors(), 200   
#
#@api.route('/vendors/<pincode>', methods=['GET'])
#def show_by_pincodes(pincode):
#    return load_vendors(pincode=pincode), 200    
#
#@api.route('/vendors/pincodes', methods=['GET'])
#def show_pincodes():
#    return load_pincodes(), 200

# ------------ dynamic texts ----#
@api.route('/dtext/chooseus/<sno>', methods=['GET'])
def chooseus_by_sno(sno):
    return chooseus_textbysno(sno), 200   