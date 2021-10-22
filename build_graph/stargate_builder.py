import json, pickle, os
from requests.exceptions import HTTPError, RequestException
from requests_futures.sessions import FuturesSession
from concurrent.futures import as_completed

session = FuturesSession(max_workers=200)

def get_stargates_futures(all_systems):
    futures = []
    for system in all_systems:
        future = session.get('https://esi.evetech.net/latest/universe/systems/' + system + '/?datasource=tranquility&language=en')
        future.system_id = system
        futures.append(future)   
    return futures

def get_stargate_results(futures, systems_and_gates, redo_systems, error_write):
    for response in as_completed(futures):
        result = response.result()
        try:
            result.raise_for_status()
            error_limit_remaining = result.headers['x-esi-error-limit-remain']
            if error_limit_remaining != "100":
                error_limit_time_to_reset = result.headers['x-esi-error-limit-reset']
                error_write.write('INFORMATIONAL: Though no error, for {} the Error Limit Remaning: {} Limit-Rest {} \n\n'.format(result.url, error_limit_remaining, error_limit_time_to_reset))
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
        if 'stargates' in json_output:
            relevant_info = {
                'name' : json_output['name'],
                'stargates' : json_output['stargates']
                }
        else:
            relevant_info = {
                'name' : json_output['name'],
                }
        systems_and_gates[response.system_id] = relevant_info
    return systems_and_gates, redo_systems

def get_system_stargates(all_systems, systems_and_gates, error_write):
    if os.path.isfile('./data/stargate.p'):
        print('stargates.p already exists')
        return pickle.load(open('./data/stargate.p', "rb"))
    redo_systems = []
    futures = get_stargates_futures(all_systems)
    systems_and_gates, redo_systems = get_stargate_results(futures, systems_and_gates, redo_systems, error_write)
    if len(redo_systems) != 0:
        systems_and_gates = get_system_stargates(redo_systems, systems_and_gates, error_write)
    print("systems and their gates information loaded from scratch")
    pickle.dump(systems_and_gates, open('./data/stargate.p', "wb"))
    return systems_and_gates