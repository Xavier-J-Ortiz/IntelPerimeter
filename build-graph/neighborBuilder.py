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
g = open("output_neighbor.txt","w+")

session = FuturesSession(max_workers=200)

# systemStargateCreator should pull in all 5413 k-space systems
def getSystemsNeighbors(all_systems, systemsAndNeighbors, g):
    redo_systems = []
    futures = getNeighborsFutures(all_systems)
    systemsAndNeighbors, redo_systems = getNeighborsResults(futures, systemsAndNeighbors, redo_systems, g)
    print(redo_systems)
    if len(redo_systems) != 0:
        systemsAndNeighbors = getSystemsNeighbors(redo_systems, systemsAndNeighbors, g)
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

def getNeighborsResults(futures, systemsAndNeighbors, redo_systems, g):
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


neighborSystem_dict = getSystemsNeighbors(all_systems, systemsAndNeighbors, g)

print(neighborSystem_dict)
print(len(neighborSystem_dict))

pickle.dump(neighborSystem_dict, open('neighbor.p', "wb"))