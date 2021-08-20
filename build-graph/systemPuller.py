
import re
import requests
def getSystems():
    systems = requests.get('https://esi.evetech.net/latest/universe/systems/?datasource=tranquility')
    answer = systems.text.replace("[", "").replace("]", "").split(",")
    regex = re.compile(r'^[3][0]')
    filtered_answer = [i for i in answer if regex.match(i)]
    return filtered_answer
