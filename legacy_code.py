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
        if source in assignments and assignments[source] == '1':
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


def closure_next_assignment(digraph, w, d):
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


# def update_top_order(top_order, v, digraph, w=[], d=""):
#     new_top_order = top_order.copy()
#     first_out_idx = d.find("1")
#     if first_out_idx == -1:
#         new_top_order.append(v)
#         # print(new_top_order)
#         return new_top_order
#     last_fix_idx = new_top_order.index(w[first_out_idx])
#     for neighbour_idx in range(first_out_idx+1, len(w)):
#         if d[neighbour_idx] == "0":
#             new_top_order.remove(w[neighbour_idx])
#             new_top_order.insert(last_fix_idx, w[neighbour_idx])
#     # print(last_fix_idx, first_out_idx, len(w))
#     if first_out_idx == len(w)-1:
#         new_top_order.insert(last_fix_idx, v)
#     else:
#         new_top_order.insert(last_fix_idx+1, v)
#     print(new_top_order,digraph.topological_sort(), w, d)
#     return new_top_order


def acyclic(graph, index=0, digraph=DiGraph(), nAcyclicOrientations=0):
    if index == (graph.order()):
        # print(f"({nAcyclicOrientations+1}) Acyclic orientation of G: {digraph.edges()}")
        return nAcyclicOrientations + 1
    neighbors = list(set(graph.neighbors(index)).intersection(digraph.vertices()))
    if neighbors == []:
        newDiGraph = digraph.copy()
        newDiGraph.add_vertex(index)
        nAcyclicOrientations = acyclic(graph, index + 1, newDiGraph, nAcyclicOrientations)
    else:
        w = [node for node in digraph.topological_sort() if node in neighbors]
        d = "0" * len(neighbors)
        last = False
        while not last:
            newDiGraph = extend(digraph, w, d, index)
            # if index+1 == graph.order():
            nAcyclicOrientations = acyclic(graph, index + 1, newDiGraph, nAcyclicOrientations)
            if d != "1" * len(neighbors):
                d = closure_next_assignment(digraph, w, d)
            else:
                last = True
    return nAcyclicOrientations


def compute_acyclic_orientations(graph):
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
