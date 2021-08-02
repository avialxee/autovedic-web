from flask.helpers import url_for
import pandas as pd
import json


class MapModels:
    def __init__(self):
        """
        returns pincode and post office name.
        """
        # --- internal ---
        self.info, self.msg = [], "failed!"

    def map_table(self):
        url_db = 'home/'+url_for('site.static', filename='rootmedia/map-table.csv')
        df = pd.read_csv(url_db)
        b = df[['Pincode','Post office','g1','g2']]
        return b

    def throw_output(self):
        return self.msg, self.info

    def map_by_pincode(self, pincode=None):
        b = self.map_table()
        if pincode is not None:
            b =b.loc[b['Pincode']==int(pincode)]
        a = b.to_json(orient='columns')
        return json.loads(a)
        
    def map_pincodes(self):
        b = self.map_table()
        res = b['Pincode'].unique().tolist()        
        return json.dumps(res)
        
mm = MapModels()
def load_maps(pincode=None):
    return mm.map_by_pincode(pincode=pincode)
    
def load_pincodes():
    return mm.map_pincodes()