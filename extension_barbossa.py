"""
Like algo.py but with some improvements
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
    newGraph = digraph.copy()  # check differance between this and copy(g)
    for ind, _ in enumerate(w):
        if d[ind] == "0":
            newGraph.add_edge(w[ind], v)
        else:
            newGraph.add_edge(v, w[ind])
    return newGraph


def legal_assignments(digraph, w, partialAssig, index, legalAssig, digirth):
    first = False
    second = False
    legal = closure(digraph, partialAssig, w, digirth)
    if (
        index == len(w) and partialAssig == legal
    ):  # easy improvemnt is to not check only at bottom, and if good stop 0
        legalAssig.append(partialAssig)
        return
    if partialAssig[:index] == legal[:index]:
        legal_assignments(digraph, w, partialAssig, index + 1, legalAssig, digirth)
        first = True
    partialAssig = partialAssig[:index] + "1" + partialAssig[index + 1 :]
    legal = closure(digraph, partialAssig, w, digirth)
    if partialAssig[:index] == legal[:index]:
        legal_assignments(digraph, w, partialAssig, index + 1, legalAssig, digirth)
        second = True
    # print(first, second)


def acyclic(graph, index=0, digraph=DiGraph(), nAcyclicOrientations=0, digirth=0):
    if index == (graph.order()):
        # digraph.show()
#        print(f"({nAcyclicOrientations+1}) Acyclic orientation of G: {digraph.edges()}")
        return nAcyclicOrientations + 1
    neighbors = list(set(graph.neighbors(index)).intersection(digraph.vertices()))
    if neighbors == []:
        newDiGraph = digraph.copy()
        newDiGraph.add_vertex(index)
        nAcyclicOrientations = acyclic(graph, index + 1, newDiGraph, nAcyclicOrientations, digirth)
    else:
        w = neighbors  # [node for node in digraph.topological_sort() if node in neighbors]
        legalAssig = []
        legal_assignments(digraph, w, "0" * len(w), 0, legalAssig, digirth)
        for assignment in legalAssig:
            newDiGraph = extend(digraph, w, assignment, index)
            nAcyclicOrientations = acyclic(graph, index + 1, newDiGraph, nAcyclicOrientations, digirth)
    return nAcyclicOrientations


def compute_acyclic_orientations_extension(graph, digirth=Infinity):
    a = process_time_ns()
    nAcyclicOrientations = acyclic(graph, digirth=digirth)
    b = process_time_ns()
    print(
        f"Found {nAcyclicOrientations} of {graph.tutte_polynomial()(2,0)} acyclic orientations in {(b-a)/1000000000}s"
    )
