from os import system
import pickle
from systemPuller import getSystems

systemsAndNeighbors = pickle.load(open('neighbor.p', 'rb'))
all_systems = getSystems()

def systemAndNeighborNameBuilder(all_systems, systemsAndNeighbors):
    universe_node_graph = {}
    for system in all_systems:
        systemName = systemsAndNeighbors[system]['name']
        if 'neighbors' in systemsAndNeighbors[system]:
            neighborNames = [neighbor['name'] for neighbor in systemsAndNeighbors[system]['neighbors']]
            universe_node_graph[systemName] = {'neighbors': neighborNames}
        else:
            universe_node_graph[systemName] = {'neighbors': None}
    return universe_node_graph

answer = systemAndNeighborNameBuilder(all_systems, systemsAndNeighbors)
print(answer)
pickle.dump(answer, open('nodes.p', "wb"))
