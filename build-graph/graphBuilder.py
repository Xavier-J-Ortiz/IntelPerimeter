import grequests
import json
from requests.exceptions import HTTPError

first_system = 30000001
last_system = 30000326
system_segments=[]
amount_of_systems = last_system - first_system + 1
request_headers = {
    "accept": "application/json",
    "Accept-Language": "en",
    "Cache-Control": "no-cache"
}

f= open("test.txt","w+")
reqs = []
for system in range(first_system, last_system + 1):
    req = grequests.get('https://esi.evetech.net/latest/universe/systems/' + str(system) + '/?datasource=tranquility&language=en', headers=request_headers)
    reqs.append(req)
print(len(reqs))
responses = grequests.map(reqs, size=30)
for response in responses:
    try:
        response.raise_for_status()
    except HTTPError:
        print('Received status code {} from {}'.format(response.status_code, response.url))
        continue
    data = response.text
    json_output = json.loads(data)
    relevant_info = {
        'system_id' : json_output['system_id'],
        'name' : json_output['name'],
        'stargates' : json_output['stargates']
    }
    f.write(str(relevant_info) + "\n")
