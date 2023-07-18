"""This file contains all the necessary parts to compute all digirth `d` orientations of a graph."""

from time import process_time_ns

VISITED = 1
OUTGOING_ASSIGNMENT = "1"
INCOMING_ASSIGNMENT = "0"


def compute_orientations_with_time(graph, digirth=Infinity):
    a = process_time_ns()
    orientations = compute_orientations(graph, digirth)
    b = process_time_ns()
    number_orientations = graph.tutte_polynomial()(2, 0) if digirth == Infinity else "?"
    print(
        f"Found {len(orientations)} of {number_orientations} {digirth}-digirth orientations in {(b-a)/999999999}s"
    )


def compute_orientations(graph, digirth=Infinity):
    if digirth < 3:
        digirth = 3
    orientations = []
    digraph = DiGraph()
    _compute_orientations_recursive(graph, orientations, 0, digraph, digirth)
    return orientations


def _compute_orientations_recursive(graph, orientations, node_to_add_id, digraph, digirth):
    if node_to_add_id == graph.order():
        orientations.append(digraph.edges(labels=False))
        return
    neighbors = _getAlreadyAddedNeighbors(graph, digraph, node_to_add_id)
    if not neighbors:
        newDiGraph = digraph.copy()
        newDiGraph.add_vertex(node_to_add_id)
        _compute_orientations_recursive(
            graph, orientations, node_to_add_id + 1, newDiGraph, digirth
        )
    else:
        compute_legal_assignments(digraph, neighbors, digirth, graph, orientations, node_to_add_id)


def _getAlreadyAddedNeighbors(graph, digraph, node_to_add_id):
    return list(set(graph.neighbors(node_to_add_id)).intersection(digraph.vertices()))


def compute_legal_assignments(digraph, neighbors, digirth, graph, orientations, node_to_add_id):
    legal_assignments = []
    initial_partial_assignment = INCOMING_ASSIGNMENT * len(neighbors)
    _compute_legal_assignments_recursive(
        digraph,
        neighbors,
        initial_partial_assignment,
        0,
        legal_assignments,
        digirth,
        graph,
        orientations,
        node_to_add_id,
    )
    return legal_assignments


def _compute_legal_assignments_recursive(
    digraph,
    neighbors,
    partial_assignment,
    partial_assignment_index,
    legal_assignments,
    digirth,
    graph,
    orientations,
    node_to_add_id,
):
    legal = closure(digraph, partial_assignment, neighbors, digirth)
    if partial_assignment_index == len(neighbors) and partial_assignment == legal:
        extended_digraph = extend(digraph, neighbors, partial_assignment, node_to_add_id)
        _compute_orientations_recursive(
            graph, orientations, node_to_add_id + 1, extended_digraph, digirth
        )
        return
    if partial_assignment[:partial_assignment_index] == legal[:partial_assignment_index]:
        _compute_legal_assignments_recursive(
            digraph,
            neighbors,
            partial_assignment,
            partial_assignment_index + 1,
            legal_assignments,
            digirth,
            graph,
            orientations,
            node_to_add_id,
        )
    partial_assignment = (
        partial_assignment[:partial_assignment_index]
        + "1"
        + partial_assignment[partial_assignment_index + 1 :]
    )
    legal = closure(digraph, partial_assignment, neighbors, digirth)
    if partial_assignment[:partial_assignment_index] == legal[:partial_assignment_index]:
        _compute_legal_assignments_recursive(
            digraph,
            neighbors,
            partial_assignment,
            partial_assignment_index + 1,
            legal_assignments,
            digirth,
            graph,
            orientations,
            node_to_add_id,
        )


def extend(digraph, w, d, v):
    newGraph = digraph.copy()
    for ind, _ in enumerate(w):
        if d[ind] == INCOMING_ASSIGNMENT:
            newGraph.add_edge(w[ind], v)
        else:
            newGraph.add_edge(v, w[ind])
    return newGraph


def closure(digraph, newD, w, digirth):
    tmpDigraph = digraph.copy()
    assignments = dict(zip(w, newD))
    neighbors_out = [
        node for node, direciton in assignments.items() if direciton == OUTGOING_ASSIGNMENT
    ]
    for node in neighbors_out:
        _visit(node, tmpDigraph, assignments, digirth - 3)
    return "".join(assignments.values())


def _visit(node, digraph, assignment, counter):
    if counter == 0:
        return
    if digraph.get_vertex(node) == VISITED:
        return
    if node in assignment:
        assignment[node] = OUTGOING_ASSIGNMENT
    digraph.set_vertex(node, VISITED)
    for descendant in digraph.neighbors_out(node):
        _visit(descendant, digraph, assignment, counter - 1)
