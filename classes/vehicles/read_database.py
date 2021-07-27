from re import split
from flask.json import jsonify
import pandas as pd
import json

url_db = 'cardatabase.txt'
df = pd.read_csv(url_db, index_col='Global-ID')

def read_db():
    #url_db = url_for('', filename='cardatabase.txt')
    #print(url_db)
    b = df[['Model', 'Company-Unique']]    
    a = b.to_json(orient='columns')
    #a = json.dumps(parsed, indent=4)
    
    return json.loads(a)