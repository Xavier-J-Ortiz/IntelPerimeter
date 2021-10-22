import pickle, os

def get_node_names(all_systems, systemsAndNeighbors):
    if os.path.isfile('./data/nodes.p'):
        print('nodes.p already exists')
        return pickle.load(open('./data/nodes.p', "rb"))
    universe_node_graph = {}
    for system in all_systems:
        systemName = systemsAndNeighbors[system]['name']
        if 'neighbors' in systemsAndNeighbors[system]:
            neighborNames = [neighbor['name'] for neighbor in systemsAndNeighbors[system]['neighbors']]
            universe_node_graph[systemName] = {'neighbors': neighborNames}
        else:
            universe_node_graph[systemName] = {'neighbors': None}
    pickle.dump(universe_node_graph, open('./data/nodes.p', "wb"))
    return universe_node_graph

#print(nodes)