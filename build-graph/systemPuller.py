
import requests
def getSystems():
    systems = requests.get('https://esi.evetech.net/latest/universe/systems/?datasource=tranquility')
    answer = systems.text.replace("[", "").replace("]", "").split(",")
    return answer
