import json
from systemPuller import getSystems
from concurrent.futures import ThreadPoolExecutor
import time
from requests.exceptions import HTTPError, RequestException
from requests_futures.sessions import FuturesSession
from concurrent.futures import as_completed

all_systems = getSystems()

f= open("test.txt","w+")
g= open("output.txt","w+")

futures = []
session = FuturesSession()

for system in all_systems:
    future = session.get('https://esi.evetech.net/latest/universe/systems/' + system + '/?datasource=tranquility&language=en')
    futures.append(future)
redo_systems = []
for response in as_completed(futures):
    result = response.result()
    try:
        result.raise_for_status()
        ELimitRemaining = result.headers['x-esi-error-limit-remain']
        ELimitTimeToReset = result.headers['x-esi-error-limit-reset']
        g.write('Limit-Remain: {} Limit-Rest {} \n'.format(ELimitRemaining, ELimitTimeToReset))
    except HTTPError:
        g.write('Received status code {} from {} \n'.format(result.status_code, result.url))
        g.write(str(result.headers) + '\n')
        if 'x-esi-error-limit-remain' in result.headers:
            ELimitRemaining = result.headers['x-esi-error-limit-remain']
            ELimitTimeToReset = result.headers['x-esi-error-limit-reset']
        #g.write("\nsleep starting in httpError\n")
        #time.sleep(int(60))
        #g.write("\nsleep ending in httpError\n")
        continue
    except RequestException as e: 
        g.write("other error is " + e + "\n")
        #g.write("\nsleep starting in other exc\n")
        #time.sleep(int(60))
        #g.write("\nsleep ending in other exc\n")
        continue
    data = result.text
    json_output = json.loads(data)
    if 'stargates' in json_output:
        relevant_info = {
            'system_id' : json_output['system_id'],
            'name' : json_output['name'],
            'stargates' : json_output['stargates']
            }
    else:
        relevant_info = {
            'system_id' : json_output['system_id'],
            'name' : json_output['name'],
            }
    f.write(str(relevant_info) + "\n")