from time import process_time_ns


def closure(digraph, newD, w):
    vertices_and_in_edges = {}
    for vertex in digraph.vertices():
        vertices_and_in_edges[vertex] = len(digraph.neighbors_in(vertex))
    sources = set(digraph.sources())
    assignments = dict(zip(w, newD))
    transforming_vertices = {vertex for vertex, assignment in assignments.items() if assignment == "1"}
    while sources:
        source = sources.pop()
        neighbors_out = digraph.neighbors_out(source)
        for vertex in neighbors_out:
            vertices_and_in_edges[vertex] -= 1
            if source in transforming_vertices:
                if vertex in assignments.keys():
                    assignments[vertex] = 1
                transforming_vertices.add(vertex)
            if not vertices_and_in_edges[vertex]:
                sources.add(vertex)
    newNewD = "".join((str(value) for value in assignments.values()))
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


def acyclic_old(graph, index=0, digraph=DiGraph(), orientations=[]):
    if index == (graph.order()):
        #print(f"(One) Acyclic orientation of G: {digraph.edges()}")
        orientations.append(digraph.edges(labels=False))
        return 0
    neighbors = list(set(graph.neighbors(index)).intersection(digraph.vertices())) # this and w could be fusioned
    # furthermore, if I knew how to pass from G to DG in an meaningful way, maybe I could just use G, it all depends on top ordering
    if neighbors == []:
        newDiGraph = digraph.copy()
        newDiGraph.add_vertex(index)
        acyclic_old(
            graph, index + 1, newDiGraph, orientations
        )  # not simply add vertex, previous edges too!
    else:
        w = [node for node in digraph.topological_sort() if node in neighbors] # set intersection doesn't conserve order
        d = "0" * len(neighbors)
        last = False
        while not last:
            newDiGraph = extend(digraph, w, d, index)
            acyclic_old(
                graph, index + 1, newDiGraph, orientations
            )  # not simply add vertex, previous edges too!
            if d != "1" * len(neighbors):
                d = next_legal_assignment(digraph, w, d)
            else:
                last = True

def acyclic0_old(graph):
    a = process_time_ns()
    orientations = []
    acyclic_old(graph, orientations=orientations)
    b = process_time_ns()
    n_acyclic_orientations = graph.tutte_polynomial()(2, 0)
    print(f"Found {len(orientations)} of {n_acyclic_orientations} and computing algorithm took {(b-a)/1000000000}s")


# dummy tries
# star and disconnected, triangle, square

# TOASK
# is it necessay to order all graph topologically? I don't think so, I think just ordering using the sonds of W-node's is enough?
# try with star graph and disconnected: nice
# with triangle: not so nice

#triangle example
#  g = Graph([(0,1),(1,2),(2,0)])

# TODO
# use the tutte polynomial, as T_G(0,2) to check that there are as many acyclic orientations
# implement topological ordering in incrementing way, so that when I add node v_i 
# implrmrnt some data structure to save antecessors
