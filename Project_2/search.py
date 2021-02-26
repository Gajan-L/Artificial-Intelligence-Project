import math

def backtrack(csp, node_list, color):
    if -1 not in csp.values():
        return csp
    node = nextNode(csp, node_list, color)
    backupNList = node_list.copy()
    avoid = []
    val = nextColor(node, avoid)
    while val != -1 and len(avoid) != len(node.domain): # while there are available values
        csp[node.index] = val
        if ac3(node, val, csp, node_list):
            result = backtrack(csp, node_list, color)
            if result:
                return result
        node_list= backupNList
        csp[node.index] = -1
        avoid.append(val)
        val = nextColor(node, avoid)
    return False

# choose the node that has the minimum remaining values
# choose the node with maximum neighbors if multiple nodes have same # of minimum remaining values


def nextNode(csp, node_list, color):
    mrv = color +1
    next = None
    for index, value in csp.items():
        if value == -1:
            candidate = node_list[index]
            if len(candidate.domain) < mrv:
                next = candidate
                mrv = len(candidate.domain)
            elif len(candidate.domain) == mrv and len(candidate.neighbors) > len(next.neighbors):
                next = candidate
    return next

# least constraint value
# choose the value if there's only one value left
# choose the value that has the least constraint on the remaining neighboring nodes
def nextColor(node, avoid):
    least_constraint = math.inf
    value = -1
    if len(node.domain) == 1:
        if node.domain[0] in avoid:
            return -1
        return node.domain[0]
    for i in node.domain:
        if i not in avoid:
            constraint = 0
            for neighbor in node.neighbors:
                if i in neighbor.domain:
                    constraint += 1
            if constraint < least_constraint:
                value = i
                least_constraint = constraint
    return value

# constraint propagation using ac3
# remove assigned color from neighboring nodes' domain
# assign the color to the node if there's only one color left in its domain
def ac3(node, val, csp,node_list):
    backupCsp = csp.copy()

    flag = []
    queue = []
    queue.append(node)
    while len(queue) != 0:
        cur = queue[0]
        val = csp[cur.index]
        queue.remove(cur)
        for neighbor in cur.neighbors:
            if csp[neighbor.index] == csp[cur.index] and csp[cur.index] != -1:
                csp = backupCsp
                return False
            elif csp[neighbor.index] == -1 and val in neighbor.domain:
                node_list[neighbor.index].domain.remove(val)
                flag.append(neighbor)
                if len(neighbor.domain) == 1:
                    if neighbor.domain[0] == csp[cur.index]:
                        csp = backupCsp
                        return False
                    else:
                        csp[neighbor.index] = neighbor.domain[0]
                        queue.append(neighbor)
                elif len(neighbor.domain) == 0 and csp[neighbor.index] == -1:
                    csp = backupCsp
                    return False
    return True
