import re, json
from requests.exceptions import HTTPError, RequestException
from requests_futures.sessions import FuturesSession
from concurrent.futures import as_completed

session = FuturesSession(max_workers=200)

def get_neighbors_futures(all_systems, systems_and_neighbors):
    futures = []
    for system in all_systems:
        if 'stargates' in systems_and_neighbors[system]:
            for gate in systems_and_neighbors[system]['stargates']:
                future = session.get('https://esi.evetech.net/latest/universe/stargates/' + str(gate) + '/?datasource=tranquility')
                future.system_id = system
                future.gate = gate
                futures.append(future)
    return futures

def get_neighbors_results(futures, systems_and_neighbors, redo_systems, error_write):
    for response in as_completed(futures):
        result = response.result()
        try:
            result.raise_for_status()
            error_limit_remaining = result.headers['x-esi-error-limit-remain']
            if error_limit_remaining != "100":
                error_limit_time_to_reset = result.headers['x-esi-error-limit-reset']
                error_write.write('For {} the Error Limit Remaing: {} Limit-Rest {} \n\n'.format(result.url, error_limit_remaining, error_limit_time_to_reset))
        except HTTPError:
            error_write.write('Received status code {} from {} With headers:\n{}\n'.format(result.status_code, result.url, str(result.headers)))
            if 'x-esi-error-limit-remain' in result.headers:
                error_limit_remaining = result.headers['x-esi-error-limit-remain']
                error_limit_time_to_reset = result.headers['x-esi-error-limit-reset']
                error_write.write('Error Limit Remaing: {} Limit-Rest {} \n'.format(error_limit_remaining, error_limit_time_to_reset))
            error_write.write("\n")
            redo_systems.append(response.system_id)
            continue
        except RequestException as e: 
            error_write.write("other error is " + e + "\n")
            continue
        data = result.text
        json_output = json.loads(data)
        system_id = str(json_output['system_id'])
        destination_system_id = json_output['destination']['system_id']
        destination_name_regex = re.compile(r'\((.*)\)')
        destination_name = destination_name_regex.search(json_output['name']).group(1)
        destination_info = {
            'system_id': destination_system_id,
            'name': destination_name
        }
        if 'neighbors' not in systems_and_neighbors[system_id]:
            systems_and_neighbors[system_id]['neighbors'] = []
        systems_and_neighbors[system_id]['neighbors'].append(destination_info)
    return systems_and_neighbors, redo_systems

def get_systems_neighbors(all_systems, systems_and_neighbors, error_write):
    redo_systems = []
    futures = get_neighbors_futures(all_systems, systems_and_neighbors)
    systems_and_neighbors, redo_systems = get_neighbors_results(futures, systems_and_neighbors, redo_systems, error_write)
    if len(redo_systems) != 0:
        systems_and_neighbors = get_systems_neighbors(redo_systems, systems_and_neighbors, error_write)
    return systems_and_neighbors