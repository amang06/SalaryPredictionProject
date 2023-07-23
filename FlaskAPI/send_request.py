import requests
from data_in import data_in

url = 'http://127.0.0.1:5000/predict'
headers = {'Content-Type': 'application/json'}
data = {'input': data_in}

r = requests.get(url, json=data, headers=headers)
print(r.json())