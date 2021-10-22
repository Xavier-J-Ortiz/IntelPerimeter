import pickle, os
from build_graph.system_puller import get_systems
from build_graph.stargate_builder import get_system_stargates
from build_graph.neighbor_builder import get_systems_neighbors

def directory_check():
    if not os.path.isdir('./data/map'):
        os.makedirs('./data/map') 
        print("map directory created")
    if not os.path.isdir('./data/output'):
        os.makedirs('./data/output') 
        print("output directory created")

def build_graph():
    if os.path.isfile('./data/map/nodes.p'):
        print('nodes.p already exists')
        return pickle.load(open('./data/map/nodes.p', "rb"))
    else:
        all_systems = get_systems()
        directory_check()
        print("systems loaded from scratch")
        error_write_neighbor = open('./data/output/output_neighbor.txt','w+')
        error_write_stargate = open('./data/output/output_stargate.txt','w+')
        systemsAndGates = {}
        systemsAndGates = get_system_stargates(all_systems, systemsAndGates, error_write_stargate)
        print("systems and their gate information loaded from scratch")
        systemsAndNeighbors = get_systems_neighbors(all_systems, systemsAndGates, error_write_neighbor)
        print("systems and their neighbor information loaded from scratch")

    universe_node_graph = {}
    for system in all_systems:
        systemName = systemsAndNeighbors[system]['name']
        if 'neighbors' in systemsAndNeighbors[system]:
            neighborNames = [neighbor['name'] for neighbor in systemsAndNeighbors[system]['neighbors']]
            universe_node_graph[systemName] = {'neighbors': neighborNames}
        else:
            universe_node_graph[systemName] = {'neighbors': None}
    pickle.dump(universe_node_graph, open('./data/map/nodes.p', "wb"))
    print("node graph loaded from scratch")
    return universe_node_graph