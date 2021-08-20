import json
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import HTTPError
from requests_futures.sessions import FuturesSession

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
session = FuturesSession(executor=ThreadPoolExecutor(max_workers=10))
for system in range(first_system, last_system + 1):
    req = session.get('https://esi.evetech.net/latest/universe/systems/' + str(system) + '/?datasource=tranquility&language=en', headers=request_headers)
    reqs.append(req)
#print(reqs)
for response in reqs:
    data = response.result().text
    json_output = json.loads(data)
    relevant_info = {
        'system_id' : json_output['system_id'],
        'name' : json_output['name'],
        'stargates' : json_output['stargates']
    }

    f.write(str(relevant_info) + "\n")
