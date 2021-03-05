from typing import Generic, TypeVar
from abc import ABC, abstractmethod
import math
import copy

V = TypeVar('V')  # variable type
D = TypeVar('D')  # domain type


# Base class for all constraints
class Constraint(Generic[V, D], ABC):
    # The variables that the constraint is between
    def __init__(self, variables):
        self.variables = variables
    @abstractmethod
    def satisfied(self, assignment):
        ...

# A constraint satisfaction problem consists of variables of type V
# that have ranges of values known as domains of type D and constraints
# that determine whether a particular variable's domain selection is valid

class CSP(Generic[V, D]):
    def __init__(self, variables, domains):
        self.variables = variables  # variables := list[V]
        self.domains = domains      # domains := dict[V, list[D]]
        self.constraints = {}       # constriants:= dict[V, list[Constraint[V, D]]]
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise LookupError("Every variable should have a domain assigned to it.")

    def add_constraint(self, constraint):
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("Variable in constraint not in CSP")
            else:
                self.constraints[variable].append(constraint)

# assignment := dict[V, D]
# Check if the value assignment is consistent by checking all constraints
# for the given variable against it
    def consistent(self, variable: V, assignment):
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True

    def neighbors(self, variable):
        neighbors = []
        for constraint in self.constraints.values():
            for i in range(len(constraint)):
                (variable1, variable2) = constraint[i].variables
                if variable1 == variable and variable2 not in neighbors:
                    neighbors.append(variable2)
                if variable2 == variable and variable1 not in neighbors:
                    neighbors.append(variable1)
        return neighbors


def backtracking_search(csp, assignment, domains):
    # assignment is complete if every variable is assigned (our base case)
    if len(assignment) == len(csp.variables):
        return assignment
    backupdomain = copy.deepcopy(domains)
    next: V = nextVariable(csp, assignment,domains)
    valueOrder = orderDomainValues(csp, next, domains)
    for value in valueOrder:
        assignment[next] = value
        if csp.consistent(next, assignment):
            # if we're still consistent, we recurse (continue)
            domains[next] = [value]
            for neighbor in csp.neighbors(next):
                if value in domains[neighbor]:
                    domains[neighbor].remove(value)
            if ac3(csp, domains):
            # we use ac3 for constraint propation
                result = backtracking_search(csp, assignment, domains)
                # if we didn't find the result, we will end up backtracking
                if result is not None:
                    return result
            domains = backupdomain
            domains[next].remove(value)
            del assignment[next]
    return None

# This function choose the next variable according to MRV heuristic
# break ties by selecting the variable that is involved in more constraints
def nextVariable(csp, assignment, domains):
    mrv = math.inf
    for v in csp.variables:
        if len(domains.get(v)) < mrv and assignment.get(v) == None:
            next = v
            mrv = len(domains.get(v))
        if len(domains.get(v)) == mrv and assignment.get(v) == None and len(csp.constraints.get(v)) > len(csp.constraints.get(next)):
            next = v
    return next

# This function orders the domain values of the variable according to LCV heuristic
def orderDomainValues(csp, variable, domains):
    order = []
    color = []
    for value in domains[variable]:
        count = 0
        for neighbor in csp.neighbors(variable):
            if value in domains[neighbor]:
                count += 1
        order.append([value, count])
    o = sorted(order, key=lambda x: x[1])
    color = [item[0] for item in o]
    return color

def ac3(csp, domains):
    queue = []
    for variable in csp.variables:
        for neighbor in csp.neighbors(variable):
            if (variable,neighbor) not in queue and (neighbor,variable) not in queue:
                queue.append((variable, neighbor))
    def revise(xi, xj):
        removed = False
        for value in domains.get(xi):
            if len(domains.get(xj)) == 1 and value == domains.get(xj)[0]:
                domains.get(xi).remove(value)
                removed = True
        return removed

    while(len(queue)!=0):
        (xi, xj) = queue.pop(0)
        if revise(xi, xj):
            if len(domains.get(xi)) == 0:
                return False
            for xk in csp.neighbors(xi):
                if xk != xj:
                    queue.append((xk, xi))
    return True

