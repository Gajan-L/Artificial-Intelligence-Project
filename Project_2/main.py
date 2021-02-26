import graph as g
from search import backtrack


def main():
    f = open("input/gc_78317094521100.txt", "r")
    Lines = f.readlines()
    f.close()
    print("Reading files")
    color, node_list = readFile(Lines)
    print("CSP graph coloring.")
    csp = {}
    for k in node_list.keys():
        csp[k] = -1
    result = backtrack(csp, node_list, color)
    print("Result of CSP Graph Coloring: ")
    if result:
        print(result)
    else:
        print("No solution was found.")
    if check(csp, node_list):
        print("Algorithm correct!")
    else:
        print("Something went wrong!")



def check(csp, node_list):
    for i in range(len(node_list)):
        if node_list.get(i):
            node = node_list.get(i)
            for neighbor in node.neighbors:
                if csp[neighbor.index] == csp[node.index]:
                    print(neighbor.index, node.index)
                    return False
    return True


def readFile(Lines):
    node_list = {}
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
            n1 = g.Nodes(x[0], color) if x[0] not in node_list else node_list.get(x[0])
            n2 = g.Nodes(x[1], color) if x[1] not in node_list else node_list.get(x[1])
            node_list[x[0]] = n1
            node_list[x[1]] = n2
            if n2 not in n1.neighbors:
                n1.add_neighbor(n2)
            if n1 not in n2.neighbors:
                n2.add_neighbor(n1)
    return color, node_list


if __name__ == "__main__":
    main()