import sys
import random
import matplotlib.pyplot as plt
import networkx as nx

class edge:
    def __init__(self, id: int, x: int, y: int):
        self.id = id
        self.x = x
        self.y = y

class node:
    def __init__(self, id: int, edges: list[int]):
        self.id = id
        self.edges = edges
        self.colors : list = []
        self.current_color = None
        self.fixed_color = False

nodes: dict[int, node] = dict()
edges: dict[int, edge] = dict()
max_degree: int = 0
colors: list = []

def getData(path: str):
    file = open(path, "r")
    lines = file.readlines()
    file.close()

    for line in lines:
        x = line.split()
        if x[0] == "v":
            createNode(x[1], [eval(i) for i in x[2:]])
        elif x[0] == "e":
            if len(x) != 4:
                print("invalid edge, check input data")
                exit()
            createEdge(x[1], x[2], x[3])

    global colors 
    for i in range(0, max_degree + 1):
        colors.append(i)
    return

def getNeighbors(node_id: int) -> list[node]:
    current = nodes[str(node_id)]
    neighbors = []
    for edge in current.edges:
        current_edge = str(edge)
        temp_x = edges[current_edge].x
        temp_y = edges[current_edge].y

        if int(temp_x) != int(node_id):
            neighbors.append(nodes[temp_x])
        else:
            neighbors.append(nodes[temp_y])

    return neighbors

def createEdge(id: int, x: int, y: int) -> edge:
    new_edge = edge(id, x, y)
    edges[id] = new_edge
    return new_edge

def createNode(id: int, edges: list[int]) -> node:
    global max_degree
    if len(edges) > max_degree:
        max_degree = len(edges)

    new_node = node(id, edges)
    nodes[id] = new_node
    return new_node

def pickRandColor():
    for node in nodes:
        current_node = nodes[str(node)]
        current_node.current_color = colors[random.randint(0, len(colors) - 1)]
    return

def checkNeighbors():
    all_independent = True
    for node in nodes:
        independent = True
        current_node = nodes[str(node)]
        available_colors = colors.copy()
        if current_node.fixed_color == True:
            continue
        neighbors = getNeighbors(current_node.id)
        for neighbor in neighbors:
            if neighbor.current_color in available_colors:
                available_colors.remove(neighbor.current_color)
            if neighbor.current_color == current_node.current_color:
                independent = False
                all_independent = False
        if independent:
            current_node.fixed_color = True
        current_node.colors = available_colors

    return all_independent

def changeColor():
    for node in nodes:
        current_node = nodes[str(node)]
        if current_node.fixed_color == True:
            continue
        
        current_node = nodes[str(node)]
        current_node.current_color = current_node.colors[random.randint(0, len(current_node.colors)) - 1]
    return

def printResult():
    edges_list = []
    for edge in edges:
        current_edge = edges[str(edge)]
        edges_list.append((int(current_edge.x), int(current_edge.y)))

    node_list = []
    node_color_list = []
    node_labels = {}
    for node in nodes:
        current_node = nodes[str(node)]
        node_list.append(int(current_node.id))
        node_color_list.append(current_node.current_color)
        node_labels[int(current_node.id)] = str(current_node.id)

    G = nx.Graph()
    G.add_nodes_from(node_list)
    G.add_edges_from(edges_list)

    options = {
    "font_size": 18,
    "node_size": 1400,
    "edgecolors": "black",
    "linewidths": 3,
    "width": 2,
    "font_color": "white",
}
    nx.draw(G, node_color=node_color_list, with_labels=True, **options)
    plt.axis("off")
    plt.show()

    return

def main():
    if len(sys.argv) < 2:
        print("Missing input file, usage: python3 algo.py <path to data.txt>")
        return

    # import data
    getData(sys.argv[1])
    # first iteration assign random colors to nodes independend of each other
    iterations = 0
    pickRandColor()

    while True:
        if checkNeighbors():
            break
        changeColor()
        iterations += 1
        

    print("iterations: " + str(iterations))
    print("highest Degree: " + str(max_degree))
    print("colours: " + str(colors))
    print("----------")

    for node in nodes:
        print("node "+ str(nodes[str(node)].id)+ ": color " + str(nodes[str(node)].current_color))

    printResult()

    return

if __name__ == "__main__":
    main()