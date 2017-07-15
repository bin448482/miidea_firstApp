from requests import post, get
import json
url = "http://localhost:8000/encryption_key"
data = {'id':'1'}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
post(url, data=json.dumps(data), headers=headers).json()