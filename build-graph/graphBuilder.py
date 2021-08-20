import json
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import HTTPError
from requests_futures.sessions import FuturesSession

first_system = 30000001
last_system = 30045354
system_segments=[]
amount_of_systems = last_system - first_system + 1
request_headers = {
    "accept": "application/json",
    "Accept-Language": "en",
    "Cache-Control": "no-cache"
}

f= open("test.txt","w+")
reqs = []
session = FuturesSession(executor=ThreadPoolExecutor(max_workers=1000))
for system in range(first_system, last_system + 1):
    req = session.get('https://esi.evetech.net/latest/universe/systems/' + str(system) + '/?datasource=tranquility&language=en', headers=request_headers)
    reqs.append(req)
#print(reqs)
for response in reqs:
    result = response.result()
    try:
        result.raise_for_status()
    except HTTPError:
        print('Received status code {} from {}'.format(result.status_code, result.url))
        print('Limit-Remain: {} Limit-Rest {}'.format(result.headers['x-esi-error-limit-remain'], result.headers['x-esi-error-limit-reset'] ))
        continue
    except requests.exceptions.RequestException as e: 
        raise SystemExit(e)
        continue
    data = result.text
    json_output = json.loads(data)
    if 'stargates' in json_output:
        relevant_info = {
            'system_id' : json_output['system_id'],
            'name' : json_output['name'],
            'stargates' : json_output['stargates']
            }

    f.write(str(relevant_info) + "\n")
