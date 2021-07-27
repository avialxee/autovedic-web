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

        def search_model(self):
            if self.vtype == 'car':
                if self.brand == 'Maruti':
                    self.info = 200
                    model = ['Alto200']
                    self.msg.append({1:model})
                    
            else :
                self.info = 204
                self.msg.append({'error':'data not found'})

            return throw_output(self)