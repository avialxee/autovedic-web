from flask.helpers import url_for
import pandas as pd
import json


class VehicleModels:
    def __init__(self):
        """
        returns model of the brand.
        """
        # --- inputs ----        
        

        # --- internal ---
        self.info, self.msg = [], "failed!"

    def car_table(self):
        url_db = 'home/'+url_for('site.static', filename='rootmedia/car-table.csv')
        df = pd.read_csv(url_db, index_col='Global-ID')
        df['Models'] = df['Model'] + ' - ' + df['Variant-desc']
        b = df[['Models', 'Company-Unique', 'Variant-desc', 'Model','Class-desc']]
        return b

    def throw_output(self):
        return self.msg, self.info

    def car_models(self, brand=None):
        b = self.car_table()
    
        if brand is not None:
            brand = brand.upper()
            b =b.loc[b['Company-Unique']==brand]
        a = b.to_json(orient='columns')
        return json.loads(a)
        
    def car_brands(self):
        b = self.car_table()
        res = b['Company-Unique'].unique().tolist()
        
        return json.dumps(res)
    
    def remove_details(self, rowno):
        url_db = 'home/'+url_for('site.static', filename='rootmedia/car-table.csv')
        df = pd.read_csv(url_db, index_col='Global-ID')
        rows =  [int(x) for x in list(rowno)]
        print(f'deleting : {rows}')
        print(df.columns)
        df.drop(rows, inplace=True)
        df.to_csv(url_db, index=True)
        return print(f'deleted : {rows}\n...........\n')
        
vm = VehicleModels()
def load_vehicles(brand=None):
    return vm.car_models(brand=brand)
    
def load_brands():
    return vm.car_brands()

def load_car_table():
    return vm.car_table()

def remove_car_details(rowno):
    return vm.remove_details(rowno)