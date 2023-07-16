"""This file contains all the necessary parts to compute all digirth
`d` orientations of a graph.
"""
from time import process_time_ns

VISITED = 1


def closure(digraph, newD, w, digirth):
    tmpDigraph = digraph.copy()
    assignments = dict(zip(w, newD))
    neighbors_out = [node for node, direciton in assignments.items() if direciton == "1"]
    for node in neighbors_out:
        _visit(node, tmpDigraph, assignments, digirth - 2)
    return "".join(assignments.values())


def _visit(node, digraph, assignment, counter):
    if counter == 0:
        return
    if digraph.get_vertex(node) == VISITED:
        return
    if node in assignment:
        assignment[node] = "1"
    digraph.set_vertex(node, VISITED)
    for descendant in digraph.neighbors_out(node):
        _visit(descendant, digraph, assignment, counter - 1)


def extend(digraph, w, d, v):
    newGraph = digraph.copy()
    for ind, _ in enumerate(w):
        if d[ind] == "0":
            newGraph.add_edge(w[ind], v)
        else:
            newGraph.add_edge(v, w[ind])
    return newGraph


def legal_assignments(digraph, w, partialAssig, index, legalAssig, digirth):
    legal = closure(digraph, partialAssig, w, digirth)
    if (
        index == len(w) and partialAssig == legal
    ):
        legalAssig.append(partialAssig)
        return
    if partialAssig[:index] == legal[:index]:
        legal_assignments(digraph, w, partialAssig, index + 1, legalAssig, digirth)
    partialAssig = partialAssig[:index] + "1" + partialAssig[index + 1 :]
    legal = closure(digraph, partialAssig, w, digirth)
    if partialAssig[:index] == legal[:index]:
        legal_assignments(digraph, w, partialAssig, index + 1, legalAssig, digirth)


def _getAlreadyAddedNeighbors(graph, digraph, node_to_add):
    return list(set(graph.neighbors(node_to_add)).intersection(digraph.vertices()))

def _compute_orientations_recursive(graph, orientations, id_node_to_add, digraph, digirth):
    if id_node_to_add == graph.order():
        orientations.append(digraph.edges(labels=False))
        return
    neighbors = _getAlreadyAddedNeighbors(graph, digraph, id_node_to_add)
    if not neighbors:
        newDiGraph = digraph.copy()
        newDiGraph.add_vertex(id_node_to_add)
        _compute_orientations_recursive(graph, orientations, id_node_to_add + 1, newDiGraph, digirth)
    else:
        legalAssig = []
        legal_assignments(digraph, neighbors, "0" * len(neighbors), 0, legalAssig, digirth)
        for assignment in legalAssig:
            newDiGraph = extend(digraph, neighbors, assignment, id_node_to_add)
            _compute_orientations_recursive(graph, orientations, id_node_to_add + 1, newDiGraph, digirth)


def compute_orientations(graph, digirth=Infinity):
    orientations = []
    digraph = DiGraph()
    _compute_orientations_recursive(graph, orientations, 0,
                                           digraph, digirth)
    return orientations


def compute_orientations_with_time(graph, digirth=Infinity):
    a = process_time_ns()
    orientations = compute_orientations(graph, digirth)
    b = process_time_ns()
    print(
        f"Found {len(orientations)} of {graph.tutte_polynomial()(2,0)} n{digirth} acyclic orientations in {(b-a)/1000000000}s"
    )
