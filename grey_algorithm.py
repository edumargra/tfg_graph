from time import process_time_ns


def compute_orientations_grey_algorithm(graph, digirth=0):
    a = process_time_ns()
    nOrientations = grey_algorithm(graph, digirth=digirth)
    b = process_time_ns()
    print(
        f"Found {nOrientations} of {graph.tutte_polynomial()(2,0)} acyclic orientations in {(b-a)/1000000000}s"
    )

def grey_algorithm(graph, digirth):
    """ TODO: you can make this algorithm recursive."""
    digraph = DiGraph()
    for edge in graph.edges():
        u, v, _ = edge
        digraph.add_edge(u, v)
    nOrientations = 0
    for edge in graph.edges():
        print(digraph.girth())
        if digraph.girth() >= digirth:
            nOrientations += 1
        u, v, _ = edge
        digraph.delete_edge(u, v)
        digraph.add_edge(v, u)
    return nOrientations
