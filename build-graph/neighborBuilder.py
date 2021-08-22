from os import system
import re
from systemPuller import getSystems
import pickle
import json
from requests.exceptions import HTTPError, RequestException
from requests_futures.sessions import FuturesSession
from concurrent.futures import as_completed

all_systems = getSystems()
systemsAndGates = pickle.load(open('stargate.p', "rb"))
systemsAndNeighbors = systemsAndGates
error_write = open("output_neighbor.txt","w+")

session = FuturesSession(max_workers=200)

# systemStargateCreator should pull in all 5413 k-space systems
def getSystemsNeighbors(all_systems, systemsAndNeighbors, error_write):
    redo_systems = []
    futures = getNeighborsFutures(all_systems)
    systemsAndNeighbors, redo_systems = getNeighborsResults(futures, systemsAndNeighbors, redo_systems, error_write)
    print(redo_systems)
    if len(redo_systems) != 0:
        systemsAndNeighbors = getSystemsNeighbors(redo_systems, systemsAndNeighbors, error_write)
    return systemsAndNeighbors

def getNeighborsFutures(all_systems):
    futures = []
    for system in all_systems:
        if 'stargates' in systemsAndNeighbors[system]:
            for gate in systemsAndNeighbors[system]['stargates']:
                future = session.get('https://esi.evetech.net/latest/universe/stargates/' + str(gate) + '/?datasource=tranquility')
                future.system_id = system
                future.gate = gate
                futures.append(future)
    return futures

def getNeighborsResults(futures, systemsAndNeighbors, redo_systems, error_write):
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
        systemID = str(json_output['system_id'])
        destinationSystemID = json_output['destination']['system_id']
        destinationNameRegex = re.compile(r'\((.*)\)')
        destinationName = destinationNameRegex.search(json_output['name']).group(1)
        destinationInfo = {
            'system_id': destinationSystemID,
            'name': destinationName
        }
        if 'neighbors' not in systemsAndNeighbors[systemID]:
            systemsAndNeighbors[systemID]['neighbors'] = []
        systemsAndNeighbors[systemID]['neighbors'].append(destinationInfo)
    return systemsAndNeighbors, redo_systems


neighborSystem_dict = getSystemsNeighbors(all_systems, systemsAndNeighbors, error_write)

#print(neighborSystem_dict)
print(len(neighborSystem_dict))

pickle.dump(neighborSystem_dict, open('neighbor.p', "wb"))