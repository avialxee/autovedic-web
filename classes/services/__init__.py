from flask.helpers import url_for
import pandas as pd
import json


class ServiceModels:
    def __init__(self):
        """
        returns service type and service gid.
        """
        # --- internal ---
        self.info, self.msg = [], "failed!"

    def service_table(self):
        url_db = 'home/'+url_for('site.static', filename='rootmedia/service-table.csv')
        df = pd.read_csv(url_db)
        b = df[['Service','Service-name','Service-subtype','Service-sname','Service-desc','Service-gid']]
        return b

    def throw_output(self):
        return self.msg, self.info

    def service_by_stype_id(self, stype_id=None):
        b = self.service_table()
        if stype_id is not None:
            b =b.loc[b['Service']==int(stype_id)]
        a = b.to_json(orient='columns')
        return json.loads(a)
        
    def service_stype_id(self):
        b = self.service_table()
        res = b['Service'].unique().tolist()        
        return json.dumps(res)
    
    def service_sname(self):
        b = self.service_table()
        res = b['Service'].unique().tolist()
        res1 = b['Service-name'].unique().tolist()
        d = {header: res[i::len(res1)] for i,header in 
        enumerate(res1)}
        return json.dumps(d)
    
        
mm = ServiceModels()
def load_services():
    return mm.service_sname()

def load_services_byid(stype_id=None):
    return mm.service_by_stype_id(stype_id=stype_id)
    
def load_stype_id():
    return mm.service_stype_id()

def load_service_table():
    return mm.service_table()