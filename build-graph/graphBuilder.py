import requests
import json
first_system = 30000001
last_system = 30000009
#last_system = 30045354

for system in range(first_system, last_system + 1):
    response = requests.get('https://esi.evetech.net/latest/universe/systems/' + str(system) + '/?datasource=tranquility&language=en')
    data = response.text
    json_output = json.loads(data)
    relevant_info = {
        'system_id' : system,
        'name' : json_output['name'],
        'stargates' : json_output['stargates']
    }
    #print('----XOXOX----\n' + json_output)
    print(relevant_info)


