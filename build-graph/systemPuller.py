import os
import re
import requests
import pickle

def getSystems():
    if os.path.isfile('systems.p'):
        print('systems.p already exist')
        return pickle.load(open('systems.p', 'rb'))
    systems = requests.get('https://esi.evetech.net/latest/universe/systems/?datasource=tranquility')
    answer = systems.text.replace("[", "").replace("]", "").split(",")
    regex = re.compile(r'^[3][0]')
    filtered_answer = [i for i in answer if regex.match(i)]
    pickle.dump(filtered_answer, open('systems.p', 'wb'))
    return filtered_answer