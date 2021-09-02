import pickle

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

node_graph = pickle.load(open('nodes.p', 'rb'))
perimeter_dict = create_perimeter('K-6K16', node_graph, 3)
print(perimeter_dict)
#pickle.dump(perimeter_dict, open('perimeter.p', 'wb'))