import random
from graph import create_graph, dijkstra, a_star
from count_time import timeit

if __name__ == '__main__':
    # read graph file and create the graph
    data_dir = "./input/"
    graph = create_graph(data_dir)

    # get the start and end points
    start, end = random.sample(graph.nodes, 2)

    path_1 = dijkstra(start, end, graph)
    print(f"Shortest path from {start} to {end}:", path_1)
    print(" ")
    path_2 = a_star(start, end, graph)
    print(f"Shortest path from {start} to {end}:", path_2)

