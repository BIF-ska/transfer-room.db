import requests
import json
from urllib.parse import urlencode
### authorize

email = 'dst@brondby.com'
password = 'BifAdmin1qazZAQ!TransferRoom'

base_url = "https://apiprod.transferroom.com/api/external/login"
params = {'email': email, 'password': password}
encoded_params = urlencode(params)
auth_url = f"{base_url}?{encoded_params}"

r = requests.post(auth_url)
token_json_data = r.json()
token = token_json_data['token']

 
headers = {"Authorization": "Bearer "+token}
 

### Get player data
request_url = 'https://apiprod.transferroom.com/api/external/players?position=0&amount=1000'
r = requests.get(request_url,headers=headers)
json_data = r.json()

### Get head coach data for Premier League - England 
request_url = 'https://apiprod.transferroom.com/api/external/coaches?position=0&amount=1000&competitionid = 757'
r = requests.get(request_url,headers=headers)
json_data = r.json()