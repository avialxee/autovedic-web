from flask.helpers import url_for
import pandas as pd
import json


class ContactDetails:
    def __init__(self):
        """
        returns service type and service gid.
        """
        # --- internal ---
        self.info, self.msg = [], "failed!"
        # df_form = pd.DataFrame(columns=['brand','model','fullname','email','phone','time','ip'])
        # df_form.to_csv(url_db,mode='a', index=False, header=False)


    def contact_details_table(self):
        url_db ='home/'+url_for('site.static', filename='rootmedia/contact-details.csv')
    
        df = pd.read_csv(url_db)
        b = df[['brand','model','fullname','email','phone']]
        return b

    def throw_output(self):
        return self.msg, self.info

    def record_details(self,formd):
        url_db ='home/'+url_for('site.static', filename='rootmedia/contact-details.csv')

        brand=formd['brand']
        model=formd['model']
        fullname=formd['fullname']
        email=formd['email']
        phone=formd['phone']
        time=formd['time']
        ip=formd['ip']
        df_form = pd.DataFrame([[brand,model,fullname,email,phone,time,ip]] , columns=['brand','model','fullname','email','phone','time','ip'])
        df_form.to_csv(url_db,mode='a', index=False, header=False, index_label='#')
        return df_form
    def read_details(self):
        url_db = 'home/'+url_for('site.static', filename='rootmedia/contact-details.csv')
        
        columns=['#','brand','model','fullname','email','phone','time','ip']
        df = pd.read_csv(url_db)
        b=df
        return b

    def remove_details(self, rowno):
        url_db = 'home/'+url_for('site.static', filename='rootmedia/contact-details.csv')
        df = pd.read_csv(url_db)
        rows =  [int(x) for x in list(rowno)]
        print(f'deleting : {rows}')
        
        df.drop(rows, inplace=True)
        df.to_csv(url_db,index=False)
        return print(f'deleted : {rows}\n...........\n')
        
cd = ContactDetails()
def record_contact_details(formd):
    return cd.record_details(formd)
def read_contact_details():
    return cd.read_details()
def remove_contact_details(rowno):
    return cd.remove_details(rowno)