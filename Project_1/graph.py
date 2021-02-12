from collections import namedtuple
from queue import PriorityQueue
from count_time import timeit


Node = namedtuple("Node", ["id", "square", "x", "y"])
Edge = namedtuple("Edge", ["from_", "to_", "dist"])

def parse_node(line):
    v, square = line.split(",")
    square = int(square)
    x, y = (square / 10) * 100, (square % 10) * 100
    return Node(int(v), square, x, y)

def parse_edge(line):
    from_vertex, to_vertex, distance = line.split(",")
    return Edge(int(from_vertex), int(to_vertex), float(distance))

def parse_path(start, end, shortest):
    if end not in shortest:
        return None
    path = []
    node = end
    while node != -1:
        dist, prev = shortest[node]
        path.append((node, dist))
        node = prev
    path.reverse()
    return path

def create_graph(data_dir):
    graph = Graph()
    with open(data_dir + "p1_graph.txt", "r") as g:
        for line in g:
            if line.startswith("#"):
                continue
            elif line.startswith("S"):
                continue
            elif line.startswith("D"):
                continue
            else:
                x = line.strip("\n").split(",")
                if len(x) == 2:
                    node = parse_node(line)
                    graph.add_node(node)
                elif len(x) == 3:
                    edge = parse_edge(line)
                    graph.add_edge(edge)
    return graph

@timeit
def dijkstra(start, end, graph):
    shortest = {}
    pq = PriorityQueue(len(graph.nodes) ** 2)
    pq.put((0.0, (start, -1)))
    i = 0
    while not pq.empty():
        dist, (node, lastNode) = pq.get()
        if node in shortest:
            continue
        shortest[node] = (dist, lastNode)
        if node == end:
            break
        for _, neighbour, d in graph.edges[node]:
            if neighbour in shortest:
                continue
            pq.put((dist + d, (neighbour, node)))
            i += 1
    print(f"dijkstra has iterated for {i} times")
    return parse_path(start, end, shortest)

@timeit
def a_star(start, end, graph):
    def heuristic(lhs, rhs): # use Manhattan Distance
        lhs = graph.get_node(lhs)
        rhs = graph.get_node(rhs)
        return abs(lhs.x - rhs.x) + abs(lhs.y - rhs.y)
    shortest = {}
    open_list = PriorityQueue(len(graph.nodes) ** 2)
    open_list.put((0.0, (start, -1, 0)))
    i = 0
    while not open_list.empty():
        f, (node, last_node, path_length) = open_list.get()
        if node in shortest and path_length >= shortest[node][0]:
            continue
        shortest[node] = (path_length, last_node)
        if node == end:
            break
        for _, neighbour, d in graph.edges[node]:
            if neighbour in shortest:
                continue
            g = path_length + d
            f = g + heuristic(neighbour, end)
            open_list.put((f, (neighbour, node, g)))
            i += 1
    print(f"a_star has iterated for {i} times")
    return parse_path(start, end, shortest)

class Graph:
    def __init__(self):
        self._nodes = {}
        self._edges = {}

    def get_node(self, node_id):
        return self._nodes[node_id]

    @property
    def nodes(self):
        return self._nodes.keys()

    @property
    def edges(self):
        return self._edges

    def add_node(self, node: Node):
        self._nodes[node.id] = node
        self._edges[node.id] = []

    def add_edge(self, edge: Edge):
        self._edges[edge.from_].append(edge)
        self._edges[edge.to_].append(Edge(edge.to_, edge.from_, edge.dist))