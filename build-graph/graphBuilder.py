import json
from systemPuller import getSystems
from concurrent.futures import ThreadPoolExecutor
import time
from requests.exceptions import HTTPError, RequestException
from requests_futures.sessions import FuturesSession
from concurrent.futures import as_completed

all_systems = getSystems()

#first_system = 30000001
#last_system = 30005354
#last_system = 30005252
#system_segment_ends=[]
#chunk = 100
#amount_of_systems = last_system - first_system + 1
#segments = int(amount_of_systems / chunk)
#remainder = amount_of_systems % chunk
#first_segment = first_system
request_headers = {
    "accept": "application/json",
    "Accept-Language": "en",
    "Cache-Control": "no-cache"
}
'''
if segments >= 1:
    for section in range(1, segments + 1):
        last_segment =  first_segment + chunk
        system_segment_ends.append(last_segment)
        first_segment = last_segment
if remainder != 0:
    last_segment =  first_segment + remainder
    system_segment_ends.append(last_segment)
    first_segment = last_segment
print(system_segment_ends)
'''

f= open("test.txt","w+")
g= open("output.txt","w+")
futures = []
session = FuturesSession()
for system in all_systems:
    future = session.get('https://esi.evetech.net/latest/universe/systems/' + system + '/?datasource=tranquility&language=en', headers=request_headers)
    futures.append(future)
#for response in as_completed(futures):
for response in futures:
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
    f.write(str(relevant_info) + "\n")