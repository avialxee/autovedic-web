import pandas as pd
import json

url_db = 'cardatabase.txt'
df = pd.read_csv(url_db, index_col='Global-ID')

def read_db():
    df['Models'] = df['Model'] + ' - ' + df['Variant-desc']
    b = df[['Models', 'Company-Unique', 'Variant-desc', 'Model']]
    a = b.to_json(orient='columns')
    return json.loads(a)