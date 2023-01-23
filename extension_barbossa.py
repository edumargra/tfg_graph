"""
Like algo.py but with some improvements
"""
from time import process_time_ns


def closure(digraph, newD, w):
    tmpDigraph = digraph.copy()
    sources = set(tmpDigraph.sources())
    assignments = dict(zip(w, newD))
    while sources:
        source = sources.pop()
        special_vertex = False
        if source in assignments and assignments[source] == "1":
            special_vertex = True
        if tmpDigraph.get_vertex(source) == "1":
            special_vertex = True
        if source in assignments and special_vertex:
            assignments[source] = "1"
        for node in tmpDigraph.neighbors_out(source):
            tmpDigraph.delete_edge(source, node)
            if not tmpDigraph.neighbors_in(node):
                sources.add(node)
            if special_vertex:
                tmpDigraph.set_vertex(node, "1")
    newNewD = "".join(assignments.values())
    return newNewD


def next_legal_assignment(digraph, w, d):
    zInd = d.rfind("0")
    newD = f"{d[:zInd]}1{'0'*(len(w)-(zInd+1))}"
    return closure(digraph, newD, w)


def extend(digraph, w, d, v):
    newGraph = digraph.copy()  # check differance between this and copy(g)
    for ind, _ in enumerate(w):
        if d[ind] == "0":
            newGraph.add_edge(w[ind], v)
        else:
            newGraph.add_edge(v, w[ind])
    return newGraph


def legal_assignments(digraph, w, partialAssig, index, legalAssig):
    first = False
    second = False
    legal = closure(digraph, partialAssig, w)
    if index == len(w) and partialAssig == legal: #easy improvemnt is to not check only at bottom, and if good stop 0
        legalAssig.append(partialAssig)
        return
    if partialAssig[:index] == legal[:index]:
        legal_assignments(digraph, w, partialAssig, index + 1, legalAssig)
        first = True
    partialAssig = partialAssig[:index] + "1" + partialAssig[index + 1:]
    legal = closure(digraph, partialAssig, w)
    if partialAssig[:index] == legal[:index]:
        legal_assignments(digraph, w, partialAssig, index + 1, legalAssig)
        second = True
    # print(first, second)


def acyclic(graph, index=0, digraph=DiGraph(), nAcyclicOrientations=0):
    if index == (graph.order()):
        # digraph.show()
        # print(f"({nAcyclicOrientations+1}) Acyclic orientation of G: {digraph.edges()}")
        return nAcyclicOrientations + 1
    neighbors = list(set(graph.neighbors(index)).intersection(digraph.vertices()))
    if neighbors == []:
        newDiGraph = digraph.copy()
        newDiGraph.add_vertex(index)
        nAcyclicOrientations = acyclic(graph, index + 1, newDiGraph, nAcyclicOrientations)
    else:
        w = neighbors#[node for node in digraph.topological_sort() if node in neighbors]
        legalAssig = []
        legal_assignments(digraph, w, "0" * len(w), 0, legalAssig)
        for assignment in legalAssig:
            newDiGraph = extend(digraph, w, assignment, index)
            nAcyclicOrientations = acyclic(graph, index + 1, newDiGraph, nAcyclicOrientations)
    return nAcyclicOrientations


def compute_acyclic_orientations_extension(graph):
    a = process_time_ns()
    nAcyclicOrientations = acyclic(graph)
    b = process_time_ns()
    print(
        f"Found {nAcyclicOrientations} of {graph.tutte_polynomial()(2,0)} acyclic orientations in {(b-a)/1000000000}s"
    )


# dummy tries
# star and disconnected, triangle, square

# TOASK
# is it necessay to order all graph topologically? I don't think so, I think just ordering using the sonds of W-node's is enough?
# try with star graph and disconnected: nice
# with triangle: not so nice

# triangle example
#  g = Graph([(0,1),(1,2),(2,0)])

# TODO
# use the tutte polynomial, as T_G(0,2) to check that there are as many acyclic orientations
# implement topological ordering in incrementing way, so that when I add node v_i
# implrmrnt some data structure to save antecessors
