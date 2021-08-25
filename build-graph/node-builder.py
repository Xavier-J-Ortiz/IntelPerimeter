import pickle
import os
from stargateBuilder import getSystemStargates
from neighborBuilder import getSystemsNeighbors
from systemPuller import getSystems

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

all_systems = getSystems()
error_write_neighbor = open("output_neighbor.txt","w+")
error_write_stargate = open("output_stargate.txt","w+")
systemsAndGates = {}
systemsAndGates = getSystemStargates(all_systems, systemsAndGates, error_write_stargate)
systemsAndNeighbors = getSystemsNeighbors(all_systems, systemsAndGates, error_write_neighbor)
nodes = getNodeNames(all_systems, systemsAndNeighbors)
#print(nodes)