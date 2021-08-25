import pickle


def createPerimeter(systemName, node_graph, jumps =5):
    Perimeter = {systemName: 0}
    neighbors = node_graph[systemName]['neighbors']
    Perimeter = delimitPerimeter(Perimeter, neighbors, node_graph, jumps)
    return Perimeter

def delimitPerimeter(Perimeter, neighbors, node_graph, jumps):
    for distance in range(1, jumps + 1):
        new_neighbors = []
        for neighbor in neighbors:
            if neighbor not in Perimeter:
                Perimeter[neighbor] = distance
                new_neighbors += node_graph[neighbor]['neighbors']
        neighbors = new_neighbors
    pickle.dump(Perimeter, open('perimeter.p', 'wb'))
    return Perimeter

node_graph = pickle.load(open('nodes.p', 'rb'))
perimeter_dict = createPerimeter('K-6K16', node_graph, 3)
print(perimeter_dict)
#pickle.dump(perimeter_dict, open('perimeter.p', 'wb'))