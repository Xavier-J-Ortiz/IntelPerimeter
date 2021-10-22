import re, requests

def get_systems():
    systems = requests.get('https://esi.evetech.net/latest/universe/systems/?datasource=tranquility')
    answer = systems.text.replace("[", "").replace("]", "").split(",")
    regex = re.compile(r'^[3][0]')
    kspace_systems = [i for i in answer if regex.match(i)]
    return kspace_systems