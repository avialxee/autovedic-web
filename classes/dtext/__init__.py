from calendar import c
from flask.helpers import url_for
import pandas as pd
import json


class ChooseUs:
    def __init__(self):
        """
        returns service type and service gid.
        """
        # --- internal ---
        self.info, self.msg = [], "failed!"

    def chooseus_table(self):
        url_db = 'home/'+url_for('site.static', filename='rootmedia/choose-us.csv')
        df = pd.read_csv(url_db)
        b = df[['Sno','Text']]
        return b

    def throw_output(self):
        return self.msg, self.info

    def text_by_sno(self, sno=None):
        b = self.chooseus_table()
        if sno is not None:
            b =b.loc[b['Sno']==int(sno)]
        a = b.to_json(orient='columns')
        return json.loads(a)
    def text_loadall(self):
        b = self.chooseus_table()
        a = b.to_json(orient='columns')
        return json.loads(a)

cutxt = ChooseUs()
def chooseus_textbysno(sno):
    if int(sno):
        return cutxt.text_by_sno(sno)
    else:
        return cutxt.text_loadall()

