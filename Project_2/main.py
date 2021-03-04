from csp import Constraint, CSP, backtracking_search
from graph import Graph
import operator

class GraphColoringConstraint(Constraint[int, int]):
    def __init__(self, vertex1: int, vertex2: int) -> None:
        super().__init__([vertex1, vertex2])
        self.vertex1: int = vertex1
        self.vertex2: int = vertex2
    def satisfied(self, assignment):
        # If either vertex is not in the assignment then it is not
        # yet possible for their colors to be conflicting
        if self.vertex1 not in assignment or self.vertex2 not in assignment:
            return True
        # check the color assigned to vertex2 is not the same as the color assigned to vertex2
        return assignment[self.vertex1] != assignment[self.vertex2]

def main():
    f = open("input/input90.txt","r")
    Lines = f.readlines()
    f.close()
    print("Reading file")
    graph, color = readFile(Lines)
    print("File reading complete! Start CSP graph coloring.")
    variables = graph.vertices()
    domains = {}
    for variable in variables:
        domains[variable] = [i for i in range(color)]
    csp = CSP(variables, domains)
    for constraint in graph.edges():
        (vertex1, vertex2) = tuple(constraint)
        csp.add_constraint(GraphColoringConstraint(vertex1, vertex2))
    assignment = {}
    solution = backtracking_search(csp, assignment, domains)
    if solution is None:
        print("No solution!")
    else:
        print("Result of graph coloring:")
        print(sorted(solution.items(), key=operator.itemgetter(0)))
    if check(solution, graph):
        print("Algorithm correct!")
    else:
        print("Something went wrong!")

def check(solution, graph):
    for edge in graph.edges():
        (vertex1, vertex2) = tuple(edge)
        if solution[vertex1] == solution[vertex2]:
            print(vertex1, vertex2)
            return False
    return True

def readFile(Lines):
    g = Graph()
    color = -1
    for line in Lines:
        if line.startswith("#"):
            continue
        elif color == -1:
            color = int(line.partition("=")[2])
        else:
            x = line.strip("\n").split(",")
            x[0] = int(x[0])
            x[1] = int(x[1])
            g.add_vertex(x[0])
            g.add_vertex(x[1])
            g.add_edge((x[0], x[1]))
    return g, color

if __name__ == "__main__":
    main()
