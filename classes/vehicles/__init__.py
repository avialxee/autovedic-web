from .read_database import read_db

class VehicleModels:
    def __init__(self, vtype, brand):
        """
        returns model of the brand.
        """
        # --- inputs ----
        self.vtype, self.brand = str(vtype), str(brand)

        # --- internal ---
        self.info, self.msg = [], "failed!"

    def throw_output(self):
        return self.msg, self.info

    def vehicle_model(self):
        a = read_db()
        return a