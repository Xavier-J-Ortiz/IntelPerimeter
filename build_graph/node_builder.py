import pickle, os
from stargate_builder import get_system_stargates
from neighbor_builder import get_systems_neighbors
from system_puller import get_systems

def getNodeNames(all_systems, systemsAndNeighbors):
    if os.path.isfile('nodes.p'):
        print('nodes.p already exists')
        return pickle.load(open('nodes.p', "rb"))
    universe_node_graph = {}
    for system in all_systems:
        systemName = systemsAndNeighbors[system]['name']
        if 'neighbors' in systemsAndNeighbors[system]:
            neighborNames = [neighbor['name'] for neighbor in systemsAndNeighbors[system]['neighbors']]
            universe_node_graph[systemName] = {'neighbors': neighborNames}
        else:
            universe_node_graph[systemName] = {'neighbors': None}
    pickle.dump(universe_node_graph, open('nodes.p', "wb"))
    return universe_node_graph

all_systems = get_systems()
error_write_neighbor = open("output_neighbor.txt","w+")
error_write_stargate = open("output_stargate.txt","w+")
systemsAndGates = {}
systemsAndGates = get_system_stargates(all_systems, systemsAndGates, error_write_stargate)
systemsAndNeighbors = get_systems_neighbors(all_systems, systemsAndGates, error_write_neighbor)
nodes = getNodeNames(all_systems, systemsAndNeighbors)
#print(nodes)