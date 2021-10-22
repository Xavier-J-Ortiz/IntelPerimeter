import pickle
from stargate_builder import get_system_stargates
from neighbor_builder import get_systems_neighbors
from system_puller import get_systems
from node_builder import get_node_names

def create_perimeter(systemName, node_graph, jumps =5):
    perimeter = {systemName: 0}
    neighbors = node_graph[systemName]['neighbors']
    perimeter = delimit_perimeter(perimeter, neighbors, node_graph, jumps)
    return perimeter

def delimit_perimeter(perimeter, neighbors, node_graph, jumps):
    for distance in range(1, jumps + 1):
        new_neighbors = []
        for neighbor in neighbors:
            if neighbor not in perimeter:
                perimeter[neighbor] = distance
                new_neighbors += node_graph[neighbor]['neighbors']
        neighbors = new_neighbors
    pickle.dump(perimeter, open('perimeter.p', 'wb'))
    return perimeter
   
all_systems = get_systems()
error_write_neighbor = open("output_neighbor.txt","w+")
error_write_stargate = open("output_stargate.txt","w+")
systemsAndGates = {}
systemsAndGates = get_system_stargates(all_systems, systemsAndGates, error_write_stargate)
systemsAndNeighbors = get_systems_neighbors(all_systems, systemsAndGates, error_write_neighbor)
nodes = get_node_names(all_systems, systemsAndNeighbors)
node_graph = pickle.load(open('nodes.p', 'rb'))
perimeter_dict = create_perimeter('K-6K16', node_graph, 3)
print(perimeter_dict)
