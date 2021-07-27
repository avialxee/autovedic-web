from classes.vehicles import VehicleModels

vm = VehicleModels('all', 'all')
def load_vehicles():
    model_company = vm.vehicle_model()
    return model_company