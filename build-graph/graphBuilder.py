import json
from systemPuller import getSystems
from requests.exceptions import HTTPError, RequestException
from requests_futures.sessions import FuturesSession
from concurrent.futures import as_completed


all_systems = getSystems()

f = open("test.txt","w+")
g = open("output.txt","w+")

session = FuturesSession(max_workers=200)

# systemStargateCreator should pull in all 5413 k-space systems
def systemStargateCreator(all_systems, f, g):
    futures = []
    redo_systems = []
    for system in all_systems:
        future = session.get('https://esi.evetech.net/latest/universe/systems/' + system + '/?datasource=tranquility&language=en')
        future.system_id = system
        futures.append(future)
    for response in as_completed(futures):
        result = response.result()
        try:
            result.raise_for_status()
            ELimitRemaining = result.headers['x-esi-error-limit-remain']
            if ELimitRemaining != "100":
                ELimitTimeToReset = result.headers['x-esi-error-limit-reset']
                g.write('For {} the Error Limit Remaing: {} Limit-Rest {} \n\n'.format(result.url, ELimitRemaining, ELimitTimeToReset))
        except HTTPError:
            g.write('Received status code {} from {} With headers:\n{}\n'.format(result.status_code, result.url, str(result.headers)))
            if 'x-esi-error-limit-remain' in result.headers:
                ELimitRemaining = result.headers['x-esi-error-limit-remain']
                ELimitTimeToReset = result.headers['x-esi-error-limit-reset']
                g.write('Error Limit Remaing: {} Limit-Rest {} \n'.format(ELimitRemaining, ELimitTimeToReset))
            g.write("\n")
            redo_systems.append(response.system_id)
            continue
        except RequestException as e: 
            g.write("other error is " + e + "\n")
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
    if len(redo_systems) != 0:
        systemStargateCreator(redo_systems, f, g)

systemStargateCreator(all_systems, f, g)
