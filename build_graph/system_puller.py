import os, re, requests, pickle

def get_systems():
    if os.path.isfile('./data/systems.p'):
        print('systems.p already exist')
        return pickle.load(open('./data/systems.p', 'rb'))
    systems = requests.get('https://esi.evetech.net/latest/universe/systems/?datasource=tranquility')
    answer = systems.text.replace("[", "").replace("]", "").split(",")
    regex = re.compile(r'^[3][0]')
    kspace_systems = [i for i in answer if regex.match(i)]
    pickle.dump(kspace_systems, open('./data/systems.p', 'wb'))
    return kspace_systems