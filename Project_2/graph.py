class Nodes:
    def __init__ (self, node_id, color):
        self.index = node_id
        self.neighbors = []
        self.domain = []
        for i in range(color):
            self.domain.append(i)

    def add_neighbor(self, neighbor_node):
        self.neighbors.append(neighbor_node)

