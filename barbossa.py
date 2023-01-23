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


def acyclic_old(graph, index=0, digraph=DiGraph()):
    if index == (graph.order()):
        print(f"(One) Acyclic orientation of G: {digraph.edges()}")
        # import pdb
        # pdb.set_trace()
        # digraph.show()
        return 0
    neighbors = list(set(graph.neighbors(index)).intersection(digraph.vertices())) # this and w could be fusioned
    # furthermore, if I knew how to pass from G to DG in an meaningful way, maybe I could just use G, it all depends on top ordering
    if neighbors == []:
        newDiGraph = digraph.copy()
        newDiGraph.add_vertex(index)
        acyclic_old(
            graph, index + 1, newDiGraph
        )  # not simply add vertex, previous edges too!
    else:
        w = [node for node in digraph.topological_sort() if node in neighbors] # set intersection doesn't conserve order
        d = "0" * len(neighbors)
        last = False
        while not last:
            newDiGraph = extend(digraph, w, d, index)
            acyclic_old(
                graph, index + 1, newDiGraph
            )  # not simply add vertex, previous edges too!
            if d != "1" * len(neighbors):
                d = next_legal_assignment(digraph, w, d)
            else:
                last = True

def acyclic0_old(graph):
    a = process_time_ns()
    acyclic_old(graph)
    b = process_time_ns()
    print(f"Computing algorithm took {(b-a)/1000000000}s")
# def acyclic0(graph):
#     di = DiGraph()
#     acyclic(graph, digraph=di)


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