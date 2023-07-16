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


def compute_orientations(graph, orientations, index=0, digraph=DiGraph(), digirth=0):
    if index == (graph.order()):
        orientations.append(digraph.edges(labels=False))
        return
    neighbors = list(set(graph.neighbors(index)).intersection(digraph.vertices()))
    if neighbors == []:
        newDiGraph = digraph.copy()
        newDiGraph.add_vertex(index)
        acyclic_orientations(graph, orientations, index + 1, newDiGraph, digirth)
    else:
        w = neighbors
        legalAssig = []
        legal_assignments(digraph, w, "0" * len(w), 0, legalAssig, digirth)
        for assignment in legalAssig:
            newDiGraph = extend(digraph, w, assignment, index)
            acyclic_orientations(graph, orientations, index + 1, newDiGraph, digirth)
    return


def compute_orientations_with_time(graph, digirth=Infinity):
    a = process_time_ns()
    orientations = []
    compute_orientations(graph, orientations, digirth=digirth)
    b = process_time_ns()
    print(
        f"Found {len(orientations)} of {graph.tutte_polynomial()(2,0)} n{digirth} acyclic orientations in {(b-a)/1000000000}s"
    )
