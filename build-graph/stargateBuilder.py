import json
import pickle
import os
from systemPuller import getSystems
from requests.exceptions import HTTPError, RequestException
from requests_futures.sessions import FuturesSession
from concurrent.futures import as_completed

#all_systems = getSystems()
#error_write = open("output_stargate.txt","w+")
#systemsAndGates = {}

session = FuturesSession(max_workers=200)

def getStargatesFutures(all_systems):
    futures = []
    for system in all_systems:
        future = session.get('https://esi.evetech.net/latest/universe/systems/' + system + '/?datasource=tranquility&language=en')
        future.system_id = system
        futures.append(future)   
    return futures

def getStargateResults(futures, systemsAndGates, redo_systems, error_write):
    for response in as_completed(futures):
        result = response.result()
        try:
            result.raise_for_status()
            ELimitRemaining = result.headers['x-esi-error-limit-remain']
            if ELimitRemaining != "100":
                ELimitTimeToReset = result.headers['x-esi-error-limit-reset']
                error_write.write('For {} the Error Limit Remaing: {} Limit-Rest {} \n\n'.format(result.url, ELimitRemaining, ELimitTimeToReset))
        except HTTPError:
            error_write.write('Received status code {} from {} With headers:\n{}\n'.format(result.status_code, result.url, str(result.headers)))
            if 'x-esi-error-limit-remain' in result.headers:
                ELimitRemaining = result.headers['x-esi-error-limit-remain']
                ELimitTimeToReset = result.headers['x-esi-error-limit-reset']
                error_write.write('Error Limit Remaing: {} Limit-Rest {} \n'.format(ELimitRemaining, ELimitTimeToReset))
            error_write.write("\n")
            redo_systems.append(response.system_id)
            continue
        except RequestException as e: 
            error_write.write("other error is " + e + "\n")
            continue
        data = result.text

        json_output = json.loads(data)
        if 'stargates' in json_output:
            relevant_info = {
                #'system_id' : json_output['system_id'],
                'name' : json_output['name'],
                'stargates' : json_output['stargates']
                }
        else:
            relevant_info = {
                #'system_id' : json_output['system_id'],
                'name' : json_output['name'],
                }
        systemsAndGates[response.system_id] = relevant_info
    return systemsAndGates, redo_systems

def getSystemStargates(all_systems, systemsAndGates, error_write):
    if os.path.isfile('stargate.p'):
        print('stargates.p already exists')
        return pickle.load(open('stargate.p', "rb"))
    redo_systems = []
    futures = getStargatesFutures(all_systems)
    systemsAndGates, redo_systems = getStargateResults(futures, systemsAndGates, redo_systems, error_write)
    if len(redo_systems) != 0:
        systemsAndGates = getSystemStargates(redo_systems, systemsAndGates, error_write)
    pickle.dump(systemsAndGates, open('stargate.p', "wb"))
    return systemsAndGates
#solarSystem_dict = getSystemStargates(all_systems, systemsAndGates, error_write)
#print(len(solarSystem_dict))
#pickle.dump(solarSystem_dict, open('stargate.p', "wb"))